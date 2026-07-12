# Rule: Covered footprint must resolve into a market keep

**Status:** permanent (2026-07-12)  
**Gate:** `python3 scripts/audit_partner_route_inheritance_health.py --fail-on-a`  
**Origin:** Dott × Doha empty routes; bolt/didi/yango footprint-only cities

## Statement

If a partner `network_footprint[]` entry has `covered: true` **and** any city resolved from that key has endpoints in `data-clean/ROUTES.json`, then **at least one** `markets[]` row must resolve a keep set that includes those cities.

Otherwise the hub may paint the city (via footprint / `_map_scope`) while **no** `/partner/<market>` page inherits the corridors — the Dott/Doha gap class.

## How to satisfy

1. **Preferred:** add/extend a `markets[]` row:
   - city seal: `scope_registry_key: "<city-id>"` + `anchor_cities: ["<city-id>"]`
   - multi-city: `scope_registry_keys: ["city-a", "city-b", …]` + matching anchors
   - or country market whose live resolve already includes the cities (slug/cluster expansion)
2. **Or demote footprint** so it is not geometry-claiming:
   - set `render` to dots / aspirational and do **not** claim covered geometry until a market keep exists
3. **Never:** invent partner-private `route_id`s or expand a city seal to a full country cluster just to “make lines show”

## Featured routes

`featured_routes[].route_id` must either:

- exist in `ROUTES.json` with geometry, or
- be intentional `display: text_only` / `_link_status: aspirational-no-built-route`

## Finance

Map inheritance ≠ finance inheritance. When a registry market exists (`bolt-cyprus`, `yango-tunisia`, …), ensure the partner’s cascade/sheet path includes it. Do not invent demand rows without registry corridors.

## Gate usage

```bash
# Report only
python3 scripts/audit_partner_route_inheritance_health.py

# Block merge/deploy when footprint-only geometry gaps remain
python3 scripts/audit_partner_route_inheritance_health.py --fail-on-a
```

Pre-flight / release: run `--fail-on-a` after partner footprint or market edits.
