# GROK SPEC — Brisbane CityCat domestic routing seal (2026-06-30)

**Authority:** Brisbane City Council ferry services (CityCat / CityHopper / Cross River), operated under Translink
**Region:** Oceania · **Country:** Australia
**Anchor city id:** `brisbane-australia`
**Home waters:** the Brisbane River
**Partner file:** `partner-pitch/partners/brisbane-citycat.json` (mirror in `data-clean/partners/brisbane-citycat.json`)
**Dossier:** `handoff/partner-map-model/PTA-DOSSIER-brisbane-citycat.json`

## Mandate (Tasklet's lane is done; this is your seal lane)
Tasklet has authored the partner page narrative, the sourced domestic boarding points, the
honest-null domestic corridors (`route_id: null` + `_link_status: "geometry_seal_pending"`), and the
honest-pending economics (empty revenue/phase ladders + qualitative public-value levers). Your lane:
seal the geometry and regenerate the economics magnitudes against the sealed network.

## ⚠ NEW GEOGRAPHY — Tasklet SEEDED the anchor; you reconcile + seal
`brisbane-australia` is **net-new**. Tasklet has already placed a **seed anchor** so the partner view and
map build resolves green today — your job is to reconcile/seal it, not mint from scratch:
1. ✅ **Done by Tasklet:** `brisbane-australia` added as a `priority_city` feature in
   `data-clean/FEATURES_BY_TYPE.json` (region **Oceania**, anchor ~[153.017, -27.473], `cluster_id: australia`,
   `coords_source: tasklet/pta-batch4-2026-06-30`, `_seed_node` flag). Registered as a member of the
   `australia` cluster in `CLUSTERS.json` (`members_present` bumped). A gold city brief ships at
   `data-clean/city_briefs/brisbane-australia.json` (mirrored in `partner-pitch/city_briefs/`).
2. **Your lane:** verify/snap the seed anchor coord, confirm region-index + nav-chip wiring, then drop the
   `_seed_node` flag once sealed.
3. Then ID-match / seal the boarding points below and build the routes.

## Boarding points to seal (anchor coords are approximate — snap to real piers/terminals)

| node | name | anchor [lng,lat] | type |
|---|---|---|---|
| `bcc-uq-st-lucia` | UQ St Lucia | [153.014, -27.499] | core_live_station |
| `bcc-west-end` | West End | [153.011, -27.4845] | core_live_station |
| `bcc-guyatt-park` | Guyatt Park | [153.008, -27.492] | core_live_station |
| `bcc-regatta` | Regatta | [152.999, -27.4815] | core_live_station |
| `bcc-milton` | Milton | [153.004, -27.472] | core_live_station |
| `bcc-north-quay` | North Quay | [153.019, -27.472] | core_live_station |
| `bcc-south-bank` | South Bank | [153.022, -27.476] | core_live_station |
| `bcc-maritime-museum` | Maritime Museum | [153.025, -27.481] | core_live_station |
| `bcc-qut-gardens-point` | QUT Gardens Point | [153.0285, -27.4775] | core_live_station |
| `bcc-riverside` | Riverside | [153.021, -27.466] | core_live_station |
| `bcc-holman-street` | Holman Street (Kangaroo Point) | [153.032, -27.472] | core_live_station |
| `bcc-thornton-street` | Thornton Street (Kangaroo Point) | [153.034, -27.476] | core_live_station |
| `bcc-dockside` | Dockside | [153.037, -27.473] | core_live_station |
| `bcc-sydney-street` | Sydney Street (New Farm) | [153.047, -27.466] | core_live_station |
| `bcc-mowbray-park` | Mowbray Park | [153.042, -27.481] | core_live_station |
| `bcc-new-farm-park` | New Farm Park | [153.049, -27.47] | core_live_station |
| `bcc-howard-smith` | Howard Smith Wharves | [153.032, -27.4625] | core_live_station |
| `bcc-hawthorne` | Hawthorne | [153.064, -27.4585] | core_live_station |
| `bcc-bulimba` | Bulimba | [153.057, -27.449] | core_live_station |
| `bcc-teneriffe` | Teneriffe | [153.047, -27.4555] | core_live_station |
| `bcc-bretts-wharf` | Bretts Wharf | [153.07, -27.443] | core_live_station |
| `bcc-apollo-road` | Apollo Road | [153.067, -27.44] | core_live_station |
| `bcc-northshore-hamilton` | Northshore Hamilton | [153.076, -27.438] | core_live_station |

Total: **23** boarding points (23 core live, 0 committed, 0 study).

## Domestic corridors to seal (route the marked channels; interior_land_km == 0)

| pair_id | from | to | ~nm | rationale |
|---|---|---|---|---|
| `bcc-d01` | UQ St Lucia | North Quay | 2.6 | The flagship campus-to-city run — UQ St Lucia up through West End to North Quay in the CBD. |
| `bcc-d02` | South Bank | Riverside | 1.0 | South Bank to Riverside — the busiest cultural-to-CBD cross-reach in the city centre. |
| `bcc-d03` | North Quay | Northshore Hamilton | 6.5 | The full river spine — North Quay through New Farm and Bulimba down to Northshore Hamilton. |
| `bcc-d04` | Riverside | Bulimba | 3.2 | Riverside to Bulimba — a heavy commute leg into the eastern suburbs. |
| `bcc-d05` | Holman Street (Kangaroo Point) | Riverside | 0.6 | Holman Street, Kangaroo Point, to Riverside — the CityHopper inner-city cross-river hop. |
| `bcc-d06` | Teneriffe | Bulimba | 0.7 | Teneriffe to Bulimba — the cross-river link between two riverside village precincts. |
| `bcc-d07` | New Farm Park | QUT Gardens Point | 2.4 | New Farm Park to QUT Gardens Point — a riverside-park-to-university commute leg. |
| `bcc-d08` | Hawthorne | North Quay | 4.4 | Hawthorne to North Quay — an eastern-suburb express commute into the city. |

Total: **8** domestic corridors. Each is `route_id: null` in the partner file;
seal them, then write the gold `route_id`s back and flip `_link_status` to sealed.

## Routing hazards — hand-waypoints required (NO land crossings)

- **Tight river meanders & strong tidal flow** — The Brisbane River winds in tight bends with a strong tidal stream; hand-waypoint the channel through every meander and account for the set on the bends.
- **Flood-debris risk** — After major floods (2011, 2022) the river carries logs and debris; routing must follow the maintained navigation channel and the council's post-flood advisories.
- **Low bridge clearances** — Victoria Bridge, the Go Between Bridge, William Jolly Bridge and the Story Bridge piers constrain the central reaches; route through the marked navigation spans with air-draft and pier clearance.
- **Shallow reaches & sandbars** — The upper (UQ / West End) and lower reaches have shoal edges and sandbars; hand-waypoint the dredged channel and account for tide height.
- **Wake-sensitive residential banks** — Long stretches of the river are lined with homes, pontoons and rowing clubs; strict low-wake operation and no-foil zones are required through the residential and rowing reaches.
- **Dense river traffic** — CityCats, CityHoppers, recreational craft and University rowing crews share the narrow river; geofence speed and give-way behaviour at the busy CBD and UQ reaches.

The CityCat network is entirely domestic on the Brisbane River. There are no international or open-sea legs — the whole proposal is domestic, inside sheltered river water.

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
- `brisbane-australia` minted, in CLUSTERS + region index, partner view resolves.
- Economics regenerated against the sealed network under the PTA economics convention.

---
_Authored by Tasklet · 2026-06-30 · PTA batch 4 · Bahrain MOTC gold pattern._
