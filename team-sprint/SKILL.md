---
name: team-sprint
description: Turns a weekly team meeting into a record and ready-to-assign tickets, for whoever holds the Product role. Reads the transcript (file, pasted, or typed notes), produces a meeting record (decisions, who took what, open questions) and draft tickets in a fixed 5-part frame (Problem, Outcome, Definition of done, Not doing, How to verify) with one assignee, one deadline, one label each. Stops for Product to edit, drop or assign; only after approval does it create the `Weekly meeting dd/mm` document on the team's Linear page, create the issues in the current cycle, and link the tickets into the record. No Linear MCP means it writes markdown to paste by hand. Never invents an assignee or a deadline, never settles a decision for the team. Use when someone says "weekly meeting notes", "meeting is over, create the tickets", "transcript to tickets", "put the meeting record on Linear", "draft tickets in the 5-part frame", "split the work after the team meeting", "team sprint", "biên bản họp tuần", "họp xong rồi, tạo ticket", "từ transcript ra ticket", or Build to Own Master week 5. Not for writing a product spec (use product-spec), drawing a flow (use userflow), or a coding plan inside a repo (use sdlc).
metadata:
  category: product
  version: "0.1.0"
  sources: "sonpiaz/bto-master `master-team-sprint` v0.0.1 and docs/week-05-team (TEAMWORK.md, ROLES.md, CONNECT-AGENT.md)"
---

# /team-sprint

## Goal

After the weekly meeting, within 24 hours, everyone on the team opens Linear and sees: what the meeting decided, which ticket is theirs, which deadline, and what "done" means. Someone who missed the meeting opens the record and knows what was decided and what they were given.

This skill covers one stretch of the weekly routine: record, transcript, meeting record, tickets. The rules below are the team rules for that stretch.

## Agent's part, your part

You are the person holding the Product role on the team.

| Agent does | You do |
|---|---|
| Reads the transcript, splits out decisions, who took what, open questions | Turn on the recording, get the transcript, hand it to the agent |
| Drafts tickets in the 5-part frame | Read them, edit, drop, assign one assignee, a deadline, a label |
| Leaves blank and asks wherever the transcript is silent | Answer the blanks, settle open questions if needed |
| After you approve: creates the record document, creates the issues in the cycle, links tickets into the record | Message the team chat so each assignee confirms |

The agent does its part first. When it reaches a step that needs you, it stops and says exactly what it needs. It does not guess.

## Permissions

- Does on its own: read the transcript, read the product's repo (team rules, `docs/SPEC.md`), read Linear (team, cycle, labels, members, documents, issues), write draft files in the working folder.
- Asks first, every time: any write to Linear (create or edit a document, issue, comment).
- Never: settle a decision for the team, assign a ticket to an agent, message the team chat for you, delete or change the state of an existing ticket.

## Inputs

1. **Transcript.** One of three: a file path (`.txt`, `.md`, `.vtt`, `.srt`, a Google Meet or Zoom download), pasted straight into the chat, or hand-typed meeting notes. Typed notes still work, but say one sentence: notes lack verbatim quotes, so the Problem field will often lack evidence.
2. **Meeting date.** From the transcript or the file name. If it is missing, ask, because the record's name needs it.
3. **Team context, read only, skip any file that is absent:** a `TEAM RULES` block (in the repo or where you point), `docs/SPEC.md`, `README.md`. Take from them: team name, who holds which role, the weekly meeting day. A name in the transcript that matches a role name in the team rules is used exactly as written there. If the transcript names only roles and there are no team rules, write the assignee by role; the Linear member name is matched in step 4.

Linear is read only in step 4, after approval; steps 1 to 3 need no Linear.

## Steps

### 1. Read the transcript, split out three things

- **Decisions:** only what the team settled in the meeting, with a clear closing line in the transcript (Product decided, or the whole group agreed). Each line says who decided. Discussed but not settled, two people with two views and nobody deciding, "let's think about it next week" are **not** decisions: they go under Open questions as "waiting for Product to decide". Handing out work (who takes which ticket) belongs under Who took what, not repeated under Decisions. The agent never settles a team decision, even when one option is clearly better.
- **Who took what:** every piece of work that has an assignee named in the meeting. The assignee comes only from the transcript: the person took it themselves, or Product gave it and the person did not refuse. Never guess by role ("design work, so probably the Designer").
- **Open questions:** a question nobody answered, work nobody took, a disagreement not settled. Work that was raised but not taken still becomes a draft ticket with `Assignee: ?`, for Product to assign or drop.

