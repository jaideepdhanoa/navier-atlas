# DiDi Mexico registry expansion status — La Paz, Mazatlán, Acapulco

**As of:** 2026-07-09  
**Status:** Research complete; registry, exact-BP geometry and finance gates remain.

## Atlas baseline

- Read `/tmp/navier-atlas` main at `749b10b7e269000c54ceaf9fbc8feb73e2967da3`; Mexico G2/G3 seal commit `56b570c2` is present.
- Exact structured checks of `CLUSTERS.json`, `ROUTES.json`, `FEATURES_BY_TYPE.json`, city briefs, matching boarding-point files and DiDi `_map_scope` found **no canonical city ID or alias, BP, city brief, or route ID** for La Paz, Mazatlán or Acapulco.
- The current DiDi Mexico-Pacific narrative mentions a future trunk toward La Paz, but La Paz is not registry/BP-bound.

## Verified findings

- Official DiDi Mexico city pages provide **exact-city operating evidence for all 3 cities**; this is stronger than country-only support.
- **Pichilingue** is a verified passenger ferry terminal. APIBCS publishes `24°16′08″N, 110°19′39″W` and confirms regular La Paz–Mazatlán service.
- **Mazatlán ferry terminal** is verified by ASIPONA documents and its 2025 monthly route-traffic workbooks.
- Official 2025 ASIPONA workbooks sum to:
  - La Paz→Mazatlán entries: **49,714 passenger movements** (42,000 Baja Ferries; 7,714 Transportación Marítima de California).
  - Mazatlán→La Paz exits: **52,544 passenger movements** (43,786; 8,758).
  - These are incumbent long-distance ferry observations, **not 1:1 Navier demand**.
- Baja Ferries' live pages show 3 service days per direction and an adult La Paz–Mazatlán tariff snapshot of **MXN 2,150**; neither page states an effective date.
- Municipal/official evidence supports the local water opportunities **Mazatlán–Isla de la Piedra** and **Caleta–Isla de la Roqueta**, but exact opposite landings, coordinates, fares, schedules and pax remain unresolved.

## Route and geometry gates

- All proposed `route_id` values remain `null`; no exact `ROUTES.json` match exists.
- La Paz–Mazatlán and Mazatlán–Puerto Bellato require long-range/offshore study; no Pioneer II assumption.
- Los Cabos–La Paz remains future-only and must be hand-routed around the East Cape; a straight segment can cross the Baja peninsula.
- Isla de la Piedra is a peninsula. Its local crossing and the Caleta–Roqueta route both require exact landing confirmation and chart-safe hand waypoints.

## Canonical brief maturity

- `data-clean/cluster_briefs/mexico.json` is already `first-class` for its current three-resort scope, so it should be **enhanced, not replaced**.
- It omits all three audited cities; has no standalone city briefs for them; and needs official city/port/operator sources, incumbent-ferry non-transferability language, and explicit range/hand-waypoint gates.
- Canonical copy must remain partner-neutral. DiDi-specific framing is isolated in `partner_narrative_notes` in the JSON artifact.

## Counts

- Cities audited: **3**; canonical matches: **0**; exact-city DiDi proofs: **3**.
- BP records: **9** — 5 verified facilities/names, 3 confirmation candidates, 1 non-BP POI.
- Corridors: **5** — 4 with current route/crossing evidence, 1 future-only; matched route IDs: **0**.
- Sources: **17**; unresolved gaps: **8**.

## Artifacts and validation

- JSON: `/tasklet/agent/home/didi-ex-china-audit/mexico/DIDI-MEXICO-LA-PAZ-MAZATLAN-ACAPULCO-REGISTRY-2026-07-09.json`
- This status: `/tasklet/agent/home/didi-ex-china-audit/mexico/DIDI-MEXICO-LA-PAZ-MAZATLAN-ACAPULCO-STATUS-2026-07-09.md`
- JSON validation: `python3 -m json.tool` — **passed**.
- Repository was not edited.
