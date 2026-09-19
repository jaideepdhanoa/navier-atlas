# Strategic-partner deck package (V2)

A partner-neutral, local-first kit for source-linked strategic-partner proposals. V2 keeps the V1 evidence, editable native output, staged lifecycle, and narrow revision protocol, while making the sales argument explicit and traceable. It is not a partner template and contains no private dossiers, credentials, live IDs, or confidential imagery.

## What V2 supports

- **Partner thesis:** `Project.sales.brief` records the audience decision, partner relevance/thesis, Navier difference, combination advantage, strategic upside, investment-companion boundary, sources, and unresolved questions.
- **Source preservation:** `sourceInventory` and `sourceDisposition` record each important proposition/reference slide and its keep/strengthen/qualify/omit treatment, reason, destination block IDs, and visual reuse decision.
- **Sales cases:** each `Opportunity` retains V1 product/customer/payer/payment/contribution fields and may add `salesCase` fields for need, current alternative, scale basis, mechanism, outcome, ambitious business, first entry point, evidence boundary, demand status, and readiness.
- **Traceable authoring:** `sales.blocks` contain actual copy or `from` references, claims, placement and opportunity/field bindings. `sales.narrative` plans takeaway, narrative job, chapter and transition. Rendered sales copy uses block IDs rather than duplicate slide prose.
- **Reusable compositions:** eight registered compositions explain opportunities, product mechanisms, platform architecture, portfolios, missions, alternatives, infrastructure, and strategic close. See [layouts](docs/LAYOUTS.md).
- **Visual truth:** `VisualBrief` captures the argument, required features, prohibited implications, provenance, architecture options and unresolved choices. `VisualAttachment` explicitly binds a mark to a parent image hash and region. The registry remains conservative about hashes, rights, clearance and attachments.
- **Separate reviews:** editorial review records fresh-reader answers and specificity/removal/source-fidelity tests. Native render review records actual full/phone artifacts. Human finished-deck and external-release decisions remain distinct from agent/fixture review.

## Operational path

1. Work in a restricted project. Recover approved evidence, partner context, and image candidates.
2. Write the `sales.brief`, source inventory/dispositions, opportunity sales cases, and narrative outline before choosing layouts. Keep future ambition separate from the first engagement and keep investment material within `investmentBoundary`.
3. Use real copy block IDs and bindings in the storyboard. Make the opportunity set legible before individual chapters. Preserve qualifiers and unresolved choices.
4. Run editorial review before native production. A review template is unsigned and held; passing validation is not persuasion approval.
5. Compile offline, then create a fresh native staging destination with an authorized `NativePort`. Verify editable output, readback, sources, payment arrows, labels, crops and image truth.
6. Run `render-review` against the actual native snapshot and PDF; inspect full and phone pages. Obtain human finished-deck review, then explicit external-release approval. Keep all missing rights/clearance holds.
7. For revisions, snapshot and backup the live baseline, allowlist narrow operations, and stage a review copy. Promotion is fail-closed without atomic conditional revisions; never unconditional-overwrite production.

## CLI

Run from this package directory:

```sh
bun src/cli.ts init --out ./my-intake --partner "Example Vessel Company" --entity "Example Vessel Company Ltd"
bun src/cli.ts validate --project ./examples/public-demo/project.json [--public]
bun src/cli.ts migrate --project ./v1-project.json --out ./held-v2-draft
bun src/cli.ts compile --project ./examples/public-demo/project.json --out ./build-demo [--urls ./asset-url-map.json]
bun src/cli.ts render-review --project ./project.json --compiled ./build/compiled.json --snapshot ./native-after.json --pdf ./deck.pdf --out ./render-review
bun src/cli.ts assets --project ./examples/public-demo/project.json --query service
bun src/cli.ts review-template --project ./examples/public-demo/project.json --stage storyboard|comprehension|visual|release --out ./review
bun src/registry-cli.ts search --registry ./registry.json --mission passenger --clearance partner
```

`init` creates a fictional incomplete hold and never overwrites files. `validate` checks schema, references, evidence, policy, audience and V2 authoring contracts. `compile` emits deterministic artifacts and holds unresolved assets/native/visual work; it does not create a native deck or certify persuasion. `migrate` preserves V1 data/assets and creates a held draft; it does not synthesize the V2 thesis or rewrite the story. `render-review` requires the actual compiled input, native snapshot and PDF and writes `render-review.json` with `inspected:false` and `externalRelease:"held"`.

## Native boundary and safety

The local CLI is offline. An authenticated adapter supplies `NativePort` for create, duplicate, snapshot, batch, and optional PDF export. `createStaging` requires an approved storyboard receipt, editorial review where configured, verified remote asset hashes, native readback, and a fresh output directory. `stageRevision` backs up and patches a review copy only. `promoteRevision` requires a human visual receipt and atomic conditional revisions; a preflight hash is not a lock.

V2 improves authoring and review; it does not claim that tests, static validation, render collection, or agent inspection passed visual or external-release gates. See [workflow](docs/WORKFLOW.md), [content contract](docs/CONTENT-CONTRACT.md), and [native lifecycle](docs/NATIVE-LIFECYCLE.md).
