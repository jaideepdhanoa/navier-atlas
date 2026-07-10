# DiDi partner-route inheritance audit

**Date:** 2026-07-10  
**Status:** source inheritance repaired; production deployment stale; one geography-precision repair remains

## Decision

The **208-route DiDi page is not the current source-derived result**. It is consistent with the older partner-page generation that applied density culling. A clean build from current main produces:

- **767 visible routes**
- **57 cities**
- **1,918 POIs**
- **15 exact cluster memberships**, 13 of which currently contain visible canonical routes

The pre-fix source reproduces approximately the reported live count at **206 routes**. The post-fix deployment failed during the Vercel upload/SSL stage, so the live page did not catch up with main. This is a production synchronization problem, not evidence that DiDi should only inherit 208 routes.

## What is working

Current source applies the geography-owned rule:

`DiDi routes = visible canonical ROUTES ∩ DiDi cluster membership`

The 767 routes are the full current intersection for DiDi's exact cluster keys. No partner-specific route subset or density cap is involved.

Largest inherited route sets are Egypt 179, Japan 161, Australia 92, Costa Rica 65, Brazil 59, Mexico 57, Panama 47 and New Zealand 42. Colombia contributes 14 geometry routes while finance remains held, as intended. Galápagos has three canonical rows but all remain quarantined/hidden; Uruguay currently has no routes.

## Residual scope-precision issue: Hong Kong versus Macau

DiDi's mixed legacy scope includes `hong-kong` as a city key. The canonical graph currently combines Hong Kong and Macau under `hong-kong-macau`:

- 37 visible Hong Kong-only routes
- 16 visible Macau-only routes
- the Hong Kong–Macau cross-route is quarantined

Adding the combined cluster would leak Macau into DiDi despite the current-operation hold. The correct fix is to split/retag the geography into separate Hong Kong and Macau clusters while preserving route IDs, then add **Hong Kong only** to DiDi. That would move the safe expected DiDi total from **767 to 804 routes** before any other new geography is sealed.

## Acceptance

1. A fresh production deployment succeeds.
2. `/didi` reports 767 routes before the Hong Kong split, not 208.
3. No legacy density culling occurs.
4. Hong Kong contributes 37 existing routes without exposing Macau's 16 routes.
5. Galápagos remains quarantined and Uruguay remains zero-route until their separate geometry gates pass.
6. No economics are promoted by this repair.
