# P0 multi-cluster coastal priority diff — 2026-06-20
Additive-only diff for Yango, Bolt, Uber, and Lyft. Existing proposal/map coverage remains the no-shrink baseline.
## Parsed official-source inventory
- Bolt official city rows parsed: **864**
- Uber official country rows parsed: **73**
- Lyft official city rows parsed: **812**
- Yango official homepage scrape returned a client-side error, so the current Yango rows are seed-only until official/local validation.

## Exact-bound additive candidates
- bolt: **2**
- lyft: **4**
- uber: **0**
- yango: **0**

These candidates map to registry city IDs already present in the current baseline artifact. They are still candidates, not automatic `network_footprint[]` changes.

## Priority backlog rows
- bolt: **75**
- uber: **33**
- lyft: **41**
- yango: **25**

Backlog rows are official-source or seed-supported coastal/island/country-scope candidates that need exact registry/geometry grounding before map display.

## Immediate next bite
1. Review/promote Bolt `crete-greece` and `malta-gozo` candidates if in-scope.
2. Review/promote Lyft Hawaii candidates if Lyft proposal should inherit Hawaii from the shared registry.
3. Run country-page city diffs for Uber’s coastal seed countries rather than enumerating all 15,000+ cities.
4. Validate Yango country seeds from official/local sources, then city-diff only coastal/Atlas-overlap markets.
