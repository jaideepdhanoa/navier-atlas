# Intra-city boarding-point mesh — backlog

## Policy (2026-06-24)

**Every sealed market with ≥2 boarding points in a city MUST run the shared mesh lane**
(`scripts/grok-geometry/mint_intra_city_mesh.py`) after corridor mint, before economics bind.

This is **not** Bolt/Yango exclusive. Corridor-only seals leave orphan BPs and under-lit partner pages.

## Shared tooling

| Script | Role |
|--------|------|
| `scripts/grok-geometry/mint_intra_city_mesh.py` | Full BP×BP mesh within each city |
| `scripts/grok-geometry/abc_offshore_waypoints.py` | Curaçao leeward arcs (Hato north→south) |
| `scripts/grok-geometry/fix_abc_curacao_offshore_routes.py` | Re-apply offshore geometry on sealed Hato legs |

Wire into seal lanes via:

```bash
python3 scripts/grok-geometry/mint_intra_city_mesh.py --dc data-clean --abc-only   # ABC / Ocean Whisperer
python3 scripts/grok-geometry/mint_intra_city_mesh.py --dc data-clean --boltyango-anchors
python3 scripts/grok-geometry/mint_intra_city_mesh.py --dc data-clean --cities dubai-uae,abu-dhabi-uae
```

## Done

- [x] **ABC islands / Ocean Whisperer** — `run-abc-islands-seal-lane.sh` step 2/9
- [x] **Bolt/Yango** — `route_bolt_yango_markets.py` delegates to shared mesh

## Backlog — markets likely under-meshed

Prioritize partner pages where `pois >> routes` on the scoped build (build-site.mjs line per partner).

| Market / partner | Symptom | Suggested `--cities` |
|----------------|---------|----------------------|
| Caribbean × Navier (generic) | Same ABC nodes as OW; corridor-only | `curacao-curacao,aruba-aruba,bonaire-bonaire` |
| Grab Thailand sub-markets | Bucket-C sealed BPs, sparse chords | per `connected_city_mesh` in partner JSON |
| French Polynesia / hospitality hubs | Resort BPs without inter-resort mesh | TBD from `BP_DEFS` or POI parent_city |
| UAE commercial (non-Bolt) | High POI density, backbone-only routes | `dubai-uae,abu-dhabi-uae,sharjah-uae` |
| Greece islands (Bolt) | Partial — Bolt anchors meshed; verify Dodecanese | `mykonos-greece,paros-greece,...` |
| Croatia / Montenegro | Dubrovnik cluster | `dubrovnik-croatia,korcula-croatia,split-croatia` |
| Red Sea / AMAALA | Spur routes without local mesh | `red-sea-global-ksa,amaala-ksa` |
| Egypt sealed corridors | `#79at` trimmed mesh to 35/city — revisit cap | per showcase cities in trim report |
| WSF / BC Ferries | Real ferry mesh exists; verify capillary gaps | `san-juan-islands-usa`, `gulf-islands-bc-canada` |

## Acceptance

- Intra-city pair coverage: all canonical sealed BPs connected (complete graph on curated endpoints).
- Curaçao Hato→south legs: `interior_land_km ≤ 0.08`, `render_smooth: false`.
- Partner scoped build: OW `routes` count rises toward full mesh (expect ~30+ intra-Curaçao after ABC mesh).