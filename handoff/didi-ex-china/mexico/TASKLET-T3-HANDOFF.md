# Tasklet T3 handoff — DiDi Mexico economics

**From:** Grok · G2/G3 seal · `2026-07-09T23:19:41Z`  
**Status after Grok:** `seal-complete / cascade-needed`  
**Do not:** invent L3, use Grab census, or cascade on catch-all `didi` market key.

## What Grok sealed

### G2 boarding points (accepted)
| bp_id | city | note |
|-------|------|------|
| `bp-062decef2f` | cancun-riviera-maya-mexico | Puerto Juárez ferry terminal |
| `bp-d08462d3d9` | cancun-riviera-maya-mexico | Isla Mujeres ferry terminal |
| `bp-pdc-muelle-fiscal` | **playa-del-carmen-mexico** (reparented) | coords snapped to ferry pier |
| `bp-1f95439031` | **cozumel-mexico** (reparented) | Ultramar Cozumel |
| `bp-608e348da1` | cancun-riviera-maya-mexico | POI only — not demand proof |

### Explicit drops / backlog (not silent)
- Chetumal, San Pedro (Belize), Puerto de Lerma — backlog or reject
- Pacific candidate BPs without confirmed coordinates — **not minted**

### G3 routes
- Unquarantined `e__playa-del-carmen…cozumel…` and rebound to real BP ids
- Corrected `from_city_id` / `to_city_id` on Playa↔Cozumel `ics-*` routes
- Marquee spine bound into DiDi `mexico-caribbean` + `mexico-pacific` featured_routes + phases

## Route-ID spine for L3 bind

Machine-readable: `MEXICO-ROUTE-SPINE-FOR-TASKLET-2026-07-09.json`

### mexico-caribbean (priority)
- **`ics-413f51cd44`** — Puerto Juárez ↔ Isla Mujeres · 5.27 nm · current_scheduled
  - demand hint: {"geography": "Puerto Juárez–Isla Mujeres", "passenger_movements_2025_approx": 5460000, "note": "APIQ/operator series — Tasklet must set directional one-way + fare mix before model use", "model_use": 
- **`ics-dd1d814699`** — Playa del Carmen ↔ Cozumel (Ultramar/Winjet) · 9.53 nm · current_scheduled
  - demand hint: {"geography": "Playa del Carmen–Cozumel", "passenger_movements_2025_approx": 3850000, "departures_2025": 27920, "fare_mxn_one_way_observed": {"ultramar_premium_plus": 320, "winjet_from_playa": 335}, "
- **`ics-03e3853317`** — Cancún Ultramar ↔ Isla Mujeres · 5.49 nm · current_scheduled
- **`ics-aa6ff40d2d`** — Punta Sam ↔ Isla Mujeres (car ferry) · 3.35 nm · current_scheduled

### mexico-pacific (priority)
- **`ics-89a8844858`** — Puerto Vallarta / Los Muertos → Yelapa · 14.5 nm · current_water_taxi_evidence
- **`ics-de6758216f`** — Puerto Vallarta → Punta de Mita · 9.9 nm · future_opportunity
- **`ics-db0930d9d1`** — Cabo San Lucas Marina → Puerto Los Cabos / SJC · 17.0 nm · future_opportunity
- **`ics-b5861451fb`** — Palmilla → San José del Cabo Marina · 3.4 nm · future_opportunity

## Tasklet T3 checklist

1. **Source** `corridor_annual_oneway_pax` + `comparable_fare_usd_pax` per spine `route_id` (directional one-way; never put port_total on a single route 1:1 without allocation note).
2. **Country-reference** Mexico opex row if missing (no Singapore silent fallback).
3. Build finance markets as **geography keys**, not catch-all `didi`:
   - `mexico-caribbean` (partner=`didi`)
   - `mexico-pacific` (partner=`didi`)
   - Spine route_ids must match this handoff exactly (finance-corridor inheritance).
4. Run aggregate → growth → frontend splice → partner JSON.
5. Update live Sheet; confirm model ↔ Sheet agree.
6. Hand back to Grok for **G4** economics sidecar + partner reseal + Gate G.

## Blockers still open (honest)

- Directional split + fare yield mix for Isla Mujeres (~5.46M movements) and Cozumel (~3.85M / 27,920 deps).
- Pacific water-taxi annual ridership (Yelapa etc.) unpublished — null beats guess.
- La Paz / Mazatlán / Acapulco candidates need registry cities + BPs (not in this seal).
- Chile / Argentina still registry-gap (Wave C).

## Files

- `G2-G3-SEAL-RECEIPT-2026-07-09.json`
- `MEXICO-ROUTE-SPINE-FOR-TASKLET-2026-07-09.json`
- Research inputs under same directory (L3 sourcing, BP briefs).

