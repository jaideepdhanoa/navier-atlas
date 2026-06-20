# PR57 — Partner proposal schema conformance

## Decision

The 483 validation mismatches were a schema-contract drift, not 483 independent content defects.

Signal from the starting audit:

- Partner files checked: 47
- Files passing the then-current schema: 0
- Files failing: 47
- Total validation errors: 483

The dominant live format is richer than the schema:

- `phases[].featured_routes` are structured route objects in 336/336 cases, while the schema still expected plain strings.
- Copy blocks are mostly structured, but several live partner and market records intentionally use concise prose strings for `hero`, `partner_context`, `differentiation`, `close`, and `the_ask`.
- Objections/proof points have legacy shorthand shapes (`q`/`a`, `objection`/`response`, or plain proof strings) that the renderer should preserve rather than force-migrate.
- Product/platform labels include N35/N35 Shuttle and N30 Pioneer II in addition to Pioneer II and Quanta-LR.

Therefore PR57 updates the schema to match the live/rendered proposal contract instead of destructively migrating proposal copy into a narrower older format.

## Changes

- Runtime and docs partner proposal schemas now match.
- Schema allows structured route refs for `featured_routes`, including Grok link metadata, scoped endpoints, model links, and Phase 3 backbone flags.
- Schema allows copy blocks as either structured objects or prose strings where the renderer supports both.
- Schema allows current route scopes (`intra`, `inter`, `intercity`, `network`, `all`, `cross_border`, `regional`).
- Schema allows platform labels currently present in partner data: `Pioneer II`, `N30 Pioneer II`, `Quanta-LR`, `both`, `N35`, `N35 Shuttle`.
- Renderer now handles the live shorthand shapes instead of silently dropping them:
  - string `partner_context`
  - string `differentiation`
  - string `close`
  - string `the_ask`
  - string proof points
  - `q`/`a` and `objection`/`response` objection formats
  - `featured_routes` with `from_label`/`to_label` instead of a single `label`
  - string/alternate hero blocks in intro/search text

## Validation after PR57

- Partner JSON parse: pass
- Runtime schema parse: pass
- Docs schema parse: pass
- Full partner proposal schema validation: **47/47 files pass, 0 errors**
- Renderer script syntax check: pass
- PR56 use-case checks remain green: empty phase arrays = 0, missing market-level use cases = 0, Phase 3 gate failures = 0

## Implication

After PR57, the repository can honestly use full partner proposal schema validation as a CI gate. Future failures should represent real data/contract regressions rather than historical schema drift.
