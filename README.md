# Agent Skills

**Production-grade AI agent skills for Claude Code, Cursor, and autonomous agent workflows.**

A skill is a structured instruction set that an agent autonomously loads and executes when encountering a specific operational domain. You do not need to memorize workflows or repeatedly paste prompts — the agent detects context, loads the guidelines, and executes with precision.

All principles are distilled from production engineering experience: rigorous market research with multi-tier source verification, clean-room product teardowns, winning-product scans, post-launch page quality and product analytics, event write-ups, and developer-machine hygiene.

## Research

- [Open the report directly in your browser](https://0xdonniechu.github.io/BYFA-skills/) — GitHub Pages.
- [Native.no competitive landscape (26 Oct 2026)](research/native-competitive-2026-10-26.html) — competitor matrix, TrustMRR snapshots, funding/valuation evidence, and a clearly caveated TAM/SAM/SOM scenario.

---

## Skills Directory

| Skill | Core Capability & Usage Context |
|---|---|
| `/market-research` | Decision-oriented research across markets, competitors, investors, and vendors; source tiers, counter-evidence, explicit sizing assumptions, pricing/funding matrices, and uncertainty labels. |
| `/teardown` | Clean-room competitor teardowns: core features, monetization models, tech stack analysis, and end-to-end user experience flows. |
| `/page-quality` | Post-launch site audits: page load performance, Core Web Vitals, and UI layout stability. |
| `/optimize-mac` | Safe disk reclamation, RAM inspection, and developer environment hygiene for macOS. |
| `/event-review` | Conference and meetup synthesis: reconstruct complete talks from slide decks and transcripts. |
| `/posthog` | Production analytics with PostHog: event tracking setup, proxy configuration, and executive dashboards. |
| `/country-map` | Which countries a product or competitor group sells in: Similarweb top-5 countries, Google Trends demand by country, revenue-per-visit calibration; classifies markets as crowded, has a winner, open, or demand with weak supply. |
| `/pricing` | Pick a business model and 3 price tiers anchored on what customers already pay (hire, freelancer, agency), a manual service to sell this week, and price questions for real people. |
| `/competitors` | Sourced competitor list (products and substitutes) with revenue, headcount and year per figure, a 20-minute trial plan each, and 2-3 picks for a pricing teardown. |
| `/pricing-teardown` | Every way a competitor charges, from pricing page to terms: revenue lines, hidden fees, totals at 3 customer sizes, mapped to 11 business models; merged into 3-6 ways for you to charge. |
| `/product-spec` | A 3-5 page product spec before any code: problem, result, core first, phased scope with a won't-do list, checkable Phase 1 criteria; loops until you score it 9-10. |
| `/userflow` | User flows to a defensible standard (ISO 9241, WCAG 2.2): flow-spec table, error branches with recovery, review gate; drawn as one offline `docs/FLOW.html`. |
| `/mockup` | Clickable mockup before code: a gallery with Playwright proof, or a single offline file with every screen state, a states panel and shareable `#state=` links. |
| `/team-sprint` | Weekly team meeting to a record and draft tickets for the Product role: decisions, who took what, open questions; 5-part tickets with one assignee, deadline and label; nothing goes to Linear before you approve. |
| `/master-winning-product` | Weekly scan for winning products (verified revenue, funding, traffic) by industry, niche and keywords; fit scored against your own profile, with a debrief. |
| `/presence-audit` | How AI assistants, search and the press describe a person or brand: the site as AI crawlers read it (no JS, robots.txt, entity markup), name and positioning sentence across profiles, AI answers checked in the apps; a ranked fix list, a press kit and a 30-day re-check. No ranking promises. |

---

## Installation

### Claude Code

Install all skills with a single command:

```bash
git clone https://github.com/0xdonniechu/BYFA-skills.git ~/.claude/skills/byfa-skills
~/.claude/skills/byfa-skills/setup
```

Or install the research skill alone:

```bash
mkdir -p ~/.claude/skills/market-research
curl -o ~/.claude/skills/market-research/SKILL.md \
  https://raw.githubusercontent.com/0xdonniechu/BYFA-skills/main/market-research/SKILL.md
mkdir -p ~/.claude/skills/market-research/references ~/.claude/skills/market-research/assets
curl -o ~/.claude/skills/market-research/references/research-playbook.md \
  https://raw.githubusercontent.com/0xdonniechu/BYFA-skills/main/market-research/references/research-playbook.md
curl -o ~/.claude/skills/market-research/references/positioning.md \
  https://raw.githubusercontent.com/0xdonniechu/BYFA-skills/main/market-research/references/positioning.md
curl -o ~/.claude/skills/market-research/assets/positioning_chart.py \
  https://raw.githubusercontent.com/0xdonniechu/BYFA-skills/main/market-research/assets/positioning_chart.py
curl -o ~/.claude/skills/market-research/assets/positioning_example.json \
  https://raw.githubusercontent.com/0xdonniechu/BYFA-skills/main/market-research/assets/positioning_example.json
```

### Cursor & Other Agents

See the complete guide in [INSTALL.md](INSTALL.md).

---

## Verification

Open a new agent session and test with prompts such as:

```
I need to research this market and evaluate competitors — which framework should we follow?
I am about to build a new feature — do we have a spec-before-code procedure?
What are our next steps for this session?
```

When the agent autonomously references the respective framework, the skills are active and ready.

---

## Core Principles

1. **Empirical Evidence Over Assumptions**: Every metric must be cited with primary sources or calculated with transparent math.
2. **Agent Assistance, Human Authority**: Skills keep agents disciplined; final approval and irreversible actions remain strictly with the user.
3. **Continuous Optimization**: Skills improve with each operational cycle and real-world deployment. See [CONTRIBUTING.md](CONTRIBUTING.md).
