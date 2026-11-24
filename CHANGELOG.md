# Changelog

## 0.0.23 · 2026-11-24

- New skill `usability-test`: the "test with 5 users" step between `/mockup` and code. Plan with 3-5 tasks taken from the flow's success criteria (no UI labels, a visible success state each), a screener from the spec's user groups, consent and a moderator script; a pilot that is never counted; local transcription and screen frames; a task table in counts ("3 of 5", never "60%") and findings with quotes, 0-4 severity and where to fix (spec, flow step or screen). Nothing changes in the spec, flow or mockup before the owner picks the fixes.
- `product-spec`: section 4 gains an ICP → UI table (trait · what we know and its source · UI decision: device, frequency, comfort with software, apps they already use, what makes them trust a tool, their words), so layout follows the user groups in section 2; unknown traits become `TODO` or a warm-up question for `/usability-test`, never a stereotype. New eval E8.
- `userflow`: step 7 ends in an event plan (reference §2): one `object_action` event per measured step and recovered failure branch, fired on the result not the click, properties without personal data, server-side for money; each metric names its events; the plan goes to `/posthog`. The review gate checks event coverage and points the real-user check to `/usability-test`. `mockup` suggests `/usability-test` after a green check.

## 0.0.22 · 2026-11-24

- New skill `presence-audit`: audit how AI assistants, search and the press describe a person or brand, and fix what makes them wrong. `site_check.py` reads a site the way AI crawlers do (raw HTML, robots.txt per AI bot, JSON-LD `sameAs`, about and pricing pages); `consistency.py` compares the name and positioning sentence across profiles; `ai_sheet.py` builds the in-app answer check and diffs two dated runs. Separates being described correctly (checkable) from being recommended (measured as a mention rate, never promised).

## 0.0.21 · 2026-11-24

- `mockup`, design-system variants: build both systems when the owner says "or"; keep the variant list in one array, one option and one check map; a dropped name falls back to the default; re-declare `.btn:hover` weight in skins that set button weight; match the base field selector's specificity for wrapped inputs; name non-public fonts first; keep the selector label readable at 390. From the aipub six-system comparison.

## 0.0.20 · 2026-11-24

- `mockup`: optional design-system variants (one scoped `skins.css`, selector + `?skin=` link, a check per variant); share links must open without a login (not Vercel previews or private artifacts); reconnect Vercel git after a repo changes owner; frame `translateZ(0)` for fixed children, `[hidden]` and `min-width: 0` rules, thumbnails scaled from the card width, a check that copied diagrams equal their sources. From the aipub mockup rebuild.

## 0.0.19 · 2026-11-23

- New skill `team-sprint` (from Build to Own Master `master-team-sprint` v0.0.1): weekly meeting transcript to a meeting record and 5-part draft tickets (one assignee, deadline, label each); stops for Product to edit, and writes to Linear (document, issues in the current cycle, links) only after a clear approval; markdown export when there is no Linear MCP.

## 0.0.18 · 2026-11-23

- New skill `product-spec` (from Build to Own Master `master-product-spec` v0.0.2): 5-part spec, at most 3 questions, won't-do list, owner-scored review loop to 9-10.
- `userflow` and `mockup` move into this repo. `userflow` gains a FLOW.html output (from `master-user-flow` v0.0.2) with `flow-template.html`; `mockup` gains a single-file mode (from `master-clickable-mockup` v0.0.2): states table, `#state=` links, states panel, logo sources, spec feedback loop.

## 0.0.17 · 2026-11-23

- New skill `competitors` (from Build to Own Master `master-scan-competitors` v0.0.3): sourced competitor list, trial plans, 2-3 picks for a pricing teardown.
- New skill `pricing-teardown` (from `master-teardown-pricing` v0.0.2): every revenue line, hidden fees, totals at 3 customer sizes, mapped to the 11 business models in `pricing/`.
- `market-research`: new revenue-per-employee (ARPE) rule in Analyze; `competitors` uses it.

## 0.0.16 · 2026-11-23

- New skill `pricing`: merges the minimalist-entrepreneur pricing principles (slavingia/skills) with the Build to Own Master week-2 workflow (`master-pricing-model` v0.0.5): anchor on what customers pay today, 11 business models (`pricing/business-models.md`), 3 tiers, a manual service to sell first, price questions for 3 real people.
- `master-winning-product`: `render-table.py` parses again and tags Show HN rows as newly launched.

## 0.0.15 · 2026-11-15

- New skill `country-map`: find which countries a product or a competitor group sells in from Similarweb top-5 countries and Google Trends, calibrated with verified revenue per visit. Ships `scripts/` (Similarweb batch reader that stops at the daily trial limit, CSV parser, Trends region reader).

## 0.0.14 · 2026-11-10

- The coding-specific skills left this repo: `sdlc`, `agent-team`, `whats-next`, `create-skill` and `secrets` are no longer here (the 0.0.13 `sdlc` update went with it). Seven skills remain: `market-research`, `teardown`, `master-winning-product`, `page-quality`, `posthog`, `optimize-mac`, `event-review`. `setup` now removes a symlink of an earlier install whose skill left this repo.

## 0.0.13 · 2026-11-10

