# Grok G4 handoff — DiDi Mexico economics sidecar + reseal

**As of:** 2026-07-09  
**Upstream geometry receipt:** `56b570c2`  
**Tasklet state:** **cascade-complete / G4-seal-needed**  
**Scope:** Mexico calibration only; do not imply the 16-jurisdiction ex-China proposal is complete.

## Inputs on this branch

- `finance/model/corridors.json` — exact two-market finance spine
- `finance/model/country-reference.json` — Mexico operating-cost row; no Singapore fallback
- `finance/recal/agg-didi.json` — refreshed aggregate
- `finance/didi-growth-case.json` — refreshed growth ladder
- `partner-pitch/partners/_growth-draft/didi.growth.json`
- `partner-pitch/partners/didi.json` — growth block + live economics URL
- `finance/PARTNER-SHEET-IDS.json` — DiDi live Sheet registration
- `handoff/didi-ex-china/mexico/DIDI-MEXICO-T3-FINANCE-EVIDENCE-2026-07-09.json`
- `handoff/didi-ex-china/mexico/TASKLET-T3-CASCADE-RECEIPT-2026-07-09.json`

Live Sheet: `https://docs.google.com/spreadsheets/d/1LY0Vp7FskgDDnEixkrEUCH0m-A_pYd2YCNuq3LF8ESM/edit`  
Master tracker: `https://docs.google.com/spreadsheets/d/1PPK-QuTWJzXqSHfYFxvcjWSoY1XvZ1uk7OmS63k89ls/edit`

## Immutable spine

### `mexico-caribbean`

1. `ics-413f51cd44`
2. `ics-dd1d814699`
3. `ics-03e3853317`
4. `ics-aa6ff40d2d`

### `mexico-pacific`

1. `ics-89a8844858`
2. `ics-de6758216f`
3. `ics-db0930d9d1`
4. `ics-b5861451fb`

Do not add a catch-all `didi` finance market. Do not inherit Grab's census. Do not create partner-specific geometry.

## Grounded result

- 2 grounded Caribbean OD anchors; 6 spine rows retained with unsupported demand held null
- transport-spend pool: **$146,344,836/year**
- grounded Navier transport-revenue floor: **$14,404,810/year**
- MID global-template full-network transport revenue: **$70,583,569/year**
- MID matured Navier transport revenue: **$322,690,363/year**
- MID partner platform revenue on Navier-linked journeys: **$174,252,796/year**

The 3.44 / 4.90 / 6.36 width band is explicitly a **global planning template pending a DiDi-specific census**, not a measured DiDi count and not Grab inheritance.

## G4 work

1. Build `economics_by_route_id.json` **against the sealed gold** and the exact eight-ID spine above.
2. Reseal DiDi's partner/data-clean economics from the refreshed aggregate/growth artifacts.
3. Preserve and verify `economics_url` on the partner view and every TAM-ladder rung.
4. Normalize the 16 existing Mexico `featured_routes[]` schema entries to `{route_id, from_label, to_label, cluster_id}`. Current non-strict inheritance passes with 0 subset issues; strict mode fails only on those missing presentation keys. Do not change the inherited corridor set.
5. Run:
   - `scripts/audit_partner_copy.py` — Gate G must pass
   - strict `validate_partner_inheritance.py` — 0 subset and 0 schema issues
   - `validate_finance_inheritance.py`
   - partner route linkage audit
   - BP/drop ledger checks and render QA
6. Commit to `main` only under Jaideep's merge/greenlight rules. Return a G4 receipt with commit, sidecar counts, exact joined route IDs, gate output, and render result.

## Null discipline

- Pacific annual ridership stays null.
- `ics-03e3853317` and `ics-aa6ff40d2d` demand/fare stay null pending exact terminal/operator allocation.
- Published fares on the two grounded anchors are comparable adult benchmarks, **not** operator realized yield.
- Do not map airport, tourism, port, or mixed terminal totals one-to-one into corridor demand.
- Do not edit the live deck directly. Corrected source JSON feeds deterministic generation.
