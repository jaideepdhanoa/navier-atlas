# Gold #65 — Phase ζ (LB-122)

Date: 2026-06-11
Scope: Grok backend punch-list. NO geometry changes.

## Changes
- **ζ1**: Added `growth_case.partner_platform_rev_full_journey_yr` banded sibling (journey_gmv × 0.18). Ceiling reference, NOT a 7th ladder rung. platform_rev rung remains Navier-subset Interpretation A (~$830M Grab).
- **ζ2**: `journey_gmv` rung re-labeled "Journey GMV — food + stays + experiences (≈3× TAM)"; basis text: "add food, stays, and experiences to every crossing in the induced market".
- **ζ3**: Added `confidence_label` field to rungs + phase horizons. Values: Grounded / Modeled / Projected.
- **ζ4**: `featured_routes[].route_ids[]` one-cycle alias added across all 27 partner files (215 routes). Render lane should read `route_ids` first, fall back to `route_id`. Multi-corridor network bundles can append additional ids to the array.

## Partner JSONs re-cascaded
- grab ✅, careem ✅, jih-global ✅, qatar ✅ (4/6 full re-cascade)
- red-sea-global / saudi-pif: pre-existing M_today=None (no rebuild from ζ; aggregate format differs)

## Reference
- LB-122 in OPS-LOOP-LEDGER.md
- HARD RULE preserved: live canonical decks NOT touched (deck cascade step E excluded)
