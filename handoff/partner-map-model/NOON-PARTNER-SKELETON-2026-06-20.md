# Noon partner skeleton — 2026-06-20

Generated a **review-safe draft**, not a live partner JSON replacement.

## Source and filter

- Source: `handoff/partner-map-model/uae-gulf-shared-corridor-spine.json`
- Filter: `usable_by_noon = true` and `current_geometry_status = geometry_present`
- Derived corridors: **484**

## Route pools

| Pool | Geometry-present rows | Treatment |
|---|---:|---|
| `domestic_uae_intra_city` | 452 | commercial-now review pool |
| `inter_emirate_uae` | 18 | selected commercial-now review pool |
| `uae_gulf_cross_border` | 14 | amber roadmap / regulatory gated |

## Derived scope IDs

- Active UAE IDs: `abu-dhabi-uae, dubai-uae, fujairah-uae, ras-al-khaimah-uae, sharjah-uae`
- Amber / non-UAE IDs: `doha-qatar, manama-bahrain, muscat-oman`

## What changed

- Built `noon.partner-skeleton.draft.json` as a schema-valid draft object using `archetype = super_app` and `category = commerce_logistics_superapp`.
- Added deterministic `scope_derivation` metadata so Grok can rederive city scope from the spine instead of trusting a hand list.
- Added phase scaffolding, local use cases, proof points, objections, and route refs with boarding-point endpoints.
- Kept every `route_id` as `null` until Grok seals canonical IDs.
- Kept KSA/Egypt/non-UAE Gulf lanes outside active map scope; cross-border rows are amber roadmap only.

## Files

- `noon.partner-skeleton.draft.json`
- `noon-skeleton-derivation-2026-06-20.json`

## Next gate

Run Grok seal/QA to bind route IDs, render-check the side panel, then cascade economics only after canonical route IDs are confirmed.
