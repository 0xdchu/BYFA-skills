#!/usr/bin/env python3
"""Check what an AI crawler sees on a website, without running JavaScript.

Usage:
  python3 site_check.py https://example.com [--name "Example Dental"]
      [--one-liner "Example Dental is ..."] [--json out.json] [--md out.md]

Standard library only. Reads the page the way AI search bots do (raw HTML, no JS),
then reports: visible text, title and description, JSON-LD entity markup and sameAs
links, robots.txt rules for AI and search bots, llms.txt, and links to about, pricing
and comparison pages.
"""
import argparse
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.request
import urllib.robotparser
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

UA = "Mozilla/5.0 (compatible; presence-audit/1.0; +https://github.com/0xdonniechu/BYFA-skills)"
TIMEOUT = 20

# kind: "search" bots fetch pages to answer and cite; "training" bots collect training data.
# Blocking a search bot means that assistant cannot read or cite the page.
BOTS = [
    ("OAI-SearchBot", "search", "ChatGPT search"),
    ("ChatGPT-User", "search", "ChatGPT, page opened for a user"),
    ("GPTBot", "training", "OpenAI training"),
    ("Claude-SearchBot", "search", "Claude search"),
    ("Claude-User", "search", "Claude, page opened for a user"),
    ("ClaudeBot", "training", "Anthropic training"),
    ("PerplexityBot", "search", "Perplexity search"),
    ("Perplexity-User", "search", "Perplexity, page opened for a user"),
    ("Googlebot", "search", "Google Search, AI Overviews, AI Mode"),
    ("Google-Extended", "training", "Gemini training and grounding opt-out"),
    ("Bingbot", "search", "Bing, Copilot, and ChatGPT search partner index"),
    ("Applebot-Extended", "training", "Apple training"),
]

PAGE_PATTERNS = {
    "about": r"(^|/)(about|about-us|company|our-story|team|who-we-are)(/|$|\.)",
    "pricing": r"(^|/)(pricing|prices|plans|price)(/|$|\.)",
    "contact": r"(^|/)(contact|contact-us)(/|$|\.)",
    "comparison": r"(-vs-|/vs/|/compare|/alternatives?)",
}
ENTITY_TYPES = {"Organization", "Corporation", "LocalBusiness", "Person", "Brand",
                "ProfessionalService", "MedicalBusiness", "Store", "OnlineBusiness",
                "NGO", "EducationalOrganization", "SoftwareApplication", "Product"}


def norm(s):
    s = unicodedata.normalize("NFC", s or "")
    return re.sub(r"\s+", " ", s).strip().casefold()


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            body = r.read(5_000_000)
            charset = r.headers.get_content_charset() or "utf-8"
            return r.status, r.geturl(), body.decode(charset, errors="replace"), None
    except urllib.error.HTTPError as e:
        return e.code, url, "", f"HTTP {e.code}"
    except Exception as e:  # network, TLS, timeout
        return None, url, "", f"{type(e).__name__}: {e}"


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text, self.links, self.jsonld, self.meta = [], [], [], {}
        self.title, self.lang, self.scripts = "", "", 0
        self._skip = 0
        self._in_title = False
        self._in_ld = False
        self._ld_buf = []
        self.root_ids = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang", "")
        if tag == "script":
            self.scripts += 1
            if (a.get("type") or "").lower() == "application/ld+json":
                self._in_ld, self._ld_buf = True, []
            else:
                self._skip += 1
        elif tag in ("style", "template", "svg"):
            self._skip += 1
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            key = (a.get("name") or a.get("property") or "").lower()
            if key in ("description", "og:title", "og:description", "og:site_name", "robots"):
                self.meta[key] = a.get("content", "")
        elif tag == "link" and (a.get("rel") or "").lower() == "canonical":
            self.meta["canonical"] = a.get("href", "")
        elif tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if a.get("id") in ("root", "__next", "app", "__nuxt", "svelte"):
            self.root_ids.append(a.get("id"))

    def handle_endtag(self, tag):
        if tag == "script":
            if self._in_ld:
                self.jsonld.append("".join(self._ld_buf))
                self._in_ld = False
            elif self._skip:
                self._skip -= 1
        elif tag in ("style", "template", "svg") and self._skip:
            self._skip -= 1
        elif tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_ld:
            self._ld_buf.append(data)
        elif self._in_title:
            self.title += data
        elif not self._skip:
            self.text.append(data)


