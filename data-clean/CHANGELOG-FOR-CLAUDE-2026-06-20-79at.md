# CHANGELOG — #79at-mesh-trim-opex-egypt (2026-06-20)

## Mesh trim
- Dropped **595** excess `_pending_mesh` routes (duplicate BP pairs + per-city cap).
- Kept **245** mesh routes (**35/city** × 7 showcase cities) for capillary map coverage.
- Routes: **7,400 → 6,813** (−587 net after Egypt mint).

## Egypt geometry
- **8 routes minted** (Red Sea + Cairo Nile + Sharm legs) via `mint_egypt_corridor_routes.py`.
- Egypt `NODE_CROSSWALK` added (`hurghada-egypt` → `hurghada-el-gouna-egypt`).
- Partner bind: bolt **174 → 176** linked; yango **90 → 99** linked.

## Sidecar opex refresh (Tasklet `sidecar-opex-refresh-2026-06-20.zip`)
- Rebuilt `economics_by_route_id.json` against sealed gold + post-opex aggs.
- **6-line opex** on corridor cards: insurance + charging/berth now surfaced.
- Partners in sidecar: bolt **127**, yango **85**, grab 59, careem 36 (+ held).
- Sample bolt record: `insurance_usd_yr=15000`, `charging_berth_usd_yr=18000`.
- Yango `growth_case` bound from fresh `agg-yango.json`.

## Economics
- **355 pinned / 141 pending** → **71.6% raw pin rate** (was 351/151 = 69.9%).
- **Actionable pin rate 95.2%** — 18 actionable vs 45 structural holds.

## Scripts
- `trim_excess_mesh.py`, `mint_egypt_corridor_routes.py`, `run_79at_lane.sh`
- `mint_pending_corridor_routes.py`: mesh off by default (`--mesh` to opt in)
- `build_economics_sidecar.py`: 6-line opex + url map from opex handoff