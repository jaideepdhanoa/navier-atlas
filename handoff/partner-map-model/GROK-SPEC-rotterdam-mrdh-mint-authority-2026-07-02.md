# GROK SPEC — Rotterdam — Waterbus Network (MRDH) (mint-heavy authority seal + economics)

**From:** Tasklet · **Date:** 2026-07-02 · **Partner:** `rotterdam-mrdh`
**Authority:** MRDH — Rotterdam-The Hague Metropolitan Area, Netherlands
**Source receipt:** `GEOMETRY-MINT-RECEIPT-rotterdam-netherlands.json`
**Dossier:** `handoff/partner-map-model/PTA-DOSSIER-rotterdam-mrdh.json`
**Status:** Partner JSON authored + fidelity **PASS**. Domestic-first. Economics honest-pending (Grok lane).

## What Tasklet shipped
- Net-new PTA authority proposal (both trees), authored from the Grok geometry receipt + verified authority facts.
- Real minted BPs bound; real sealed `rn-` route_ids bound where they exist; unsealed pairs = `route_id: null`, `_link_status: "pending-seal"`.
- Decarbonisation anchor: MRDH Waterbus — largest public-transport ferry in NL; new electric Waterbus vessels; Netherlands 2050 climate-neutrality.
- No commercial `growth_case`; renderer guards on the key (hidden until authority economics regen).

## Boarding points (minted — from receipt)
| bp_id | node | name | lng, lat |
|---|---|---|---|
| `bp-dff1961510` | `rtd-erasmusbrug` | Erasmusbrug (Willemsplein) Waterbus | 4.482, 51.916 |
| `bp-c0e473fc31` | `rtd-dordrecht` | Dordrecht Merwekade Waterbus | 4.668, 51.808 |
| `bp-2d74e3e111` | `rtd-kinderdijk` | Kinderdijk Waterbus Stop | 4.635, 51.883 |
| `bp-27d899645a` | `rtd-hoek-van-holland` | Hoek van Holland Haven | 4.133, 51.977 |

## Sealed corridors bound (real geometry)
| route_id | corridor | distance | state |
|---|---|---|---|
| — | — | — | none sealed at mint time |

## Pending-seal corridors (Grok to mint geometry — hand-waypoints, no land crossings)
| corridor | node pair | state |
|---|---|---|
| Erasmusbrug (Willemsplein) Waterbus ↔ Dordrecht Merwekade Waterbus | `rtd-erasmusbrug` → `rtd-dordrecht` | pending-seal (null route_id) |
| Erasmusbrug (Willemsplein) Waterbus ↔ Kinderdijk Waterbus Stop | `rtd-erasmusbrug` → `rtd-kinderdijk` | pending-seal (null route_id) |
| Dordrecht Merwekade Waterbus ↔ Kinderdijk Waterbus Stop | `rtd-dordrecht` → `rtd-kinderdijk` | pending-seal (null route_id) |
| Erasmusbrug (Willemsplein) Waterbus ↔ Hoek van Holland Haven | `rtd-erasmusbrug` → `rtd-hoek-van-holland` | pending-seal (null route_id) |

## Grok asks
1. **Seal the pending-seal pairs** above with explicit hand-waypoints (no land crossings); land-QA at `interior_land_km ≤ 0.05`. Return `rn-` ids for Tasklet to bind (or keep honest-null if a pair truly cannot be sealed).
2. **Regenerate authority public-value economics** (`_economics_status: pta_regenerated`) using the authority-economics convention — public-value + fare/operating frame; no GMV/TAM/SAM; no Prove/Scale/Mature phase language.
3. Confirm `archetype`/chip renders as a canonical public-transit label.

## Acceptance
- `python3 scripts/audit_proposal_fidelity.py --partner rotterdam-mrdh` → **PASS**
- Build clean (auto-discovery; new slug picked up by directory scan).
