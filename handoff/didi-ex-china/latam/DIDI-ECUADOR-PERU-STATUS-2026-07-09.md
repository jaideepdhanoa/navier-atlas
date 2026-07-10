# DiDi Ecuador + Peru deepening — Wave B status

**As of:** 2026-07-09  
**Artifact:** `DIDI-ECUADOR-PERU-DEEPENING-2026-07-09.json`  
**Validation:** PASS (`python3 json.load` plus required-key, count, unique-source, route-ID and null-demand assertions)  
**Repository:** not edited.

## Completion status

| Market group | Status | Publication treatment |
|---|---|---|
| Galápagos (Santa Cruz, Isabela, San Cristóbal, Floreana) | **research-complete / seal-needed**, with P0 route-stamp blocker | Publish Atlas/current-launch context only after stamp repair; **do not claim DiDi island service** |
| Lima / Callao | **research-complete / seal-needed** | `lima-peru` is the only Wave B Atlas city explicitly supported by DiDi’s official roster; do not extend that proof to a specific Callao pier without service-area confirmation |
| Paracas / Ballestas | **research-complete / seal-needed** | Publish current excursion opportunity and sourced demand context; do not claim DiDi Paracas service or a sealed Navier route |
| Pisco / San Andrés | **research-needed** | Hold passenger-route and local-DiDi claims; DPA authorization, exact BP, brief and geometry remain unresolved |

Overall status: **research-complete for three market groups; research-needed for Pisco/San Andrés; not complete until P0 data repair, Grok seal/render QA and finance cascade.**

## DiDi operating evidence — no island overclaim

- Official DiDi Ecuador page currently names **Guayaquil and Quito only**. None of the four Galápagos cities is named.
- Official DiDi Peru city roster currently names **Arequipa, Cusco and Lima**. It does not name Paracas or Pisco/San Andrés.
- Exact Wave B Atlas match: **`lima-peru` only** (`city_supported`).
- The other six Wave B city IDs are **country-supported only** and require a visible “local service not verified” caveat:
  - `santa-cruz-galapagos-ecuador`
  - `isabela-galapagos-ecuador`
  - `san-cristobal-galapagos-ecuador`
  - `floreana-galapagos-ecuador`
  - `paracas-peru`
  - `pisco-san-andres-peru`

## Exact Atlas baseline and corruption finding

Canonical-derived baseline contains seven exact city IDs and three exact current Galápagos route-ID matches:

1. `e__santa-cruz-galapagos-ecuador__puerto-ayora__isabela-galapagos-ecuador__puerto-villamil`
2. `e__santa-cruz-galapagos-ecuador__puerto-ayora__san-cristobal-galapagos-ecuador__puerto-baquerizo-moreno`
3. `e__santa-cruz-galapagos-ecuador__puerto-ayora__floreana-galapagos-ecuador__puerto-velasco-ibarra`

**P0 corruption:** the `galapagos-ecuador` stamp currently contains 46 routes whose endpoints are outside all four member cities, while all three real member routes are stamped outside the cluster. Do not inherit that stamp set into DiDi map scope, finance or a deck. This artifact identifies the defect but does not patch the repo.

The requested `/tmp/navier-atlas` checkout was not mounted in this subagent sandbox. Exact city/route findings come from the 2026-07-09 canonical-derived LATAM audit and scope ledger. Every BP still requires canonical BP-ID/name/coordinate revalidation.

## Boarding-point and corridor inventory

**12 researched records:**

- **8 source-verified real-world boarding points:** four Galápagos piers; El Chaco; Muelle Dársena/Plaza Grau; Marina Club; Muelle Canottieri.
- **1 candidate needing authorization:** DPA San Andrés.
- **2 non-BP destination POIs:** Islas Ballestas and Islotes Palomino.
- **1 reject/drop as passenger BP:** Terminal Portuario General San Martín.
- **0 exact Atlas BP IDs matched** because raw canonical BP files were unavailable.

**7 corridor records:**

