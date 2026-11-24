# <Product name>: usability test plan, round <N>

- Date: <YYYY-MM-DD>
- Tests: <share link, opens without a login: checked <date>> | <offline mockup/index.html, sessions in person>
- Spec: docs/SPEC.md v<x> · Flow: docs/FLOW.html
- Moderator: <role, not the person who built the screens if possible>
- Status: draft, waiting for the owner

## 1. What we want to learn

| # | Question | Flow step |
|---|---|---|
| Q1 | <Do first-time users find …?> | <n> |

## 2. Tasks

Read aloud one at a time. No UI labels, no hints.

| # | Scenario (participant's words) | Start link | Success state on screen | Time cap | Question |
|---|---|---|---|---|---|
| T1 | <reason + goal> | <URL or #state=…> | <what is visible when done> | <min> (agent suggestion) | Q1 |

## 3. Who we test with

User group(s) from SPEC §2: <group> × 5.

Screener (what they do today):
1. <question> → keep if <answer>
2. …

Exclude: the team, friends who have seen the product, people building a similar product.

## 4. Invite and consent

Invite: <short message the owner sends>

Consent (read before recording): we record the screen and voice; only <who> watches it; we delete it on <date>; we write you as a code (P1, P2, …), never your name; you can stop at any time.

## 5. Moderator script (30-45 min)

1. Open: "We are testing the product, not you. There are no wrong answers. Please say out loud what you are thinking."
2. Warm-up: <2-3 questions on how they do this job today> + <one per `TODO` trait in the spec's ICP → UI table>
3. Tasks T1…Tn. After each: "How easy or hard was that, from 1 (very hard) to 7 (very easy)?"
4. Rules: do not help or explain. Answer with "What would you expect?". Silent 10 s: "What are you thinking now?". Past the cap or stuck: smallest hint, note it. Finished after it = success with hint; not finished = fail, go on.
5. Close: "What was most confusing?" · "What would you tell a friend this does?"

## 6. Pilot

- Pilot with: <role>, <date> (not counted)
- Changed after the pilot: <task wording, links, caps>

---

# Session note template: sessions/P<n>.md

- Participant: P<n> · group: <group> · date: <YYYY-MM-DD> · recording: <local path, not in git>
- Warm-up: <how they do it today, gist or quote with timestamp>

| Task | Outcome | Time | Wrong turns | SEQ | Stuck at (flow step · screen) |
|---|---|---|---|---|---|
| T1 | success / success with hint / fail / gave up | m:ss | <n> | <1-7> | <step · screen-id> |

Quotes: "<verbatim>" (P<n>, mm:ss)
Hints given: <task, hint, mm:ss>
Close answers: <…>
