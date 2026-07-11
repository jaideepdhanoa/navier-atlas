# DiDi Argentina demand-semantics correction

**Status:** review-ready; no finance cascade authorized

## Correction

The controlled T1–T12 review found two published passenger totals stored under annual-one-way fields even though the sources aggregate both directions:

- `rn-f451444da7fe` — Rosario → Isla Sabino Corsi: **38,900** is a 2025–2026 summer-season total, not a calendar-year annual one-way value.
- `rn-04b92d6952d2` — Buenos Aires ↔ Colonia: **2,177,670** is a 2024 annual port-pair total with both directions aggregated, not annual one-way passengers.

This change sets both `corridor_annual_oneway_pax` values to `null`, preserves each exact published total in its direction-qualified `_demand_record`, and marks each record `benchmark_only`. The Rosario partner journey also changes `annual_one_way_pax` to `null` and retains 38,900 only in a clearly labelled `_demand_benchmark` record. Partner and `data-clean` DiDi JSON remain identical.

## Release boundary

- No geometry, route ID, market scope, fare, economics total, sheet, sidecar, or live deck is changed.
- Both routes were already outside the grounded floor and remain held.
- Costa Rica’s two exact-demand routes remain evidence-ready but cascade-blocked until exact country-reference inputs are complete.
- Argentina remains held for both incomplete country inputs and invalid annual-one-way demand semantics.

## Verification

- Structural diff: **12** intended finance-field changes and **3** mirrored partner-field changes per DiDi surface; no unrelated JSON changes.
- Country-reference gate: **PASS** — 12 active corridors, four explicit holds, zero errors.
- Partner copy audit: **PASS** — zero internal-jargon leaks across both DiDi surfaces.
- Strict partner inheritance: **PASS** — both proposal and `data-clean` surfaces, zero schema or subset issues.
- Finance inheritance: **PASS** — 14 shared geographies checked, zero divergent spines.
- Partner/data-clean parity: **PASS**.

The accompanying 47-record controlled-review ledger remains authoritative: 2 A1 evidence-ready/cascade-blocked, 3 A2 controls-only, 10 benchmark-only, and 32 hold/null.
