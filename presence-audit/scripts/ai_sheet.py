#!/usr/bin/env python3
"""Build the AI answer check sheet, and compare two runs.

Usage:
  python3 ai_sheet.py sheet facts.json --out answers-YYYY-MM-DD.json [--md sheet.md]
  python3 ai_sheet.py summary answers-YYYY-MM-DD.json
  python3 ai_sheet.py diff answers-OLD.json answers-NEW.json

`sheet` writes one record per (assistant, question) with empty answer fields, and a
markdown sheet for whoever asks the questions. Ask in the consumer apps (what customers
see), in a fresh chat, with web search on and memory off. Paste each answer verbatim,
then set `verdict` (correct, partly, wrong, unknown) for described questions, or
`mentioned` (true/false) for recommendation questions.

`summary` gives the scorecard of one run for AUDIT.md. `diff` shows what changed
between two dated runs of the same sheet. `sheet` never overwrites an existing file.
"""
import argparse
import json
import os
import sys
from collections import Counter

ASSISTANTS = ["ChatGPT", "Perplexity", "Gemini", "Claude", "Google AI Mode"]

BRAND_Q = [
    ("what", "What is {name}?"),
    ("does", "What does {name} do, and who is it for?"),
    ("where", "Where is {name} based, and where does it operate?"),
    ("price", "How much does {name} cost?"),
    ("vs", "How is {name} different from {competitor}?"),
]
PERSON_Q = [
    ("who", "Who is {name}?"),
    ("does", "What does {name} work on, and where?"),
    ("known", "What is {name} known for?"),
    ("contact", "How can I work with or contact {name}?"),
    ("vs", "How does {name}'s work compare with {competitor}'s?"),
]


def build(facts, runs):
    s = facts["subject"]
    qs = PERSON_Q if s.get("type") == "person" else BRAND_Q
    comp = (s.get("competitors") or ["the main alternative"])[0]
    recs = []
    for asst in facts.get("assistants", ASSISTANTS):
        for qid, q in qs:
            recs.append({"assistant": asst, "kind": "described", "qid": qid,
                         "question": q.format(name=s["name"], competitor=comp),
                         "answer": "", "sources_cited": [], "verdict": "", "wrong_fact": "", "run": 1})
        for i, q in enumerate(facts.get("recommend_queries", []), 1):
            for run in range(1, runs + 1):
                recs.append({"assistant": asst, "kind": "recommend", "qid": f"rec{i}",
                             "question": q, "answer": "", "sources_cited": [], "mentioned": None, "run": run})
    return recs


def sheet_md(facts, recs, runs):
    s = facts["subject"]
    L = [f"# AI answer check: {s['name']}", "",
         "How to ask: consumer app, fresh chat, signed out or memory off, web search on. "
         "Paste the answer verbatim and list the sources it cites. Screenshot each answer.", "",
         f"Facts to judge against: {s.get('one_liner', '')} Location: {s.get('location', '')}. "
         f"Price: {s.get('price', '')}.", ""]
    for asst in dict.fromkeys(r["assistant"] for r in recs):
        L += [f"## {asst}", "", "| # | Question | Verdict |", "|---|---|---|"]
        for r in recs:
            if r["assistant"] == asst and r["run"] == 1:
                L.append(f"| {r['qid']} | {r['question']} | |")
        L.append("")
    if facts.get("recommend_queries"):
        L += [f"Recommendation questions: ask each one {runs} times in separate fresh chats; "
              "answers change almost every run, so count how often the name appears, never its position."]
    return "\n".join(L)


VERDICTS = {"correct", "partly", "wrong", "unknown"}


def verdict(r):
    v = str(r.get("verdict") or "").strip().lower()
    return v if v in VERDICTS else ("blank" if not v else f"invalid:{v}")


def mentioned(r):
    """True, False, or None (not filled). Accepts booleans and yes/no/true/false strings."""
    m = r.get("mentioned")
    if isinstance(m, bool) or m is None:
        return m
    t = str(m).strip().lower()
    if t in ("yes", "y", "true", "1"):
        return True
    if t in ("no", "n", "false", "0"):
        return False
    return None


def summarize(recs):
    d = Counter(verdict(r) for r in recs if r["kind"] == "described")
    rec = [r for r in recs if r["kind"] == "recommend" and mentioned(r) is not None]
    rate = sum(1 for r in rec if mentioned(r)) / len(rec) if rec else None
    return d, rate, len(rec)


def scorecard(recs):
    L = ["| Assistant | correct | partly | wrong | unknown | blank | Mention rate (runs) |", "|---|---|---|---|---|---|---|"]
    for asst in dict.fromkeys(r["assistant"] for r in recs):
        mine = [r for r in recs if r["assistant"] == asst]
        d, rate, n = summarize(mine)
        L.append(f"| {asst} | " + " | ".join(str(d.get(k, 0)) for k in ("correct", "partly", "wrong", "unknown", "blank")) +
                 f" | {'n/a' if rate is None else f'{rate:.0%} ({n})'} |")
    bad = sorted({v for r in recs if r["kind"] == "described" for v in [verdict(r)] if v.startswith("invalid:")})
    if bad:
        L.append(f"\nFix these verdict values (use correct, partly, wrong or unknown): {', '.join(bad)}")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s1 = sub.add_parser("sheet")
    s1.add_argument("facts")
    s1.add_argument("--out", required=True)
    s1.add_argument("--md")
    s1.add_argument("--runs", type=int, default=10, help="repeats per recommendation question (default 10)")
    s1.add_argument("--force", action="store_true", help="overwrite an existing --out file")
    s3 = sub.add_parser("summary")
    s3.add_argument("answers")
    s2 = sub.add_parser("diff")
    s2.add_argument("old")
    s2.add_argument("new")
    a = ap.parse_args()

    if a.cmd == "sheet":
        if os.path.exists(a.out) and not a.force:
            print(f"{a.out} already exists and may hold pasted answers. Use a new dated name, or --force.",
                  file=sys.stderr)
            return 2
        with open(a.facts, encoding="utf-8") as f:
            facts = json.load(f)
        recs = build(facts, a.runs)
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(recs, f, ensure_ascii=False, indent=2)
        md = sheet_md(facts, recs, a.runs)
        if a.md:
            with open(a.md, "w", encoding="utf-8") as f:
                f.write(md + "\n")
        print(md)
        print(f"\nWrote {len(recs)} records to {a.out}")
        return 0

    if a.cmd == "summary":
        with open(a.answers, encoding="utf-8") as f:
            print(scorecard(json.load(f)))
        return 0

    old = json.load(open(a.old, encoding="utf-8"))
    new = json.load(open(a.new, encoding="utf-8"))
    key = lambda r: (r["assistant"], r["qid"], r.get("run", 1))
    o = {key(r): r for r in old}
    L = ["| Assistant | Question | Before | After |", "|---|---|---|---|"]
    for r in new:
        if r["kind"] != "described":
            continue
        b = verdict(o[key(r)]) if key(r) in o else "blank"
        n = verdict(r)
        L.append(f"| {r['assistant']} | {r['question']} | {b} | {n}{' (changed)' if b != n else ''} |")
    for label, recs in (("Before", old), ("After", new)):
        d, rate, n = summarize(recs)
        L.append("")
        L.append(f"{label}: described answers {dict(d)}; recommendation mention rate "
                 f"{'n/a' if rate is None else f'{rate:.0%} of {n} runs'}")
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    sys.exit(main())
