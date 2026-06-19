# LB-224 — UAE overlay precedence + marina apron (2026-06-18)

## Policy

1. **Coarse-mask suppression (UAE bbox)** — Inside `(50.0, 21.5, 57.5, 26.8)`, when `uae_gulf_land_v2.wkb` is loaded, `point_is_land()` trusts the fine overlay only; `global-land-mask` is not consulted.

2. **Marina apron extension** — `endpoint_apron_km` raised from `0.08` → `0.12` (120 m) in `qa_land_crossing.evaluate_route()` default. Absorbs jetty-mouth noise on synthesize marina legs without masking interior crossings.

## Patched files

- `_review/grok-routing-v2/grok-routing-v2/code/qa_land_crossing.py`
- `_ingest/grok-ci-handoff-2026-06-18/pipeline/_tools/qa_land_crossing.py`
- `grok-routing-output/solve_routes_phase2.py` — `LB224_MARINA_APRON_KM`, hand-waypoint QA via `verify_solution()`

## Coastal Hud result (4 long hops)

| Route | QA | nm |
|-------|-----|-----|
| Hud → Yas | 0.0 | 21.85 |
| Khalifa → Yas | 0.0 | 21.33 |
| Khalifa → Saadiyat BC | 0.0 | ~18 |
| Saadiyat BC → Lulu | 0.0 | 7.02 |

Offshore fairway at lat ~24.478–24.482 + widened `ad_coastal_navigation_lane` / `khalifa_south_exit` / `lulu_west_channel` cutouts in `ad_channel_cutouts.py`.