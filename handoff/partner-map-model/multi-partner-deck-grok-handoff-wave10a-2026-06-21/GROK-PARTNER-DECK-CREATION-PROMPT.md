# Grok Partner Deck Creation Prompt — Wave 10A

You are preparing live Google Slides partner decks from Tasklet-generated Deck Studio artifacts.

## Non-negotiables

- Use Slides API only. No PPTX round-trip, no full replacement.
- For each partner: bind or create the live deck ID, then pull full slide/object inventory before edits.
- Use only source-backed partner JSON/economics/handoff claims.
- Unknown route IDs, city IDs, boarding points, sheet IDs, and image sources stay pending/null.
- Preserve source phase topology; do not restructure `phases[]` or hub `markets[]`.
- Do not overwrite `model_link`, `route_id`, or `route_ids` in source data.
- N30/N35 composites only, with market-specific approved backgrounds; no Atlas-generated images.
- Return QA receipt with deck ID, slide count, source-map coverage, image provenance ledger, render receipts, unresolved gaps, and no-op replay result.

## Partner order and special holds

### `qatar`
- Read `deck-studio/decks/qatar/deck.config.json`, `slide-manifest.json`, `content-source.json`, and `image-manifest.json`.
- Guardrail: Authority/tourism deck. Commercial-now content should stay on Doha Bay / Doha domestic route economics already cascaded; Gulf capital corridors are roadmap-only where economics_status=roadmap_excluded and must stay visually separated.

### `bahrain-motc`
- Read `deck-studio/decks/bahrain-motc/deck.config.json`, `slide-manifest.json`, `content-source.json`, and `image-manifest.json`.
- Guardrail: Authority proposal, not a mobility-platform proposal. Bahrain domestic + Manama↔KSA Eastern Province are the only commercial-now candidates; Doha/Dubai/Abu Dhabi/Muscat/Ras Al Khaimah legs are roadmap-only unless separately resealed and range-gated.

### `rakta`
- Read `deck-studio/decks/rakta/deck.config.json`, `slide-manifest.json`, `content-source.json`, and `image-manifest.json`.
- Guardrail: Authority proposal, not a mobility-platform proposal. RAK domestic resort/city access and RAK↔Dubai/northern-emirates are proposal candidates. Musandam/Khasab remains exact-bind-required; Gulf capital links remain roadmap-only.

### `hong-kong`
- Read `deck-studio/decks/hong-kong/deck.config.json`, `slide-manifest.json`, `content-source.json`, and `image-manifest.json`.
- Guardrail: Authority/destination-region proposal. Many ferry/PRD routes remain unlinked in source; deck must show exact-bound Victoria Harbour first and treat Macau/PRD crossings as Grok holds until IDs exist.

### `gojek`
- Read `deck-studio/decks/gojek/deck.config.json`, `slide-manifest.json`, `content-source.json`, and `image-manifest.json`.
- Guardrail: Commercial super-app deck. IMPORTANT: the source contains an inheritance contamination flag: phases/journeys currently include Korea/Kakao route labels despite Gojek’s Indonesia/Singapore network thesis. Grok must not present Korean route content; rebuild launch-market slide from source markets/network_footprint only after exact ID validation.

### `abu-dhabi-itc`
- Read `deck-studio/decks/abu-dhabi-itc/deck.config.json`, `slide-manifest.json`, `content-source.json`, and `image-manifest.json`.
- Guardrail: Authority deck. Focus Abu Dhabi island-core / emirates connectivity first. Gulf cross-border legs are range-gated roadmap and must not be sold as N30 commercial-now.

### `dubai-rta`
- Read `deck-studio/decks/dubai-rta/deck.config.json`, `slide-manifest.json`, `content-source.json`, and `image-manifest.json`.
- Guardrail: Authority deck. Focus Dubai Creek/Harbour/Palm/Dubai Islands and UAE emirates connectivity. Gulf cross-border legs are Quanta-LR roadmap only.

### `singapore-mpa`
- Read `deck-studio/decks/singapore-mpa/deck.config.json`, `slide-manifest.json`, `content-source.json`, and `image-manifest.json`.
- Guardrail: Authority/regulator deck. Focus clean harbour-craft mandate, Singapore inner-waterfront, and exact-bound Batam/Bintan/Desaru/Riau candidates. Regional SEA examples outside Singapore must be source-labeled and not overclaimed as MPA scope.

### `red-sea-global`
- Read `deck-studio/decks/red-sea-global/deck.config.json`, `slide-manifest.json`, `content-source.json`, and `image-manifest.json`.
- Guardrail: Hospitality/sovereign developer deck included by explicit user request. Preserve prior guardrail: do not create new NEOM/Red Sea Global binds elsewhere; for this deck use only source-backed Red Sea Global assets and leave inherited Maldives/Four Seasons/Bora Bora artifacts as gaps unless validated.

### `saudi-pif`
- Read `deck-studio/decks/saudi-pif/deck.config.json`, `slide-manifest.json`, `content-source.json`, and `image-manifest.json`.
- Guardrail: Sovereign investment deck. Preserve prior guardrail: no new NEOM / Red Sea Global binds unless exact existing source requires them; separate PIF national/Jeddah/Eastern Province narrative from NEOM/RSG roadmap/hold items.

### `jih-global`
- Read `deck-studio/decks/jih-global/deck.config.json`, `slide-manifest.json`, `content-source.json`, and `image-manifest.json`.
- Guardrail: Sovereign/JV Maldives deck. Economics URL and sidecar exist; routes show limited exact binding. Grok should anchor to Velana/Greater Malé first and leave mid-atoll resort hops pending/null until sealed.

