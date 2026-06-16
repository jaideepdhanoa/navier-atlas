# Gold #79z — Wave HK-1 housekeeping (LB-194)

**Date:** 2026-06-16
**Prior gold:** #79y (LB-193 Wave 8 RSG captive-resort)
**Mode:** Housekeeping — no route/POI/city/cluster count delta.
**Counts:** routes 5376 (Δ0) · pois 10821 (Δ0) · cities 176 (Δ0) · clusters 104 (Δ0)

## What changed

### Task A — LB-174 cluster-anchor burn-down (CLUSTERS.json)
- 49 country/region clusters re-anchored from virtual `city_id` sources to real BP anchors (centroid-on-real-BP rule).
- 3 opportunistic fixes: `mexico` anchor coords snapped to BP (was 1.11km drift); `oman` dangling anchor BP `bp-095a41dfcb` → `bp-217780de19` (Jebel Sifah Marina); `philippines` dangling anchor BP `bp-d4738f6ad2` → `bp-3face0c774` (Berberabe Port).
- 2 synthetic-no-BP clusters remain WARN by design (no minted POI to anchor): `great-lakes-usa`, `shanghai-china`. Promotion to FAIL requires an enrich-mint plan (§43 archetype 1).

### Task B — Dar es Salaam re-parent (FEATURES_BY_TYPE.json)
- 12 mainland-Dar BPs (lat < −6.5°S) re-parented from `zanzibar-tanzania` → `dar-es-salaam-tanzania`. Payload said 8; geo+name triangulation found 12. All 12 are clearly mainland Dar/Kunduchi/Bongoyo/Slipway/Kigamboni — not Zanzibar archipelago. **Flagging for human ack: confirm OK or specify exclusions.**
- BP ids unchanged → all route endpoints still resolve. `tanzania` cluster already lists both `dar-es-salaam-tanzania` and `zanzibar-tanzania` in `member_city_ids` — no cluster edit needed.

### Task C — Codification
- **LB-192a** (base-gold extraction mandate): live `data-clean/` chronic-stale since #79v; splice worker Phase 0 now mandates extracting prior gold zip as canonical base. Added to `navier-scrub-wave-splice-seal.md` Phase 0 + `_SHARED_PRINCIPLES.md` §45 A.
- **LB-193** (captive-resort sub-cluster split): 4th cluster-mint archetype added to `_SHARED_PRINCIPLES.md` §44 and `PARTNER-RECAL-PLAYBOOK.md` cluster-mint archetypes table.
- **LB-191a** (post-mint haversine standing rule + auto Q-LR amber-dashed bump): codified in `_SHARED_PRINCIPLES.md` §45 B; already referenced in `navier-scrub-enrich-wave.md` Phase B.
- **`gate_cluster_anchor_realbp.py`** wired into Phase 3 postflight step 6d. Baseline post-HK-1: PASS=102 WARN=2 FAIL=0.

## Seal gates
| Gate | Result |
|---|---|
| `gate_city_ids` | PASS (211 valid nodes / 5376 routes / 104 clusters) |
| `gate_cluster_anchor_realbp` (NEW postflight 6d) | PASS=102 WARN=2 FAIL=0 (was 51/2/51 pre-bite) |
| `gate_premint_pair` | 0 flagged / 5376 routes (15th consecutive 0) |
| `gate_partner_rationale_leak` | clean |
| `gate_osm_noise_bp --check-only` | PASS (21 advisory route-referenced, carry-forward) |
| `gate_endpoint_labels` | 4 HARD FLAGS carry-forward unchanged from #79x/#79y (not touched by this bite) |

## Carry-forward
- 4 HARD endpoint-label flags identical to #79y baseline (PH Cebu-Bohol, uae-careem Marina↔Creek, uae-luxury Jebel Dhanna↔Sir Bani Yas, uae-luxury Dubai Harbour↔Wynn Al Marjan).
- Economics sidecar (`economics_by_route_id.json`) unchanged — routes unchanged; carried forward from #79y verbatim.

## Blockers for human judgment
1. Task B count discrepancy: payload said 8 mainland-Dar BPs, found 12. All 12 re-parented; please confirm or specify exclusions.
2. `great-lakes-usa` and `shanghai-china` synthetic-no-BP clusters: recommend follow-up greenfield BP mint (§43 archetype 1) or accept perpetual WARN.

## LB refs
LB-174, LB-186, LB-188, LB-189, LB-190, LB-191a, LB-192a, LB-193, LB-194
