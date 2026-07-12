# Partner route inheritance health — 2026-07-12

## Why this pass
Dott × Doha failed because **city-level partner scope** only keeps routes whose **endpoint city ∈ keep**, while many Doha metro BPs/routes were stamped under the wrong city (`al-wakrah-qatar` / `manama-bahrain`). That is a **join bug**, not a missing corridor invention problem.

## Permanent audit
```bash
python3 scripts/audit_partner_route_inheritance_health.py
# → grok-routing-output/partner-route-inheritance-health.json
```

Also keep running:
- `python3 scripts/validate_partner_inheritance.py` (featured ⊆ inherited geometry)
- `python3 scripts/validate_finance_inheritance.py` (shared geography finance spines)
- `python3 scripts/validate_scope_resolution.py` (registry keys resolve)
- `node scripts/audit-partner-scope-drift.mjs` (stored vs live cluster scope)

## Failure classes (Dott/Doha pattern)

| Code | Meaning | Severity when real |
|------|---------|-------------------|
| A | Covered footprint city has geometry but **no market keep** includes it | HIGH — empty market surface |
| B | City-level seal id used as `partnerClusters` cluster_id | INFO by design if endpoint stamps work |
| C | Keep city has **zero** route endpoints | MED — empty city on map |
| D | Featured `route_id` missing from `ROUTES.json` | HIGH — marquee dead |
| E | Finance `inheritance_spec` omits registry market for covered footprint | MED |
| F | POI name/coords imply city A, `parent_city_id` is B | HIGH — same as Doha root cause |
| G | Market both-endpoint filter yields 0 displayable routes | HIGH (unless aspirational-only) |

## Systemic code already fixed (this lineage)
1. Market + legacy route filters fall back to `from_city_id`/`to_city_id` when BP node missing (`build-site.mjs`, `route-display.mjs`).
2. String `network_footprint` entries no longer crash sealed-key collection (`partner-scope.mjs` / `partner_scope_py.py`).
3. Dott Doha markets + finance inherit + signature rebind (#245–#246).
4. Additional Doha-named BPs misparented to **Manama** reparented to `doha-qatar` (coords confirm Doha bay).

## Cross-partner results (post-refine)

### A — true footprint-only gaps (geometry, no market keep)
- `bolt:cyprus (geo 10)`
- `bolt:auckland-new-zealand (geo 28)`
- `didi:cozumel-mexico (geo 3)`
- `didi:playa-del-carmen-mexico (geo 3)`
- `didi:floreana-galapagos-ecuador (geo 1)`
- `didi:isabela-galapagos-ecuador (geo 1)`
- `didi:san-cristobal-galapagos-ecuador (geo 1)`
- `didi:santa-cruz-galapagos-ecuador (geo 3)`
- `didi:lima-peru (geo 10)`
- `didi:paracas-peru (geo 3)`
- `didi:pisco-san-andres-peru (geo 1)`
- `yango:accra-tema-ghana (geo 2)`
- `yango:karachi-pakistan (geo 7)`
- `yango:lobito-benguela-angola (geo 1)`
- `yango:luanda-angola (geo 3)`
- `yango:maputo-mozambique (geo 16)`
- `yango:baku-azerbaijan (geo 9)`
- `yango:tunis-tunisia (geo 4)`
- `yango:djerba-tunisia (geo 3)`

These need either a `markets[]` row with `scope_registry_key` / anchors (Dott/Doha pattern) **or** an explicit aspirational footprint (`render` dots / not geometry).

### E — finance inherit gaps
- none (false friends filtered)

### G — market zero geometry (non-aspirational)
- `ola:chennai-ecr-cuddalore-puducherry-coast G_market_zero_geometry`
- `rapido:chennai-ecr-cuddalore-puducherry-coast G_market_zero_geometry`
- `uber-india:chennai-ecr-cuddalore-puducherry-coast G_market_zero_geometry`
- `uber:chennai-ecr-cuddalore-puducherry-coast G_market_zero_geometry`

### C — keep cities with zero routes
48 city×partner pairs (often inland / river keys or coverage keys without sealed marine geometry). Treat as coverage honesty, not invent routes.

### B — city-level seals
Expected for Dott `doha-qatar` / `jeddah-ksa` and India city seals. Cluster fallback must **not** expand to full country; endpoint city stamps must be correct (F).

### F — POI mismatches remaining
29 heuristic hits (many Palm locale parents / West Bay name collisions). Sample in JSON report.

## Cascade rule (always)
```
partner_routes(P) = ROUTES where
  (from_city_id ∈ keep(P) OR to_city_id ∈ keep(P) OR cityIdOf(endpoint) ∈ keep(P))
  [market pages: BOTH endpoints ∈ keep]
keep(P) = live resolve(markets[].scope_registry_key ∪ footprint covered ∪ _map_scope.registry_keys)
  city-level keys resolve to that city only — never invent partner-private corridors
featured.route_id MUST exist in ROUTES.json or be intentional null / aspirational text_only
finance inherit_markets only from existing corridors.json market keys
```

## Do not
- Invent route_ids or hand-draw partner-only lines
- Expand city seals to full country clusters to “make lines show”
- Treat missing grounded demand as a map inheritance failure

Generated: 2026-07-12T20:34:31.159265+00:00
