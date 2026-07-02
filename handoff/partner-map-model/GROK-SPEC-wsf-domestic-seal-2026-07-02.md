# GROK SPEC — Washington State Ferries (WSF) — pending-corridor seal

**From:** Tasklet · **Date:** 2026-07-02 · **Partner:** `wsf`
**Authority:** Washington State Ferries (WSDOT) — Puget Sound & the San Juan Islands
**Dossier:** `handoff/partner-map-model/PTA-DOSSIER-wsf.json`
**Status:** Authority narrative + economics already live (Grok-regenerated, fidelity **PASS**). This spec covers only the residual honest-null corridors + closes the Batch-6 dossier gap.

## What Tasklet shipped in this PR
- Authored `PTA-DOSSIER-wsf.json` (Batch-6 provenance parity: terminals, sealed/pending corridors, hazards).
- Reworded `close.body` to remove the residual `start → scale → mature` phase-ladder prose (PTA gold: no Prove/Scale/Mature). Domestic-first arc preserved.
- No economics change (Grok's authority regen untouched).

## Sealed corridors already bound (real geometry)
| corridor | route_id |
|---|---|
| Seattle (Colman Dock) ↔ Bremerton | `rn-01adad364cdf` |
| Mukilteo ↔ Clinton | `rn-0574f069dd70` |
| Port Townsend ↔ Coupeville | `rn-db80b9ca9f0e` |
| Anacortes ↔ Friday Harbor | `rn-e7e480584051` |

## Pending-seal corridors (Grok to mint — hand-waypoints, no land crossings, respect currents/TSS)
| corridor | state |
|---|---|
| Seattle (Colman Dock) ↔ Bainbridge Island | pending-seal (null route_id) |
| Edmonds ↔ Kingston | pending-seal (null route_id) |
| Fauntleroy ↔ Vashon Island | pending-seal (null route_id) |
| Vashon Island ↔ Southworth | pending-seal (null route_id) |

## Grok asks
1. Seal the four pending WSF corridors with explicit hand-waypoints (Puget Sound currents, traffic-separation schemes, clear of Bremerton naval restricted zones); land-QA at `interior_land_km ≤ 0.05`. Return `rn-` ids or keep honest-null.
2. No economics regen needed — authority economics already regenerated this lane.

## Acceptance
- `python3 scripts/audit_proposal_fidelity.py --partner wsf` → **PASS**
- Build clean.
