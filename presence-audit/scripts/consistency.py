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


def norm(s):
    s = unicodedata.normalize("NFC", s or "")
    return re.sub(r"\s+", " ", s).strip().casefold()


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
    site = (s.get("website") or "").split("//")[-1].strip("/").lower()

    rows, problems = [], 0
    for p in facts.get("profiles", []):
        ns = name_status(p.get("name_shown", ""), name, aliases)
        bio = p.get("bio", "")
        sim = difflib.SequenceMatcher(None, norm(one), norm(bio)).ratio() if one and bio else 0.0
        has_cat = bool(cat) and norm(cat) in norm(bio)
        links = p.get("links_to_site")
        if links is None and site:
            links = site in norm(bio) or site in norm(p.get("website_field", ""))
        ok = ns in ("exact", "alias") and has_cat and sim >= 0.6 and links
        problems += 0 if ok else 1
        rows.append((p.get("platform", "?"), p.get("url", ""), ns, f"{sim:.0%}", "yes" if has_cat else "NO",
                     "yes" if links else "NO", "ok" if ok else "FIX"))

    L = [f"# Profile consistency: {name}", "",
         f"Canonical sentence: \"{one}\"", f"Category phrase: \"{cat}\"", "",
         "| Platform | URL | Name | Bio vs sentence | Category in bio | Links to site | Status |",
         "|---|---|---|---|---|---|---|"]
    L += ["| " + " | ".join(r) + " |" for r in rows]
    L += ["", f"{problems} of {len(rows)} profiles need a fix. Target: name exact, category named, "
          "bio at least 60% the same as the canonical sentence, link to the website."]
    md = "\n".join(L)
    if a.md:
        with open(a.md, "w", encoding="utf-8") as f:
            f.write(md + "\n")
    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
