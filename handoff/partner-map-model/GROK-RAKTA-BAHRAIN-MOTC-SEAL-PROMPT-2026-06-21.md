# Grok deterministic seal prompt — RAKTA + Bahrain MOTC authority proposals (2026-06-21)

## Mandate
Tasklet has completed the review-safe authority-proposal lane for RAKTA and Bahrain MOTC from the PR #58 UAE/Gulf shared spine. Publish only after deterministic seal and QA. Do not invent route IDs, city IDs, distances, or economics.

## Inputs in this PR
- `partner-pitch/partners/rakta.json`
- `partner-pitch/partners/bahrain-motc.json`
- `partner-pitch/RAKTA-ANCHOR-CITY-CROSSWALK.json`
- `partner-pitch/BAHRAIN-MOTC-ANCHOR-CITY-CROSSWALK.json`
- `handoff/partner-map-model/rakta-route-seal-ledger-2026-06-21.json`
- `handoff/partner-map-model/rakta-held-null-route-ledger-2026-06-21.json`
- `handoff/partner-map-model/rakta-scope-2026-06-21.json`
- `handoff/partner-map-model/bahrain-motc-route-seal-ledger-2026-06-21.json`
- `handoff/partner-map-model/bahrain-motc-held-null-route-ledger-2026-06-21.json`
- `handoff/partner-map-model/bahrain-motc-scope-2026-06-21.json`

## RAKTA guardrails
- RAK domestic and RAK↔Dubai may become commercial-now candidates only after exact BP/city/route seal, land/water QA, and range gate.
- RAK↔Sharjah / Abu Dhabi / Fujairah are held-null in this Tasklet extraction unless exact spine geometry is found.
- RAK↔Musandam/Khasab must receive exact Oman/Musandam registry treatment; do not show Khasab as a RAK city substitute.
- RAK↔Muscat / Doha / Bahrain remain Quanta-LR roadmap / amber-dashed, not N30 launch claims.

## Bahrain MOTC guardrails
- Bahrain domestic and Manama↔KSA Eastern Province may become proposal candidates after seal.
- Manama↔KSA Eastern Province is the only commercial-now cross-border lane in this pass.
- Bahrain↔Doha / Dubai / Abu Dhabi remain Quanta-LR roadmap / amber-dashed.

## Required Grok outputs
For each partner:
1. Anchor-city crosswalk with OK / ID_MISMATCH / MISSING_GEOMETRY.
2. Route seal ledger mapping Tasklet `_spine_corridor_id` to live `route_id` or held-null reason.
3. Held-null route ledger with every unsealed candidate and reason.
4. Land/water QA and no silent dropped routes.
5. Range/vessel gate QA: ≤70nm N30 candidate; 75–150nm Quanta-LR roadmap; >150nm Quanta-LR review.
6. Render QA: side panel loads, route chips resolve where sealed, roadmap routes visually distinct, no stale economics provenance.
7. Only after route IDs are sealed: trigger Tasklet finance cascade for authority economics, transparent Sheets, partner JSON growth blocks, `economics_by_route_id` sidecar, and master tracker update.

Null beats sparkle-dust: leave IDs and economics null where exact seal fails.
