# Strategic partnership deck package

A partner-neutral, local-first production kit for source-linked strategic-partnership decks. It standardizes the reusable parts of the workflow—intake, evidence, opportunities, storyboards, layouts, asset search, compilation, and review records—without bundling partner dossiers, credentials or live presentation IDs. An optional account-neutral adapter connects the native lifecycle to approved Tasklet services.

The package is intended to live at `deck-studio/strategic-partners/`.

## What is reusable

- **Intake:** `Project.meta` records the audience, objective, meeting context, classification, and disclosure level. `init` creates a clearly fictional, held scaffold; it is not a production brief.
- **Evidence:** source-linked `Claim` records carry an evidence class, basis, limitations, audience clearance, and source IDs. Keep measured, demonstrated, modeled, planned, and proposed material distinct.
- **Opportunities:** each `Opportunity` states the product, customer, payer, commercial logic, partner benefit, contributions, and next question. Do not merge different payment relationships into a generic collaboration.
- **Storyboard and layouts:** slides select a narrative layout (`cover`, `fit`, `options`, `models`, `channels`, `missions`, or `close`) and bind claims, sources, opportunities, notes, and visuals.
- **Asset catalogue:** `Asset` records include version hashes, dimensions, maturity, mission/geography/role tags, rights, audience clearance, caption, and optional crop/focal guidance. `registry-cli.ts` builds searchable registries and shortlists from local projects.
- **Local compiler:** `src/cli.ts compile` emits deterministic JSON/Markdown artifacts and an explicit held status when assets, evidence, native rendering, or visual QA remain unresolved.

## Recommended workflow

See the full [operating workflow](docs/WORKFLOW.md) and [quickstart](docs/QUICKSTART.md). New decks have two user checkpoints: thesis/storyboard and finished-deck approval. Independent content and visual checks support those checkpoints rather than adding user review rounds.

1. Recover the relevant context and create an intake for the correct legal entity, audience, meeting objective, and disclosure level.
2. Assemble a source-linked evidence pack and approved local assets. Keep private or restricted records out of public examples.
3. Write the commercial thesis as concrete opportunities: who buys, who pays, what each party contributes, and what must be assessed next.
4. Produce a visual storyboard and asset shortlist. Change the composition when content does not fit; do not shrink the whole deck to accommodate long names.
5. Obtain the **storyboard/editorial approval** before native production. This is an internal checkpoint, not external release approval.
6. Compile locally, then use an authenticated adapter for native staging when required. Inspect the actual rendered deck, including crop, wrapping, diagrams, payment arrows, and image truthfulness.
7. Obtain a separate comprehension/visual review and an explicit **release approval** before external circulation. Review-template files are unsigned `HELD` records, never approvals.

## Local CLI

Run from this package directory:

```sh
bun src/cli.ts init --out ./my-intake --partner "Example Vessel Company" --entity "Example Vessel Company Ltd"
bun src/cli.ts validate --project ./examples/public-demo/project.json --public
bun src/cli.ts compile --project ./examples/public-demo/project.json --out ./build-demo
bun src/cli.ts assets --project ./examples/public-demo/project.json --query service
bun src/cli.ts review-template --project ./examples/public-demo/project.json --stage storyboard --out ./review
bun src/registry-cli.ts search --registry ./registry.json --mission passenger --clearance partner
bun test tests --timeout 30000
```

The CLI is offline: it does not create a native deck, publish a presentation, fetch image bytes, or perform visual QA. `compile` may use `--urls` for exact HTTPS image URLs, but unresolved `asset://` placeholders remain a hold. Public validation rejects private sources/assets, including unused records.

## Native integration boundary

Native Slides work is deliberately an adapter boundary. The library in `src/lifecycle.ts` supports a provided authenticated `NativePort` for create, duplicate, snapshot, batch, and optional PDF export; the local CLI does not provide credentials or a service connection. See [`docs/NATIVE-LIFECYCLE.md`](docs/NATIVE-LIFECYCLE.md).

Creation is resumable and journaled by `createStaging`; it requires an approved storyboard receipt, fresh compiled input, verified remote asset hashes (or explicitly permitted internal exceptions), and native readback. Revision staging uses a backup and a review copy. Revision promotion is fail-closed unless the adapter supports atomic conditional revisions. The current Google Slides connection does not provide that primitive, so production promotion is held; a preflight hash is not a concurrency lock.

Revision operations are intentionally narrow: editable text replacement, axis-aligned movement (with optional attached marks), and exact-HTTPS image replacement. There is no delete-slide, replace-all, or full-rebuild operation. Human-edited decks must be treated as the baseline, and unexpected changes stop the workflow.

## Public-package boundary

This repository may contain only partner-neutral contracts, fictional examples, local test fixtures, and reusable documentation. Do not add private partner names, relationship notes, private text, production deck IDs, service-account IDs, confidential assets, or proposals. Keep restricted research, bindings, backups, and release records in the appropriate private project.

The package helps assemble evidence and review artifacts; it does not certify claims, commercial readiness, native rendering, visual quality, or external approval.
