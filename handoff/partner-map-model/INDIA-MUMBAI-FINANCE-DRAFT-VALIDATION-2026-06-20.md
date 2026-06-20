# India Mumbai finance draft validation — 2026-06-20

## Scope
Adds draft-only Mumbai sealed route rows to `finance/model/corridors.json` for:

- `ola-mumbai` — 11 Pioneer II rows
- `rapido-mumbai` — 13 Pioneer II rows
- `uber-mumbai` / partner `uber-india-derivative` — 13 Pioneer II rows

## Controls
- Route IDs come only from the PR59 India wiring spec.
- Quanta-LR Goa→Mumbai long-haul row is excluded from near-term finance rows.
- Demand remains null because passenger counts are not yet captured.
- M2M Ferries ₹400 passenger fare is stored as `public_fare_floor_usd_pax = 4.7`; it is **not** inserted as `comparable_fare_usd_pax`.
- Rows are held out of grounded and estimated totals using `_in_grounded_floor=false` and `_tier=experience_upside`.
- `model_use` is `draft_only_demand_null_held_out_until_route_counts_captured`.

## Validation run
Commands run locally from `finance/model`:

```bash
python3 aggregate.py --partner ola --markets mumbai --json /tmp/india-agg/agg-ola.json
python3 aggregate.py --partner rapido --markets mumbai --json /tmp/india-agg/agg-rapido.json
python3 aggregate.py --partner uber-india-derivative --markets mumbai --json /tmp/india-agg/agg-uber-india-derivative.json
```

Observed results:

| Partner | Rows | Markets | Fare field | Estimated pool | Estimated fleet | Expected flags |
|---|---:|---|---|---:|---:|---|
| ola | 11 | `ola-mumbai` | `None` | 0 | 0 | `NULL_revenue:no_comparable_fare`, `NULL_demand:no_pool` |
| rapido | 13 | `rapido-mumbai` | `None` | 0 | 0 | `NULL_revenue:no_comparable_fare`, `NULL_demand:no_pool` |
| uber-india-derivative | 13 | `uber-mumbai` | `None` | 0 | 0 | `NULL_revenue:no_comparable_fare`, `NULL_demand:no_pool` |

## Next gates before partner-facing finance publish
1. Capture direct route passenger counts for Mumbai/Mandwa/Elephanta/Navi Mumbai water corridors.
2. Source a premium/on-demand comparable fare separately; do not reuse the public M2M fare floor as Navier premium fare.
3. Register sheet targets in `finance/PARTNER-SHEET-IDS.json` for Rapido/Ola/Uber India derivative if/when publish is approved.
4. Re-run aggregate/growth/materialization only after rows graduate from demand-null/fare-null state.