- **3 exact existing route IDs:** the Galápagos links above.
- **2 current excursion opportunities with `route_id: null`:** El Chaco–Ballestas and Callao–Palomino.
- **2 future-only concepts with `route_id: null`:** Lima/Callao–Paracas and DPA San Andrés–El Chaco.
- No new route ID was invented.
- Ballestas and Palomino need hand waypoints/operator tracks. The Palomino source reports “11 miles / 32 km,” an internally inconsistent conversion; it is flagged and excluded from geometry/economics.

## Demand and fare ledger

- **Galápagos 2025:** 290,404 tourist arrivals; 62% foreign, 38% national; 79% land lodging, 21% aboard. This is archipelago TAM, not route demand.
- **Galápagos airports 2024:** Baltra 246,434 entries / 241,704 exits; San Cristóbal 104,242 entries / 110,199 exits. Airport traffic is not maritime demand.
- **Galápagos launches:** official page publishes USD 30 per person per route, 2–3 hours, launches up to 20 passengers; daily context for Isabela/San Cristóbal and Tuesday/Thursday for Floreana; January–June calmer than July–December.
- **Lima airport 2025:** 25.5 million passengers (15.22 million domestic; over 10.27 million international; over 1.6 million international transfers). Top-of-funnel only.
- **Pisco airport 2024:** report chart gives a rounded 0.7% share of the 7.5 million-passenger AdP network; no precise passenger count is derived. Pisco aircraft operations were mainly instruction/military, not commercial.
- **Ballestas 2024:** MINAM reports 609,253 visits. Mincetur names El Chaco and publishes average commercial price context of PEN 35–40 high season / PEN 30–35 low season. The 2021 nationality split appears anomalous and is quarantined pending reconciliation.
- **Palomino 2023:** official Mincetur inventory reports 14,898 visitors (8,934 foreign; 5,964 national), PEN 11 protected-area entry, all-year/weather-dependent context, and three Callao origins. Commercial transport fare remains unknown.
- **Every corridor’s `annual_one_way_pax` remains `null`.** No tourism, attraction or airport count was converted into route riders.

## Source and artifact counts

- 22 sources: 21 official web sources + 1 internal canonical-derived audit.
- 7 cities; 1 city-supported, 6 country-supported only.
- 12 BP/POI records; 8 verified BPs, 1 candidate, 2 POIs, 1 reject.
- 7 corridors; 3 exact route IDs, 2 current excursion records, 2 future-only concepts.
- 9 demand/fare records; 0 with annual one-way route passengers.
- Brief maturity: 6/7 present; `pisco-san-andres-peru` missing.
- 11 gaps: 2 P0, 8 P1, 1 P2.

## Blockers and owners

1. **P0 — Atlas data/geometry:** repair Galápagos stamps and run inheritance/no-shrink/render QA.
2. **P0 — Atlas repository owner:** recheck all BPs and endpoints against the live canonical checkout.
3. **DiDi partnership:** verify service areas for Galápagos, Callao piers, Paracas and Pisco/San Andrés; only Lima is city-supported today.
4. **Authority/operators:** obtain route manifests, monthly ridership, sailings, cancellations, load factors, fares and tracks.
5. **FONDEPES/APN/Capitanía:** establish DPA San Andrés structural status and passenger authorization.
6. **Canonical content:** create a partner-neutral `pisco-san-andres-peru` brief.
7. **Finance:** wait for sealed geometry and route-level evidence; do not use broad tourism totals as riders.

## Do not publish

- Corrupted Galápagos stamp set.
- DiDi service on any Galápagos island, at a Callao pier, in Paracas or in Pisco/San Andrés without direct proof.
- Any marine route as DiDi-operated.
- General San Martín as a passenger BP, DPA San Andrés as passenger-capable, or Ballestas/Palomino as landing BPs.
- Straight-line route geometry, inferred route IDs, converted tourism/airport demand, or the inconsistent Palomino distance pair.
- DiDi-specific copy inside canonical city briefs.
