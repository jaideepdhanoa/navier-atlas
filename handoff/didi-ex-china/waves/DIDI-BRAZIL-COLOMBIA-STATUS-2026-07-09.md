# DiDi × Navier — Brazil via 99 + Colombia deepening

**As of:** 2026-07-09  
**Status:** **research-complete / seal-needed**. No corridor is finance-base-case ready: route-level annual one-way passenger counts remain unavailable.

## Scope completed

- Read `CLUSTERS.json`, all five canonical city briefs, `ROUTES.json`, the DiDi partner JSON, `FEATURES_BY_TYPE.json`, and the BP crosswalk.
- Researched five existing Atlas cities: Angra/Ilha Grande, Florianópolis, Rio, Cartagena, and Barranquilla.
- Captured 20 sources, prioritizing 99, DiDi, municipal/state transport, DIMAR, official tourism, airports, and operators.
- Reviewed 17 priority terminals/POIs: 10 verified existing BPs, 5 coordinate/source-confirmation candidates, and 2 non-BP POIs.
- Defined 11 current/historical/future corridor records. Five use exact existing `ROUTES.json` IDs; every other `route_id` is null.
- Added 11 demand/fare records with explicit non-conversion boundaries. `annual_one_way_pax` remains null in all 11.

## Partner coverage proof

- **99 city-supported:** Rio de Janeiro and Florianópolis appear in the official 99 city inventory.
- **99 country-supported only:** Angra dos Reis did not appear in the fetched official city list; do not claim city-level 99 service.
- **DiDi city-supported:** official DiDi Colombia pages name Cartagena and Barranquilla.

## High-value findings

### Rio de Janeiro

- Four exact, existing public-ferry route IDs are usable for geometry continuity:
  - `rn-1886629dbf0c` — Praça XV → Arariboia, 2.7 nm
  - `rn-80f0d0ebe0bd` — Praça XV → Charitas, 4.4 nm
  - `rn-00bb6ded4be5` — Praça XV → Paquetá, 9.2 nm
  - `rn-369ef0eb69d9` — Praça XV → Cocotá, 6.0 nm
- State evidence reports **58,000+ system boardings in one record day** and **7,928 on Charitas** that day. These are peak-day observations and must not be annualized.
- Current-fare notice shows **R$5.00** on Arariboia, Cocotá and Paquetá; the notice's effective year needs confirmation. Charitas has a **R$7.70** 2025 benchmark.
- RIOgaleão reported **17,906,990 passengers in 2025**; this is broad top-of-funnel context only.

### Cartagena

- DIMAR confirms **Muelle La Bodeguita** as an authorized public-passenger terminal toward island destinations.
- Official tourism data reports **619,282 terminal entries in 2023**, versus 586,160 in 2022 (+6%). This is mixed terminal traffic, not a single route or direction.
- One operator currently displays **COP115,000** for the Cartagena–Isla Grande transfer plus **COP40,000 port tax**, with departures 08:00–09:00, return 14:00 and about 50 minutes. Treat as one product benchmark, not a market average.
- Exact Atlas route `rn-aa790551baa7` (Club de pesca marina → Bocachica, 5.74 nm) exists, but current scheduled service was not verified.

### Angra dos Reis / Ilha Grande

- Official municipal sources validate **Cais da Lapa** and the **Vila do Abraão ferry/Estação Abraão** infrastructure.
- A 2015 municipal notice reported a 40-minute Angra–Abraão catamaran. It is historical evidence; current timetable, fare and ridership remain unresolved.
- More than **190,000 cruise visitors** were reported for the prior season. Do not convert this to island-ferry demand.

### Florianópolis

- Official municipal study says regular lacustrine transport exists only on **Lagoa da Conceição**, serving land-isolated **Costa da Lagoa**.
- Operator page displays a **R$30** fare and daily service, but fare basis, update date, exact stop sequence and annual ridership need confirmation.
- Floripa Airport reported **5.1 million passengers in 2025**; this is not route demand.

### Barranquilla

- Río-Bus is supported as an official project/demonstration, **not as verified current scheduled service**.
- All timetable, fare, station and passenger-demand fields remain null.
- Airport throughput was **3,184,185 passenger movements in 2023**; it cannot be converted to river demand.

## Canonical brief maturity (5-point)

| City | Score | Main enhancement |
|---|---:|---|
| Angra/Ilha Grande | 4.0 | Add authoritative terminals, current service/fare and assumption ledger |
| Rio | 3.7 | Bind exact route IDs; replace unquantified volume claims with dated evidence |
| Cartagena | 3.8 | Bind La Bodeguita; add official terminal entries and operator benchmark caveats |
| Florianópolis | 3.1 | Lead with verified Costa da Lagoa service; separate future coastal routes |
| Barranquilla | 2.6 | Replace Wikipedia-heavy sourcing; classify Río-Bus as future until operational proof |

Canonical briefs should remain partner-neutral. The JSON contains a separate 99/DiDi narrative block for the sub-proposal.

## Critical blockers

1. Current Angra–Abraão timetable, fare and annual route passengers.
2. Monthly/annual Rio boardings by line and confirmed 2026 fare effective dates.
3. Costa da Lagoa stop GIS, capacity, fare basis and passenger history.
4. Exact La Bodeguita BP/coordinate and terminal traffic split by destination/operator/direction.
5. Cartagena operator product basis and exact Isla Grande dock.
6. Río-Bus current phase, stations, operator, timetable, fare and demand study.
7. Atlas BP parent/catchment cleanup: Angra and Rio records are heavily cross-assigned; Cartagena includes Santa Marta/general POIs.

## Files

- Structured artifact: `DIDI-BRAZIL-COLOMBIA-DEEPENING-2026-07-09.json`
- This status: `DIDI-BRAZIL-COLOMBIA-STATUS-2026-07-09.md`

No repository files were edited.
