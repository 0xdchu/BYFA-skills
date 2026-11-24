---
name: usability-test
description: Test a user flow or clickable mockup with 5 people who match the ICP before code, then turn the sessions into ranked findings that point back to the spec section, flow step or screen to fix. Writes the plan (3-5 tasks from the flow's success criteria, an ICP screener, consent, a moderator script), guides a pilot and 5 think-aloud sessions, transcribes recordings locally, scores each task and writes findings with verbatim quotes, "k of 5" counts and a 0-4 severity. Use when saying "usability test", "user test", "test the mockup with users", "thử với khách", "thử với 5 người", "kiểm thử khả dụng", or when the userflow review gate still needs "checked with a real user". Not for discovery interviews before any design (product-spec section 2), drawing the flow (userflow), building screens (mockup), analytics on a live product (posthog), or A/B tests.
metadata:
  category: product
  version: "0.1.0"
---

# /usability-test

Watch 5 real people from the target group try to do the product's main jobs on the mockup, and write down where they get stuck. The deliverable is a **findings list**: each problem with who hit it, what they said, how bad it is and which spec section, flow step or screen to change.

A mockup that the team finds clear proves nothing; the team already knows how it works. This step is where the flow's success criteria meet people who do not.

## When to use

- A clickable mockup (`/mockup`) or a working build exists and the main flow is drawn (`/userflow`).
- The userflow review gate's last item, "checked with a real user", is still open.
- A fixed version needs a second round to see whether the fixes worked.

## Don't use

- Before any design, to learn whether the problem is real: that is a discovery interview (`/product-spec` section 2, "talk to 3-5 people").
- To measure a live product: analytics (`/posthog`). A/B tests are out of scope for every skill here.
- To ask people what price they would pay: `/pricing` has its own price questions.

## Agent's part, owner's part

| Agent does | Owner does |
|---|---|
| Writes the plan, tasks, screener, invite and moderator script | Recruits the 5 people and books the sessions |
| Checks every task's start link opens without a login | Runs the pilot and the sessions (or asks a teammate who did not build it) |
| Transcribes recordings locally, reads screen frames | Gets consent and records each session |
| Scores tasks and writes the findings | Decides which fixes to make |

The agent never contacts participants, never invents one, and never fills a session it did not get a recording or notes for.

## Read first

1. `docs/SPEC.md`: section 2 (user groups and how they do it today), section 3 (the result and its numbers), the ICP → UI table in section 4 if present.
2. `docs/FLOW.html` and the flow-spec table: steps, failure branches, the measurement column.
3. The mockup: its share link and `#state=` links (gallery mode, step 7 of `/mockup`; it must open without a login), or the offline `mockup/index.html` (single-file mode). An offline file is tested in person on the moderator's machine, or deployed as `/mockup` step 7 says before any remote session.
4. An earlier round in `docs/usability/`, if any: re-test its fixed problems first.

Missing spec or flow: stop and say which skill to run first. Missing mockup: test the flow on paper only if the owner asks; say the result is weaker.

## Steps

### 1. Pick what to learn, then the tasks
- Write 3-5 questions the test must answer, each tied to a flow step ("Do first-time users find where to connect their page, step 3?"). Take them from the riskiest steps: the path to the first result, the main failure branch, any step the spec marks unclear.
- Turn them into **3-5 tasks**, one per question, in the order a real user meets them. Each task has:
  - a scenario in the participant's words, with a reason to do it ("Your shop opens a new branch next week; get the posts for it ready");
  - **no UI labels and no hints** ("click Create project" gives the answer away);
  - a start link (URL or `#state=` link) so every participant starts from the same screen;
  - a **success state** someone can see on screen, taken from the flow-spec result column;
  - a time cap (agent suggestion: 2x the time a teammate needs; mark it so).
- Done when: every task maps to a flow step number and has a visible success state.

### 2. Write the screener from the ICP
- Turn each row of the spec's user table into 3-5 screening questions about what people **do today**, not who they say they are ("How did you make your last 5 posts?", not "Are you a content creator?").
- **5 people per user group.** Two groups that use different screens: 5 each, or 3-4 each when time is short (say which). Five people find most of the problems a round can find; the rest comes from a second round after fixes (Nielsen, "Why You Only Need to Test with 5 Users", NN/g, 2000).
- Exclude: the team, friends who have seen the product, people who build similar products, unless they are the ICP.
- Draft the invite message and a short consent text: what is recorded, who sees it, when it is deleted, that they can stop at any time.
- Done when: the screener rejects someone outside the ICP on paper.

### 3. Pilot once
- The owner runs the full script with one person (anyone). Fix wording that confused them, links that broke, tasks that ran over time.
- Pilot results are never counted in the findings.

### 4. Run the sessions (owner), with the moderator script
Write the script into the plan (`templates/plan.md`). 30-45 minutes, one person at a time, remote with screen share and recording, or in person recording the screen.
- **Open:** "We are testing the product, not you. There are no wrong answers. Please say out loud what you are thinking."
- **Warm-up (5 min):** 2-3 questions on how they do this job today, plus one question for each trait still `TODO` in the spec's ICP → UI table. It checks they fit the ICP, gives words for the findings, and fills those traits (write the answers back into the spec only with the owner's consent).
- **Tasks:** read one at a time. After each, ask the Single Ease Question (Sauro and Dumas, 2009): "How easy or hard was that, from 1 (very hard) to 7 (very easy)?"
- **Moderator rules:** do not help, do not explain, do not defend the design. Answer a question with a question ("What would you expect?"). Silent for 10 seconds: "What are you thinking now?" Past the time cap or stuck: give the smallest hint and write it down. Finished after the hint = `success with hint`; still not finished = `fail`, then move on so the later tasks stay testable.
- **Close:** "What was most confusing?" and "What would you tell a friend this does?" (checks the result in spec section 3 came across).
- Done when: each session has a recording or the moderator's notes with timestamps.

