# Grok — Dott/Voi coverage seal

**UTC:** 2026-07-10T17:27:48Z
**Status:** `scope_resealed / voi_europe_only / dott_uae_confirmed / finance_not_promoted`
**Upstream:** PR #216

## Renderer
- Hub inheritance: full cluster_id route set; no density/legacy cull
- No legacy `_map_scope.cluster_city_ids` union on hub-index

## Dott
- Registry keys: 17
- Scope cities: 62 (beirut=False)
- Canonical routes in scope clusters: **1204**
- Stale removed: bahrain, cyprus, dalmatia-croatia, egypt, estonia, ireland, lebanon, monaco, morocco, portugal, qatar, romania, sweden

## Voi
- Registry keys: 14 (Europe only; no UAE/MENA coverage)
- Scope cities: 36 (beirut=False)
- Canonical routes in scope clusters: **408**
- Stale removed: cyprus, dalmatia-croatia, egypt, estonia, greece, ireland, israel, lebanon, monaco, morocco, portugal, romania, saudi-arabia, uae

## Acceptance
- `dott_no_beirut_in_scope_cities`: **True**
- `voi_no_beirut_in_scope_cities`: **True**
- `dott_no_qatar_key`: **True**
- `dott_no_sweden_key`: **True**
- `dott_uae_current_coverage`: **True**
- `dott_abu_dhabi_dubai_in_scope`: **True**
- `voi_europe_only_no_uae_or_mena_scope`: **True**
- `netherlands_in_both`: **True**

Gate G: PASS
Partner inheritance (strict, data + pitch): PASS

Machine: `handoff/partner-map-model/dott-voi/GROK-DOTT-VOI-COVERAGE-SEAL-RECEIPT-2026-07-10.json`
