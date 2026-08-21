# Grok handoff — round 6i: /invest + /teaser financials → Board Plan (v36.1)

**Status: FINAL — approved by Jaideep 2026-08-20/21. Contracts already updated on the PR #387 branch (money.json v4, gtm.json). This note is the render guidance.**

## What changed and why
The operating model moved from v34 → v36.1 (Board Plan, Aug 2026). Every financial figure on both routes re-sources to the new model. The raise re-frames from "$10M B-1 first close of $100–150M" to **one $120M program: $20M Series B-1 (closing September 2026) + $100M Series B-2 (targeting Q4 2026)**.

## Exact deltas (all inside `money.json` v4 + one line in `gtm.json`)

### 05 · Money — KPI stat band (`operating-plan`)
| Old | New |
|---|---|
| $512M FY30E revenue | **$571M** |
| 9% recurring by FY30E | **7%** |
| ~80% GM on recurring | unchanged |
| 567 vessels by FY30E | **515** |

### 05 · Money — ramp charts (`ramp-charts`) — new series (native coded charts, PNG ban stands)
- Revenue: 10.5 / 64.3 / 146.8 / 287.9 / **570.8** (recurring: 0.5 / 3.3 / 10.8 / 22.4 / 40.5)
- EBITDA: −10.4 / −15.7 / −11.0 / **+8.2** / **+70.5** (zero-line crossing now lands in FY29 — verify the crossing renders between FY28 and FY29 ticks)
- Fleet cumulative: 14 / 50 / 133 / 275 / **515**; delivered-in-year points: 10 / 36 / 83 / 142 / **240**

### 05 · Money — the round (`the-round`)
- Headline: **"$20M Series B-1 → $100M Series B-2 — One $120M Program"**
- Col 1 (eyebrow SEPTEMBER 2026): B-1 items, now includes "two rush mold sets"
- Col 2 (eyebrow Q4 2026): three model-traced items — US shipyard $45M · tooling & molds $28M · vessel programmes $27M (sums to $100M exactly)

### 05 · Money — five markets (`five-markets`)
- Closing line: "…The **$20M** first close buys the build slots."

### 04 · GTM — market section (`gtm.json`)
- "the plan: **515** hulls by FY30 — **<8%** of the floor."

## QA gates (add to the v10 screenshot set)
1. Money chapter at 1280/1440/2560 — KPI band FIRST, charts below, no PNG charts.
2. EBITDA chart zero-line crossing visibly in FY29.
3. The-round two columns — col 2 items sum $100M; no "$10M" or "$100–150M" anywhere on either route (scripted text scan, paste output).
4. Five-markets closing line shows $20M.
5. Both routes: grep rendered HTML for `512M|567|127M|\$10M first close|100–150` → must be zero hits.

## Firewall reminders (unchanged)
No valuations, no lead identity, no terms beyond the-round slide text. Slide-34 thesis descriptor now reads "$20M buys the build slots" wherever the old $10M phrasing appeared — but ONLY in contracts listed here; do not free-edit other sections.
