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
- This handoff folder: source inventory, anchor-city crosswalk, gap queue, Yassir Algeria market source/mint queue, Algeria country-reference draft, and Algeria route-source hardening batch 1.

## Hard gates
1. **Anchor-city IDs:** use `handoff/.../anchor-city-crosswalk.json`. All listed anchors are currently `OK`; do not rename by filename. Render join key is sealed `city_id`.
2. **Yassir scope:** Morocco + Tunisia only for display/economics in this pass. Algeria is sourced and route-hardened, but held from render/economics because no sealed Atlas Algeria geometry was found.
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

## Algeria mint request — route hardening batch 1
Use `yassir-algeria-market-source-and-mint-queue.json`, `algeria-country-reference-draft.json`, and `yassir-algeria-route-source-hardening-batch-1.json` as inputs for a deterministic Algeria seal pass.

### What to seal if exact
- City IDs to mint/validate:
  - `algiers-algeria`
  - `bejaia-algeria`
  - `oran-algeria`
  - `mostaganem-algeria`
  - `annaba-algeria`
- Boarding points to mint/validate only from named source-backed terminals/ports:
  - Port d'Alger / Gare Maritime d'Alger / La Pêcherie
  - El Djamila / Aïn Bénian
  - Tamentfoust / El Marsa
  - Les Sablettes / Hussein Dey waterfront
  - Port de Béjaïa passenger terminal
  - Port d'Oran passenger/marina area
  - Mostaganem port / passenger area
  - Port d'Annaba passenger terminal, only if official/port source is strong enough

### Candidate routes
- A: Algiers Bay — La Pêcherie / Port d’Alger ↔ El Djamila / Aïn Bénian.
- A-: Algiers Bay — La Pêcherie ↔ Tamentfoust / Les Sablettes axis.
- A-: Port de Béjaïa ↔ Port d’Alger HSC line; range-gate before any commercial-now label.
- B+: Oran ↔ Mostaganem seasonal ENTMV line; validate recurrence/current service before economics.
- B: Annaba port existence lead only; do not model as a route yet.

### Algeria hard gates
- Null beats wrong: return `null` for any endpoint or route that cannot be deterministically sealed.
- Do not bind Algeria to Morocco/Tunisia IDs or broad country centroids.
- Do not add `yassir-algeria` to display/economics until Algeria city IDs, boarding points, route IDs, country-reference row, and route-level demand/fare anchors are all ready.
- Do not use Europe-facing ferry fares as Navier commuter fares without local route validation.
- If exact seal succeeds, return a QA ledger with: city IDs minted, BPs sealed/dropped with reasons, route IDs created/held, land-crossing proof, and whether each route is N30/N35 commercial-now, seasonal, or roadmap-only.

