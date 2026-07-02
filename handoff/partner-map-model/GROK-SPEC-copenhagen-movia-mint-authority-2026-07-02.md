# GROK SPEC — Copenhagen — Movia Harbour Bus Network (mint-heavy authority seal + economics)

**From:** Tasklet · **Date:** 2026-07-02 · **Partner:** `copenhagen-movia`
**Authority:** Movia — Greater Copenhagen, Denmark
**Source receipt:** `GEOMETRY-MINT-RECEIPT-copenhagen-denmark.json`
**Dossier:** `handoff/partner-map-model/PTA-DOSSIER-copenhagen-movia.json`
**Status:** Partner JSON authored + fidelity **PASS**. Domestic-first. Economics honest-pending (Grok lane).

## What Tasklet shipped
- Net-new PTA authority proposal (both trees), authored from the Grok geometry receipt + verified authority facts.
- Real minted BPs bound; real sealed `rn-` route_ids bound where they exist; unsealed pairs = `route_id: null`, `_link_status: "pending-seal"`.
- Decarbonisation anchor: Movia's fully-electric harbour buses since 2020; Copenhagen carbon-neutrality programme.
- No commercial `growth_case`; renderer guards on the key (hidden until authority economics regen).

## Boarding points (minted — from receipt)
| bp_id | node | name | lng, lat |
|---|---|---|---|
| `bp-f5bc7b664c` | `cph-nyhavn` | Nyhavn Harbour Bus Stop | 12.59, 55.68 |
| `bp-2893b3d34e` | `cph-refshaleoen` | Refshaleøen Ferry Stop | 12.61, 55.693 |
| `bp-9e814c8d64` | `cph-opera` | Opera House Ferry Stop | 12.602, 55.682 |
| `bp-1579f3be90` | `cph-nordre-toldbod` | Nordre Toldbod Ferry Stop | 12.595, 55.685 |

## Sealed corridors bound (real geometry)
| route_id | corridor | distance | state |
|---|---|---|---|
| `rn-f7d4a824ec58` | Nyhavn Harbour Bus Stop ↔ Opera House Ferry Stop | 0.4 nm | **bound (sealed)** |

## Pending-seal corridors (Grok to mint geometry — hand-waypoints, no land crossings)
| corridor | node pair | state |
|---|---|---|
| Nyhavn Harbour Bus Stop ↔ Refshaleøen Ferry Stop | `cph-nyhavn` → `cph-refshaleoen` | pending-seal (null route_id) |
| Opera House Ferry Stop ↔ Nordre Toldbod Ferry Stop | `cph-opera` → `cph-nordre-toldbod` | pending-seal (null route_id) |
| Nordre Toldbod Ferry Stop ↔ Refshaleøen Ferry Stop | `cph-nordre-toldbod` → `cph-refshaleoen` | pending-seal (null route_id) |

## Grok asks
1. **Seal the pending-seal pairs** above with explicit hand-waypoints (no land crossings); land-QA at `interior_land_km ≤ 0.05`. Return `rn-` ids for Tasklet to bind (or keep honest-null if a pair truly cannot be sealed).
2. **Regenerate authority public-value economics** (`_economics_status: pta_regenerated`) using the authority-economics convention — public-value + fare/operating frame; no GMV/TAM/SAM; no Prove/Scale/Mature phase language.
3. Confirm `archetype`/chip renders as a canonical public-transit label.

## Acceptance
- `python3 scripts/audit_proposal_fidelity.py --partner copenhagen-movia` → **PASS**
- Build clean (auto-discovery; new slug picked up by directory scan).
