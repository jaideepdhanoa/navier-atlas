# DiDi × Navier — Brazil via 99 + Colombia deepening

**As of:** 2026-07-09  
**Overall:** **research-complete / seal-needed for partner coverage and corridor classification; finance research-needed.** No corridor is finance-base-case ready because no source establishes route-level `annual_one_way_pax`.

## Publication status

- **Partner narrative:** publishable with evidence tiers and the JSON `do_not_publish[]` guardrails.
- **Current-service context:** publishable for Angra–Ilha Grande, the four Rio ferry lines, Costa da Lagoa, and Cartagena La Bodeguita–island movement at the evidence level stated.
- **Future opportunities:** brief-only; Barranquilla Río-Bus and unverified waterfront concepts must remain labeled future.
- **Economics:** hold. All 18 demand records retain `annual_one_way_pax: null`.
- **Geometry:** seal-needed where `route_id` is null. The five preserved canonical IDs prove only an exact pre-existing Atlas route match, not current service by themselves.

## No-shrink and exact-ID reconciliation

- Scope-ledger clusters preserved exactly: `brazil`, `colombia`.
- All five canonical member city IDs preserved, with no fuzzy or invented IDs:
  - `angra-dos-reis-ilha-grande-brazil`
  - `florianopolis-brazil`
  - `rio-de-janeiro-brazil`
  - `cartagena-colombia`
  - `barranquilla-colombia`
- Five and only five pre-existing exact route IDs are used:
  - `rn-1886629dbf0c` — Praça XV → Arariboia
  - `rn-80f0d0ebe0bd` — Praça XV → Charitas
  - `rn-00bb6ded4be5` — Praça XV → Paquetá
  - `rn-369ef0eb69d9` — Praça XV → Cocotá
  - `rn-aa790551baa7` — Club de pesca marina → Bocachica
- Every other corridor has `route_id: null`.
- The earlier pass recorded a successful repo read. `/tmp/navier-atlas` was no longer mounted during the final improvement pass, so no canonical ID was re-derived or newly created; the exact prior baseline was preserved.

## Current 99 / DiDi operating evidence

| Atlas city | Best evidence tier | Evidence conclusion |
|---|---|---|
| Angra dos Reis / Ilha Grande | `region_supported` | Official 99 inventory exactly lists **Baia da Ilha Grande**. It does not name Angra dos Reis, so do not call this city-supported. |
| Florianópolis | `city_supported` | Official 99 inventory exactly lists Florianópolis. |
| Rio de Janeiro | `city_supported` | Official 99 inventory exactly lists Rio de Janeiro. |
| Cartagena | `city_supported` | Official DiDi Colombia service-city inventory names Cartagena. |
| Barranquilla | `city_supported` | Official DiDi Colombia service-city inventory names Barranquilla. |

## Current transport evidence added

### Angra dos Reis / Ilha Grande

Barcas Rio's current official overview now confirms **Angra dos Reis–Ilha Grande**, **R$20.50**, and **110 minutes**. This upgrades the corridor from historical-only to current-route evidence. The exact detailed calendar/frequency and annual passenger series remain unresolved. The 2015 municipal 40-minute catamaran reference is retained only as historical evidence and must not overwrite the current 110-minute benchmark.

### Rio de Janeiro

Current official line pages now provide fare, travel time, and service-day evidence:

| Corridor | Fare | Time | Service pattern |
|---|---:|---:|---|
| Praça XV–Arariboia | R$5.00 | up to 22 min | weekdays, Saturdays, Sundays/holidays |
| Praça XV–Charitas | R$7.70 | up to 28 min | weekdays only |
| Praça XV–Paquetá | R$5.00 | up to 81 min | weekdays and weekends/holidays |
| Praça XV–Cocotá | R$5.00 | up to 61 min | weekdays only; three published departures per direction |

The prior state record of 58,000+ system boardings and 7,928 Charitas riders on one record day remains a peak-day observation only. It is not annualized.

### Cartagena

- Official 2025 tourism bulletin: **745,079 passengers moved through Muelle La Bodeguita**, **+18.2% vs 2024**, **19,155 sailings**, **56+ island destinations**, **295 registered vessels**, and **100 operators**.
- DIMAR: **48,479 maritime passengers** in **2,830 vessels** over eight days of Holy Week 2025, **+12% vs 2024**, across La Bodeguita, Pegasos, marinas, and other points.
- Official tourism bulletin: **3,822,913 air arrivals in 2025**.
- Existing operator benchmark retained: **COP115,000** plus **COP40,000 port tax** for one Cartagena–Isla Grande product, around 50 minutes, departure 08:00–09:00 and return 14:00.

The annual terminal count, holiday count, airport arrivals, and operator fare are separate records. None may be converted into route-level annual one-way passengers or allocated to Isla Grande without destination/operator/direction splits.

## Inventory and corridor counts

- **27 sources** with exact URLs and proof statements.
- **5 cities** across **2 exact Atlas clusters**.
- **17 priority BP/POI records:** 10 verified real-world BPs, 5 candidates requiring coordinate/source confirmation, and 2 non-BP POIs.
- **11 corridors:** 5 with exact existing route IDs and 6 with null IDs.
- **18 demand/fare records:** 0 with supported annual one-way route passengers.
- **8 unresolved gaps**, each with owner and next action.

## City brief maturity

| City | Score / 5 | Enhancement, not replacement |
|---|---:|---|
| Angra/Ilha Grande | 4.0 | Add current R$20.50/110-minute Barcas Rio benchmark, detailed frequency, and annual line ridership. |
| Rio | 3.7 | Bind the four exact route IDs and add current official fares/times/service days; obtain annual line series. |
| Cartagena | 3.8 | Bind La Bodeguita, add the 2025 745,079-passenger context, and keep mixed-terminal allocation caveats. |
| Florianópolis | 3.1 | Lead with verified Costa da Lagoa service; obtain stop GIS, fare basis, and passenger history. |
| Barranquilla | 2.6 | Keep Río-Bus future-only until current operator/stations/timetable/fare evidence exists. |

Canonical briefs remain partner-neutral. 99/DiDi framing stays in the JSON's separate `partner_narrative_notes` block.

## Research-complete vs research-needed

### Research-complete

- Atlas cluster/city set reconciliation and no-shrink check.
- Best-available 99/DiDi operation tier for every in-scope Atlas city.
- Priority BP inventory and current/historical/future corridor classification.
- Exact preservation of only verified pre-existing route IDs.
- Current official fares/service patterns where exposed, plus broad-demand non-conversion boundaries.

### Research-needed

1. Annual/monthly route passengers by direction for all economics candidates.
2. Angra–Ilha Grande detailed current service calendar/frequency.
3. Rio line-by-line 2025/2026 passenger series.
4. Costa da Lagoa stop GIS, capacity, fare basis, and passenger history.
5. La Bodeguita authoritative Atlas BP/coordinate plus 745,079-passenger split by route, operator, month, and direction.
6. Exact Isla Grande dock and operator fare product basis.
7. Barranquilla Río-Bus current phase, stations, operator, timetable, fare, and demand study.
8. Grok route/BP seal and render QA, followed by the finance cascade only for source-qualified corridors.

## Validation

`python3 -m json.tool` passed after overwrite. Additional assertions passed: unique source/demand IDs, exact five-city no-shrink set, exactly five allowed non-null route IDs, zero invented city IDs, and `annual_one_way_pax == null` in all demand records.
