# Native lifecycle and render review

The CLI is offline. Native work uses an authenticated caller-supplied `NativePort` with snapshot/create/duplicate/batch and optional PDF export. Never store credentials, connection IDs, account IDs or destination IDs in this package.

## Staging

`createStaging` revalidates input, requires an approved storyboard receipt matching the compiled hash, verified remote asset hashes, a fresh destination, native readback and notes/bindings checks. It writes receipts only after completion and keeps output editable. A stage receipt, PDF or readback proves staging—not visual quality, installation or external approval.

## Actual render review

Run `render-review` with compiled input, actual native snapshot and PDF. `renderDiagnostics` reports density, bound numeral issues, actual native geometry collisions and optional PDF orphan lines; it never sets human inspection true. Missing PDF words means orphan-wrap detection is explicitly unchecked. Intentional image/text overlays are excluded, while text-text overlaps and out-of-bounds text are flagged. Inspect full and phone pages for hierarchy, wraps, crops, labels, marks, arrows, product truth and bounds. Record `VisualInspection` only after human inspection. External release remains held until the correct human purpose receipt and disclosure/rights clearance.

## Evidence and notes

V2.1 footnotes are claim-linked, audience-safe and capped at 240 characters; fonts are not reduced, and reflow requires actual inspection. `TalkTrack` notes export only when audience and recipients are cleared; audit notes are internal. The full evidence manifest is restricted.

## Revision and promotion

`stageRevision` snapshots the complete baseline, backs it up, patches a review copy using a narrow allowlist, reads it back and confirms the source stayed unchanged. Preserve human edits and explicit attachments. `promoteRevision` is fail-closed without provider atomic conditional revisions; a preflight hash is not a lock. If unsupported, deliver the review copy and hold production promotion.
