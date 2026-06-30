# GROK SPEC — Boston Harbor Ferries (MBTA) domestic routing seal (2026-07-01)

**Authority:** Massachusetts Bay Transportation Authority (MBTA)
**Region:** North America · **Country:** United States
**Anchor city id:** `boston-new-england-usa`
**Home waters:** Boston Harbor and Massachusetts Bay
**Partner file:** `partner-pitch/partners/boston-mbta-ferry.json` (mirror in `data-clean/partners/boston-mbta-ferry.json`)
**Dossier:** `handoff/partner-map-model/PTA-DOSSIER-boston-mbta-ferry.json`

## Mandate (Tasklet's lane is done; this is your seal lane)
Tasklet has authored the partner page narrative, the sourced domestic boarding points, the
honest-null domestic corridors (`route_id: null` + `_link_status: "geometry_seal_pending"`), and the
honest-pending economics (empty revenue/phase ladders + qualitative public-value levers). Your lane:
seal the geometry and regenerate the economics magnitudes against the sealed network.

## City node (already anchored)
`boston-new-england-usa` already has a city brief at `data-clean/city_briefs/boston-new-england-usa.json`.
ID-match / seal the boarding points below into that city and build the routes.

## Boarding points to seal (anchor coords are approximate — snap to real piers/terminals)

| node | name | anchor [lng,lat] | type |
|---|---|---|---|
| `bos-long-wharf` | Long Wharf | [-71.05, 42.36] | core_live_station |
| `bos-rowes-wharf` | Rowes Wharf | [-71.051, 42.356] | core_live_station |
| `bos-charlestown` | Charlestown Navy Yard | [-71.054, 42.374] | core_live_station |
| `bos-east-boston` | East Boston (Lewis Mall) | [-71.039, 42.366] | core_live_station |
| `bos-hingham` | Hingham Shipyard | [-70.919, 42.256] | core_live_station |
| `bos-hull` | Hull (Pemberton Point) | [-70.921, 42.3] | core_live_station |
| `bos-lynn` | Lynn | [-70.945, 42.46] | core_live_station |
| `bos-winthrop` | Winthrop | [-70.983, 42.375] | core_live_station |
| `bos-quincy` | Quincy (Fore River) | [-70.97, 42.247] | core_live_station |
| `bos-logan` | Logan Airport ferry dock | [-71.025, 42.364] | core_live_station |
| `bos-seaport` | Seaport (Fan Pier) | [-71.043, 42.353] | study_station |

Total: **11** boarding points (10 core live, 0 committed, 1 study).

## Domestic corridors to seal (route the marked channels; interior_land_km == 0)

| pair_id | from | to | ~nm | rationale |
|---|---|---|---|---|
| `bos-1` | Long Wharf | Charlestown Navy Yard | 1 | The year-round Charlestown Navy Yard commuter line. |
| `bos-2` | Long Wharf | East Boston (Lewis Mall) | 1 | The East Boston (Lewis Mall) inner-harbor line. |
| `bos-3` | Long Wharf | Hingham Shipyard | 9 | The flagship Hingham commuter line down the South Shore. |
| `bos-4` | Long Wharf | Hull (Pemberton Point) | 7 | Hull (Pemberton Point) commuter line. |
| `bos-5` | Hingham Shipyard | Hull (Pemberton Point) | 3 | South Shore link between Hingham and Hull. |
| `bos-6` | Long Wharf | Winthrop | 4 | Winthrop outer-harbor line. |
| `bos-7` | Long Wharf | Lynn | 6 | North Shore line to Lynn. |
| `bos-8` | Long Wharf | Quincy (Fore River) | 6 | Quincy (Fore River) South Shore line. |
| `bos-9` | Long Wharf | Logan Airport ferry dock | 1 | Airport ferry link to Logan. |
| `bos-10` | Quincy (Fore River) | Logan Airport ferry dock | 6 | South Shore to airport via the harbor. |

Total: **10** domestic corridors. Each is `route_id: null` in the partner file;
seal them, then write the gold `route_id`s back and flip `_link_status` to sealed.

## Routing hazards — hand-waypoints required (NO land crossings)

- **Boston Harbor shipping channel** — The main shipping channel and Logan approach are busy with container, cruise and tanker traffic — cross at marked points; coordinate with the Logan ferry dock.
- **Harbor Islands & shoals** — Boston Harbor Islands and shoals (e.g. off Hull/Quincy) require hand-waypointing through the marked channels.
- **Logan Airport security zone** — The Logan ferry dock sits inside the airport security perimeter — routing must respect the marine exclusion zones.
- **Tidal flats — South Shore** — Hingham/Hull/Quincy approaches have tidal flats and narrow channels — follow the marked fairways at all tides.

Domestic-only network across Boston Harbor and the South/North Shore. Provincetown / Cape links are seasonal and secondary, out of scope for this phase.

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
_Authored by Tasklet · 2026-07-01 · PTA batch 5 · Bahrain MOTC gold pattern._
