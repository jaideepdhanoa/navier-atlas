# UAE geometry recovery — full 4-workstream plan (2026-06-29)

**Status:** EXECUTING — no deferrals  
**Parent:** `handoff/PROPOSAL-CREDIBILITY-PLAN-2026-06-29.md`  
**Honest baseline:** Audit PASS ≠ map truth; 15×1 HAND_WAYPOINTS; fronds deferred; 1900 mesh fails; 3/29 hubs PASS

---

## Workstream A — UAE geometry truth (P0)

| Step | Goal | Done when |
|------|------|-----------|
| A1 | 30–50 commercial pairs, 3–8 waypoints each | `uae_hand_waypoints.json` ≥30 pairs, avg waypoints ≥3, receipt with `qa_pass` |
| A2 | Frond-resolution land mask + channel-primary solver | Palm-tagged routes 0 failures at 0.08 km; intra-Palm pairs in triage pass |
| A3 | `_geometry_land_km` sync + mesh traffic discipline | Live QA matches route props; partner-page mesh capped |
| A5 | Browser visual QA | `UAE-VISUAL-QA-RECEIPT.json` for /careem, /noon |

**Pipeline:** `author_uae_hand_waypoints.py` → `mint_hand_waypoints.py` → `mint_story_channels.py --no-fail-only --uae-only --apply`

---

## Workstream B — Global mesh (~1900 fails)

Batch via `run-geometry-seal-lane.sh --wave g3 --apply` → `fix_route_geometry.py --all`

---

## Workstream C — Hub RE-GROUND (24 REWRITE)

`reground_proposal_surfaces.py` → `relink_partner_journeys.py --apply` → re-audit → expand preflight §3.7

---

## Workstream D — Schema (5 partners)

Normalize `boats`, `route_scope`, `featured_route` shape; scaffold `centara-thailand` market phases.

Target: `validate_partner_proposals.py` → 63/63 pass.

---

## Execution order

1. A1 → A2 → A3 → A5 (UAE)
2. B0/B1 mesh burn-down
3. C wave 1+2 (all REWRITE hubs)
4. D schema normalization
5. Gate expansion + final audit

---

## Receipts

| Receipt | Path |
|---------|------|
| HAND_WAYPOINTS | `handoff/partner-map-model/UAE-HAND-WAYPOINTS-v1.json` |
| Channel graphs | `handoff/partner-map-model/UAE-CHANNEL-GRAPHS-v2.json` |
| Story mint | `handoff/partner-map-model/geometry-channel-mint-report.json` |
| Visual QA | `handoff/partner-map-model/UAE-VISUAL-QA-RECEIPT.json` |
| Mesh | `handoff/partner-map-model/GEOMETRY-TRIAGE.json` |
| Hubs | `handoff/partner-map-model/PROPOSAL-FIDELITY-AUDIT.json` |