# V2 asset catalogue and visual truth

`Asset` records are source-linked and conservative. They include ID, local path, exact SHA-256, dimensions, MIME type, maturity (`actual`, `demonstrated`, `concept`, `context`, `brand`), title/vessel/tags, source IDs, visibility, audience clearance, rights note, caption, and optional focal/keep/crop guidance. `VisualBrief` adds the intended argument, required visible features, prohibited implications, origin (`existing`, `generated`, `derivative`, `fixture`), reference sources, architecture options, unresolved choices, optional source-slide reference, and review record.

Use a visual because of the argument it makes: a control image is not automatically evidence of lower drag; a concept scene cannot establish performance, deployment, selected configuration, approvals or economics. Actual/demonstrated, context and proposed material must remain visibly distinct. Generated scenes need recognizable product references and an illustrative/proposed caption.

## Reuse and search

The offline registry reads project JSON and safe local files; it does not fetch URLs, grant rights, or identify pixels. Build/search/shortlist/contact-sheet/report commands:

```sh
bun src/registry-cli.ts build --project ./project.json --out ./registry.json
bun src/registry-cli.ts search --registry ./registry.json --mission passenger --clearance partner
bun src/registry-cli.ts shortlist --registry ./registry.json --role "buyer gallery" --rights held --limit 12 --out ./shortlist.html
bun src/registry-cli.ts contact-sheet --registry ./registry.json --mission service --out ./shortlist.md --format markdown
bun src/registry-cli.ts report --registry ./registry.json
```

Matching uses exact local bytes and keeps project namespaces/collisions separate. Clearance and rights are copied conservatively; a second project cannot upgrade them. URLs, absolute paths, traversal, missing files and escaping symlinks are not fetched. An accessible URL is not automatic release clearance.

## Attachments and crops

Parent/mark relationships must be explicit via `VisualAttachment` (`assetId`, `parentSha256`, `assetSha256`, normalized `region`, review). Registry extensions may include explicit `attachedMarks`, `attachedMarkAssetIds`, `hullLogoAssetIds`, `attachedHullLogos`, or `hullLogoAssetId`; absent metadata remains `status:'unknown'`, not inferred empty. Parent geometry is normalized to the uncropped image, so stale parent bytes or clipped marks are refused. Preserve attached hull marks during narrow revisions and recalculate geometry from current native dimensions.

Arbitrary crop metadata is not silently applied by native rendering. Use an archived derivative or reviewed native edit for custom crops. Focal/keep regions produce review guidance, not automatic CENTER_CROP truth.

## Selection checklist

For every selected visual, record: argument; source and exact version; maturity/caption; required features; prohibited implications; crop/focal review; attachment relation if applicable; rights and audience clearance; and unresolved architecture choices. A shortlist is a selection aid, not approval. Keep restricted source catalogues and relationship imagery outside this package.
