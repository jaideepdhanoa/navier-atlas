# Slide-3 / TAM-ladder KPI sidecar — deterministic build spec (Grok-owned)

**Owner: Grok build loop.** This is a pure pull-and-transform from the model. No judgement, no Tasklet
hand-off. Run `gen_slide3_kpis.py <partner>` whenever (a) you build/refresh a deck, or (b) the economics
cascade reruns. The output is regenerated, never hand-edited.

## Command
```
python3 deck-studio/decks/gen_slide3_kpis.py <partner>      # run from repo root
```

## Inputs (read-only — the ONLY sources of numbers)
| File | Provides |
|---|---|
| `finance/recal/agg-<partner>.json` | `rows[]` (per-corridor, scenario sub-objects `thin/mid/full`), `rollup.grounded_floor_by_market`, `rollup.n_corridors_total` |
| `finance/recal/growth-<partner>.json` | `grounded{}` + `estimated_total{}` LB-254 ladder rungs |
| `deck-studio/decks/<partner>/market-scope.json` | ordered focus markets, labels, tags, `gulf_slide_only` flags — the single source of deck scope |

## Output
`deck-studio/decks/<partner>/slide3-kpis-<partner>.json`

## Field mapping (literal — no interpretation)
**Per market card** (from `rollup.grounded_floor_by_market[key]`, except routes/riders):
- `routes_mapped` = count of `rows[]` where `row.market == key`
- `addressable_pool_usd_m` = `transport_spend_pool_yr` / 1e6, 2dp
- `navier_rev_grounded_floor_usd_m` = `market_rev_yr` / 1e6, 2dp
- `fleet_at_floor` = `fleet`
- `modeled_riders_per_day_floor` = round( Σ(`row.mid.pax_per_year`, fallback `row.thin.pax_per_year`) / 365 )
- `co2_saved_t_yr` = round(`co2_saved_t_yr`)

**Network headline** (`ladder()` over `grounded` then `estimated_total`):
- `addressable_transport_spend_usd_m` = `M_today_transport_spend_yr` /1e6
- `SOM_floor_navier_rev_usd_m` = `SOM_floor_navier_transport_rev_yr` /1e6
- `SAM_navier_rev_mid_usd_b` = `SAM_navier_transport_rev_yr["mid"]` /1e9
- `TAM_journey_gmv_mid_usd_b` = `TAM_journey_gmv_yr["mid"]` /1e9
- `partner_platform_rev_mid_usd_b` = `partner_platform_rev_yr["mid"]` /1e9
- `effective_capture` = `_eff_capture_floor`; `is_captive` = `_is_captive`
- `routes_mapped_total` = `rollup.n_corridors_total`

## Hard rules (the anti-misinterpretation guardrails)
1. **Never hard-code a number.** Read every value from the input files. A literal in the output JSON = bug.
2. **Scenario keys are fixed:** `grounded` (headline) and `estimated_total` (upside). Don't invent scenarios.
3. **SAM/TAM/platform-rev → always `["mid"]`** on the headline. Never surface low/high there.
4. **Scope comes only from `market-scope.json`.** To add/remove/reorder a market or flip a market to
   Gulf-only, edit that file — not the generator.
5. **null beats confidently-wrong.** If a scoped market is absent from the source files, emit `"kpis": null`
   for it. Do not interpolate, borrow a neighbour, or guess.
6. **`gulf_slide_only: true` markets must never render on a Europe surface** (same leak rule as the images).
7. Every number stays **labelled grounded floor / modeled, not measured** via `_provenance_note`. Don't strip it.

## Regeneration trigger
Wire this into the post-cascade step: after the economics model reruns (e.g. post-seal Thailand or any
parameter change), `gen_slide3_kpis.py` reruns for each affected partner and the renderer re-reads the
sidecar. The deck figures then track the live model automatically — no manual refresh.
