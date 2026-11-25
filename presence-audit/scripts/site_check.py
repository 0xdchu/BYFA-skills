#!/usr/bin/env python3
"""Check what an AI crawler sees on a website, without running JavaScript.

Usage:
  python3 site_check.py https://example.com [--name "Example Dental"]
      [--one-liner "Example Dental is ..."] [--page-pattern about=REGEX ...]
      [--json out.json] [--md out.md]

Standard library only. Reads the page the way the OpenAI, Anthropic and Perplexity
crawlers do (raw HTML, no JavaScript), then reports: visible text, title and
description, JSON-LD entity markup and sameAs links, robots.txt rules per AI and
search bot (Google's matching rules: wildcards, longest match wins), llms.txt, and
links to about, pricing, contact and comparison pages.
"""
import argparse
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.request
from html.parser import HTMLParser
from urllib.parse import quote, urljoin, urlparse, urlsplit, urlunsplit

UA = "Mozilla/5.0 (compatible; presence-audit/1.0; +https://github.com/0xdchu/BYFA-skills)"
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
    ("Googlebot", "search", "Google Search, AI Overviews, AI Mode, Gemini"),
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
# Entity-like schema.org types. Any LocalBusiness or Organization subtype not listed
# still counts when the node has both a name and sameAs.
ENTITY_TYPES = {
    "Organization", "Corporation", "LocalBusiness", "Person", "Brand", "OnlineBusiness",
    "ProfessionalService", "MedicalBusiness", "MedicalOrganization", "Dentist", "Physician",
    "MedicalClinic", "Hospital", "Store", "Restaurant", "LegalService", "Attorney",
    "FinancialService", "RealEstateAgent", "HomeAndConstructionBusiness", "AutoRepair",
    "BeautySalon", "HealthAndBeautyBusiness", "EducationalOrganization", "NGO",
    "SportsOrganization", "NewsMediaOrganization", "TravelAgency", "Hotel",
    "LodgingBusiness", "FoodEstablishment", "SoftwareApplication", "WebApplication",
    "MobileApplication", "Product", "Service",
}


def norm(s):
    s = unicodedata.normalize("NFC", s or "")
    return re.sub(r"\s+", " ", s).strip().casefold()


def iri_safe(url):
    """Percent-encode non-ASCII paths and IDNA-encode hosts so urllib can send them."""
    p = urlsplit(url)
    host = p.hostname.encode("idna").decode("ascii") if p.hostname else ""
    netloc = host + (f":{p.port}" if p.port else "")
    return urlunsplit((p.scheme, netloc, quote(p.path, safe="/%:@!$&'()*+,;=-._~"),
                       quote(p.query, safe="=&%+/?:@,;-._~"), ""))


def fetch(url):
    """Return (status, final_url, text, content_type, error, kind).
    kind: None ok; "http" server answered with an error; "network"; "script"."""
    try:
        req = urllib.request.Request(iri_safe(url), headers={"User-Agent": UA, "Accept": "text/html,*/*"})
    except Exception as e:
        return None, url, "", "", f"{type(e).__name__}: {e}", "script"
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            body = r.read(5_000_000)
            charset = r.headers.get_content_charset() or "utf-8"
            try:
                text = body.decode(charset, errors="replace")
            except LookupError:
                text = body.decode("utf-8", errors="replace")
            return r.status, r.geturl(), text, r.headers.get_content_type(), None, None
    except urllib.error.HTTPError as e:
        return e.code, url, "", "", f"HTTP {e.code}", "http"
    except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
        return None, url, "", "", f"{type(e).__name__}: {e}", "network"
    except Exception as e:
        return None, url, "", "", f"{type(e).__name__}: {e}", "script"


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
            self.lang = a.get("lang", "") or ""
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
                self.meta[key] = a.get("content", "") or ""
        elif tag == "link" and (a.get("rel") or "").lower() == "canonical":
            self.meta["canonical"] = a.get("href", "") or ""
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


def type_names(t):
    items = t if isinstance(t, list) else [t]
    out = []
    for x in items:
        if isinstance(x, str) and x:
            out.append(re.split(r"[/#:]", x.rstrip("/"))[-1])  # full IRI -> last segment
    return out


def walk_ld(node, out):
    """Collect entity-like nodes anywhere in the JSON-LD tree (graphs, nested publishers)."""
    if isinstance(node, list):
        for n in node:
            walk_ld(n, out)
        return
    if not isinstance(node, dict):
        return
    types = type_names(node.get("@type"))
    same = node.get("sameAs") or []
    same = [s for s in (same if isinstance(same, list) else [same]) if isinstance(s, str)]
    if any(x in ENTITY_TYPES for x in types) or (types and node.get("name") and same):
        out.append({
            "type": types,
            "name": node.get("name", "") if isinstance(node.get("name"), str) else "",
            "sameAs": same,
            "has_logo": bool(node.get("logo") or node.get("image")),
            "has_founder": bool(node.get("founder") or node.get("founders") or node.get("worksFor")),
            "has_address": bool(node.get("address")),
            "has_description": bool(node.get("description")),
        })
    for k, v in node.items():
        if k != "@type":
            walk_ld(v, out)


