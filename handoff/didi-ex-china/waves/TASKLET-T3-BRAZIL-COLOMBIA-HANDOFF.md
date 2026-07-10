# Tasklet T3 handoff — DiDi Brazil / Colombia economics

**From:** Grok · Brazil/Colombia G2 seal · `2026-07-10T02:14:11Z`  
**Status after Grok:** `seal-complete / cascade-needed`  
**Do not:** invent L3 demand, annualize peak-day counts, use Grab census, or cascade on catch-all `didi` market.

## What Grok sealed

### Brazil — Rio public ferries (4 exact gold route IDs)

- `rn-1886629dbf0c` — Praça XV ↔ Arariboia (Niterói) — 2.7 nm — `current_scheduled`
- `rn-80f0d0ebe0bd` — Praça XV ↔ Charitas (Niterói) — 4.4 nm — `current_scheduled`
- `rn-00bb6ded4be5` — Praça XV ↔ Paquetá — 9.2 nm — `current_scheduled`
- `rn-369ef0eb69d9` — Praça XV ↔ Cocotá — 6.0 nm — `current_scheduled`

### Colombia — geometry baseline only

- `rn-aa790551baa7` — Club de Pesca Marina ↔ Bocachica (Tierrabomba) — **service unverified**

### Held null (no route_id)

- Cais da Lapa ↔ Vila do Abraão (Estação Abraão) — `historical_operation_current_timetable_unverified`
- Costa da Lagoa lacustrine line — `current_service_evidence_route_geometry_unsealed`
- Muelle La Bodeguita ↔ Isla Grande / Rosario — `la_bodeguita_bp_and_destination_split_unsealed`
- Barranquilla Río-Bus — `future_project_not_current_scheduled`

## Tasklet owns next

1. Annual one-way pax by Rio line (Arariboia, Charitas, Paquetá, Cocotá) + confirmed fare effective year → USD yield.
2. Optional: La Bodeguita exact BP/coords + destination split before any Rosario finance row.
3. Río-Bus stays future until current scheduled operation proof.
4. Country-reference rows for Brazil/Colombia if missing before cascade.
5. Run aggregate → growth → Sheet only on sealed route IDs; leave unsupported null.

## Spine artifact

- `handoff/didi-ex-china/waves/BRAZIL-COLOMBIA-ROUTE-SPINE-FOR-TASKLET-2026-07-09.json`
- Receipt: `handoff/didi-ex-china/waves/G2-BRAZIL-COLOMBIA-SEAL-RECEIPT-2026-07-09.json`

## Partner proof reminders

- 99 city-supported: Rio, Florianópolis (not Angra city-level).
- DiDi city-supported: Cartagena, Barranquilla.

