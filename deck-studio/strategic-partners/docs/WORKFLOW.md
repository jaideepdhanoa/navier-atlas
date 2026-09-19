# V2 operating workflow

Use this lane for a bespoke strategic-partner proposal. Keep investor, authority, employer-network, route-economics and two-pager narratives separate. Work in a restricted project; public examples are fictional.

## 1. Intake and evidence

Confirm legal entity, audience, decision, meeting context, relationship stage and disclosure level. Recover approved sources, partner research, source-slide references, claims, and image candidates. Record dates, evidence class, basis, limitations and audience clearance. Separate fact, proposal, hypothesis and unresolved question.

## 2. Thesis and source preservation

Before an outline, complete `sales.brief`. State why the opportunity matters to this partner, what Navier changes, why the combination is better than the current alternative/build-alone path, the strategic prize, the ask, and the standalone/investment-companion boundary. Investment-companion decks may reuse necessary technology proof but should not repeat the investment team/origin/fundraising case.

Create `sourceInventory` and one disposition per important proposition/reference slide. A retained idea needs a rendered destination; a core idea cannot disappear silently. Decide explicitly whether to reuse a native source composition, adapt it, replace it, or leave it non-visual. Qualify unsupported certainty rather than deleting ambition.

## 3. Sales cases and narrative

For each opportunity, preserve product/customer/payer/payment/contribution fields and complete the sales case: need, current alternative, scale basis, Navier mechanism, outcome, partner upside, ambitious business, credible first engagement, and evidence boundary. Record demand status and readiness. The first engagement is an entry point, not the business ceiling.

Plan the narrative before selecting compositions. Use `sales.narrative` to state each slide's one takeaway, narrative job, chapter, transition and opportunity IDs. Introduce the opportunity portfolio before detailed chapters. Sell the opportunity; put detailed requirements, validation plans, risk allocation and contracting choices in notes/appendix unless they are necessary to the visible argument. Build copy blocks with actual IDs, claims, placement and field bindings.

## 4. Visual storyboard — checkpoint 1

Choose among the eight registered compositions by explanatory job, not fixed slide count. Shortlist real candidates from the local catalogue and record each visual's argument, required visible features, prohibited implications, maturity, source, crop and review. For a generated/derivative scene, state product references, illustrative status, architecture options and unresolved choices. Never let a concept select an unresolved power source, site, scale, configuration or commercial commitment.

Record explicit parent-image attachments for hull marks or other overlays with parent hash, mark hash, normalized region and review. Do not infer attachment from filenames or pixels. Run the editorial/fresh-reader review and resolve findings before native production. A review template is unsigned `HELD`, not user approval.

## 5. Compile and stage native output

Run `validate`, then `compile` into a fresh output directory. Compile emits deterministic JSON/Markdown/manifests and holds unresolved asset URLs, evidence, native work or QA; it does not fetch bytes or create a deck. With an authorized `NativePort`, `createStaging` requires an approved storyboard receipt, editorial review when configured, verified remote asset hashes, fresh destination, native readback and notes/bindings checks. Preserve editable text, shapes, images, labels and payment arrows.

## 6. Actual render review — checkpoint 2

Run `render-review` with the actual compiled deck, native snapshot and PDF. Inspect full and phone outputs for hierarchy, headline gist, wrapping, crops, labels, product truth, arrows, logos and bounds. Record `VisualInspection` only after inspection; the generated bundle starts `inspected:false` and external release held. Keep source fidelity, rights, clearance and qualification checks separate from visual checks.

Obtain human finished-deck approval, then explicit human external-release approval with the correct review purpose. Agent or fixture checks, tests, validation, and render collection are not approvals. Missing clearance remains held.

## 7. Revise safely

Read a fresh complete native snapshot, bind exact deck identity, archive a backup, and apply only allowlisted narrow edits to a review copy. Preserve unrequested human edits and attached marks; recompute image geometry from current dimensions. Never full-rebuild or unconditionally overwrite production. Promotion is fail-closed unless the provider supports atomic conditional revisions.

## 8. V1 migration and delivery

`migrate --project <v1> --out <draft>` preserves V1 fields/assets and creates a held V2 draft. It does not synthesize a thesis, source dispositions, sales cases, narrative or approvals; complete those explicitly. Deliver editable staging output, PDF, source/claim/asset records, hashes, native readback, review receipts, binding, backups and open holds together in a restricted versioned project.
