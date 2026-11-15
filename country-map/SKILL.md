---
name: country-map
description: Find which countries a product, or a group of competing products, has customers in; which markets are crowded, which have one winner, which are open, and where demand meets weak supply. Uses Similarweb top-5 countries per domain, Google Trends interest by country, and verified revenue as a calibration. Use when asked "which countries does X sell in", "where is this product dominant", "country map", "traffic by country", "blue-ocean market", "chiếm thị trường nước nào".
---

# Country map: where a product has customers

The question is not "what is the exact revenue per country". It is "where do these products already have customers, where is the market crowded, and where is demand left unserved". Data-driven inference is the goal: not absolute, but never baseless.

First run: 31 content-repurposing and social-scheduling tools, November 2026, in four short daily sessions.

## What you need
- A browser the agent can drive, logged in to Similarweb by the user. A free trial is enough. The examples below use the `orca` browser CLI (`orca goto`, `orca eval`); swap in your own browser tool.
- No paid plan: **the top 5 countries per product were enough** to see the picture. The full country list was not worth buying.

## Method

1. **List the domains, highest revenue first.** Take the group from your competitor research. Sort by known MRR or ARR (Stripe-verified listings first, founder statements next, aggregator estimates last). The trial runs out daily, so the products that matter most go first.

2. **Similarweb: monthly visits and the top 5 countries.**
   - `scripts/batch.sh <queue.txt> <out.csv>` reads one domain per line from the queue, opens Similarweb's geography and overview pages, appends rows to the CSV, removes finished domains from the queue, and stops at the daily limit.
   - CSV columns: `domain, period, monthly_visits, countries_total, rank, country, share_pct, date_read, source`.
   - Keep the queue file somewhere that survives the session; the work spans days.

3. **Calibrate revenue per visit.** For each product with a revenue figure: monthly revenue / monthly visits. In the first run, four anchors gave $0.05 to $0.32 per visit per month; the Stripe-verified one sat at $0.11. Drop an anchor that sits 20× away from the rest. It is usually a stale MRR or an aggregator guess. Multiply visits by the range to get an estimate band, and label it as an estimate.
   - Similarweb gives no revenue by country, so use country numbers to **rank** markets, never as a forecast.

4. **Demand by country: Google Trends.** Open `https://trends.google.com/trends/explore?date=today%2012-m&q=<keyword>`, wait about 15 s, then run `scripts/trends.js` in the page (for example `orca eval --expression "$(cat scripts/trends.js)"`). It pages through "Interest by region" and returns `Country=index;...`. Use 5 to 7 category keywords, not only brand names. If a keyword has no country data, use a close synonym.

5. **Classify every country.**

   | Class | Signal |
   |---|---|
   | Crowded | many products have it in their top 5 |
   | Has a winner | 1 to 4 products, one clearly leads there |
   | Open, no leader | several products, none above about 10% of its traffic |
   | Demand, weak supply | high Trends index, but almost no product has it in its top 5 |

   First-run example: the US and India were crowded; Spanish-speaking markets had one winner; Indonesia and Brazil were open. Vietnam ranked #1 worldwide for "ai clip", yet only one of 31 products had it in its top 5, so it went to demand, weak supply.

6. **Write the report** with the source and read date on every number, an "estimate" label on every derived revenue figure, and a limits section.

## Failures met, and the fix
- **Free Similarweb pages return 403 to every fetcher** (direct fetch, reader proxies). The fix: read it in a browser session the user is logged into.
- **The trial stops after about 7 domains a day** ("Daily usage limit reached"). The first run sat on a modal while 24 domains were "scraped" with the previous page's data. Fix: `batch.sh` checks that the page shows the domain it asked for, and treats anything else as the limit. Run one batch a day.
- **A hardcoded read date and CRLF line ends** got into the CSV on day 2 (Python's `csv.writer` defaults to `\r\n`). `parse.py` now sets `lineterminator="\n"` and writes today's date.
- **Scheduled jobs inside an agent session die when the session restarts.** Three days in a row the morning run did not happen. What worked: the user pings the session and the batch runs then.
- **English keywords under-count non-English countries.** In Vietnamese, "clip" is an everyday word for video, so the #1 for "ai clip" may be inflated. Say so in the report and check with local-language keywords.
- **Trends values are relative** (a keyword's share of that country's searches, top country = 100), not search volumes.
- **Web traffic misses app-only and API customers.** Flag API-first products: their real reach is larger than their site traffic.
- **A link to an unpublished report** slipped into a copy meant for a public site. Before publishing a copy, check every relative link.
