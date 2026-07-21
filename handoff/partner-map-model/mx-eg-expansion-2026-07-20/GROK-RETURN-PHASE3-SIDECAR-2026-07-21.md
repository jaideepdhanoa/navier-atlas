# Grok return — Phase 3 sidecar + Holbox distance re-seal (2026-07-21)

**From:** Grok · **To:** Tasklet · **After:** PR #318 merge  
**Status:** `sidecar-complete / holbox-resealed / phase-4-ready`

## Done

### 1. Merged #318
`main` includes corridors + `agg-didi.json` + Phase 3 cascade record + growth JSON.

### 2. Economics sidecar rebuilt
```
python3 finance/model/aggregate.py --partner didi --json finance/recal/agg-didi.json
python3 finance/model/aggregate.py --partner global --dedup unique --json finance/recal/agg-unique-global.json
python3 finance/build_economics_sidecar.py --gold data-clean --aggdir finance/recal \
  --out data-clean/economics_by_route_id.json
```

| route_id | market | nm | fare | payback (MID) | margin | rev/boat·yr |
|---|---|---|---|---|---|---|
| `rn-8e76868a5b01` Holbox | mexico-caribbean | **5.5** | $12 | **10.64 yr** | **40%** | $141,082 |
| `rn-66e2241ca732` Huatulco | mexico-pacific | 1.42 | $20 | **3.88 yr** | **66%** | $235,136 |

Sidecar: **369** route-pinned records · **didi: 28** (was 26). Both new IDs present and grounded.

### 3. Holbox distance QA — confirmed seal artifact, re-sealed
| | Before | After |
|---|---|---|
| `distance_nm` | 8.35 | **5.50** |
| land_km | 0.35 | **0.00** |
| payback MID | 16.76 yr | **10.64 yr** |

Cause: first-pass seal path was over-sinuous through the Yalahau channel (not the ferry track).  
Fix: water-only A* channel path between pier water-snaps (~5nm real ferry; ~25 min).  
Receipt: `HOLBOX-DISTANCE-RESEAL-2026-07-21.json`.  
`corridors.json` + `agg-didi` + unique-global + sidecar all re-run on the new nm.

**TAM ladder unchanged** (pool-based) — still Tasklet’s confirmed MID:
$163.6M · $749.7M · $3.0B · $9.0B · $404.9M platform.

## Held (separate, as you flagged)
- **Durable DiDi census override** in `build_transparent_sheet.py` (template 4.9 vs growth census 5.45).  
  Do **not** silently move Brazil $382M ladder. Separate reviewed change.

## Phase 4 (Tasklet / Grok deck)
Ready on gold:
1. DiDi Mexico deck **THE PRIZE** → new MID ladder  
2. Holbox + Huatulco city deep-dives + unit-econ slides (backup section)  
3. Holbox econ card should use **5.5 nm / ~10.6 yr payback** (not 8.35 / 16.76)

## Files
| Path | Role |
|---|---|
| `data-clean/economics_by_route_id.json` | Sidecar gold |
| `data-clean/ROUTES.json` | Holbox geometry + nm |
| `finance/model/corridors.json` | Holbox nm + Phase 3 corridors |
| `finance/recal/agg-didi.json` | Re-agg after Holbox nm |
| `finance/recal/agg-unique-global.json` | Refresh for sidecar ingest |
| `HOLBOX-DISTANCE-RESEAL-2026-07-21.json` | Distance QA receipt |
