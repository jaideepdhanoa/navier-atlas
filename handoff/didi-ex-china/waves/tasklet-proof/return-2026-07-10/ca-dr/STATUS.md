# Central America + Dominican Republic P0 — T2/T3/T4

As of **2026-07-10**. Evidence research only; **no finance materialization**.

## Classification count

| Classification | Count |
|---|---:|
| `usable_for_base_case` | 2 |
| `benchmark_only` | 0 |
| `not_publicly_supported` | 2 |
| `permission_required` | 2 |
| **Total records** | **6** |

## What can materialize in the evidence layer

- **T2 / `rn-7e59f984abec` — Paquera → Puntarenas:** MOPT Cuadro 6.2 gives **642,133 one-way passenger journeys in 2024**. Opposite direction is published separately; do not double or halve.
- **T2 / `rn-eb4ca32edbef` — Playa Naranjo → Puntarenas:** MOPT Cuadro 6.2 gives **317,859 one-way passenger journeys in 2024**. Opposite direction is published separately; do not double or halve.
- Source semantics: passengers transported by named ferry direction, not vehicles, tickets, round trips, or visitors. The table is labeled `(Miles)`; the ledger normalizes the extracted six-digit figures to passenger persons (642.133 thousand and 317.859 thousand), not millions.
- ARESEP fares were already banked. These records do not assert realized yield and do not authorize a finance cascade.

## What stays null / on hold

- **T3 / `rn-8fb072f5a8a8` — Puerto Cartí → Cartí Sugdup:** `permission_required`. Official Guna rules say an operation permit is granted by motivated resolution, but no route-specific resolution, permit holder, or approved operator was recovered.
- **T3 / `rn-87eec178e86f` — El Porvenir → Cayos Limones:** `permission_required` for the same reason. General maritime authority, vessel, transfer, excursion, and tourism evidence is insufficient.
- **T4 / `rn-64effc46b976` — Samaná → Sabana de la Mar:** hard null. A reseller currently displays the exact crossing, a US$16 ticket, and selectable times, but no primary operator, permit, official timetable, service-day statement, or official tariff was found. Do not promote the reseller evidence.
- **T4 / `rn-c3a4ef933700` — Cayo Levantado ↔ Samaná:** the Ministry of Tourism confirms regular daily boat taxis, but publishes no exact-route passenger count. Cruise-port, hotel, excursion, destination-visitor, airport, and whale-watching totals are not usable as route passengers.

## Exact next action

1. Ask the **Congreso General Guna / Secretaría de Transporte Marítimo** for the motivated resolution number, permit holder/operator, validity dates, vessel(s), and exact authorized OD for each Panama route. Do not substitute the AMP auxiliary-industry license list.
2. Ask **APORDOM / the Samaná and Sabana de la Mar port authorities or harbor masters** for the licensed carrier, operating authorization, official timetable/service days, and approved passenger tariff for `rn-64effc46b976`.
3. Ask **APORDOM/MITUR and the Samaná launch operators** for annual manifests or boarding records explicitly split to Samaná public launch ↔ Cayo Levantado Public Dock, with direction and unit semantics. Keep `rn-c3a4ef933700` null unless that exact OD is supplied.

Full source quotes, dates, local-language queries, rejected nearby evidence, and null rationales are in `EVIDENCE-LEDGER.json`.
