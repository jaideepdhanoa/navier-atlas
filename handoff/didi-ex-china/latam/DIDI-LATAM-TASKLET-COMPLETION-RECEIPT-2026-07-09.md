# DiDi Latin America — Tasklet research completion receipt

**Research as of:** 2026-07-09  
**Revised:** 2026-07-10T02:57:33Z  
**Scope:** Waves A1, A2, B and C only: Brazil, Colombia, Costa Rica, Panama, Dominican Republic, Ecuador, Peru, Chile and Argentina. Mexico remains outside this synthesis because its T3/G4 handoff is separate.

## Boundary of this receipt

This receipt closes **Tasklet's source-led research synthesis and exact-ID recheck**, not the full DiDi proposal, not a global route seal and not finance.

- `research-complete / seal-needed`: Brazil, Colombia, Ecuador.
- `research-needed`: Costa Rica, Panama, Dominican Republic, Peru.
- `registry-research-complete / mint-and-seal-needed`: Chile, Argentina.
- No market is represented as proposal-complete, seal-complete or finance-cascade-ready.
- Exact route existence, correct cluster stamping and active visibility are three different states. None alone is render approval.

## Tasklet work completed

1. Consolidated the four Latin America waves in fixed order A1 → A2 → B → C.
2. Normalized 185 source records, 175 BP/POI research records, 39 candidate corridors and 49 demand/fare records.
3. Preserved every `annual_one_way_pax` as null; no broad tourism, airport, attraction, hotel, whale, cruise or metro count was converted into route demand.
4. Rechecked all non-null references against the pinned canonical snapshot with exact matching only:
   - 15 city IDs validated;
   - four explicitly referenced cluster IDs validated;
   - 19 route references validated with valid endpoints: 18 candidate-corridor IDs plus Peru stamp-cleanup reference `rn-f0a756c7f278`;
   - zero invalid city, cluster, route or route-endpoint references;
   - all Wave C proposed IDs correctly remain null.
5. Preserved the no-shrink baseline at the exact-record/ID layer. This PASS does **not** assert BP/geometry seal, partner binding, active eligibility or render approval.
6. Produced deterministic Grok inputs, operation-evidence tiers, do-not-publish controls, market blockers, owners and next actions.
7. Validated both JSON outputs with Python.

## Exact-existing versus active/renderable truth

Current-main excludes `_quarantine=true` or `relevance="hide"` records from active global canonical/rendered sets. Partner inheritance must use only the active canonical set intersected with approved geography scope.

| Cluster | Stamped / exact-existing | Active / renderable now | Excluded quarantine/hidden |
|---|---:|---:|---:|
| `brazil` | 59 | 59 | 0 |
| `colombia` | 15 | 14 | 1 |
| `costa-rica` | 67 | 65 | 2 |
| `panama` | 47 | 47 | 0 |
| `dominican-republic` | 32 | 29 | 3 |
| `galapagos-ecuador` | 3 | 0 | 3 |
| `peru` | 12 | 12 | 0 |
| **Total** | **235** | **226** | **9** |

Among the 19 validated route references, 15 are active/renderable under current exclusion rules and four are quarantine/hidden: the three genuine Galápagos member routes and `rn-60740d4c3114` in Dominican Republic.

The 46 foreign Galápagos stamps are absent, all three genuine records are stamped `galapagos-ecuador`, and `rn-f0a756c7f278` is stamped `peru`. These are stamp-cleanup facts only. They do not prove completed route seals, partner bindings or render approval. In particular, Galápagos is **3 stamped / 0 active**, not a rendering route set.

## Concise wave inventory

| Wave | Markets | Sources | BP/POI records | Corridors | Exact candidate route IDs | Null candidate route IDs | Demand/fare records | Null annual demand |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| A1 | Brazil, Colombia | 27 | 17 | 11 | 5 | 6 | 18 | 18 |
| A2 | Costa Rica, Panama, Dominican Republic | 122 | 124 | 11 | 10 | 1 | 12 | 12 |
| B | Ecuador, Peru | 22 | 12 | 7 | 3 | 4 | 9 | 9 |
| C | Chile, Argentina | 14 | 22 | 10 | 0 | 10 | 10 | 10 |
| **Total** | **9 markets** | **185** | **175** | **39** | **18** | **21** | **49** | **49** |

The extra nineteenth route reference is Peru stamp-cleanup verification `rn-f0a756c7f278`; it is not one of the 39 candidate corridors.

## Remaining Grok registry/BP/route seal

Grok work remains open for every wave. The deterministic handoff requires Grok to:

1. Reconcile all 175 BP/POI records to sealed, held or dropped outcomes with reasons; prove zero silent drops, ghost endpoints and orphans.
2. Preserve exact IDs while separating stamped inventory from active/renderable inheritance. Reproduce the 235 stamped / 226 active / 9 excluded before-state and return reasoned record-level deltas.
3. Run BP identity, authority/source, coordinate, geometry, endpoint, water/land-crossing, protected-area, quarantine/visibility, inheritance and render gates. Do not claim that complete stamped sets render.
4. Treat the Galápagos and Peru stamp cleanup as hygiene only. Independently qualify each route, keep all three Galápagos records excluded until approved, and separately report seal and render results.
5. Run registry approval and canonical mint/seal for Chile/Argentina; return every minted exact ID. Candidate labels/keys are not IDs.
6. Keep every unresolved route/BP ID null and every unsupported operation claim caveated.
7. Return the required machine- and human-readable handback receipts with pre/post hashes, stamped/active/excluded counts and render evidence.

## Future finance cascade

No finance cascade is authorized or complete.

