# Nordics exact-depth audit — status

**Audit date:** 2026-07-10  
**Lane:** Norway, Denmark, Finland, Sweden · Dott + Voi  
**State:** research handoff ready for review; **not seal-complete**  
**Repository source edited:** no

## Programmatic counts

| Metric | Total | Dott | Voi |
|---|---:|---:|---:|
| Source rows reviewed | 97 | 50 | 47 |
| Current rows (country + city) | 95 | 48 | 47 |
| Current city rows | 91 | 48 | 43 |
| Marine-relevant rows in lane | 56 | 25 | 31 |
| Exact-bind rows | 9 | 2 | 7 |
| Unresolved marine rows | 47 | 23 | 24 |
| Inland/out-of-lane excludes | 35 | 23 | 12 |
| Insufficient/non-current rows | 6 | 2 | 4 |

There are **7 unique exact Atlas city IDs** behind the 9 partner-row binds. The four global country clusters already exist; this lane proposes **zero new clusters**. Current partner scope correctly includes `denmark`, `finland`, `norway` for Dott (**121** canonical routes in-lane) and all four keys for Voi (**141**); Dott Sweden remains held.

## Exact reuse

- **Shared Dott + Voi:** `copenhagen-denmark` (4 canonical routes) and `helsinki-finland` (31 canonical routes).
- **Voi:** `bergen-norway` (32 routes touching the city ID), `oslo-norway` (4), `stavanger-norway` (23), `gothenburg-sweden` (4), and `stockholm-sweden` (16).
- Copenhagen, Oslo and Gothenburg have stable cluster-member and route-endpoint IDs but no current city feature node or city brief file. This is a missing-layer repair, not permission to mint a duplicate city ID.

## P0 recommendations

1. **Trondheimfjord shared unlock:** Dott and Voi both list Trondheim. Reuse `norway`; review the proposed `trondheim-norway` city layer, then source-ground Trondheim hurtigbåtterminal, Vanvikan hurtigbåtkai and Brekstad kai. Candidate legs stay `route_id: null`.
2. **Repair before minting:** Porvoo River Quay plus seven Finland routes are already banked under `helsinki-finland`; Kleppestø/Askøy plus seven Norway routes are banked under `bergen-norway`. Add/approve city attribution and preserve route IDs rather than duplicating routes.
3. **Exact shared reuse:** Keep Copenhagen and Helsinki stable and inherit their full global cluster route sets. No partner-specific corridor list.

## P1 research packages

- **Tampere/Pyhäjärvi:** shared partner evidence; municipal and operator sources confirm Laukontori Harbour–Viikinsaari service. This is a narrow lake exception, not inland bulk.
- **Aalborg–Egholm:** Voi city evidence plus an Aalborg municipality five-minute ferry. Landing labels/points still need canonical verification.
- **Turku waterbus:** Voi city evidence plus Föli's 2026 Martinsilta–Forum Marinum–Ruissalo system.
- **Knarvik:** current Voi row and two banked routes, but the endpoint is name-only and has no stable BP ID.

## Holds and exclusions

- Dott Sweden is non-current: explicit 2025 exit. The conflicted Gothenburg story cannot reactivate Sweden.
- Country presence is not proof of pickup at every Atlas city or BP.
- Remaining coastal rows stay research queue until named authoritative BPs exist; inland rows are excluded from this lane.
- No demand, fares, coordinates, route IDs, economics or operation-at-pier claims were invented.
- Candidate IDs are clearly `not_banked`; no source repository files were changed.

## Files

- `EXACT-BIND-LEDGER.json` — all 97 source rows, exact IDs, classifications, route/BP reuse and programmatic counts.
- `CANONICAL-GEOGRAPHY-HANDOFF.json` — canonical P0/P1 proposals, citations, null-ID routes, holds and deterministic Grok actions.
- `FAILED-SOURCES.md` — failed/weak-source log.
