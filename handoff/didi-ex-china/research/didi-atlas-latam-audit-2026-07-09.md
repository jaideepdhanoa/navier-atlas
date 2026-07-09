# DiDi Atlas LATAM coverage audit — 2026-07-09

**Repository:** `/tmp/navier-atlas`  
**Commit:** `ae1b96917eaed901a84302b856ce53f6efd767ae` (2026-07-09 00:01:55 -0700)  
**Repo source files modified:** no

## Executive result

- **10 countries audited:** 8 have canonical Atlas clusters; 2 are country-level registry gaps.
- **Current full DiDi proposal:** 7 full markets across 6 countries. Ecuador and Peru have existing Atlas coverage but are absent; Chile and Argentina have no canonical cluster.
- **20 Atlas member cities:** 10 `already_full`, 3 `thin_to_full`, 7 `new_display_coverage`. Two additional country-level `true_registry_gap` records have no invented city IDs.
- **Finance is not usable:** durable model = 0 corridors; scoped recal = 38, but only 8 route IDs resolve and 30 are stale; aggregate = 0 while the proposal embeds a $5.8M floor and $1.53B journey GMV.
- **Briefs:** 19/20; only one brief contains DiDi-specific content. Canonical marquee coverage is 9 featured / 8 wow routes, all in three clusters.

## Country and cluster coverage

| Country | Cluster ID | Class | Member city IDs | Routes stamped / touching | POIs / route BPs | Marquee F/W | Finance model / current recal | Current full market(s) | Briefs |
|---|---|---|---|---:|---:|---:|---:|---|---:|
| Mexico | `mexico` | `thin_to_full` | `cancun-riviera-maya-mexico`, `cozumel-mexico`, `los-cabos-mexico`, `playa-del-carmen-mexico`, `puerto-vallarta-mexico` | 76 / 57 | 141 / 49 | 0 / 0 | 0 / 6 | `mexico-pacific`, `mexico-caribbean` | 5/5 |
| Brazil | `brazil` | `already_full` | `angra-dos-reis-ilha-grande-brazil`, `florianopolis-brazil`, `rio-de-janeiro-brazil` | 59 / 59 | 194 / 49 | 0 / 0 | 0 / 1 | `brazil` | 3/3 |
| Colombia | `colombia` | `thin_to_full` | `cartagena-colombia`, `barranquilla-colombia` | 15 / 16 | 49 / 15 | 0 / 0 | 0 / 0 | `colombia` | 2/2 |
| Chile | — | `true_registry_gap` | — | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | — | 0/0 |
| Costa Rica | `costa-rica` | `already_full` | `nicoya-papagayo-costa-rica` | 67 / 67 | 39 / 50 | 6 / 5 | 0 / 0 | `costa-rica` | 1/1 |
| Panama | `panama` | `already_full` | `san-blas-panama` | 47 / 47 | 48 / 38 | 1 / 1 | 0 / 1 | `panama` | 1/1 |
| Argentina | — | `true_registry_gap` | — | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | — | 0/0 |
| Ecuador | `galapagos-ecuador` | `new_display_coverage` | `floreana-galapagos-ecuador`, `isabela-galapagos-ecuador`, `san-cristobal-galapagos-ecuador`, `santa-cruz-galapagos-ecuador` | 46 / 3 | 6 / 0 | 0 / 0 | 0 / 0 | — | 4/4 |
| Peru | `peru` | `new_display_coverage` | `lima-peru`, `paracas-peru`, `pisco-san-andres-peru` | 11 / 12 | 10 / 10 | 0 / 0 | 0 / 0 | — | 2/3 |
| Dominican Republic | `dominican-republic` | `already_full` | `samana-dominican-republic` | 32 / 32 | 36 / 28 | 2 / 2 | 0 / 0 | `dominican-republic` | 1/1 |

