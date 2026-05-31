# CHANGELOG FOR CLAUDE — 2026-05-31 (session: display-bug fix + Claude data-list complete)

**TL;DR:** Fixed a systemic display bug that left ~17 cities rendering ZERO POIs (Vietnam,
Cambodia, Taiwan, Malaysia, Korea, Turkey, Japan), moved Maldives + Colombo to South Asia,
densified 7 markets, and completed your entire 9-item data list. Rebuild from the new
`data-clean/` — counts below. **Bake from `data-clean/`, not `partner-pitch/`.**

---

## 1. CRITICAL DISPLAY BUG FIXED — BP_CITY_MAP convention drift (root cause)

**Symptom (Jaideep-reported):** Vietnam, Cambodia, Taiwan, Malaysia, Korea, Turkey, Japan
cities showed no POIs on the map.

**Root cause:** ARCH.2 canonicalized node ids to `{place}-{country}` (e.g. `da-nang-hoi-an-vietnam`),
but `BP_CITY_MAP` **values** in `build.py` still used the old `{country}-{place}` form
(`vietnam-da-nang-hoi-an`). Those values matched no node → POIs were orphaned to non-existent
parents → never rendered.

**Fix:** Remapped 17 stale values to canonical node ids in `build.py`. Now-rendering counts:
Da Nang 48 · Ha Long 33 · Phu Quoc 36 · Koh Rong 21 · Kaohsiung 27 · Penghu 21 · Penang 32 ·
Desaru 17 · Sabah/KK 27 · Busan 39 · Jeju 34 · Yeosu 24 · Bodrum 52 · Antalya 36 · Çeşme 27 ·
Hokkaido 19 · Setouchi 52.

**Hardening (new build-time GATE):** `build.py` now hard-fails if any `BP_CITY_MAP` value does
not resolve to a real node (main or supplemental). Console: `[gate] BP_CITY_MAP: all N values
resolve to real nodes ✓`. This class of silent orphaning cannot recur.

## 2. REGION FIXES
- **Maldives (`male-maldives`) + Colombo: SEA → South Asia.** Moved `male-maldives.md` from
  `regions/sea/` to `regions/south-asia/` (region derives from directory). Colombo already SA.
- **Turkey shell node: Europe → Turkey.** Moved `regions/europe/turkey.md` → `regions/turkey/`,
  removed the now-empty `europe/` dir. Eliminates the lone-"Europe" region split you flagged.
- **New region-completeness census** printed at build time (no city left untagged).
- Region normalizer already folds SEA/Southeast Asia, Caribbean/LatAm-Caribbean, etc. (was the
  older live build that showed variants).

## 3. TWO NEW RENDERING CITIES — Colombo + Istanbul
- Had briefs/nodes but **no BP files** → zero POIs. Created seed corridor BP files, then ran the
  gate-clean densify conveyor: **Colombo 107 BPs**, **Istanbul 90 BPs**.
- Added both to `BP_CITY_MAP` (`colombo-sri-lanka`, `istanbul-turkey`).

## 4. DENSIFY SWEEPS (gate-clean, prominence-driven)
Managed markets Jaideep flagged as gappy — all re-swept:
Dubai 71→151 · Abu Dhabi 43→148 · Singapore 53→160 · Bali 65→267 · Phuket 54→204.

## 5. DATA-QUALITY: junk-POI removal + hardened negative filter
- The `bp_on_water_gate.py` audit surfaced inland non-boardable POIs that matched marine search
  terms. **NOTE:** the gate uses `is_ocean`, so it false-flags legitimate **river/lake/delta**
  piers (Bangkok Chao Phraya, Lake Toba, SF Sacramento delta) — water-distance is NOT a safe
  deletion criterion. Cleanup was **name-based, swept-only** (never curated).
- Removed 11 unambiguous junk swept points (e.g. "Secret Yacht Party Dubai", "Marina Salon",
  "Khao Sok Bus Station", "Navy Exchange Mall", "Marino Mall", "Party Boat").
- **Hardened `densify_boarding_points.py` `NEG_RE`** permanently: office/headquarters/salon/mall/
  carnival/party/kost/sales gallery/showroom/furniture/interiors/bus station/immigration/dry dock/
  etc. Future sweeps reject these at collection time.
