# Grok — Dott/Voi coverage seal (PR #216)

**Status:** `scope_resealed / inheritance_renderer_fixed / end_state_scrubbed / finance_not_promoted`

## Renderer fixes
- `partner-scope.mjs`: no legacy `cluster_city_ids` union; no `end_state_cities` re-injection; micromobility market→cluster aliases
- `route-display.mjs`: hub `inheritClusters` ships full set (no density cull / no auto-legacy)
- `build-site.mjs`: hub routes = `ROUTES ∩ sealed registry cluster_ids`

## Scope (evidence-supported)
| Partner | Clusters | Beirut | Qatar | Sweden | NL routes | Expected routes (cluster ∩) |
|---------|----------|--------|-------|--------|-----------|------------------------------|
| Dott | 17 (incl. UAE current) | 0 | 0 | 0 | **8/8** | **~1204** |
| Voi | 14 + UAE expansion | 0 | n/a | 20 (current) | **8/8** | **~807** (incl. ~399 UAE expansion) |

## Stale removed
- **Dott:** bahrain, cyprus, dalmatia-croatia, egypt, estonia, ireland, lebanon, monaco, morocco, portugal, qatar, romania, sweden
- **Voi:** cyprus, dalmatia-croatia, egypt, estonia, greece, ireland, israel, lebanon, monaco, morocco, portugal, romania, saudi-arabia

## Still P1 registry (null / not minted)
Belgium · Voi Le Havre · UK/Germany/Nordics depth · Poland (Dott) · Switzerland zero-route · Austria/Hungary

## Gates
- Gate G: PASS
- No economics promotion

Machine: `GROK-DOTT-VOI-COVERAGE-SEAL-RECEIPT-2026-07-10.json`