def walk_ld(node, out):
    if isinstance(node, list):
        for n in node:
            walk_ld(n, out)
    elif isinstance(node, dict):
        if "@graph" in node:
            walk_ld(node["@graph"], out)
        t = node.get("@type")
        types = t if isinstance(t, list) else [t] if t else []
        if any(x in ENTITY_TYPES for x in types):
            same = node.get("sameAs") or []
            out.append({
                "type": types,
                "name": node.get("name", ""),
                "sameAs": same if isinstance(same, list) else [same],
                "has_logo": bool(node.get("logo") or node.get("image")),
                "has_founder": bool(node.get("founder") or node.get("founders")),
                "has_address": bool(node.get("address")),
                "has_description": bool(node.get("description")),
            })


def check_robots(base, path):
    rp = urllib.robotparser.RobotFileParser()
    status, _, body, err = fetch(urljoin(base, "/robots.txt"))
    if status is None or status >= 400:
        return {"status": status, "error": err, "bots": [
            {"bot": b, "kind": k, "what": w, "allowed": True, "note": "no robots.txt, allowed by default"}
            for b, k, w in BOTS]}
    rp.parse(body.splitlines())
    bots = []
    for b, k, w in BOTS:
        bots.append({"bot": b, "kind": k, "what": w,
                     "allowed": rp.can_fetch(b, urljoin(base, path or "/"))})
    return {"status": status, "error": None, "bots": bots}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--name", default="")
    ap.add_argument("--one-liner", default="")
    ap.add_argument("--json")
    ap.add_argument("--md")
    args = ap.parse_args()

    url = args.url if "://" in args.url else "https://" + args.url
    status, final, html, err = fetch(url)
    res = {"url": url, "final_url": final, "status": status, "error": err}
    if not html:
        res["verdict"] = "page not readable"
        out(res, args)
        return 1

    p = Page()
    p.feed(html)
    text = re.sub(r"\s+", " ", " ".join(p.text)).strip()
    words = len(text.split())
    ntext = norm(text)
    entities = []
    ld_errors = 0
    for raw in p.jsonld:
        try:
            walk_ld(json.loads(raw), entities)
        except json.JSONDecodeError:
            ld_errors += 1

    host = urlparse(final).netloc
    pages = {k: [] for k in PAGE_PATTERNS}
    for href in p.links:
        full = urljoin(final, href)
        u = urlparse(full)
        if u.netloc != host:
            continue
        for k, pat in PAGE_PATTERNS.items():
            if re.search(pat, u.path.lower()) and full not in pages[k]:
                pages[k].append(full)

    llms_status, _, _, _ = fetch(urljoin(final, "/llms.txt"))
    robots = check_robots(final, urlparse(final).path)

    res.update({
        "lang": p.lang,
        "title": p.title.strip(),
        "meta": p.meta,
        "visible_words_without_js": words,
        "script_tags": p.scripts,
        "spa_root_ids": p.root_ids,
        "likely_client_rendered": words < 150 and (p.scripts >= 5 or bool(p.root_ids)),
        "name_in_html": (norm(args.name) in ntext) if args.name else None,
        "name_in_title": (norm(args.name) in norm(p.title)) if args.name else None,
        "one_liner_in_html": (norm(args.one_liner) in ntext) if args.one_liner else None,
        "jsonld_blocks": len(p.jsonld),
        "jsonld_parse_errors": ld_errors,
        "entities": entities,
        "pages": pages,
        "llms_txt": llms_status == 200,
        "robots": robots,
        "text_sample": text[:400],
    })
    out(res, args)
    return 0


