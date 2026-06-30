# GROK SPEC — Hamburg Harbour Ferries (HADAG) domestic routing seal (2026-07-01)

**Authority:** HADAG Seetouristik und Fährdienst AG, the City of Hamburg harbour-ferry operator within the HVV
**Region:** Europe · **Country:** Germany
**Anchor city id:** `hamburg-germany`
**Home waters:** the Port of Hamburg and the lower Elbe
**Partner file:** `partner-pitch/partners/hamburg-hadag.json` (mirror in `data-clean/partners/hamburg-hadag.json`)
**Dossier:** `handoff/partner-map-model/PTA-DOSSIER-hamburg-hadag.json`

## Mandate (Tasklet's lane is done; this is your seal lane)
Tasklet has authored the partner page narrative, the sourced domestic boarding points, the
honest-null domestic corridors (`route_id: null` + `_link_status: "geometry_seal_pending"`), and the
honest-pending economics (empty revenue/phase ladders + qualitative public-value levers). Your lane:
seal the geometry and regenerate the economics magnitudes against the sealed network.

## ⚠ NEW GEOGRAPHY — Tasklet seeded the city anchor; reconcile & seal
`hamburg-germany` is **net-new** geography. Tasklet has **seeded** it so the build resolves:
- A `priority_city` feature `hamburg-germany` is minted in `data-clean/FEATURES_BY_TYPE.json` (anchor near the city centre on the water, ~[9.969, 53.546]), tagged `_seed_node` + provenance.
- A **new cluster** `germany` (region **Europe**) is added in `data-clean/CLUSTERS.json` with `hamburg-germany` as its first member (`members_present: 1`).
- A gold city brief ships at `data-clean/city_briefs/hamburg-germany.json` (mirror in `partner-pitch/`).

**Your job:** verify the seed anchor against the real city centre, snap it precisely, promote it into
the region index / map card layer if anything beyond CLUSTERS is needed, then ID-match / seal the
boarding points below and build the routes. Null-beats-wrong — if anything can't be reconciled cleanly,
flag it rather than guess.

## Boarding points to seal (anchor coords are approximate — snap to real piers/terminals)

| node | name | anchor [lng,lat] | type |
|---|---|---|---|
| `ham-landungsbrucken` | Landungsbrücken | [9.969, 53.546] | core_live_station |
| `ham-altona` | Altona (Fischmarkt) | [9.946, 53.5455] | core_live_station |
| `ham-dockland` | Dockland (Fischereihafen) | [9.937, 53.545] | core_live_station |
| `ham-neumuhlen` | Neumühlen / Övelgönne | [9.913, 53.544] | core_live_station |
| `ham-teufelsbruck` | Teufelsbrück | [9.84, 53.55] | core_live_station |
| `ham-finkenwerder` | Finkenwerder | [9.872, 53.535] | core_live_station |
| `ham-neuhof` | Neuhof | [9.955, 53.523] | core_live_station |
| `ham-elbphilharmonie` | Elbphilharmonie | [9.984, 53.541] | core_live_station |
| `ham-arningstrasse` | Arningstraße | [9.997, 53.53] | core_live_station |
| `ham-ernst-august` | Ernst-August-Schleuse | [10.008, 53.505] | core_live_station |
| `ham-steinwerder` | Steinwerder | [9.958, 53.534] | core_live_station |
| `ham-argentinienbrucke` | Argentinienbrücke | [9.974, 53.523] | core_live_station |
| `ham-bubendey-ufer` | Bubendey-Ufer | [9.887, 53.529] | core_live_station |
| `ham-blankenese` | Blankenese | [9.798, 53.557] | core_live_station |
| `ham-ruschpark` | Rüschpark | [9.852, 53.536] | core_live_station |
| `ham-waltershof` | Waltershof | [9.91, 53.523] | core_live_station |

Total: **16** boarding points (16 core live, 0 committed, 0 study).

## Domestic corridors to seal (route the marked channels; interior_land_km == 0)

| pair_id | from | to | ~nm | rationale |
|---|---|---|---|---|
| `ham-1` | Landungsbrücken | Finkenwerder | 3 | HADAG line 62 — the busiest harbour ferry line, central piers to Finkenwerder. |
| `ham-2` | Landungsbrücken | Neuhof | 3 | Line 73 south-bank harbour line to the working port. |
| `ham-3` | Landungsbrücken | Altona (Fischmarkt) | 2 | Central waterfront line to Altona / Fischmarkt. |
| `ham-4` | Finkenwerder | Teufelsbrück | 1 | Cross-Elbe line linking Finkenwerder to the north bank (Airbus commuters). |
| `ham-5` | Landungsbrücken | Blankenese | 5 | Western Elbe line to the Blankenese village. |
| `ham-6` | Blankenese | Rüschpark | 2 | Cross-Elbe link to the Rüschpark / Airbus side. |
| `ham-7` | Landungsbrücken | Elbphilharmonie | 1 | HafenCity waterfront line to the Elbphilharmonie. |
| `ham-8` | Elbphilharmonie | Arningstraße | 1 | HafenCity / east-harbour line. |
| `ham-9` | Landungsbrücken | Steinwerder | 1 | Cross-harbour line to the Steinwerder theatre and port. |

Total: **9** domestic corridors. Each is `route_id: null` in the partner file;
seal them, then write the gold `route_id`s back and flip `_link_status` to sealed.

## Routing hazards — hand-waypoints required (NO land crossings)

- **Port of Hamburg working traffic** — Hamburg is one of Europe's largest container ports — the Elbe fairway is busy with container ships and feeders; cross at marked points and waypoint clear of terminals and turning basins.
- **Strong tidal Elbe currents** — The tidal Elbe runs strong currents and the fairway shifts with dredging — follow the marked navigation channel.
- **Bridge & lock structures** — The Köhlbrand crossing, harbour locks (Ernst-August-Schleuse) and bridge piers require hand-waypointing.
- **Residential no-wake reaches** — The western Elbe (Övelgönne, Blankenese) is residential with strict wake limits — no-foil zones near the beaches and landings.

Domestic-only network across the Port of Hamburg and the lower Elbe. Any down-Elbe links toward Stade/Cuxhaven are secondary and out of scope for this phase.

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
- `hamburg-germany` reconciled/snapped, in CLUSTERS + region index, partner view resolves.
- Economics regenerated against the sealed network under the PTA economics convention.

---
_Authored by Tasklet · 2026-07-01 · PTA batch 5 · Bahrain MOTC gold pattern._
