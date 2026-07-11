# Dott/Voi Wave 1 coordinate-gated seal receipt

**At:** 2026-07-11T05:01:14Z  
**Source:** `grok/dott-voi-coordinate-gated-wave1-2026-07-11`  
**Status:** `sealed_partial`  
**Upstream PRs:** [225, 226, 227]

## Before → after

| Surface | Before | After | Δ |
|---------|-------:|------:|--:|
| Cities | 358 | 358 | 0 |
| POIs | 11538 | 11538 | 0 |
| Routes | 6251 | 6264 | 13 |
| Clusters | 142 | 142 | 0 |

## Boarding points (89/89 classified — 0 silent drops)

```json
{
  "held": 21,
  "reused_name_match": 66,
  "reused": 2
}
```

- **66** sealed on first pass (T1/T2, water-adjacent)
- **2** exact existing ID reuses (Nyon, Rolle)
- **21** held (null coords, non-coordinate gates, identity ambiguity, closed pontoon, etc.)

## Routes (42/42 classified — 0 silent drops)

```json
{
  "held": 29,
  "sealed": 13
}
```

- **13** sealed with water-aware or inland-water densified geometry (land-mask false-positive budget applied)
- **29** held: 10 coordinate-held pairs + 4 non-coordinate-held + 15 hand-geometry needed (overland chord / long river bend exceeds budget)

## Gates

```json
{
  "bp_receipt_covers_all": true,
  "route_receipt_covers_all": true,
  "silent_drops": 0,
  "economics_touched": false,
  "voi_europe_only": true,
  "dott_uae_retained": true,
  "sealed_with_land_flag": 11
}
```

## Partner inheritance

- Dott UAE retained; new Europe clusters bound via `_map_scope.registry_keys` / `cluster_city_ids`
- Voi Europe-only; same cluster inheritance pattern
- No partner-specific route forks; corridors authored once in global `ROUTES.json`

## Economics

**Untouched** in this seal.

## Machine receipt

`GROK-WAVE1-COORDINATE-GATED-SEAL-RECEIPT-2026-07-11.json`
