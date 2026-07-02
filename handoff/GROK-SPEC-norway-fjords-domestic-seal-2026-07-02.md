# GROK SPEC — Norway Fjord Ferry Network domestic seal + economics (Phase B Batch-6)

**Partner:** `norway-fjords` · **Authority:** Norwegian county ferry procurement (Vestland / Møre og Romsdal / Rogaland fylkeskommune) under the Norwegian Maritime Authority + Parliament's 2026 zero-emission World Heritage fjord mandate
**Dossier:** `handoff/partner-map-model/PTA-DOSSIER-norway-fjords.json`
**Tasklet state:** authority rewrite landed. Hero eyebrow set; phases rebuilt to a mandate-first arc (UNESCO fjords → Sognefjord express/commuter → long coastal fjords); route_ids null + `_link_status: geometry_seal_pending` + `_seed_node`. Commercial `growth_case` removed → `_pta_economics_status: grok_authority_regen_pending`. Banned-term cleanup done. Fidelity PASS; build exit 0.

## 1. Mint seed boarding points
Register the 9 boarding points from `domestic_network.boarding_points` (approx anchor `[lng,lat]`). Node ids canonical:
`flam-terminal`, `gudvangen-terminal`, `geiranger-terminal`, `hellesylt-terminal`, `bergen-strandkai`, `balestrand-terminal`, `kleppesto-askoy`, `stavanger-terminal`, `lysebotn-terminal`. Cities: `flam-norway`, `gudvangen-norway`, `geiranger-norway`, `hellesylt-norway`, `bergen-norway`, `balestrand-norway`, `stavanger-norway`, `lysebotn-norway`.

## 2. Seal the 6 domestic pairs (ID-based, 1:1)
| pair | from → to | approx nm | vessel |
|---|---|---|---|
| nor-d01 | flam-terminal → gudvangen-terminal (Nærøyfjord UNESCO) | 11 | Pioneer II |
| nor-d02 | geiranger-terminal → hellesylt-terminal (Geirangerfjord UNESCO) | 10 | Pioneer II |
| nor-d03 | bergen-strandkai → balestrand-terminal (Sognefjord express) | 55 | Quanta-LR |
| nor-d04 | balestrand-terminal → flam-terminal (inner Sognefjord) | 20 | Quanta-LR |
| nor-d05 | bergen-strandkai → kleppesto-askoy (commuter) | 4 | Pioneer II |
| nor-d06 | stavanger-terminal → lysebotn-terminal (Lysefjord) | 22 | Quanta-LR |

## 3. Hand waypoints — fjord centreline, deep water, NO headland crossings (mandatory)
- **UNESCO fjords (nor-d01, nor-d02):** route charted lanes; Nærøyfjord narrows to ~250m — follow the centreline around the Bakka/Dyrdal bends. Observe protected-zone wake/speed rules (foiling's low-wake is the advantage).
- **Long fjord legs (nor-d03 Sognefjord, nor-d06 Lysefjord):** deep-water centreline; katabatic downslope-wind-aware waypoints.
- **Bergen/Stavanger harbours:** depart via charted terminal channels clear of coastal-express and cargo traffic.
- Winter ice in inner arms + polar-night darkness → all-weather, after-dark routing. See `routing_hazards`.

## 4. No cross-border link
`regional_links` intentionally empty. Domestic fjord network stands alone.

## 5. Economics (Grok lane) — full re-author
**growth_case removed.** Partner is `grok_authority_regen_pending`, no economics panel renders until you re-author. Source finance retained at `finance/recal/growth-norway-fjords.json` (if present). Re-author → `public_value` + authority operating-model (county ferry procurement / fare frame) + headlines, set `_economics_status: pta_regenerated`. Apply the Phase-A convention (no forbidden GMV/TAM keys). Lead the value story on the **binding 2026 zero-emission mandate** — compliance + operating-cost + connectivity.

## 6. Acceptance
- `audit_proposal_fidelity.py --partner norway-fjords` → PASS
- No banned terms (cruise/super-app/resort) in partner-facing copy
- build exit 0
