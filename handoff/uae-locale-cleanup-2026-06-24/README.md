# UAE locale + POI cleanup — seal handoff (2026-06-24)

Tasklet-owned **input** package. Grok seals onto the live Atlas front end (two-worlds rule).

## What Jaideep flagged
UAE → Dubai → locales is a mess: Abu Dhabi locales (Corniche, Saadiyat, Sir Bani Yas) showing under
Dubai; combined areas producing pins that land nowhere near the named place; a meaningless
"Sharjah / Ajman / RAK coastal hop". Directive: **eliminate anything not placeable at 99%+ confidence.**

## Root cause
1. The seal promoted **every** sub-cluster row to a locale pin — including cross-emirate corridor-endpoint
   rows that are strategy analysis, not places.
2. A radius scrape mis-tagged neighbouring-emirate / cross-Gulf POIs to the search-origin city.

## Contents
| Path | What | Grok does |
|---|---|---|
| `GROK-SEAL-PROMPT.md` | Mandate + deterministic rule + acceptance | Executes |
| `inputs/UAE-CLEANUP-LEDGER.json` | 14 locale drops (exact ids) + 17 keeps; 165 high-confidence POI drops; residual-gate spec + per-emirate allowlists | Applies drops, runs residual water-adjacency gate, reseals |

## The fix in one line
Drop cross-emirate, combined-but-far, vague, and non-maritime locales; drop wrong-emirate / junk POIs;
add a permanent guardrail so corridor rows never render as pins again. Strategy markdown keeps its
corridor analysis — it just stops becoming map pins.

## Disposition summary
- **Locales:** keep 17 (Dubai 6 / Abu Dhabi 5 / Sharjah 3 / RAK 1 / Fujairah 2), drop 14.
- **POIs:** 165 high-confidence drops; residual non-emirate junk finished by Grok's water-adjacency gate
  (0 silent drops). Legitimately-distant in-emirate outliers (Sir Bani Yas, Khorfakkan, north Fujairah)
  are explicitly preserved.
