# Demand-pool handoff — 2026-08-20

Package for Grok: make fleet-investor pages show who rides the corridors.

| File | What it is |
|---|---|
| `GROK-SPEC-demand-pool-v3-2026-08-20.md` | **The instruction.** Audit of all 15 cities, the v3 row contract, seven template changes, acceptance gate. |
| `data/bay-area.demand_pool.json` | 16 authored rows, city total 3,441 indicative seats. Drop in as the `demand_pool` key of `employer-hub/hubs/bay-area/fleet-investors.json`. |
| `data/new-york.demand_pool.json` | 14 authored rows, city total 2,769 indicative seats. Same for `new-york`. |
| `DROP-LEDGER.md` | Every tracker row that didn't make it and why; rows kept but reframed; two open questions for Jaideep. |
| `SOURCE-BOUNDARY.md` | Which tracker columns may ever reach a rendered surface. Answer for 8 of 11: never. |
| `MIGRATION-5-CITIES.md` | Follow-on pass. **Not** the same PR. |

## The short version

The `demand_pool` pipe already exists in every city. Seattle, Miami and DC already author good rows.
The renderer reads neither the `value` nor the `note` field, so that work is invisible; Bay Area and
New York have no rows at all. Fix the renderer, add the two missing cities, and fourteen of fifteen
pages become correct without new research.

## Headline numbers

- **Bay Area — 3,441 indicative seats** across 16 rows: Genentech, UCSF Mission Bay, Salesforce, Meta,
  OpenAI, Uber, Oracle, Kaiser, PG&E and others.
- **New York — 2,769 indicative seats** across 14 rows: NewYork-Presbyterian/Weill Cornell, Memorial
  Sloan Kettering, Goldman Sachs, JPMorgan Chase, BlackRock, Brooklyn Navy Yard and others.

Both totals are 3% of the headcounts shown, labelled as such on the page.

## Two things that need Jaideep, not Grok

1. NewYork-Presbyterian is 49% of the New York total, on a system-wide staff figure for campuses a mile
   from the water. Publish as-is, or exclude from the total (→ 1,419)?
2. The playbook shuttles the East Side medical campuses from **E 34th**; the employer universe maps them
   off **E 90th**. Both stops exist. E 34th used here.

See `DROP-LEDGER.md` for both.
