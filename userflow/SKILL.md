---
name: userflow
description: Design or review a software user flow to a defensible standard — one primary actor and goal, entry and exit, happy path, decision and error branches with recovery, a flow-spec table, accessibility notes and measurable success criteria, drawn as one offline-ready docs/FLOW.html (core flow, key exchange, roles) from a product spec; grounded in ISO 9241-210/11/110, ISO/IEC 25010 and WCAG 2.2. Use when saying "design a user flow", "review this user flow", "make a flow spec", "chuẩn hóa user flow", "vẽ luồng người dùng theo chuẩn", "vẽ user flow", "FLOW.html", "swimlane", or when a flow has no error branches, actors or success criteria. Not for sequence diagrams or code-traced request flows (use graph, which can also render the checked flow), clickable screens (use mockup), or architecture/C4 diagrams (use archify).
---

# /userflow

Turn a vague journey into a flow a team can build, test and review. The deliverable is a **flow spec** plus a diagram brief; the diagram is a view of the spec, not the spec itself.

## When to use

- A product flow is being designed, critiqued or handed to engineering.
- A diagram has boxes but no actors, entry/exit, failure paths or success criteria.
- Someone says "user flow", "flow spec", "luồng người dùng", "chuẩn hóa flow", "review flow".

## Don't use

- Sequence diagrams or code-traced request flows: use `graph`. To render the checked flow as an offline HTML diagram, use `graph` workflow or sequence; this skill owns the spec and review.
- Clickable screens or prototypes: use `mockup`.
- Architecture, C4 or service maps: use `archify` or Structurizr.

## Standards that apply

There is no ISO/IEC standard for the drawing itself. Apply the layers around it:

| Layer | Standard | What it gives the flow |
|---|---|---|
| Process | ISO 9241-210:2019 | Context, user requirements, design solution, evaluation; the flow is evaluated, not just drawn. |
| Usability | ISO 9241-11:2018 | Exit criteria: effectiveness, efficiency, satisfaction in a stated context. |
| Interaction | ISO 9241-110:2020 | Seven principles per step: task fit, self-descriptive, expectations, learnable, controllable, error-robust, engaging. |
| Quality | ISO/IEC 25010:2023 | Interaction capability as a product-quality requirement. |
| Accessibility | WCAG 2.2 / ISO/IEC 40500:2025 | Keyboard, focus, labels, error identification, contrast, target size. |
| Notation | BPMN 2.0.2 / UML 2.5.1 | Use only when a formal cross-role or software model is required; never mix notations. |

Open [reference.md](reference.md) for the full checklist, table template and review rubric.

## Steps

**Stop rule.** If actors, permissions, recovery behaviour or metric baselines are missing from the prompt or code, stop and ask. In a one-shot run, mark the gap `[?]` and the step `unmeasured`; never invent it.

1. **Fix scope.** Name one primary actor, one goal, one entry point and one exit. If two actors each make decisions, write one flow per actor and show the other as a handoff. If there are two goals, write two flows.
2. **List actors and handoffs.** Human roles, the product, external services. Mark who decides and who only receives.
3. **Write the happy path first.** Number every step. Keep the shortest path that achieves the goal.
4. **Add branches.** Decision, validation error, external failure, timeout, cancel, permission denied. Every failure branch names a recovery and where it returns; a dead end is a defect.
5. **Add preconditions and results.** State what must be true before the step and what is true after it. Include data created or changed.
6. **Annotate accessibility.** Keyboard path, focus order, label, error text, contrast, target size, no colour-only signal.
7. **Define measurement.** Completion per step, time, error rate, retry rate, drop-off. Do not invent targets before a baseline. Then write the **event plan** that will produce those numbers once the product is live (template in reference §2):
   - One event per flow-spec row whose completion or drop-off is measured, plus one per failure branch that has a recovery. Name it `object_action` in `snake_case`, one name one meaning (`project_created`, `post_approved`, `payment_failed`), as `/posthog` Step 4 does; where Step 4 already requires a name for this site type (`user_signed_up`, `checkout_started`, …), use that name.
   - For each event: the flow step number, when it fires (the result column, not the click: `post_approved` fires when the approval is saved), its properties (only what a metric needs; no email, name or free text), and where it is sent from. Money and anything confirmed by a server fires from the server.
   - Map each metric in the metrics table to the events it is computed from (completion of step 4 = `post_approved` / `draft_opened`). A metric with no event is marked `unmeasured`.
   - Hand the event plan to `/posthog` when the product is wired; this skill names events, it does not install tracking.
8. **Choose notation and write the diagram brief.** A simple flowchart for one actor is enough. Use BPMN for pools/lanes and gateways across roles; use UML activity for software logic. The brief carries actors, boundary, entry/exit, failure group, legend and source (reference §6).
9. **Draw or update the diagram, then check parity.** Every row in the spec appears in the diagram and every branch in the diagram appears in the spec. Give the brief to `graph` if an offline HTML diagram is wanted.
10. **Review against the gate.** Use the Blocker / Should fix / Nit rubric in reference §4 and fix every blocker before handoff.

## FLOW.html output (default diagram)

When the flow comes from a product spec (`docs/SPEC.md`, see `/product-spec`) or the user wants one file to open in a browser, draw `docs/FLOW.html` from `flow-template.html` next to this skill. Edit an existing `docs/FLOW.html` in place.

