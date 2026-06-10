# Gold #48 — Geometry-first partner recalibration (JIH/Maldives + Careem/UAE + Saudi/RSG + Qatar economics)

**Base:** Gold #47 `navier-export-20260609T223827Z.zip` (extracted full zip, overlay-only per LB-67). **Routes 5,260 → 5,269 (+9).** Economics **80 → 97 resolved / 21 → 5 pending**. CLUSTERS (75) / FEATURES_BY_TYPE / STORIES / VESSEL_SPECS **byte-unchanged** (hash-verified against the #47 seal). `build.mjs` reads `data-clean/` as before; the `economics_by_route_id.json` sidecar is regenerated — re-join it onto route features by `route_id`.

## What changed (all geometry-first, water-solved + independently fine-OSM verified — LB-59/66; arcs spliced verbatim, no straight-line re-gate)

### JIH / Maldives recalibration (LB-69)
- **35 existing `e__velana__` / `e__mald__` arcs rebuilt** with independently re-verified endpoint coords (Wikidata/Nominatim/Overpass + atoll-bbox gate; Mapbox is banned for Maldives resorts — it collapses POIs to Malé). Route ids are STABLE; only `geometry` + `distance_nm` changed. Worst corrections: St Regis Vommuli 2.7 → 17.0 nm, The Standard Huruvalhi 11.5 → 40.4 nm, Le Meridien Thilamaafushi 4.0 → 19.8 nm, Ayada 12.9 → 29.6 nm. Two airport anchors (Dharavandhoo, Kudahuvadhoo) were themselves displaced ~11 nm, dragging every spoke.
- **4 missing Velana spokes minted** (Pioneer II): `e__velana__patina-fari-jetty` (27.4 nm), `e__velana__ritz-fari-jetty` (26.5 nm), `e__velana__waldorf-ithaafushi-jetty` (14.6 nm), `e__velana__westin-miriandhoo-jetty` (61.4 nm).

### Careem / UAE mints (Pioneer II)
- `rn-2e112eb57142` — **Bluewaters Island / Dubai Marina Pier → Dubai Festival City Marina** (up Dubai Creek), 18.1 nm.
- `rn-2f5e450c7e2c` — **Dubai Harbour Marina → Saadiyat Beach Club Jetty** (Abu Dhabi), 52.4 nm.
- `rn-f94dae947809` — **Dubai Harbour Marina → Wynn Al Marjan Island Arrival Lagoon** (RAK), 53.3 nm.

### Saudi mints (KSA / Red Sea water-solver arcs)
- `ics-4e71b19ab7` — **Sindalah Marina → Magna** (NEOM), 30.8 nm, Pioneer II.
- `ics-c52891a862` — **Shura Island Marina → AMAALA Triple Bay**, 82.9 nm, **Quanta-LR** (amber-dashed, H2 2026+).

## Economics sidecar — regenerated (97 records / 5 pending)
- **NEW `qatar` market** in `finance/model/corridors.json` (4 corridors; 3 near-term agg rows — Lusail↔Manama 94.5 nm held for Quanta-LR). `qatar` added to the sidecar PARTNERS set.
- **JIH now 43/43 resolved** (was the bulk of #47's 21 pending) — geometry-first rebinds onto the recalibrated/minted arcs; distances in `corridors.json` corrected to routed sea nm.
- Careem 14, Grab 31, Saudi-PIF 4, RSG 2, Qatar 3. Remaining **5 pending = Grab `endpoints_city_level_not_pinned`** (honest defers, not regressions).
- Per-record `breakdown` payload (revenue_build / run_cost / result) carried from #47.

## Gates / audit (all green on #48)
- Endpoint label↔geometry seal-gate (LB-62): **0 HARD FLAGS** (13 weak single-token binds, all known-benign city/island anchor tokens incl. new `nujuma` Saudi rows).
- `gate_city_ids` (LB-67): **PASS** — 198 valid nodes, 5,269 routes, 75 clusters, 0 unresolved.
- SEAL blob hashes verified over raw bytes for every blob + sidecar; carried blobs byte-identical to #47.
