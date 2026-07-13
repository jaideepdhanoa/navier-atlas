# inDrive Brazil + Egypt evidence research status — 2026-07-13

## Status

**Overall: `research-needed`.**

- **Brazil / Rio de Janeiro:** `research-complete / seal-needed` for the four supplied Rio ferry routes. Exact route IDs, 2023 one-way boarding semantics, and public comparable fares are present. Grok render/seal QA and the country-reference/model cascade remain outstanding.
- **Brazil / Angra dos Reis–Ilha Grande:** `research-needed`. Strong operator and destination-pool context exists, but no canonical route ID or annual route boarding count was found in the supplied files.
- **Brazil / Florianópolis:** `research-needed`. Official inDrive city evidence and official island/airport context exist; canonical marine routes and route-level one-way demand/fare remain absent.
- **Egypt / Hurghada, El Gouna, Sharm El Sheikh:** `research-needed`. Official inDrive city evidence exists for Hurghada and Sharm; El Gouna is country-supported only. Four supplied demand/fare records were triaged, but none clears production because demand is derived/aspirational and fares are day-trip, Dubai, or legacy proxies.
- **Egypt / Cairo:** distribution context only. Official inDrive city evidence exists, but no exact marine evidence was promoted.

No repository files were edited, no routes were invented, no finance value was created, and no partner capture/commercial overlay was copied.

## Source count

| Country | Unique external sources | Mix |
|---|---:|---|
| Brazil | 8 | 3 official inDrive; Barcas Rio; AGETRANSP; Angra municipality; Florianópolis municipality; Floripa Airport |
| Egypt | 7 | 3 official inDrive city pages; 3 Egyptian Tourism Authority destination pages; El Gouna / Abu Tig Marina operator page |
| **Total** | **15** | Source registers and URLs are in the two ledgers. |

## Current inDrive-operation evidence

| Market | Evidence tier | Verdict |
|---|---|---|
| Brazil | `country_supported` | Official Brazil-localized inDrive service page. |
| Rio de Janeiro | `city_supported` | Official inDrive Rio page. |
| Florianópolis | `city_supported` | Official inDrive Florianópolis page. |
| Angra dos Reis / Ilha Grande | `country_supported` | May inherit existing Atlas geography from Brazil evidence; no exact inDrive city page found. |
| Egypt | `country_supported` | Official Egypt-localized city/service pages. |
| Hurghada | `city_supported` | Official inDrive Hurghada page. |
| Sharm El Sheikh | `city_supported` | Official inDrive Sharm page. |
| El Gouna | `country_supported` | No exact inDrive El Gouna page found; nearby Hurghada evidence does not prove city-level service. |
| Cairo | `city_supported` | Official inDrive Cairo page; retained only for distribution context. |

## Exact route IDs found

### Brazil — 4

All four are in the supplied `corridors-main.json` `brazil` market:

1. `rn-1886629dbf0c` — Praça XV Terminal → Arariboia Terminal
2. `rn-80f0d0ebe0bd` — Praça XV Terminal → Charitas Terminal
3. `rn-369ef0eb69d9` — Praça XV Terminal → Cocotá Terminal
4. `rn-00bb6ded4be5` — Praça XV Terminal → Paquetá Island Terminal

**No exact canonical route ID was found for Angra dos Reis–Ilha Grande or Florianópolis.**

### Egypt — 14 focus/adjacent Red Sea routes

From the supplied corridor and partner files, exactly as recorded:

1. `gcn-6f2754b63b-yango` — Hurghada → El Gouna
2. `gcn-73d7e2f19c-bolt` — Hurghada / El Gouna → Sharm El Sheikh
3. `rn-b06f6971ed47` — Hurghada Marina → Giftun Island
4. `rn-f562c5e3e868` — Marina El Gouna → Giftun Island
5. `rn-c8d1f3720765` — Soma Bay Marina → Giftun Island
6. `rn-3d161664de08` — Hurghada Marina → Sahl Hasheesh Marina
7. `rn-b5e0aa24ef82` — Soma Bay Marina → Sahl Hasheesh Marina
8. `rn-236717891041` — Landmark Marina → Sharks Bay Marina
9. `rn-65d0faf55453` — Landmark Marina → Ras Mohammed
10. `rn-5b13d8a6534e` — Sharm Marina → Landmark Marina
11. `rn-c16a1627130f` — Sharm Marina → Ras Mohammed
12. `rn-42cf3b291895` — Sharks Bay Marina → Ras Mohammed
13. `rn-d0b2645ab338` — Landmark Marina → Sharks Bay Marina
14. `rn-285fc16b29dc` — Sharm Marina → Sharks Bay Marina

Caveats:

- `gcn-6f2754b63b-yango` and `gcn-73d7e2f19c-bolt` retain peer suffixes; inDrive scope inheritance requires registry confirmation rather than renaming.
- `rn-236717891041` and `rn-d0b2645ab338` have effectively identical Landmark–Sharks Bay endpoint labels. Both were preserved, but economics must not aggregate both until canonical ownership/dedup is resolved.
- The supplied Taba route was not included because this assignment focused on Hurghada, El Gouna, and Sharm El Sheikh.

## Supported demand/fare rows

### Brazil — 4 supported geography rows

These rows reuse exact-route geography evidence only. **No DiDi/peer capture rate or commercial overlay is copied.** Annual semantics are gross passenger boardings / one-way passenger-trips across both directions in 2023; one boarding equals one one-way trip, with no doubling, halving, terminal allocation, or daily annualization.

