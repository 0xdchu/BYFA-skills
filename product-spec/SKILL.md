---
name: product-spec
description: Write a 3-5 page product spec (docs/SPEC.md) for your own product before any code, in a fixed 5-part frame - problem and who has it, the result users get, how it works core first, phased scope with an explicit "won't do" list, and "Phase 1 is done when" with a check for each line. Reads the context already on the machine first, asks at most 3 questions, never invents customer quotes or numbers, and loops on your feedback until you score it 9-10/10. Use when someone says "write a spec", "product spec", "PRD for my product", "SPEC.md", "viết spec", "đặc tả sản phẩm", "revise the spec from feedback", or Build to Own Master week 4. Not for drawing the flow (use userflow), a clickable mockup (use mockup), or a coding plan inside a repo (use sdlc).
metadata:
  category: product
  version: "0.2.0"
  sources: "sonpiaz/bto-master `master-product-spec` v0.0.2"
---

# /product-spec

## Goal

**One 3-5 page spec** an agent can build from correctly and you can check. It follows a fixed 5-part frame and is done only when **you** score it 9-10 out of 10.

Building is now the easy part; describing what you want is the hard part. The better the spec, the less the flow, mockup and MVP after it need fixing. The "won't do" list exists so the building agent does not add things on its own.

Example of the shape (read for shape, never copy content): the Citeable spec at `https://github.com/sonpiaz/bto-master/tree/main/docs/week-04-product-spec/example`.

## Agent's part, your part

| Agent does | You do |
|---|---|
| Reads context already on the machine | Say the idea and the result users should get |
| Asks at most 3 questions for what is missing | Give 2-3 reference products **you have really used**, their docs, step screenshots |
| Writes `docs/SPEC.md`, core separated from shell | Give what real users said about the problem |
| Revises from feedback, logs each change | Read each part, score it, comment until 9-10 |

## Inputs

### 1. Gather context first, ask after
Read only, change nothing. Stop as soon as you have (a) the product name and (b) an answer to each of the 3 questions below; a vague hint is not an answer.
1. Loaded instructions and memory: `CLAUDE.md`, `AGENTS.md`, project notes, `~/.bto-master/me.md`.
2. Files in the working folder (root and one level down): `PLAN.md`, `ROADMAP.md`, `research*.md`, `competitors*.md`, `pricing*.md`, `SPEC*.md`, `PRD*.md`, `README.md`, `docs/`, `notes/`.
3. Earlier work: `winning-product.config.md`, `pricing-model.md`, `competitors.md`, `pricing-teardown.md`.
4. The product's website or landing page, if any.

Read these without asking; skip missing files silently. Ask before reading anything else outside the working folder. Skip files over about 200 KB. Ignore context about other projects.

### 2. At most 3 questions, in one message
Only for what context does not answer, in this priority:
1. **Who has the problem, and how do you know?** Has anyone told you, and what did they say?
2. **After using it, what can users do** that they cannot today?
3. **2-3 reference products you have really used**: links, which step you liked, which you hated; docs, API, screenshots if any.

No 4th question. Anything else missing: infer it, or write `TODO` plus "agent suggestion" in the spec. Default writing: the user's language, technical terms in English. If the user or context asks for plain language, explain each technical term once, short sentences, no abbreviations.

No reference product used yet: write `TODO: try 2 reference products` and say section 4's reference table stays weak until then. Never use a product the user has not opened. A reference with no likes or dislikes: keep it, `TODO` in the empty cells.

## Steps

### 1. Write the spec
Write `docs/SPEC.md` in the product folder. "Section N" means the `## N.` heading. Replace `<...>`, copy the rest. The Flow, Mockup and References lines say `not drawn`, `not built`, `none` until the file exists, then its path. Unknown owner name: `you`. The v0.1 history line is written at creation.

