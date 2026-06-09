# Gold #45 — Singapore (Tanah Merah) → Tioman Island (final Quanta-LR staged Grab corridor)

**Base:** Gold #44 (navier-export-20260609T200638Z.zip, 5,257 routes).
**This build:** +1 route → **5,258**. CLUSTERS 75 (malaysia +1 member: `tioman-island`). FEATURES_BY_TYPE byte-unchanged.

## What changed
- **B2 pre-routed edge-mint** `ics-1a53f8237d`: Singapore (Tanah Merah Ferry Terminal) → Tioman Island
  (Tekek / Berjaya jetty, east-coast Malaysia). 12-waypoint water-solved arc (LB-59 fine-OSM, clips=0,
  min_clearance=0.36nm) spliced **VERBATIM** as the LineString — NO straight-line land gate (LB-65 resolved).
  Quanta-LR → `platform:"Quanta-LR"`, `render_style:"amber_dashed"`, `availability:"H2_2026_plus"`,
  `vessel_class:"quanta_lr"`. `distance_nm=108.6` (routed sea nm). New node `tioman-island` [104.1494, 2.8227]
  added to `malaysia` cluster (Floreana byte-level template). ROUTES byte-append (LB-56).
- **B4 corridors.json relink**: `cross-border` corridor #3 → `route_id=ics-1a53f8237d`,
  `from="Singapore (Tanah Merah)"`, `to="Tioman Island (east-coast Malaysia)"`, `distance_nm=108.6`.
  Roadmap leg, **NOT** in the committed Grab floor (128 boats/$39M) — model dedups on label, no growth.py/grab.json cascade.

## Gates
- Economics sidecar: **78 records / 23 pending** (true baseline 78/23 → after 78/23: zero growth, zero regression —
  the roadmap leg has no committed grab agg row, so it pins no record, exactly as specified).
- Endpoint label↔geometry seal-gate (LB-62): **0 HARD FLAGS** (8 pre-existing WEAK single-token binds, non-blocking).
- datastore_audit: PASS.

GOLD-COPY.txt NOT flipped — parent promotes.
