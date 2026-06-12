# Gold #67 — Philippines splice overlay (LB-124 / LB-129)

## What changed (one file overlay)
- `data-clean/partners/grab.json` — post-η Philippines cascade landed in partner-pitch source AFTER gold #66 sealed.
  - `committed_fleet`: 231 → **289**
  - `growth_case.partner_platform_rev_on_navier.mid`: $830M → **$985M** (low $200M, high $3.79B)
  - `steady_state_ceiling`: **1,132** (sibling ceiling retained)
- No geometry / no ROUTES.json / no CLUSTERS.json / no corridors.json change.
- `economics_by_route_id.json` regenerated against unchanged routes (109 route-pinned, 20 _pending_route_pin).
- `SEAL.json` sidecar hash refreshed.

## Why this seal exists
Grok front-end was reading the still-sealed gold-#66 zip and surfacing stale Grab KPIs (fleet 231, MID $830M). Single-file overlay re-seal is the cheapest correct fix.

## Untouched
ROUTES.json, CLUSTERS.json, STORIES.json, VESSEL_SPECS.json, FEATURES_BY_TYPE.json, CORRIDOR-ENDPOINT-GROUNDING.json, all cluster_briefs, all city_briefs, every other partner pitch — bit-identical to gold #66.
