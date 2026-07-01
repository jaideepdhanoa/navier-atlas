# GROK SPEC — San Francisco Bay Ferry domestic routing seal (2026-06-30)

**Authority:** San Francisco Bay Area Water Emergency Transportation Authority (WETA), trading as San Francisco Bay Ferry
**Region:** North America · **Country:** United States
**Anchor city id:** `san-francisco-bay-area-usa`
**Home waters:** San Francisco Bay
**Partner file:** `partner-pitch/partners/sf-bay-ferry.json` (mirror in `data-clean/partners/sf-bay-ferry.json`)
**Dossier:** `handoff/partner-map-model/PTA-DOSSIER-sf-bay-ferry.json`

## Mandate (Tasklet's lane is done; this is your seal lane)
Tasklet has authored the partner page narrative, the sourced domestic boarding points, the
honest-null domestic corridors (`route_id: null` + `_link_status: "geometry_seal_pending"`), and the
honest-pending economics (empty revenue/phase ladders + qualitative public-value levers). Your lane:
seal the geometry and regenerate the economics magnitudes against the sealed network.

## City node (already anchored)
`san-francisco-bay-area-usa` already has a city brief at `data-clean/city_briefs/san-francisco-bay-area-usa.json`.
**ID-match note:** CLUSTERS currently carries `san-francisco-bay-usa` while the city brief is
`san-francisco-bay-area-usa`. Bind by ID-match to the existing node; do **not** mint a divergent
city. Null-beats-wrong — if the alias can't be resolved cleanly, flag it rather than guess.
ID-match / seal the boarding points below into that city and build the routes.

## Boarding points to seal (anchor coords are approximate — snap to real piers/terminals)

| node | name | anchor [lng,lat] | type |
|---|---|---|---|
| `sfbf-ferry-building` | San Francisco Ferry Building | [-122.3933, 37.7955] | core_live_station |
| `sfbf-pier-41` | San Francisco – Pier 41 | [-122.4169, 37.8088] | core_live_station |
| `sfbf-oakland` | Oakland – Jack London Square | [-122.2776, 37.7945] | core_live_station |
| `sfbf-alameda-main` | Alameda – Main Street | [-122.2792, 37.7906] | core_live_station |
| `sfbf-alameda-seaplane` | Alameda – Seaplane Lagoon | [-122.3015, 37.7855] | core_live_station |
| `sfbf-harbor-bay` | Harbor Bay (Bay Farm Island) | [-122.253, 37.735] | core_live_station |
| `sfbf-richmond` | Richmond Ferry Terminal | [-122.354, 37.911] | core_live_station |
| `sfbf-south-sf` | South San Francisco (Oyster Point) | [-122.376, 37.665] | core_live_station |
| `sfbf-vallejo` | Vallejo Ferry Terminal | [-122.273, 38.099] | core_live_station |
| `sfbf-mare-island` | Mare Island | [-122.269, 38.096] | core_live_station |
| `sfbf-mission-bay` | Mission Bay (16th St / China Basin) | [-122.387, 37.77] | committed_station |
| `sfbf-treasure-island` | Treasure Island | [-122.37, 37.82] | committed_station |
| `sfbf-berkeley` | Berkeley Marina | [-122.318, 37.865] | committed_station |
| `sfbf-redwood-city` | Port of Redwood City | [-122.21, 37.505] | committed_station |
| `sfbf-antioch` | Antioch | [-121.815, 38.015] | study_station |
| `sfbf-hercules` | Hercules | [-122.29, 38.017] | study_station |
| `sfbf-martinez` | Martinez | [-122.141, 38.029] | study_station |

Total: **17** boarding points (10 core live, 4 committed, 3 study).

## Domestic corridors to seal (route the marked channels; interior_land_km == 0)

