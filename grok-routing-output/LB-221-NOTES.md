# LB-221 Notes — Abu Dhabi dredged-channel mask holes

Generated: 2026-06-18

## Deliverables

| File | Purpose |
|------|---------|
| `uae_gulf_land_v2.wkb` | Rebuilt with AD channel cutouts + jetty cores (134 polys) |
| `ad_channel_cutouts.py` | 7 dredged fairway centerlines + refined reclamation + jetty land cores |
| `build_landmask_v2.py` | Updated builder (subtracts channels, re-adds jetty cores) |
| `solve_routes_phase2.py` | Updated Hud hand-waypoints |

## Channel fairways authored

| Channel | Width | Connects |
|---------|------:|----------|
| `hud_west_approach` | 450m | Hudayriyat → EP corridor |
| `lulu_west_channel` | 400m | Lulu ↔ mainland / EP |
| `saadiyat_reem_gap` | 350m | Saadiyat Marina ↔ Reem |
| `saadiyat_lulu_north` | 550m | Saadiyat Beach Club ↔ Lulu |
| `khalifa_coast_approach` | 500m | Khalifa Port south fairway |
| `khalifa_saadiyat_coast` | 450m | Khalifa → Saadiyat north coast |
| `yas_north_fairway` | 450m | Offshore north of Yas → Yas Marina |
| `emirates_palace_approach` | 300m | EP marina mouth |

Method: buffered `LineString` corridors subtracted from land union; marina jetty cores re-added as small land disks so BPs stay LAND.

## Sentinel checks: 15/15 pass

Includes AD channel midpoints (water) + all 8 AD jetty BPs (land).

## Hud-set solve status (strict QA, v2 + coarse)

| Route | Status |
|-------|--------|
| Hudayriyat → Emirates Palace | **PASS** |
| Lulu → Emirates Palace | **PASS** |
| Saadiyat Marina → Reem | **PASS** |
| Hudayriyat → Yas Marina | UNSOLVED — long coastal; coarse mask + v2 grid |
| Khalifa Port → Yas Marina | UNSOLVED — Taweelah→Yas fairway; coarse mainland FP |
| Khalifa Port → Saadiyat Beach Club | UNSOLVED — v2 clean but coarse 0.61 km interior |
| Saadiyat Beach Club → Lulu | UNSOLVED — v2 0.15 km interior (channel width) |

**7/7 strict-QA pass** (2026-06-18 LB-224): offshore waypoints along lat ~24.478 fairway + widened channel cutouts + 120 m marina apron. See `LB-224-NOTES.md`.

## Overall Phase 2 impact

After channel rebuild: **22/42 strict-QA pass** (up from 0/42 pre-channels). Includes improved densify `rn-*` solves.

## Tasklet apply

1. Replace geom-gates `uae_gulf_land.wkb` with rebuilt `uae_gulf_land_v2.wkb`
2. Merge 3 new Hud PASS geometries from `route-solutions.jsonl` (EP + Lulu + Saadiyat-Reem)
3. Long Hud coastal hops: apply with extended offshore waypoints or mark aspirational until LB-224