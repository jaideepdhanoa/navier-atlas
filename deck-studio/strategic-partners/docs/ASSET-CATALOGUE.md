# Local cross-project asset registry

`src/registry.ts` and `src/registry-cli.ts` provide a small, offline registry for the V1 project package. They **read** project JSON and local asset files; they do not fetch URLs, change projects, make rights decisions, publish assets, or update the existing package CLI.

The registry is intentionally a catalogue and review aid, not a new project schema. It derives its records from the existing `Project`/`Asset` contract and keeps partner-specific source projects outside this package.

## What is recorded

Each asset record contains:

- the source `asset.id` as `logicalId`, a project namespace (`projectBinding`), a stable record id, and the source project/revision;
- the declared SHA-256, the locally observed SHA-256 when the safe local path exists, a `hashStatus`, and `exactVersionHash` for exact-byte reuse matching;
- provenance (`projectPath`, `sourceIds`, caption, local asset path), vessel, missions, geography, roles, maturity, visibility, and `clearedFor` audiences;
- a conservative `rightsStatus`: `cleared`, `held`, or `unknown`;
- focal point, protected/keep region (including an explicitly supplied `protectedRegion` extension), and crop metadata;
- attachment relations, including hull-logo relations, when explicitly present.

`Asset.id` is **not** assumed to be globally unique. Every source record stays separate, even where two records have the same id or exact bytes. Reuse is matched by exact local bytes (`exactVersionHash`), not by filename, title, or visual similarity. Cross-project logical-id reuse is listed under `collisions` rather than silently merged.

A source `rightsStatus`/`rightsCleared` field, if present, is honored. Otherwise the registry only recognizes conservative wording such as “rights cleared” or “internal workflow use only” in `rightsNote`; all other cases are `unknown`. Audience clearance is copied, not inferred. Reuse-report aggregates use the strictest rights/visibility and the intersection of audience clearance, so copying an asset into a second project cannot upgrade it.

Attachment metadata is never inferred from filenames, logos, crops, or image pixels. If no supported attachment field is present, the result is:

```json
{
  "attachments": {
    "status": "unknown",
    "attachedMarkAssetIds": null,
    "hullLogoAssetIds": null,
    "fields": []
  }
}
```

An explicit `attachedMarks: []` or `hullLogoAssetIds: []` is different: it records a known empty relation for that field. Supported optional source metadata (without changing `types.ts`) is `attachedMarks`, `attachedMarkAssetIds`, `hullLogoAssetIds`, `attachedHullLogos`, and `hullLogoAssetId`. Values can be ids or objects containing `assetId`, `id`, or `ref`. Unsupported shapes remain conservative and are not guessed.

## Build a registry

From the package directory, pass one or more local project JSON paths. `--project` can be repeated; `--projects` accepts a comma-separated list. The output is deterministic for the same source paths and bytes (there is no generated timestamp).

```sh
bun src/registry-cli.ts build \
  --project ./examples/public-demo/project.json \
  --out ./build/asset-registry.json

# Multiple projects (including restricted projects kept outside this package)
bun src/registry-cli.ts build \
  --project /path/to/project-a/project.json \
  --project /path/to/project-b/project.json \
  --out /path/to/review/asset-registry.json
```

Building hashes only local, safe, relative asset paths under each project directory. URLs, absolute paths, traversal, missing files, and symlinks escaping the project directory are not fetched; their records have no observed hash and are marked unavailable/missing. A declared valid SHA-256 may still appear as `exactVersionHash` when a file is unavailable, but `hashStatus` makes that limitation visible. A local mismatch is marked `mismatch`; do not treat it as a verified release asset.

## Search and shortlist

Search is case-insensitive. Mission, geography, role, vessel, project id, and logical id use exact-or-substring tag matching. Enum filters (`maturity`, `clearance`, `rights`) match explicitly. Repeated filters are OR within one dimension and AND across dimensions.

```sh
bun src/registry-cli.ts search \
  --registry ./build/asset-registry.json \
  --mission passenger --geography "San Francisco Bay" \
  --maturity actual --clearance internal

bun src/registry-cli.ts shortlist \
  --registry ./build/asset-registry.json \
  --role "buyer gallery" --rights held --limit 12 \
  --out ./build/shortlist.html
```

The `shortlist` command writes a read-only review artifact; it does not modify any source project or registry. Use `--format markdown` or a `.md` output for a text contact sheet:

```sh
bun src/registry-cli.ts contact-sheet \
  --registry ./build/asset-registry.json \
  --mission service --out ./build/service-shortlist.md --format markdown
```

HTML and Markdown thumbnails are relative paths to local files only. A missing or unavailable local file is shown as “No local thumbnail”; no URL is requested. The sheet is a selection aid, not an approval or rights clearance.

## Reuse and collision report

```sh
bun src/registry-cli.ts report --registry ./build/asset-registry.json
```

The report groups records by exact version hash and includes the records, projects, strictest rights status/visibility, and effective clearance intersection. `reusableVersionCount` counts byte-identical versions represented in more than one source record. `collisions` lists every logical id used by more than one record; this is deliberately conservative even if the bytes happen to match.

Programmatic use is also available:

```ts
import { buildRegistry, reuseReport, searchRegistry } from './src/registry';

const registry = await buildRegistry([
  './examples/public-demo/project.json',
  '/path/to/a/private/project.json',
]);
const passenger = searchRegistry(registry, { mission: 'passenger', rights: 'cleared' });
const reuse = reuseReport(registry);
```

## Scope and limitations

- The registry does not decide whether an image may be sent to a partner. Human review and the source project's rights process remain authoritative.
- It does not inspect pixels to identify hull marks, logos, locations, maturity, or deployment claims.
- It does not merge conflicting metadata, repair stale hashes, or infer missing provenance.
- It does not create or modify a new universal schema. Optional relation fields are read only as explicit extensions on source asset JSON.
- The generic tests create fictional projects in temporary directories. Private project files may be supplied at runtime but are not copied into this package, fixtures, or public examples.
