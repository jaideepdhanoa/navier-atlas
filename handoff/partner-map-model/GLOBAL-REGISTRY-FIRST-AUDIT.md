# Global Registry First — Partner Inheritance Audit
This corrects the PR #55 sequencing: build the global Atlas registry universe first, then map partners into it.
## Source-of-truth layers
- `data-clean/city_briefs/*.json`: researched global market/city universe.
- `data-clean/CLUSTERS.json`: region/cluster membership and anchors.
- `data-clean/ROUTES.json`: route geometry and endpoint city IDs.
- `data-clean/FEATURES_BY_TYPE.json` + boarding-point exports: BP/node evidence.
- `finance/model/corridors.json`: economics-ready inheritance subset, not the whole global universe.

## Counts
- **city_briefs**: 208
- **clusters**: 102
- **routes**: 6846
- **economics_registry_markets**: 54
- **partner_files_scanned**: 117
- **partner_market_mentions_normalized**: 173
- **city_briefs_economics_ready**: 51
- **city_briefs_atlas_routed_not_econ**: 125
- **city_briefs_brief_only**: 25

## Delta summary
- **economics_ready_today**: 51
- **ready_to_promote_from_active_routes**: 125
- **needs_route_or_unquarantine**: 15
- **needs_boarding_points_or_grounding**: 10
- **brief_stub_or_low_signal**: 7

## Operating rule
A partner can inherit only from canonical registry keys. If a partner-relevant market exists as a city brief/route/BP but not yet as a registry key, promote the market into the global registry first; if it lacks BP/route grounding, put it into the registry gap queue.

## Generated artifacts
- `global-registry-source-inventory.json` — full city/cluster/route/BP/economics inventory.
- `global-registry-delta.json` — markets researched in Atlas but absent from the economics inheritance registry, grouped by next action.
- `partner-market-registry-match-audit.json` — partner market mentions matched against registry/city IDs for the second step.
