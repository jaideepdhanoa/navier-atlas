# GROK SPEC — DiDi Ex-China Full-Parity Build

**Status:** execution authorized by Jaideep on 9 July 2026; proceed phase-by-phase and return the required receipts.  
**Mainland China:** excluded.  
**Goal:** Bolt/Grab-depth DiDi proposal with full geography, route identity, economics, partner pages, and deterministic deck package.

## Non-negotiable scope

### Direct / owned-brand / JV markets

- Latin America: Mexico, Brazil via 99, Colombia, Chile, Costa Rica, Panama, Argentina, Ecuador, Peru, Dominican Republic.
- APAC: Australia, New Zealand, Japan via DiDi Mobility Japan, Hong Kong.
- Africa/MENA: Egypt.
- Taiwan: keep as an additive scope seed, but do not publish as a verified current direct market until Tasklet supplies a current-status receipt.

### Do not treat as direct DiDi footprint

- Singapore, South Korea, Malaysia, Thailand, Indonesia, Cambodia, Vietnam, Philippines: aggregation-only.
- South Africa, Kazakhstan: historical exits.
- Macau: not proven in this audit. It shares the `hong-kong-macau` cluster, so prevent accidental Macau partner-footprint claims.
- Mainland China: remove from DiDi proposal/map scope for this ex-China build.

## Target architecture

- 16 jurisdictions.
- 17 full sub-proposals: Mexico Pacific; Mexico Caribbean; Brazil/99; Colombia; Chile; Costa Rica; Panama; Argentina; Ecuador/Galápagos; Peru; Dominican Republic; Australia; New Zealand; Japan; Hong Kong; Taiwan after gate; Egypt.
- 14 existing Atlas clusters and 43 current member-city IDs.
- True registry expansions: Chile and Argentina.
- Every in-scope market page must be full Grab-parity, never a roll-up stub.

## Permanent contracts

1. Corridors belong to geography. Derive DiDi corridors from the global canonical set and DiDi cluster membership. Never curate a DiDi-only subset.
2. Finance spine route IDs must equal the canonical inherited spine in every shared market. Only demand, capture, archetype, and fleet overlay may differ.
3. Do not invent route IDs, city IDs, BPs, demand, fares, or current-market status. Null beats wrong.
4. Use the one canonical cluster marquee set; DiDi featured/wow routes must be a strict inherited subset.
5. Remove the current `grab-greenfield-census.json` dependency. Use DiDi’s own census or the labelled global template band.
6. Never run economics from the current catch-all `didi` market key. Use real geography keys.
7. Do not preserve stale partner economics merely because they render. Current displayed $5.768M floor / $1.526B journey spend is not reproducible from the current aggregate.
8. Gate G partner-copy audit must be zero-leak before any seal/PR/complete claim.

## Sequence and return receipts

### G0 — Scope repair

Inputs from Tasklet:
- `DIDI-SCOPE-LEDGER-2026-07-09.json`
- official footprint research JSONs
- Atlas audits

Actions:
- Remove mainland China leakage, including Shanghai.
- Remove non-city market IDs from `cluster_city_ids`.
- Derive a clean partner scope from approved cluster/city membership.
- Handle Hong Kong without asserting Macau. If the current cluster model cannot do this safely, stop and return an explicit scope-conflict proposal; do not overclaim.
- Keep Taiwan behind a visible internal verification gate.

Return:
- scope before/after diff;
- exact city/cluster roster;
- full-market/footprint/map reconciliation report;
- anchor-city crosswalk.

### G1 — Route hygiene

Actions:
- Repair foreign/mis-stamped routes in Mexico, Galápagos, New Zealand and all target clusters.
- Run dedupe, land-crossing, orphan, missing-label, endpoint, distance, and quarantine checks.
- Do not delete genuine distinct intra-metro pier meshes.
- Re-derive all partner views after global fixes.

Return:
- route count before/after per cluster;
- changed route IDs and reasons;
- zero-land-crossing proof;
- global partner-inheritance gate report;
- finance-inheritance preflight.

### G2 — BP promotion / new geometry

Inputs from Tasklet:
- full BP manifests;
- Chile/Argentina registry research;
- hand waypoints for every route at land-crossing risk;
- drop-ledger schema.

Actions:
- Deterministically ID-match/promote BPs.
- Build only real BP↔BP water routes.
- Preserve source IDs and country/cluster/city tags.
- Return every rejected BP with a reason.