# ---- robots.txt, following Google's documented rules (RFC 9309 plus wildcards) ----

def parse_robots(text):
    groups, cur, in_rules = [], None, False
    for line in text.lstrip("\ufeff").splitlines():
        line = line.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k, v = k.strip().lower(), v.strip()
        if k == "user-agent":
            if cur is None or in_rules:
                cur = {"agents": [], "rules": []}
                groups.append(cur)
                in_rules = False
            cur["agents"].append(v.lower())
        elif k in ("allow", "disallow") and cur is not None:
            in_rules = True
            if v:
                cur["rules"].append((k == "allow", v))
    return groups


def rules_for(groups, bot):
    b = bot.lower()
    best, rules = -1, []
    for g in groups:
        for a in g["agents"]:
            if a != "*" and b.startswith(a):
                if len(a) > best:
                    best, rules = len(a), list(g["rules"])
                elif len(a) == best:
                    rules += g["rules"]
    if best >= 0:
        return rules
    return [r for g in groups if "*" in g["agents"] for r in g["rules"]]


def pattern_re(p):
    end = p.endswith("$")
    body = re.escape(p[:-1] if end else p).replace(r"\*", ".*")
    return re.compile("^" + body + ("$" if end else ""))


def allowed(rules, path):
    best_len, verdict = -1, True
    for allow, pat in rules:
        if pattern_re(pat).match(path):
            L = len(pat)
            if L > best_len or (L == best_len and allow):
                best_len, verdict = L, allow
    return verdict


def check_robots(base, path):
    status, _, body, _, err, kind = fetch(urljoin(base, "/robots.txt"))
    if status is not None and 400 <= status < 500:
        note = f"robots.txt HTTP {status}: treated as no rules (everything allowed)"
        return {"status": status, "note": note, "bots": [
            {"bot": b, "kind": k, "what": w, "allowed": True} for b, k, w in BOTS]}
    if status is None or status >= 500:
        note = (f"robots.txt unreachable ({err}): Google treats a server error as 'disallow everything'; "
                "other crawlers may too. Fix the robots.txt response first.")
        return {"status": status, "note": note, "bots": [
            {"bot": b, "kind": k, "what": w, "allowed": None} for b, k, w in BOTS]}
    groups = parse_robots(body)
    return {"status": status, "note": "", "bots": [
        {"bot": b, "kind": k, "what": w, "allowed": allowed(rules_for(groups, b), path or "/")}
        for b, k, w in BOTS]}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--name", default="")
    ap.add_argument("--one-liner", default="")
    ap.add_argument("--page-pattern", action="append", default=[],
                    help="extra page pattern KIND=REGEX on the URL path, e.g. about=/ueber-uns (repeatable)")
    ap.add_argument("--json")
    ap.add_argument("--md")
    args = ap.parse_args()

    patterns = dict(PAGE_PATTERNS)
    for pp in args.page_pattern:
        k, _, rx = pp.partition("=")
        patterns[k] = f"(?:{patterns[k]})|(?:{rx})" if k in patterns else rx

    url = args.url if "://" in args.url else "https://" + args.url
    status, final, html, ctype, err, kind = fetch(url)
    p0 = urlsplit(url)
    robots = check_robots(f"{p0.scheme}://{p0.netloc}", (p0.path or "/") + (f"?{p0.query}" if p0.query else ""))
    res = {"url": url, "final_url": final, "status": status, "error": err, "error_kind": kind, "robots": robots}
    if not html:
        if status == 200:
            err, kind = "HTTP 200 with an empty body", "http"
            res.update(error=err, error_kind=kind)
        res["verdict"] = "page not read"
        out(res, args)
        return 1

    p = Page()
    p.feed(html)
    text = re.sub(r"\s+", " ", " ".join(p.text)).strip()
    words = len(text.split())
    ntext = norm(text)
    entities, ld_errors = [], 0
    for raw in p.jsonld:
        try:
            walk_ld(json.loads(raw), entities)
        except (json.JSONDecodeError, ValueError):
            ld_errors += 1

    host = urlparse(final).netloc
    pages = {k: [] for k in patterns}
    for href in p.links:
        full = urljoin(final, href)
        u = urlparse(full)
        if u.netloc != host:
            continue
        for k, pat in patterns.items():
            if re.search(pat, u.path.lower()) and full not in pages[k]:
                pages[k].append(full)

    l_status, _, l_body, l_type, _, _ = fetch(urljoin(final, "/llms.txt"))
    llms = l_status == 200 and l_type != "text/html" and not l_body.lstrip().lower().startswith(("<!doctype", "<html"))

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
        "llms_txt": llms,
        "text_sample": text[:400],
    })
    out(res, args)
    return 0


