# CHANGELOG — #79ar-pending-uae (2026-06-20)

## Economics (honest accounting)
- Sidecar rebuilt against full recalibrated corridor set.
- **296 pinned** / **208 pending** → **58.7% raw pin rate** (was 166/335 = 33%).
- **Actionable pin rate 88.4%** — 39 actionable pending vs 78 structural intra-city holds.
- `data-clean/PENDING-ECONOMICS-TRIAGE.json` added for bucketed reporting.

## Geometry
- bp-seal handoff: **14 new POIs** sealed (51 validated; remainder reconciled existing), **0 silent drops**.
- **197 gcn-\*** corridor routes minted into gold (UAE node crosswalk `dubai` → `dubai-uae`).
- Bolt/Yango coastal synth + mesh: **+100 routes** (6340 total).
- Portugal corridors: 12 node-id patches (`lisbon-tagus-portugal` placeholders → Porto/Algarve city chips).

## Partners
- Spliced `subproposals-enriched-2026-06-20.json`: **14 bolt + 8 yango** active markets (11 pruned pages excluded).
- Bolt binding: 153 linked / 57 unlinked featured+journey refs.
- Yango binding: 82 linked / 34 unlinked.

## Scripts
- `mint_gcn_corridor_routes.py`, `triage_pending_economics.py`, `portugal_corridors_patch.py`
- `run_pending_uae_boltyango_lane.sh` orchestrator
- `NODE_CROSSWALK` in `bolt_yango_routing_shared.py` for finance node chips