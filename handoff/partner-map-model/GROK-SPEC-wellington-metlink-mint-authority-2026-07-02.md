# GROK SPEC — Wellington — Metlink Harbour Ferry (mint-heavy authority seal + economics)

**From:** Tasklet · **Date:** 2026-07-02 · **Partner:** `wellington-metlink`
**Authority:** Metlink — Greater Wellington, New Zealand
**Source receipt:** `GEOMETRY-MINT-RECEIPT-wellington-new-zealand.json`
**Dossier:** `handoff/partner-map-model/PTA-DOSSIER-wellington-metlink.json`
**Status:** Partner JSON authored + fidelity **PASS**. Domestic-first. Economics honest-pending (Grok lane).

## What Tasklet shipped
- Net-new PTA authority proposal (both trees), authored from the Grok geometry receipt + verified authority facts.
- Real minted BPs bound; real sealed `rn-` route_ids bound where they exist; unsealed pairs = `route_id: null`, `_link_status: "pending-seal"`.
- Decarbonisation anchor: Metlink's Ika Rere — Southern Hemisphere's first fully electric passenger ferry; NZ Zero Carbon Act net-zero-2050.
- No commercial `growth_case`; renderer guards on the key (hidden until authority economics regen).

## Boarding points (minted — from receipt)
| bp_id | node | name | lng, lat |
|---|---|---|---|
| `bp-ad70a1bc3a` | `wlg-queens-wharf` | Queens Wharf Ferry Terminal | 174.778, -41.286 |
| `bp-b9cecc2b08` | `wlg-days-bay` | Days Bay Wharf | 174.917, -41.212 |
| `bp-2e89c287bb` | `wlg-seatoun` | Seatoun Wharf | 174.833, -41.32 |
| `bp-057aba0eac` | `wlg-somes-island` | Somes Island (Matiu) Pier | 174.857, -41.257 |

## Sealed corridors bound (real geometry)
| route_id | corridor | distance | state |
|---|---|---|---|
| `rn-a3c31405844f` | Seatoun Wharf ↔ Somes Island (Matiu) Pier | 3.9 nm | **bound (sealed)** |

## Pending-seal corridors (Grok to mint geometry — hand-waypoints, no land crossings)
| corridor | node pair | state |
|---|---|---|
| Queens Wharf Ferry Terminal ↔ Days Bay Wharf | `wlg-queens-wharf` → `wlg-days-bay` | pending-seal (null route_id) |
| Queens Wharf Ferry Terminal ↔ Seatoun Wharf | `wlg-queens-wharf` → `wlg-seatoun` | pending-seal (null route_id) |
| Queens Wharf Ferry Terminal ↔ Somes Island (Matiu) Pier | `wlg-queens-wharf` → `wlg-somes-island` | pending-seal (null route_id) |

## Grok asks
1. **Seal the pending-seal pairs** above with explicit hand-waypoints (no land crossings); land-QA at `interior_land_km ≤ 0.05`. Return `rn-` ids for Tasklet to bind (or keep honest-null if a pair truly cannot be sealed).
2. **Regenerate authority public-value economics** (`_economics_status: pta_regenerated`) using the authority-economics convention — public-value + fare/operating frame; no GMV/TAM/SAM; no Prove/Scale/Mature phase language.
3. Confirm `archetype`/chip renders as a canonical public-transit label.

## Acceptance
- `python3 scripts/audit_proposal_fidelity.py --partner wellington-metlink` → **PASS**
- Build clean (auto-discovery; new slug picked up by directory scan).
