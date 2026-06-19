# Phase 1 Notes — Grok Routing (landmask v2 + seaward candidates)

Generated: 2026-06-18T09:01:16.412396+00:00

## Deliverables

- `uae_gulf_land_v2.wkb` — upgraded landmask
- `seaward-candidates.json` — per-BP coastline-normal seaward points (LB-211)

## Landmask v2 method

- Base: v1 WKB (111 polygons)
- Removed Palm unified blobs at indices: [87, 88, 89, 94]
- Added 18 hand-authored Palm polygons (trunk + fronds + crown + crescent; inter-frond gaps = water)
- Added 6 Abu Dhabi reclamation polygons (Hudayriyat, Khalifa Port, Lulu, Saadiyat, Reem)
- Subtracted 15 dredged-channel cutouts (LB-221 channel holes)
- Output: 132 polygons

## Overpass (tight-bbox)

- Palm Overpass: OK (MultiPolygon)
- AD coast Overpass: OK (MultiPolygon)
- Overpass polygons NOT merged into v2 (would solidify Palm frond channels).
- Fetched 59 Overpass clip polygons; excluded from union (Palm channel safety)

## Sentinel checks

| Point | Expected | Actual | Pass |
|---|---|---|---|
| palm_spine_channel | WATER | WATER | ✓ |
| palm_trunk_mid_channel | WATER | WATER | ✓ |
| atlantis_jetty | LAND | LAND | ✓ |
| kempinski_jetty | LAND | LAND | ✓ |
| hudayriyat_bp | LAND | LAND | ✓ |
| khalifa_port_bp | LAND | LAND | ✓ |
| lulu_bp | LAND | LAND | ✓ |
| saadiyat_marina | LAND | LAND | ✓ |
| reem_waterfront | LAND | LAND | ✓ |
| open_gulf | WATER | WATER | ✓ |
| hud_channel_mid | WATER | WATER | ✓ |
| lulu_west_channel_mid | WATER | WATER | ✓ |
| saadiyat_reem_gap_mid | WATER | WATER | ✓ |
| yas_north_fairway_mid | WATER | WATER | ✓ |
| ep_approach_mid | WATER | WATER | ✓ |

## Seaward candidates (LB-211)

- BP ids from densify-residual tier: 35
- Resolved: 35/35

## Phase 2 handoff

- Tasklet wires `seaward-candidates.json` into `_solve_corridor_waypoints.py` / densify pass
- Run `qa_land_crossing.py --overlay uae_gulf_land_v2.wkb` on route-solutions output
- Palm cross-trunk (9): attempt A* with v2 channels; expect 3–5 UNSOLVED needing hand waypoints

## Kickoff answers (locked)

1. **Overpass:** tight-bbox first (this build); flag failures above
2. **Seaward JSON shape:** `_meta` + `candidates.{bp_id}` per BRIEF §8
3. **Cross-trunk Palm:** attempt all 9; UNSOLVED where channel selection ambiguous
