# GROK SPEC — Amsterdam — GVB IJ Ferry Network (mint-heavy authority seal + economics)

**From:** Tasklet · **Date:** 2026-07-02 · **Partner:** `amsterdam-gvb`
**Authority:** GVB — Amsterdam, Netherlands
**Source receipt:** `GEOMETRY-MINT-RECEIPT-amsterdam-netherlands.json`
**Dossier:** `handoff/partner-map-model/PTA-DOSSIER-amsterdam-gvb.json`
**Status:** Partner JSON authored + fidelity **PASS**. Domestic-first. Economics honest-pending (Grok lane).

## What Tasklet shipped
- Net-new PTA authority proposal (both trees), authored from the Grok geometry receipt + verified authority facts.
- Real minted BPs bound; real sealed `rn-` route_ids bound where they exist; unsealed pairs = `route_id: null`, `_link_status: "pending-seal"`.
- Decarbonisation anchor: Amsterdam municipal commitment to emission-free city ferries + new electric IJ vessels; free GVB F1–F7 public crossings; climate-neutrality target.
- No commercial `growth_case`; renderer guards on the key (hidden until authority economics regen).

## Boarding points (minted — from receipt)
| bp_id | node | name | lng, lat |
|---|---|---|---|
| `bp-3b092232a2` | `ams-centraal-ij` | Centraal Station IJ Pontoon | 4.897, 52.383 |
| `bp-ce88410c66` | `ams-buiksloterweg` | Buiksloterweg Ferry Pontoon | 4.92, 52.4 |
| `bp-50b8a2994b` | `ams-ijplein` | IJplein Ferry Pontoon | 4.91, 52.388 |
| `bp-5817037b2f` | `ams-ndsm` | NDSM Ferry Pontoon | 4.892, 52.405 |

## Sealed corridors bound (real geometry)
| route_id | corridor | distance | state |
|---|---|---|---|
| — | — | — | none sealed at mint time |

## Pending-seal corridors (Grok to mint geometry — hand-waypoints, no land crossings)
| corridor | node pair | state |
|---|---|---|
| Centraal Station IJ Pontoon ↔ Buiksloterweg Ferry Pontoon | `ams-centraal-ij` → `ams-buiksloterweg` | pending-seal (null route_id) |
| Centraal Station IJ Pontoon ↔ IJplein Ferry Pontoon | `ams-centraal-ij` → `ams-ijplein` | pending-seal (null route_id) |
| Centraal Station IJ Pontoon ↔ NDSM Ferry Pontoon | `ams-centraal-ij` → `ams-ndsm` | pending-seal (null route_id) |
| Buiksloterweg Ferry Pontoon ↔ NDSM Ferry Pontoon | `ams-buiksloterweg` → `ams-ndsm` | pending-seal (null route_id) |

## Grok asks
1. **Seal the pending-seal pairs** above with explicit hand-waypoints (no land crossings); land-QA at `interior_land_km ≤ 0.05`. Return `rn-` ids for Tasklet to bind (or keep honest-null if a pair truly cannot be sealed).
2. **Regenerate authority public-value economics** (`_economics_status: pta_regenerated`) using the authority-economics convention — public-value + fare/operating frame; no GMV/TAM/SAM; no Prove/Scale/Mature phase language.
3. Confirm `archetype`/chip renders as a canonical public-transit label.

## Acceptance
- `python3 scripts/audit_proposal_fidelity.py --partner amsterdam-gvb` → **PASS**
- Build clean (auto-discovery; new slug picked up by directory scan).
