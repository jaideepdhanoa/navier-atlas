# Gold #79ah — UAE route geometry fix (Phase 3 OVERLAY-ONLY)

## Scope
- 130 UAE routes had no-cross polygon detours inserted via OVERLAY-ONLY waypoint
  insertion. Each route's original LineString coordinates are preserved; new
  seaward corner waypoints are inserted between adjacent original coords where
  segments enter/cross a no-cross bbox.
- Per-route validation: new interior_land_km ≤ original (coarse global_land_mask).
  Global FAIL count stable at 219 (= #79ag baseline). 0 routes regressed.
- 20 patched routes retain residual coarse-mask interior_land_km in the
  0.4–0.9 km range (≤ 1.0 km threshold) due to pre-existing densified coords
  over Saadiyat / Dubai / Lulu reclamation — within gate.

## No-cross polygons applied (axis-aligned bboxes)
- Palm Jumeirah (55.105–55.180 / 25.090–25.155)
- Dubai/Deira Islands (55.290–55.370 / 25.260–25.340) — newly added per Jaideep image 157/158
- The World Islands (55.155–55.230 / 25.195–25.255)
- Bluewaters (55.115–55.135 / 25.071–25.087)
- Atlantis Royal block (55.121–55.135 / 25.135–25.146)
- Jebel Ali Port (55.000–55.080 / 24.960–25.050)
- Saadiyat (54.380–54.490 / 24.510–24.620)
- Yas (54.550–54.670 / 24.420–24.520)
- Lulu (54.360–54.410 / 24.490–24.560)

## Phase 2 BP coord snap
- `bp-56d5f5bd8d` Dubai Harbour Marina: [55.139787, 25.081055] (inland Dubai Marina block)
  → [55.1383, 25.0935] (Dubai Harbour basin centre, between Cruise Terminal A and Bay Marina).
  All routes referencing the old endpoint coord auto-snapped to new value.

## Phase 4 marquee tone-down
- 10 UAE marquee corridors with traffic_weight ≥0.65 retuned to band 0.45–0.55
  (and 0.60 for hero route if matched). Spiderweb routes (0.15) untouched.

## Gates
- qa_land_crossing FAIL: 219 / 5198 (= #79ag baseline; no regression).
- LB-171 SEAL recomputed: blobs.ROUTES/FEATURES_BY_TYPE/CLUSTERS sha256 + full file_hashes.
- LB-23 zip-patch viable (≤20 files content-changed conceptually, but ROUTES.json
  edits → full re-zip is required).

## Known limitations (carry-forward)
- Intra-Palm hops still register "crossing Palm bbox" because endpoints lie inside
  the bbox — needs frond-resolution polygon to author trunk-channel routing.
- Axis-aligned bboxes are conservative; fine deck geometry (e.g., follow Palm
  trunk waterway) deferred to next pass.
