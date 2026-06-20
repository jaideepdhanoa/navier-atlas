# Partner Coverage Continuation Plan

Date: 2026-06-20  
Scope: P0 promotion + P1/P2 broad-footprint-first research for multi-cluster partners

## Goal

Continue the partner market coverage workflow without shrinking any existing Navier/Atlas coverage. The plan is to promote only safe exact-bound candidates, use Jaideep's Yango regional notes as interim seed evidence, and expand the source-led scan across the remaining P1 mobility and P2 non-rideshare multi-cluster partners.

## Guardrails

1. **No-shrink baseline first:** existing partner JSON, map scope, seal scope, registry map, and prior handoff artifacts are the starting point, never the ceiling.
2. **Additive only:** source omissions cannot delete, demote, or hide existing coverage.
3. **Exactness over coverage:** only ID/alias/provenance-backed matches can become exact-bound candidates.
4. **Null beats wrong:** ambiguous cities, duplicate names, and unsupported geography stay in backlog/prose.
5. **Registry-first:** map footprint changes only use existing sealed registry keys with Atlas hierarchy/geometry support.
6. **Coverage note for broader reach:** ungrounded countries/regions are recorded as prose or backlog, not as map cards.

## Workstream A — P0 exact-bound candidate review/promote

Partners: **Yango, Bolt, Uber, Lyft**

### Inputs

- `partner-market-coverage-p0-no-shrink-baselines-2026-06-20.json`
- `partner-market-coverage-p0-coastal-priority-diff-2026-06-20.json`
- existing registry/map artifacts in `handoff/partner-map-model/`

### Steps

1. Review the 6 current exact-bound additive candidates:
   - Bolt: `crete-greece`, `malta-gozo`
   - Lyft: `oahu-honolulu-hawaii-usa`, `maui-county-hawaii-usa`, `kauai-hawaii-usa`, `kona-hilo-hawaii-island-usa`
2. Verify each candidate has:
   - existing registry key,
   - sealed cluster/city hierarchy,
   - stable match basis from source row to registry key,
   - no conflict with current partner scope.
3. Save promotion decisions as a review artifact:
   - promote-ready,
   - hold-for-human,
   - hold-for-alias,
   - hold-for-geometry,
   - reject/non-marine.
4. Do **not** mutate live partner pages until review output is clean.

### Output

- `partner-market-coverage-p0-promotion-review-2026-06-20.json`
- `PARTNER-MARKET-COVERAGE-P0-PROMOTION-REVIEW-STATUS.md`

## Workstream B — Yango interim broad seed from Jaideep notes

### Input seed from Jaideep

Use the provided regional hypothesis as interim evidence while official page scrape remains unresolved:

- MENAP: UAE, Oman, Egypt, Bahrain, Jordan, Qatar, Pakistan
- Africa: Ghana, Senegal, Ivory Coast, Cameroon, Zambia, Angola, Mozambique, Namibia, Ethiopia, DRC
- Latin America: Bolivia, Peru, Colombia, Guatemala
- Asia & South Caucasus: Nepal, Sri Lanka, Armenia, Georgia, Uzbekistan, Kazakhstan, plus broader CIS/Central Asia
- Europe: Finland, Norway; B2B tech in some other markets

### Steps

1. Record the seed exactly as **user-provided interim regional evidence**, not official city truth.
2. Reconcile against the existing Yango no-shrink baseline.
3. Split rows into:
   - already-covered baseline,
   - country-scope-only,
   - coastal/island priority backlog,
   - inland/non-marine parked,
   - B2B-tech-only / not consumer footprint.
4. Prioritize coastal or island markets for later exact-binding only where Atlas support exists.

### Output

- `partner-market-coverage-yango-interim-regional-seed-2026-06-20.json`
- update or append to Yango triage/status notes.

## Workstream C — Continue P1 mobility partner research

Partners:

- Grab
- DiDi
- Gojek / GoTo
- Ola
- inDrive
- Cabify
- FREENOW
- Kakao Mobility

### Steps per partner

1. Load existing Navier baseline if present.
2. Capture official/source-led country or city footprint evidence.
3. Normalize source rows.
4. Apply coastal/island/waterfront priority filter.
5. Attempt exact-binding only against existing registry/Atlas hierarchy.
6. Save unbound useful markets to gap queue with exact reason.