| pair_id | from | to | ~nm | rationale |
|---|---|---|---|---|
| `sfbf-d01` | San Francisco Ferry Building | Oakland – Jack London Square | 4.0 | The flagship East Bay commute crossing — the Ferry Building to Jack London Square, Oakland; a fast passenger-only foiling layer above the busiest route. |
| `sfbf-d02` | San Francisco Ferry Building | Alameda – Main Street | 4.3 | Ferry Building to Alameda Main Street — a heavy commute crossing into the Island City. |
| `sfbf-d03` | San Francisco Ferry Building | Richmond Ferry Terminal | 9.5 | Ferry Building to Richmond across the central Bay — a long commute crossing where a fast foiling boat cuts the time sharply. |
| `sfbf-d04` | San Francisco Ferry Building | Vallejo Ferry Terminal | 22.0 | Ferry Building to Vallejo up San Pablo Bay and the Carquinez approach — the longest mainline commute run, ideal for the fast tier. |
| `sfbf-d05` | San Francisco Ferry Building | Harbor Bay (Bay Farm Island) | 5.0 | Ferry Building to Harbor Bay on Bay Farm Island — a dense peninsula commute leg. |
| `sfbf-d06` | San Francisco Ferry Building | Alameda – Seaplane Lagoon | 4.6 | Ferry Building to the Alameda Seaplane Lagoon — the newest commute landing on the south Alameda shore. |
| `sfbf-d07` | San Francisco Ferry Building | South San Francisco (Oyster Point) | 9.0 | Ferry Building to South San Francisco (Oyster Point) — the biotech-corridor commute down the western shore. |
| `sfbf-d08` | San Francisco Ferry Building | Mission Bay (16th St / China Basin) | 1.5 | Ferry Building to the committed Mission Bay landing — a short, very high-frequency hop serving Chase Center and the new waterfront. |
| `sfbf-d09` | San Francisco Ferry Building | Treasure Island | 2.4 | Ferry Building to the committed Treasure Island landing — a short central-Bay hop for the growing island community. |
| `sfbf-d10` | Oakland – Jack London Square | South San Francisco (Oyster Point) | 8.5 | Oakland to South San Francisco across the Bay — an east–west cross-Bay commute link. |

Total: **10** domestic corridors. Each is `route_id: null` in the partner file;
seal them, then write the gold `route_id`s back and flip `_link_status` to sealed.

## Routing hazards — hand-waypoints required (NO land crossings)

- **Golden Gate & Central Bay currents and swell** — The Golden Gate runs strong reversing tidal currents and ocean swell at the mouth; hand-waypoint the marked channels and manage set and chop on the central-Bay crossings.
- **Deep-draft shipping lanes & VTS** — San Francisco Bay carries deep-draft commercial traffic to the Port of Oakland and the refineries under Coast Guard Vessel Traffic Service; respect the traffic-separation scheme and cross lanes at right angles.
- **Bridge piers** — The Bay Bridge, Richmond–San Rafael and San Mateo–Hayward bridges have pier fields; route through the marked navigation spans, never across the pier lines.
- **Shallow South Bay & San Bruno Shoal** — The South Bay approaches to South San Francisco and Redwood City are shoal; hand-waypoint the dredged channels and account for tide height.
- **Carquinez Strait current** — The Vallejo and Mare Island legs run up San Pablo Bay into the Carquinez Strait, which runs a strong tidal current; route the marked channel.
- **Fog & wake limits** — Summer fog reduces visibility across the central Bay; strict low-wake operation is required near the marinas, the Ferry Building basin and the estuary terminals.

WETA's network is entirely domestic within San Francisco Bay and the Sacramento–San Joaquin Delta approaches. There are no international legs — the whole proposal is domestic.

## Economics regeneration (your lane, post-seal)
- Build the route-keyed econ sidecar against the **sealed** network.
- Regenerate `growth_case.revenue_potential.rungs` + `phase_economics.horizons` from the sealed
  corridors, per `handoff/partner-map-model/PTA-ECONOMICS-CONVENTION.md` (operating/fare + public-value,
  **not** SOM/SAM/TAM/GMV super-app language).
- Replace the qualitative `public_value.levers` with quantified figures (CO2 t/yr, road-trips relieved,
  minutes saved) + a fares/operating-model table.

## Acceptance
- 0 land crossings (post-waypoint); 0 orphan routes; every sealed BP carries a source id.
- All 10 corridors sealed with gold `route_id`s; `_link_status` flipped from `geometry_seal_pending`.
- Economics regenerated against the sealed network under the PTA economics convention.

---
_Authored by Tasklet · 2026-06-30 · PTA batch 4 · Bahrain MOTC gold pattern._
