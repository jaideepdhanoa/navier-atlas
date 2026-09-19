---
name: strategic-partner-deck
description: Build or revise persuasive strategic-partner sales decks for industrial/OEM, energy, manufacturing, licensing or distribution partnerships. Use V2 sales cases, source preservation, reusable visuals and human-edit-safe production.
---

# Strategic-partner decks (V2)

Read [README](README.md), [workflow](docs/WORKFLOW.md), [content contract](docs/CONTENT-CONTRACT.md), [layouts](docs/LAYOUTS.md), and [native lifecycle](docs/NATIVE-LIFECYCLE.md). For imagery read [asset catalogue](docs/ASSET-CATALOGUE.md); for revisions read [revision safety](docs/REVISION-SAFETY.md).

Use this lane for a partner-specific proposal—not an investor deck, authority proposal, employer network, route-economics deck, or standalone two-pager. Keep partner dossiers, relationship notes, live IDs, credentials, and confidential imagery in a restricted project; this package remains generic.

## Required story before production

1. Establish a `sales.brief` with `role` (`standalone` or `investment-companion`), `audienceDecision`, `partnerRelevance`, `partnerThesis`, `companyDifference`, `combinationAdvantage`, `strategicUpside`, `investmentBoundary`, `sourceIds`, and `unresolvedQuestions`.
2. Record each important source proposition/reference slide in `sales.sourceInventory`, then disposition every item as `keep`, `strengthen`, `qualify`, or `omit`. A retained item must bind to rendered copy; an omission needs a reason. Decide whether to `reuse-native`, `adapt`, `replace`, or leave `not-visual`.
3. Model opportunities with the normal commercial fields plus `salesCase`: `need`, `alternative`, `scaleBasis`, `mechanism`, `outcome`, `ambition`, `entryPoint`, `evidenceBoundary`, `demandStatus`, and `readiness`. Keep the ambitious business distinct from the credible first engagement.
4. Explain the opportunity set before detailed chapters. Use `sales.blocks` (actual copy or `from` references), explicit opportunity bindings, `placement` (`core`, `appendix`, `notes`), claims, and qualification. A binding provides traceability; it does not prove that prose communicates the asserted meaning.
5. Plan each slide in `sales.narrative` with `takeaway`, `job`, `chapter`, `transition`, opportunity IDs, and placement. Sell need → solution → differentiated mechanism → outcome → partner upside; do not turn the internal sales-case checklist into an on-slide grid.

The eight registered V2 compositions are `partner-opportunity`, `product-value`, `platform-architecture`, `opportunity-portfolio`, `mission-hero`, `customer-alternative`, `integrated-infrastructure`, and `strategic-close`. Unknown composition fields fail validation. See [layouts](docs/LAYOUTS.md).

## Visual truth and review

Every `VisualBrief` states its `argument`, `requiredFeatures`, `prohibitedImplications`, `origin`, reference sources, architecture options, unresolved choices, and review. Generated scenes are illustrative; they cannot establish proof or silently select unresolved architecture. Explicit `VisualAttachment` records bind a mark to a parent image hash and normalized region; do not infer attachment from filenames or pixels. Source-slide reuse is a recorded storyboard decision, not automatic rights clearance.

Before native production, create the editorial review with fresh-reader answers for partner importance, company difference, recognizable businesses, strategic upside, and invitation, plus partner-specificity/name-swap, company-removal, and source-fidelity tests. These are editorial judgments, not proof from passing software checks.

After native staging, use `render-review` for the actual PDF/native snapshot and inspect full and phone pages. Review kind and purpose matter: agent/fixture inspection is not human finished-deck or external-release approval. Unsigned templates are `HELD`; missing clearances stay held. Do not unconditionally overwrite a live deck. Revision promotion requires provider atomic conditional revisions; otherwise stage a review copy only. See [native lifecycle](docs/NATIVE-LIFECYCLE.md).

V1 projects remain readable. `migrate` creates a held draft with explicit unresolved V2 authoring; it does not invent a thesis, rewrite sales cases, or approve a deck.
