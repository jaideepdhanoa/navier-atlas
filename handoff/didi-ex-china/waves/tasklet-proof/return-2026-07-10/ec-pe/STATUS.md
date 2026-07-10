# Ecuador + Peru P1 — T5/T6 status

**As of:** 2026-07-10  
**Base-case materializations:** 0  
**Records:** 6 — 3 `benchmark_only`, 3 `not_publicly_supported`

## T5 — sealed Galápagos exact ODs

A stronger official historical source was found: *Estadísticas Turismo Galápagos — Informe Semestral Enero–junio 2022*, published by the Observatorio de Turismo de Galápagos with movement data credited to GAD Municipal Santa Cruz, Dirección de Desarrollo Productivo y Sostenible.

It reports exact directional **public-maritime-transport passenger movements** for January–June 2022:

- `e__santa-cruz-galapagos-ecuador__puerto-ayora__isabela-galapagos-ecuador__puerto-villamil`: Puerto Villamil → Puerto Ayora, **38,281 arrivals at Santa Cruz**; Puerto Ayora → Puerto Villamil, **39,860 departures from Santa Cruz**.
- `e__santa-cruz-galapagos-ecuador__puerto-ayora__san-cristobal-galapagos-ecuador__puerto-baquerizo-moreno`: Puerto Baquerizo Moreno → Puerto Ayora, **29,578 arrivals at Santa Cruz**; Puerto Ayora → Puerto Baquerizo Moreno, **28,287 departures from Santa Cruz**.
- `e__santa-cruz-galapagos-ecuador__puerto-ayora__floreana-galapagos-ecuador__puerto-velasco-ibarra`: Puerto Velasco Ibarra → Puerto Ayora, **2,751 arrivals at Santa Cruz**; Puerto Ayora → Puerto Velasco Ibarra, **2,314 departures from Santa Cruz**.

These are one-way passenger movements, not round trips, vehicles, tickets, visitors, or sailings. They are **six-month aggregates, not monthly manifests**, and no current/full-year exact-OD series was found. All three are therefore `benchmark_only` / hold. Do not annualize, average, combine directions, or populate `annual_one_way_pax`. USD 30 remains a published fare benchmark only, not realized yield.

## T6 — Peru

- **Ballestas:** no public official passenger-boardings series was found for **Embarcadero turístico de El Chaco, Paracas → Islas Ballestas**. MINCETUR/SERNANP visitor-arrival totals are explicitly excluded: visitor arrivals are not exact-terminal embarkations or route passenger journeys.
- **Palomino:** SERNANP confirms two exact access terminals — **Muelle Plaza Grau** and **Marina Club** — to Islas Cavinzas e Islotes Palomino, but publishes no terminal-level boarding counts. Both records remain hard null.
- Peru route IDs remain `null`/unsealed.

## Exact next action

1. Request from **GAD Municipal Santa Cruz / Dirección de Desarrollo Productivo y Sostenible** and **CAPAYO** a machine-readable monthly extract by origin port, destination port, direction, month, passenger movements/boardings, sailings, cancellations, and reporting coverage for 2022–2026; obtain the data dictionary so boardings are not confused with tickets or visitors.
2. Request from **SERNANP**, **DICAPI/APN**, and the responsible terminal/operator registries monthly boarding or passenger-manifest totals separately for:
   - Embarcadero turístico de El Chaco → Islas Ballestas;
   - Muelle Plaza Grau → Islas Cavinzas e Islotes Palomino;
   - Marina Club → Islas Cavinzas e Islotes Palomino.
3. Keep every annual passenger input null until a full-period exact-OD/exact-terminal source with explicit passenger semantics is received.
