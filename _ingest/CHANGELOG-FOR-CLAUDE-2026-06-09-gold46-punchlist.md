# Gold #46 — post-#44 punch-list fixes (P1a / P1b / P2b / P3)

**gold_seq:** 46 · **routes:** 5,258 (unchanged) · **city nodes:** 165→170 · base: Gold #45 (Tioman).
No geometry changed — all 5,258 route geometries asserted byte-identical to #45. Economics unchanged (78 resolved / 23 pending; all route_ids verified present in new ROUTES).

## P1 — render-breaking (FIXED)
**P1a — city_id resolution.** 5 routes had a `from/to_city_id` that resolved to no node (render silently dropped the endpoint); 2 used a bare country token.
- Added 5 city nodes (verified endpoint coords + cluster_id + country): `caye-caulker-belize`, `cozumel-mexico`, `playa-del-carmen-mexico`, `floreana-galapagos-ecuador`, `tioman-island`.
- Re-pointed bare tokens to existing 0.0 nm nodes: `cambodia` → `cambodia__koh-rong-krabey-koh-kood-thailand-soneva-kiri`; `korea` → `korea__busan-geoje-cross-strait-fukuoka-cross-border`.
- **New seal gate `gate_city_ids.py`** (complements the LB-62 endpoint gate): asserts every ROUTES `*_city_id` + every CLUSTERS `member_city_ids` resolves to a node. PASS (0 unresolved / 5,258 routes / 75 clusters / 198 nodes).

**P1b — Singapore tri-border mislabel.** SG west/south waterfront boarding points were parented to foreign clusters (`riau-islands-indonesia` / `desaru-coast-malaysia`) → intra-SG hops mislabeled foreign + genuine SG↔ID/MY crossings invisible to cross-border detection.
- 230 route endpoint `*_city_id` reclassifications (geometry-first coordinate classifier): riau→sg 102, desaru→sg 120, desaru→riau 3, riau→desaru 5. (The non-SG flips are genuine corrections too: Nongsapura/Bentan/Nirup→Indonesia; Desaru/Tanjong Balau/Kukup→Malaysia.)
- 159 POI `parent_city_id` re-parents to the city each physically sits in.

**trip_purpose `"local"`.** `"local"` was scope, not purpose (100% correlated with intra-city). 
- Added a real **`trip_scope`** field to EVERY route: `intra_city` 5,034 / `domestic` 113 / `cross_border` 111 (zero nulls).
- **Nulled** `trip_purpose` where it was `"local"` (2,711 routes).
- **FRONTEND HANDOFF:** the hover should read **`trip_scope`** (not `trip_purpose`) for scope. This kills the "Local · Local" bug.

## P2 — in this seal
**P2b — cluster `label_anchor`.** Authored on-land `label_anchor:[lng,lat]` for spread clusters: `spain` (Palma), `greece` (Mykonos town), `mexico` (Playa del Carmen), `belize` (Belize City), `galapagos-ecuador` (Puerto Ayora), `malaysia` (Tioman). Render prefers it when present.

## P3 — housekeeping
- `country` backfilled on 53 empty-country nodes (unambiguous `{place}-{country}` id suffix) — also eliminated all null `trip_scope`.
- cluster_id node-property lag: **0 found** (already consistent both directions — likely fixed in an earlier seal).
- **FLAG:** 7 stray `bp-*` ids are miscategorised inside the FEATURES `city` array (left null on country). Needs upstream reclassification.

## Still owed (next tranche — acknowledged, not in this seal)
- **P2a** Singapore marquee corridors: East Coast→Marina/CBD + Marina→Changi/Pulau Ubin (need real boarding points); confirm the 89 single-token weak matches were swept.
- **P2c** per-record economics `breakdown{ revenue_build, run_cost, result }`.
- **P3** city_briefs: caye-caulker, floreana, playa-del-carmen, cozumel, mafia, Cape Cod & Islands + new #44 corridor endpoints.
- Confirm the East Coast→CBD economics drop (prior export) was intentional vs accidental.
