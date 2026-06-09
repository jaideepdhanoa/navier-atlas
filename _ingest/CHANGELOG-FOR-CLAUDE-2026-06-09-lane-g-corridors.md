# Gold #39 — Lane G TIER1 corridor splice (+4 inter-cluster routes)

**Base:** Gold #38 (`navier-export-20260609T050225Z.zip`, 5,207 routes)
**Result:** 5,211 routes (+4). All other blobs byte-identical except CLUSTERS (one member added).

## What changed
Spliced 4 **satellite-verified, open-water, Pioneer II (≤70nm)** inter-cluster corridors that fill
previously tag-only / orphan clusters. Endpoints geo-resolved via the LB-55 multi-channel recipe
(Wikidata + Mapbox + bbox sanity gate) — **no Google Places**. Each line was visually confirmed
clear-water on Mapbox satellite before minting.

| Route id | Corridor | nm | Vessel |
|---|---|---|---|
| `e__belize-city-cayes-belize__belize-city-water-taxi__caye-caulker-belize__caye-caulker-main-dock` | Belize City ↔ Caye Caulker | 17.4 | Pioneer II |
| `e__kaohsiung-taiwan__kaohsiung-port__penghu-taiwan__magong-harbor` | Kaohsiung ↔ Magong (Penghu) | 68.9 | Pioneer II |
| `e__mafia-tanzania__kilindoni-port__dar-es-salaam-tanzania__dar-ferry-terminal` | Mafia (Kilindoni) ↔ Dar es Salaam | 69.5 | Pioneer II |
| `e__belize-city-cayes-belize__belize-city-water-taxi__placencia-belize__placencia-village-pier` | Belize City ↔ Placencia | 62.6 | Pioneer II |

Node ids = canonical `CLUSTERS.json` members. Geometry = densified great-circle (precise resolved
boarding-point coords as endpoints). `edge_class: inter-city`; front-end renders ↔ bidirectional.

## Blob updates (SEAL kept consistent)
- `ROUTES`: hash + count → 5,211
- `CLUSTERS`: added `caye-caulker-belize` to the `belize` cluster `member_city_ids` (75 clusters unchanged); hash updated.
- Source `clusters/city-cluster-map.json`: `caye-caulker-belize → belize` (source-side; gold uses CLUSTERS.json).

## Two node-brief gaps (content-lane follow-up, NOT blocking)
`caye-caulker-belize` (new) and `mafia-tanzania` (pre-existing orphan member) have **no `city_briefs/*.json`**.
Consistent with the existing orphan-member pattern (mafia-tanzania has shipped brief-less for many golds).
Nodes render from route props; detail panels will be sparse until briefs are authored.

## Deferred (honest holds — NOT shipped)
- **Dibba ↔ Zighy Bay (Oman)** — straight line crosses the Musandam headland (satellite-confirmed land clip).
  Needs the real water-following solver (the OOM-blocked land-gate). Endpoints are T1-confirmed; geometry pending.
- **>70nm corridors → held Quanta-LR batch:** Palma ↔ Mahon (78nm), Fukuoka ↔ Busan (119nm), Zanzibar ↔ Pemba (87nm).
- **Galapagos Puerto Ayora ↔ Villamil** — Wikidata/Mapbox disagree on Puerto Ayora by ~41nm; held until re-verified (exactness > coverage).

## Re-solve note
Same as #38: the 4 geometries are great-circle. When the high-memory land-gate solver can run
(needs >900MB; this sandbox has ~570MB free), re-solve for precise water-following paths.
Endpoints + topology are authoritative now.
