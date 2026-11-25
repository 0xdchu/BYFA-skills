---
name: mockup
description: "Build a clickable end-user mockup from a user flow, PRD or system architecture into a gallery that lists every screen, where each screen opens as a real page with hover and focus states, loading to complete states, web and mobile, light and dark, seeded demo data, and a Playwright check that proves the routes, states and overflow. Also a single-file mode from a product spec: mockup/index.html with every screen state, a \"Mockup states\" panel and shareable #state= links, offline. Use when saying \"build a mockup\", \"make a clickable prototype\", \"turn this user flow into screens\", \"mockup gallery\", \"prototype the app UI\", \"dựng mockup\", \"làm mockup\", \"mockup bấm được\", \"mockup/index.html\", or when a user-flow or architecture artifact exists and the UI must be seen before code. Don't use when drawing a diagram or one-page explainer (use archify), when only reviewing an existing UI, or for a single static page with no interactions."
---

# /mockup

Turn a flow into something a person can click: a gallery of every screen, each opening as a real page.
Static HTML, no framework, no backend — the point is to see and approve the UI before code exists.

## When to use

- A user flow, PRD or architecture artifact exists and someone asks to "see it" as an app.
- A feature needs a clickable prototype for review, a demo, or a pricing/onboarding decision.
- You catch yourself rebuilding the same gallery + router + theme + check script a second time.

## Don't use when

- The ask is a diagram, flow chart or one-page explainer — use `archify`.
- The ask is to review an existing UI, not to build one.
- The work is one static page with no states, routes or interaction.
- The input is only a screenshot and no written flow. Ask for the flow in words or a URL first.

## Read first

1. The flow or architecture artifact (role × stage, or screen list). Name the source in the mockup README.
2. The product's existing design language (tokens, font, mascot or brand assets) if one exists.
3. `template/` in this skill: shell, tokens, router, state machine and `check.mjs`.

## Steps

### 1. List screens from the flow
- Do: one screen per role-stage where the user decides or acts; drop steps with no UI (emails, backend jobs). Group them (onboarding, core loop, billing, config, support — add or drop groups for this product).
- Done when: a table of `id · title · group · one-line purpose` exists, and every flow stage maps to a screen or is named as intentionally omitted.

### 2. Fix the design language
- Do: if the repo has `design-systems/` (the coding-playbook repo carries six: shadcn for modern SaaS, Radix for app UI, Open Props for playful products, Fluent for Microsoft-style productivity, Carbon for enterprise consoles, Flex for luxury/private-banking editorial), pick one, copy its `tokens.css` and `components.css` beside the mockup and link them before `styles.css`. Otherwise:
- Do: tokens for light and dark, one accent colour, a heading face, and the asset rules (mascot size, background, one pose per screen). If the product has no brand, choose a neutral pair and say so.
- Done when: the copied system's `tokens.css`, or `styles.css :root` and the dark block, hold every colour and font the screens use; no inline hex in screen markup.

### 3. Copy and rename the template
- Do: copy `template/` into the repo (`labs/app/`, `app-mockup/`, …), replace product name and copy placeholders.
- Do: the device frame is a 390px box inside the desktop viewport, so `@media` queries never fire inside it. Write mobile layout as `.device-mobile ...` rules (or container queries on an inner wrapper), and check at 390 for real.
- Do: give the frame `transform: translateZ(0)` so `position: fixed` children (tab bar, sheet, toast) stay inside the 390px box instead of pinning to the browser window.
- Do: keep the global `[hidden]{display:none!important}` from the template; any component rule that sets `display` otherwise beats the `hidden` attribute (a menu stayed open in the aipub run).
- Do: grid and flex children that hold long text or chip rows get `min-width: 0`; without it they force horizontal scroll at 390 (two aipub screens overflowed until this was added).
- Done when: `index.html` opens over `file://` and the gallery renders without a server.

