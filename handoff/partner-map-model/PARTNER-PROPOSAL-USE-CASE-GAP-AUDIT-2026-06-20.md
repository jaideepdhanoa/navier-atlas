# Partner proposal use-case render and gap audit — 2026-06-20

## Diagnosis

Grab → Singapore did have phase-level use-case content, but PR #55 stored it as `{label, summary}` objects. The live proposal renderer only understood strings or `{title, body}`, so those rows rendered blank. This same class affected Bolt, Grab, Yango, and a few sovereign/deck partner files.

## Correction applied

- `index.html` now renders use cases shaped as strings, `{title, body}`, or `{label, summary}`.
- No data rewrite was required; this is a renderer-tolerance fix. Schema formalization remains a Phase 3 hygiene item.
- No partner geography/economics was changed.

## Grab → Singapore now renders

- Phase 1 — Marina Bay & Sentosa (Pioneer II): leisure hop: Marina Bay–Sentosa harbour hops.; premium ridehail: Premium water legs to Sentosa, booked in-app.
- Phase 2 — East Coast transport berths: coastal commute: East Coast–CBD foiling commute.; transport berth activation: MPA transport berths flying past the ECP crawl.
- Phase 3 — the city-state water mesh: city water network: Marina, Sentosa and Pulau Ubin on one app.; regional template: The city-state template, ready to replicate.

## Important remaining gaps

- Before this patch, `127` phase records were at blank-render risk because they used `{label, summary}` objects.
  - `bolt.json`: 45
  - `grab.json`: 42
  - `yango.json`: 24
  - `red-sea-global.json`: 4
  - `saudi-pif.json`: 3
  - `qatar.json`: 3
  - `jih-global.json`: 3
  - `careem.json`: 3
- `18` phase records still have empty use-case arrays and need authored local use cases.
  - `indrive.json`: 4
  - `didi.json`: 4
  - `yango.json`: 3
  - `uber.json`: 3
  - `discovery-land.json`: 3
  - `careem.json`: 1
- `113` hub/sub-proposal markets lack optional market-level use-case summaries. Phase use cases now render, but if cards need use-case chips this should be formalized and backfilled.

## Phase 3 gate

Every newly promoted partner-market bind should carry at least two local use cases before it is marked proposal-ready; otherwise it stays display-only / economics-pending. This prevents coverage promotion from outrunning pitch completeness.