def yn(v):
    if v is None:
        return "not checked (pass --name / --one-liner)"
    return "yes" if v else "NO"


def cell(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def robots_md(r):
    L = ["## robots.txt by bot", ""]
    if r["note"]:
        L += [r["note"], ""]
    L += ["| Bot | Kind | Used for | Allowed on this URL |", "|---|---|---|---|"]
    for b in r["bots"]:
        a = "unknown" if b["allowed"] is None else yn(b["allowed"])
        L.append(f"| {b['bot']} | {b['kind']} | {b['what']} | {a} |")
    return L


def to_md(r):
    L = [f"# Site check: {r['url']}", ""]
    if r.get("verdict") == "page not read":
        if r["error"] == "HTTP 200 with an empty body":
            L += ["The page returned 200 with an empty body. AI crawlers would read nothing either; "
                  "check the page in a browser and the server's response to non-browser clients."]
        elif r["error_kind"] == "http":
            L += [f"The server answered {r['error']} to this script. That does not prove AI crawlers are refused: "
                  "many sites block unknown user agents but allow named crawlers. Read the robots.txt table below, "
                  "then check the page in a browser or ask an assistant with web search to read the URL."]
        elif r["error_kind"] == "network":
            L += [f"Could not connect: {r['error']}. Check the URL and DNS, then rerun."]
        else:
            L += [f"The script failed on this URL ({r['error']}). This is a script problem, not a finding about the site."]
        return "\n".join(L + [""] + robots_md(r["robots"]))
    blocked = [b for b in r["robots"]["bots"] if b["kind"] == "search" and b["allowed"] is False]
    unknown = r["robots"]["bots"][0]["allowed"] is None
    L += ["| Check | Result | Why it matters |", "|---|---|---|",
          f"| HTTP status | {r['status']} (final URL {cell(r['final_url'])}) | Bots only read pages that return 200 |",
          f"| Words readable without JavaScript | {r['visible_words_without_js']} | The OpenAI, Anthropic and Perplexity crawlers tested by Vercel (Dec 2024) do not run JavaScript; Googlebot and Applebot do |",
          f"| Looks client-rendered | {'YES, fix first' if r['likely_client_rendered'] else 'no'} | An empty shell gives ChatGPT, Claude and Perplexity nothing to read |",
          f"| Name in page text / title | {yn(r['name_in_html'])} / {yn(r['name_in_title'])} | The entity must be named in plain text |",
          f"| Positioning sentence in page text | {yn(r['one_liner_in_html'])} | The same sentence everywhere is what AI repeats |",
          f"| Title | {cell(r['title'][:90]) or 'MISSING'} | |",
          f"| Meta description | {cell((r['meta'].get('description') or 'MISSING')[:120])} | |",
          f"| html lang | {r['lang'] or 'MISSING'} | |",
          f"| JSON-LD blocks (parse errors) | {r['jsonld_blocks']} ({r['jsonld_parse_errors']}) | |",
          f"| Entity markup | {cell(', '.join('/'.join(e['type']) for e in r['entities'])) or 'NONE'} | Organization or Person ties the profiles together |",
          f"| sameAs links | {sum(len(e['sameAs']) for e in r['entities'])} | Each social and directory profile should be listed |",
          "| Pages linked from this page | " + ", ".join(f"{k} {len(v)}" for k, v in r["pages"].items()) +
          " | Pages that answer the sub-questions AI asks |",
          f"| llms.txt | {'present' if r['llms_txt'] else 'absent'} | No evidence major assistants use it; informational only |",
          f"| Search bots blocked by robots.txt | {'unknown, see note' if unknown else ', '.join(b['bot'] for b in blocked) or 'none'} | A blocked search bot cannot cite the site |",
          ""]
    L += robots_md(r["robots"])
    if r["entities"]:
        L += ["", "## Entity markup found", ""]
        for e in r["entities"]:
            L.append(f"- {'/'.join(e['type'])} \"{e['name']}\": sameAs {len(e['sameAs'])}, logo {yn(e['has_logo'])}, "
                     f"founder or employer {yn(e['has_founder'])}, address {yn(e['has_address'])}, "
                     f"description {yn(e['has_description'])}")
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