Terms: **user** is whoever uses your product. If users have their own customers (a spa owner uses it, the spa's clients book through a link), call that group **users' customers**, never just "customers". Quotes keep the speaker's words. UI labels are in the language of the person who sees that screen.

```markdown
# <Product name>: Product spec v0.1

- Status: draft, waiting for <owner> to approve. Phase 1 is built only after approval.
- Date: <YYYY-MM-DD>
- Flow: not drawn
- Mockup: not built
- References: none

## 1. Summary
## 2. Problem and who has it
## 3. Result the user gets
## 4. How it works, core first
## 5. Scope by phase, and what we won't do
## 6. Phase 1 is done when, and how to check
## 7. Open questions
## 8. Risks
## Change history
- v0.1 · <YYYY-MM-DD> · first draft, no feedback yet · written from <context files read>
```

**1. Summary.** One paragraph: what it does, for whom, how it differs from what they do today.

**2. Problem and who has it.** Table: user group · how they do it today · where it hurts · how you know. Users' customers get their own row labelled `Users' customers` or `<name> (users' customers)`. Real quotes in quotation marks with who and when. Remembered gist only: no quotation marks, start with `(gist, not verbatim)`, still who and when (a range is fine). Unnamed speaker: role plus "unnamed". Remember someone spoke but not what: `TODO: what did <role> say?`. Nobody real: `TODO: talk to 3-5 people`, and say it is an assumption. Never invent a quote.

**3. Result the user gets.** Written as what users do and see, with a number where possible ("empty project to first result in under 15 minutes"). Define every metric with a formula.

**4. How it works, core first.** The longest section.
- **Core and shell.** Two-column table. Core makes the product work; without it there is no product. Shell is UI, buttons, extras. Describe the core in depth: input, processing, output, where it breaks.
- **Learning from references.** Table: product · what you used · what to learn · what not to learn. Screenshots go in `docs/refs/01-....png` with `docs/refs/README.md` listing each; then set the References header line to that README.
- **Main flow.** One short `mermaid` flowchart (about 12 nodes max), then one item per step: screen, what the user does, what the system does. The full diagrams belong to `/userflow`.
- **Context from the user's own agent.** Not asked. If users already use an AI agent (ChatGPT, Claude, Cursor…), propose a setup prompt they paste into it; the agent fills in their context and writes it to the product (via MCP) or prints JSON to paste. Context silent: keep the proposal, prefixed `TODO: do users already use an AI agent?` and "agent suggestion". Context says they don't: drop it.
- **ICP → UI decisions.** Before the UI bullet, a table that turns each user group in section 2 into UI choices, so layout follows who uses it instead of taste: trait · what we know and its source · UI decision. One row per trait that changes a screen:

  | Trait | Typical decision |
  |---|---|
  | Device and where they use it (phone on the go, desk) | Phone-first or desktop-first; one-hand reach; how much fits on a screen |
  | How often (daily vs. now and then) | Dense screens and shortcuts vs. guided steps and reminders |
  | Comfort with software | Wizard with one choice per screen vs. one editable page |
  | Apps they already use every day | Copy those apps' patterns (navigation, list, chat, checkout) instead of inventing new ones |
  | What makes them trust a new tool | Where proof, price and a support contact sit |
  | Language and terms they use | UI labels in their words (section 2 quotes), not ours |

  The middle column is a source (a quote, a talk, data) or `TODO: ask <group> about <trait>`; never "agent suggestion" and never a stereotype of the group. The decision column may be an "agent suggestion". A `TODO` trait goes on the list for the section 2 talks; if still open when the mockup is tested, `/usability-test` asks it in the warm-up. Users' customers who see their own screens get their own rows.
- **UI.** Layout (where the menu and content sit), numbered list of main screens, labels in the viewer's language. Each layout choice that comes from the ICP table names its row.
- **Data.** Main tables, one line each: name, key columns.
- **Proposed tech.** Marked "proposal, decided at build time". The smallest thing that works.

**5. Scope and won't do.** Phase table: Phase 1 includes / excludes; Phase 2; Later. Then a separate **Won't do** list, one concrete item per line (e.g. no login yet, no real payment yet). This is where the building agent learns where to stop.

**6. Phase 1 is done when.** Numbered list; each line a **checkable** condition with how to check it: who does what and sees what. Never "works well" or "easy to use". Thresholds ("under 15 minutes", "3 spa owners try it") are numbers too: source, `TODO`, or "agent suggestion". Same for section 3.

**7. Open questions.** Only what the owner can decide (price, who gets the trial, name), numbered so they can answer by number.

**8. Risks.** One line each, with how to reduce it.

Length: 3-5 pages, about 1,500-3,000 words (`wc -w docs/SPEC.md`). Too long: cut the shell, never the core.

### 2. Self-check before handing over
- The 5 parts (sections 2-6) present; section 4 has the core/shell table and the ICP → UI table; section 5 has Won't do; every section 6 line has a check.
- Every number (including thresholds), name and quote has a source, `TODO`, or "agent suggestion".
- No promised outcome ("will definitely get customers", "will make revenue").
- No code; only diagrams, tables, short data examples.

### 3. Review loop until 9-10
One message:
1. Full path of `docs/SPEC.md`.
2. A 5-line summary, one per part.
3. **The 3 places the agent is least sure of**, one sentence each.
4. "Read each part, score the whole thing out of 10, comment on anything, even just a hard sentence."

On feedback: change only what was pointed at; bump the version (v0.1 → v0.2) and add a history line (version · date · feedback · change); if feedback contradicts another part, say so and ask which wins; hand back in the same 4-part form.

**The user scores, never the agent.** Below 9: ask "What is missing to reach 9?" and loop. **Do not suggest the next step before 9.**

### 4. At 9-10
- Status line becomes "approved v0.x, <date>".
- Write or update `START-HERE.md` in the product folder: one sentence on what it does · status · reading order (SPEC, FLOW, mockup) · next step.
- Suggest `/userflow` to draw `docs/FLOW.html` from this spec.
- Debrief, 3 lines: the core · the 3 most important won't-dos · the score and how many rounds.

## Output

- `docs/SPEC.md` with change history.
- `docs/refs/` and its `README.md`, if screenshots were given.
- `START-HERE.md`, after approval.

Re-run in a folder with `docs/SPEC.md`: read it and its history, continue that version, never start a new one.

## Do not

- Write code, create a project or install anything.
- Suggest the next step before a 9-10 score.
- Invent users, quotes, numbers or reference products the user has not used.
- Promise outcomes.
- Copy the Citeable spec's content; take only its shape.
- Put screenshots with other people's personal data in a public repo.
- Print or write an API key.

## Eval

| # | Check | Target |
|---|---|---|
| E1 | Sections 2-6 present; section 4 has the core/shell table and the ICP → UI table | 100% |
| E2 | Won't do has at least 3 concrete lines | 100% |
| E3 | Every "Phase 1 is done when" line has a check | 100% |
| E4 | Questions asked before writing | ≤ 3 |
| E5 | Quotes or numbers (thresholds included) without source, `TODO` or "agent suggestion" | 0 |
| E6 | Next step suggested before a 9-10 score | 0 |
| E7 | Lines of application code written | 0 |
| E8 | ICP → UI rows whose trait has neither a source nor a `TODO` | 0 |

## Improve from use

After each use: log which part needed the most rounds, with the comment. Once a spec has been built into an MVP, check whether the building agent did anything on the Won't do list; if so, sharpen how section 5 is written.
