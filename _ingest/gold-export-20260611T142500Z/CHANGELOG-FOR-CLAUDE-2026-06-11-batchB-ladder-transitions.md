# Gold #54 batchB — grab.json ladder_transitions[] (P0 Grok item shipped)

**Date:** 2026-06-11
**Method:** LB-23 zip-patch from Gold #53. No geometry, no economics rebuild.
**Changed files (1):** `data-clean/partners/grab.json`

## What landed
`growth_case.ladder_transitions[]` — 4 bridge objects across 5 rungs of the SAM/SOM ladder. Each bridge records:
- `from_rung_id` → `to_rung_id`
- `headline` + `basis` (the conceptual step)
- `derivation` (the arithmetic: mid × multiplier → mid)
- `multipliers_cited` (numeric values from `finance/recal/growth-grab.json:parameters_used`)
- `source_fields[]` (pointer paths back into the recal source)

All four bridges verified to **0.00% error** vs the corresponding `revenue_potential.rungs` mids.

## Render impact
`ladder_transitions[]` is now available for the growth-ladder modal render. Each rung-to-rung transition has a typed bridge object explaining WHY the next rung is larger (capture-rate step vs corridor-width step vs both), with the math and the cited multipliers inline.

## What did NOT change
- ROUTES / CLUSTERS / FEATURES / STORIES / VESSEL_SPECS — untouched (SHAs carried forward).
- Economics sidecar — carried forward (105 records, sha unchanged).
- All other partner files — untouched.
- Top-level `deck_only` block — stripped during overlay per externalization rule.

## Gate results (post-patch)
- `gate_chips.py` — PASS (0 nulls; identical to G#53).
- `gate_route_id.py` — PASS (featured_nulled=5, journey_nulled=11; identical to G#53 — no regression).
- `gate_endpoint_labels.py` — PASS (0 hard flags).
- `gate_city_ids.py` — PASS (198 valid nodes, 5280 routes, 75 clusters).

## Provenance
`SEAL.json._gold54_batchB_ladder_transitions` carries the sealed grab.json sha256 + gate results.