**Route-count warning:** “stamped” means the current `ROUTES.properties.cluster_id`; “touching” is recomputed from stable endpoint city IDs. The difference is a data defect, not geography judgment. In particular, `galapagos-ecuador` is stamped onto 46 routes with zero Galápagos endpoints, while the three actual Galápagos member routes are stamped elsewhere. Mexico has 21 foreign-stamped routes and two member routes stamped outside `mexico`.

## City-level inventory

### Mexico — `mexico`

| City ID | Class | Routes touch / cluster_city | POIs / route BPs | Marquee F/W | Finance current | DiDi map / full anchor | Brief maturity |
|---|---|---:|---:|---:|---:|---|---|
| `cancun-riviera-maya-mexico` | `already_full` | 24 / 24 | 75 / 25 | 0 / 0 | 3 | yes / `mexico-caribbean` | `starter` (12/12 core; DiDi-specific: no) |
| `cozumel-mexico` | `thin_to_full` | 1 / 0 | 0 / 0 | 0 / 0 | 0 | yes / no | `canonical_complete_untiered` (12/12 core; DiDi-specific: no) |
| `los-cabos-mexico` | `already_full` | 16 / 16 | 34 / 12 | 0 / 0 | 3 | yes / `mexico-pacific` | `starter` (12/12 core; DiDi-specific: no) |
| `playa-del-carmen-mexico` | `thin_to_full` | 1 / 0 | 0 / 0 | 0 / 0 | 0 | yes / no | `canonical_complete_untiered` (12/12 core; DiDi-specific: no) |
| `puerto-vallarta-mexico` | `already_full` | 16 / 16 | 32 / 12 | 0 / 0 | 0 | yes / `mexico-pacific` | `starter` (12/12 core; DiDi-specific: no) |

### Brazil — `brazil`

| City ID | Class | Routes touch / cluster_city | POIs / route BPs | Marquee F/W | Finance current | DiDi map / full anchor | Brief maturity |
|---|---|---:|---:|---:|---:|---|---|
| `angra-dos-reis-ilha-grande-brazil` | `already_full` | 1 / 17 | 74 / 1 | 0 / 0 | 1 | yes / `brazil` | `canonical_complete_untiered` (12/12 core; DiDi-specific: no) |
| `florianopolis-brazil` | `already_full` | 20 / 20 | 61 / 16 | 0 / 0 | 0 | yes / `brazil` | `starter` (12/12 core; DiDi-specific: no) |
| `rio-de-janeiro-brazil` | `already_full` | 39 / 18 | 59 / 32 | 0 / 0 | 1 | yes / `brazil` | `starter` (12/12 core; DiDi-specific: no) |

### Colombia — `colombia`

| City ID | Class | Routes touch / cluster_city | POIs / route BPs | Marquee F/W | Finance current | DiDi map / full anchor | Brief maturity |
|---|---|---:|---:|---:|---:|---|---|
| `cartagena-colombia` | `already_full` | 15 / 6 | 47 / 13 | 0 / 0 | 0 | yes / `colombia` | `starter` (12/12 core; DiDi-specific: yes) |
| `barranquilla-colombia` | `thin_to_full` | 1 / 0 | 2 / 2 | 0 / 0 | 0 | yes / no | `canonical_complete_untiered` (12/12 core; DiDi-specific: no) |

### Costa Rica — `costa-rica`

| City ID | Class | Routes touch / cluster_city | POIs / route BPs | Marquee F/W | Finance current | DiDi map / full anchor | Brief maturity |
|---|---|---:|---:|---:|---:|---|---|
| `nicoya-papagayo-costa-rica` | `already_full` | 67 / 22 | 39 / 50 | 6 / 5 | 0 | yes / `costa-rica` | `canonical_complete_untiered` (12/12 core; DiDi-specific: no) |

### Panama — `panama`

| City ID | Class | Routes touch / cluster_city | POIs / route BPs | Marquee F/W | Finance current | DiDi map / full anchor | Brief maturity |
|---|---|---:|---:|---:|---:|---|---|
| `san-blas-panama` | `already_full` | 47 / 0 | 48 / 38 | 1 / 1 | 1 | yes / `panama` | `canonical_complete_untiered` (12/12 core; DiDi-specific: no) |

