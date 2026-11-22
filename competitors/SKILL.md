---
name: competitors
description: Build a sourced competitor list for your product. Searches "<brand> competitors" and "<brand> alternatives" (plus local-language queries), keeps 5-10 products and substitutes after you approve the list, records annual revenue and headcount with year and source, drafts a 20-minute hands-on trial plan for each, and picks 2-3 to tear down on pricing. Outputs competitors.csv, competitors.md and a 3-line debrief. Use when someone says "find competitors", "competitor list", "alternatives to X", "who competes with X", or Build to Own Master week 3 assignment 1. Not for a full market report or sizing (use market-research), a competitor's pricing (use pricing-teardown), or a feature clean-room spec (use teardown).
metadata:
  category: business
  version: "0.1.0"
  sources: "sonpiaz/bto-master `master-scan-competitors` v0.0.3"
---

# /competitors

## Goal

**One competitor table with numbers**: each row has annual revenue, headcount, revenue per employee, year of each figure, source, and a "tried it" column. It feeds `/pricing-teardown` and `/pricing`.

> "Brand name plus the word competitor or alternative." "This report is old; sometimes you have to verify it again." "Once you have your competitors, go in and use their product." (Son Piaz, Build to Own Master, week 3)

## Agent's part, your part

| Agent does | You do |
|---|---|
| Finds local and international competitors, with links | Name your product, or a brand you are aiming at |
| Finds revenue and headcount with year and source | Pick which competitors to keep |
| Drafts a trial plan for each | **Sign up and try them yourself**, note strengths and weaknesses |
| Picks 2-3 to tear down on pricing | Agree or change |

Do your part first. When a step needs the user, stop and say exactly what is needed; do not guess.

## Inputs

Read first, ask only what is missing: `~/.bto-master/me.md`, `winning-product.config.md`, `pricing-model.config.md` in the working folder if present. If `competitors.csv` exists, update it; do not start over.

Ask on the first run, save to `competitors.config.md` in the working folder:
1. **Starting point**: a brand winning in the niche (e.g. Teachable), or one sentence describing your product.
2. **Market**: Vietnam, international, or both (search both sides when both).
3. **Currency** for the whole table: USD or VND; convert others and note rate and date.

## Steps

### 1. Find competitors
- Only a description, no brand: search it (`best <product type> software`), pick 2-3 leaders, ask which is the `anchor`, then run the searches below.
- Search `<brand> competitors` and `<brand> alternatives`. Vietnam: add `đối thủ <brand>`, `phần mềm <job> Việt Nam`.
- Gather 8-15 candidates, drop duplicates and closed ones, keep **5-10**. Show the list for approval before looking for numbers.
- Type each row: `anchor` (the starting brand, always one row), `product` (same kind as yours), or `substitute` (hiring, agency, spreadsheet, plugin). Keep both products and substitutes.
- A different model from yours (marketplace vs. tool): keep it, note the difference.

### 2. Revenue, headcount, revenue per employee
Follow the **Revenue per employee (ARPE)** rule in `/market-research` (`~/.claude/skills/market-research/SKILL.md`, Analyze): source confidence, stale figures, ranges, ARR, two sources for the top 3, the one-year match, `suspect`, `n/a` for substitutes. Not found: `unchecked`. Never invent or estimate in place of a source. Add one efficiency line for the table.

### 3. Trial plan: your part
For each competitor: free plan or trial length, card required (`page does not say` if silent) or demo only; sign-up link; 3 things to do in a 20-minute trial (e.g. create a course, open checkout, see the email students get). Column `tried` starts at `N`; after trying, set `Y` and write 3 strengths and 3 weaknesses in `competitors.md`. The agent **never creates accounts, enters a card, or logs in for you.**

### 4. Pick 2-3 to go deeper
Prefer real revenue (high or medium confidence) first, then closest to your customer. One sentence why each. Suggest `/pricing-teardown` for each.

### 5. Output
- `competitors.csv` in the working folder, columns: `name,link,type,market,annual_revenue,revenue_year,revenue_source,confidence,employees,employees_year,employees_source,revenue_per_employee,tried,trial_plan,notes`.
- `competitors.md`: readable table, the efficiency line, the 2-3 picks, blanks for strengths and weaknesses.
- Print both full paths. Re-runs update these two files, no dated copies.
- Debrief, 3 lines: strongest competitor and why · which numbers are stale or unchecked · which you will try this week.

## Do not

- Invent revenue, headcount or years; write a number without year and source.
- Create accounts, enter a card, or log in to a competitor.
- Write the commentary as certain; estimator figures are estimates.
- Print an API key.

## Eval

| # | Check | Target |
|---|---|---|
| E1 | Every revenue and headcount figure has year and link, or `unchecked` | 100% |
| E2 | Figures older than 2 years are marked stale | 100% |
| E3 | Revenue per employee only where the two figures are ≤ 1 year apart | 100% |
| E4 | Every competitor has a trial plan and a `tried` column | 100% |
| E5 | No account created, no card entered | 100% |
| E6 | Both local and international rows when the market is both | 100% |
