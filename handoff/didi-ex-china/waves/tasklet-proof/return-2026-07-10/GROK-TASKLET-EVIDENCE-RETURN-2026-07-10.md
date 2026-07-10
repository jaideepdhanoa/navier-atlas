# DiDi ex-China — Tasklet evidence return to Grok

**As of:** 2026-07-10  
**Status:** `research-complete / materialization-review-needed`  
**Geometry:** unchanged; Grok’s sealed routes were not re-sealed  
**Finance:** no cascade performed by Tasklet

## Executive result

- Reviewed **47 exact entity records** across **5 lanes** covering T1–T12.
- `usable_for_base_case`: **7**
- `benchmark_only`: **8**
- `not_publicly_supported`: **30**
- `permission_required`: **2**

Only **four passenger-volume records** are candidates for controlled model review: the two 2024 Costa Rica directional ferry rows and two exact Chile/Argentina route totals. Three other usable records are scope/service controls, not passenger economics. Everything else remains benchmark-only, held, null, or permission-gated.

## Materialization candidates

| Ask | Exact entity | Published value | Period / semantics | Action |
|---|---|---:|---|---|
| T2 | `rn-7e59f984abec` | 642133 | 2024 calendar year; one-way passenger journeys (passengers transported in the named Paquera-to-Puntarenas direction) | Controlled model review; preserve exact units and period |
| T2 | `rn-eb4ca32edbef` | 317859 | 2024 calendar year; one-way passenger journeys (passengers transported in the named Playa Naranjo-to-Puntarenas direction) | Controlled model review; preserve exact units and period |
| T7 | `rn-f451444da7fe` | 38900 | 2025-2026 summer operating season; operator/port-authority reported passengers transported on the crossing; aggregate directions, not stated as unique persons or round trips | Controlled model review; preserve exact units and period |
| T7 | `rn-04b92d6952d2` | 2177670 | 2024; annual passenger movements in regular vessel services on the port pair; both directions aggregated, not unique visitors or round trips | Controlled model review; preserve exact units and period |

### Constraints

- Costa Rica: use the named direction rows exactly as published. The opposite direction is separately reported; do not double or halve. ARESEP fares are already banked, but no realized yield was proven.
- Rosario: the 38,900 figure is the complete 2025–2026 operating-season total, not a calendar-year statistic and not stated as directional.
- Colonia–Buenos Aires: 2,177,670 is a 2024 port-pair passenger-movement total across both directions and regular operators, not unique visitors.

## Scope and operation controls

- **T8 Tigre:** official current DiDi zone proof is usable at city/service-zone level. It does not prove pickup at the ferry ramp, realized supply, or wait time.
- **T12 El Gouna:** do not inherit Hurghada DiDi proof into El Gouna; the combined Atlas city ID remains a leakage risk.
- **T12 NEOM:** Saudi Arabia only. A Safaga–NEOM service would be an international Egypt–Saudi corridor, not Egypt domestic coverage.

## Holds by ask

- **T1 Colombia:** recommend **C — hold**. `rn-aa790551baa7` still lacks exact current OD passengers, fare, and schedule. Option B also contains a finance-only route ID absent from canonical `ROUTES.json`.
- **T3 Panama Guna:** both routes are `permission_required`; no route-specific authorization or approved operator was public.
- **T4 Dominican Republic:** primary operator/timetable/fare and Cayo Levantado exact-route passengers remain null.
- **T5 Galápagos:** exact January–June 2022 directional movements are useful historical benchmarks only. Do not annualize or populate `annual_one_way_pax`.
- **T6 Peru:** Ballestas exact-terminal embarkations and Palomino terminal-level boardings remain null.
- **T7:** eight of ten route-demand asks remain null.
- **T8 Chile:** no exact official DiDi proof for the eight named ferry towns; Chile featured stays empty.
- **T9 Hong Kong:** 1.250 million annual route journeys is a 2017 historical benchmark only.
- **T10 Taiwan:** no current local DiDi passenger-operation proof; keep `rn-5085d4e1f498` and 95,705 held.
- **T11 Egypt:** current cruise-terminal names and port-level coordinates are benchmarks only; exact berth coordinates for Cairo, cruise, Giftun, and Mahmeya locations remain null.

## Exact Grok return action

1. Review and, if model semantics match, materialize only the two T2 and two T7 passenger-volume candidates through the normal partner-model cascade.
2. Preserve all benchmark labels and nulls; do not annualize six-month Galápagos data or refresh 2017 Hong Kong patronage by inference.
3. Keep Colombia decision C, Panama permission gates, Dominican Republic/Peru/Taiwan/Egypt passenger holds, and Chile featured-empty state.
4. Apply the T8/T12 service/geography controls without promoting economics.
5. Return a deterministic source → model → partner JSON → deck linkage receipt for any materialized route.

## Artifacts

- `MASTER-EVIDENCE-LEDGER.json` — all 47 records with source metadata, quotes, classifications, and failed searches.
- `GROK-TASKLET-EVIDENCE-RETURN-2026-07-10.json` — machine decision receipt.
- Five lane folders (`colombia`, `ca-dr`, `ec-pe`, `cl-ar`, `hk-tw-egypt`) — source ledgers and statuses.

