# GROK SPEC — Vancouver SeaBus (TransLink) domestic routing seal (2026-07-01)

**Authority:** TransLink (South Coast British Columbia Transportation Authority)
**Region:** North America · **Country:** Canada
**Anchor city id:** `vancouver-canada`
**Home waters:** Burrard Inlet and the lower Fraser
**Partner file:** `partner-pitch/partners/vancouver-seabus.json` (mirror in `data-clean/partners/vancouver-seabus.json`)
**Dossier:** `handoff/partner-map-model/PTA-DOSSIER-vancouver-seabus.json`

## Mandate (Tasklet's lane is done; this is your seal lane)
Tasklet has authored the partner page narrative, the sourced domestic boarding points, the
honest-null domestic corridors (`route_id: null` + `_link_status: "geometry_seal_pending"`), and the
honest-pending economics (empty revenue/phase ladders + qualitative public-value levers). Your lane:
seal the geometry and regenerate the economics magnitudes against the sealed network.

## City node (already anchored)
`vancouver-canada` already has a city brief at `data-clean/city_briefs/vancouver-canada.json`.
ID-match / seal the boarding points below into that city and build the routes.

## Boarding points to seal (anchor coords are approximate — snap to real piers/terminals)

| node | name | anchor [lng,lat] | type |
|---|---|---|---|
| `yvr-waterfront` | Waterfront (downtown Vancouver) | [-123.1115, 49.286] | core_live_station |
| `yvr-lonsdale-quay` | Lonsdale Quay (North Vancouver) | [-123.073, 49.31] | core_live_station |
| `yvr-ambleside` | Ambleside (West Vancouver) | [-123.16, 49.327] | study_station |
| `yvr-maplewood` | Maplewood (North Vancouver) | [-123.02, 49.3] | study_station |
| `yvr-port-moody` | Port Moody (Rocky Point) | [-122.865, 49.288] | study_station |
| `yvr-new-westminster` | New Westminster Quay (Fraser) | [-122.91, 49.2] | study_station |

Total: **6** boarding points (2 core live, 0 committed, 4 study).

## Domestic corridors to seal (route the marked channels; interior_land_km == 0)

| pair_id | from | to | ~nm | rationale |
|---|---|---|---|---|
| `yvr-1` | Waterfront (downtown Vancouver) | Lonsdale Quay (North Vancouver) | 1 | The live SeaBus crossing — downtown to North Vancouver across Burrard Inlet. |
| `yvr-2` | Waterfront (downtown Vancouver) | Ambleside (West Vancouver) | 4 | New fast cross-inlet line to West Vancouver's Ambleside — a crossing the big SeaBus hulls don't serve. |
| `yvr-3` | Lonsdale Quay (North Vancouver) | Ambleside (West Vancouver) | 3 | North-shore waterfront link between Lonsdale and Ambleside. |
| `yvr-4` | Waterfront (downtown Vancouver) | Maplewood (North Vancouver) | 5 | East-inlet line to the North Vancouver employment lands. |
| `yvr-5` | Waterfront (downtown Vancouver) | Port Moody (Rocky Point) | 12 | Up-inlet commuter line to Port Moody at the head of Burrard Inlet. |
| `yvr-6` | Waterfront (downtown Vancouver) | New Westminster Quay (Fraser) | 14 | Fraser River line to New Westminster Quay. |

Total: **6** domestic corridors. Each is `route_id: null` in the partner file;
seal them, then write the gold `route_id`s back and flip `_link_status` to sealed.

## Routing hazards — hand-waypoints required (NO land crossings)

- **Burrard Inlet shipping channel** — Burrard Inlet is a major commercial port with tanker and bulk traffic — cross the shipping channel at marked points; waypoint clear of anchorages and the Second Narrows.
- **First/Second Narrows bridge piers** — The Lions Gate (First Narrows) and Ironworkers Memorial (Second Narrows) bridge piers and strong tidal currents at the narrows require hand-waypointing.
- **Fraser River currents & sandbars** — The Fraser has strong currents, log booms and shifting sandbars — follow the marked navigation channel.
- **Indian Arm / marine habitat** — Up-inlet routes pass sensitive habitat — low-wake operation near the shore.

Domestic-only network across Burrard Inlet and the lower Fraser. Sunshine Coast / Vancouver Island links are secondary and out of scope for this phase.

## Economics regeneration (your lane, post-seal)
- Build the route-keyed econ sidecar against the **sealed** network.
- Regenerate `growth_case.revenue_potential.rungs` + `phase_economics.horizons` from the sealed
  corridors, per `handoff/partner-map-model/PTA-ECONOMICS-CONVENTION.md` (operating/fare + public-value,
  **not** SOM/SAM/TAM/GMV super-app language).
- Replace the qualitative `public_value.levers` with quantified figures (CO2 t/yr, road-trips relieved,
  minutes saved) + a fares/operating-model table.

## Acceptance
- 0 land crossings (post-waypoint); 0 orphan routes; every sealed BP carries a source id.
- All 6 corridors sealed with gold `route_id`s; `_link_status` flipped from `geometry_seal_pending`.
- Economics regenerated against the sealed network under the PTA economics convention.

---
_Authored by Tasklet · 2026-07-01 · PTA batch 5 · Bahrain MOTC gold pattern._
