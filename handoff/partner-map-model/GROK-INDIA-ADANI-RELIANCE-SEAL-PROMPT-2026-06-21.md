# Grok prompt — India Adani / Reliance proposal seal-readiness pass

Date: 2026-06-21
Owner split: Tasklet authored research/narrative/scope; Grok owns deterministic ID matching, geometry minting, route binding, render QA and seal acceptance.

## Inputs in this PR

- `partner-pitch/partners/adani-ports.json`
- `partner-pitch/partners/reliance-industries.json`
- `handoff/partner-map-model/india-adani-reliance-expanded-proposal-control-2026-06-21.json`
- `handoff/partner-map-model/india-adani-reliance-sealed-atlas-crosswalk-2026-06-21.json`
- `handoff/partner-map-model/INDIA-ADANI-RELIANCE-EXPANDED-PROPOSAL-PACKAGE-2026-06-21.md`
- `handoff/partner-map-model/INDIA-ADANI-RELIANCE-SEALED-ATLAS-CROSSWALK-2026-06-21.md`
- Prior research-only queue files already in PR #61.

## Objective

Make the Adani and Reliance India proposal files renderable and seal-ready without any further Tasklet input, while preserving exactness:

1. Use the broad owner/operator narrative: both partners can own/run Navier India across all relevant markets.
2. Use only exact Atlas IDs for executable display scope.
3. Leave every unbound route/BP/corridor as `null` with an explicit hold reason.
4. Do not invent economics.

## Current display scope

These are the only existing Atlas display city IDs Tasklet found for India:

- `mumbai-india`
- `goa-india`
- `kerala-backwaters-india`
- `andaman-india`

The sealed crosswalk includes POI and route counts and full sealed POI/route rows by city. Use it as the first registry lookup.

## Reviewable sealed hits

- Reliance / Nariman Point:
  - `bp-mum-nariman-point` — `Nariman Point Water-Taxi Jetty`
  - route review-only: `ics-mum-gorai-nariman` confirms Nariman is routable, but **does not** satisfy RCP/NMIA/Ulwe route intent.
- Goa / Mormugao:
  - sealed Goa BP hits exist and may support Goa display-market routing.
  - Do **not** present Mormugao as Adani-owned unless separately source-backed.

## Must remain null until exact-bound or minted

- Adani: Ulwe/NMIA passenger BP, Dighi/Agardanda, Hazira, Mundra, Tuna, Dahej, Vizhinjam, Kattupalli, Ennore, Krishnapatnam, Gangavaram, Dhamra, Haldia, Karaikal, Gopalpur.
- Reliance: Ghansoli/RCP, Jamnagar, Hazira, Dahej, Nagothane, Patalganga, Gadimoga / KG D6, plus any industrial/campus route lacking a passenger-water access proof.

## Deterministic tasks

1. Validate every `markets[].anchor_cities[]` against sealed Atlas `city_id` values or the accepted city/cluster registry.
2. For every `journeys_unlocked[]` / phase `featured_routes[]`:
   - bind `from_node_id`, `to_node_id`, and `route_id` only when exact endpoint intent matches a sealed route or newly minted route;
   - otherwise keep `route_id: null` and append a hold reason.
3. For backlog assets:
   - exact-match to existing sealed POIs/routes first;
   - if no exact hit, mint only when official/source-backed coordinates and water/passenger suitability are adequate;
   - otherwise leave `candidate_only_no_bind` or `brief_only_registry_gap_queue`.
4. Range-gate every corridor:
   - ≤70nm → N30 / Pioneer II;
   - 75–150nm → Quanta-LR amber-roadmap;
   - >150nm → Quanta-LR review, never Pioneer II.
5. Produce a drop/hold ledger with zero silent drops.
6. Render-check both partner proposal pages and all sub-pages.
7. Do **not** run finance/economics unless route-level demand and fare records are separately sourced and added.

## Acceptance output expected from Grok

- Updated partner JSON files with exact IDs where valid and null/hold ledger elsewhere.
- Anchor-city crosswalk: OK / ID_MISMATCH / MISSING_GEOMETRY.
- BP/route bind ledger: bound / minted / held / dropped, with source and reason.
- Render QA: every display market appears; no empty pages caused by ID mismatch.
- No economics sidecar unless a later economics cascade supplies demand/fare inputs.

## Non-actions

- Do not create a second `adani-ports` partner shell.
- Do not promote broad country/port/campus evidence into executable map footprint.
- Do not use substring matches such as `tuna` inside unrelated names like `Fortuna` or `Natuna`.
- Do not treat route labels as exact if the endpoint intent differs.
