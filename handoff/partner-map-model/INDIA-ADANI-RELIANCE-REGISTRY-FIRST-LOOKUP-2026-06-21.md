# India Adani/Reliance registry-first lookup — 2026-06-21

Status: **lookup note only**. No new partner binds, route binds, boarding points, economics, or Atlas sealing.

## Files checked

- `handoff/partner-map-model/partner-global-registry-map.json`
- `handoff/partner-map-model/partner-market-canonical-bindings.json`
- `finance/model/corridors.json`

## Result summary

| Search target | Registry result | Interpretation | Action |
|---|---|---|---|
| `adani-ports` | Existing partner shell found: `partner_id = adani-ports`, display `Adani Ports & SEZ`, `market_count = 0`, `mapped_count = 0`, `markets = []` | Do not recreate Adani as a new partner. It exists as a shell but has no validated markets in the registry map. | Reuse shell only after exact market/asset validation; no footprint promotion yet. |
| Mumbai | Existing broad city ID found: `mumbai-india` in several partner market bindings | City-level geometry exists but is not asset-level proof for NMIA, Nariman Point, RCP, or Mumbai/Mandwa economics. | Can be a city-level lookup anchor only; not enough to bind proposal corridors. |
| Navi Mumbai / Ulwe / NMIA | No exact registry hit in checked files | No reusable exact BP/route ID found from this pass. | Keep `adani_nmia_ulwe_airport_waterfront_access_candidate` null. |
| Dighi / Agardanda | No exact registry hit in checked files | No reusable exact BP/route ID found from this pass. | Keep Dighi/Agardanda candidate null. |
| Hazira | No exact registry hit in checked files | No reusable exact BP/route ID found from this pass; also avoid conflating Adani Hazira Port with Reliance Hazira carbon-fibre seed. | Keep both Hazira candidates null pending exact geometry. |
| Mundra | No exact registry hit in checked files | No reusable exact BP/route ID found from this pass. | Keep Mundra candidate null. |
| Jamnagar | No exact registry hit in checked files | No reusable exact BP/route ID found from this pass. | Keep Jamnagar candidate null. |
| Nariman Point | No exact registry hit in checked files | No reusable exact BP/route ID found from this pass. | Keep RIL corporate-office corridor null. |
| Ghansoli / RCP | No exact registry hit in checked files | RCP official page exists, but no exact registry ID. | Keep RCP candidate null. |

## Exactness decision

The only reusable ID surfaced in this pass is broad `mumbai-india`. That is useful as a search anchor, but it is **not sufficient** to bind:

- NMIA / Ulwe airport access;
- RCP / Ghansoli corporate access;
- Nariman Point waterfront access;
- Dighi / Agardanda port access;
- Hazira Adani or Reliance assets;
- Mundra or Jamnagar industrial contexts.

## Next clean step

Build a manual `known / unknown / blocked` crosswalk against the underlying Atlas boarding-point registry, if available, using these exact labels only:

- Mumbai
- Navi Mumbai
- Ulwe
- NMIA / Navi Mumbai International Airport
- Nariman Point
- Ghansoli / Reliance Corporate Park
- Dighi
- Agardanda
- Hazira
- Mundra
- Jamnagar

If the boarding-point registry has no exact label hit, keep the candidate null and add it to the gap queue rather than creating speculative geography.
