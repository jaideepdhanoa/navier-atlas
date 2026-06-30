# GROK SPEC — Stockholm Archipelago Ferries (Waxholmsbolaget) domestic routing seal (2026-07-01)

**Authority:** Region Stockholm — Waxholms Ångfartygs AB (Waxholmsbolaget), the public archipelago ferry operator within SL
**Region:** Europe · **Country:** Sweden
**Anchor city id:** `stockholm-sweden`
**Home waters:** the Stockholm archipelago
**Partner file:** `partner-pitch/partners/stockholm-waxholm.json` (mirror in `data-clean/partners/stockholm-waxholm.json`)
**Dossier:** `handoff/partner-map-model/PTA-DOSSIER-stockholm-waxholm.json`

## Mandate (Tasklet's lane is done; this is your seal lane)
Tasklet has authored the partner page narrative, the sourced domestic boarding points, the
honest-null domestic corridors (`route_id: null` + `_link_status: "geometry_seal_pending"`), and the
honest-pending economics (empty revenue/phase ladders + qualitative public-value levers). Your lane:
seal the geometry and regenerate the economics magnitudes against the sealed network.

## City node (already anchored)
`stockholm-sweden` already has a city brief at `data-clean/city_briefs/stockholm-sweden.json`.
ID-match / seal the boarding points below into that city and build the routes.

## Boarding points to seal (anchor coords are approximate — snap to real piers/terminals)

| node | name | anchor [lng,lat] | type |
|---|---|---|---|
| `stk-stromkajen` | Strömkajen (central Stockholm) | [18.0786, 59.3293] | core_live_station |
| `stk-slussen` | Slussen | [18.0717, 59.3193] | core_live_station |
| `stk-nybroplan` | Nybroplan | [18.076, 59.332] | core_live_station |
| `stk-nacka-strand` | Nacka Strand | [18.16, 59.31] | core_live_station |
| `stk-frihamnen` | Frihamnen | [18.11, 59.34] | core_live_station |
| `stk-vaxholm` | Vaxholm | [18.3505, 59.402] | core_live_station |
| `stk-grinda` | Grinda | [18.587, 59.415] | core_live_station |
| `stk-stavsnas` | Stavsnäs | [18.6958, 59.284] | core_live_station |
| `stk-sandhamn` | Sandhamn | [18.907, 59.288] | core_live_station |
| `stk-moja` | Möja | [18.899, 59.392] | core_live_station |
| `stk-namdo` | Nämdö | [18.68, 59.22] | core_live_station |
| `stk-uto` | Utö | [18.29, 58.987] | core_live_station |
| `stk-ljustero` | Ljusterö (Linanäs) | [18.63, 59.52] | core_live_station |
| `stk-finnhamn` | Finnhamn | [18.82, 59.45] | core_live_station |
| `stk-gallno` | Gällnö | [18.69, 59.4] | core_live_station |
| `stk-tynningo` | Tynningö | [18.31, 59.37] | core_live_station |

Total: **16** boarding points (16 core live, 0 committed, 0 study).

## Domestic corridors to seal (route the marked channels; interior_land_km == 0)

| pair_id | from | to | ~nm | rationale |
|---|---|---|---|---|
| `stk-1` | Strömkajen (central Stockholm) | Vaxholm | 12 | Busiest commuter line (SL 83) — central Stockholm to the inner-archipelago town. |
| `stk-2` | Strömkajen (central Stockholm) | Nacka Strand | 6 | Sjövägen (line 80) commuter hop linking the inner-harbour districts. |
| `stk-3` | Frihamnen | Nybroplan | 4 | Inner-harbour commuter link across the central waterfront. |
| `stk-4` | Vaxholm | Grinda | 7 | Inner-archipelago island access beyond Vaxholm. |
| `stk-5` | Stavsnäs | Sandhamn | 9 | Gateway to the outer archipelago and the Sandhamn sailing hub. |
| `stk-6` | Strömkajen (central Stockholm) | Sandhamn | 28 | Direct central-Stockholm to outer-archipelago run. |
| `stk-7` | Vaxholm | Ljusterö (Linanäs) | 11 | Mid-archipelago island link north of Vaxholm. |
| `stk-8` | Grinda | Finnhamn | 8 | Outer-island hop across the middle archipelago. |
| `stk-9` | Stavsnäs | Nämdö | 10 | Southern archipelago island access. |
| `stk-10` | Vaxholm | Gällnö | 13 | Mid-archipelago link to the Gällnö nature-reserve islands. |
| `stk-11` | Strömkajen (central Stockholm) | Utö | 30 | Long southern-archipelago run to Utö. |

Total: **11** domestic corridors. Each is `route_id: null` in the partner file;
seal them, then write the gold `route_id`s back and flip `_link_status` to sealed.

## Routing hazards — hand-waypoints required (NO land crossings)

- **Shallow archipelago channels** — The archipelago is a maze of skerries, rocks and shallows — every leg must follow the marked deep-water fairways; hand-waypoint around skerries and reefs.
- **Winter ice** — Inner and middle archipelago routes ice over in winter; seasonal routing and ice-class limits apply — flag legs that need winter suspension.
- **Nature-reserve no-wake zones** — Several middle-archipelago islands sit in nature reserves with strict wake limits; no-foil zones near landings and reserve shorelines.
- **Central Stockholm harbour traffic** — Strömkajen/Slussen/Nybroplan are busy with sightseeing, commuter and Djurgården traffic — low-wake, geofenced no-foil zones in the inner harbour.

Domestic-only network across the Stockholm archipelago and inner waterways. Any future Åland/Baltic links are clearly secondary and out of scope for this phase.

## Economics regeneration (your lane, post-seal)
- Build the route-keyed econ sidecar against the **sealed** network.
- Regenerate `growth_case.revenue_potential.rungs` + `phase_economics.horizons` from the sealed
  corridors, per `handoff/partner-map-model/PTA-ECONOMICS-CONVENTION.md` (operating/fare + public-value,
  **not** SOM/SAM/TAM/GMV super-app language).
- Replace the qualitative `public_value.levers` with quantified figures (CO2 t/yr, road-trips relieved,
  minutes saved) + a fares/operating-model table.

## Acceptance
- 0 land crossings (post-waypoint); 0 orphan routes; every sealed BP carries a source id.
- All 11 corridors sealed with gold `route_id`s; `_link_status` flipped from `geometry_seal_pending`.
- Economics regenerated against the sealed network under the PTA economics convention.

---
_Authored by Tasklet · 2026-07-01 · PTA batch 5 · Bahrain MOTC gold pattern._
