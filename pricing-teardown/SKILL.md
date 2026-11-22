---
name: pricing-teardown
description: Tear down a competitor's pricing into every way it charges. Reads the pricing page, its FAQ, terms and billing docs; lists each revenue line (subscription, seats, usage, transaction %, add-ons, white label, enterprise, done-for-you) with a quote or link; finds hidden fees and price jumps; computes the total monthly bill at 3 customer sizes; maps each line to the 11 business models. With 2-3 competitors, merges them and proposes 3-6 ways for you to charge. Outputs pricing-teardown.md. Use when someone says "tear down their pricing", "how does X charge", "hidden fees", "competitor pricing analysis", or Build to Own Master week 3 step 4. Not for setting your own price (use pricing) or a feature teardown (use teardown).
metadata:
  category: business
  version: "0.1.0"
  sources: "sonpiaz/bto-master `master-teardown-pricing` v0.0.2"
---

# /pricing-teardown

## Goal

For each competitor, **every way it charges**, sourced, plus the total a customer pays at 3 sizes. After 2-3 competitors, **3-6 ways to charge** for your product, each with a reason.

Example from class: Teachable looks like one $39 or $189 plan, but has 5 revenue lines including an active-student limit; an account with 9,000+ active students on a 100-student plan was quoted **$913.80 a month** (2026-11-05). The real fee often sits in the terms or usage-fee page, not the pricing page. Always read the vendor's own current pages.

Reads other people's prices to learn from them; setting your own number is `/pricing`.

## Agent's part, your part

| Agent does | You do |
|---|---|
| Reads pricing page, FAQ, terms, billing docs, quotes each line | Give a pricing link, or pick from `competitors.csv` |
| Lists revenue lines, hidden fees, price jumps | Choose 3 customer sizes like yours |
| Totals the bill at 3 sizes, maps to the 11 models | Check behind the login while trialling |
| Merges 2-3 competitors, proposes 3-6 ways to charge | Choose the final ways |

## Inputs

- A pricing link, a screenshot, or a name from `competitors.csv` (from `/competitors`).
- If `pricing-teardown.md` exists, add new competitors; do not redo finished ones.
- Ask once, save in `pricing-teardown.md`:
  1. **3 customer sizes** to total. The customer is whoever would pay for *your* product (course app → creators). Default small, medium, large; use real customer sizes if the user has them.
  2. **Average order value**, if there are per-transaction fees. Default $50, labelled `assumption`.
- Competitor bills in a different unit than the user gave (Kajabi per contact vs. students): convert, label the conversion `assumption`.

## Steps

### 1. Read every source
Pricing page, its FAQ, terms, billing or limits docs, changelog or price-change notices. Record the read date. Anything only visible after login: `check during trial`.
- "Unlimited" on the pricing page may not be; check terms and usage-fee pages.
- The vendor's own pages beat blogs, reviews and coupon sites; use outside sources only when the vendor is silent, and label them.
- Two pricing regimes (legacy vs. new customers): total on the new-customer one, one line for the other.

### 2. List each revenue line
One row each, with a short verbatim quote or a link to the exact section.

| # | Line | Yes/no | Details (numbers, limits) | Source | Model |
|---|---|---|---|---|---|
| 1 | Monthly or annual subscription, annual discount | | | | |
| 2 | Per user or seat | | | | |
| 3 | Usage (active students, calls, tokens, storage, emails) | | | | |
| 4 | % per transaction | | | | |
| 5 | Per product or project | | | | |
| 6 | Paid add-ons | | | | |
| 7 | White label, remove branding, custom domain | | | | |
| 8 | Custom or enterprise (contact us) | | | | |
| 9 | Done-for-you, setup, training | | | | |
| 10 | Trial: days, card required | | | | |
| 11 | Refunds | | | | |
| 12 | What you lose when you stop paying (data, customers, content) | | | | |

- A limit that only separates tiers, with no price of its own: `No, tier gate only`, limit in details.
- **"N ways to charge"** counts only rows 1-9 that have their own price or fee. Rows 10-12 are terms.

### 3. Hidden fees and price jumps
Every place the customer pays more than the headline price: going over a limit, transaction fees, near-mandatory add-ons, a forced upgrade for one feature. For each: which threshold, and the new price.

### 4. Total at 3 sizes
Table: size · required plan · subscription · usage fees · platform transaction fees · card processing · add-ons · **monthly total** · total without card fees (everyone pays card fees; separate them to see what the competitor really takes). Label every agent assumption `assumption`. A fee that depends on an unknown (how many students are billable): give a low-high range, do not pick one.

### 5. Map to the 11 models
Use `~/.claude/skills/pricing/business-models.md`. Fill the Model column for each row of step 2. No clean fit: `closest: <model>` or `no fit`; do not force it.

### 6. Merge 2-3 competitors and choose for yourself
With 2 or more torn down:
- Merged table: rows are revenue lines, columns competitors, cells yes/no.
- Propose **3-6 ways to charge** for the user's product, one reason each based on their customer.
- Starting point: 1-2 ways now, the rest added as customers grow.
- 3 things to learn, 1 to avoid (e.g. locking customers in with their data, making them feel trapped).
- Suggest `/pricing` to set the actual numbers.

### 7. Output
- `pricing-teardown.md` in the working folder, one section per competitor, the merge at the end. Print the full path.
- Every conclusion is a suggestion to check, not a claim.
- Debrief, 3 lines: ways to charge per competitor · biggest hidden fee found · the 3-6 ways you chose.

## Do not

- Invent prices, limits or percentages; unreadable means `unchecked` or `check during trial`.
- Sign up, enter a card, or log in to see prices.
- Copy a competitor's pricing page into the file; quote briefly and link.
- Set a price for the user's product (that is `/pricing`).
- Print an API key.

## Eval

| # | Check | Target |
|---|---|---|
| E1 | Every revenue line has a source (link or short quote) or a check label | 100% |
| E2 | The step 2 table has all 12 rows, including "no" rows | 100% |
| E3 | Totals at 3 sizes, assumptions labelled | 100% |
| E4 | Every line mapped to one of the 11 models (or `closest`/`no fit`) | 100% |
| E5 | With 2+ competitors: 3-6 ways to charge, each with a reason | 100% |
| E6 | No price set for the user's product, no account created | 100% |
