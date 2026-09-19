# V2 quickstart — build the sales argument first

Use this package to create a partner-specific strategic sales deck, either standalone or complementary to an investment deck. It is not an evaluation-plan template. Standardize evidence, authoring, production and review—not the partner's story.

The CLI works offline. An authorized adapter stages a native deck separately. Start with the [workflow](WORKFLOW.md), [content contract](CONTENT-CONTRACT.md) and [composition guide](LAYOUTS.md).

## 1. Open a restricted project

Run from the package directory; place real partner work outside the generic package:

```sh
bun src/cli.ts init --out ../my-partner-project --partner "Example Vessel Company" --entity "Example Vessel Company Ltd"
```

`init` creates an incomplete V2 scaffold, including empty sales-authoring fields. It is explicitly fictional and held, contains no evidence or approvals, and never overwrites files. Replace every demo identity and field. Recover approved company evidence, the partner brief/two-pager, strong reference slides, relationship context and image candidates before researching or rewriting from scratch.

## 2. Write the thesis and source map before slides

Complete `sales.brief`: the audience decision, why the opportunity matters to this partner, what the company changes, why the combination is attractive, strategic upside and the desired invitation. Choose `standalone` or `investment-companion`; record what the independent investment deck already covers and avoid repeating its fundraising story.

Inventory the important propositions and reference slides. Give each an explicit keep/strengthen/qualify/omit disposition and a destination, plus a visual reuse decision. Preserve the strongest ideas; qualify unsupported certainty without shrinking ambition. Do not bury an essential proposition in notes merely to pass a checklist.

For each opportunity, retain product/customer/payer/payment/contribution fields and complete its `salesCase`: need, current alternative, market or operating basis, differentiated mechanism, customer outcome, ambitious business, credible first engagement, evidence boundary, demand status and readiness. The first study or evaluation is an entry point—not the business being sold.

## 3. Storyboard the visible argument

Introduce the businesses before the detailed chapters. Plan narrative jobs, takeaways and transitions in `sales.narrative`; author the actual slide copy in `sales.blocks` with source/claim and opportunity-field bindings. Use core copy to sell importance, the solution, differentiation, outcomes and strategic upside. Move most scoping, validation and contracting detail to notes or an appendix.

Choose compositions for their explanatory job, not a fixed slide sequence. Three wholly fictional V2 examples demonstrate different structures:

- `examples/energy-infrastructure/`: four opportunities, 11 slides.
- `examples/industrial-oem/`: three opportunities, nine slides.
- `examples/research-network/`: one opportunity, seven slides.

These are regression fixtures, not approved sales decks or prescribed storyboards. Their synthetic assets and pending review records must not be carried into real work.

For every visual, record its argument, required features, prohibited implications, maturity, exact bytes, rights/clearance, crop and review. Generated scenes must identify unresolved architecture choices rather than accidentally selecting a power source, site or configuration. Use approved product references; attach marks explicitly rather than inferring them from pixels.

## 4. Validate and review persuasion

```sh
bun src/cli.ts validate --project ../my-partner-project/project.json
bun src/cli.ts assets --project ../my-partner-project/project.json --query service
bun src/cli.ts review-template --project ../my-partner-project/project.json --stage storyboard --out ../my-partner-project/storyboard-review
```

A review template is unsigned and `HELD`. Complete the editorial review against the actual visible copy: can a fresh reader explain why this partner should care, why this company is special, what businesses are proposed, the strategic upside and the invitation? Apply the partner-name-swap, company-removal and source-fidelity tests. Software checks do not answer those questions for the reviewer.

Obtain the user's thesis/storyboard approval before real native production. `validate --public` is a publication-privacy check for deliberately public inputs; it does not authorize disclosure of a restricted partner project.

## 5. Compile locally, then stage native output

A safe fictional V2 example:

```sh
bun src/cli.ts compile --project ./examples/research-network/project.json --out ./build-research-demo
```

For a completed restricted project, use a fresh output directory:

```sh
bun src/cli.ts compile --project ../my-partner-project/project.json --out ../my-partner-project/build --urls ../my-partner-project/asset-url-map.json
```

Compilation emits copy/storyboard, source/asset records, native requests and holds. Missing remote asset URLs remain unresolved. URL mappings do not verify remote bytes; compilation does not create a native deck, visually inspect it or approve the pitch.

An authorized `NativePort` then supplies native staging. Require the approved storyboard receipt, matching editorial review where configured, verified remote assets and a fresh staging destination. Read back the native output. See [native lifecycle](NATIVE-LIFECYCLE.md).

## 6. Inspect the actual deck and approve release separately

```sh
bun src/cli.ts render-review --project ../my-partner-project/project.json --compiled ../my-partner-project/build/compiled.json --snapshot ../my-partner-project/native-after.json --pdf ../my-partner-project/deck.pdf --out ../my-partner-project/render-review
```

This records the actual native/PDF/full-page/phone artifacts and starts `inspected:false` with release held. Inspect every slide and record the results; collection is not inspection. Human finished-deck and external-release approvals remain distinct from agent/fixture observations. Missing rights or claim clearance stays held.

Revisions use a fresh baseline, backup, narrow allowlist and review copy. Never rebuild over human edits. Live promotion remains blocked without provider atomic conditional revisions; a snapshot hash is not a concurrency lock. See [revision safety](REVISION-SAFETY.md).

## V1 compatibility and checks

The original `examples/public-demo/` remains a V1 compatibility fixture. `migrate` preserves a valid V1 project/assets and produces an incomplete authoring draft—not compiler-ready V2 input or an automatic rewrite:

```sh
bun src/cli.ts migrate --project ../old-project/project.json --out ../held-v2-draft
bun test tests --timeout 30000
bun scripts/smoke.ts
```

Tests validate implementation behavior. They do not certify sales quality, actual imagery, native visual inspection or external release. Keep real partner dossiers, live IDs, relationship notes and confidential assets outside this package.
