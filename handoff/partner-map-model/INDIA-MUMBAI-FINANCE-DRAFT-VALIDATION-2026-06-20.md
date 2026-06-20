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

## Demand source update — still held null
Captured direct Mumbai water-taxi load anchors after initial validation:

- Indian Express (2023-02-08): Nayantara/NAYAN XI 200-seat DCT→Mandwa via Belapur service had poor DCT ridership, but averaged 120 passengers from Belapur; fares ₹400 lower deck / ₹450 upper-business.
- The Hindu (2022-11-13): Belapur→Elephanta was filling ~80% capacity on a 32-seat vessel with three round trips; Belapur→JNPT was “doing very well”; DCT→Mandwa had 60 round trips in 10 days with <10% occupancy on a 200-seat vessel.
- PIB MoPSW (2022-02-17): route/terminal proof for DCT, Nerul, Belapur, Elephanta, JNPT plus Belapur movements to Bhaucha Dhakka, Mandwa, Elephanta and Karanja.

Decision: these are strong load/service-health anchors but not route-level annual demand. Annual demand remains null; aggregate validation still must show no fare, no demand pool, no fleet, no revenue.
