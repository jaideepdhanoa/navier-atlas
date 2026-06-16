# CHANGELOG — 2026-06-16 — UAE Phase 1 substrate cleanup (Gold #79aa)

**Bite:** UAE-P1-cleanup (scrub-only substrate cleanup; NO new geometry, NO new corridors).
**Base gold:** #79z (`navier-export-20260616T105646Z-hk-1-housekeeping.zip`, 5376 routes) — extracted as
canonical splice base per LB-192a. Live `data-clean/` ignored (degraded: missing SEAL/ROUTES/FEATURES).

## Counts vs #79z
- ROUTES:  5376 → 5184  (Δ −192, decrease expected — noise/dedupe/micro-cull)
- POIs:    10821 → 10644 (Δ −177, BP deletes)
- CITIES:  176 → 176 (unchanged)
- PRIORITY_CITY: 37 → 37 (unchanged)
- CLUSTERS: 104 → 104 (unchanged; `uae` cluster anchor bp-44685987bc survived, re-parented sharjah→fujairah, referenced by id so no CLUSTERS.json edit)

## What changed (delta applied — FEATURES_BY_TYPE.json + ROUTES.json only)
- **OSM-noise scrub:** 91 noise BP kills (50 unique names) across dubai/abu-dhabi/sharjah/ras-al-khaimah — food chains, yacht-rental brokers, retail/LLC, experiences/marketing, residences, gym, medical, jet-ski/dragonboat. Samples: "Classy.Boat", "Barry's Dubai Marina", "Dhow Cruise Dubai Marina", "Dubai Harbour Residences", "321 Sports", "Golden Harbour LLC".
- **Dedup:** 86 colocated losers removed (65 groups; <150m + same normalized name). Canonical = correct-parent > most-route-refs > lowest-id; route endpoints rewritten to canonical BP id (rn-* hashes do not embed bp ids — LB-104 safe). Systemic cross-emirate replication corrected.
- **City re-parent:** 83 survivor re-parents by coordinate longitude bands + lat gate + name overrides (AD<54.95<Dubai<55.36<Sharjah<55.70<RAK<56.15<Fujairah; RAK Al Marjan/Al Hamra/Mina Al Arab; Fujairah Khorfakkan/Dibba east-coast; Sharjah Al Khan/Al Majaz/Aquarium).
- **Micro-route cull:** 48 spiderweb <1nm routes culled; 22 marquee showcase <1nm kept (Palm Jumeirah resort ring, Saadiyat, Al Marjan, Bluewaters↔The World, Bal Harbour) — Jaideep-approved rule (keep <1nm only if BOTH endpoints marquee resort/island).
- **Route changes:** 119 dropped noise-endpoint, 25 dropped duplicate-pair, 48 micro-culled, 118 re-parented/relabeled (emirate prefix corrected, e.g. "Abu Dhabi: Dubai Harbour…" → "Dubai: Dubai Harbour…").

## BP totals
- Deleted: 177 BPs. UAE survivors: 315 (dubai 141 / abu-dhabi 82 / ras-al-khaimah 34 / sharjah 29 / fujairah 29).
- **Marquee survival — ALL present & correctly parented:** Dubai Harbour, Palm Jumeirah, Bluewaters, The World (Heart of Europe / Lebanon Island), Dubai Creek, Al Marjan/RAK, Yas Marina, Saadiyat, Sir Bani Yas, Hudayriyat, Sharjah (Al Khan/Aquarium/Al Majaz), AD Corniche/Al Bateen.

## Seal gates — ALL PASS
- gate_city_ids: PASS (211 valid nodes / 5184 routes / 104 clusters / 0 mis-parents)
- gate_premint_pair: 0 / 5184 flagged @0.5 (16th consecutive 0-flag at scale)
- gate_osm_noise_bp --check-only --global: PASS (0 safe kills; 29 advisory route-referenced, all non-UAE carries — UAE noise scrubbed this bite)
- gate_cluster_anchor_realbp: PASS=102 WARN=2 FAIL=0 (great-lakes-usa, shanghai-china synthetic-no-BP WARN by design — baseline preserved)
- gate_endpoint_labels: 4 HARD carry-forward unchanged from #79w/x/y/z (Philippines + UAE×3 in corridors.json finance model) / 3 WEAK advisory — no NEW flags; cleanup bite doesn't author labels
- Route floor: PASS 5184 ≥ 5072 (margin 112)
- New dangling refs introduced: 0 / route-refs to deleted BPs: 0

## Economics sidecar (LB-28)
- Rebuilt against new geometry (fresh full-recipe aggregates: grab/careem/jih-global/red-sea-global/saudi-redsea-pif/qatar).
- 78 route-pinned records / 48 _pending_route_pin. 0 prior-pinned corridors lost (no UAE corridor regressed to pending). All 11 UAE careem corridors preserved. (+34 non-UAE corridors newly resolved vs the under-resolved #79z sidecar — net improvement, ID-based exact only.)

## Known carries (not regressions)
- 5 `ics-` duplicate route ids — pre-existing in #79z (identical set), carry-forward.
- 4 HARD endpoint-label flags (Philippines + UAE×3) — owed a dedicated label-fix bite.
