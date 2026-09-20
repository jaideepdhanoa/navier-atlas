# Native revision safety

Revision is a controlled patch to a fresh native snapshot, never a rebuild over a human-edited presentation.

1. Read the complete snapshot (slides, groups, elements, notes, styles, transforms, images and revision token).
2. Bind exact presentation identity and reject protected IDs; compute the canonical snapshot hash.
3. Build and verify an explicit allowlisted patch plan.
4. Back up and create a review copy; recompute the plan there, apply only narrow operations, read back fully and confirm the source is unchanged.
5. Obtain human visual inspection with the matching plan hash.
6. Promote only via atomic conditional revisions; otherwise hold and deliver the review copy.

Supported operations are specified text insertion/deletion in one text box, axis-aligned movement with fresh geometry (including explicit attached marks), and exact-HTTPS image replacement using native center crop. No delete-slide, replace-all, arbitrary crop, full rebuild or unconditional overwrite.

Preserve logos, hull marks, crops, notes, text, images and unrequested objects. Re-read image dimensions and parent hashes before moving attachments. Source or review-copy drift is a hold. A no-op is idempotency, not concurrency protection. Tests, diagnostics and agent inspection cannot satisfy human finished-deck or external-release gates.
