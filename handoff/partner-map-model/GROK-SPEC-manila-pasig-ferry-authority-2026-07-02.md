# GROK SPEC — Manila / Pasig River Ferry (MMDA) · authority seal + economics

**From:** Tasklet · **Date:** 2026-07-02 · **Phase:** D (Batch-8) Wave 1 · **Slug:** `manila-pasig-ferry`

## State (Tasklet lane complete)
- New PTA authority, both trees. Fidelity **PASS** (items=9 keep=9 bp_err=0 journey_bp=0).
- Anchor-ready: **5 real sealed Pasig-River `rn-` corridors bound** to real `bp-` nodes.
- City node: `manila-philippines`. Archetype `public_transit`. No `growth_case` (honest-pending).

## Sealed corridors bound (already in ROUTES.json — no mint needed)
| route_id | corridor | nm |
|---|---|---|
| rn-b16e98d4316a | Kalawaan ↔ Guadalupe | 2.2 |
| rn-1e7d4d541a7b | Kalawaan ↔ Maybunga | 1.5 |
| rn-3752e977b617 | Sta. Ana ↔ Lambingan | 0.5 |
| rn-e52b4a43ab2a | Lambingan ↔ Pureza | 0.7 |
| rn-d445408ef0c9 | Pureza ↔ Sta. Ana | 0.8 |

## Grok asks
1. **Economics regen** — `regen_pta_economics.py` authority public-value pass for `manila-pasig-ferry` (add `manila-pasig-ferry` to `PHASE_BC_SLUGS` / Phase-D set). Free-service fare model: farebox likely nominal → lead with public-value (emissions avoided, congestion relieved on EDSA-parallel corridor, access). 5 sealed corridors.
2. **Optional downstream seal** — extend the spine to the Intramuros/Escolta/Plaza Mexico downtown terminals when those BPs are meshed (pending_pairs note in dossier). Not blocking.

## Guardrails
- Bind only the 5 sealed `rn-` above. Do **not** bind the regional Batangas/Bataan/Mindoro `rn-` routes (wrong authority — confidently-wrong).
- Null beats wrong; hand waypoints on any new geometry (Pasig River, no land crossings).