### Outputs

- partner-level source inventory/triage JSON where enough evidence exists,
- consolidated P1 gap queue,
- human-readable P1 status Markdown.

## Workstream D — Continue P2 non-rideshare multi-cluster research

Initial P2 partners from current baseline:

### D1 — Hospitality / property-origin partners

- Aman
- Four Seasons
- Six Senses
- Discovery Land
- Soneva

Important caveat: these partners should **not** be expanded as full country/city operating footprints. Their Navier-relevant routes originate from specific hotels, resorts, clubs, residences, marinas, or waterfront properties — not from every city in a country where the brand has presence.

### Hospitality/property-origin rules

1. Treat official property/resort lists as the source inventory, not country/city coverage pages.
2. Create or update a **property-origin footprint** / backlog rather than broad `network_footprint[]` city expansion.
3. Exact-bind only where a specific property can be safely associated with an existing Atlas city/cluster/locale/boarding-point/corridor.
4. If a hotel is in a coastal/island/waterfront market but lacks an existing Atlas-supported boarding point or route, keep it as:
   - property-origin backlog,
   - brief-only opportunity,
   - or future BP/corridor candidate.
5. Do not add full country nodes, broad city nodes, or non-property market cards just because the hotel group operates in that country.
6. Proposal language should say “selected property-origin routes” / “resort and marina transfers,” not “countrywide operating footprint.”

### D2 — Non-hotel multi-cluster partners

- LINE
- Rapido

Rapido is a mobility partner and should continue through the normal mobility coverage workflow. LINE is not a hotel developer, so it should continue through the normal non-hotel platform workflow. Both are unaffected by the property-origin caveat.

### Steps per hospitality/property-origin partner

1. Capture official property/resort/club/location inventory.
2. Normalize property name, city/area, country, and coordinates if available.
3. Filter for island, coastal, waterfront, marina-adjacent, resort-transfer, or airport-to-waterfront relevance.
4. Exact-bind only to existing Atlas-supported hierarchy/geometry.
5. Save unbound coastal properties to a property-origin backlog with the exact missing dependency.

### Steps per non-hotel partner

1. Confirm whether the partner is truly multi-cluster and partner-relevant.
2. Capture broad official footprint / operating markets.
3. Apply the relevant mobility/platform coverage filter.
4. Exact-bind only existing Atlas/registry-supported locations.
5. Save broader footprint in prose/backlog if not grounded.

### Outputs

- P2 source seed file,
- P2 hospitality property-origin backlog,
- P2 non-hotel coastal priority backlog,
- P2 exact-bound candidate file if any.

## Workstream E — PR #55 handoff discipline

For each bite-sized pass:

1. Save local artifacts under `/tasklet/agent/home/pr55-multicluster-scan/`.
2. Push only clean handoff artifacts to `handoff/partner-map-model/` on PR #55 branch.
3. Use short commits by workstream.
4. Do not regenerate partner pages or economics sidecars until the promotion review is approved/clean.

## Proposed immediate sequence

1. Build and push **P0 promotion review** for the 6 exact-bound candidates.
2. Build and push **Yango interim regional seed** from Jaideep’s notes.
3. Continue P1 research in this order:
   1. Grab
   2. inDrive
   3. Cabify
   4. FREENOW
   5. DiDi
   6. Gojek / GoTo
   7. Ola
   8. Kakao Mobility
4. Start P2 source seeding:
   1. Aman
   2. Four Seasons
   3. Six Senses
   4. Soneva
   5. Discovery Land
   6. LINE
   7. Rapido

## Stop points / human review

Pause before:

- mutating partner proposal JSON,
- promoting candidates into `network_footprint[]`,
- adding new registry keys or geometry,
- changing economics sidecars,
- treating user-provided Yango seed as official city-level evidence.

This keeps the workflow additive, inspectable, and proposal-safe.

## Success criteria for this continuation

- P0 promotion review is explicit and auditable.
- Yango interim regional footprint is captured without overclaiming.
- P1/P2 partners have source-seeded coastal priority queues.
- PR #55 has clean artifacts for the next exact-binding pass.
- No existing partner coverage shrinks.

Tiny chisel, clean marble — but with a bigger bench of partners now queued.