### 5. Transcribe and look
- Recordings go in `docs/usability/<round>/raw/`, which is gitignored. They stay on this machine and are never uploaded to a third-party service unless the consent text says so.
- Check the tools first: `command -v whisper ffmpeg`. Missing one: skip that part, work from the moderator's timestamped notes, and say in `findings.md` which sessions had no transcript or no frames.
- Transcribe each recording with a local Whisper in the session's language (`whisper <file> --language <code>`). Long files use a lot of memory; on Linux run it under a cap (`systemd-run --user --scope -p MemoryMax=8G whisper …`).
- From the screen recording, cut frames with `ffmpeg` around each task (one frame every 2-5 seconds into a contact sheet) and read them as images, to see where they clicked, not only what they said.
- Write one `sessions/P<n>.md` per participant (template in `templates/plan.md`): warm-up answers, then per task outcome, time, wrong turns, SEQ, quotes with timestamps.

### 6. Score each task
One table, tasks × participants, in `findings.md`:
- **Outcome:** `success` · `success with hint` · `fail` · `gave up`. Only `success` counts as a success; `success with hint` is shown next to it ("2 of 5, +1 with hint"), never added in.
- **Time on task** from the recording, for unassisted successes only; `n/a` otherwise.
- **Wrong turns:** each time they went to a screen or pressed a control off the flow's path.
- **SEQ** 1-7.
- **Where stuck:** flow step number and mockup screen id.

With 5 people, write counts, **"3 of 5", never "60%"**, and no averages presented as statistics. Medians of time are fine with the count next to them.

### 7. Write the findings
Group what you saw into problems. Each problem in `findings.md` (`templates/findings.md`):
- what happened, in one sentence a builder can act on;
- **k of N** who hit it, and which participants;
- evidence: verbatim quote with participant and timestamp, or the frame that shows it;
- **severity 0-4** (Nielsen, "Severity Ratings for Usability Problems", NN/g): 0 not a problem · 1 cosmetic · 2 minor · 3 major, high priority to fix · 4 catastrophe, imperative to fix before release. Judge frequency, impact and whether it repeats;
- **where to fix**: `SPEC §n`, `FLOW step n`, or mockup `screen-id` + state;
- **root or surface**: a problem with the offer, the ICP or the core goes to the spec first; a label, layout or missing state goes to the mockup;
- a proposed fix, marked "agent suggestion".

Also list what worked (tasks most people did without hesitation), so a fix does not break it. A problem seen once stays in the list as 1 of N; do not drop it, do not inflate it.

### 8. Hand back and loop
- One message: full path of `findings.md`; the task table; the severity 3-4 problems first; the 3 findings the agent is least sure of and why.
- The owner decides what to fix. The agent changes the spec, flow or mockup only after that decision, through `/product-spec`, `/userflow` or `/mockup`.
- After fixes: round 2 with 5 **new** people, on the tasks that touched fixed problems plus one task that worked, to catch regressions.
- Record the round in the `## Review` section of the flow spec (`/userflow` reference §2): "Usability round <N>: `<date>`, `docs/usability/<round>/findings.md`", and in `START-HERE.md`.

## Output

```
docs/usability/<YYYY-MM-DD>-round<N>/
  plan.md        questions, tasks, screener, invite, consent, moderator script
  sessions/P1.md … P5.md
  findings.md    task table, problems by severity, what worked
  raw/           recordings, full transcripts, frames (gitignored)
```

Add `docs/usability/*/raw/` to `.gitignore` before the first session; recordings and full transcripts hold personal data. Files use participant codes P1-P5, never names, phone numbers or faces.

## Do not

- Invent a participant, a quote, a time or a score. A session without a recording or notes does not exist.
- Count the team, friends or the pilot as ICP participants.
- Lead: name a button, nod at the right answer, explain the design mid-task.
- Report percentages or averages from 5 people as if they were statistics.
- Ask "do you like it" or "would you use it"; watch what they do instead.
- Publish recordings, faces or real names, or upload them to an outside service without consent.
- Change the spec, flow or mockup before the owner chooses the fixes.
- Promise that a fixed mockup will sell.

## Done when

- `findings.md` has the task table filled for every participant who took part, and every problem has k of N, evidence, severity and where to fix.
- Every severity 3-4 problem has a disposition from the owner: fix now, fix later with a reason, or not a problem with a reason.
- The flow spec's `## Review` section names this round.

## Eval

| # | Check | Target |
|---|---|---|
| E1 | Tasks that contain a UI label or hint | 0 |
| E2 | Tasks without a flow step number and a visible success state | 0 |
| E3 | Quotes, times or scores without a participant code and timestamp | 0 |
| E4 | Percentages, or averages without their count, in the task table or findings | 0 |
| E5 | Problems without severity or where to fix | 0 |
| E6 | Pilot or team members counted as participants | 0 |
| E7 | Spec, flow or mockup edits before the owner's decision | 0 |

## Feedback log

| Date | What happened | What changed |
|---|---|---|
| 2026-11-24 | First version. A review of the UI design process (core and ICP → user flow → mockup → test with users → analytics) found the "test with 5 users" step had no skill: `/mockup` proves screens render, and the userflow gate asks for "checked with a real user" with no method behind it | New skill; not yet run on a real round. Log the first round here, with what the owner changed in the plan |

## This skill must improve itself

After each round, add a line to the feedback log: which task wording confused people in the pilot, which finding the owner rejected and why, and any step the owner had to do that this skill did not tell them. A rule added here needs the round that showed it.