Return:
- BPs accepted/dropped/repointed;
- zero silent drops;
- routes built/culled;
- render QA per city;
- stable route IDs for finance binding.

### G3 — Mexico calibration seal

Order:
1. Mexico Pacific.
2. Mexico Caribbean.

Actions:
- Seal all accepted Mexico BPs/routes globally.
- Re-derive every partner in Mexico.
- Bind canonical cluster marquees only after final route IDs exist.

Return:
- exact inherited Mexico spine;
- all-partner parity receipt;
- render screenshots/QA counts;
- route-ID manifest for Tasklet economics.

### T3 — Tasklet finance interlock

Grok pauses while Tasklet:
- sources corridor demand/fare records;
- completes country-reference rows;
- builds DiDi’s overlay on the sealed shared spine;
- runs aggregate/growth/frontend splice;
- updates the transparent Sheet in place;
- confirms model and Sheet agree.

Do not synthesize L3 demand to unblock the cascade.

### G4 — Economics sidecar and partner reseal

Inputs from Tasklet:
- fresh aggregate/growth/partner JSON;
- live economics URL;
- route-keyed source records;
- full Mexico sub-proposals.

Actions:
- Build `economics_by_route_id.json` against the new gold.
- Reseal the DiDi partner surface.
- Wire unit-economics chip and ladder links to the live Sheet.
- Run route/spine/partner-copy/render gates.

Return:
- data-clean partner JSON;
- sidecar receipt;
- economics URL receipt;
- Gates A–G report;
- render receipt.

### G5 — Remaining waves

Repeat G2→T3→G4:
- LatAm Wave A: Brazil, Colombia, Costa Rica, Panama, Dominican Republic.
- LatAm Wave B: Ecuador, Peru.
- LatAm Wave C: Chile and Argentina after registry expansion.
- Global Wave: Australia, New Zealand, Japan, Hong Kong, verified Taiwan, Egypt.

Do not batch a market with incomplete BPs/demand into a false-complete result. Geography may ship with honest-null economics, but the market must remain `cascade-needed`.

### G6 — Proposal/deck closure

After all approved markets pass:
- verify 17 full sub-proposals;
- verify per-phase route bindings, fleet confidence, and vessel sizing;
- open `deck-studio/decks/didi/deck.config.json` first;
- bank a logo only with an actual committed file and `LOGO-SOURCE.json`;
- sync live deck ID and slide manifest;
- generate the deterministic deck package;
- leave Atlas screenshot slots for Jaideep;
- use Slides API only, never PPTX round-trip/full replacement.

Return:
- Deck Studio config/manifest/asset registry diff;
- build receipt;
- PDF QA;
- partner-copy lint;
- slide-by-slide defect ledger.

## Acceptance gates

- 0 unsupported direct-operation claims.
- 0 mainland-China leakage.
- 0 market IDs in city-ID arrays.
- 0 partner-specific corridor divergence.
- 0 finance-spine divergence in shared markets.
- 0 silent BP drops.
- 0 land crossings/orphans.
- 0 stale route IDs in economics.
- 0 peer-census borrowing.
- 0 countries falling back silently to Singapore costs.
- 17 approved full sub-proposals, each with complete phases and vessel sizing.
- Model, Sheet, partner JSON, data-clean JSON, sidecar and deck agree.
- Gate G and deck partner-copy lint pass.

## Input artifacts

- `/tasklet/agent/home/didi-ex-china-audit/DIDI-SCOPE-LEDGER-2026-07-09.json`
- `/tasklet/agent/home/didi-ex-china-audit/didi-latam-footprint-2026-07-09.json`
- `/tasklet/agent/home/didi-ex-china-audit/didi-apac-africa-footprint-2026-07-09.json`
- `/tasklet/agent/home/didi-ex-china-audit/didi-atlas-latam-audit-2026-07-09.json`
- `/tasklet/agent/home/didi-ex-china-audit/didi-atlas-global-audit-2026-07-09.json`
- `/tasklet/agent/home/didi-ex-china-audit/DIDI-EX-CHINA-COVERAGE-AUDIT-AND-BUILD-PLAN-2026-07-09.md`

## Completion language

Do not call the proposal complete until the full chain exists. Use:
- `research-needed`
- `research-complete / seal-needed`
- `seal-complete / cascade-needed`
- `proposal-complete`
