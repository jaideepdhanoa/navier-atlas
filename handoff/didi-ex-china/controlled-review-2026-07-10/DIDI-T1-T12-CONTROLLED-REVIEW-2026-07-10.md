# DiDi T1–T12 controlled model review — 2026-07-10

## Decision

Reviewed all **47** evidence records from merged PR #218 against the production rule: exact sealed route ID, exact **annual one-way** passengers, supported fare, and country-cost coverage.

| Decision | Count | Meaning |
|---|---:|---|
| A1 — economics evidence-ready | 2 | Exact route and annual one-way demand; still blocked from cascade by missing country-reference coverage. |
| A2 — control-ready | 3 | Exact scope/operation control only; no economics. |
| B — benchmark-only | 10 | Sourced context, but not valid production annual one-way demand. |
| C — hold/null | 32 | Exact evidence gate not cleared. |

## A1 — retain as exact demand inputs

- `rn-7e59f984abec` — Paquera → Puntarenas: **642,133** one-way passenger journeys, named direction, 2024.
- `rn-eb4ca32edbef` — Playa Naranjo → Puntarenas: **317,859** one-way passenger journeys, named direction, 2024.

Both exact IDs and endpoints reconcile to the canonical route graph. The published ARESEP fares may remain explicitly labelled **comparable tariff benchmarks**, not realized yield.

**Cascade blocker:** Costa Rica has no `country-reference.json` row. Do not run aggregate/growth/sheet work until an honest country-cost row is sourced and both economics engines can use it.

## B — correct the annual-one-way fields

- `rn-f451444da7fe` — Rosario → Isla Sabino Corsi: **38,900** is a full summer-season total with directions aggregated. It is neither a calendar-year value nor exact one-way passengers.
- `rn-04b92d6952d2` — Buenos Aires ↔ Colonia: **2,177,670** is an annual port-pair total with both directions aggregated.

Current `main` stores both values under `corridor_annual_oneway_pax`; the Rosario value is also exposed as `annual_one_way_pax` in the partner source. Those labels overstate the evidence. Set the annual-one-way fields to `null` and preserve the published totals only in direction-qualified benchmark records. Neither route currently enters the grounded floor, so this is a semantics correction rather than a revenue change.

## A2 — apply controls only

- Tigre: official DiDi zone proof supports city-level scope, not ferry-ramp supply or pickup performance.
- El Gouna: do not inherit Hurghada operation through the combined city ID.
- NEOM/Sindalah: Saudi Arabia only; never inherit into Egypt.

## C holds retained

Colombia remains decision C. Panama permission, Dominican Republic, Peru, Chile ferry-town operation, Taiwan current local operation, and exact Egypt berth coordinates remain held/null. Galápagos and 2017 Hong Kong patronage remain benchmark-only with no annualization.

## Safe next actions

1. Correct the two Argentina annual-one-way field semantics.
2. Source Costa Rica country-cost inputs; independently validate both model engines.
3. Cascade only the two Costa Rica routes after that preflight.
4. Leave geometry, Colombia, Taiwan, and all other nulls untouched.
