# GROK SPEC — Auckland Ferries (Auckland Transport) domestic routing seal (2026-07-01)

**Authority:** Auckland Transport (AT), the Auckland Council transport authority
**Region:** Oceania · **Country:** New Zealand
**Anchor city id:** `auckland-new-zealand`
**Home waters:** the Waitematā Harbour and inner Hauraki Gulf
**Partner file:** `partner-pitch/partners/auckland-ferries.json` (mirror in `data-clean/partners/auckland-ferries.json`)
**Dossier:** `handoff/partner-map-model/PTA-DOSSIER-auckland-ferries.json`

## Mandate (Tasklet's lane is done; this is your seal lane)
Tasklet has authored the partner page narrative, the sourced domestic boarding points, the
honest-null domestic corridors (`route_id: null` + `_link_status: "geometry_seal_pending"`), and the
honest-pending economics (empty revenue/phase ladders + qualitative public-value levers). Your lane:
seal the geometry and regenerate the economics magnitudes against the sealed network.

## City node (already anchored)
`auckland-new-zealand` already has a city brief at `data-clean/city_briefs/auckland-new-zealand.json`.
ID-match / seal the boarding points below into that city and build the routes.

## Boarding points to seal (anchor coords are approximate — snap to real piers/terminals)

| node | name | anchor [lng,lat] | type |
|---|---|---|---|
| `akl-downtown` | Downtown (City Ferry Terminal) | [174.768, -36.843] | core_live_station |
| `akl-devonport` | Devonport | [174.795, -36.833] | core_live_station |
| `akl-bayswater` | Bayswater | [174.777, -36.82] | core_live_station |
| `akl-birkenhead` | Birkenhead | [174.73, -36.813] | core_live_station |
| `akl-beach-haven` | Beach Haven | [174.696, -36.796] | core_live_station |
| `akl-northcote` | Northcote Point (Te Onewa) | [174.743, -36.82] | core_live_station |
| `akl-hobsonville` | Hobsonville Point | [174.661, -36.795] | core_live_station |
| `akl-west-harbour` | West Harbour | [174.63, -36.82] | core_live_station |
| `akl-half-moon-bay` | Half Moon Bay | [174.9, -36.88] | core_live_station |
| `akl-pine-harbour` | Pine Harbour | [174.92, -36.89] | core_live_station |
| `akl-gulf-harbour` | Gulf Harbour | [174.787, -36.625] | core_live_station |
| `akl-waiheke` | Waiheke (Matiatia) | [175.083, -36.783] | core_live_station |
| `akl-stanley-bay` | Stanley Bay | [174.79, -36.827] | core_live_station |
| `akl-rakino` | Rakino Island | [174.95, -36.73] | core_live_station |

Total: **14** boarding points (14 core live, 0 committed, 0 study).

## Domestic corridors to seal (route the marked channels; interior_land_km == 0)

| pair_id | from | to | ~nm | rationale |
|---|---|---|---|---|
| `akl-1` | Downtown (City Ferry Terminal) | Devonport | 1 | Auckland's busiest harbour commuter line. |
| `akl-2` | Downtown (City Ferry Terminal) | Half Moon Bay | 6 | Eastern-suburbs commuter run across the Waitematā. |
| `akl-3` | Downtown (City Ferry Terminal) | Hobsonville Point | 7 | Upper-harbour commuter line to the fast-growing northwest. |
| `akl-4` | Downtown (City Ferry Terminal) | Gulf Harbour | 12 | Whangaparaōa peninsula commuter line. |
| `akl-5` | Downtown (City Ferry Terminal) | Waiheke (Matiatia) | 9 | The busy Waiheke Island line. |
| `akl-6` | Downtown (City Ferry Terminal) | Bayswater | 2 | North-shore commuter hop. |
| `akl-7` | Downtown (City Ferry Terminal) | Birkenhead | 2 | North-shore line via Birkenhead and Northcote. |
| `akl-8` | Half Moon Bay | Pine Harbour | 3 | Southeastern commuter link. |
| `akl-9` | Downtown (City Ferry Terminal) | Beach Haven | 4 | Upper-harbour line to Beach Haven. |

Total: **9** domestic corridors. Each is `route_id: null` in the partner file;
seal them, then write the gold `route_id`s back and flip `_link_status` to sealed.

## Routing hazards — hand-waypoints required (NO land crossings)

- **Hauraki Gulf Marine Park** — Much of the Gulf is a marine park with marine-mammal protections — speed and wake limits and seasonal routing apply; flag legs crossing sanctuary zones.
- **Harbour Bridge & shipping channel** — The Waitematā shipping channel and Harbour Bridge piers sit in the route — waypoint clear and cross the channel at marked points.
- **Tidal sandbanks** — The upper harbour (Hobsonville, Beach Haven) and eastern beaches have tidal sandbanks — follow the marked channels.
- **Ferry Basin congestion** — Downtown Ferry Basin is busy with multiple operators — low-wake, geofenced no-foil zones at the terminal.

Domestic-only network across the Waitematā Harbour and inner Hauraki Gulf. Outer-Gulf and Coromandel links are secondary and out of scope for this phase.

## Economics regeneration (your lane, post-seal)
- Build the route-keyed econ sidecar against the **sealed** network.
- Regenerate `growth_case.revenue_potential.rungs` + `phase_economics.horizons` from the sealed
  corridors, per `handoff/partner-map-model/PTA-ECONOMICS-CONVENTION.md` (operating/fare + public-value,
  **not** SOM/SAM/TAM/GMV super-app language).
- Replace the qualitative `public_value.levers` with quantified figures (CO2 t/yr, road-trips relieved,
  minutes saved) + a fares/operating-model table.

## Acceptance
- 0 land crossings (post-waypoint); 0 orphan routes; every sealed BP carries a source id.
- All 9 corridors sealed with gold `route_id`s; `_link_status` flipped from `geometry_seal_pending`.
- Economics regenerated against the sealed network under the PTA economics convention.

---
_Authored by Tasklet · 2026-07-01 · PTA batch 5 · Bahrain MOTC gold pattern._
