# Gold #53 — BATCH A: grab.json copy + chip-flag clear (LB-23 zip-patch)

**Method:** LB-23 zip-patch from Gold #52. Single-file delta. No rebuild.
**Prev gold:** navier-export-20260611T034626Z.zip (Gold #52)

## Scope
One file changed: `data-clean/partners/grab.json` (baked surface; `deck_only` stripped per externalization gate).

## What changed in grab.json
- Copy fixes across modal/display strings (chip + hero copy polish).
- New `growth_case.modal_headline` field.
- New `growth_case.modal_lead` field.
- New `growth_case._recal_provenance.root_phase_ramp` (4-element ramp) + `root_phase_ramp_as_of` + `root_phase_ramp_source` provenance metadata.
- `growth_case._render_chip_flag.needs_new_layouts` (3-entry array) CLEARED → replaced with `layouts_shipped_in` scalar (chips have shipped; flag retired).

## What did NOT change
- Geometry (no ROUTES.json / CLUSTERS.json edits).
- Economics (`economics_by_route_id.json` byte-identical; sidecar sha + count = 105 preserved in SEAL.json).
- Sidecars block in SEAL.json.
- All other partner files (incl. agg-grab.json — untouched, no agg-grab.json in zip).
- City/cluster nodes, FEATURES_BY_TYPE, STORIES, VESSEL_SPECS, CORRIDOR-ENDPOINT-GROUNDING — all carried verbatim from #52.

## Grok punch-list items addressed
- **P0 items 1–5:** modal copy polish + modal_headline + modal_lead + provenance for root_phase_ramp.
- **P3 _render_chip_flag:** `needs_new_layouts` cleared; `layouts_shipped_in` records the gold in which the layouts shipped.

## Gates (all PASS on staged zip surface)
- gate_chips.py: 37 items w/ chips, 107 chips before/after, 0 nulled.
- gate_route_id.py: featured 235/1017 had_id, 5 nulled; journey 145/657 had_id, 11 nulled (identical to #52; no regressions — this gate also runs in --write mode on prev golds; here we run read-only).
- gate_city_ids.py: PASS — 198 valid nodes, 5280 routes, 75 clusters all resolve.
- gate_endpoint_labels.py: 108 OK, 1 OK_NO_DISTINCTIVE, 13 WEAK_SINGLE_TOKEN (carry-over review items from #52 — no NEW hard flags introduced by this patch).

## SEAL.json deltas
- `version`: (absent) → 53
- `meta.gold`: "#18" (frozen legacy field) → "#53"
- `meta.note`: rewritten to describe this patch.
- `sealed_at`: bumped.
- `changed_files`: ["data-clean/partners/grab.json"].
- `sidecars.economics_by_route_id.json`: UNCHANGED (sha256 6f64b117…, count 105).
