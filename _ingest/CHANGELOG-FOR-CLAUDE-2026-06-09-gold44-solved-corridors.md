# Gold #44 — water-solver pre-routed corridors + geometry-verified label fixes (2026-06-09)

Base = Gold #43 (navier-export-20260609T185526Z.zip, 5248 routes). Routes 5248 -> 5257 (+9).

## B2 — 9 LB-59 water-solver PRE-ROUTED corridors (spliced VERBATIM, no straight-line gate)
Each corridor's multi-waypoint water-routed arc (verify: CLEAR, LB-59 solver + independent fine-OSM gate)
was spliced verbatim as the route LineString. 8 Pioneer II (commercial) + 1 Quanta-LR (amber_dashed / H2_2026_plus).
ics- island-hop scheme; both endpoints already gold cluster members (no CLUSTERS/FEATURES change).
Tioman (Singapore↔Tioman, 108nm Quanta) INTENTIONALLY EXCLUDED — still in solver queue.

| route_id | market | from -> to | sea_nm | vessel |
|---|---|---|---|---|
| ics-40367adcc3 | cambodia | Sihanoukville ferry port -> Koh Russey (Ream private-island resort cluster; Alila Villas / Koh Russey Resort) — Koh Russey arrival pier | 8.5 | Pioneer II |
| ics-474721ce45 | cambodia | Sihanoukville ferry port (Serendipity / Ochheuteal) -> Saracen Bay pier, Koh Rong Sanloem | 13.0 | Pioneer II |
| ics-8301406c4e | cambodia | Sihanoukville Port (Song Saa Lounge) -> Song Saa Private Island (off NE Koh Rong, near Prek Svay) | 18.8 | Pioneer II |
| ics-dfe4ef40b3 | cambodia | Sihanoukville ferry port -> Koh Kong town (Cardamom coast) | 75.4 | Quanta-LR |
| ics-5a3e48e4cf | philippines | Manila — Esplanade Seaside Terminal (SM Mall of Asia, Pasay) -> Camaya Coast Beach & Resort Ferry Terminal (Mariveles, Bataan) | 35.3 | Pioneer II |
| ics-b737c5ae68 | phuket | Royal Phuket Marina -> Khao Phing Kan (James Bond Island), Phang Nga Bay | 20.5 | Pioneer II |
| ics-25ecef3e3b | taiwan | Magong South Sea Visitor Center / Magong Harbour (馬公南海遊客中心), Penghu -> Qimei Nanhu Port (七美南滏港), Qimei Island | 25.2 | Pioneer II |
| ics-f21c5d7e8d | vietnam | Tuan Chau International Marina -> Cat Ba town port (Beo Harbour) | 16.3 | Pioneer II |
| ics-0263dd49bb | vietnam | Duong Dong (Phu Quoc) -> An Thoi (south Phu Quoc / An Thoi archipelago gateway) | 12.9 | Pioneer II |

## B3 — 10 geometry-verified label fixes (in place, geometry untouched)
- ics-91951379c0: 'Kaohsiung' -> 'Liuqiu (Xiaoliuqiu)' (to/to_city/to_label/label). Geometry end 0.4nm from Liuqiu, not Kaohsiung.
- 9 Borneo routes (ics-3c55ce6e65, ics-5d9f47b3c4, ics-be4a12ba5c, ics-e33d21f71e, ics-b7b04ed77d, rn-1cc974a00262, rn-47f19e2c1004, rn-9d4c519ed0df, rn-e1e1fcbd2819): 'Mabul Island Resorts' -> 'Gaya Island Resorts' and 'Pulau Mabul' -> 'Pulau Gaya' (endpoints sit 0.7nm from Pulau Gaya off KK; real Mabul ~160nm SE).

## B4 — corridors.json null
- cambodia 'Sihanoukville' -> 'Koh Ta Kiev / Ream National Park' route_id set null (defer; ics-9df91bf7d4 self-mislabel logged for later geometry-first relabel).

## Economics sidecar
69 -> 78 records / 32 -> 23 pending. All 9 newly-minted route_ids resolve (previously pending deferred land-clippers).

## Endpoint label<->geometry seal gate (LB-62): 0 HARD FLAGS.

GOLD-COPY.txt NOT flipped — parent promotes.
