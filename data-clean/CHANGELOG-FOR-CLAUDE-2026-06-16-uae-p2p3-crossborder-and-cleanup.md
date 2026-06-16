# CHANGELOG — Gold #79ae — UAE P2P3 cross-border + cleanup bite (2026-06-16)

**Base:** #79ad (`navier-export-20260616T205824Z-uae-p2p3-marjan-sharjah-trunk.zip`, 5201 routes).
**Method:** LB-67/81 zip-patch overlay (ROUTES.json + FEATURES_BY_TYPE.json) onto extracted #79ad base. LB-192a: live `data-clean/` skeletal (economics + partners only, no SEAL/ROUTES) → base-gold drift detected & logged; spliced onto gold extract. LB-171: SEAL recomputed on actual blob bytes.

## Counts vs #79ad
- ROUTES:   5201 → **5198**  (Δ −3 net: +2 cross-border mints, −5 dedup duplicate occurrences)
- POIs:     10646 → 10646 (Δ 0 — 2 World BPs relocated in place, none added/removed)
- CITIES:   176 → 176 · PRIORITY_CITY 37 → 37 · CLUSTERS 107 → 107 (unchanged)

## Changes
**+2 cross-border aspirational corridors (Quanta-LR, amber-dashed, aspirational:true):**
- `e__dubai-uae__dubai-harbour__doha-qatar__old-doha-port` — Dubai Harbour Marina (Dubai) → Old Doha Port (Doha), 195.4nm. Land gate PASS 0.000 km.
- `e__abu-dhabi-uae__breakwater-corniche__manama-bahrain__bfh-marina` — Marina Mall / Breakwater Marina (Abu Dhabi) → Bahrain Financial Harbour Marina (Manama), 235.4nm. Land gate PASS 0.000 km.

**2 World (offshore Dubai) BP relocations** (resolves deferred #79ab mislocation flag):
- `bp-ee346f4b52` Heart of Europe — Main Marina (The World): [55.134401, 25.077766] → [55.1545, 25.2118] (moved ~8.1nm NE to true marina position).
- `bp-e9bcfc941c` Lebanon Island Beach Club Jetty: [55.274839, 25.196819] → [55.1862, 25.2316] (moved ~5.25nm W).

**3 Heart-of-Europe routes re-solved edit-in-place (LB-104, byte-stable ids)** after the BP relocations, all PASS land gate 0.000 km:
- `rn-199599f6b2c8` Bluewaters Ferry → HoE Main Marina (10.23nm, 14 pts)
- `rn-5a196635c94f` Bluewaters Marina → HoE Main Marina (9.88nm, 10 pts)
- `rn-c0a6b911f416` Dubai → HoE Main Marina (9.95nm, 13 pts)

**1 demotion to aspirational label-only:**
- `rn-f0352563fbc0` Business Bay Marine Transport Station → Lebanon Island Beach Club Jetty (Dubai Water Canal link) — geometry [] (label-only), aspirational:true + render_style amber_dashed. Reason: Dubai Water Canal unmodelable; honest path ~0.95km coarse-land. **Pending Jaideep review.**

**5 duplicate `ics-*` route-id occurrences removed (dedup sweep — clears the long-standing owed item):**
- ics-3c55ce6e65 / ics-5d9f47b3c4 / ics-b7b04ed77d / ics-be4a12ba5c / ics-e33d21f71e — each appeared 2× (Pulau Gaya vs Pulau Mabul destination); kept Pulau Gaya variant (17 props), dropped Pulau Mabul variant (16 props). 0 duplicate route ids remain.

## Seal gates — ALL PASS
- gate_city_ids: PASS (211 nodes / 5198 routes / 107 clusters / 0 unresolved)
- gate_premint_pair: FLAGGED 0
- gate_cluster_anchor_realbp --check-only: PASS=105 WARN=2 FAIL=0 (great-lakes-usa / shanghai-china synthetic-no-BP WARN by design)
- gate_osm_noise_bp --check-only --global: CHECK-ONLY PASS (0 safe kills; 29 advisory carry, 0 new)
- gate_partner_rationale_leak: clean
- gate_endpoint_labels: 4 HARD carry (Philippines + uae-careem + uae-luxury×2 FLAG_MISSING_IN_GOLD), 0 NEW (advisory, exit 0)
- UAE land gate (qa_land_crossing) over 5 changed corridors w/ geometry: 0 / 5 FAIL (0.000 km)
- Full-file land QA: 219 / 5198 = unchanged from base 219 / 5201 (0 new crossers)
- LB-175a: ROUTES 5198 ≥ floor 5072 (margin 126)

## Economics sidecar (LB-28)
Carried forward unchanged from #79ad (78 pinned / 48 pending). Pre-rebuild resolution probe: the 2 new aspirational cross-border ids match **0** `corridors.json` pins (which expect al-khobar→bahrain / doha-lusail→bahrain) and 0 pending corridors → provably byte-identical → carried (LB-199 regression-guard; avoids stale-aggregate rebuild).

## Carries / follow-ups
- `rn-f0352563fbc0` aspirational label-only — **pending Jaideep review**.
- Oman-Musandam points filed under `fujairah-uae` — upstream geo carry (log-only).
- 4 HARD endpoint-label flags — 9th consecutive carry; owed corridors.json re-pin/label-fix bite (incl. re-pin Wynn corridor to rn-dd4500aa99f5).
- Live `data-clean/` skeletal — rehydrate-live housekeeping bite still recommended.