### 4. Write the demo seed
- Do: real-shaped copy for one example user, states included (`pending`, `approved`, `empty`). Seed the screen at the state where the flow **starts**, not after it — if a screen shows a connected source, either add the connect step or label the seed. Mark demo data in the README.
- Done when: `node -e "console.log(require('./data.js').screens.length)"` prints the screen count.

### 5. Render screens and the gallery
- Do: one render function per screen, registered in `RENDER`; one gallery card per screen, showing a live scaled thumbnail and Open/Mobile links. States (empty, loading, complete) live inside the screen and are reached by clicking, not as extra cards. No element `id`s inside screens — thumbnails render them more than once. Never wrap a whole screen or preview in an `<a>`; screens already contain links and buttons.
- Do: scale each thumbnail from its card's real width (measure on render and resize), not a fixed `scale()`; a fixed factor leaves gaps or crops when the grid changes columns.
- Do: diagrams or maps copied into the mockup folder so the team can open them (user flow, sequence, system map) are copies, not sources. Add a check assertion that each copy is byte-identical to its source file, or it drifts silently after the next edit to the source.
- Done when: every screen opens from the gallery, and the thumbnail matches the page.

### 6. Wire interactions and states
- Do: router, theme persistence, web/mobile toggle, and one state machine per async action (`idle → loading → complete`, plus error where real). Hover and keyboard focus must both be visible; hover changes colour and font weight.
- Done when: generate/approve/save show a spinner or skeleton, then a success state, without reload.

### 7. Prove and deploy
- Do: run `check.mjs`; rewrite its screen ids and selectors for the real screens while keeping each assertion's intent (a counter or list changes, a route renders, theme persists), adapting direction to the flow, then fix until 0 fail.
- Do: deploy only when a repo and target (Vercel/project, Pages) are given: static, root = the folder, build/install empty, output `.`, noindex header. Otherwise a green local check is done.
- Do: the link the team receives must open without a login. Vercel branch previews sit behind Vercel SSO by default and private chat artifacts open only for their owner, so neither is a share link; use the production URL of a noindex mockup project (or ask before turning preview protection off). In the aipub run the owner rejected a private artifact link because it had to go to the team.
- Do: after the repo moves to another GitHub owner, the Vercel project keeps deploying only from the CLI until an admin of the new owner installs the Vercel GitHub app on that repo and `vercel git connect <url>` runs again; say so instead of assuming merges deploy.
- Done when: `node check.mjs` exits 0, and if deployed the live URL returns 200 with the full gallery of cards.

## Design-system variants (optional)

Use when the owner wants the same screens in another design system to compare direction. When the owner names two systems with "or", build both behind one selector: in the aipub run the owner compared, dropped one (Carbon) and asked for more until six systems sat side by side (Fluent 2, Material 3, shadcn/ui, Ant Design, Polaris, Atlassian).

- Do: one extra stylesheet (`skins.css`) scoped by `<html data-skin="<name>">` that changes only tokens (colour, font, radius, shadow) and component shapes (tab indicator, nav selection, field style, notification border). Screens, copy and behaviour stay the same, so the comparison is fair.
- Do: a selector in the mockup chrome, saved with the rest of the mockup state, and a `?skin=<name>` query so a link opens the right variant. Light and dark for each variant.
- Do: keep the variant list in one place each: the `SKINS` array in `app.js`, one `<option>` per variant, and in `check.mjs` one map `{ name: [font substring, card radius] }` that the per-variant loop reads. Adding or dropping a system is then one CSS block plus three one-line edits.
- Do: per variant in `check.mjs`: the choice survives reload, the computed font and card radius match the system, no horizontal overflow on every route at 390 and 1440, the `?skin=` link works, and switching back removes the variant. When a variant is dropped, a saved or linked old name must fall back to the default; assert that `?skin=<dropped>` changes nothing.
- Do: a skin that sets `font-weight` on `.btn` silently cancels the base `.btn:hover` weight change (same specificity, later file wins), so re-declare `.btn:hover` weight in every skin that sets it; the hover assertion catches it only if it runs per variant.
- Do: match the specificity of the base field rule. The template styles fields with `input:not([type=checkbox])…`; a skin rule for inputs inside a wrapper (search box, select pill) needs the same `:not()` chain or it loses, and the wrapped input shows a second border (Atlassian search box in the aipub run). Look at a screenshot of a page with a search box and a filter select for each variant.
- Do: declare a non-public system font first (`"Atlassian Sans", -apple-system, …`, `"Segoe UI Variable Text", …`) so the computed `font-family` still names the system for the check, and say in the README that the browser shows a fallback. Keep the selector label readable at 390 (the longest name, "Material 3", was cut until the select got 118px).
- Don't: copy the other company's logo or assets; take token values from the system's public documentation. A system font that only ships with one OS (Segoe UI) falls back elsewhere; say so in the README.
- Done when: the check is green for every variant and the README names the variants and the link format.

