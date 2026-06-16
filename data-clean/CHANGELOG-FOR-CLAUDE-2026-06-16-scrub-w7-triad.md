# CHANGELOG — Wave 7 scrub+enrich (TAG-ONLY triad)
**Date:** 2026-06-16
**Bite:** scrub-w7-triad
**Mode:** TAG-ONLY (no new routes, no scrub kills — thin-starter rule, sister to LB-186 Ionian / LB-189 Maldives)
**Prior gold:** #79w → **New gold:** #79x
**LB-ref:** LB-192 / LB-174 / LB-188 / LB-189 / LB-191

## Scope
3 metros / clusters:
- **Galápagos (Ecuador)** — Baltra · Puerto Ayora · Puerto Baquerizo Moreno · Isabela
- **Belize** — Belize City · San Pedro (Ambergris) · Caye Caulker · Placencia
- **Lamu (Kenya)** supplement — Lamu · Manda · Shela · Kiwayu

## Phase A — Scrub
0 kills across all 3 metros. All three are node-id-style starters: `boarding-points/*.json` exists but `FEATURES_BY_TYPE.poi` carries 0 entries for these `parent_city_id`s. `gate_osm_noise_bp.py` over bbox returns advisory flags ONLY against curated POIs → zero in-scope POIs → zero advisory flags → zero kills.

## Phase B — Enrich (4 BPs / 0 routes / 0 new clusters / 3 re-anchors)
4 new ferry_terminal Gateway BPs (LB-188 corollary):

| id | name | parent_city_id | coords |
|---|---|---|---|
| bp-w7-blz-anchor | Belize City SPBE Marine Terminal | belize-city-cayes-belize | -88.1847, 17.4941 |
| bp-w7-gal-anchor | Puerto Ayora Main Dock (Muelle de los Pescadores) | santa-cruz-galapagos-ecuador | -90.3121, -0.7434 |
| bp-w7-ken-anchor | Likoni Ferry — Mombasa Island Terminal | mombasa-kenya | 39.6656, -4.0783 |
| bp-w7-lam-kiwayu | Kiwayu Island Jetty (Mkokoni) | lamu-kenya | 41.2667, -1.9167 |

0 new routes — all 3 country/region clusters already had ≥4 members with pre-existing intra-mesh routes (TAG-ONLY honored).

## LB-174 re-anchors (3 country clusters → real pier BPs)
- **belize** → `bp-w7-blz-anchor` (was `belize-city-cayes-belize` city_id virtual)
- **galapagos-ecuador** → `bp-w7-gal-anchor` (was `santa-cruz-galapagos-ecuador` city_id virtual)
- **kenya** → `bp-w7-ken-anchor` (was `bp-w6-456755fa1b` Mombasa Old Port Jetty — replaced per payload)

LB-189 reuse honored: re-anchored existing clusters instead of minting duplicates.

## Counts vs Gold #79w
- POI: 10,808 → 10,812 (Δ +4)
- ROUTES: 5,369 (unchanged)
- CITIES: 173 (unchanged)
- CLUSTERS: 101 (unchanged; 3 re-anchored in place)

## Gates — all PASS / no new flags
- `gate_endpoint_labels`: 4 HARD carry-fwd (Philippines + UAE, same as #79w) / 3 WEAK advisory
- `gate_city_ids`: PASS (208 valid nodes / 5,369 routes / 101 clusters)
- `gate_partner_rationale_leak`: clean
- `gate_osm_noise_bp --check-only` (bbox + --global): PASS (0 safe kills; 21 / 33 advisory carries unchanged)
- `gate_premint_pair`: 0 / 5,369 flagged at threshold 0.5 — **13th consecutive 0-flag**

## Learnings
- TAG-ONLY = scrub-skip + jump to BP-promotion (codify into wave skill)
- boarding-points → POI promotion: when curated `boarding-points/<metro>.json` exists but absent from `FEATURES_BY_TYPE.poi`, mint `bp-w<N>-<slug>-anchor` directly; promotable to helper `promote_boarding_points_to_pois.py`
- LB-188 corollary confirmed: LB-174 anchor BPs for country/region clusters MUST be `bp_type=ferry_terminal` (Gateway). 4-of-4 this bite.
- LB-189-reuse-with-supplement-mint: when payload says "X supplement", mint BPs under an existing `city_id` rather than mint a new `city_id`.
- ~28 LB-174 audit candidates remain — recommend single-bite LB-174 sweep next.
