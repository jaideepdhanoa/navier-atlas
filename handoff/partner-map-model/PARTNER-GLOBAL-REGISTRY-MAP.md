# Partner → Atlas Hierarchy Crosswalk

Maps partner operating-market buckets to existing Atlas city IDs. This is a derived crosswalk over the existing `region → cluster → city → locale_type/archetype` hierarchy, not a separate geography model.

## Display policy
- Partner proposal pages can display canonical Atlas cities/routes when the mapped city IDs have routed geometry.
- Economics/financials are tracked for sidecar/model promotion, but are **not** a display gate.
- Synthetic route categories, e.g. Grab `cross-border`, remain route categories rather than market nodes.
- No new BP/route research is introduced by this artifact.

## Summary
- **partners**: 47
- **partner_markets**: 113
- **mapped_partner_markets**: 112
- **unmapped_partner_markets**: 1
- **display_ready partner buckets**: 99
- **mixed display-ready / route-cleanup buckets**: 11
- **route-grounding queue buckets**: 2
- **unmatched/route-category buckets**: 1
- **all economics-ready buckets**: 32
- **mixed economics-ready/pending buckets**: 29
- **economics-pending tracked buckets**: 51

## Priority notes

### DiDi / LATAM
DiDi now maps to existing Atlas city IDs and can display where those city routes are geometry-ready:

- `brazil` → Rio de Janeiro, Angra / Ilha Grande, Florianópolis
- `mexico-pacific` → Los Cabos, Puerto Vallarta / Riviera Nayarit
- `mexico-caribbean` → Cancún / Riviera Maya, Cozumel, Playa del Carmen
- `colombia` → Cartagena / Rosario Islands
- `panama` → San Blas / Guna Yala
- `costa-rica` → Nicoya / Papagayo
- `dominican-republic` → Samaná

Most of these are display-ready from Atlas geometry and should be tracked for economics/financial-model promotion separately.

### Remaining unmatched bucket
- Grab `cross-border` → intentionally unmapped as a market; keep as a route/category concept.

## Next implementation step
Regenerate partner `network_footprint[]` from this crosswalk using display readiness for proposal-page visibility, while carrying economics readiness as metadata for promotion/model/sidecar work.
