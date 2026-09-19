# V2 content contract

The runtime contract is in `src/types.ts`, `src/sales-types.ts`, and `project.schema.json`; validation and rendering must agree. A valid project is not automatically persuasive, rights-cleared, visually inspected, or approved for release.

## Brief, sources, and opportunities

`Project.sales.brief` requires:

- `role`: `standalone` or `investment-companion`;
- `audienceDecision`, `partnerRelevance`, `partnerThesis`, `companyDifference`, `combinationAdvantage`, `strategicUpside`;
- `investmentBoundary`, `sourceIds`, and `unresolvedQuestions`.

`sourceInventory` records `id`, `sourceId`, `kind` (`proposition` or `reference-slide`), `importance`, `summary`, and optional locator. Every item gets one `sourceDisposition`: `action` (`keep`, `strengthen`, `qualify`, `omit`), reason, destination block IDs, and visual decision (`reuse-native`, `adapt`, `replace`, `not-visual`) with reason. Retained propositions must reach rendered copy; core material must remain in core placement or be explicitly omitted.

`Opportunity` keeps V1 fields: `kind`, `title`, `product`, `customer`, `payer`, `commercialLogic`, `partnerBenefit`, both contributions, `nextQuestion`, `claimIds`, and `status` (`proposed` or `existing`). Its optional `salesCase` adds `need`, `alternative`, `scaleBasis`, `mechanism`, `outcome`, `ambition`, `entryPoint`, `evidenceBoundary`, `demandStatus` (`partner-demand`, `market-context`, `hypothesis`), and `readiness` (`existing`, `demonstrated`, `in-design`, `exploratory`). Do not combine distinct payer or payment relationships. Do not turn a first study/evaluation into the ceiling of the business.

Claims remain source-linked and carry evidence class, basis, limitations, audience clearance, and source IDs. Visible qualifiers must match the evidence class: a generic concept or confidentiality label does not qualify a modeled estimate. Keep demonstrated, modeled, planned, proposed, and unresolved material distinct. Unknowns remain unresolved; do not invent demand, economics, readiness, approvals, capacity, or launch dates.

## Authoring and traceability

`CopyBlock` has an ID, either `text` or `from`, `bindings`, `claimIds`, `placement` (`core`, `appendix`, `notes`), optional `placementReason`, and optional qualification. `OpportunityBinding` names an opportunity and field (including `salesCase.*`). Sales slide string fields are block IDs, not duplicate prose. A `from` block resolves a field at compile time; an authored block still needs semantic bindings. Bindings are traceability assertions, not proof that prose communicates the meaning.

`NarrativeEntry` records `slideKey`, `job`, `takeaway`, `transition`, `chapter`, placement, and opportunity IDs. Jobs are `opening`, `partner-relevance`, `company-advantage`, `platform`, `portfolio`, `opportunity`, `strategic-value`, `invitation`, and `support`. Introduce the opportunity set before detailed chapters; use sales-layer copy for need, product, difference, proof, upside and invitation, while keeping detailed scoping/validation/contracting in notes or appendix.

## Layout and evidence rules

Sales compositions are registered and strictly validated; unknown composition fields fail. Titles/copy budgets, allowed fields, visual requirements and bindings are documented in [LAYOUTS](LAYOUTS.md). Payment flows use explicit `Transaction` objects with actors, labels, and `kind: "payment"`.

Assets require local path, SHA-256, positive dimensions, MIME, maturity, rights note, caption, visibility, clearance and source IDs. Concepts must be visibly labeled. URLs do not confer rights or release clearance. The registry copies clearance conservatively and never infers attachments or visual facts.

## Reviews and records

`EditorialReview` is schema `2.0.0` and binds `subjectHash` and `visibleCopyHash`. It records reviewer identity/kind, decision, five reader answers (`partnerImportance`, `companyDifference`, `businesses`, `strategicUpside`, `invitation`), three tests (`partnerSpecificity`, `companyRemoval`, `sourceFidelity`), and findings. These are editorial assessments.

`RenderReviewBundle` binds compiled/native/PDF hashes and native presentation ID, page count, PDF, full/phone page artifacts, text coverage, holds, `inspected:false`, and `externalRelease:'held'`. `VisualInspection` binds the bundle hash and records full/phone inspection per page. Reviewer kind and purpose are not interchangeable: agent or fixture review cannot satisfy human finished-deck or external-release approval.
