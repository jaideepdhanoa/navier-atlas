# Dott/Voi coordinate-gated canonical handoff

**Status:** research-complete / seal-needed

This package consolidates all five Wave 1 coordinate ledgers against current `main`. Coordinate readiness is evidence readiness only; it does not mint geography, routes, access rights, or economics.

## Counts

- Boarding-point candidates: **89**
- Coordinate-ready (T1/T2): **75**
- Held with `coordinates: null`: **14**
- Existing exact BP-ID reuses: **2**
- Coordinate-ready but non-coordinate-held BPs: **7**
- New BP candidates eligible for deterministic seal review: **66**
- Candidate endpoint pairs: **42**
- Both endpoints coordinate-ready: **32**
- Coordinate-held endpoint pairs: **10**
- Coordinate-ready but non-coordinate-held endpoint pairs: **4**
- Existing exact canonical route reuses: **0**
- New route pairs needing deterministic geometry seal: **28**

## Lane summary

- **be-ch** — BPs 17/21 ready; route pairs 6/9 coordinate-ready; exact existing BP IDs 2; exact existing routes 0.
- **dott-at-hu-balearics** — BPs 16/18 ready; route pairs 6/8 coordinate-ready; exact existing BP IDs 0; exact existing routes 0.
- **nordics** — BPs 9/10 ready; route pairs 5/6 coordinate-ready; exact existing BP IDs 0; exact existing routes 0.
- **uk-de** — BPs 18/23 ready; route pairs 9/11 coordinate-ready; exact existing BP IDs 0; exact existing routes 0.
- **voi-lehavre-dott-poland** — BPs 15/17 ready; route pairs 6/8 coordinate-ready; exact existing BP IDs 0; exact existing routes 0.

## Hard gates

- Reuse only exact current IDs; do not promote placeholder `proposed-*` IDs verbatim.
- Mint geography only once in the global canonical graph; Dott and Voi inherit by cluster membership.
- Validate every route for water geometry, land crossing, N30/Quanta range, public pickup/access, duplicate endpoints, and country tagging.
- Coordinate-ready marinas are not automatically passenger-service or public-access claims.
- Preserve all held points and endpoint pairs in the drop ledger; acceptance requires **0 silent drops**.
- Do not change economics in this seal. Demand, fares, and annual one-way passenger values remain separate evidence gates.

## Existing reuses

- Nyon and Rolle are exact existing BP IDs on the Lake Geneva graph; reuse those endpoints. No exact current Nyon–Rolle route exists, so the candidate pair still requires deterministic geometry and duplicate checks.
- Ibiza/Formentera routes were already reused in Wave 1; no new Balearics route is requested here.

## Acceptance receipt required from Grok

1. BP result for all candidates: reused, sealed, or dropped with reason.
2. Route result for every coordinate-ready endpoint pair: reused, sealed, or held with reason.
3. Before/after city, POI, route, and cluster counts.
4. Zero land crossings, orphan routes, duplicate IDs, and partner-specific corridor forks.
5. Strict Dott/Voi inheritance and copy gates; Voi remains Europe-only and Dott retains verified UAE scope.
