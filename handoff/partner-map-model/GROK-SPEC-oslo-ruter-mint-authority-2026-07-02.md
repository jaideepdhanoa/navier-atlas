# GROK SPEC — Oslo — Ruter Fjord Ferry Network (mint-heavy authority seal + economics)

**From:** Tasklet · **Date:** 2026-07-02 · **Partner:** `oslo-ruter`
**Authority:** Ruter — Oslo & Akershus, Norway
**Source receipt:** `GEOMETRY-MINT-RECEIPT-oslo-norway.json`
**Dossier:** `handoff/partner-map-model/PTA-DOSSIER-oslo-ruter.json`
**Status:** Partner JSON authored + fidelity **PASS**. Domestic-first. Economics honest-pending (Grok lane).

## What Tasklet shipped
- Net-new PTA authority proposal (both trees), authored from the Grok geometry receipt + verified authority facts.
- Real minted BPs bound; real sealed `rn-` route_ids bound where they exist; unsealed pairs = `route_id: null`, `_link_status: "pending-seal"`.
- Decarbonisation anchor: Ruter–Norled Oslofjord express-boat electrification (2022); Aker Brygge–Nesoddtangen largest car-free ferry route; Oslo 95%-by-2030 climate target.
- No commercial `growth_case`; renderer guards on the key (hidden until authority economics regen).

## Boarding points (minted — from receipt)
| bp_id | node | name | lng, lat |
|---|---|---|---|
| `bp-e6f7d9a75f` | `oslo-aker-brygge` | Aker Brygge Ferry Terminal | 10.732, 59.908 |
| `bp-a8f4c4e571` | `oslo-nesoddtangen` | Nesoddtangen Ferry Terminal | 10.665, 59.862 |
| `bp-10d41adebe` | `oslo-hovedoya` | Hovedøya Island Pier | 10.768, 59.894 |
| `bp-190516cc2c` | `oslo-bygdoy` | Bygdøy Ferry Pier | 10.688, 59.901 |

## Sealed corridors bound (real geometry)
| route_id | corridor | distance | state |
|---|---|---|---|
| — | — | — | none sealed at mint time |

## Pending-seal corridors (Grok to mint geometry — hand-waypoints, no land crossings)
| corridor | node pair | state |
|---|---|---|
| Aker Brygge Ferry Terminal ↔ Nesoddtangen Ferry Terminal | `oslo-aker-brygge` → `oslo-nesoddtangen` | pending-seal (null route_id) |
| Aker Brygge Ferry Terminal ↔ Hovedøya Island Pier | `oslo-aker-brygge` → `oslo-hovedoya` | pending-seal (null route_id) |
| Aker Brygge Ferry Terminal ↔ Bygdøy Ferry Pier | `oslo-aker-brygge` → `oslo-bygdoy` | pending-seal (null route_id) |
| Hovedøya Island Pier ↔ Bygdøy Ferry Pier | `oslo-hovedoya` → `oslo-bygdoy` | pending-seal (null route_id) |

## Grok asks
1. **Seal the pending-seal pairs** above with explicit hand-waypoints (no land crossings); land-QA at `interior_land_km ≤ 0.05`. Return `rn-` ids for Tasklet to bind (or keep honest-null if a pair truly cannot be sealed).
2. **Regenerate authority public-value economics** (`_economics_status: pta_regenerated`) using the authority-economics convention — public-value + fare/operating frame; no GMV/TAM/SAM; no Prove/Scale/Mature phase language.
3. Confirm `archetype`/chip renders as a canonical public-transit label.

## Acceptance
- `python3 scripts/audit_proposal_fidelity.py --partner oslo-ruter` → **PASS**
- Build clean (auto-discovery; new slug picked up by directory scan).