- All 49 route-demand values remain null.
- Broad context counts are not route riders.
- Exact route existence or a correct stamp does not make a corridor model-ready.
- Route-level annual one-way demand, current fares, costs, schedules, source-qualified geometry and final IDs must pass separate gates.
- Only after Grok returns an accepted global seal/render receipt may Tasklet run the separate partner-model cascade for source-qualified corridors. Atlas/render geography and finance remain separate data worlds.

## All unresolved research items

### Brazil

1. Annual/monthly passengers by line and direction for every economics candidate.
2. Current Angra–Ilha Grande detailed calendar/frequency beyond the verified R$20.50 / 110-minute benchmark.
3. Rio 2025/2026 line-by-line passenger series.
4. Costa da Lagoa exact stop GIS, authoritative coordinates, capacity, fare basis and passenger history.
5. Candidate BP source/coordinate confirmation and water-only geometry for the three null-route candidates.

### Colombia

1. Authoritative La Bodeguita Atlas BP identity/coordinate and the 745,079-passenger split by route, operator, month and direction.
2. Exact Isla Grande dock plus operator fare-product basis.
3. Barranquilla Río-Bus current phase, stations, operator, timetable, fare and demand study; keep future-only meanwhile.
4. Annual/monthly route passengers by direction for every economics candidate.

### Costa Rica

1. Terminal-level DiDi availability; Liberia proves only a gateway overlap.
2. Authority/operator boardability and accepted coordinates for property-, beach- and OSM-led candidates.
3. Route-level annual passenger series for priority ferries.
4. Durable operator/service-day confirmation where the captured Playa Naranjo schedule is date-bounded.

### Panama

1. Official annual Guna Yala visitor and route-level passenger series.
2. Authority-confirmed Cartí-area ports, community docks, coordinates, permissions and local operating model.
3. Current local DiDi service proof for Cartí/Guna Yala if any; Panama City proof cannot be extended.
4. Cartí–Colón fare, schedule and hand-routed geometry, or continued rejection; its route ID remains null.

### Dominican Republic

1. Primary Samaná ferry operator, exact terminals, both-direction timetable, service days and walk-up fare.
2. Route-level annual passenger series.
3. App/written local DiDi service evidence for Samaná; current official city list does not include it.
4. Authority-grade BP coordinates/boardability, including the additive Sabana de la Mar landing candidate.
5. Current whale-sanctuary vessel, permit, speed and noise constraints.

### Ecuador

1. App/written DiDi service-area evidence for each Galápagos island; current evidence supports Ecuador only, not local island service.
2. Accepted canonical BP IDs/coordinates and operator tracks for the four researched piers.
3. Route manifests, monthly ridership, sailings, schedules, cancellations, load factors and fare history.
4. Protected-area/authority operating constraints and finance cost/revenue/capture inputs.

The stale 46 foreign Galápagos stamps are absent in the pinned snapshot and the three genuine records are correctly stamped, but all three remain `quarantine=true` and `relevance=hide`. This is stamp cleanup only: Galápagos has 3 stamped/exact-existing and 0 active/renderable routes. Grok must re-prove the state and independently complete BP/geometry/seal/render gates before any activation.

### Peru

1. DPA San Andrés structural status, passenger authorization, exact BP and coordinate.
2. Partner-neutral `pisco-san-andres-peru` canonical brief.
3. Callao operator-to-pier allocation, commercial fares, authoritative tracks, manifests and route-level passengers.
4. Ballestas audited embarkations by period/operator/direction and seasonality; do not use total attraction visits as one-way route riders.
5. Palomino commercial transport fare and reconciliation of the inconsistent “11 miles / 32 km” source pair.
6. Authority-qualified BPs and water-only geometry for all four null-route candidates.
7. Direct local DiDi proof for Callao piers, Paracas and Pisco/San Andrés; only Lima city support is established.

### Chile

1. Registry-owner approval of Chile hierarchy and promoted marine cities; mint canonical cluster/city IDs only in the canonical registry.
2. Authority-confirmed names/coordinates/boardability for 14 BP records.
3. Hand-routed water-only geometry and exact endpoint binding for six null-route candidates.
4. Annual one-way route passengers, current fare tables and source-qualified schedules.
5. DiDi service polygons for nearby ferry municipalities rather than inference from Concepción, Puerto Montt, Punta Arenas, Valdivia, Valparaíso or Viña del Mar.
6. Domestic regulatory/protected-area review and partner-neutral canonical briefs.
7. Current passenger-service proof for Muelle Blanco; preserve Muelle Prat as excursion-only.

### Argentina

1. Registry-owner approval of Argentina hierarchy and promoted marine cities; mint canonical cluster/city IDs only in the canonical registry.
2. Authority-confirmed names/coordinates/boardability for eight BP records.
3. Hand-routed river/lake geometry and exact endpoint binding for four null-route candidates.
4. Annual one-way route passengers, current fare tables and source-qualified schedules.
5. Direct Tigre service-area proof; Buenos Aires city support cannot be extended to Tigre.
6. Rosario–Isla Sabino Corsi seasonal reactivation/current schedule evidence.
7. Buenos Aires–Colonia cross-border legal, customs, deployment and country-scope review.
8. Partner-neutral canonical briefs and domestic operating constraints.

## Final boundary

Tasklet has banked the Latin America research control, exact-ID/existence receipt and deterministic Grok instructions. Remaining work is explicitly: **(a) unresolved research below, (b) Grok global registry/BP/route seal and active-set render QA, then (c) future Tasklet finance research and cascade for qualifying corridors.** None is complete merely because an exact route record exists or this receipt was issued.
