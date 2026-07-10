# DiDi Mexico residual T3 proof — status

**Repository seal:** `jaideepdhanoa/navier-atlas@d3817d9`  
**Scope:** six residual rows in the sealed eight-ID Mexico spine  
**Finance gate:** `t3_buildable_non_null` — **one row can move from null; five retain null annual demand**.

## Decisive result

`ics-aa6ff40d2d` **Punta Sam ↔ Isla Mujeres (car ferry)** is newly buildable with non-null exact-route evidence:

- **2025 annual demand:** APIQROO’s official transbordador table reports **238,128 passenger one-way crossing journeys, both directions combined**. Punta Sam has 116,169 passenger entradas and 121,959 salidas; Isla Mujeres mirrors those values. Use **one endpoint total, 238,128, without doubling or halving**.
- **Published comparable fare:** Ultra Carga’s exact route page publishes **MXN 290 adult passenger, one way**. This is a retail benchmark, **not realized operator yield**.
- **Standardized model candidate:** MXN 290 / the already sealed 2025 World Bank annual-average FX of 19.2375083333333 = **USD 15.07/pax**. This conversion is only a comparator and does not claim the undated live tariff applied throughout 2025.
- **Current operation:** the operator publishes both directions, four departures each way on weekdays and three each way on Saturday/Sunday.
- **Permission:** Mexico’s navigation law establishes that passenger services require permission, but no exact route/operator permit instrument was located. Permission remains a diligence gate rather than a fabricated approval.

Primary demand source: [APIQROO 2025 transbordador table](https://servicios.apiqroo.com.mx/estadistica/datos/informeTransbordador.php?anio=2025)  
Current fare/schedule source: [Ultra Carga Punta Sam–Isla Mujeres](https://ultracarga.com/ruta-punta-sam-isla-mujeres/)

## Route-by-route disposition

| Route ID | Sealed OD | Demand | Fare/timetable | Current operation | Permission | Finance gate | Move from null? |
|---|---|---|---|---|---|---|---|
| `ics-03e3853317` | Cancún Ultramar ↔ Isla Mujeres | `not_publicly_supported` | `not_publicly_supported` for the exact ID | `current_ops_proof_only` | `permission_required` | `blocked_pending_primary_evidence` | **No** |
| `ics-aa6ff40d2d` | Punta Sam ↔ Isla Mujeres | **`usable_for_base_case`: 238,128 (2025)** | **`usable_for_base_case`: MXN 290 adult one way** | `current_ops_proof_only` | `permission_required` | **`t3_buildable_non_null`** | **Yes** |
| `ics-89a8844858` | Puerto Vallarta / Los Muertos → Yelapa | `not_publicly_supported` | `benchmark_only` | `current_ops_proof_only` | `permission_required` | `t3_buildable_null_only` | **No** |
| `ics-de6758216f` | Puerto Vallarta → Punta de Mita | `not_publicly_supported` | `not_publicly_supported` | `not_publicly_supported` | `permission_required` | `t3_buildable_null_only` | **No** |
| `ics-db0930d9d1` | Cabo San Lucas Marina → Los Cabos | `not_publicly_supported` | `not_publicly_supported` | `not_publicly_supported` | `permission_required` | `t3_buildable_null_only` | **No** |
| `ics-b5861451fb` | Palmilla → San José del Cabo Marina | `not_publicly_supported` | `not_publicly_supported` | `not_publicly_supported` | `permission_required` | `t3_buildable_null_only` | **No** |

### Why `ics-03e3853317` remains null

Ultramar currently publishes several separately named Cancún–Isla Mujeres terminals (Puerto Juárez, Playa Tortugas and Playa Caracol) with live fares/schedules. The sealed row’s origin is only **“Ultramar”**, with no boarding-point binding. APIQROO’s large passenger-route total is specifically Puerto Juárez–Isla Mujeres. Assigning it to this duplicate/ambiguous row would violate the no-terminal-allocation rule.

### Why Yelapa remains demand-null

Current exact-route commercial pages publish daily Los Muertos–Yelapa schedules and MXN 550 round-trip products; the existing model carries an MXN 350 one-way benchmark from Yelapa.info. These are differing products/channels and not realized yield. No authority, port, operator annual report or statistical table located an exact annual passenger count, so `annual_one_way_pax` remains null.

### Why the three Pacific opportunity rows remain null

For Puerto Vallarta–Punta de Mita, Cabo San Lucas Marina–Los Cabos and Palmilla–San José del Cabo Marina, public searches found only broad coastal-connectivity language, tours, charters, marinas, resort transfers or nearby services. None establishes the sealed scheduled OD, exact-route annual passenger demand or an exact public scheduled fare.

## Permission disposition

[Article 42 of Mexico’s Ley de Navegación y Comercio Marítimos](https://www.diputados.gob.mx/LeyesBiblio/pdf/LNCM.pdf) says passenger-transport and tourist-cruise services require permission from the Secretaría and separately addresses port-captain permission for passenger/nautical-tourism service using recreational or sport vessels. This proves **permission required**, not permission granted. No route-specific instrument was found for any of the six IDs.

## DiDi-specific Mexico marine census

**Disposition: `not_publicly_supported`; crossing count = `null`.**

DiDi’s official Mexico city index lists road-platform operation in cities including Cancún and Puerto Vallarta. It does **not** publish a DiDi ferry/water-taxi product, a list of DiDi marine crossings, a marine operator partnership, or a marine-network count. The six Atlas rows cannot be relabeled as DiDi-operated crossings, and no Grab/peer census was borrowed. Absence of proof is not asserted as zero.

## Failed-search summary

- No exact boarding-point/terminal allocation for `ics-03e3853317`.
- No exact annual Los Muertos–Yelapa passenger series.
- No scheduled exact-OD proof or finance inputs for the three Pacific opportunity rows.
- No public exact-route permit/concession instrument for any of the six rows.
- No DiDi-specific Mexico marine crossing census.

The complete evidence ledger, exact quotes, units, directionality, passenger/vehicle distinctions, failed searches and model candidate fields are in:

`/tasklet/agent/home/didi-ex-china-audit/proof/DIDI-MEXICO-RESIDUAL-T3-PROOF-2026-07-09.json`
