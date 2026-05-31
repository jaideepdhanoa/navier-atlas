# BP-WATER BACKLOG RESOLVED (2026-05-31, late) — appended

The pre-existing `bp_on_water` "known-gaps" backlog is now fully cleared. Gate verdict is an **honest PASS — 0 true mis-geocodes**.

**5 genuine geocode errors fixed** (had matched company HQs / wrong-city namesakes):
- `jkt-krakatau-anchorage`: Jakarta company "PT Krakatau Niaga" → Anak Krakatau volcano, Sunda Strait (105.42, −6.10)
- `jkt-bintan-lobam`: estate's Jakarta office → Teluk Lobam, Bintan (104.26, 1.00)
- Penang `Pulau Aman` jetty → Batu Musang Jetty (100.41, 5.27)
- Setouchi `Hoshinoya Setouchi (pipeline)`: matched Hoshinoya **Tokyo** → Seto Inland Sea / Naoshima waters (134.07, 34.46)
- Ghantoot Marina (abu-dhabi + dubai files): snapped to nearest coastal water

**58 benign points transparently allowlisted** (NOT errors — ocean-mask can't see them):
- New file `bp_water_allowlist.json` + generator `bp_water_allowlist_gen.py`
- Named navigable water-body bounding boxes: Chao Phraya river, Dubai Creek/Business Bay canal, Lake Toba, Lake Tōya, Halong/Hai Phong delta, Phang Nga estuary, Sungai Lebam estuary, Brunei Bay/Temburong
- Plus region-centroid label points (no pier token) and planned/pipeline labels
- `bp_on_water_gate.py` now loads the allowlist; verdict = true mis-geocodes only

**No action needed from Claude** — these are data-clean source fixes already in the reseal.

---

# Changelog for Claude — 2026-05-31 — US Expansion + Partner Stories

**Seal**: fresh seal written to `atlas-repo/data-clean/` (SEAL.json updated). Bake from `data-clean/` as always — NOT raw `partner-pitch/`.

## What changed (rebuild + redeploy required)

### New nodes (8) — Hawaii + Florida + Bay Area
- **Hawaii (4)**: `oahu-honolulu-hawaii-usa`, `maui-county-hawaii-usa`, `kona-hilo-hawaii-island-usa`, `kauai-hawaii-usa`
- **Florida (3)**: `palm-beach-florida-usa`, `naples-fort-myers-florida-usa`, `tampa-bay-sarasota-florida-usa`
- **Bay Area (1)**: `san-francisco-bay-area-usa`
- All 8 have: world-map `.md`, city-anchor coords, BP files (53 points, 0 unresolved), intra-cluster Pioneer II spokes, cross-file edges (inter-island Hawaii incl. Quanta-LR line-hauls Honolulu↔Maui/Kauaʻi; Pioneer II ʻAlenuihāhā & ʻAuʻau crossings; Palm Beach↔Miami Gold-Coast connector), and full city_briefs.

### City briefs: 70 → 78
- +8 new (above). Marquee depth: Oʻahu, Maui County, Palm Beach, SF Bay. Starter depth: Kona/Hilo, Kauaʻi, Naples, Tampa.

### Partners: 9 → 10
- **NEW `hawaii.json`** — Pulama Lānaʻi × DOT Harbors, "Superferry done right" hero. 3-phase: Pulama Lānaʻi signature arrival → Maui County inter-island (ʻAlenuihāhā seasickness-relief hero) → statewide DOT Harbors network.
- **`uber.json` US market enriched** — US phases now reference real nodes (Miami → Florida Gold Coast + SF Bay → Hawaii + Caribbean); journeys updated for Miami/Palm Beach/SF/Honolulu/Bahamas.

### Stories: 7 → 12 (ALL 10 partners now covered)
- **NEW `gen_partner_stories.py`** (in `atlas-external/`) — deterministic projector: every partner page that lacks a hand-authored story is projected to a `partner_story` in `supplemental-stories.json`. Curated supplemental (maldives-hospitality, qatar-transport) preserved verbatim; base stories (grab/careem/red-sea-global/singapore-mpa/uae-waterfront) untouched.
- Projected this run: `abu-dhabi-itc`, `dubai-rta`, `hawaii`, `saudi-pif`, `uber`.
- **COMMON DATA CONTRACT**: partner page = single source of truth; story auto-derives. Re-run `gen_partner_stories.py` before seal whenever a partner page changes. Relevant for the Proposal Designer app (W7).

### Featured cities (PRIORITY_CITIES): 13 → 23
- Added: miami, oahu-honolulu, maui-county, palm-beach, san-francisco-bay-area, nassau, san-juan, usvi-bvi, st-barths-st-maarten + (existing 13). 23 baked into FEATURES_BY_TYPE priority_city tag.

### Pipeline changes
- `resolve_cross_file_edges.py`: `_normalize()` now strips diacritics + parentheticals (Hawaiian ʻokina names match). 8 new CITY_ALIASES added.
- `build.py`: `BP_CITY_MAP` + `_SPLIT_SLUGS` + `PRIORITY_CITIES` extended for the 8 new nodes.

## Gate verdicts (this seal)
- externalization: **PASS** — 0 exclusion hits (79 files)
- land_crossing: **PASS** — 0/1559
- bp_on_water: FAIL (non-blocking) — pre-existing SEA/MENA harbor-mask + Manila rot known-gaps; **0 from new US/Caribbean/Hawaii nodes**
- referential_integrity: **PASS** — 0 errors (2 known-gap warnings)

## Action for Claude
1. `build.mjs` from `data-clean/` → `atlas-data.js`
2. `deploy.sh` → Vercel
3. Expect: 61 cities, 1860 POIs, 23 featured, 1559 routes, 12 stories, 78 briefs, 10 partners.
