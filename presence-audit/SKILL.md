---
name: presence-audit
description: Audit how a person or a brand is described when AI assistants (ChatGPT, Perplexity, Gemini, Claude, Google AI Mode), search and the press look them up, and produce a ranked fix list. Checks the website the way AI crawlers read it (no JavaScript, robots.txt, entity markup), the name and positioning sentence across social profiles and directories, third-party mentions, and the answers AI assistants actually give; writes a press kit and a 30-day re-check. Use when someone says "presence audit", "how does ChatGPT describe us", "AI visibility audit", "GEO audit", "AEO audit", "make AI describe my brand correctly", "personal brand audit", "entity consistency". Not for ranking promises in AI answers (there is no reliable method; see the honesty rule), a classic SEO keyword audit, or a page-speed audit (use page-quality).
---

# Presence audit: make AI, search and the press describe you correctly

Two goals look alike and are not:

| | Being **recommended** ("best X for Y?") | Being **described correctly** ("what is [name]?") |
|---|---|---|
| Is there a method? | No reliable one. Answers change almost every run, and the most-mentioned brands take most slots. | Yes. |
| Can you check it? | Only as a mention rate over many runs, and even then you cannot prove what caused a change. | Yes: ask, read the answer, compare with the facts. |
| Lever | Fame: press, reviews, communities, years of work | The same facts in every place AI reads |

This skill works on the second goal and measures the first. **Honesty rule:** never promise a ranking or a "top spot" in an AI answer. What you can offer is a checkable target: the named assistants describe the subject correctly on the five core questions, shown with before and after screenshots. Whether the fixes get there, and how fast, is not yet measured; record each run's result.

First run: none yet. The rules come from published studies read in November 2026 (sources at the end), not yet from failure stories as CONTRIBUTING asks; replace or confirm each one with a story from a real run under "Failures met".

## What you need
- Python 3 (standard library only).
- The subject's website URL and the list of its profiles.
- Someone who can ask the questions in the consumer apps (the user, or a browser the agent can drive). API answers differ from what customers see in the apps, so the check uses the apps.
- No keys and no paid tools.

## Method

Work in a folder `presence-audit/<slug>-<YYYY-MM-DD>/`. Every number in the report carries its source and read date.

1. **Facts sheet.** Copy `templates/facts.example.json` to `facts.json` and fill it from the website and at most 5 questions to the user. Required: `type` (brand or person), `name` (exact spelling, case and accents), `website`, `category`, `location`, `price` (brands), `competitors`, 2-5 `recommend_queries` (narrow questions a real customer would ask).
2. **The positioning sentence.** Draft `one_liner` and get the user to approve it word for word. It is the core of the audit.
   - Brand: `[Name] is [category] that helps [who] [do what], in [where].`
   - Person: `[Name] is [role] at [organisation], specialising in [narrow field], who [one result with a number].`
   - Use the category words customers type, not a slogan. Narrow beats broad: an unknown name has a chance on narrow questions and almost none on broad ones.
3. **Website.** `python3 scripts/site_check.py <url> --name "<name>" --one-liner "<sentence>" --json site.json --md site.md`. Also run it on the about and pricing pages it finds; for pages with non-English slugs add `--page-pattern about=<regex>`. Read the "First 400 characters a bot reads": if that is not the subject in plain words, nothing else matters yet. If the script gets HTTP 403, that is the site refusing this script, not proof that AI crawlers are refused: read the robots.txt table it still prints, and check the page by asking an assistant with web search to read the URL.
4. **Profiles and directories.** For every profile in `facts.json`, open it and copy into `name_shown`, `bio` and `website_field` exactly what it shows. A page that blocks the fetcher goes to a browser session; never log in on the user's behalf. Then `python3 scripts/consistency.py facts.json --md profiles.md`. Check that the directories for the subject's type exist and agree: Google Business Profile (local business), G2 or Capterra (B2B software), Crunchbase (funded company), industry association listings, author pages and speaker bios (person).
5. **Third-party mentions.** Search the exact name in news, Reddit, YouTube and Wikipedia. Record each mention with URL, date, and whether it states the name and category correctly. This is the "fame" lever: count it, do not promise to change it fast.
6. **AI answers.** `python3 scripts/ai_sheet.py sheet facts.json --out answers-<date>.json --md ai-sheet.md` (it refuses to overwrite an existing answers file). Ask every question in each app: fresh chat, signed out or memory off, web search on. Paste answers verbatim with cited sources, and screenshot them. Then judge each described answer against `facts.json`: `correct`, `partly`, `wrong` (write the wrong fact in `wrong_fact`) or `unknown`. For recommendation questions set `mentioned` (true or false) per run, and report a mention rate, never a position. `python3 scripts/ai_sheet.py summary answers-<date>.json` prints the per-assistant scorecard for AUDIT.md.
7. **Trace every wrong answer to a source.** For each wrong or unknown answer, look at the sources the assistant cited. The fix goes to that source: the site, a profile, a directory, an old article. An answer with no cited source usually means the site or profiles do not state the fact in plain text.
8. **Write `AUDIT.md`** (structure below) and a filled `press-kit.md` from `templates/press-kit.md`.
9. **Re-check after 30 days.** Run steps 3, 4 and 6 again into a new dated folder, then `python3 scripts/ai_sheet.py diff <old answers> <new answers>`. Report what changed and what did not.

