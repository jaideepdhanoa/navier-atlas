# Gold #38 — JIH Maldives resort-jetty splice + economics pins (2026-06-09)

## What changed
- **+6 Velana→resort jetty routes** spliced into ROUTES.json (5201 → 5207):
  `e__velana__{kurumba,gili-lankanfushi,baros,oneonly-reethi-rah,constance-halaveli,conrad-rangali}-jetty`
  All `platform: Pioneer II` (all ≤70nm: 2.1 / 6.4 / 8.3 / 22.0 / 37.7 / 59.3 nm).
- **economics_by_route_id.json sidecar: 71 → 77 records, pending 23 → 17.** The 6 jetties now pin
  JIH economics (corridors.json route_id set for each).
- All other blobs (FEATURES_BY_TYPE / STORIES / VESSEL_SPECS / CLUSTERS) byte-identical to Gold #37.

## How the endpoints were sourced (NO Google Places — LB-55)
Multi-channel resolver (Wikidata entity-match + Mapbox cross-check) + satellite visual gate:
- 3 double-confirmed (Wikidata+Mapbox <0.05nm): gili-lankanfushi, baros, constance-halaveli.
- 3 Wikidata-entity + satellite-confirmed resort island: kurumba, oneonly-reethi-rah, conrad-rangali.
- **4 left as honest NULL** (not shipped): waldorf-ithaafushi (WD coord was open ocean — satellite
  showed no island), ritz-fari, patina-fari, westin-miriandhoo (no entity match). Null > confidently-wrong.

## GEOMETRY CAVEAT — re-solve when convenient
The 6 geometries are **densified great-circle lines**, NOT land-gate-solved. Reason: `global_land_mask`
(~900MB) OOMs the current 570MB-free sandbox, so `_solve_corridor_waypoints.py` could not run.
Mitigation: every corridor was **visually verified open-water** against Mapbox satellite with the
straight line overlaid (see resolver notes). Endpoints are authoritative; economics pins are
authoritative. When a high-memory env is available, re-solve these 6 through the land-gate and
replace geometry in place (endpoints unchanged). The `_gold38_jih_jetties` SEAL key lists the ids.

## Integrity
ROUTES.json spliced at byte level (existing bytes preserved exactly; 6 features appended before
closing `]`). SEAL ROUTES + sidecar hashes recomputed over file bytes and verified. Postflight-equiv:
route floor 5207≥5072 ✓, all blob/sidecar hashes match ✓, 6 jetties present + pinned ✓.
