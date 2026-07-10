# DiDi Ecuador (Galápagos) / Peru T3 proof status — 2026-07-09

## Finance gate

**`blocked_pending_primary_evidence`**

No sealed Galápagos OD has a public exact annual passenger count or a defensible realized route load factor. Ballestas has an official **visitor-arrival** series, not route/embarkation passenger semantics; Palomino has no public monthly or annual passenger series. Posted fares remain customer benchmarks, not realized operator or DiDi yields.

The exact supplied spine seals only the three Galápagos route IDs below. Ballestas and Palomino remain unsealed candidate excursion circuits in the prior deepening artifact; this pass minted no IDs and substituted no ODs.

## Sealed route dispositions

| Exact sealed route | Annual route passengers | Realized load factor | Fare | Current operation | Permission / DiDi | Finance |
|---|---:|---:|---|---|---|---|
| `e__santa-cruz-galapagos-ecuador__puerto-ayora__isabela-galapagos-ecuador__puerto-villamil` — Puerto Ayora ↔ Puerto Villamil | **null — `not_publicly_supported`** | **null — `not_publicly_supported`** | USD 30 regular per person/per route; USD 40 special; **`benchmark_only`** | DPNG lists Santa Cruz→Isabela 13:45–16:00 and reverse 06:00–08:30; **`current_ops_proof_only`** | Vessel/shipowner route authorization required; no DiDi proof for Puerto Ayora or Puerto Villamil | blocked |
| `e__santa-cruz-galapagos-ecuador__puerto-ayora__san-cristobal-galapagos-ecuador__puerto-baquerizo-moreno` — Puerto Ayora ↔ Puerto Baquerizo Moreno | **null — `not_publicly_supported`** | **null — `not_publicly_supported`** | Same regulated/published semantics; **`benchmark_only`** | Santa Cruz→San Cristóbal 13:45–16:00 and reverse 07:00–09:30; **`current_ops_proof_only`** | Route authorization required; no DiDi proof for either endpoint | blocked |
| `e__santa-cruz-galapagos-ecuador__puerto-ayora__floreana-galapagos-ecuador__puerto-velasco-ibarra` — Puerto Ayora ↔ Puerto Velasco Ibarra | **null — `not_publicly_supported`** | **null — `not_publicly_supported`** | Same regulated/published semantics; **`benchmark_only`** | Santa Cruz→Floreana 08:00–09:45 and reverse 15:00–17:00, Tuesday/Thursday; **`current_ops_proof_only`** | Route authorization required; no DiDi proof for either endpoint | blocked |

### Galápagos fare semantics

