# Native lifecycle and render review

The CLI is offline. Native work uses an authenticated caller-supplied `NativePort` with `snapshot`, `create`, `duplicate`, `batch`, optional `exportPDF`, and `conditionalRevisions`. Never store credentials, connection IDs, account IDs, or destination IDs in this package.

## Create staging

`createStaging(project, compiled, port, options)` revalidates input, requires an approved storyboard receipt matching the compiled input hash, requires verified remote asset hashes (apart from explicitly permitted internal exceptions), creates/resumes a journaled fresh destination, checks deterministic slide identity/requests, image bindings, notes and readback, and writes receipts/binding only after completion. Supply editorial review when configured. It will not silently replay uncertain creation, remove unexpected slides, or target a protected destination. The stage receipt/PDF/readback are evidence of staging, not external approval.

Native output is editable text/shapes/lines/images, not a raster slide. Inspect actual output for wrapping, bounds, payment arrows, labels, crops, logos, source notes, product references and concept qualifications.

## Render review

After staging, call the CLI with actual artifacts:

```sh
bun src/cli.ts render-review \
  --project ./project.json --compiled ./build/compiled.json \
  --snapshot ./native-after.json --pdf ./deck.pdf --out ./render-review
```

`collectRenderReview` writes `render-review.json` (`schemaVersion:'2.0.0'`) bound to compiled hash, native snapshot hash, native presentation ID, PDF hash, page count, visible-copy hash, and each page's full/phone artifact and text coverage. It starts `status:'ready-for-inspection'`, `inspected:false`, and `externalRelease:'held'`; holds are retained. Inspect the actual full and phone images, then record `VisualInspection` with reviewer kind/name, bundle hash, per-page flags, headline gist and findings. The bundle or inspection is not release approval.

## Reviews and purposes

`EditorialReview` happens before native production and records fresh-reader answers for partner importance, company difference, recognizable businesses, strategic upside and invitation, plus partner-specificity/name-swap, company-removal and source-fidelity tests. `ReviewReceipt` stages are `storyboard`, `comprehension`, `visual`, and `release`; their `purpose` distinguishes storyboard approval, internal readiness, visual inspection, finished-deck, external-release, and workflow-test. `requireReview` matches subject hash, decision, reviewer and timestamp; a finished-deck-purpose visual review and release require a human, and external release requires purpose `external-release`. Agent/fixture reviews cannot satisfy human gates. Unsigned CLI templates are held.

## Revision staging and promotion

`stageRevision(binding, plan, port, out)` snapshots the complete baseline, makes a backup and review copy, recomputes/verifies a narrow allowlisted patch, applies it to the copy, reads it back, and confirms the source remained unchanged. Keep human edits and attached marks. Supported patch operations remain narrow: specified text replacement, axis-aligned movement, and exact-HTTPS image replacement; there is no delete-slide, replace-all, full rebuild or unconditional overwrite.

`promoteRevision` is fail-closed unless `port.conditionalRevisions` is true. It requires a matching human visual receipt, rechecks immediately, sends conditional requests, and verifies readback. A preflight hash is not a concurrency lock. If the provider lacks atomic conditional revisions, deliver the staged review copy and hold production promotion.
