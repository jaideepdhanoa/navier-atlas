# Atlas Hierarchy First — Partner Display + Economics Audit

This corrects the PR #55 sequencing and terminology: mirror the existing Atlas `region → cluster → city → locale_type/archetype` hierarchy first, then map partner operating-market buckets into that hierarchy.

## Source-of-truth layers
- `data-clean/city_briefs/*.json`: researched global city/market universe.
- `data-clean/CLUSTERS.json`: existing region/cluster membership and anchors.
- `data-clean/ROUTES.json`: route geometry and endpoint city IDs.
- `data-clean/FEATURES_BY_TYPE.json` + boarding-point exports: BP/node evidence.
- `finance/model/corridors.json`: economics/financial-model-ready subset, **not** the display gate and not the whole global geography universe.

## Operating rules
- The Atlas hierarchy is the geography source of truth; do not invent a parallel geography model.
- Partner maps/pages may display canonical Atlas cities/routes when the hierarchy key + route geometry exist.
- Economics/financials are tracked enrichment for model/sidecar promotion; they do **not** gate proposal-page display.
- ID/provenance match only; null beats confidently-wrong.

## Counts
- **city_briefs**: 208
- **clusters**: 102
- **routes**: 6,846
- **economics_registry_markets**: 54
- **partner_files_scanned**: 117
- **partner_market_mentions_normalized**: 173
- **city_briefs_economics_ready**: 51
- **display_ready_city_markets_with_geometry**: 176
- **display_ready_but_economics_pending**: 125
- **city_briefs_needing_route_or_grounding_cleanup**: 32

## Delta summary
- **economics_ready_today**: 51
- **display_ready_but_economics_pending**: 125
- **needs_route_or_unquarantine**: 15
- **needs_boarding_points_or_grounding**: 10
- **brief_stub_or_low_signal**: 7

## Display vs. promotion
A partner bucket should resolve to canonical Atlas city IDs. If those city IDs already have route geometry, they can appear on a partner proposal page even before economics/financials are complete. “Promotion” means adding/aligning economics/model inheritance and sidecar fields; it is not geography creation and should not block display.

## Generated artifacts
- `global-registry-source-inventory.json` — full city/cluster/route/BP/economics inventory from existing Atlas sources.
- `global-registry-delta.json` — existing Atlas markets grouped by display/economics/cleanup status.
- `global-inheritance-registry.json` — derived manifest mirroring Atlas city IDs with display and economics readiness flags.
- `partner-global-registry-map.json` — partner market buckets mapped to existing Atlas city IDs.
- `partner-market-registry-match-audit.json` — partner market mentions matched against registry/city IDs for the second step.
