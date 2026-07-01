# GROK SPEC — Lisbon Tagus Ferries (Transtejo / Soflusa) domestic routing seal (2026-07-01)

**Authority:** Transtejo & Soflusa (TTSL), the State-owned Tagus ferry operator
**Region:** Europe · **Country:** Portugal
**Anchor city id:** `lisbon-tagus-portugal`
**Home waters:** the Tagus estuary
**Partner file:** `partner-pitch/partners/lisbon-transtejo.json` (mirror in `data-clean/partners/lisbon-transtejo.json`)
**Dossier:** `handoff/partner-map-model/PTA-DOSSIER-lisbon-transtejo.json`

## Mandate (Tasklet's lane is done; this is your seal lane)
Tasklet has authored the partner page narrative, the sourced domestic boarding points, the
honest-null domestic corridors (`route_id: null` + `_link_status: "geometry_seal_pending"`), and the
honest-pending economics (empty revenue/phase ladders + qualitative public-value levers). Your lane:
seal the geometry and regenerate the economics magnitudes against the sealed network.

## City node (already anchored)
`lisbon-tagus-portugal` already has a city brief at `data-clean/city_briefs/lisbon-tagus-portugal.json`.
**ID-match note:** CLUSTERS/feature id is `lisbon-tagus-portugal` while the city brief's internal `city_id` is `lisbon-tagus`. Bind by ID-match to the existing `lisbon-tagus-portugal` node; do not mint a divergent city. Null-beats-wrong if the alias can't resolve cleanly.
ID-match / seal the boarding points below into that city and build the routes.

## Boarding points to seal (anchor coords are approximate — snap to real piers/terminals)

| node | name | anchor [lng,lat] | type |
|---|---|---|---|
| `lis-cais-sodre` | Cais do Sodré | [-9.1455, 38.7057] | core_live_station |
| `lis-terreiro-paco` | Terreiro do Paço | [-9.134, 38.7075] | core_live_station |
| `lis-belem` | Belém | [-9.203, 38.6955] | core_live_station |
| `lis-cacilhas` | Cacilhas | [-9.1495, 38.688] | core_live_station |
| `lis-seixal` | Seixal | [-9.1015, 38.64] | core_live_station |
| `lis-montijo` | Montijo | [-8.974, 38.705] | core_live_station |
| `lis-barreiro` | Barreiro | [-9.073, 38.662] | core_live_station |
| `lis-trafaria` | Trafaria | [-9.24, 38.668] | core_live_station |
| `lis-porto-brandao` | Porto Brandão | [-9.208, 38.677] | core_live_station |

Total: **9** boarding points (9 core live, 0 committed, 0 study).

## Domestic corridors to seal (route the marked channels; interior_land_km == 0)

| pair_id | from | to | ~nm | rationale |
|---|---|---|---|---|
| `lis-1` | Cais do Sodré | Cacilhas | 1 | The busiest Tagus crossing — central Lisbon to Cacilhas in minutes. |
| `lis-2` | Cais do Sodré | Seixal | 4 | Commuter line to the south-bank town of Seixal. |
| `lis-3` | Cais do Sodré | Montijo | 6 | Cross-estuary commuter run to Montijo. |
| `lis-4` | Terreiro do Paço | Barreiro | 4 | Soflusa commuter line to Barreiro and the rail interchange. |
| `lis-5` | Belém | Trafaria | 2 | West-Lisbon crossing to Trafaria on the south bank. |
| `lis-6` | Belém | Porto Brandão | 1 | Short west-Lisbon hop to Porto Brandão. |
| `lis-7` | Cais do Sodré | Belém | 4 | North-bank waterfront line linking central Lisbon to Belém. |
| `lis-8` | Trafaria | Porto Brandão | 1 | South-bank link between the two western terminals. |

Total: **8** domestic corridors. Each is `route_id: null` in the partner file;
seal them, then write the gold `route_id`s back and flip `_link_status` to sealed.

## Routing hazards — hand-waypoints required (NO land crossings)

- **Tagus tidal currents & sandbanks** — The estuary has strong tidal currents and shifting sandbanks (e.g. off Trafaria/Cova do Vapor) — follow the marked channels and hand-waypoint around the bars.
- **Bridge piers** — The 25 de Abril and Vasco da Gama bridge piers sit in the fairway — waypoint clear of the pier protection zones.
- **Port & cruise traffic** — Lisbon is a busy commercial and cruise port; cross the shipping channel at marked points with low-wake transit near terminals.
- **Estuary nature area** — The south-bank estuary reserves require low-wake operation near the shore and mudflats.

Domestic-only network across the Tagus estuary. No cross-border links in scope.

## Economics regeneration (your lane, post-seal)
- Build the route-keyed econ sidecar against the **sealed** network.
- Regenerate `growth_case.revenue_potential.rungs` + `phase_economics.horizons` from the sealed
  corridors, per `handoff/partner-map-model/PTA-ECONOMICS-CONVENTION.md` (operating/fare + public-value,
  **not** SOM/SAM/TAM/GMV super-app language).
- Replace the qualitative `public_value.levers` with quantified figures (CO2 t/yr, road-trips relieved,
  minutes saved) + a fares/operating-model table.

## Acceptance
- 0 land crossings (post-waypoint); 0 orphan routes; every sealed BP carries a source id.
- All 8 corridors sealed with gold `route_id`s; `_link_status` flipped from `geometry_seal_pending`.
- Economics regenerated against the sealed network under the PTA economics convention.

---
_Authored by Tasklet · 2026-07-01 · PTA batch 5 · Bahrain MOTC gold pattern._
