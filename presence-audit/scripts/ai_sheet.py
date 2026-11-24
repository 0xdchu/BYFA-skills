#!/usr/bin/env python3
"""Build the AI answer check sheet, and compare two runs.

Usage:
  python3 ai_sheet.py sheet facts.json --out answers-YYYY-MM-DD.json [--md sheet.md]
  python3 ai_sheet.py diff answers-OLD.json answers-NEW.json

`sheet` writes one record per (assistant, question) with empty answer fields, and a
markdown sheet for whoever asks the questions. Ask in the consumer apps (what customers
see), in a fresh chat, with web search on and memory off. Paste each answer verbatim,
then set `verdict` (correct, partly, wrong, unknown) for described questions, or
`mentioned` (true/false) for recommendation questions.

`diff` shows what changed between two dated runs of the same sheet.
"""
import argparse
import json
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


def summarize(recs):
    d = Counter(r.get("verdict") or "blank" for r in recs if r["kind"] == "described")
    rec = [r for r in recs if r["kind"] == "recommend" and r.get("mentioned") is not None]
    rate = sum(1 for r in rec if r["mentioned"]) / len(rec) if rec else None
    return d, rate, len(rec)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s1 = sub.add_parser("sheet")
    s1.add_argument("facts")
    s1.add_argument("--out", required=True)
    s1.add_argument("--md")
    s1.add_argument("--runs", type=int, default=10, help="repeats per recommendation question (default 10)")
    s2 = sub.add_parser("diff")
    s2.add_argument("old")
    s2.add_argument("new")
    a = ap.parse_args()

    if a.cmd == "sheet":
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

    old = json.load(open(a.old, encoding="utf-8"))
    new = json.load(open(a.new, encoding="utf-8"))
    key = lambda r: (r["assistant"], r["qid"], r.get("run", 1))
    o = {key(r): r for r in old}
    L = ["| Assistant | Question | Before | After |", "|---|---|---|---|"]
    for r in new:
        if r["kind"] != "described":
            continue
        b = o.get(key(r), {}).get("verdict") or "blank"
        n = r.get("verdict") or "blank"
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