- **Read the spec into 4 lists:** screens (number and name as in the spec), roles (the user groups in the spec's user table, name before any bracket, plus `System` for the product itself; add no others), third parties in Phase 1 only, and the one most important exchange (money, customer data, or an AI call).
- **Required sections, in order:** `1. Core flow` (`flowchart TD`, first screen to result, main error branch, loop if the product repeats) · `2. <exchange name>` (`sequenceDiagram`, `alt` for branches, `loop` for repeats; product is `participant System`) · `3. Roles` (`flowchart TD`, one `subgraph` per role) only when the spec has 2+ user groups, otherwise drop it and say why in the subtitle. Optional, at most 2 more: a secondary diagram, `Layout` (the `.wire` block, only if the spec has a UI section; otherwise delete it and rename "Flow and Layout" to "Flow"), a small number table. Renumber after dropping a section.
- **Template:** replace every placeholder (`PRODUCT_NAME`, `SPEC_VERSION`, `YYYY-MM-DD`, `LANG`, notes, `.wire` text, diagram bodies) and delete the guidance comment. Keep the light background, white `.card` per diagram, system font, numbered `<h2>`, and the pinned Mermaid import. Headings in English; notes and diagram text in the spec's language.
- **Diagram rules:** every arrow labelled (`A -->|clicks Continue| B`, `U->>S: sends request`). Short ASCII node ids, display text in quotes. No `;` or `#` in sequence messages; no `<` except `<br/>`. Screen, role and button names exactly as in the spec. Max 15 nodes per flowchart, 6 participants and 15 messages per sequence, 4 roles and 12 nodes per Roles diagram; split beyond that. One `p.note` under each `<h2>` saying what question the diagram answers.
- **Gaps in the spec:** do not decide. Draw the branch with label `<action>, unclear` pointing at a node holding the question: reuse the spec's open-question number if it exists, else `Open question (proposed): …` and propose adding it. In a sequence: `alt <condition>, unclear` with `Note over`. Change the spec only with the user's consent.
- **Self-check:** open headlessly, wait for Mermaid; the number of `<svg>` equals the number of diagrams, no `Syntax error`, and at 1440 px no Roles SVG is shrunk below its `viewBox` width minus 1 px (split if so). Without a browser: `grep -nE -- '-->|==>|-\.->' docs/FLOW.html | grep -vE '\|.+\||-->>'` for unlabelled arrows, and ask the user to open it.
- **Hand-off:** full path, one line per diagram, the `unclear` branches, how to open (Mac: double-click or `open docs/FLOW.html`; Windows: double-click or drag into Chrome/Edge; first open needs internet for Mermaid). When the user says it is right: set the spec's "Flow" header line to `docs/FLOW.html`, add it to `START-HERE.md`, suggest `/mockup`.

The flow-spec table below stays required; FLOW.html is its view, and the parity check applies.

## Review mode

When reviewing an existing flow, do not redraw it first. Output findings under **Blocker / Should fix / Nit** from reference §4, each with the step or file and a concrete fix. A review is done when every blocker has a disposition and the spec/diagram parity check has run.

## Flow spec (required)

| # | Step | Actor | Precondition | Result | Failure / recovery |
|---|---|---|---|---|---|
| 1 | Entry | actor | how they arrive | what opens | broken link, no access |
| 2 | Action | actor | required data | system response | validation, retry, cancel |
| … | … | … | … | … | … |
| n | Exit | actor | success state | confirmation | support path |

Add a measurement column when the flow has a metric owner. Keep one row per user-visible step; backend-only steps belong in a separate technical flow.

## Review gate

- One primary actor, one goal, one entry, one exit; every node reachable.
- Happy path and at least one failure/recovery path are shown.
- Every decision has labelled exits; no unlabelled arrow.
- Actors and handoffs are explicit; permissions are not implied.
- Preconditions, results and data changes are stated.
- Accessibility notes exist for every input and error.
- Each step has a measurable success signal or is marked unmeasured.
- Notation is consistent and named; no mixing flowchart, BPMN and UML shapes.
- Every measured step and every recovered failure branch has an event in the event plan; no event fires on a click alone when the step's result is saved later.
- Checked, with the result in the flow spec's `## Review` section (reference §2): before a mockup exists, a documented inspection that walks every step against ISO 9241-110 and the WCAG checklist in reference §3; once `/mockup` exists, a round of `/usability-test`, its `findings.md` named there.

## Done when

- The flow spec table is complete and stored next to the diagram.
- The diagram matches the table; every branch in one appears in the other.
- A reviewer can trace entry → exit and every failure → recovery without asking a question.

## Don't

- Don't draw a "user flow" that is only screens in a line.
- Don't invent metrics, actors, permissions or error behaviour.
- Don't publish internal mechanisms or secrets in a public flow.
- Don't use BPMN/UML decoration without the semantics.

## Eval

| Metric | How to measure | Target |
|---|---|---|
| Flow completeness | Review gate items passed on a real flow | no blocker findings (reference §4) |
| Branch coverage | Failure/recovery paths present vs identified risks | every high-risk path has one |
| Spec/diagram parity | Steps and branches in table vs diagram | 100% match |
| Review usefulness | Reviewer questions that the spec could not answer | 0 |
| Event coverage | Measured steps and recovered failure branches without an event | 0 |

## Feedback log

| Date | What happened | What changed |
|---|---|---|
| 2026-11-20 | First version, built from an ISO/WCAG review of a public product flow | Added flow spec, failure band, accessibility and measurement sections |
| 2026-11-23 | Merged Build to Own Master `master-user-flow` v0.0.2 | Added the FLOW.html output section and `flow-template.html` |
| 2026-11-24 | A review of the UI design process found step 7 named metrics but no events, so the flow handed nothing `/posthog` could wire, and the review gate asked for a real-user check with no skill behind it | Step 7 now ends in an event plan (reference §2); the gate checks event coverage and points to `/usability-test` |
| 2026-11-20 | Fresh-agent trial on an invite/accept case: it split into two actor flows, marked metrics unmeasured, and asked whether two deciding actors need one flow or two | Step 1 now says one flow per deciding actor; added the stop rule for missing actors, permissions and baselines |
