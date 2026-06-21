# Grok handoff — Caribbean Mobility + Yassir gold-standard proposal package

## Mandate
Bring `yassir` and `caribbean-mobility` to the same render/QA discipline as Grab/Careem without shortcuts.

## Inputs
- `partner-pitch/partners/yassir.json`
- `partner-pitch/partners/caribbean-mobility.json`
- `finance/model/corridors.json` additions: `yassir-tunisia`, `yassir-morocco`
- `finance/recal/agg-yassir.json`
- `finance/growth-yassir.json`
- `partner-pitch/partners/_growth-draft/yassir.growth.json`
- `finance/_sheet_out/yassir_unit_econ.xlsx`
- This handoff folder: source inventory, anchor-city crosswalk, and gap queue.

## Hard gates
1. **Anchor-city IDs:** use `handoff/.../anchor-city-crosswalk.json`. All listed anchors are currently `OK`; do not rename by filename. Render join key is sealed `city_id`.
2. **Yassir scope:** Morocco + Tunisia only for display/economics in this pass. Algeria is sourced but held because no Atlas geometry was found.
3. **Caribbean scope:** use existing Atlas Caribbean IDs only. Do not invent country/city support for a specific app partner; this is partner-generic until an operator is named.
4. **Economics:** Yassir economics may render from generated files. Caribbean economics must stay pending until country-reference rows and route-specific demand anchors are added.
5. **Range gate:** N30/N35 only for <=70nm. 75–150nm is Quanta-LR roadmap. >150nm is review. Do not fake long legs.
6. **Route IDs:** all authored `route_id: null` values are intentional. Bind only by deterministic seal from node IDs / routes.
7. **No Atlas images in decks:** use deterministic N30/N35 compositing and market-specific backgrounds only.

## Acceptance
- Both partner pages validate and render.
- Yassir Morocco/Tunisia map has no dark market caused by anchor ID mismatch.
- Yassir TAM ladder points to the live economics sheet once uploaded/replaced.
- Caribbean page renders as a partner-generic regional proposal with explicit economics-gap badges, not invented numbers.
- QA report lists every unresolved registry/economics gap with next action.
