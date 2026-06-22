# Deck economics VALUES — deterministic build spec (Grok-owned)

**Owner: Grok build loop.** This generator emits **every number a partner deck shows**, pulled
straight from the model engine. No hand-typing, no judgement, no Tasklet hand-off. It is the
companion *values* file to `economics-binding.json`:

| File | Role |
|---|---|
| `decks/<partner>/economics-binding.json` | **WHERE** — object_id per field (already in repo) |
| `decks/<partner>/deck-economics-values-<partner>.json` | **WHAT** — generated formatted value per field |
| join | `value[slide][field]` → `binding[slide][field].object_id` → style-preserving text op |

This **supersedes** the earlier `gen_slide3_kpis.py` (slide-3 is now folded in here). Keep one entrypoint.

## Command (run from repo root)
```
python3 deck-studio/decks/gen_deck_economics.py <partner>
python3 deck-studio/decks/gen_deck_economics.py grab --validate   # reproduce gold, write nothing
```
`--validate` reproduces the **Grab gold deck**'s slide-7-family numbers field-by-field. It currently
passes **112/112**. Run it after any model change as a regression gate before trusting a fresh build.

## Inputs (read-only — the ONLY origin of numbers)
| File | Provides |
|---|---|
| `finance/recal/agg-<partner>.json` | `rows[]` (per-corridor `thin/mid/full`), `rollup` |
| `finance/recal/growth-<partner>.json` | `grounded{}` LB-254 ladder |
| `deck-studio/decks/<partner>/market-scope.json` | ordered deck markets + `gulf_slide_only` flags |
| `deck-studio/decks/<partner>/economics-binding.json` | which slide indices/fields exist |

## Output: `deck-economics-values-<partner>.json`
- `slide3_kpi.network_cards` — the 4 headline KPI cards
- `slide3_kpi.per_market_cards` — 6 per-market cards (routes, pool, rev floor, fleet, riders/day, CO₂)
- `slide10_tam.rungs` — SOM → SAM → TAM(marine) → Journey GMV → partner platform revenue
- `economics_slides[idx]` — per-market unit economics for every slide-7-family index

## Field derivation (literal — no interpretation)
**Per econ slide** (one representative corridor per market):
- representative corridor = **grounded first, then `revenue_per_boat_yr` desc** (fixed rule)
- `header_market` = `WHAT ONE BOAT EARNS · {MARKET}`
- `route_line` = `{corridor}  ·  ~{round(nm)} nm  ·  {vessel} ({pax_capacity} seats)`
- `summary_line` = `{rev} revenue − {opex_total} run cost = {profit} profit / boat·yr · {margin} margin · {payback} yrs payback`
- `trips_per_day` = `mid.trips_per_day`; `operating_days` = `assumptions.operating_days_yr`;
  `revenue_legs` = `assumptions.revenue_leg_pct`; `seats_per_trip` = `mid.pax_per_trip` (1dp);
  `paid_seats_yr` = `mid.pax_per_year` (comma int); `premium_fare` = `${mid.navier_fare_usd} / seat`
- `revenue_per_boat` = `mid.revenue_per_boat_yr`
- **OPEX 6 lines** (flush-left, fixed order) from `mid.cost_components`:
  `opex_energy, opex_crew, opex_marina, opex_maintenance, opex_insurance, opex_charging_berth`
- `opex_total` = `mid.annual_opex` ( = sum of the six lines; excludes depreciation )
- `result_profit` = `mid.ebitda_per_boat_yr`; `result_margin` = `mid.margin`;
  `result_payback` = `mid.payback_years` + " yrs"; `result_co2` = `mid.co2_saved_t_per_boat_yr` + " t"
- `result_capex` = **`cost_components.depreciation_usd_yr × 20`** (the model's own dep-life;
  reproduces $900K US/EU, $600K RoW without re-encoding the region rule)

**slide10 ladder** (mid of band): `SOM_floor_navier_transport_rev_yr`, `SAM_navier_transport_rev_yr.mid`,
`marine_mobility_tam_yr.mid` (TAM), `TAM_journey_gmv_yr.mid` (Journey GMV), `partner_platform_rev_yr.mid`.

**slide3 cards:** `rollup.n_corridors_total`, `M_today_transport_spend_yr`, SOM floor, `marine_mobility_tam_yr.mid`.

## Slide↔market mapping
Econ slide indices (sorted) are filled in order from `market-scope.json` markets (in order).
Surplus gold econ slides beyond the partner's market count are emitted
`"status":"no_market_drop_slide"` (the editplan drops them — never fill with a borrowed market).

## Hard rules (anti-misinterpretation)
1. **Never hard-code a number** — read every value from the inputs; a literal in the output = bug.
2. **Scope lives only in `market-scope.json`** — add/remove/reorder/flip-to-Gulf-only there, not in code.
3. **null beats confidently-wrong** — market with no corridor → `"fields": null`, never borrow a neighbour.
4. **Mid only** on the headline ladder (SAM/TAM/Journey/platform). Never surface low/high there.
5. `gulf_slide_only: true` markets must never land on a Europe surface (slide-3 grid / Europe cover) —
   they are fine on their own per-market econ slide.
6. Keep `_meta.provenance_note` — every number stays **grounded floor / modeled, not measured**.
7. **`--validate` must stay green** (Grab 112/112). If it breaks after a model change, the binding's
   sample_values or a field name drifted — reconcile before building partner decks.

## Regeneration trigger
Wire into the post-cascade step: after any economics rerun (post-Thailand-seal or any parameter change),
`gen_deck_economics.py <partner>` reruns for each affected partner and the renderer re-reads the sidecar.
Deck figures then track the live model automatically — no manual refresh, no Tasklet.
