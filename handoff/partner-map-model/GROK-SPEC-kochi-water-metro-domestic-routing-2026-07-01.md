# GROK SPEC — Kochi Water Metro (KMRL) domestic routing seal (2026-07-01)

**Authority:** Kochi Water Metro — Kochi Metro Rail Limited (KMRL), a Government of Kerala / Government of India joint venture
**Region:** South Asia · **Country:** India
**Anchor city id:** `kochi-india`
**Home waters:** the Kochi backwaters and Vembanad Lake
**Partner file:** `partner-pitch/partners/kochi-water-metro.json` (mirror in `data-clean/partners/kochi-water-metro.json`)
**Dossier:** `handoff/partner-map-model/PTA-DOSSIER-kochi-water-metro.json`

## Mandate (Tasklet's lane is done; this is your seal lane)
Tasklet has authored the partner page narrative, the sourced domestic boarding points, the
honest-null domestic corridors (`route_id: null` + `_link_status: "geometry_seal_pending"`), and the
honest-pending economics (empty revenue/phase ladders + qualitative public-value levers). Your lane:
seal the geometry and regenerate the economics magnitudes against the sealed network.

## ⚠ NEW GEOGRAPHY — Tasklet seeded the city anchor; reconcile & seal
`kochi-india` is **net-new** geography. Tasklet has **seeded** it so the build resolves:
- A `priority_city` feature `kochi-india` is minted in `data-clean/FEATURES_BY_TYPE.json` (anchor near the city centre on the water, ~[76.258, 9.958]), tagged `_seed_node` + provenance.
- `kochi-india` is registered into the existing **`india`** cluster in `data-clean/CLUSTERS.json` (`member_city_ids` + `members_present` bumped).
- A gold city brief ships at `data-clean/city_briefs/kochi-india.json` (mirror in `partner-pitch/`).

**Your job:** verify the seed anchor against the real city centre, snap it precisely, promote it into
the region index / map card layer if anything beyond CLUSTERS is needed, then ID-match / seal the
boarding points below and build the routes. Null-beats-wrong — if anything can't be reconciled cleanly,
flag it rather than guess.

## Boarding points to seal (anchor coords are approximate — snap to real piers/terminals)

| node | name | anchor [lng,lat] | type |
|---|---|---|---|
| `kch-high-court` | High Court (Ernakulam) | [76.278, 9.987] | core_live_station |
| `kch-vyttila` | Vyttila (mobility hub) | [76.318, 9.969] | core_live_station |
| `kch-vypin` | Vypin | [76.256, 9.97] | core_live_station |
| `kch-fort-kochi` | Fort Kochi | [76.242, 9.965] | core_live_station |
| `kch-south-chittoor` | South Chittoor | [76.295, 10.025] | core_live_station |
| `kch-cheranallur` | Cheranallur | [76.288, 10.042] | core_live_station |
| `kch-eloor` | Eloor | [76.292, 10.068] | core_live_station |
| `kch-willingdon-island` | Willingdon Island | [76.27, 9.956] | core_live_station |
| `kch-mattancherry` | Mattancherry | [76.258, 9.958] | core_live_station |
| `kch-kakkanad` | Kakkanad | [76.345, 10.013] | core_live_station |
| `kch-bolgatty` | Bolgatty | [76.272, 9.992] | committed_station |
| `kch-mulavukad-north` | Mulavukad North | [76.282, 10.008] | committed_station |
| `kch-infopark` | InfoPark | [76.352, 10.015] | committed_station |
| `kch-nettoor` | Nettoor | [76.318, 9.93] | committed_station |
| `kch-kumbalam` | Kumbalam | [76.31, 9.89] | committed_station |
| `kch-eroor` | Eroor | [76.335, 9.965] | committed_station |

Total: **16** boarding points (10 core live, 6 committed, 0 study).

## Domestic corridors to seal (route the marked channels; interior_land_km == 0)

| pair_id | from | to | ~nm | rationale |
|---|---|---|---|---|
| `kch-1` | High Court (Ernakulam) | Vypin | 1 | The first Water Metro line — Ernakulam High Court to Vypin across the backwaters. |
| `kch-2` | Vyttila (mobility hub) | Kakkanad | 3 | The Vyttila mobility-hub line to the Kakkanad IT corridor. |
| `kch-3` | High Court (Ernakulam) | Fort Kochi | 2 | Ernakulam to the Fort Kochi heritage island. |
| `kch-4` | High Court (Ernakulam) | South Chittoor | 3 | Northern backwater line to South Chittoor. |
| `kch-5` | South Chittoor | Cheranallur | 2 | Northern island link. |
| `kch-6` | Cheranallur | Eloor | 2 | Upper-backwater industrial line to Eloor. |
| `kch-7` | High Court (Ernakulam) | Willingdon Island | 2 | Ernakulam to Willingdon Island. |
| `kch-8` | Willingdon Island | Mattancherry | 1 | Island link to Mattancherry. |
| `kch-9` | Vyttila (mobility hub) | InfoPark | 4 | Extension from Vyttila to the InfoPark IT hub. |
| `kch-10` | High Court (Ernakulam) | Bolgatty | 1 | Short line to Bolgatty island. |

Total: **10** domestic corridors. Each is `route_id: null` in the partner file;
seal them, then write the gold `route_id`s back and flip `_link_status` to sealed.

## Routing hazards — hand-waypoints required (NO land crossings)

- **Backwater shallows & weed** — The Vembanad backwaters are shallow with shifting silt and seasonal water hyacinth — follow the dredged Water Metro channels and hand-waypoint around the shallows.
- **Ferry & country-boat traffic** — The backwaters carry dense local ferry and country-boat traffic — low-wake operation and geofenced no-foil zones at the jetties.
- **Shipping channel — Cochin Port** — The Ernakulam/Willingdon Island reach crosses the Cochin Port shipping channel — cross at marked points clear of large vessels.
- **Monsoon flows** — Backwater levels and currents swing sharply in the monsoon — routing must account for high-flow periods.

Domestic-only network across the Kochi backwaters and Vembanad Lake. Wider Kerala backwater links (Alappuzha/Kottayam) are secondary and out of scope for this phase.

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
- `kochi-india` reconciled/snapped, in CLUSTERS + region index, partner view resolves.
- Economics regenerated against the sealed network under the PTA economics convention.

---
_Authored by Tasklet · 2026-07-01 · PTA batch 5 · Bahrain MOTC gold pattern._
