# GROK SPEC — BC Ferries domestic seal + economics regen (Phase B Batch-6)

**Partner:** `bc-ferries` · **Authority:** British Columbia Ferry Services Inc. (BC Ferries)
**Dossier:** `handoff/partner-map-model/PTA-DOSSIER-bc-ferries.json`
**Tasklet state:** authority-proposal rewrite landed (hero eyebrow + domestic-first phases + real corridors). All route_ids null, `_link_status: geometry_seal_pending`, `_seed_node: true`. Fidelity audit PASS; build exit 0.

## 1. Mint seed boarding points
Register the 12 boarding points from `domestic_network.boarding_points` (approximate anchor `[lng,lat]`) as `priority_city`/BP features in the matching clusters. Node ids are canonical — bind partner cards by these ids:
`van-harbour-flight-centre`, `victoria-inner-harbour`, `nanaimo-harbour`, `tsawwassen`, `swartz-bay`, `horseshoe-bay`, `departure-bay-nanaimo`, `langdale`, `fulford-harbour`, `ganges-harbour`, `long-harbour`, `village-bay-mayne`.
Cities: `vancouver-canada`, `victoria-canada`, `nanaimo-canada`, `sunshine-coast-canada`, `gulf-islands-canada`. Mint any missing city node.

## 2. Seal the 8 domestic pairs (ID-based)
From `domestic_network.domestic_pairs` — seal each `from`→`to` and write `route_id` back to the matching partner card (both trees). **Inherit 1:1; do not curate a subset.**

| pair | from → to | approx nm | vessel |
|---|---|---|---|
| bcf-d01 | van-harbour-flight-centre → victoria-inner-harbour | 53 | Quanta-LR |
| bcf-d02 | van-harbour-flight-centre → nanaimo-harbour | 30 | Quanta-LR |
| bcf-d03 | tsawwassen → swartz-bay | 24 | Quanta-LR |
| bcf-d04 | horseshoe-bay → departure-bay-nanaimo | 17 | Quanta-LR |
| bcf-d05 | horseshoe-bay → langdale | 7 | Pioneer II |
| bcf-d06 | swartz-bay → fulford-harbour | 7 | Pioneer II |
| bcf-d07 | fulford-harbour → ganges-harbour | 5 | Pioneer II |
| bcf-d08 | long-harbour → village-bay-mayne | 5 | Pioneer II |

## 3. Hand waypoints — NO land crossings (mandatory)
Route every leg through navigable open water only. Explicit pinch-point waypoints:
- **Vancouver Harbour departures (d01, d02):** exit through **First Narrows** (under Lions Gate) into English Bay before crossing the Strait of Georgia. Never straight-line across Stanley Park / the North Shore.
- **d01 Van→Victoria:** cross the Strait of Georgia mid-channel, transit **Haro Strait** (or Active Pass with traffic-aware waypoints) into Juan de Fuca, approach Victoria Inner Harbour from the south. No crossing of Saanich Peninsula land.
- **d06 Swartz Bay→Fulford:** follow **Satellite Channel**; do not cross the Saanich land.
- **d07, d08 (Gulf Islands):** stay in charted channels; route **clear of Active Pass** ferry traffic; never cut across Galiano/Mayne/Salt Spring land.
- **d03, d04:** cross mid-Strait clear of the **Roberts Bank / Tsawwassen traffic-separation scheme**.
See `routing_hazards` in the dossier for the full list.

## 4. Regional link — DO NOT seal for phase 1
`bcf-r01` (Victoria ↔ Seattle) is `roadmap_excluded` / `economics_status: roadmap_excluded`. International, out of phase-1 scope. Leave unsealed.

## 5. Economics regen (Grok lane)
**NOTE — growth_case removed.** The prior commercial `growth_case` (SOM/SAM/TAM/GMV ladder) has been **removed** from both partner trees; the partner is now `_pta_economics_status: grok_authority_regen_pending` and renders **no** economics panel until you re-author. Source finance data remains in-repo at `finance/recal/growth-bc-ferries.json`.
Re-author `growth_case` for `bc-ferries` from the dossier + finance source → `public_value` + authority operating-model + headlines, and set `_economics_status: pta_regenerated` so `_isPtaEconomics()` renders the PTA branch. **Apply the Phase-A presentation convention** (no `_render_chip_flag`/`_marine_tam_split_provenance`, revenue as supporting layer, authority-specific fare framing — BC Ferries fares under the Coastal Ferry Act). Do not emit forbidden `journey_gmv`/`marine_mobility_tam`.

## 6. Acceptance
- `audit_proposal_fidelity.py --partner bc-ferries` → PASS
- `audit_partner_coverage_rollup.py` → bc-ferries featured geom sealed
- build exit 0