## Single-file mode (from a product spec)

Use when the input is `docs/SPEC.md` (and `docs/FLOW.html`) from `/product-spec` and `/userflow`, or the user wants one file that runs offline with no Node. Output `mockup/index.html`, `mockup/STATES.md`, and `mockup/assets/` only if a logo is used. Edit an existing mockup in place.

1. **Screens × states table first.** Each main screen in the spec is a group with `loading`, `empty`, `error`, `success` plus screen-specific states from the spec or FLOW (e.g. `link-expired`). Any other state you add is labelled "agent suggestion"; nothing outside the table is built. A state that does not apply: `not applicable, <reason>`, the same sentence in the table and in the states panel. A FLOW branch marked `unclear` gets no screen, only a panel line `<branch>: unclear, see open question`. Save to `mockup/STATES.md` and confirm once: "N screens, M states, right?"
2. **One file.** Inline CSS and JS, no framework, no build, no network at runtime. Light by default, colours as `:root` variables, `tabular-nums` for numbers. Layout from the spec's UI section, else left menu and centred content. A screen outside the app shell (a public page opened from a link) has no menu and is reached only from the states panel.
3. **Really clickable.** Primary buttons navigate, forms validate, modals and drawers open and close, long actions after a real click fake `loading` with `setTimeout` then show the result; jumping to `loading` stays on the skeleton. Real navigation writes `#<screen>`; `jump('<screen>--<state>')` writes `#state=<screen>--<state>` (English kebab-case, split at the first `--`). On load and on `hashchange`, `#state=` calls `jump`, `#<screen>` opens it at `success`. A shared link opens the exact state.
4. **Seeded demo data**, consistent across screens (same names, totals add up), commented as demo; no real people's names, emails or phones.
5. **"Mockup states" panel** `/* mockup controls (not part of the product) */`: dark, fixed bottom-right, collapsible, open on desktop; one group per screen numbered as the spec, one button per state, "Start over", and a line saying the real buttons work too. At ≤ 760 px: a collapsed full-width bar at the bottom, opens to max 60% height with inner scroll, page gets matching `padding-bottom`. Menu collapses to a top bar, wide tables scroll inside their box, no page-level horizontal scroll at 390 px.
6. **Logos:** other brands only as real files from dashboard-icons (`https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/<name>.svg`) or lobehub (`https://unpkg.com/@lobehub/icons-static-svg@<pinned version>/icons/<name>.svg`), downloaded into `mockup/assets/` and opened to confirm they are the right mark. Not found in either: the name as text. Never draw a logo or use an emoji. The product's own logo: the user's file, else a square with its initial.
7. **Self-check:** headlessly click every panel button (each state renders, 0 console errors), walk the real buttons in FLOW order from first screen to result, screenshot 2-3 screens at 390 and 1440 px. Without a browser, list these steps for the user and say what was not checked.
8. **Feedback loop:** UI feedback (copy, colour, position) changes the mockup. Behaviour feedback (add a step, drop a screen, change a rule) changes the mockup **and** proposes the exact edit to `docs/SPEC.md` (and `docs/FLOW.html` if affected); edit the spec only with consent, and add a line to its change history. When the user says it is right: set the spec's "Mockup" line to `mockup/index.html`, add it to `START-HERE.md`, suggest `/usability-test` on this file first (in person, or deployed as Steps "7. Prove and deploy" says for remote sessions), then building only the core of Phase 1 (`/sdlc` if available).

