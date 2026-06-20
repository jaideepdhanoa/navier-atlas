# P1/P2 continuation batch status — 2026-06-20

## Completed in this batch

- Captured current source evidence for P1 mobility/non-hotel platform partners: DiDi, Gojek/GoTo, Ola, Rapido, Kakao Mobility/Kakao T, and LINE/LY.
- Captured property-origin evidence for P2 hotel/resort/private-community partners: Aman, Four Seasons, Six Senses, Soneva, and Discovery Land Company.
- Re-applied the new durable rule: hotel/resort/private-community brands are **property-origin only**, not full country/city footprint partners.

## Key parsed counts

- DiDi official country links parsed: **14**.
- Ola official city-table rows parsed: **205**; coastal-state hint rows: **88**.
- Four Seasons official page states **135 hotels and resorts**; parsed non-image candidate labels: **165**.
- Six Senses official selector text captured; parser cleanup required before exact binding.
- Soneva official resorts captured: **3**.
- Discovery Land official community cards parsed: **39**.

## Promotion posture

Nothing in this batch directly creates broad map scope. The output is a source-backed queue for exact-binding review:

1. Mobility/country seeds remain seeds until exact Atlas city/cluster/route support exists.
2. LINE remains prose/brief-only; no marine or taxi footprint card.
3. Property partners bind only from specific property/community origins.
4. Unsupported or stale rows stay null/backlog.

## Artifact

- `handoff/partner-map-model/partner-market-coverage-p1-p2-continuation-batch-2026-06-20.json`


## Parser caution

- Four Seasons binding should use non-image property/location links only.
- Six Senses selector text is official but concatenated by the scrape; leave property rows null until cleanup.
