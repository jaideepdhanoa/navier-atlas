# Gold #27 — Partner route-link accuracy → 100% (P0 #1 resolved)

**Geometry unchanged from #26** (5,229 routes; FEATURES/ROUTES/STORIES/VESSEL_SPECS hashes identical). This is a **pitch-surface accuracy** seal only.

## What changed
The baked public surface `data-clean/partners/` now links at **100% precision** on every axis:

| axis | before (#26) | after (#27) |
|---|---|---|
| featured `route_id` linked / pass ±25% | 45 / measured low | **49 / 49 (100%)** |
| journey `route_id` linked / pass ±25% | 45 / measured low | **47 / 47 (100%)** |
| `route_ids` chips total / in-gate | 1830 / 67 (~4%) | **107 / 107 (100%)** |

## Root cause of the 31%/23% you reported
`gated_relink.py` correctly gated the **singular** `route_id`, but left the **plural `route_ids` chip arrays** ungated. The render lane resolves those chips for click-to-highlight, so the displayed accuracy tracked the chips (only 67 of 1,702 in-gate), not the route_id.

## Fix
1. Re-ran `gated_relink.py` on #26 geometry — more corridors exist now, so featured 45→49, journeys 45→47 (all pass distance + endpoint + name gates).
2. **NEW** `partner-pitch/_tools/gate_chips.py` — prunes every `route_ids` array by the same gates: distance ±25% of label `distance_nm` AND unordered endpoint city-pair ID match. Chips we can't verify are dropped. 193 items had **zero** in-gate chips → `route_ids: null` (honest, no highlight). 37 items keep a tight, distance-accurate set.

Principle held throughout: **exactness over coverage; null beats confidently-wrong; ID-based only.**

## Note on coverage
Many items are null because **no gold corridor exists yet** for that label (not a linking bug). As Track C geometry lands (orphan clusters, curated-waypoint edges), re-running both tools will lift coverage automatically — precision stays 100%.
