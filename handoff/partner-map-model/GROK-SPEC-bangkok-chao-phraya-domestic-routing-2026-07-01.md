# GROK SPEC — Bangkok Chao Phraya River Transit domestic routing seal (2026-07-01)

**Authority:** Bangkok Chao Phraya river-transit network — regulated by the Marine Department (Ministry of Transport), operated by the Chao Phraya Express Boat and the electric MINE Smart Ferry
**Region:** Southeast Asia · **Country:** Thailand
**Anchor city id:** `bangkok-thailand`
**Home waters:** the Chao Phraya River
**Partner file:** `partner-pitch/partners/bangkok-chao-phraya.json` (mirror in `data-clean/partners/bangkok-chao-phraya.json`)
**Dossier:** `handoff/partner-map-model/PTA-DOSSIER-bangkok-chao-phraya.json`

## Mandate (Tasklet's lane is done; this is your seal lane)
Tasklet has authored the partner page narrative, the sourced domestic boarding points, the
honest-null domestic corridors (`route_id: null` + `_link_status: "geometry_seal_pending"`), and the
honest-pending economics (empty revenue/phase ladders + qualitative public-value levers). Your lane:
seal the geometry and regenerate the economics magnitudes against the sealed network.

## City node (already anchored)
`bangkok-thailand` already has a city brief at `data-clean/city_briefs/bangkok-thailand.json`.
ID-match / seal the boarding points below into that city and build the routes.

## Boarding points to seal (anchor coords are approximate — snap to real piers/terminals)

| node | name | anchor [lng,lat] | type |
|---|---|---|---|
| `bkk-sathorn` | Sathorn (Central / Taksin) | [100.5095, 13.719] | core_live_station |
| `bkk-oriental` | Oriental (N1) | [100.5135, 13.7235] | core_live_station |
| `bkk-si-phraya` | Si Phraya (N3) | [100.5125, 13.728] | core_live_station |
| `bkk-rachawong` | Rachawong (N5) | [100.5085, 13.737] | core_live_station |
| `bkk-memorial-bridge` | Memorial Bridge (N6) | [100.4975, 13.74] | core_live_station |
| `bkk-rajinee` | Rajinee (N7) | [100.4945, 13.744] | core_live_station |
| `bkk-tha-tien` | Tha Tien (N8) | [100.4915, 13.7435] | core_live_station |
| `bkk-tha-chang` | Tha Chang (N9) | [100.488, 13.751] | core_live_station |
| `bkk-wang-lang` | Wang Lang (N10) | [100.4855, 13.7575] | core_live_station |
| `bkk-phra-arthit` | Phra Arthit (N13) | [100.4955, 13.7625] | core_live_station |
| `bkk-rama8` | Rama VIII (N14) | [100.501, 13.7665] | core_live_station |
| `bkk-thewes` | Thewes (N15) | [100.505, 13.772] | core_live_station |
| `bkk-nonthaburi` | Nonthaburi (N30) | [100.492, 13.859] | core_live_station |
| `bkk-pakkret` | Pak Kret (N33) | [100.505, 13.913] | core_live_station |
| `bkk-wat-rajsingkorn` | Wat Rajsingkorn (S3) | [100.496, 13.708] | core_live_station |
| `bkk-iconsiam` | ICONSIAM | [100.51, 13.7265] | core_live_station |
| `bkk-ratburana` | Rat Burana (S4) | [100.498, 13.68] | study_station |

Total: **17** boarding points (16 core live, 0 committed, 1 study).

## Domestic corridors to seal (route the marked channels; interior_land_km == 0)

| pair_id | from | to | ~nm | rationale |
|---|---|---|---|---|
| `bkk-1` | Sathorn (Central / Taksin) | Phra Arthit (N13) | 3 | The core Old City line — Sathorn up to Phra Arthit and the Rattanakosin temples. |
| `bkk-2` | Sathorn (Central / Taksin) | Nonthaburi (N30) | 8 | The main north line to Nonthaburi. |
| `bkk-3` | Nonthaburi (N30) | Pak Kret (N33) | 4 | Upper-river extension to Pak Kret. |
| `bkk-4` | Sathorn (Central / Taksin) | Wat Rajsingkorn (S3) | 3 | Southern line to the Wat Rajsingkorn / Charoen Nakhon side. |
| `bkk-5` | Sathorn (Central / Taksin) | Tha Chang (N9) | 3 | Central line to the Grand Palace pier (Tha Chang). |
| `bkk-6` | Sathorn (Central / Taksin) | ICONSIAM | 1 | Cross-river shuttle to the ICONSIAM riverfront. |
| `bkk-7` | Sathorn (Central / Taksin) | Rat Burana (S4) | 6 | Southern commuter extension toward Rat Burana. |
| `bkk-8` | Sathorn (Central / Taksin) | Rama VIII (N14) | 4 | Central-to-north line via Rama VIII. |
| `bkk-9` | Tha Tien (N8) | Wang Lang (N10) | 1 | Cross-river temple line (Wat Pho/Wat Arun side to Wang Lang). |

Total: **9** domestic corridors. Each is `route_id: null` in the partner file;
seal them, then write the gold `route_id`s back and flip `_link_status` to sealed.

## Routing hazards — hand-waypoints required (NO land crossings)

- **Strong Chao Phraya current & barges** — The river runs a strong current and heavy rice/sand barge tows — follow the marked channel and waypoint clear of barge trains and moorings.
- **Dense pier traffic** — The express-boat piers are extremely busy with frequent stops — strict low-wake, geofenced no-foil zones at every pier.
- **Bridge piers** — Numerous bridge piers (Memorial, Rama VIII, Phra Nang Klao) sit in the channel — hand-waypoint clear.
- **Tidal & flood-season levels** — River level swings with tide and the monsoon flood season — routing and pier access must account for high-flow periods.

Domestic-only network on the Chao Phraya within Greater Bangkok. Khlong (canal) and Gulf links are secondary and out of scope for this phase.

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
