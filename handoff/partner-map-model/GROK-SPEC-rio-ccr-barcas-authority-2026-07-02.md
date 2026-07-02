# GROK SPEC — Rio de Janeiro / CCR Barcas · authority mint-seal + economics

**From:** Tasklet · **Date:** 2026-07-02 · **Phase:** D (Batch-8) Wave 1 · **Slug:** `rio-ccr-barcas`

## State (Tasklet lane complete)
- New PTA authority, both trees. Fidelity **PASS** (items=8 keep=8 bp_err=0 journey_bp=0).
- City node `rio-de-janeiro-brazil` + **5 real CCR Barcas `bp-` terminals** anchored (Praça XV hub + 4 spokes). Corridors **pending-seal** (route_id null).
- Archetype `public_transit`. No `growth_case` (honest-pending). Renderer guards on null → builds clean.

## Boarding points (real, anchored)
| node | bp_id | terminal | lng,lat |
|---|---|---|---|
| rio-praca-xv | bp-660ea6736a | Praça XV (central Rio hub) | -43.17208, -22.90288 |
| rio-arariboia | bp-45ba34fda2 | Arariboia (Niterói) | -43.12426, -22.893722 |
| rio-charitas | bp-85947006eb | Charitas (Niterói fast cat) | -43.099279, -22.932383 |
| rio-paqueta | bp-e2aae460aa | Paquetá island | -43.107014, -22.7621 |
| rio-cocota | bp-53684b584c | Cocotá (Ilha do Governador) | -43.17849, -22.80411 |

## Corridors to MINT (Guanabara Bay open water, hand waypoints, NO land crossings)
| pair | approx nm |
|---|---|
| Praça XV ↔ Niterói (Arariboia) | 2.7 |
| Praça XV ↔ Charitas | 3.4 |
| Praça XV ↔ Paquetá | 8.3 |
| Praça XV ↔ Cocotá | 6.0 |

## Grok asks
1. **Mint** the 4 hub-and-spoke corridors from Praça XV across Guanabara Bay (open water; keep clear of Ilha das Cobras / Ilha do Governador shorelines with explicit waypoints). Bind `rn-` route_ids back into `journeys_unlocked` + `phases[].featured_routes` (`_link_status: sealed`).
2. **Economics regen** — authority public-value pass (add slug to Phase-D set).

## Guardrails
- Praça XV is the single hub; all 4 corridors radiate from it (matches real CCR Barcas network). No spoke-to-spoke corridors.
- Exclude yacht-club POIs (Paqueta Yacht Club, Clube Naval Charitas). Null beats wrong.
