# GROK SPEC — Gothenburg — Västtrafik Archipelago Ferry Network (mint-heavy authority seal + economics)

**From:** Tasklet · **Date:** 2026-07-02 · **Partner:** `gothenburg-vasttrafik`
**Authority:** Västtrafik — Västra Götaland, Sweden
**Source receipt:** `GEOMETRY-MINT-RECEIPT-gothenburg-sweden.json`
**Dossier:** `handoff/partner-map-model/PTA-DOSSIER-gothenburg-vasttrafik.json`
**Status:** Partner JSON authored + fidelity **PASS**. Domestic-first. Economics honest-pending (Grok lane).

## What Tasklet shipped
- Net-new PTA authority proposal (both trees), authored from the Grok geometry receipt + verified authority facts.
- Real minted BPs bound; real sealed `rn-` route_ids bound where they exist; unsealed pairs = `route_id: null`, `_link_status: "pending-seal"`.
- Decarbonisation anchor: Västtrafik electric-hydrofoil archipelago route trial; Saltholmen southern-archipelago public ferries; Sweden net-zero-2045.
- No commercial `growth_case`; renderer guards on the key (hidden until authority economics regen).

## Boarding points (minted — from receipt)
| bp_id | node | name | lng, lat |
|---|---|---|---|
| `bp-ebb76bc749` | `got-saltholmen` | Saltholmen Ferry Terminal | 11.87, 57.665 |
| `bp-cea1b15c9c` | `got-styrso-bratten` | Styrsö Bratten Pier | 11.81, 57.638 |
| `bp-bec25bb299` | `got-vrango` | Vrångö Pier | 11.76, 57.6 |
| `bp-87e244a203` | `got-fiskebackskil` | Fiskebäckskil Pier | 11.92, 57.68 |

## Sealed corridors bound (real geometry)
| route_id | corridor | distance | state |
|---|---|---|---|
| `rn-f1d39ae68265` | Styrsö Bratten Pier ↔ Vrångö Pier | 3.1 nm | **bound (sealed)** |

## Pending-seal corridors (Grok to mint geometry — hand-waypoints, no land crossings)
| corridor | node pair | state |
|---|---|---|
| Saltholmen Ferry Terminal ↔ Styrsö Bratten Pier | `got-saltholmen` → `got-styrso-bratten` | pending-seal (null route_id) |
| Saltholmen Ferry Terminal ↔ Vrångö Pier | `got-saltholmen` → `got-vrango` | pending-seal (null route_id) |
| Saltholmen Ferry Terminal ↔ Fiskebäckskil Pier | `got-saltholmen` → `got-fiskebackskil` | pending-seal (null route_id) |

## Grok asks
1. **Seal the pending-seal pairs** above with explicit hand-waypoints (no land crossings); land-QA at `interior_land_km ≤ 0.05`. Return `rn-` ids for Tasklet to bind (or keep honest-null if a pair truly cannot be sealed).
2. **Regenerate authority public-value economics** (`_economics_status: pta_regenerated`) using the authority-economics convention — public-value + fare/operating frame; no GMV/TAM/SAM; no Prove/Scale/Mature phase language.
3. Confirm `archetype`/chip renders as a canonical public-transit label.

## Acceptance
- `python3 scripts/audit_proposal_fidelity.py --partner gothenburg-vasttrafik` → **PASS**
- Build clean (auto-discovery; new slug picked up by directory scan).