def yn(v):
    if v is None:
        return "not checked (pass --name / --one-liner)"
    return "yes" if v else "NO"


def to_md(r):
    L = [f"# Site check: {r['url']}", ""]
    if r.get("verdict") == "page not readable":
        L += [f"Page not readable: {r.get('error') or r.get('status')}. "
              "AI crawlers likely cannot read it either; check the URL in a browser and retry."]
        return "\n".join(L)
    blocked = [b for b in r["robots"]["bots"] if b["kind"] == "search" and not b["allowed"]]
    L += ["| Check | Result | Why it matters |", "|---|---|---|",
          f"| HTTP status | {r['status']} (final URL {r['final_url']}) | Bots only read pages that return 200 |",
          f"| Words readable without JavaScript | {r['visible_words_without_js']} | AI crawlers tested by Vercel (Dec 2024) do not run JavaScript |",
          f"| Looks client-rendered | {'YES, fix first' if r['likely_client_rendered'] else 'no'} | An empty shell gives AI nothing to read |",
          f"| Name in page text / title | {yn(r['name_in_html'])} / {yn(r['name_in_title'])} | The entity must be named in plain text |",
          f"| Positioning sentence in page text | {yn(r['one_liner_in_html'])} | The same sentence everywhere is what AI repeats |",
          f"| Title | {r['title'][:90] or 'MISSING'} | |",
          f"| Meta description | {(r['meta'].get('description') or 'MISSING')[:120]} | |",
          f"| html lang | {r['lang'] or 'MISSING'} | |",
          f"| JSON-LD blocks (parse errors) | {r['jsonld_blocks']} ({r['jsonld_parse_errors']}) | |",
          f"| Entity markup | {', '.join('/'.join(e['type']) for e in r['entities']) or 'NONE'} | Organization or Person ties the profiles together |",
          f"| sameAs links | {sum(len(e['sameAs']) for e in r['entities'])} | Each social and directory profile should be listed |",
          f"| About / pricing / contact / comparison pages linked | "
          f"{len(r['pages']['about'])} / {len(r['pages']['pricing'])} / {len(r['pages']['contact'])} / {len(r['pages']['comparison'])} | "
          "Pages that answer the sub-questions AI asks |",
          f"| llms.txt | {'present' if r['llms_txt'] else 'absent'} | No evidence major assistants use it; informational only |",
          f"| Search bots blocked by robots.txt | {', '.join(b['bot'] for b in blocked) or 'none'} | A blocked search bot cannot cite the site |",
          ""]
    L += ["## robots.txt by bot", "", "| Bot | Kind | Used for | Allowed |", "|---|---|---|---|"]
    for b in r["robots"]["bots"]:
        L.append(f"| {b['bot']} | {b['kind']} | {b['what']} | {yn(b['allowed'])} |")
    if r["entities"]:
        L += ["", "## Entity markup found", ""]
        for e in r["entities"]:
            L.append(f"- {'/'.join(e['type'])} \"{e['name']}\": sameAs {len(e['sameAs'])}, logo {yn(e['has_logo'])}, "
                     f"founder {yn(e['has_founder'])}, address {yn(e['has_address'])}, description {yn(e['has_description'])}")
            for s in e["sameAs"]:
                L.append(f"  - {s}")
    L += ["", "## First 400 characters a bot reads", "", "> " + (r["text_sample"] or "(nothing)")]
    return "\n".join(L)


def out(res, args):
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=2)
    md = to_md(res)
    if args.md:
        with open(args.md, "w", encoding="utf-8") as f:
            f.write(md + "\n")
    print(md)


if __name__ == "__main__":
    sys.exit(main())
