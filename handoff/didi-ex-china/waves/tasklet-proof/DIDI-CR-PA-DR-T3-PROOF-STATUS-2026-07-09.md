# DiDi CR / PA / DR T3 proof status — 2026-07-09

**Sealed commit:** `ba48bc5d`  
**Wave finance gate:** `blocked_pending_primary_evidence`  
**JSON ledger:** `DIDI-CR-PA-DR-T3-PROOF-2026-07-09.json`

This was an incremental proof pass: the sealed handoff, exact route spine, prior deepening artifact, and country reference were read before new searches. Every requested item has a disposition, including explicit nulls; the wave does **not** have complete non-null finance proof.

## Route dispositions

| Route | Proof status | Finance gate | Disposition |
|---|---|---|---|
| `rn-7e59f984abec` Paquera ↔ Puntarenas | Current schedule and official fare proven; official annual one-way passengers **null** | `t3_buildable_null_only` | Keep current. Adult CRC 810, minor CRC 480, senior exempt, effective 2026-07-01. No demand/revenue. |
| `rn-eb4ca32edbef` Playa Naranjo ↔ Puntarenas | Current operator service and official fare proven; official annual one-way passengers **null** | `t3_buildable_null_only` | Keep current. Adult CRC 1,000, minor CRC 600, senior exempt, effective 2026-07-01. No demand/revenue. |
| `rn-55b63e976bb7` Marina Papagayo ↔ Four Seasons Papagayo | No current scheduled-service proof | `t3_buildable_null_only` | Remain `future_opportunity_not_current_scheduled`; no current economics. |
| `rn-8fb072f5a8a8` Puerto Cartí ↔ Cartí Sugdup | General Guna permit authority proven; exact-route approval not found | `blocked_pending_primary_evidence` | No Panama base-case economics until Guna route/operator/boarding approval. |
| `rn-87eec178e86f` El Porvenir ↔ Cayos Limones | General Guna permit authority proven; exact-route approval not found | `blocked_pending_primary_evidence` | No Panama base-case economics until Guna route/operator/boarding approval. |
| `rn-64effc46b976` Samaná ↔ Sabana de la Mar | Primary current operator, timetable, and fare all **null** | `blocked_pending_primary_evidence` | Keep `current_route_evidence_primary_confirm_needed`; reseller/social claims are not model truth. |
| `rn-c3a4ef933700` Samaná ↔ Cayo Levantado | Official current daily/regular boat-taxi activity proven; volume and yield **null** | `t3_buildable_null_only` | Narrow current-activity statement only; no whale/tourism/cruise conversion and no revenue. |

**Held null:** Cartí ↔ Colón remains an unsealed research concept with no route ID, permission, operator, demand, fare, or economics.

## Costa Rica fares and FX

ARESEP Resolution `RE-0074-IT-2026`, published 2026-06-26 and effective 2026-07-01, supplies current passenger classes:

- **Puntarenas–Paquera:** adult CRC 810; minor CRC 480; senior exempt.
- **Puntarenas–Playa Naranjo:** adult CRC 1,000; minor CRC 600; senior exempt.

BCCR official **venta** reference rate on 2026-07-09: **453.77 CRC/USD**. Using `USD = CRC / 453.77`:

- Paquera: adult **$1.7850**, minor **$1.0578**, senior **$0**.
- Playa Naranjo: adult **$2.2038**, minor **$1.3223**, senior **$0**.

These are regulated published passenger fares and reporting conversions, **not realized operator yield**. Vehicle tariffs were not used.

## Demand result

No defensible official annual one-way passenger number was recovered separately for either Gulf of Nicoya route. MOPT official reporting, ARESEP material, MOPT/INEC/open-data searches, and both operator sites were checked. Public sources proved current fares/schedules but did not expose a route/year passenger value with explicit passenger and direction semantics. No vehicle, terminal, tourism, or peak-period values were substituted.

## Dominican Republic result

- **Samaná–Sabana de la Mar:** APORDOM, MITUR/GoDominicanRepublic, INTRANT, municipal/operator-oriented searches, resellers, and social leads did not yield a primary current operator page, current timetable, or current fare/effective date. All remain null.
- **Samaná–Cayo Levantado:** the Dominican tourism authority states that boat taxis depart regularly from Samaná port and bring visitors daily to the island. This is `current_ops_proof_only`; it provides no passenger count, direction split, fare, or realized yield.

## Guna permission result

Official Guna sources establish the governance gate:

- The Guna maritime authority defines a transit permit as a document issued by the Secretaría de Transporte Marítimo authorizing a vessel to transit Gunayala territorial waters.
- Maritime Regulation Article 123 states: “El permiso de operación se concederá mediante resolución motivada.”

No route-specific resolution, permit number, approved operator, boarding authorization, timetable, or fare was recovered for either sealed Panama OD. Both remain `permission_required`; Panama base-case economics are blocked.

## Country-reference opex source gaps

At `ba48bc5d`, **Costa Rica, Panama, and Dominican Republic are absent** from `finance/model/country-reference.json`. For each country, the missing operating/source fields are only:

- `electricity_usd_per_kwh` + `electricity_basis`
- `grid_co2_kg_per_kwh` + `grid_co2_basis`
- `captain_crew_usd_per_year` + `crew_basis`
- `marina_overhead_usd_per_year` + `marina_basis`

No fallback-country opex should be used. CAPEX, route demand, fares, and geometry were not treated as country-reference opex-source fields.