## Don't

- Never invent testimonials, user counts, ratings or "live" numbers. Demo copy is labelled demo.
- Never describe a trade-secret mechanism in UI copy; show the surface, not the internals.
- Never add a backend, auth, analytics or a CDN script to a mockup unless asked.
- Never ship a page that only works at desktop width; 390 is part of done.
- Never call it done on screenshots alone; the check script is the proof.

## Done when

- `node check.mjs` exits 0 (routes, theme persistence, hover colour + weight, loading → complete, 1440/390 no overflow, 0 console errors; copied diagrams equal their sources; each design-system variant if any).
- The gallery lists every screen, and each opens on web and mobile, light and dark.
- If deployed, the live URL is 200 and `X-Robots-Tag: noindex`.

Next: a green check proves the screens render, not that people can use them. Suggest `/usability-test` with the share link (single-file mode: the offline file, see its step 8) before any code.

## Eval

| Metric | How to measure | Target |
|---|---|---|
| Invoked at the right time | 5 should-invoke + 5 sound-alike-but-shouldn't phrases, count correct | ≥ 9/10 |
| Screen coverage | every stage of the source flow has a card and a route | 100% |
| Proof green | `node check.mjs` exit code | 0 every run |
| Hand fixes after the first build | count per run | down to 0 |

## Feedback log

| Date | What happened | What changed |
|---|---|---|
| 24/11/2026 | aipub skins v2 and v3: Carbon dropped, Material 3, shadcn/ui, Ant Design, Polaris, Atlassian added (check 101 → 118); a double border on wrapped inputs found only from a screenshot; the mobile selector label was cut | Variants section: build both when the owner says "or", one list per place, dropped-name fallback, hover weight per skin, field specificity, non-public fonts, label width |
| 24/11/2026 | aipub mockup rebuilt to the new landing (13 screens, 91 → 101 assertions): fixed by hand a `hidden` menu that stayed visible, 390px overflow from grid children, fixed-scale thumbnails; owner rejected a private artifact link for team review; Vercel stopped deploying from git after the repo moved owner; owner asked for Fluent 2 / Carbon versions | Step 3 frame transform, `[hidden]`, `min-width: 0`; Step 5 measured thumbnails and copied-diagram check; Step 7 share links and git reconnect; new design-system variants section |
| 23/11/2026 | Merged Build to Own Master `master-clickable-mockup` v0.0.2 | Added single-file mode: states table, `#state=` links, states panel, logo sources, spec feedback loop |
| 20/11/2026 | Trial 2, fresh agent on a 4-stage flow (8 screens): 53 pass, 0 fail; asked whether states get their own cards and how literal "keep every assertion" is | Step 5 one card per screen, states by click; Step 7 assertion intent; groups include billing |
| 20/11/2026 | Trial 1, fresh agent on a 4-stage flow (10 screens): 72 pass, 0 fail; guessed at mobile-frame media queries, check selectors, seed state | Added the 390px frame rule, check-selector step, seed-at-start rule, focus assertion, deploy scope |
| 20/11/2026 | Created from the aipub app mockup (11 screens, gallery + Vercel); trialed on that case | v1 |

## This skill must improve itself

1. **Eval after every run.** Grade the table; any missing step goes back into this file with one log row.
2. **Look things up occasionally.** Playwright launch flags, Vercel project settings and font URLs change.
3. **With a stronger model, rerun the trial.** Drop lines it no longer needs.
4. **When unsure, ask a human.**
