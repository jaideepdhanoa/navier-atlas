# GROK SPEC — Venice Vaporetto (ACTV) domestic routing seal (2026-06-30)

**Authority:** ACTV (Azienda del Consorzio Trasporti Veneziano), the AVM-group public-transport operator for the City of Venice
**Region:** Europe · **Country:** Italy
**Anchor city id:** `venice-italy`
**Home waters:** the Venetian Lagoon and the Grand Canal
**Partner file:** `partner-pitch/partners/venice-actv.json` (mirror in `data-clean/partners/venice-actv.json`)
**Dossier:** `handoff/partner-map-model/PTA-DOSSIER-venice-actv.json`

## Mandate (Tasklet's lane is done; this is your seal lane)
Tasklet has authored the partner page narrative, the sourced domestic boarding points, the
honest-null domestic corridors (`route_id: null` + `_link_status: "geometry_seal_pending"`), and the
honest-pending economics (empty revenue/phase ladders + qualitative public-value levers). Your lane:
seal the geometry and regenerate the economics magnitudes against the sealed network.

## City node (already anchored)
`venice-italy` already has a city brief at `data-clean/city_briefs/venice-italy.json`.
ID-match / seal the boarding points below into that city and build the routes.

## Boarding points to seal (anchor coords are approximate — snap to real piers/terminals)

| node | name | anchor [lng,lat] | type |
|---|---|---|---|
| `actv-piazzale-roma` | Piazzale Roma | [12.3185, 45.438] | core_live_station |
| `actv-ferrovia` | Ferrovia (Santa Lucia) | [12.321, 45.441] | core_live_station |
| `actv-rialto` | Rialto | [12.336, 45.438] | core_live_station |
| `actv-san-marco` | San Marco (Vallaresso) | [12.337, 45.432] | core_live_station |
| `actv-san-zaccaria` | San Zaccaria | [12.345, 45.433] | core_live_station |
| `actv-accademia` | Accademia | [12.3285, 45.4315] | core_live_station |
| `actv-ca-rezzonico` | Ca' Rezzonico | [12.327, 45.4335] | core_live_station |
| `actv-san-toma` | San Tomà | [12.326, 45.436] | core_live_station |
| `actv-ca-doro` | Ca' d'Oro | [12.334, 45.4405] | core_live_station |
| `actv-san-marcuola` | San Marcuola | [12.329, 45.443] | core_live_station |
| `actv-riva-de-biasio` | Riva de Biasio | [12.326, 45.442] | core_live_station |
| `actv-zattere` | Zattere | [12.326, 45.429] | core_live_station |
| `actv-giudecca-palanca` | Giudecca (Palanca) | [12.321, 45.4275] | core_live_station |
| `actv-san-giorgio` | San Giorgio Maggiore | [12.343, 45.429] | core_live_station |
| `actv-arsenale` | Arsenale | [12.351, 45.434] | core_live_station |
| `actv-giardini` | Giardini | [12.359, 45.4275] | core_live_station |
| `actv-santelena` | Sant'Elena | [12.364, 45.425] | core_live_station |
| `actv-lido-sme` | Lido (Santa Maria Elisabetta) | [12.369, 45.415] | core_live_station |
| `actv-fondamente-nove` | Fondamente Nove | [12.342, 45.445] | core_live_station |
| `actv-murano-faro` | Murano (Faro) | [12.354, 45.457] | core_live_station |
| `actv-burano` | Burano | [12.417, 45.4855] | core_live_station |
| `actv-torcello` | Torcello | [12.418, 45.497] | core_live_station |
| `actv-san-basilio` | San Basilio | [12.318, 45.429] | core_live_station |
| `actv-tronchetto` | Tronchetto | [12.301, 45.44] | core_live_station |
| `actv-sacca-fisola` | Sacca Fisola | [12.312, 45.428] | core_live_station |
| `actv-madonna-dellorto` | Madonna dell'Orto | [12.332, 45.4475] | core_live_station |

Total: **26** boarding points (26 core live, 0 committed, 0 study).

## Domestic corridors to seal (route the marked channels; interior_land_km == 0)

| pair_id | from | to | ~nm | rationale |
|---|---|---|---|---|
| `actv-d01` | Fondamente Nove | Murano (Faro) | 0.9 | Fondamente Nove to Murano across the open northern lagoon — the busiest island crossing, ideal for a quiet low-wake foiling hop. |
| `actv-d02` | Murano (Faro) | Burano | 3.1 | Murano to Burano across the lagoon — the long island run a fast, quiet boat transforms. |
| `actv-d03` | Burano | Torcello | 0.6 | Burano to Torcello — the short hop to the lagoon's oldest island. |
| `actv-d04` | San Zaccaria | Lido (Santa Maria Elisabetta) | 2.4 | San Zaccaria to the Lido across the San Marco basin — the city-to-beach crossing. |
| `actv-d05` | Fondamente Nove | Burano | 3.6 | Fondamente Nove direct to Burano across the northern lagoon — a fast quiet run on open water. |
| `actv-d06` | Tronchetto | Lido (Santa Maria Elisabetta) | 4.0 | Tronchetto to the Lido around the city — a car-terminal-to-island link on the lagoon edge. |
| `actv-d07` | San Marco (Vallaresso) | San Giorgio Maggiore | 0.3 | San Marco to San Giorgio Maggiore across the basin — the short island hop with the city's most famous view. |
| `actv-d08` | Lido (Santa Maria Elisabetta) | Sant'Elena | 1.6 | The Lido to Sant'Elena across the basin edge — an island-to-east-Venice link. |

Total: **8** domestic corridors. Each is `route_id: null` in the partner file;
seal them, then write the gold `route_id`s back and flip `_link_status` to sealed.

## Routing hazards — hand-waypoints required (NO land crossings)

- **Motondoso wake limits** — Venice enforces strict speed and wake limits to protect building foundations, banks and the lagoon ecology; the Grand Canal and inner canals are no-foil, low-speed only — foiling is used only on the open lagoon crossings.
- **Narrow congested canals** — The Grand Canal and inner canals are crowded with vaporetti, water taxis, delivery boats and gondolas; conventional low-speed handling and strict give-way only.
- **Shallow lagoon mudflats & marked channels** — The lagoon is shallow with mudflats (velme/barene) between marked channels staked by bricole; hand-waypoint the staked channels and never cut across the flats.
- **MOSE barriers & acqua alta** — The MOSE storm-surge barriers close the lagoon inlets during high tides; routing must respect barrier-closure status and the acqua alta tidal range.
- **Lido inlet exposure** — The Lido and Malamocco inlets open to the Adriatic with swell and current; manage exposure on the outer-edge legs.
- **Basin & commercial traffic** — The San Marco and Giudecca basins carry heavy public, commercial and (rerouted) large-vessel traffic; geofence speed and route clear of the working channels.

The vaporetto network is entirely domestic within the Venetian Lagoon. There are no international legs — the whole proposal is domestic, inside sheltered lagoon water.

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
_Authored by Tasklet · 2026-06-30 · PTA batch 4 · Bahrain MOTC gold pattern._
