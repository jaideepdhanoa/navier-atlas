# Gold #79y — Wave 8 scrub+enrich (Red Sea Global captive-resort sub-cluster split — FINAL POI scrub+enrich wave)

Date: 2026-06-16 UTC
Base: navier-export-20260616T100515Z-scrub-w7-triad.zip (Gold #79x)
LB ref: LB-193

## Scope
- Single metro: `red-sea-global-ksa` (captive-resort archetype).
- 0 kills (captive-resort metro has no OSM stream → 0 in-scope POIs; sister to LB-186/LB-189/LB-192 thin-starter rule).
- 9 new BPs + 7 new routes + 3 new sub-clusters + 1 LB-174 country re-anchor.

## Counts vs Gold #79x
- POIs:    10,812 → 10,821 (Δ +9)
- ROUTES:  5,369  → 5,376  (Δ +7)
- CITIES:  173    → 176    (Δ +3)
- CLUSTERS: 101   → 104    (Δ +3; +1 in-place LB-174 re-anchor on `saudi-arabia`)

## Sub-cluster split (LB-193 codification)
Parent `red-sea-global-ksa` city_id retained. 3 new city features + 3 new sub-clusters anchored on real BPs (LB-174 compliant):

| Sub-cluster | Anchor BP | Coords | Captive archetype |
|---|---|---|---|
| `the-red-sea-archipelago` (archipelago) | bp-w8-shura-marina (Shura Island Marina) | 36.8264, 25.5106 | captive-resort |
| `amaala-triple-bay` (coastal) | bp-w8-amaala-marina (AMAALA Triple Bay Marina) | 36.4717, 26.7456 | captive-resort |
| `thuwal-private-retreat` (coastal) | bp-w8-thuwal-jetty (Thuwal Private Retreat Jetty) | 39.0850, 22.2780 | captive-resort |

## LB-174 re-anchor
- `saudi-arabia` country cluster: from virtual `red-sea-global-ksa` city_id [36.85, 26.0] (mid-land defect) → bp-w8-shura-marina [36.8264, 25.5106]
- `member_city_ids` widened to include `the-red-sea-archipelago-ksa`, `amaala-triple-bay-ksa`, `thuwal-private-retreat-ksa`.
- LB-174 audit backlog burn-down: ≈28 → ≈27 remaining.

## BPs minted (9)
- bp-w8-shura-marina (marina) — Shura Island Marina
- bp-w8-ummahat-jetty (hotel_jetty) — Ummahat AlShaykh Resort Jetty
- bp-w8-sheybarah-jetty (hotel_jetty) — Sheybarah Island Resort Jetty
- bp-w8-laheq-jetty (hotel_jetty) — Laheq Island Jetty (The Ring)
- bp-w8-rsi-seaplane (seaplane_base) — Red Sea International (RSI) Seaplane Base
- bp-w8-amaala-marina (marina) — AMAALA Triple Bay Marina
- bp-w8-amaala-yacht-club (yacht_club) — AMAALA Yacht Club Jetty
- bp-w8-thuwal-jetty (hotel_jetty) — Thuwal Private Retreat Jetty
- bp-w8-kaust-harbour (marina) — KAUST Harbour (Thuwal)

Coord confidence: `medium` (press-derived, not Mapbox direct) — codified standing rule for captive-resort BPs.

## Routes minted (7)
- bp-w8-rsi-seaplane ↔ bp-w8-shura-marina — 26.7 nm — Pioneer II
- bp-w8-shura-marina ↔ bp-w8-ummahat-jetty — 19.9 nm — Pioneer II
- bp-w8-shura-marina ↔ bp-w8-sheybarah-jetty — 11.3 nm — Pioneer II
- bp-w8-shura-marina ↔ bp-w8-laheq-jetty — 4.4 nm — Pioneer II
- bp-w8-amaala-marina ↔ bp-w8-amaala-yacht-club — 0.4 nm — Pioneer II
- bp-w8-kaust-harbour ↔ bp-w8-thuwal-jetty — 1.8 nm — Pioneer II
- bp-w8-amaala-marina ↔ bp-w8-shura-marina — **76.6 nm — Quanta-LR** (amber-dashed aspirational, intra-region captive-resort; outside P-II 70nm hard cap per LB-189 → classified Q-LR; 3rd archetype of Q-LR-outside-P-II aspirational)

LB-191a post-mint haversine recompute: AMAALA↔Shura corrected from payload ~70nm → actual 76.6nm, auto-classified Q-LR aspirational. Standing rule validated for 3rd consecutive bite.

## Seal gates — ALL PASS
- `gate_endpoint_labels`: 4 HARD carry-fwd (Philippines + UAE, identical to #79x) / 3 WEAK advisory.
- `gate_city_ids`: PASS (211 valid nodes / 5,376 routes / 104 clusters).
- `gate_partner_rationale_leak`: clean.
- `gate_osm_noise_bp --check-only --global`: PASS (0 safe kills; 33 advisory carries unchanged from #79x).
- `gate_premint_pair`: 0 / 5,376 flagged at threshold 0.5 — **14th consecutive 0-flag at scale**.
- LB-175a pre-build: ROUTES 5,376 ≥ floor 5,369 ✓ / new-BP pier-coord verification 100% (premint gate proxy) / P-II 70nm hard cap 0 violations / Q-LR 700nm cap max 76.6nm ✓.
- `datastore_audit`: pending Phase 4 step 8.

## Learnings captured (LB-193 codification → `_scrub-enrich-learnings.md`)
- **Captive-resort partner-wrapper sub-cluster split pattern (LB-193):** keep parent city_id, mint N city features + N sub-clusters anchored on real BPs (LB-174), re-anchor country cluster + widen member_city_ids. First instance: RSG → 3 sub-clusters under saudi-arabia.
- **3rd archetype of Q-LR-outside-P-II aspirational:** captive-resort intra-region (AMAALA↔Shura 76.6nm).
- **Coord confidence tier for captive-resort BPs:** default `confidence: medium` (press-derived not Mapbox direct).
- **LB-191a validated 3rd time:** post-mint haversine recompute caught payload distance defect (AMAALA↔Shura ~70nm → 76.6nm). Never trust payload distance_nm; recompute over endpoint coords pre-stage.
- **LB-174 audit backlog burn-down:** saudi-arabia re-anchored (≈28 → ≈27 remaining country/region clusters on virtual city_id anchors).

## Wave 8 = FINAL POI scrub+enrich wave
Plan-file `PLAN-POI-SCRUB-AND-ENRICHMENT-2026-06-16.md` marked COMPLETE upon seal.

## Carry-forwards (unchanged from #79x)
- 4 HARD endpoint-label flags (Philippines + UAE).
- 33 advisory route-referenced noise candidates.
- ~27 LB-174 audit candidates remaining.
- navier-content.db disk I/O carry (13+ consecutive bites; not regressed).
