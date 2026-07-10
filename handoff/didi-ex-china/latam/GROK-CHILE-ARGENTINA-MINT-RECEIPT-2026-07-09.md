# Chile + Argentina registry mint — Grok handback

**UTC:** 2026-07-10T03:28:26Z  
**Git commit:** `8c8884825318`  
**Approval:** Jaideep approval 2026-07-10: Tasklet suggestions + include cross-border  
**Status:** `registry_minted / routes_quarantined_pending_hand_waypoints / finance_not_run`

## Minted

- Clusters: `chile`, `argentina`, `uruguay`
- Cities: **21**
- Boarding points: **21**
- Routes: **10** (all quarantine/hide pending hand waypoints)

### Cross-border

- Included: Buenos Aires ↔ Colonia — `rn-04b92d6952d2`
- Marked international; not domestic-ready

### Explicitly not minted as passenger BP

- Muelle Blanco (service unproven)
- Muelle Prat kept as tourism pier only (`_not_route_demand_proof`)

## DiDi partner

- Markets added: `chile`, `argentina`
- Featured routes: **empty** until routes un-quarantine
- Aspirational journeys present (no route_id)

## Finance

- Cascade **not** run; annual one-way pax remain null

## Gates

- **gate_g:** PASS (exit 1)
- **inheritance_strict:** PASS (exit 0)
- **fidelity:** PASS (exit 0)

## Next

- Hand-route water-only geometries; re-run land-crossing QA
- Un-quarantine routes that pass geometry gates
- Then bind DiDi featured_routes to active set
- Tasklet: annual one-way pax + fares before finance cascade
- Verify DiDi service polygons for nearby ferry municipalities

Machine receipt: `handoff/didi-ex-china/latam/GROK-CHILE-ARGENTINA-MINT-RECEIPT-2026-07-09.json`

