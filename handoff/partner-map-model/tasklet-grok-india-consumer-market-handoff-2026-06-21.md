# Tasklet × Grok handoff — India consumer-market partner proposals

_Date: 2026-06-21_

## Why this exists

PR #61 added Kolkata/Hooghly and Chennai/ECR/Cuddalore/Puducherry to Adani Ports and Reliance only. Ola, Rapido and Uber still had the earlier India proposal footprint: Mumbai, Goa, Kerala and Andamans. That made the live partner pages look inconsistent even though the Tasklet research brief had already identified Kolkata and Chennai as in-scope high-value consumer markets.

This patch applies the same market inclusion rule to:

- `partner-pitch/partners/ola.json`
- `partner-pitch/partners/rapido.json`
- `partner-pitch/partners/uber.json`

## Division of labor

### Tasklet owns

- Public-source market research and proof points.
- Partner-specific proposal framing.
- Candidate journey labels and narrative.
- Explicit `brief_only_grok_mint_required` status where exact Atlas IDs do not exist.
- Keeping unsealed route fields null instead of inventing IDs, distances or economics.

### Grok owns

- Minting or exact-binding Atlas boarding-point IDs / city IDs.
- Binding route IDs by exact ID match only.
- Measuring route distance and assigning vessel gates.
- Relinking partner journeys and featured routes.
- Route/economics cascade once IDs are sealed.
- Render QA and build-site smoke.

## Guardrails

- Kolkata and Chennai are in scope for India consumer partner proposals.
- Priority B remains out of scope unless explicitly reintroduced.
- Broad-footprint-first is okay for Tasklet narrative; exact-bind-second belongs to Grok.
- `null` beats confidently wrong.
- Brief-only markets must not claim sealed distances, fares, route economics or live Atlas city IDs.

## Current patch behavior

Kolkata and Chennai are added to Ola, Rapido and Uber as proposal-included, brief-only markets with empty `anchor_cities` and null route IDs. This means they can appear in proposal content, but they should not be treated as sealed map/economics claims until Grok returns the deterministic seal ledger.

## Next Grok prompt

Run the India consumer-market deterministic lane for `ola`, `rapido` and `uber`:

1. Read the new `kolkata_hooghly_waterfront` and `chennai_ecr_cuddalore_puducherry_coast` market blocks.
2. Mint or exact-bind candidate BPs/routes only where the registry supports them.
3. Leave all unsupported journeys null with a held-null reason.
4. Produce per-partner route seal ledgers, held-null ledgers, distance/vessel gates, and render QA.
5. Only after route seal, cascade economics into partner JSON / transparent Sheets / tracker.