## Rules for the fix list

Order fixes by what blocks the rest.

1. **Blockers.** Search bots blocked in robots.txt (OAI-SearchBot, Claude-SearchBot, PerplexityBot, Googlebot, Bingbot); a robots.txt that returns a server error (Google then treats the whole site as disallowed); a page that is empty without JavaScript (ChatGPT, Claude and Perplexity crawlers do not run it; Googlebot does); a non-200 status. Blocking *training* bots (GPTBot, ClaudeBot, Google-Extended) is the owner's choice: state the trade-off, do not decide it.
2. **Wrong facts in AI answers**, each tied to the source to fix.
3. **The sentence.** Put the positioning sentence word for word on the homepage in plain text, in the about page, in the meta description, and in every profile bio. Same name spelling everywhere.
4. **Entity markup.** One `Organization` (or `Person`) JSON-LD block with `name`, `url`, `logo`, `description` equal to the sentence, `founder` or `worksFor`, `address` when local, and `sameAs` listing every profile. Markup must match visible text; Google says no special schema is needed for its AI features, so treat this as tidy wiring, not a ranking trick.
5. **Pages that answer sub-questions.** A public pricing page, an about page made of facts (year, founders, location, customers, what you do not do), comparison pages ("[name] vs [competitor]") and use-case pages. Assistants split a question into sub-questions and cite pages that answer them.
6. **One source of original data** (a survey, benchmark or price index) when the subject can produce it: assistants cite sources of numbers, and that is the way in for a name nobody knows yet.
7. **Press.** The press kit: the sentence in the first answer, one quotable number, the category named, the "About" paragraph sent with every interview, the same message every time.
8. **Skip** `llms.txt` work unless everything above is done: no evidence that major assistants use it.

Do not write fixes the owner cannot verify. Every fix has a check: a URL to open, a command to rerun, or a question to ask again.

## AUDIT.md structure

1. Verdict in three lines: how the assistants describe the subject today, the top blocker, the date of the re-check.
2. Scorecard: Website (step 3), Profiles (step 4), Third-party mentions (step 5), AI answers (step 6: correct / partly / wrong / unknown per assistant; mention rate on recommendation questions with the number of runs).
3. Fix list in the order above: what, where, why (one line of evidence), how to check it, owner.
4. What this audit cannot promise: being recommended on broad questions.
5. Sources and read dates.

## Evidence behind the rules (read November 2026)

- Same prompt, same brand list in under 1% of runs; same order in under 0.1% (SparkToro and Gumshoe, 2026): report mention rates over many runs, never positions. https://searchengineland.com/ai-recommendation-lists-rarely-repeat-study-468076
- Branded web mentions correlate 0.664 with AI Overview visibility, backlinks 0.218; the top quartile gets about 10 times the mentions of the next (Ahrefs, 75,000 brands, May 2025; correlation, not cause). https://ahrefs.com/blog/ai-overview-brand-correlation/
- About 84% of AI citations come from earned and third-party sources; journalism about 22-27% depending on the wave (Muck Rack, 2025-2026, as reported; vendor study, contested definition of "earned"). https://www.unite.ai/?p=496470 and https://prsay.prsa.org/2025/07/28/news-articles-and-who-they-quote-influence-ai-generated-content-study-finds/
- Each assistant leans on different sources: ChatGPT on Wikipedia, Perplexity and AI Overviews on Reddit, Gemini barely on Reddit (Profound and others; shifts month to month). https://searchengineland.com/ai-citation-data-no-universal-top-source-brands-471285
- Only about 38% of AI Overview citations rank in Google's top 10 for the same query (Ahrefs, March 2026, down from about 76% in July 2025 with a different method): pages answering sub-questions get cited. https://ahrefs.com/blog/ai-overview-citations-top-10/
- Adding citations, quotations and statistics raised visibility up to about 40% in tests (Princeton GEO paper, KDD 2024; mostly a simulated engine). https://arxiv.org/abs/2311.09735
- The OpenAI, Anthropic and Perplexity crawlers tested do not run JavaScript; Googlebot (which feeds Gemini and AI Overviews) and Applebot do (Vercel and MERJ, December 2024; one study, check your own server logs). https://vercel.com/blog/the-rise-of-the-ai-crawler
- No special optimisation or schema is needed for Google's AI features; structured data must match visible text. https://developers.google.com/search/docs/appearance/ai-features

## Failures met, and the fix
- **A pricing page read wrong.** In the research behind this skill, a competitor's "150 / 500 / 1,000 / 2,000" tiers were first recorded as dollars; they were credits. Read the unit next to every number, and say when a page contradicts itself.
- **Rank trackers report positions that do not repeat.** Paid AI-visibility dashboards show "rank #2"; the same prompt rarely gives the same list twice. The fix: count mentions over at least 10 runs per question and report a rate.