- `sdlc`: replaced with the newer version. Adds `clarify` (an intent cannot reach `approved` while an open point remains), a `## Tasks` section in the plan that feeds each builder's contract, and `converge` (lists changed files outside the plan's tasks, tasks left untouched and Proof items without a result). The skill now ships `sdlc/scripts/` (`sdlc-check.py`, `dispatch.py`, `contract.py`, standard library only), so it is no longer a single-file skill; the old `sdlc/SKILL.md` is gone.

## 0.0.12 · 2026-10-26

- `market-research`: substantial research now defaults to a browser-viewable HTML report with a verified direct URL using existing authorized hosting; keeps sensitive research private and does not create hosting accounts.

## 0.0.11 · 2026-10-26

- Merged the existing `market-research` skill with the `byfa-researchmarket` workflow; added sourcing, review, market sizing, finance, and investor/vendor diligence playbooks while preserving the existing chart workflow.
- Removed the `byfa-researchmarket` directory, updated README/install/contributing; `setup` removes the old symlink only when it points exactly at the removed skill.
- Preserved the SVG chart tool; clarified when to use matrix, sizing, and valuation methods; added Eval and feedback based on the Native research case.

## 0.0.10 · 2026-09-28

- Added `byfa-create-skill`, the skill-creation skill: first ask whether this should be a skill at all (one-off work gets a prompt; machine-blockable errors get a hook or script), then ask five questions, write `SKILL.md`, trial it on a real case in a fresh session, add a countable eval and a feedback log, and install into Claude Code or Cursor. Ships with `byfa-create-skill/TEMPLATE.md`, a one-page `SKILL.md` template with guiding notes. If installed via `setup`, re-run `git pull` and `setup` to receive the new skill.

## 0.0.9 · 2026-09-28

- Added `byfa-posthog`: audits your product's PostHog against a complete standard (project setup, SDK per site type, identify/reset, key events, reverse proxy), builds an overview dashboard set as the Home page, then re-measures to confirm numbers land in the right project. Ships with a dashboard layout example and a one-page checklist. If installed via `setup`, run `git pull` then `setup` to receive the new skill.

## 0.0.8 · 2026-09-28

- Member guide: count all nine skills correctly (install command and Method A heading still said eight), added `byfa-event-review` to the when-to-use table. README has been correct since 0.0.6.

## 0.0.7 · 2026-09-28

- Switched the `description` of `byfa-event-review` and `byfa-optimize-mac` to Vietnamese to match the other seven skills. Skill names stay English while descriptions stay Vietnamese so you know at a glance when to invoke them. Also fixed the `byfa-event-review` frontmatter bug (the old description contained a colon that broke YAML parsing). Names and invocation unchanged, no reinstall needed.

## 0.0.6 · 2026-09-27

- `byfa-event-review`: from a talk's recording or video plus slide images, rewrites each talk in full (no summarizing), with independent agent review and a completeness-measurement script. Example output: https://homus.dev. Original: https://github.com/0xdonniechu/event-review

## 0.0.5 · 2026-09-15

Fixed per the public security/content review (Grok, 09-15):

- Member guide: removed personal names; added `byfa-optimize-mac` warnings (`rm -rf` cache, no personal files, no `sudo`).
- Removed `CLAUDE.md` — internal notes, not shipped to users.

## 0.0.4 · 2026-09-15

Five wave-2 skills for users (Sessions 4–8):

- `byfa-sdlc` — artifact chain intent → plan → build → verify → ship
- `byfa-agent-team` — single approval, multiple agent roles, run to done
- `byfa-whats-next` — session triage, next-step recommendations (read-only)
- `byfa-page-quality` — page quality measurement, Core Web Vitals, post-launch
- `byfa-optimize-mac` — safe macOS RAM/disk cleanup

Added the member guide: install Claude Code + Cursor, verify skills, common errors.
README updated with the 8-skill table.

## 0.0.1 · 2026-08-30

First three skills, distributed for releases after Session 3:

- `giu-khoa` — keep API keys safe when delegating work to agents
- `research-market` — agent-driven market research, sourced numbers, TAM SAM SOM
- `teardown` — decompose products and rebuild under clean-room rules

## 0.0.2 · 2026-08-30

Renamed all three skills under Son's two new rules: the `byfa-`
brand prefix (following the OMC product-name-prefix pattern) and an English name part.

- `giu-khoa` → `byfa-secrets`
- `research-market` → `byfa-researchmarket`
- `teardown` → `byfa-teardown`

README gained a program intro, pointing to github.com/0xdonniechu/BYFA-skills.

## 0.0.3 · 2026-08-30

Four requirements from Son after Session 3, plus cross-checked content from the real transcript:

- Each skill gains a "When to use" section and a "This skill must improve itself" section:
  eval after each run, occasional lookups to update, ask the
  open-source community or Son Piaz when unsure
- `byfa-researchmarket` adds the 1-star/2-star review filtering technique and three validation
  methods (landing plus waitlist, talking to 5 real customers, preselling), exactly as taught
  live in Session 3
- `byfa-teardown` adds the IBM clean-room case told in Session 3
- Added CONTRIBUTING.md: fork, clone, open PRs, contribution rules, where to ask when stuck
