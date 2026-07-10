# DiDi × Navier Costa Rica / Panama / Dominican Republic — status

**As of:** 2026-07-09  
**Status:** scope/source audit research-complete; authority BP seal and finance inputs research-needed  
**Publication:** conditional internal use only; not finance-ready  
**JSON:** `/tasklet/agent/home/didi-ex-china-audit/waves/DIDI-COSTA-RICA-PANAMA-DOMINICAN-DEEPENING-2026-07-09.json`

## Completion receipt

- Normalized **122 sources / 122 unique URLs**. Every source now carries title, publisher, date (nullable), access date, exact proof, confidence, market, category, publication use and research status.
- Inventoried all baseline BP source URLs without upgrading weak evidence: **13 high-confidence**, **77 low-confidence OSM map references**, **30 medium**, **1 medium-high**, **1 low-medium**.
- Added explicit country/city DiDi coverage reconciliation, publication status, research-complete/research-needed lists, registry reconciliation, and route-match basis.
- JSON parses successfully and structural assertions passed: no duplicate baseline BP IDs, no non-null annual route demand, and route IDs occur only on recorded exact matches.
- Repository was **not edited**.

## Exact DiDi coverage guardrails

| Atlas city ID | Official current DiDi evidence | Allowed claim | Unsupported claim |
|---|---|---|---|
| `nicoya-papagayo-costa-rica` | Official Costa Rica list names Liberia, San Carlos and San José | Liberia is a verified Guanacaste gateway overlap | DiDi at each Papagayo/Nicoya terminal, Paquera, Playa Naranjo or beach landing |
| `san-blas-panama` | Official page/list names Ciudad de Panamá only | Panama City urban origin/gateway | Direct DiDi service at Cartí, Guna Yala, El Porvenir or island communities |
| `samana-dominican-republic` | Official Dominican list names seven cities, not Samaná | Dominican country/city-list presence and a future Samaná opportunity | Current local DiDi service in Samaná, Sabana de la Mar or Las Galeras |

San Blas/Guna Yala is therefore an access-chain and local-partnership opportunity, not a direct DiDi service claim. Samaná use cases remain partner opportunity framing until local service is proven.

## No-shrink and boarding-point reconciliation

- **PASS:** all **123 existing Atlas BP IDs** were preserved with no duplicates or silent drops:
  - Costa Rica: **39 / 39**
  - Panama: **48 / 48**
  - Dominican Republic: **36 / 36**
- Added one **additive, missing-registry candidate**: the Sabana de la Mar ferry landing. It has no accepted BP ID or coordinate and requires a primary operator/authority source.
- Research artifact now contains **124 BP records**: 123 preserved Atlas records + 1 additive missing candidate.
- Classifications: 19 verified existing facilities, 10 needing boarding confirmation, 76 needing coordinate and primary-source confirmation, 5 future opportunities, 11 non-BP POIs and 3 reject/drop records.
- `Colón Caribbean waterfront` remains an undefined generic endpoint, not a BP. The generic Samaná–Las Galeras route endpoints still need registry binding review; do not auto-substitute by name.

## Corridor coverage

- **11** priority corridors reviewed.
- **10** retain exact existing `ROUTES.json` IDs, each labeled with exact-ID-and-endpoint-pair match basis.
- The speculative Cartí–Colón concept correctly remains `route_id: null`, requires coastal hand waypoints and is excluded from publication/economics.
- Existing Atlas route IDs do **not** prove current service, fare, passenger volume or boardability; each corridor’s `evidence_state` controls those claims.

## Demand, fares and service evidence

### Costa Rica

- Official ICT 2024 context: 2,661,488 air tourist arrivals nationally and 881,289 tourist entries through Daniel Oduber airport. Neither was converted into route demand.
- ARESEP adult one-way fares effective 1 July 2026: **CRC 810** Puntarenas–Paquera and **CRC 1,000** Puntarenas–Playa Naranjo.
- Naviera Tambor publishes eight Paquera departures per direction.
- Newly captured COONATRAMAR operator schedule for **4–20 July 2026** shows eight departures from each end: **05:15, 07:30, 10:00, 12:30, 14:30, 16:30, 18:45, 20:30**.

### Panama / Guna Yala

- Official Visit Panamá evidence confirms 365+ islands and explicitly describes taking a small boat from Cartí to the destination island.
- Guna-owned operator material supports advance coordination, local control and Cartí-area boat-transfer patterns, but not fixed public schedules or annual route demand.
- No current DiDi service, annual visitor series, route-pax count or finance-grade fare was found for Cartí/Guna Yala.

### Samaná

- Official Q1 2024 whale-observation participation: **61,558 visitors**; retained only as seasonal destination context.
- Official 2025 whale season: **15 January–31 March**.
- Official 2024 El Catey throughput: **101,555 commercial passengers**; tourism supply approximately **2,600 rooms / 46 hotels**. Neither was converted into water-route demand.
- Commercial seller evidence supports the Samaná–Sabana de la Mar crossing and a one-hour trip, but the US$16 reseller fare and indexed timetable remain non-finance-grade until primary confirmation.

**All 12 demand records retain `annual_one_way_pax: null`.**

## Brief maturity

- Nicoya/Papagayo: **76/100** — retain structure; add official ferry schedule/fare context and eventual route-pax evidence.
- San Blas: **68/100** — governance framing is strong; remove unsupported timing/income claims, distinguish present Guna transfers from future corridors, and verify docks with Guna authority.
- Samaná: **74/100** — retain whale-sensitive framing; separate public ferry, excursion/resort and future app-orchestration use cases.

Canonical briefs stay partner-neutral. DiDi-specific language remains isolated in `partner_narrative_notes`.

## Research complete

1. Official DiDi city-list/page reconciliation for all three countries.
2. Canonical Atlas city-ID and 123-BP no-shrink reconciliation against the supplied ledger/input extraction.
3. Exact existing route-ID binding for ten matched corridors.
4. Costa Rica regulated fares and accessed operator schedules for both Gulf of Nicoya ferries.
5. Official Cartí small-boat access-chain evidence.
6. Official Samaná whale-season, airport and tourism-supply context.
7. Brief maturity, source-quality and publication guardrails.

## Research needed / owners

1. **Execution environment / Grok handoff:** restore the pinned `/tmp/navier-atlas` snapshot and rerun file-level ID/count/hash checks before seal. The snapshot was unavailable for a fresh re-read in this session; the preserved extraction was cross-checked to the DiDi scope ledger counts.
2. **Finance research:** obtain route-level annual passenger series for the priority corridors; keep all economics demand null meanwhile.
3. **Research / Dominican transport:** identify the primary Samaná ferry operator, exact terminals, both-direction timetable, service days and walk-up fare.
4. **Guna partnerships + geometry:** confirm ports, community docks, permissions and local operating model with Guna authority/operators.
5. **Partner coverage:** obtain app or written local-service evidence before any terminal-level Costa Rica, Guna Yala or Samaná DiDi claim.
6. **Geometry/registry:** replace OSM/property-only candidate evidence with authority/operator boardability and accepted coordinates.
7. **Dominican regulatory research:** extract current whale-sanctuary vessel, noise, speed and permit constraints.

## Do not publish or model

- Any non-null annual route passenger demand from broad airport, visitor, hotel or whale counts.
- Direct DiDi service in Cartí/Guna Yala or Samaná.
- OSM-only points as verified boarding locations.
- Cartí–Colón as an existing corridor or with a route ID.
- Guna panga, public ferry, excursion, resort transfer and future water taxi as one service class.
- The Samaná reseller fare/timetable as finance-grade.
