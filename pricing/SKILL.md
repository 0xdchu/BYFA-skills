---
name: pricing
description: Choose a business model and price a product or service. Anchors price on what customers already pay to get the job done (hiring, freelancer, agency, doing it by hand), not on same-category software; picks from 11 business models, packages 3 tiers, defines a manual service to sell this week, and drafts price questions for 3 real people. Keeps the minimalist-entrepreneur principles (always charge, start low and raise, the financial-independence math). Outputs pricing-model.md and a debrief. Use when someone is setting or changing prices, picking a business model, packaging tiers, asking "how much should I charge", or doing Build to Own Master week 2. Not for a full competitor price teardown (use teardown) or market sizing (use market-research).
metadata:
  category: business
  version: "0.1.0"
  sources: "slavingia/skills `pricing` (The Minimalist Entrepreneur) + sonpiaz/bto-master `master-pricing-model` v0.0.5"
---

# /pricing

## Goal

**One business model and 3 proposed price tiers, each with a reason**, anchored on what customers already pay for this job elsewhere, plus a first step you can sell this week. Every number is a suggestion to test, never a claim.

> "Don't compare yourself with software sellers; compare yourself with the services they are already paying for." "Start with a service. Do it by hand first, then package it, and only then let AI do the repeated work." (Son Piaz, Build to Own Master, week 2)

## Principles

1. **Charge something. Always.** Free vs. $1 is a different market (the zero price effect). Free trials are fine, with a clear path to paid; don't confuse marketing with giving the product away.
2. **Anchor on the alternative, not on software.** The strongest anchor is what the customer pays a person, freelancer or agency today. Same-category software prices go in the table but are never the main anchor.
3. **Value over cost.** Know your cost floor (hosting, time, payment fees, margin), but price on value to the customer.
4. **Start low, raise over time.** Pricing is iterated, not fixed. Tiers are the goal (economy, business, first class).
5. **Service first.** Sell it by hand first, package it, then automate the repeated part.

## Agent's part, your part

| Agent does | You do |
|---|---|
| Finds the cost of hiring, freelancers, agencies for this job, with sources | Say what job the product does, for whom |
| Builds a short local + international competitor table | Give numbers you know from your market (salaries, local agency prices) |
| Proposes the model and 3 tiers, says why | Pick a tier, change prices |
| Drafts the price questions, summarises the answers | Ask 3 real people, record their words verbatim |

Do your part first. When a step needs the user, stop and say exactly what is needed; do not guess.

## Inputs

Read first, ask only what is missing: `~/.bto-master/me.md` and `winning-product.config.md` in the working folder if they exist, plus any product context on the machine (the product repo, its CLAUDE.md).

Ask on the first run and save to `pricing-model.config.md` in the working folder:
1. **What job the product finishes** for the customer, in one sentence.
2. **Who the customer is**: person or business, industry, size, country.
3. **How they do it today**, if known. If not, the agent looks it up and marks it as agent-researched.
4. **Market**: Vietnam, international or both. Pick **one** currency for the whole file (VND or USD); convert others and note the rate and date. Both markets: USD, unless most customers are in Vietnam.
5. **Monthly income you need** from this product (for the step 6 math). Optional.

On a later run in a folder that has `pricing-model.config.md`: read it, do not ask again.

## Steps

### 1. Who the customer pays today, and how much
At least **3 ways** the customer solves this job today, each with a cost. Default per month; for per-job work (a video, a project) use that unit and say so.

| Way | Example | Cost (with unit) | Source |
|---|---|---|---|
| Full-time hire | 1 employee doing this job | | job boards, salary surveys |
| Freelancer or agency | Upwork, local agency | | pricing or service pages |
| By hand | hours per week × owner's hourly rate | | user estimate |
| Software in use | | | pricing page |

- A number without a source is marked "unchecked"; never invented.
- The strongest anchors (local agency prices) are often not on the web: mark "unchecked" and turn it into a question in step 7.
- Savings for the customer = people doing the job × salary × share of their time spent on it, each number sourced.

### 2. Competitors, local and international
Short table: name · price · model · revenue, traffic or funding (only with a source). Include international competitors. For a deep dive offer `/market-research` or `/teardown`; do not run them unasked.

### 3. Pick from the 11 models
Read `business-models.md` next to this skill. Propose 1 main model, plus at most 1 combined model if it fits (e.g. subscription software plus a done-for-you plan). One sentence why, based on how the customer wants to pay.

### 4. Three tiers
| | Low | Middle | High |
|---|---|---|---|
| Name | | | |
| Price | | | |
| Includes (clear scope) | | | |
| Manual part vs. software or AI part | | | |
| For whom | | | |

- Put each price next to the step 1 anchor: "X times cheaper than hiring". A tier above the anchor: say so plainly, with why customers would still buy (faster, no one to manage) or propose a change.
- Check each tier against the cost floor: price minus variable cost per customer must leave a margin.
- The high tier is often done-for-you.

### 5. Step 1: a manual service to sell this week
One paragraph: what service, for whom, which part is done by hand, step-1 price. The repeated part is saved for automation later.

### 6. The math
Monthly income needed ÷ price = customers needed. At one new customer per business day (about 260 a year), when is that reached? Show it for the middle tier. Skip if the user gave no income target.

### 7. Ask 3 real people
Draft 4 questions; the user asks and records verbatim:
1. At what price would it be so cheap you'd doubt the quality?
2. At what price is it cheap, a good deal?
3. At what price is it expensive but you'd still consider it?
4. At what price would you not buy?

Add questions that fill any "unchecked" anchor ("The last time you paid someone for this, how much was it?"). When answers come back, summarise and propose tier changes. The agent never messages or calls anyone itself.

### 8. Output and debrief
- Prices the agent proposed without a source are labelled "agent suggestion".
- Write every number and conclusion as a suggestion to test ("suggested", "estimate", "check in step 7"), never "the right price is".
- Write everything to `pricing-model.md` in the working folder and print its full path.
- Debrief, 4 parts, for the group or a Campus submission: model and why · 3 tiers · anchors compared · open questions. Add when to revisit prices (after the step 7 answers, and after the first 10 paying customers).

## Do not

- Present a price or conclusion as certain.
- Use same-category software prices as the main anchor.
- Invent salaries, agency prices, revenue; unreadable means "unchecked".
- Promise revenue or customer counts.
- Contact anyone on the user's behalf.
- Print an API key.

## Eval

| # | Check | Target |
|---|---|---|
| E1 | Step 1 has at least 3 ways the customer pays today, each with a cost and unit | 100% |
| E2 | Every number has a source or "unchecked" | 100% |
| E3 | The main anchor is a step 1 cost, not same-category software | 100% |
| E4 | 3 tiers, each with all 5 rows, each checked against the cost floor | 100% |
| E5 | A step-1 manual service is defined | 100% |
| E6 | The agent contacted no one and promised no revenue | 100% |