### Ecuador — `galapagos-ecuador`

| City ID | Class | Routes touch / cluster_city | POIs / route BPs | Marquee F/W | Finance current | DiDi map / full anchor | Brief maturity |
|---|---|---:|---:|---:|---:|---|---|
| `floreana-galapagos-ecuador` | `new_display_coverage` | 1 / 0 | 0 / 0 | 0 / 0 | 0 | no / no | `canonical_complete_untiered` (12/12 core; DiDi-specific: no) |
| `isabela-galapagos-ecuador` | `new_display_coverage` | 1 / 0 | 1 / 0 | 0 / 0 | 0 | no / no | `canonical_complete_untiered` (12/12 core; DiDi-specific: no) |
| `san-cristobal-galapagos-ecuador` | `new_display_coverage` | 1 / 0 | 1 / 0 | 0 / 0 | 0 | no / no | `canonical_complete_untiered` (12/12 core; DiDi-specific: no) |
| `santa-cruz-galapagos-ecuador` | `new_display_coverage` | 3 / 0 | 4 / 0 | 0 / 0 | 0 | no / no | `canonical_complete_untiered` (12/12 core; DiDi-specific: no) |

### Peru — `peru`

| City ID | Class | Routes touch / cluster_city | POIs / route BPs | Marquee F/W | Finance current | DiDi map / full anchor | Brief maturity |
|---|---|---:|---:|---:|---:|---|---|
| `lima-peru` | `new_display_coverage` | 10 / 0 | 7 / 7 | 0 / 0 | 0 | no / no | `canonical_complete_untiered` (12/12 core; DiDi-specific: no) |
| `paracas-peru` | `new_display_coverage` | 3 / 0 | 2 / 2 | 0 / 0 | 0 | no / no | `canonical_complete_untiered` (12/12 core; DiDi-specific: no) |
| `pisco-san-andres-peru` | `new_display_coverage` | 1 / 0 | 1 / 1 | 0 / 0 | 0 | no / no | `missing` (0/12 core; DiDi-specific: no) |

### Dominican Republic — `dominican-republic`

| City ID | Class | Routes touch / cluster_city | POIs / route BPs | Marquee F/W | Finance current | DiDi map / full anchor | Brief maturity |
|---|---|---:|---:|---:|---:|---|---|
| `samana-dominican-republic` | `already_full` | 32 / 0 | 36 / 28 | 2 / 2 | 0 | yes / `dominican-republic` | `canonical_complete_untiered` (12/12 core; DiDi-specific: no) |

## Proposal parity Gates A–G

| Gate | Status | Finding |
|---|---|---|
| A | **FAIL** | All 10 anchors resolve, but roster/crosswalk and linkage parity fail. |
| B | **FAIL** | The finance spine is absent from the durable model and stale/contradictory elsewhere. |
| C | **FAIL** | Seven current markets have full narrative fields, but expansion markets and phase bindings are incomplete. |
| C.1 | **FAIL** | Hub vessel method exists, but per-market/per-phase vessel and route bindings do not. |
| D | **FAIL** | No transparent sheet/deck binding; model, recal, proposal and data-clean do not form a coherent cascade. |
| E | **PASS** | No special sovereign/sanctions framing is required for this assigned LatAm audit. |
| F | **PASS** | DiDi carries all five deck narrative source fields and the strict narrative guard reported all deck-eligible partners ready. |
| G | **PASS** | Partner copy lint passes. |

### Exact parity failures

