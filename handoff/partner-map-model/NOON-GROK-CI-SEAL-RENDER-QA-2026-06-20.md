# Noon — Grok CI seal/render QA handoff (2026-06-20)

## Purpose

Turn the Tasklet-built Noon skeleton into a deterministic Grok CI lane: anchor-city ID crosswalk, featured-route ID sealing, and render QA. This is **not** permission to broaden Noon beyond UAE-first scope.

## Inputs

- `handoff/partner-map-model/noon.partner-skeleton.draft.json`
- `handoff/partner-map-model/noon-skeleton-derivation-2026-06-20.json`
- `handoff/partner-map-model/uae-gulf-shared-corridor-spine.json`
- `partner-pitch/schema/partner_proposal.schema.json`

## Scope contract

- Active map scope: `abu-dhabi-uae, dubai-uae, fujairah-uae, ras-al-khaimah-uae, sharjah-uae`
- Amber/future only: `doha-qatar, manama-bahrain, muscat-oman`
- Route pools already derived from the UAE/Gulf spine:
  - Domestic UAE: **452**
  - Inter-emirate UAE: **18**
  - UAE/Gulf cross-border: **14**, amber/regulatory-roadmap only

## Required Grok tasks

1. **Anchor-city crosswalk** — resolve skeleton city IDs to renderer city IDs; output `partner-pitch/NOON-ANCHOR-CITY-CROSSWALK.json`.
2. **Featured-route seal** — bind canonical route IDs from source corridor IDs and BP nodes; output `handoff/partner-map-model/noon-route-seal-ledger.json`.
3. **Render-safe Noon draft** — create a render-safe draft/live JSON after crosswalk and route seal; keep active scope UAE-only and no footprint-card grid.
4. **Render QA ledger** — confirm UAE markets/routes render and held/economics-pending items are explicit; output `handoff/partner-map-model/noon-render-qa-ledger.json`.

## Featured routes requiring route seal

The machine manifest carries the full route-seal queue (`featured_routes_requiring_seal`) with 12 source corridors, BP nodes, distances, and current held/null status.

## Hard gates

- Null beats confidently wrong.
- No KSA/Egypt active scope.
- No Qatar/Bahrain/Oman active scope; keep Gulf cross-border as amber/regulatory roadmap.
- No Adani/Reliance geography promotion in this lane.
- Display can proceed without economics, but economics-pending must remain explicit.
- Economics cascade starts only after route IDs and render QA pass.

## Machine manifest

See `handoff/partner-map-model/noon-grok-ci-seal-render-qa-2026-06-20.json`.
