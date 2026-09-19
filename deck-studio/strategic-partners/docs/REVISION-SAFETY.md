# Native revision safety

This package provides a deliberately narrow, partner-neutral patch protocol in `src/revisions.ts`. It is an adapter boundary, not a claim that a current Slides connection can make a concurrent update safe.

## Required protocol

1. Read a complete native deck snapshot: ordered slides, page elements, groups, notes, image properties, transforms, and text styles.
2. Bind that snapshot to the expected presentation ID and exact title. Protected IDs are always rejected.
3. Build a plan with `makePatchPlan`. It computes the canonical `snapshotHash` as `baseHash`, records an explicit object allowlist, and computes a deterministic `planHash`. Never accept a caller-supplied hash without recomputing it.
4. Before emitting requests, call `verifyPatchPlan`, then `patchRequests`. A baseline mismatch, wrong deck, malformed native geometry, duplicate target, duplicate stale revision, or modified plan is a hold/error.
5. Keep a native backup and obtain review before applying a live plan in an adapter. After native write, read back the complete deck and call `verifyPatchResult`.
6. Treat any image replacement as requiring actual visual review even when structural readback passes.

`verifyPatchPlan` returns `no-op` only when the binding's `lastApplied.revision`, `planHash`, and recorded `afterHash` all match the current snapshot. It returns `applied` for a new plan. This does not eliminate a last-millisecond race. The current Google Slides connection has no atomic `writeControl`/conditional-revision primitive, so production promotion must remain held unless the adapter supplies conditional revisions.

## Supported operations

The allowlist must contain every target and every attached mark, with no duplicates; every allowlisted object must be targeted. The protocol supports only:

- **Text:** delete and insert text in one specified native `TEXT_BOX`; optional font size is expressed explicitly in PT. It never performs replace-all.
- **Move:** axis-aligned EMU geometry only. Fresh native size and transform are required. PT dimensions, missing units, grouped objects, rotation, and skew are rejected. Aspect ratio is preserved unless `preserveAspect: false` is explicit. An attached mark must be separately named in the allowlist and receives the same affine move.
- **Replace image:** exact HTTPS URL and native `CENTER_CROP` only. A requested crop is unsupported. The provider may therefore change intrinsic image size and crop properties while replacing the source. Readback must preserve the displayed frame and non-source image styling, and must compare `sourceUrl` exactly when supplied. Structural verification sets `requiresVisualReview: true`; inspect the actual rendered slide before approval.

Delete-slide, full rebuild, replace-all, and other unlisted operations are intentionally unsupported. The protocol never assumes that a preflight hash is a lock.

## Snapshot and readback boundaries

The canonical hash ignores only top-level `revisionId`, image `contentUrl`, and notes-page thumbnails. Meaningful text/style, image crops and source URLs, grouped objects, notes, slide order, logos, and metadata remain part of the digest. Readback comparison is stricter for unallowed objects and detects changes outside the explicit allowlist.

Before promotion, preserve a native backup and require a human visual review receipt whose `subjectHash` is the plan hash. A review receipt is evidence of a human decision, not something this package can invent. Editorial storyboard approval, comprehension review, visual review, and external release approval are distinct gates.
