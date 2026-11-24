#!/usr/bin/env python3
"""Compare the name and positioning sentence across every profile in facts.json.

Usage:
  python3 consistency.py facts.json [--md out.md]

For each profile, fill `name_shown` and `bio` with exactly what the profile shows
(copy, do not paraphrase). The script reports whether the name matches the canonical
name or an alias, how close the bio is to the positioning sentence, whether the bio
names the category, and whether the profile links back to the website.
"""
import argparse
import difflib
import json
import re
import sys
import unicodedata
from urllib.parse import urlparse


def norm(s):
    s = unicodedata.normalize("NFC", s or "")
    return re.sub(r"\s+", " ", s).strip().casefold()


def words(s):
    return re.findall(r"\w+", norm(s))


def coverage(sentence, bio):
    """Share of the sentence's words that appear in the bio in the same order.
    Extra text in the bio does not lower it; a rewritten sentence does."""
    sw, bw = words(sentence), words(bio)
    if not sw or not bw:
        return 0.0
    m = difflib.SequenceMatcher(None, sw, bw, autojunk=False)
    return sum(b.size for b in m.get_matching_blocks()) / len(sw)


def host_of(url):
    u = url if "://" in url else "https://" + url
    h = (urlparse(u).hostname or "").lower()
    return h[4:] if h.startswith("www.") else h


def mentions_host(text, host):
    """True when text holds a link or bare domain whose host is `host` or a subdomain of it."""
    for m in re.finditer(r"(?:https?://)?((?:[\w-]+\.)+[a-z]{2,})", (text or "").lower()):
        h = m.group(1)
        h = h[4:] if h.startswith("www.") else h
        if h == host or h.endswith("." + host):
            return True
    return False


def name_status(shown, name, aliases):
    if not shown:
        return "missing"
    exact = lambda s: re.sub(r"\s+", " ", unicodedata.normalize("NFC", s or "")).strip()
    if exact(shown) == exact(name):
        return "exact"
    if any(exact(shown) == exact(x) for x in aliases):
        return "alias"
    n = norm(shown)
    if n == norm(name) or any(n == norm(x) for x in aliases):
        return "case differs"
    # Same letters but different accents is still a mismatch for an entity.
    strip = lambda s: "".join(c for c in unicodedata.normalize("NFD", norm(s)) if unicodedata.category(c) != "Mn")
    if strip(shown) == strip(name):
        return "accents differ"
    return "differs"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("facts")
    ap.add_argument("--md")
    a = ap.parse_args()

    with open(a.facts, encoding="utf-8") as f:
        facts = json.load(f)
    s = facts["subject"]
    name, aliases = s["name"], s.get("aliases", [])
    one, cat = s.get("one_liner", ""), s.get("category", "")
    site = host_of(s.get("website") or "")

    rows, problems = [], 0
    for p in facts.get("profiles", []):
        ns = name_status(p.get("name_shown", ""), name, aliases)
        bio = p.get("bio", "")
        cov = coverage(one, bio)
        has_cat = bool(cat) and norm(cat) in norm(bio)
        links = p.get("links_to_site")
        if links is None:
            links = bool(site) and (mentions_host(bio, site) or mentions_host(p.get("website_field", ""), site))
        ok = ns in ("exact", "alias") and has_cat and cov >= 0.9 and links
        problems += 0 if ok else 1
        rows.append((p.get("platform", "?"), p.get("url", ""), ns, f"{cov:.0%}", "yes" if has_cat else "NO",
                     "yes" if links else "NO", "ok" if ok else "FIX"))

    L = [f"# Profile consistency: {name}", "",
         f"Canonical sentence: \"{one}\"", f"Category phrase: \"{cat}\"", "",
         "| Platform | URL | Name | Sentence covered in bio | Category in bio | Links to site | Status |",
         "|---|---|---|---|---|---|---|"]
    L += ["| " + " | ".join(r) + " |" for r in rows]
    L += ["", f"{problems} of {len(rows)} profiles need a fix. Target: name exact, category named, "
          "bio contains at least 90% of the canonical sentence in order, link to the website."]
    md = "\n".join(L)
    if a.md:
        with open(a.md, "w", encoding="utf-8") as f:
            f.write(md + "\n")
    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
