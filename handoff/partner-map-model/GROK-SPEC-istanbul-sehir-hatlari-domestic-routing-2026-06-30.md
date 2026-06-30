# GROK SPEC — İstanbul Şehir Hatları (City Lines) domestic routing seal (2026-06-30)

**Authority:** Şehir Hatları A.Ş., the public ferry operator owned by the Istanbul Metropolitan Municipality (İBB)
**Region:** Europe · **Country:** Türkiye
**Anchor city id:** `istanbul-turkey`
**Home waters:** the Bosphorus, the Golden Horn and the Sea of Marmara
**Partner file:** `partner-pitch/partners/istanbul-sehir-hatlari.json` (mirror in `data-clean/partners/istanbul-sehir-hatlari.json`)
**Dossier:** `handoff/partner-map-model/PTA-DOSSIER-istanbul-sehir-hatlari.json`

## Mandate (Tasklet's lane is done; this is your seal lane)
Tasklet has authored the partner page narrative, the sourced domestic boarding points, the
honest-null domestic corridors (`route_id: null` + `_link_status: "geometry_seal_pending"`), and the
honest-pending economics (empty revenue/phase ladders + qualitative public-value levers). Your lane:
seal the geometry and regenerate the economics magnitudes against the sealed network.

## City node (already anchored)
`istanbul-turkey` already has a city brief at `data-clean/city_briefs/istanbul-turkey.json`.
ID-match / seal the boarding points below into that city and build the routes.

## Boarding points to seal (anchor coords are approximate — snap to real piers/terminals)

| node | name | anchor [lng,lat] | type |
|---|---|---|---|
| `sh-eminonu` | Eminönü | [28.973, 41.0175] | core_live_station |
| `sh-karakoy` | Karaköy | [28.976, 41.022] | core_live_station |
| `sh-besiktas` | Beşiktaş | [29.006, 41.041] | core_live_station |
| `sh-kabatas` | Kabataş | [28.994, 41.033] | core_live_station |
| `sh-uskudar` | Üsküdar | [29.015, 41.026] | core_live_station |
| `sh-kadikoy` | Kadıköy | [29.009, 40.992] | core_live_station |
| `sh-ortakoy` | Ortaköy | [29.027, 41.047] | core_live_station |
| `sh-beylerbeyi` | Beylerbeyi | [29.042, 41.043] | core_live_station |
| `sh-cengelkoy` | Çengelköy | [29.054, 41.053] | core_live_station |
| `sh-kuzguncuk` | Kuzguncuk | [29.032, 41.034] | core_live_station |
| `sh-kanlica` | Kanlıca | [29.061, 41.089] | core_live_station |
| `sh-anadolu-hisari` | Anadolu Hisarı | [29.066, 41.082] | core_live_station |
| `sh-emirgan` | Emirgan | [29.054, 41.109] | core_live_station |
| `sh-istinye` | İstinye | [29.058, 41.115] | core_live_station |
| `sh-yenikoy` | Yeniköy | [29.056, 41.123] | core_live_station |
| `sh-sariyer` | Sarıyer | [29.056, 41.167] | core_live_station |
| `sh-rumeli-kavagi` | Rumeli Kavağı | [29.068, 41.188] | core_live_station |
| `sh-anadolu-kavagi` | Anadolu Kavağı | [29.09, 41.175] | core_live_station |
| `sh-beykoz` | Beykoz | [29.09, 41.13] | core_live_station |
| `sh-bostanci` | Bostancı | [29.095, 40.956] | core_live_station |
| `sh-buyukada` | Büyükada | [29.123, 40.876] | core_live_station |
| `sh-heybeliada` | Heybeliada | [29.095, 40.877] | core_live_station |
| `sh-burgazada` | Burgazada | [29.068, 40.881] | core_live_station |
| `sh-kinaliada` | Kınalıada | [29.051, 40.908] | core_live_station |
| `sh-eyup` | Eyüp | [28.934, 41.048] | core_live_station |
| `sh-haskoy` | Hasköy | [28.949, 41.041] | core_live_station |
| `sh-fener-balat` | Fener-Balat | [28.949, 41.029] | core_live_station |
| `sh-kasimpasa` | Kasımpaşa | [28.966, 41.036] | core_live_station |

Total: **28** boarding points (28 core live, 0 committed, 0 study).

## Domestic corridors to seal (route the marked channels; interior_land_km == 0)

| pair_id | from | to | ~nm | rationale |
|---|---|---|---|---|
| `sh-d01` | Eminönü | Kadıköy | 3.2 | The flagship cross-Bosphorus commute — Eminönü on the European shore to Kadıköy on the Asian shore. |
| `sh-d02` | Eminönü | Üsküdar | 1.3 | Eminönü to Üsküdar across the Bosphorus mouth — the shortest, busiest continent-to-continent hop. |
| `sh-d03` | Karaköy | Kadıköy | 3.0 | Karaköy to Kadıköy — a heavy cross-strait commute from the European waterfront. |
| `sh-d04` | Beşiktaş | Üsküdar | 1.4 | Beşiktaş to Üsküdar — a core cross-Bosphorus commute crossing. |
| `sh-d05` | Beşiktaş | Kadıköy | 3.1 | Beşiktaş to Kadıköy — a busy European-to-Asian commute line. |
| `sh-d06` | Eminönü | Anadolu Kavağı | 12.5 | Eminönü up the full Bosphorus to Anadolu Kavağı — the classic strait line past the villages and fortresses. |
| `sh-d07` | Kabataş | Büyükada | 9.5 | Kabataş across the Sea of Marmara to Büyükada — the main Princes' Islands run. |
| `sh-d08` | Bostancı | Büyükada | 4.6 | Bostancı on the Asian shore to Büyükada — the short Princes' Islands crossing. |
| `sh-d09` | Üsküdar | Eyüp | 4.2 | Üsküdar up the Golden Horn to Eyüp — the historic Haliç line. |
| `sh-d10` | Büyükada | Heybeliada | 1.1 | Büyükada to Heybeliada — the inter-island hop in the Princes' Islands. |

Total: **10** domestic corridors. Each is `route_id: null` in the partner file;
seal them, then write the gold `route_id`s back and flip `_link_status` to sealed.

## Routing hazards — hand-waypoints required (NO land crossings)

- **Bosphorus currents** — The Bosphorus runs a strong surface current with a reverse counter-current beneath; hand-waypoint the crossings and account for the set on every continent-to-continent leg.
- **One of the world's busiest shipping straits** — The Bosphorus carries heavy commercial and tanker traffic under a traffic-separation scheme; cross-strait legs must cross the lanes perpendicular and route clear of the through-traffic.
- **Sea of Marmara open-water crossings** — The Princes' Islands legs cross open Marmara water exposed to wind and swell; route the marked crossings and manage exposure.
- **Golden Horn low bridges** — The Galata, Atatürk and Haliç metro bridges constrain the Golden Horn; route through the marked openings with air-draft and pier clearance.
- **Lodos storms & fog** — Southerly lodos storms and Bosphorus fog reduce conditions in winter; routing and speed must respect closure advisories.
- **Dense pier traffic** — Eminönü, Karaköy, Üsküdar and Kadıköy are extremely busy ferry and fishing-boat piers; geofence speed and give-way behaviour on the approaches.

The Şehir Hatları network is entirely domestic within Istanbul's waters — the Bosphorus, the Golden Horn and the Sea of Marmara to the Princes' Islands. There are no international legs; the whole proposal is domestic.

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
_Authored by Tasklet · 2026-06-30 · PTA batch 4 · Bahrain MOTC gold pattern._