### 2. Draft the tickets

One ticket per piece of work, in this frame:

```
Title: <verb + concrete result>
Problem: who is hitting what, with evidence
Outcome: what the user sees differently when it is done
Definition of done: a checklist you can check by eye
Not doing: what lies outside this ticket
How to verify: steps another person follows in 5 minutes
Assignee: <one person> · Deadline: ... · Label: ...
```

Rules for filling it in:
- **Each ticket has 5 parts, one assignee, one deadline, one label.** Work for several people is split into several tickets. Work that cannot finish in a 1-week cycle is split smaller.
- **"Not doing" is the part most often skipped, so write it out.** Never leave it empty.
- Words taken from the transcript are written as the transcript says them. Words the agent adds itself (a line of Definition of done, a verify step, a Not doing line) are marked `(agent suggestion)` so you know which lines need a careful read.
- **Problem** needs evidence: a number, a user's words, something that happened. If the transcript has none, write `TODO: evidence?`. Never invent a number or a user quote.
- **Assignee** is only a person on the team. If the transcript does not say who takes it, write `Assignee: ?` and ask. Never assign to an agent: if someone says "let the agent do it", the assignee is the person who directs that agent, and work with decision content (choosing a price, a market, a product) always belongs to a person.
- **Deadline** comes only from the transcript, in the transcript's exact words ("Thursday", "before next week's meeting"). Linear needs a concrete date: if the words are not yet a date, the agent does not convert them; put them under Blanks for Product to write the date (for example `T2 "Thursday" is which date?`), with no date the agent guessed. If the transcript gives no deadline, write `Deadline: ?` and ask; it may offer `before next week's meeting` as one option for Product to pick, never fill it in itself.
- **Label** is one of five: Feature, Bug, Design, Research, Marketing. A label is a classification, so the agent may propose one; mark it `(agent suggestion)` if the transcript does not say.

### 3. Stop, hand it to you for approval

Give, in **one message**:
1. The draft meeting record (frame under Output).
2. The draft tickets, numbered T1, T2, **each ticket printed with all 7 lines of the frame**, no summary: Product approves the exact words that go to Linear.
3. **Blanks that need you**, collected in one numbered list: which ticket lacks an assignee or deadline; which open question needs settling now; the meeting date if it is missing.
4. The invitation: "Edit, drop, assign by number (for example `T2 assignee Growth, deadline 27/11`, `drop T3`). When approved, type `create on Linear`."

Write the same draft to `docs/meetings/<YYYY-MM-DD>-weekly-meeting.md` in the working folder, so several rounds of editing do not lose anything. That file is on your machine, not Linear. It does not copy the transcript, only says where the transcript came from (a path or "pasted in chat"), because the product's repo may be public; the transcript goes only into the Linear document.

The team name is needed only in step 4, so do not ask for it here: if it is unknown, leave the Team field in the record as `?` and do not put it in Blanks. A value Product just typed (a date, an assignee) is used straight away, not asked to be confirmed again.

**Without a clear approval, write nothing to Linear.** A clear approval is you typing `create on Linear`, `approved`, `go ahead`, or a phrase of the same meaning after seeing the final draft. If you only edit one ticket, that is an edit, not approval: after the edit show the draft again and ask again. A sentence that both edits and says go ("T1 change deadline to 28/11, then do it") is the same: apply the edit, show the final draft, ask one question, because you have not seen the draft after the edit. A ticket still missing an assignee or deadline gets reminded by name and is not created; you assign it, or type `drop T<n>`.

If you push back or comment in a way that contradicts the transcript (for example assigning to someone who refused in the meeting): say so in one sentence and do as you say, because Product decides.

### 4. Write to Linear, after approval

Check for the Linear MCP first: does the session have tools from the Linear server (`https://mcp.linear.app/mcp`)? If not, go to step 5.

