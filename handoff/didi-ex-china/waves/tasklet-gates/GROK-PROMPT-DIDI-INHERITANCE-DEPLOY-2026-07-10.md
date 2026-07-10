# Grok repair handoff — DiDi inheritance and production synchronization

Work from current `main`. Do not change finance or promote held economics.

## Bite 0 — production synchronization

1. Build the DiDi partner page from current main with the full canonical cluster intersection and no legacy density cull.
2. Confirm the build receipt: 767 visible routes, 57 cities and 1,918 POIs before any Hong Kong cluster repair.
3. Re-run deployment and verify the deployed `/didi` page, not only local output.
4. Report source commit, deployment run, live route count and cache/build provenance.

The observed 208-route page is stale. A pre-fix build reproduces approximately that state at 206 routes, while current source builds 767.

## Bite 1 — Hong Kong/Macau geography precision

The combined `hong-kong-macau` cluster contains 37 visible Hong Kong-only routes and 16 visible Macau-only routes. The cross-city route is quarantined. DiDi has Hong Kong support; Macau remains held absent current local passenger-operation evidence.

1. Split/retag Hong Kong and Macau as separate geography-owned clusters while preserving all existing route IDs and geometry.
2. Add only the Hong Kong cluster to DiDi's normalized cluster membership.
3. Do not add Macau to DiDi.
4. Confirm that the DiDi page rises from 767 to 804 routes, subject only to route-cleanliness gates.
5. Audit other partners sharing the former combined cluster so no route is silently lost.

## Hard acceptance

- `DiDi routes = visible canonical ROUTES ∩ DiDi clusters`
- no city-key fallback that leaks a sibling geography
- no partner-specific route list or density cull
- 0 land crossings, 0 orphan routes, route IDs preserved
- Galápagos remains quarantined; Uruguay remains zero-route until separately sealed
- Taiwan and Macau operation holds remain intact
- inheritance, finance-inheritance and partner-copy gates pass
- fresh production verification records the live count