- **Anchor resolution:** 10/10 anchor IDs resolve to both `FEATURES_BY_TYPE.city` IDs and `CLUSTERS.member_city_ids`. The crosswalk artifact is nevertheless missing.
- **Roster:** `_map_scope.cluster_city_ids` has 18 IDs versus 10 full-market anchors. Assigned-LatAm scope has 13 canonical cities; the three inherited-but-not-full cities are `barranquilla-colombia`, `cozumel-mexico`, `playa-del-carmen-mexico`. The scope also contains `hong-kong`, `macau-china`, `mexico-caribbean`, `mexico-pacific`, `shanghai-china`; `covered_markets_and_footprint_union_cluster_members` has allowed covered:false China records and two market IDs to leak into a city-ID list.
- **Linkage:** 28 market journeys and 4 hub journeys have zero route IDs; all 21 phase `featured_routes[]` arrays are empty; zero phases have `fleet_confidence`; zero subpages have `vessel_sizing`.
- **Finance identity:** `38` scoped recal corridors → `8` current route IDs; `30` stale. `agg-didi.json` is zero/null, contradicting embedded SOM `$5,768,158`, marine TAM `$508,751,562`, journey GMV `$1,526,254,686`, and partner revenue `$68,681,461`.
- **Demand:** all 38 recal demand records are T3 `bite2/econ_sidecar_inherit`; growth references `grab-greenfield-census.json`, which is borrowed peer census, not a labelled global template.
- **Country references:** present only for Brazil, Colombia, Peru. Missing: Mexico, Chile, Costa Rica, Panama, Argentina, Ecuador, Dominican Republic. Four are already in the current full proposal: Mexico, Costa Rica, Panama, Dominican Republic.
- **Copy/narrative:** both pass: all five narrative fields are present; strict narrative reports 30/30 deck-eligible partners ready; proposal copy lint reports zero leaks.

## Coverage promotion queue

- **Already full (10 cities):** `cancun-riviera-maya-mexico`, `los-cabos-mexico`, `puerto-vallarta-mexico`, `angra-dos-reis-ilha-grande-brazil`, `florianopolis-brazil`, `rio-de-janeiro-brazil`, `cartagena-colombia`, `nicoya-papagayo-costa-rica`, `san-blas-panama`, `samana-dominican-republic`.
- **Thin → full (3 cities):** `cozumel-mexico`, `playa-del-carmen-mexico`, `barranquilla-colombia`.
- **New display coverage (7 cities):** `floreana-galapagos-ecuador`, `isabela-galapagos-ecuador`, `san-cristobal-galapagos-ecuador`, `santa-cruz-galapagos-ecuador`, `lima-peru`, `paracas-peru`, `pisco-san-andres-peru`.
- **True registry gaps (country level):** Argentina, Chile. Official DiDi country evidence exists, but no exact coastal city inventory exists in the repo; no city IDs were invented.
- **`not_in_atlas` / `exclude_inland`:** zero exact rows. The available DiDi source is country-level only, so it cannot support an inland city exclusion roster.

## Prioritized defect register

