# PTA Geometry-Completeness — Grok Handoff Index (Phases A–D remediation)

**From:** Tasklet · **Date:** 2026-07-02 · **Purpose:** one clean handoff so Grok can do all corridor routing + hand-waypoints with **zero land crossings**, bringing every Phase A–D authority to real-world network scale.

**Global rules (all specs):** ID-based match only · null-beats-wrong · additive only · seal at 0 km land with explicit hand waypoints · re-run land-crossing QA each pass (hold program-wide 0-crossing record) · honest operational-status flags · preserve Batch-5 #150 economics scrub · never rewrite WSF growth_case · never invent route_ids.

**Handback loop:** Grok mints BPs + seals corridors → emits mint receipt → Tasklet binds partner `journeys_unlocked` in both trees (data-clean `ensure_ascii=True`; partner-pitch `ensure_ascii=False`; indent 2; trailing newline).

## Spec set
| Phase | Spec | Scope |
|---|---|---|
| R1 | `GROK-SPEC-R1-mintheavy-seal.md` | Seal 10 already-declared mint-heavy corridors (Rotterdam-first, kills empty render) |
| R2 | `GROK-SPEC-R2-calmac.md` | CalMac 41 new BPs / 27 corridors (Clyde + Hebrides) |
| R2 | `GROK-SPEC-R2-seoul-hangang-bus.md` | Seoul Hangang 4 new BPs / 7 corridors (full 8-pier line) |
| R2 | `GROK-SPEC-R2-kolkata-wbtc.md` | Kolkata 10 new ghats / 9 corridors (Hooghly mesh) |
| R3 | `GROK-SPEC-R3-greenfield-anchor-deepening.md` | Manila 5→13, Kochi 6 routes, Hamburg 15→21, Helsinki island add; validate rio/toronto/mersey/hcmc/brisbane |
| R4/R5 | `GROK-SPEC-R4-R5-seal-and-chip-hygiene.md` | fullers360 3 routes, hawaii Lahaina-Manele, wsf 4 + bc-ferries 4 land-QA; batch-5 chip bind |

## Supporting artifacts
- `audit/PTA-GEOMETRY-COMPLETENESS-AUDIT.md` — full 44-authority audit (421 sealed, 0 land crossings).
- `audit/PTA-REMEDIATION-MASTER-PLAN.md` — R1–R5 progress log.
- `dossiers/R2/*.json`, `dossiers/R3/SOURCED-NETWORKS.md` — live-sourced real networks + seed coords.
- `dossiers/R4/BATCH5-BIND-MAP.json` — 18 chip→sealed-route_id binds + 6 honest-aspirational.

## Validated COMPLETE (no action)
rio-ccr-barcas · toronto-island-ferry · mersey-ferries · (near-complete: hcmc-saigon-waterbus, brisbane-citycat) · all mature Phase-A networks (istanbul/nyc/venice/lisbon/etc. — sealed = planned, 0 crossings).

## Honest-null / later-horizon carried (renderer-guarded, not blockers)
CalMac Oban↔Craignure (Sound of Mull land-QA) · Manila Intramuros downstream · WSF 4 Puget Sound land-QA · bc-ferries bcf-d04 Georgia Strait · hawaii aspirational inter-island (non-live). All seal when a clean 0-km water polyline is found; else stay honest-null.
