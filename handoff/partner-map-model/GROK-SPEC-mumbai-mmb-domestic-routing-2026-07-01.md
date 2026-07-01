# GROK SPEC — Mumbai Water Transport (Maharashtra Maritime Board) domestic routing seal (2026-07-01)

**Authority:** Maharashtra Maritime Board (MMB), the State maritime authority
**Region:** South Asia · **Country:** India
**Anchor city id:** `mumbai-india`
**Home waters:** Mumbai harbour, Thane creek and the Alibaug coast
**Partner file:** `partner-pitch/partners/mumbai-mmb.json` (mirror in `data-clean/partners/mumbai-mmb.json`)
**Dossier:** `handoff/partner-map-model/PTA-DOSSIER-mumbai-mmb.json`

## Mandate (Tasklet's lane is done; this is your seal lane)
Tasklet has authored the partner page narrative, the sourced domestic boarding points, the
honest-null domestic corridors (`route_id: null` + `_link_status: "geometry_seal_pending"`), and the
honest-pending economics (empty revenue/phase ladders + qualitative public-value levers). Your lane:
seal the geometry and regenerate the economics magnitudes against the sealed network.

## City node (already anchored)
`mumbai-india` already has a city brief at `data-clean/city_briefs/mumbai-india.json`.
ID-match / seal the boarding points below into that city and build the routes.

## Boarding points to seal (anchor coords are approximate — snap to real piers/terminals)

| node | name | anchor [lng,lat] | type |
|---|---|---|---|
| `mum-gateway` | Gateway of India | [72.8347, 18.922] | core_live_station |
| `mum-ferry-wharf` | Ferry Wharf (Bhaucha Dhakka) | [72.842, 18.956] | core_live_station |
| `mum-mandwa` | Mandwa (Alibaug) | [72.874, 18.806] | core_live_station |
| `mum-belapur` | Belapur (Navi Mumbai) | [73.035, 19.015] | core_live_station |
| `mum-elephanta` | Elephanta (Gharapuri) | [72.931, 18.963] | core_live_station |
| `mum-mora` | Mora (Uran) | [72.918, 18.84] | core_live_station |
| `mum-nerul` | Nerul | [73.02, 19.033] | committed_station |
| `mum-vashi` | Vashi | [72.999, 19.076] | committed_station |
| `mum-airoli` | Airoli | [72.998, 19.155] | committed_station |
| `mum-jnpt` | JNPT (Nhava Sheva) | [72.949, 18.949] | committed_station |
| `mum-rewas` | Rewas | [72.93, 18.77] | committed_station |
| `mum-bandra` | Bandra | [72.82, 19.044] | study_station |
| `mum-worli` | Worli | [72.815, 19.005] | study_station |

Total: **13** boarding points (6 core live, 5 committed, 2 study).

## Domestic corridors to seal (route the marked channels; interior_land_km == 0)

| pair_id | from | to | ~nm | rationale |
|---|---|---|---|---|
| `mum-1` | Gateway of India | Mandwa (Alibaug) | 9 | The flagship RoPax / passenger line across the harbour to Mandwa (Alibaug). |
| `mum-2` | Gateway of India | Elephanta (Gharapuri) | 6 | The Elephanta Caves heritage line. |
| `mum-3` | Ferry Wharf (Bhaucha Dhakka) | Mora (Uran) | 7 | Historic Bhaucha Dhakka line to Mora (Uran). |
| `mum-4` | Belapur (Navi Mumbai) | Gateway of India | 12 | Navi Mumbai water-taxi line to South Mumbai. |
| `mum-5` | Belapur (Navi Mumbai) | Nerul | 3 | Navi Mumbai harbour link. |
| `mum-6` | Gateway of India | JNPT (Nhava Sheva) | 8 | Harbour line to the Nhava Sheva port / industrial area. |
| `mum-7` | Vashi | Airoli | 4 | Thane-creek line through Navi Mumbai. |
| `mum-8` | Gateway of India | Rewas | 11 | Southern harbour line to Rewas / Alibaug. |
| `mum-9` | Bandra | Gateway of India | 7 | Proposed west-coast water-metro line linking Bandra to South Mumbai. |

Total: **9** domestic corridors. Each is `route_id: null` in the partner file;
seal them, then write the gold `route_id`s back and flip `_link_status` to sealed.

## Routing hazards — hand-waypoints required (NO land crossings)

- **Mumbai harbour shipping & naval zones** — Mumbai harbour is a major commercial and naval port (JNPT, Naval Dockyard) — routing must respect the shipping channel and naval exclusion zones; cross at marked points.
- **Thane creek shallows & mangroves** — Thane creek is shallow with mangroves and is a protected flamingo habitat — follow the marked channel and keep low-wake clear of the mangroves.
- **Monsoon sea state** — The open harbour and Mandwa/Rewas crossings get rough in the southwest monsoon — flag seasonal limits; Quanta-LR for the more exposed legs.
- **Atal Setu & bridge piers** — The Atal Setu (MTHL) sea bridge and other piers cross the harbour — hand-waypoint clear of the pier protection zones.

Domestic-only network across Mumbai harbour, Thane creek and the Alibaug coast. Konkan-coast links (Ratnagiri etc.) are secondary and out of scope for this phase.

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
