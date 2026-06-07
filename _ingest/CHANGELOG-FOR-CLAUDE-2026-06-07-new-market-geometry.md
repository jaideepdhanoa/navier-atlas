# Changelog — Gold #10 (new-market geometry delta) — 2026-06-07

## What changed
Added **9 new greenfield Mediterranean clusters** to the atlas with real, web-verified
boarding points and water-validated routes (geometry delta, append-only onto Gold #9).

| Cluster | New BP POIs | New routes |
|---|---|---|
| Naxos & Small Cyclades (GR) | 5 | 6 |
| Milos & Western Cyclades (GR) | 5 | 7 |
| Naples–Capri–Procida (IT) | 7 | 13 |
| Malta & Gozo | 5 | 3 |
| Menorca (ES) | 3 | 1 |
| Corsica (FR) | 5 | 4 |
| Costa Brava (ES) | 5 | 12 |
| Djerba (TN) | 3 | 1 |
| Marseille & the Calanques (FR) | 4 | 6 |
| **Total** | **42** | **53** |

- POIs: 11,245 → **11,287**.  Routes: 5,077 → **5,130**.
- City pins for all 9 already existed (rendered) — this fills their previously-empty BP + route networks.

## How (LB-25 — `add_market.py`)
Geometry delta tool that composes the **same** build.py stages on just the new clusters,
then splices onto the sealed gold (never a full rebuild — protects gold, avoids the LB-17
superset break):
1. BP-POI injection (mirrors build.py ~590-690)
2. `intra_cluster_routes.generate()` — water-validated spokes (SeaGrid; **23 land-crossers dropped in-generate**)
3. `route_labels.apply_labels()` — gold-schema labels (City → sub-point)
4. `scrub_land_routes.py` safety net (**5 more land-crossers dropped**)
- Split into `--phase gen` (heavy: sea grid) / `--phase label` (light) to stay within memory.

## Provenance / safety
- Every boarding point web-verified (operator/port-authority/Wikipedia/sea-seek/Navily/OpenSeaMap); `source`, `confidence`, `precision` recorded in `boarding-points/{slug}.json`.
- 0 id collisions with gold; append-only → gold ⊆ gold #10 by construction.
- 0 Pioneer II routes >70 nm (1 route Ajaccio→Bastia 130.8 nm correctly Quanta-LR).
- 0 banned-token leaks; 0 degenerate/null labels.

## Note for render lane
These 9 clusters are not partner-pitch cities, so P0 partner-route relink (Gold #9) is unaffected.
The new routes do, however, make more *future* signature/journey links possible if any partner later references these corridors.
