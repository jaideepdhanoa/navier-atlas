# Gold #18 — Maldives inter-island expansion + finance-model layer (2026-06-07)

## Geometry
- **+31 real open-water edges** spliced into `data-clean/ROUTES.json` (5,175 → 5,206), de-Malé-ifying the Maldives cluster across **9 atoll gateways**: South Ari (Maamigili), Baa (Dharavandhoo), Noonu (Maafaru), Raa (Ifuru), Dhaalu (Kudahuvadhoo), Gaafu (Kooddoo), Laamu (Kadhdhoo), Addu (Gan), Lhaviyani.
- All 31 solved offline via `_solve_corridor_waypoints.py` (fine-grid A* + visibility-simplify); **every edge gate-passes at ≤1.0 km interior land** (all 0.0 km). `edge_class` inter-island/island-hop, platform Pioneer II (all ≤18nm).
- Endpoint ids `male-maldives__<slug>`; existing resort endpoints reused (soneva-fushi-jetty, soneva-jani-jetty, six-senses-laamu-jetty) to avoid duplicate pins. Route ids `e__mald__<md5>` — zero collisions.
- **Front-end note:** these are new `LineString` features in ROUTES.json; render bidirectional `↔` per standing rule.

## Finance model
- **Capex/useful-life → 20yr** (marine commercial-passenger-vessel best practice): per-boat depreciation $90K→$45K/yr; paybacks/margins improve, fleet & market-rev unchanged.
- **A′ capture** ON (per-corridor `captive` flags on 29 luxury corridors; blanket archetype map NOT used → zero contested-leg over-claim).
- **Saudi/Red Sea → forward/SAM** (`_forward_sam`): bucketed out of near-term grounded floor + out of demand-cascade median.
- **R-FLOOR-2 network-sum fleet basis** for captive archipelago clusters (one fleet serves the cluster; sum fractional need, round once) — opt-in per-market, only `maldives-jih`. Contested markets (Grab/Careem/Saudi/RedSea) keep per-corridor floor → zero regression (verified).
- **Maldives 19 → 39 boats / $38.9M → $87.5M** near-term floor. Sidecar 38 → **69** route-pinned records (jih-global 33).

## Verify (Claude)
- `SEAL.json` blobs.ROUTES count 5206 / new sha; sidecars.economics_by_route_id.json count 69 / new sha.
- No `index.html` emitted; `build.mjs` bakes `atlas-data.js` from `data-clean/`.
