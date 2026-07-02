# GROK SPEC — Auckland Transport / Fullers360 domestic seal + economics (Phase B Batch-6)

**Partner:** `fullers360` · **Authority:** Auckland Transport (AT), operator Fullers360
**Dossier:** `handoff/partner-map-model/PTA-DOSSIER-fullers360.json`
**Tasklet state:** authority rewrite landed (hero eyebrow + domestic-first phases + real Waitematā/Hauraki-Gulf corridors, replacing the prior sailing-club/boat-ramp junk corridors). route_ids null, `_link_status: geometry_seal_pending`, `_seed_node: true`. Commercial `growth_case` removed → `_pta_economics_status: grok_authority_regen_pending`. Fidelity PASS; build exit 0.

## 1. Mint seed boarding points
Register the 9 boarding points from `domestic_network.boarding_points` (approximate anchor `[lng,lat]`). Node ids canonical:
`auckland-downtown-ferry`, `devonport-wharf`, `bayswater-wharf`, `hobsonville-point`, `half-moon-bay`, `matiatia-waiheke`, `gulf-harbour`, `rangitoto-wharf`, `tryphena-great-barrier`. City: `auckland-new-zealand`.

## 2. Seal the 8 domestic pairs (ID-based, 1:1)
| pair | from → to | approx nm | vessel |
|---|---|---|---|
| ful-d01 | auckland-downtown-ferry → devonport-wharf | 1.3 | Pioneer II |
| ful-d02 | auckland-downtown-ferry → matiatia-waiheke | 10 | Pioneer II |
| ful-d03 | auckland-downtown-ferry → half-moon-bay | 7 | Pioneer II |
| ful-d04 | auckland-downtown-ferry → hobsonville-point | 8 | Pioneer II |
| ful-d05 | auckland-downtown-ferry → bayswater-wharf | 2 | Pioneer II |
| ful-d06 | auckland-downtown-ferry → gulf-harbour | 15 | Pioneer II |
| ful-d07 | auckland-downtown-ferry → rangitoto-wharf | 4 | Pioneer II |
| ful-d08 | auckland-downtown-ferry → tryphena-great-barrier | 50 | Quanta-LR |

## 3. Hand waypoints — harbour/gulf water only, NO land crossings (mandatory)
- Upper-harbour legs (ful-d04 Hobsonville) transit the charted channel under/around the **Auckland Harbour Bridge**; busy inner-harbour traffic.
- Gulf legs (ful-d02 Waiheke, ful-d06 Gulf Harbour, ful-d07 Rangitoto) route via the **Rangitoto Channel** clear of North Head and reefs — never straight-line across islands.
- **Hauraki Gulf Marine Park:** protected seabird/marine-mammal habitat; low-wake foiling is an advantage but route to charted channels and observe protected zones.
- ful-d08 Great Barrier (Aotea): open outer-gulf exposure; weather-aware waypoints.
- Tidal approaches at Half Moon Bay, Hobsonville, Matiatia — route to charted wharf channels.
See `routing_hazards` in the dossier.

## 4. No regional/cross-border link
`regional_links` intentionally empty (Auckland commuter + Gulf network stands alone). Do not invent a cross-border corridor.

## 5. Economics (Grok lane) — full re-author
**growth_case removed.** Partner is `grok_authority_regen_pending` and renders **no** economics panel until you re-author. Source finance data retained at `finance/recal/growth-fullers360.json`.
Re-author `growth_case` from the dossier + finance source → `public_value` + authority operating-model + headlines, set `_economics_status: pta_regenerated` so `_isPtaEconomics()` renders the PTA branch. Apply the Phase-A presentation convention (no `_render_chip_flag`/`_marine_tam_split_provenance`, revenue as supporting layer, plain-English fare framing — AT/Fullers360 public-transport fares under the AT HOP system). Do not emit forbidden `journey_gmv`/`marine_mobility_tam`.

## 6. Acceptance
- `audit_proposal_fidelity.py --partner fullers360` → PASS
- coverage rollup → fullers360 featured geom sealed
- build exit 0
