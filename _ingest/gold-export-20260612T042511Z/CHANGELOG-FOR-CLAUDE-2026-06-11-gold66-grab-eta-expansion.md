# Gold #66 — Phase η (Grab delta v2 expansion)

Base: Gold #65 (`navier-export-20260611T190524Z.zip`, 5,285 routes).
Method: LB-67 SAFE-RESEAL (unzipped prev gold, overlay-only). LB-34/56 byte-level append.

## Routes — 12 new directional edges (6 bidirectional corridors)

All endpoints are existing gold POIs (or appended POI for Carabao). Great-circle geometry, haversine distance, Pioneer II (≤70nm).

1. **Telaga Harbour (Langkawi) ↔ Koh Lipe Bundhaya Pier (TH)** — 23.7nm cross-border (international)
   - `bp-aa9ef06a49` Telaga Harbour Park [99.682054, 6.367978] ↔ `bp-bc4ae4ea8d` Koh Lipe [99.303232, 6.486755]
   - `e__langkawi-malaysia__telaga-harbour__langkawi-malaysia__koh-lipe-bundhaya-pier` (+ reverse)
2. **Budai Port ↔ Magong Harbor (Penghu)** — 34.4nm (domestic)
   - `bp-34e32bc2f3` [120.154386, 23.384663] ↔ `bp-42b7325105` [119.562783, 23.569402]
   - `e__penghu-taiwan__budai-port__penghu-taiwan__magong-harbor` (+ reverse)
3. **Magong Harbor ↔ Chikan Harbour (Baisha)** — 6.3nm (domestic)
   - `bp-42b7325105` ↔ `bp-addfeba39b` [119.60346, 23.668372]
   - `e__penghu-taiwan__magong-harbor__penghu-taiwan__chikan-harbour-baisha` (+ reverse)
4. **Kaohsiung Gushan ↔ Cijin Ferry Pier** — 0.3nm (domestic)
   - `bp-78479cbbc5` [120.269955, 22.619782] ↔ `bp-b5c6de26ca` [120.269698, 22.614089]
   - `e__kaohsiung-taiwan__gushan-ferry-pier__kaohsiung-taiwan__cijin-ferry-pier` (+ reverse)
5. **CCP/Esplanade Pier ↔ Corregidor (North Dock)** — 24.8nm (domestic)
   - `bp-fdd18892ef` [120.980312, 14.541926] ↔ `bp-d95bae0870` [120.583975, 14.388496]
   - `e__manila-philippines__ccp-esplanade-pier__manila-philippines__corregidor-north-dock` (+ reverse)
6. **Cagban Jetty (Boracay) ↔ San Jose (Said) Port, Carabao Island** — 6.9nm (domestic)
   - `bp-3fd20df42b` [121.939258, 11.940361] ↔ `bor-carabao-san-jose-said-port` [121.95964, 12.05413] (NEW POI)
   - `e__boracay-philippines__cagban-jetty__boracay-philippines__carabao-san-jose-said` (+ reverse)

## POI append — Carabao Island
`bor-carabao-san-jose-said-port` "San Jose (Said) Port, Carabao Island" [121.95964, 12.05413]
ferry_terminal · parent_city_id `boracay-philippines` · operational · OSM+web 2026-06-11.

## Restyle — Kaohsiung↔Magong
`e__kaohsiung-taiwan__kaohsiung-port__penghu-taiwan__magong-harbor` platform `Pioneer II` → `quanta_lr` (amber-dashed / H2_2026_plus / LB-112(b)/LB-117).

## Sidecar refresh
`economics_by_route_id.json`: 104 records (route-pinned), 21 pending. Engine: `build_economics_sidecar.py` (same as transparent Sheet).

## Counts
Routes 5,285 → **5,297** · POIs 11,373 → **11,374** · Clusters 75 · Cities 170 + 37 priority_city.

## Gates
- LB-67 city_id gate: **PASS** (198 valid nodes; all from/to_city_id + member_city_ids resolve).
- LB-62 endpoint label gate: 14 HARD FLAGs — all `FLAG_MISSING_IN_GOLD` PRE-EXISTING in Gold #65 corridors.json bindings (none introduced by these mints; new `e__` route_ids are not bound in corridors.json yet).

## Notes
- Spine `boracay-philippines` node verified present (E task — verify only).
- Pure corridor-class deltas (LB-17). No `add_market.py`. No index.html / no GitHub push.
- GOLD-COPY.txt NOT flipped — parent promotes.