Linear does not publish tool names, so pick tools by function. In order:
1. **Find the team.** List the teams; one team, use it; several, use the team named in the team rules; unsure, ask.
2. **Find the current cycle** of the team: the cycle running today. A 1-week cycle starts on the meeting day, so tickets after the meeting go into the new cycle. If the team has no cycles enabled, stop and tell the user to enable them (Team settings > Cycles: Enable cycles, 1 week, starting on the meeting day); do not change team settings yourself.
3. **Match assignees and labels.** Find the member by the name you approved; a name matching two people, ask. A label that does not exist in the team is not created: create the ticket without a label and list it.
4. **Check for duplicates.** A document `Weekly meeting dd/mm` or an issue with the same title already exists (the skill ran twice): edit the existing one, do not create a second; ask you if the content differs.
5. **Create the record document** on the team's page, named exactly `Weekly meeting dd/mm`.
6. **Create the issues**, one per ticket: team, title, 5-part description, assignee, due date, label, current cycle. At the end of the description add two lines:
   - `From the record: Weekly meeting dd/mm` with the document link.
   - `When done: report in a comment (what was done, link, how to check) and tag <Product name>.`
7. **Link the tickets into the record.** Edit the document: in Who took what, add the ticket code and link to each row (for example `ABC-12`). Linear shows a ticket link as a small clickable item; if it only shows plain text, tell the user to open the document, type `@` and then the ticket name.

Everything the MCP writes stands under your Linear account. At the end of the document add one line `[agent] Draft built by the agent, <Product name> approved <date time>`, so the team knows which lines are human and which are the agent's. Any comment the agent writes starts with `[agent]`.

When one write fails, stop, say which call failed and what was already created, and do not retry blindly.

### 5. No Linear MCP: export markdown

Write `docs/meetings/<YYYY-MM-DD>-weekly-meeting.md` with the final approved version, in two parts: `## Record` (the block to paste into a new document named `Weekly meeting dd/mm`; under Transcript write "paste the transcript here") and `## Tickets` (one block per ticket to paste into a new issue, with the last two lines as in step 4.6). The record block also ends with the `[agent]` line. Do not say it was created on Linear. Print the full path, then one line:

`To let the agent create these next time: claude mcp add --transport http linear-server https://mcp.linear.app/mcp, open Claude Code, type /mcp to sign in to Linear.`

### 6. Report back

Applies to both paths (Linear MCP or markdown). Give you, in one message:
- The record document link and the list of created tickets (code, title, assignee, deadline). For the markdown path, the file path.
- Time against the 24 hours after the meeting: how much is left, or how far past. One line, no blame. Counted from the meeting's end time in the transcript; if the time is unknown, count from the meeting date and say "about".
- **A draft message for the team chat** for you to send yourself: the record link, one line per person with their tickets, and a request for each person to confirm in the chat.
- One line for the assignees: at the start of each work session, ask your agent what is new on Linear for you (needs Linear connected).

## Output

The meeting record, with technical terms kept as-is:

```markdown
# Weekly meeting dd/mm

- Team: <team name> · Meeting date: <dd/mm/yyyy> · Present: <list> · Absent: <list or "none">
- Record: <link if any>

## Decisions
1. <decision> (decided by <who>)

## Who took what
| Ticket | Assignee | Deadline | Label |
|---|---|---|---|
| <title> <code and link once created> | ... | ... | ... |

## Open questions
1. <question> (waiting for <who> to decide)

## Transcript
<full transcript, or the meeting notes>
```

No decisions: write `No new decisions.` Do not invent one to fill the section. If you want the Transcript section dropped from the document, drop it.

## Not doing

- Do not write anything to Linear before you approve.
- Do not invent an assignee, a deadline, a number, or a user quote. If it is missing, leave it blank and ask.
- Do not settle a decision for the team, and do not turn an unsettled idea into a decision.
- Do not assign a ticket to an agent, and do not assign one ticket to two people.
- Do not create new labels, change team or cycle settings, or delete or change the state of existing tickets.
- Do not message the team chat for you.
- Do not commit the transcript into a public repo: it holds the whole team's words.
- Do not print API keys on screen.

## Checks

| # | Check | Target |
|---|---|---|
| E1 | A ticket has all 5 parts and "Not doing" is not empty | 100% |
| E2 | An assignee or deadline not in the transcript is filled in without Product assigning it | 0 |
| E3 | A Linear write before a clear approval | 0 |
| E4 | An unsettled idea recorded as a decision | 0 |
| E5 | A ticket assigned to an agent or to two people | 0 |
| E6 | No Linear MCP: a markdown file and the one line on how to connect | 100% |

## Self-improvement

After each use: the field Product edits most (usually Not doing and How to verify) gets noted with the comment. A comment repeated by two or more teams changes the Steps and adds a case to the checks. On closed tickets: read the assignee's report comment, and where a ticket came back because the Definition of done was vague, sharpen the fill-in rule in step 2. When a stronger model arrives, rerun the checks and drop any rule the new model already follows by itself.
