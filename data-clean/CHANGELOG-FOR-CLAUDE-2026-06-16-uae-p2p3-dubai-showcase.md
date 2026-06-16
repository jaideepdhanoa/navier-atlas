# CHANGELOG — Gold #79ab — UAE Phase 2/3 Dubai Showcase (scrub+enrich corridor bite)

**Sealed:** 2026-06-16 · **Base:** #79aa (`navier-export-20260616T121620Z-uae-p1-cleanup.zip`, 5184 routes)
**Method:** LB-192a base-gold extraction → LB-67/81 zip-patch delta overlay (ROUTES.json + CLUSTERS.json only; FEATURES_BY_TYPE.json byte-identical — all endpoint BPs pre-existing). LB-171 SEAL recompute on actual blob bytes after assembly. LB-191a haversine platform recompute.

## Counts vs #79aa base
- ROUTES:   5184 → 5189  (Δ +5 new + 1 edit-in-place, 0 removed)
- CLUSTERS: 104  → 106   (Δ +2 — Palm Jumeirah + The World Islands)
- POIs:     10644 → 10644 (Δ 0 — all 8 featured BPs pre-existing, verified)
- CITIES:   176  → 176    (Δ 0) · Priority-cities 37 → 37

## New corridors (6 Dubai featured routes, all Pioneer II, land-gate PASS 0.000 km)
1. `rn-42aa1791bb60` NEW — Dubai Harbour Marina <-> Palm Jumeirah Marina West (2.1 nm)
2. `rn-dcc7d4c3b9f9` NEW — Dubai Harbour Marina <-> Bluewaters Marina (1.1 nm)
3. `rn-12f09bd4d4d6` NEW — Dubai Harbour Marina <-> Cote d'Azur (The World) (9.2 nm)
4. `rn-b49c885ed913` NEW — Palm Jumeirah Marina West <-> Atlantis The Palm Jetty (1.3 nm, intra-Palm spoke)
5. `rn-355d8ba3c15a` NEW — Dubai Creek Marina <-> Al Seef Marine Transport Station (1.5 nm, in-channel OSM creek A*)
6. `rn-af9d261fd724` EDIT-IN-PLACE (LB-104) — Cote d'Azur (The World) <-> Anantara World Islands (2.4 nm, intra-World spoke re-solved fine-OSM)

## New clusters (2 — LB-174 real-BP anchors)
- `palm-jumeirah-dubai` "Palm Jumeirah" — anchor bp-8294b693cc (Palm Jumeirah Marina West) [55.135, 25.11527]
- `the-world-dubai` "The World Islands" — anchor bp-2e74b28e12 (Cote d'Azur / Heart of Europe) [55.15889, 25.23078]

## Featured BPs (all pre-existing, multi-channel reuse LB-55, water-verified)
Dubai Harbour Marina, Palm Jumeirah Marina West, Atlantis The Palm Jetty, Bluewaters Marina,
Cote d'Azur Resort Marina (Heart of Europe), Anantara World Islands Resort Jetty, Dubai Creek Marina, Al Seef Marine Transport Station.

## Seal gates — ALL PASS
- gate_city_ids: PASS (211 nodes / 5189 routes / 106 clusters)
- gate_premint_pair: 0 / 5189 @0.5 (17th consecutive 0-flag at scale)
- gate_cluster_anchor_realbp: PASS=104 WARN=2 FAIL=0 (2 new Dubai clusters resolve to real BPs; great-lakes/shanghai synthetic WARN by design)
- gate_osm_noise_bp --check-only --global: PASS (0 safe kills; 29 advisory route-referenced — carry-forward unchanged)
- gate_endpoint_labels: 4 HARD carry-forward (Philippines + uae-careem + uae-luxury×2; unchanged since #79w) / 3 WEAK advisory — 0 NEW
- gate_partner_rationale_leak: clean
- UAE land gate (qa_land_crossing over 6 Dubai corridors): 6/6 PASS 0.000 km
- LB-175a pre-build: ROUTES 5189 >= floor 5072 / pier-coord verification on featured endpoint BPs
- economics sidecar: 78 pinned / 48 pending; 0 prior-pinned corridors lost (regression guard)

## Deferred data-quality follow-ups (NOT fixed this bite — cascade risk)
- bp-ee346f4b52 'Heart of Europe — Main Marina (The World)' mislocated ~9 nm SW (used by 2 existing Bluewaters routes that only pass via the mislocation).
- bp-e9bcfc941c 'Lebanon Island Beach Club Jetty' mislocated ~5 nm E of real Lebanon Island (used by existing Business Bay route).
