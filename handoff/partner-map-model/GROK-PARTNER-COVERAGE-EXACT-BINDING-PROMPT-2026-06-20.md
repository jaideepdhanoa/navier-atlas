# Grok handoff — partner coverage exact-binding / render-check batch (2026-06-20)

## Mandate

Use the PR #55 handoff artifacts to run the deterministic partner-page sealing/render-check loop for the conservative exact-bound coverage batch. Do **not** perform new research. Do **not** infer markets from partner country/platform footprints.

## Inputs

- `handoff/partner-map-model/partner-market-coverage-targeted-exact-binding-batch-2026-06-20.json`
- `handoff/partner-map-model/PARTNER-MARKET-COVERAGE-TARGETED-EXACT-BINDING-BATCH-STATUS.md`
- `handoff/partner-map-model/partner-market-coverage-p1-p2-continuation-batch-2026-06-20.json`
- `handoff/partner-map-model/partner-market-coverage-p0-promotion-review-2026-06-20.json`
- Existing model contracts in `handoff/partner-map-model/`, especially `PARTNER-MAP-MODEL-SPEC.md`, `global-inheritance-registry.json`, `partner-global-registry-map.json`, `map-scope.json`, and `partner-market-canonical-bindings.json`.

## Apply only these supported items

1. P0 promoted exact registry keys:
   - Bolt: `crete-greece`, `malta-gozo`
   - Lyft: `oahu-honolulu-hawaii-usa`, `maui-county-hawaii-usa`, `kauai-hawaii-usa`, `kona-hilo-hawaii-island-usa`
2. P1/P2 conservative support items:
   - Kakao Mobility / Kakao T: `jeju-korea`
   - Four Seasons property-origin anchors only: `oahu-honolulu-hawaii-usa`, `sydney-australia`, `nassau-bahamas`
   - Soneva property-origin sealed local nodes already present in existing scope: `male-maldives__soneva-fushi-jetty`, `male-maldives__soneva-jani-jetty`

## Guardrails

- Exact ID matching only. `null` beats confidently-wrong.
- Additive only: source omissions must not shrink existing partner baselines.
- Hotel/resort/private-community partners are **property-origin only**. Do not create broad country/city footprint coverage for Aman, Four Seasons, Six Senses, Discovery Land, or Soneva.
- LINE remains prose/brief-only; no marine footprint card or ridehail footprint inference.
- DiDi country links remain country seeds only; no map scope until city-level evidence and Atlas exact support exist.
- Ola dated city table rows remain evidence queue only until current validation + Atlas exact match.
- Six Senses selector text is official but scrape-concatenated; clean before binding, otherwise leave null.
- Discovery Land community-origin rows require property-level/nearest-node review; do not infer broad city/country coverage.
- Economics-pending should not block display-ready Atlas geometry, but economics must remain separately tracked.

## Deterministic tasks

1. Update partner-page coverage surfaces and sidecar/derived model fields only for the supported exact-bound items above.
2. Preserve existing `network_footprint` entries and coverage notes; no shrink.
3. Regenerate any derived partner view/scope outputs according to the existing model contract.
4. Run render checks for affected partner pages: Bolt, Lyft, Kakao Mobility, Four Seasons, and Soneva.
5. Report changed files and before/after coverage counts by partner.

## Acceptance

- All supported IDs render or are explicitly noted as already supported sealed local nodes.
- Backlog/null rows remain absent from map scope and are recorded, not silently dropped.
- No separate non-marine footprint category is introduced.
- No country/platform seed is promoted without exact Atlas hierarchy/geometry support.
- If any routing/mask work is triggered, fold `route_water_allowlist.json` / LB-242 into that lane before route validation.