- [MTOP Resolution `MTOP-SPTM-2018-0082-R`](https://www.gob.ec/regulaciones/resolucion-mtop-sptm-2018-0082-r), signed **2018-08-13** and effective on publication in Official Register No. 338 on **2018-10-01**, sets **USD 30 regular** and **USD 40 special** passenger-service tariffs.
- Its preferential tariff is 50% of the applicable fare for the listed eligible passenger groups.
- The [current DPNG page](https://galapagos.gob.ec/transporte-entre-islas-pobladas/) says tickets cost **USD 30 per person and per route** and supplies the directional schedule above.
- Classification: **`benchmark_only`**. This is a regulated/published customer fare, not realized yield.
- A complete current all-in stack remains **`not_publicly_supported`**: no defensible primary source established current terminal/dock, tender/water-taxi, booking/payment, or tax components. No anecdotal add-ons were used.

The 2019 official capacity report gives only a non-route benchmark: **84,105 passengers moved between populated islands from 2019-08-19 through 2019-12-31**, across tourism modalities, public transport, and “other.” It is not annualized or allocated to any sealed OD.

## Peru candidate circuit dispositions

### Paracas / Islas Ballestas — no sealed route ID

- **Demand — `benchmark_only`:** MINCETUR [Cuadro N° 94](https://www.gob.pe/institucion/mincetur/informes-publicaciones/6529654-compendio-de-cifras-de-turismo-ano-2025), sourced to SERNANP, reports **618,023 visitor arrivals in 2025** (385,633 national; 232,390 foreign). Monthly totals are 57,022; 65,753; 57,675; 50,974; 40,356; 36,122; 58,919; 49,582; 37,926; 61,413; 47,624; and 54,657.
- These are **visitors**, not labelled boat passenger boardings, one-way trips, or embarkations. No conversion or terminal allocation is permitted.
- **Posted adult stack — `benchmark_only`:** a 2026 commercial page posts S/40 regular or S/60 on named holidays, plus mandatory combined pier-use/SERNANP charges of S/16 at embarkation: **S/56 regular** or **S/76 holiday**. This is a customer quote, not realized yield; payment/tax treatment beyond the page is not independently established.
- [SERNANP](https://visitaareasnaturales.sernanp.gob.pe/anps/reserva-nacional-siipg-islas-ballestas/) separately posts Ballestas entry of S/11 for national adults and a S/17 two-area Paracas/Ballestas promotion; do not infer that either is the allocation inside the seller's S/16 combined charge.
- **Terminal — `conflicting`:** the seller says current embarkation is Muelle El Chaco and La Marina Turística de Paracas is not operating. That does not seal or rebind a route here.

### Callao / Islas Cavinzas e Islotes Palomino — no sealed route ID

- **Demand — `not_publicly_supported`:** no official monthly/annual route or embarkation passenger count was found. Callao/Lima totals are excluded.
- **Official entry — `benchmark_only`:** [SERNANP](https://visitaareasnaturales.sernanp.gob.pe/anps/reserva-nacional-siipg-islas-cavinzas-e-islotes-palomino/) posts S/11 general/national adult, S/5 national minor, and S/5 local adult/minor, with listed exemptions.
- **Commercial stack — `benchmark_only`:** authorized-roster operator Mar Adentro's booking offer shows **USD 60–65 plus 5% service**, or **USD 63–68.25** after that stated service charge. Its tour page says protection and embarkation fees are included, but the exact price variant and any unstated tax treatment remain unresolved. This is not realized yield.
- **Exact-terminal caveat:** Mar Adentro's meeting point is Comandante Fanning 145, La Punta—not the prior artifact endpoint Muelle Dársena / Plaza Grau. Its price is therefore a Palomino activity benchmark, not exact-terminal fare proof.
- **Permission — `permission_required`:** SERNANP says visitors must hire an authorized operator and links an operator roster. The roster's visible extract has no issue/effective date, so authorization must be revalidated before contracting.

## City-level DiDi operation proof

Official DiDi city inventories support only:

- Ecuador: **Guayaquil, Quito** — `current_ops_proof_only`
- Peru: **Lima** (also Arequipa and Cusco, not relevant here) — `current_ops_proof_only`

No official city-level proof was found for **Puerto Ayora, Puerto Villamil, Puerto Baquerizo Moreno, Puerto Velasco Ibarra, Callao, Paracas, or Pisco**; each is `not_publicly_supported`. Inventory omission is not proof of absence, and Lima is not silently promoted to Callao.

## Required next primary evidence

1. CAPAYO/DPNG or licensed-operator monthly manifests by exact Galápagos OD, direction, passenger class, sailings, usable seats, and cancellations.
2. A current official Galápagos all-in customer fee schedule or itemized operator invoices/settlement data.
3. Ballestas embarkation/ticket totals by terminal and route semantics, plus an itemized current operator settlement stack.
4. Palomino monthly passenger/boarding totals by Muelle Plaza Grau, Marina Club, or each exact operator departure point, with current authorization and all-in fare terms.
5. Official DiDi city/service-area statements for any endpoint or gateway not named in the current inventories.

## Geometry and production status

Finance evidence does **not** change geometry. Repo spine status remains **`geometry_stamp_verified / partner_market_bind_deferred / cascade-needed`**. A Galápagos stamp does not itself make a route partner-bound or render-active; Peru candidates remain unsealed. No repository production file, model, partner JSON, Sheet, PR, Slack, or external service was edited.