| Priority | ID | Defect | Exact evidence |
|---|---|---|---|
| P0 | `DIDI-LATAM-01` | Rebuild one canonical DiDi finance spine | `"finance/model has 0 DiDi corridors; scoped recal declares 38 but only 8 route IDs exist in current ROUTES and 30 are stale; agg is zero while proposal SOM floor is $5,768,158."` |
| P0 | `DIDI-LATAM-02` | Repair global route cluster stamping before inheriting Ecuador/Peru | `{"verdict":"FAIL","foreign_stamped_route_id_samples":["ics-2fe885536a","ics-3b1885b0e5","ics-6a2d222c1d","ics-73527c3365","ics-9409a653d6","ics-9797408cf4","ics-bcf8a66caf","ics-c1f5deb1fa"],"member_route_outside_cluster_id_samples":["e__santa-cruz-galapagos-ecuador__puerto-ayora__isabela-galapagos-ecuador__puerto-villamil","e__santa-cruz-galapagos-ecuador__puerto-ayora__san-cristobal-galapagos-ecuador__puerto-baq…` |
| P0 | `DIDI-LATAM-03` | Reconcile DiDi map/full-market/network rosters | `{"map_scope_ids":18,"assigned_latam_scope_ids":13,"anchor_ids":10,"scope_without_anchor":["barranquilla-colombia","cozumel-mexico","playa-del-carmen-mexico"],"out_of_payload_scope_ids":["hong-kong","macau-china","mexico-caribbean","mexico-pacific","shanghai-china"],"non_city_scope_ids":["mexico-caribbean","mexico-pacific"]}` |
| P1 | `DIDI-LATAM-04` | Add country-supported display coverage for Ecuador and Peru | `{"ecuador_city_ids":["floreana-galapagos-ecuador","isabela-galapagos-ecuador","san-cristobal-galapagos-ecuador","santa-cruz-galapagos-ecuador"],"peru_city_ids":["lima-peru","paracas-peru","pisco-san-andres-peru"]}` |
| P1 | `DIDI-LATAM-05` | Deepen three thin current cities to full subproposal coverage | `{"city_ids":["barranquilla-colombia","cozumel-mexico","playa-del-carmen-mexico"]}` |
| P1 | `DIDI-LATAM-06` | Fix country-reference and country-key coverage | `{"missing_assigned":["Mexico","Chile","Costa Rica","Panama","Argentina","Ecuador","Dominican Republic"],"missing_current":["Mexico","Costa Rica","Panama","Dominican Republic"],"recal_country_values":{"Samaná":6,"San Blas":6,"cartagena-colombia":4,"Angra dos Reis":4,"Puerto Vallarta & Riviera Nayarit":3,"Los Cabos":3,"Cartagena & the Rosario Islands":1,"Cancún & the Riviera Maya":1,"Cancún & The Riviera Maya":1,"Fl…` |
| P1 | `DIDI-LATAM-07` | Replace T3 inherited demand and borrowed Grab census | `{"demand_tiers":{"T3":38},"borrowed_census":"grab-greenfield-census.json"}` |
| P1 | `DIDI-LATAM-08` | Bind phase routes and phase fleet methodology | `{"phases":21,"phase_featured_routes":0,"phase_fleet_confidence":0,"subpage_vessel_sizing":0}` |
| P1 | `DIDI-LATAM-09` | Close brief and partner-overlay gaps | `{"briefs_present":19,"briefs_total":20,"missing_city_ids":["pisco-san-andres-peru"],"didi_specific_brief_city_ids":["cartagena-colombia"]}` |
| P2 | `DIDI-LATAM-10` | Create missing sheet/deck delivery artifacts | `{"economics_url":null,"sheet_id":false,"transparent_sheet":false,"deck":false}` |
| P2 | `DIDI-LATAM-11` | Invalidate stale PASS receipts | `{"spine_parity":"PASS at 82/95 (86.3%)","page_qa_checked_at":"2026-06-21T14:25:19Z","current_market_journey_route_ids":0}` |
| P2 | `DIDI-LATAM-12` | Expand canonical marquee curation beyond three clusters | `{"canonical_marquee_featured":9,"canonical_marquee_wow":8,"cities_with_marquee":["nicoya-papagayo-costa-rica","san-blas-panama","samana-dominican-republic"]}` |

## Missing artifacts

- `partner-pitch/DIDI-ANCHOR-CITY-CROSSWALK.json`
- `DiDi entry in finance/PARTNER-SHEET-IDS.json`
- `DiDi transparent economics sheet artifact`
- `proposal economics_url`
- `DiDi deck-studio artifacts`
- `fresh render/spine identity receipt after cascade`

## Status

**research-needed / repair-needed.** Country evidence is adequate for 80:20 inheritance, but global route-cluster stamping, the DiDi roster, demand provenance, finance identity, country references, phase route bindings, sheet, sidecar/deck delivery chain, and fresh render receipts must be fixed before any proposal-complete claim.

The JSON companion contains every city record, exact count methodology, all stale route IDs, Gate A–G check objects, and machine-readable next actions.