| Route ID | 2023 annual one-way pax | Comparable one-way public fare | Evidence status |
|---|---:|---:|---|
| `rn-1886629dbf0c` | 10,848,719 | BRL 5.00 / USD 0.9741 | Supported exact line |
| `rn-80f0d0ebe0bd` | 825,637 | BRL 7.70 / USD 1.5001 | Supported exact line |
| `rn-369ef0eb69d9` | 278,607 | BRL 5.00 / USD 0.9741 | Supported exact line |
| `rn-00bb6ded4be5` | 1,170,652 | BRL 5.00 / USD 0.9741 | Supported exact line |

The USD values are the supplied geography record’s 2026 comparable-fare conversions, not operator yield and not an inDrive fare. The route record cites the 2026-07-09 Banco Central do Brasil PTAX sell rate of 5.1329 BRL/USD.

Angra–Ilha Grande has a current operator-published **BRL 20.50 / 110-minute** trip, but it remains an unbound context row: `route_id = null`, `annual_oneway_pax = null`, and `production_fare_usd = null`.

### Egypt — 0 production-supported rows; 3 labeled destination-pool candidates + 1 aspirational hold

| Supplied route ID | Candidate annual one-way pax | Candidate fare | Production verdict |
|---|---:|---:|---|
| `gcn-6f2754b63b-yango` Hurghada–El Gouna | 10,402 | $40.80 | **Hold.** Demand is a room/occupancy/stay pool × 5% assumption; fare is explicitly a Dubai placeholder. Production demand/fare remain null. |
| `rn-b06f6971ed47` Hurghada Marina–Giftun | 1,204,586 | $32.00 | **Hold.** Demand is Hurghada airport-arrival pool × 25% excursion assumption; fare is a day-trip product, not exact one-way fare. Production demand/fare remain null. |
| `rn-c16a1627130f` Sharm Marina–Ras Mohammed | 50,000 | $50.00 | **Hold.** Demand is a Ras Mohammed visitor pool, not observed route boardings; fare is a VIP/day-trip proxy. Production demand/fare remain null. |
| `gcn-73d7e2f19c-bolt` Hurghada/El Gouna–Sharm | null | $110.00 | **Hold.** Registry labels route defunct/unserved and aspirational; fare is legacy context. Production demand/fare remain null. |

The ledgers preserve these values only as auditable candidates from the supplied files. They do not promote them into production economics.

## Partner-facing context highlights

### Brazil

- Barcas Rio publishes the Rio commuter crossings and tariffs, including Praça XV–Arariboia at 22 minutes / BRL 5.00 and Praça XV–Charitas at 28 minutes / BRL 7.70.
- Angra municipality reports about 1.8 million annual visitors, including 1.2 million on Ilha Grande. This is destination context, not route demand.
- Barcas Rio publishes Angra–Ilha Grande at 110 minutes / BRL 20.50.
- Florianópolis Airport reports 5.1 million 2025 passengers, including 1.2 million international; the municipal Ilha do Campeche portal requires official or declared maritime transport. Neither metric is marine route demand.

### Egypt

- Egypt’s tourism authority describes Hurghada as a global Red Sea destination with resorts, coastline, coral reefs, water sports, marina activity, and Giftun Island access.
- The authority places El Gouna 25 km north of Hurghada and describes its marinas, canals, lagoons, sailing, and beaches.
- Abu Tig Marina lists boat rentals, utilities, pump-out, fuel, 24-hour security, and dry storage for over 100 boats.
- The authority positions Sharm between Ras Muhammad National Park and Nabq Protectorate, with reefs, resorts, and international-airport access.

## Hold list

1. **Angra / Ilha Grande:** canonical route ID absent; visitor count cannot be converted into one-way route pax.
2. **Florianópolis:** route IDs, route-level annual one-way pax, and route fares all remain null.
3. **Brazil country economics:** captain wage/on-cost, commercial energy, grid CO₂, berth/port administration, and cost index must be sourced before cascade; no fallback country.
4. **El Gouna operation tier:** remain `country_supported`; no exact inDrive El Gouna page found.
5. **Egypt production demand/fare:** all remain null pending observed route throughput or an explicitly approved destination-pool methodology plus exact one-way local fares.
6. **Hurghada/El Gouna–Sharm:** no active service/demand; legacy $110 fare cannot enter economics.
7. **Landmark–Sharks Bay:** duplicate endpoint IDs require dedup/ownership resolution.
8. **Cairo:** distribution context only; marine route IDs/demand/fare/economics remain null.
9. **Egypt country economics:** all five mandatory country-reference inputs must be sourced before model/sheet cascade; no Singapore or neighboring-country fallback.
10. **Commercial overlays:** all inDrive capture, platform revenue, and partner economics remain null; no DiDi/Bolt/Yango commercial overlay was copied.

## Files written and validation

- `INDRIVE-BRAZIL-EVIDENCE-LEDGER-2026-07-13.json`
- `INDRIVE-EGYPT-EVIDENCE-LEDGER-2026-07-13.json`
- `INDRIVE-BRAZIL-EGYPT-RESEARCH-STATUS-2026-07-13.md`

Both JSON ledgers pass `python3 -m json.tool`. Source counts match their source arrays (Brazil 8; Egypt 7). Route-ID counts match their inventories (Brazil 4; Egypt 14).
