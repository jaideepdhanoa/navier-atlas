# GROK SPEC — Hawaiʻi DOT Harbors inter-island seal + economics regen (Phase B Batch-6)

**Partner:** `hawaii` · **Authority:** State of Hawaiʻi DOT Harbors Division (Pulama Lānaʻi launch anchor)
**Dossier:** `handoff/partner-map-model/PTA-DOSSIER-hawaii.json`
**Tasklet state:** authority rewrite landed (hero eyebrow + domestic-first phases + real inter-island corridors; forbidden `tam_framing` key removed). route_ids null, `_link_status: geometry_seal_pending`, `_seed_node: true`. Fidelity audit PASS; build exit 0.

## 1. Mint seed boarding points
Register the 7 boarding points from `domestic_network.boarding_points` (approximate anchor `[lng,lat]`). Node ids canonical:
`manele-lanai`, `lahaina-maui`, `maalaea-maui`, `honolulu-harbour`, `kaunakakai-molokai`, `kawaihae-hawaii-island`, `nawiliwili-kauai`.
Cities: `maui-county-hawaii-usa`, `oahu-honolulu-hawaii-usa`, `kona-hilo-hawaii-island-usa`, `kauai-hawaii-usa`.

## 2. Seal the 7 inter-island pairs (ID-based, 1:1)
| pair | from → to | approx nm | channel | vessel |
|---|---|---|---|---|
| haw-d01 | lahaina-maui → manele-lanai | 9 | ʻAuʻau (sheltered, LIVE ferry) | Pioneer II |
| haw-d02 | maalaea-maui → manele-lanai | 13 | ʻAuʻau | Pioneer II |
| haw-d03 | honolulu-harbour → kaunakakai-molokai | 40 | Kaʻiwi | Quanta-LR |
| haw-d04 | honolulu-harbour → lahaina-maui | 72 | Kaʻiwi/Pailolo | Quanta-LR |
| haw-d05 | lahaina-maui → kaunakakai-molokai | 15 | Pailolo | Pioneer II |
| haw-d06 | maalaea-maui → kawaihae-hawaii-island | 30 | ʻAlenuihāhā (roughest) | Quanta-LR |
| haw-d07 | honolulu-harbour → nawiliwili-kauai | 72 | Kaʻieʻie/Kauaʻi | Quanta-LR |

## 3. Hand waypoints — open-ocean channels, NO land crossings (mandatory)
- Every leg is an island-to-island channel crossing: route mid-channel to charted harbor entrances; never straight-line across island land or reefs.
- **Humpback sanctuary (defining constraint):** the ʻAuʻau / Pailolo / Maui-County waters are protected humpback habitat (peak ~Nov–May). Document whale-safe, low-wake routing on haw-d01/d02/d05; this is the exact concern that ended the Superferry.
- **haw-d06 ʻAlenuihāhā:** weather-aware waypoints; extreme wind acceleration off Haleakalā/Mauna Kea.
- **haw-d03/d07:** mid-channel routing clear of Oʻahu headlands.
- **Honolulu Harbor:** follow charted commercial entrance channel.
See `routing_hazards` in the dossier.

## 4. No regional/cross-border link
Hawaiʻi is isolated; `regional_links` is intentionally empty. Do not invent an external corridor.

## 5. Economics regen (Grok lane)
**NOTE — growth_case removed.** The prior commercial `growth_case` (SOM/SAM/TAM/GMV ladder) has been **removed** from both partner trees; the partner is now `_pta_economics_status: grok_authority_regen_pending` and renders **no** economics panel until you re-author. Source finance data remains in-repo at `finance/recal/growth-hawaii.json`.
Re-author `growth_case` for `hawaii` from the dossier + finance source → `public_value` + authority operating-model + headlines, and set `_economics_status: pta_regenerated` so `_isPtaEconomics()` renders the PTA branch. Apply the Phase-A presentation convention (no forbidden GMV/TAM keys, revenue as supporting layer). Note the partner still carries a good `end_state`/`objections`/`proof_points` narrative — do not clobber those.

## 6. Acceptance
- `audit_proposal_fidelity.py --partner hawaii` → PASS
- coverage rollup → hawaii featured geom sealed
- build exit 0
