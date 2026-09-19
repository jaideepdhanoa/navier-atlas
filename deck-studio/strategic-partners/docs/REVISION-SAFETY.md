# Native revision safety

Revision is a controlled patch to a fresh native snapshot, not a rebuild of a human-edited presentation. The source deck, benchmark IDs, live IDs and protected objects remain protected.

## Protocol

1. Read a complete snapshot: ordered slides, elements/groups, notes, text styles, image properties, transforms and revision token when available.
2. Bind exact presentation ID/title and reject protected IDs. Compute the canonical snapshot hash; never accept a caller-supplied hash as truth.
3. Use `makePatchPlan` with an explicit revision label, operations and object allowlist. Verify the plan before requests.
4. Create a backup and review copy. Recompute/verify the plan on the copy, apply only allowlisted operations, read back fully, and confirm the source stayed unchanged.
5. Obtain a human visual review receipt whose `subjectHash` is the plan hash before promotion.
6. Promote only through provider atomic conditional revisions. If unsupported, hold promotion and deliver the review copy.

## Supported operations

The allowlist must include every target and explicit attached mark, without duplicates, and every allowlisted object must be targeted. Supported operations are:

- specified text deletion/insertion in one `TEXT_BOX` (never replace-all);
- axis-aligned movement with fresh EMU geometry, optional aspect preservation, and the same affine move for an explicitly attached mark;
- exact HTTPS image replacement using native `CENTER_CROP`, followed by visual inspection.

Delete-slide, full rebuild, arbitrary crop requests and other unlisted operations are unsupported. Image replacement can change intrinsic bytes/crop; structural readback does not replace visual review.

## Attachment and human-edit protection

Use explicit attachment records/relations. Preserve logos, hull marks, crops, notes, text, images, and unrequested objects. Re-read current intrinsic image dimensions before moving an attached mark; stale dimensions or stale parent hash are a hold. Unexpected source or review-copy changes stop the workflow.

`verifyPatchPlan` can return `no-op` only for a matching recorded revision/plan/after hash. This is idempotency, not concurrency protection. The current adapter's lack of atomic conditional revisions keeps live promotion held. Agent or fixture inspection cannot satisfy a human finished-deck or external-release gate.