- **Ghantoot confirmed ON WATER** (`is_ocean=True` @ 54.88127,24.90089) — your item #8 resolved.
  (Minor: a low-confidence duplicate "Jalboot Marine Network - Abu Dhabi Mall" entry was dropped.)

## 6. YOUR 9-ITEM DATA LIST — COMPLETE
1. **Journeys → node ids:** every `journeys_unlocked[]` entry now has `from_node_id`/`to_node_id`;
   `route_id` added where a clean cross-file edge exists (grab 3/6, careem/dubai-rta/mpa 1/3, hawaii 3/5).
2. **End-state per partner:** all 10 partners now have an `end_state{}` block — `headline`,
   `addressable_regions`, `addressable_market_count`, `addressable_footprint`, `end_state_cities[]`
   (canonical ids), `steady_state{total_markets,total_corridors,vessels_at_scale,platform_mix,tam_framing}`,
   `narrative`. Schema matches grab's (your cited example).
3. **Grab stale final-phase id:** `manila-cebu-palawan-philippines` → split to `manila-philippines`
   + `cebu-philippines` + `palawan-philippines`; grab `end_state_cities` also canonicalized
   (`malaysia-desaru-coast`→`desaru-coast-malaysia`, `malaysia-penang`→`penang-malaysia`).
4. **Region-label canonicalization:** see §2. One label per region; completeness gate added.
5. **`from_city_id`/`to_city_id` on every route:** **100% (2996/2996).** `route_labels.py` now
   resolves endpoint → stable node slug (`from_node`/`to_node`) → `cluster_city_id` fallback
   (intra-cluster archipelago spokes attribute to their parent cluster).
6. **Voice → second person:** `partner_context.*`, `differentiation.why_navier`/`vs_status_quo`,
   `the_ask.partner_brings`, and partner-named `why_now` rewritten to address the partner as
   "you/your" across all 10 partners. **Field KEYS unchanged** (their_ambition etc.) — only copy.
7. **Careem platform reconciliation:** Dubai↔Abu Dhabi route = Pioneer II @ 46.5nm (matches JSON);
   tightened "~60 nm" copy to "~47 nm".
8. **Ghantoot on water:** confirmed (see §5).
9. **Per-partner SEAL.json:** NOT done this session (lower priority) — single-bundle seal stands.

## 7. BUILD / SEAL CHANGES
- **`build.py` now emits `VESSEL_SPECS.json`** to `output-external/` (the seal requires it as a
  blob; it was previously only inlined as `__VESSELS__`). count=2 (Pioneer II + Quanta-LR).
- Seal verdicts: `--ext pass --land pass`; `bp_on_water` = REVIEWED; integrity gate PASS.

## 8. CURRENT SEALED COUNTS (data-clean/)
- FEATURES_BY_TYPE: **city=77, poi=4460, priority_city=23**
- ROUTES: **2996** (100% city-id attributed)
- STORIES: 12 · VESSEL_SPECS: 2
- city_briefs: 78 · partners: 10 (internal/deck_only stripped)
- Coverage scorecard: 89 cities — DONE=20, NEARLY=26, IN_PROGRESS=12, STUB=31.

## FILES TOUCHED
- `atlas-external/build.py` — BP_CITY_MAP remap (17) + Colombo/Istanbul + BP-orphan gate +
  region completeness census + VESSEL_SPECS blob emit.
- `atlas-external/route_labels.py` — from_city_id/to_city_id emit + cluster_city_id fallback.
- `atlas-external/densify_boarding_points.py` — hardened NEG_RE.
- `world-map/regions/south-asia/male-maldives.md` (moved), `world-map/regions/turkey/turkey.md` (moved).
- `atlas-external/boarding-points/{colombo-sri-lanka,istanbul-turkey}.json` (new seeds + swept) +
  re-swept dubai/abu-dhabi/singapore/bali/phuket + 11 junk removed across 7 files.
- `partner-pitch/partners/*.json` — journeys node-ids, end_state, voice, grab id fixes, careem copy.
