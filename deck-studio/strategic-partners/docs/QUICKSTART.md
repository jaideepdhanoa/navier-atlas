# Quickstart

This is a partner-neutral package for source-linked strategic-partnership evaluation decks. Its CLI is offline: it does not connect to a service, create a native deck, publish a presentation, or certify visual QA. The library also provides an optional authenticated adapter for native create/stage/revise; see [`NATIVE-LIFECYCLE.md`](NATIVE-LIFECYCLE.md). Start with the [operating workflow](WORKFLOW.md) for the editorial and review checkpoints.

## 1. Create and complete an intake

From the package directory:

```sh
bun src/cli.ts init --out ./my-intake --partner "Example Vessel Company" --entity "Example Vessel Company Ltd"
```

`init` refuses overlong display names rather than shrinking the fixed name area. It creates a fictional `INCOMPLETE-INTAKE` hold and an empty scaffold. Replace every demo field, add source-linked claims and locally archived assets, and obtain review before any production use. It never overwrites existing files.

A project should distinguish:

- evidence sources and claims (`Source`, `Claim`) with audience clearance, evidence class, basis, and limitations;
- opportunities (`Opportunity`) with product, customer, payer, contributions, partner benefit, commercial logic, and next question;
- visuals (`Asset`/`Visual`) with exact version hash, maturity, rights, clearance, role tags, caption, and crop guidance; and
- slides with explicit claims, sources, opportunities, notes, and a selected narrative layout.

Use the approved asset library first. `registry-cli.ts` can build and search a local catalogue without network fetches:

```sh
bun src/registry-cli.ts build --project ./my-intake/project.json --out ./registry.json
bun src/registry-cli.ts shortlist --registry ./registry.json --maturity actual --rights held --limit 12 --out ./shortlist.html
```

## 2. Validate and storyboard

```sh
bun src/cli.ts validate --project ./my-intake/project.json
bun src/cli.ts validate --project ./my-intake/project.json --public
bun src/cli.ts assets --project ./my-intake/project.json --query service
bun src/cli.ts review-template --project ./my-intake/project.json --stage storyboard --out ./storyboard-review
```

The storyboard template is unsigned and `HELD`. A human must review the commercial thesis, evidence/disclosure, visual choices, and unresolved questions. This internal editorial checkpoint is not approval to send externally. A separate comprehension/visual review and release approval are required later.

## 3. Compile locally

```sh
bun src/cli.ts compile --project ./examples/public-demo/project.json --out ./build-demo
bun src/cli.ts compile --project ./examples/public-demo/project.json --out ./build-demo --urls ./asset-url-map.json
```

`compile` checks schema references, audience clearance, policies, local asset paths, hashes, image metadata, and publication privacy. It emits `compiled.json`, `visible-copy.md`, `storyboard.md`, `content-source.json`, `image-manifest.json`, `build-manifest.json`, and a held storyboard review template. URL mappings are local input; they do not download or verify image bytes. Missing mappings use offline `asset://` placeholders and remain a native-staging hold. A build directory belonging to another input is never overwritten.

The output explicitly records that native rendering and visual QA were not performed. Visible copy is useful for comprehension review, but it is not a rendered deck.

## 4. Native boundary

A caller with an authenticated provider implements `NativePort` and calls the lifecycle functions in `src/lifecycle.ts`. The local CLI itself remains offline. Creation requires a storyboard receipt and creates a new staging destination; it must never target another partner's or a live production deck. Revision staging duplicates the source into a backup and review copy, applies a narrow verified plan there, and stops if the source changes.

The current Google Slides connection lacks atomic conditional revision support. Consequently, `promoteRevision` remains held unless a provider supplies that capability. A preflight hash is not a lock, and the package must not claim concurrent live-write safety. See [`NATIVE-LIFECYCLE.md`](NATIVE-LIFECYCLE.md) and [`REVISION-SAFETY.md`](REVISION-SAFETY.md).

## 5. Tests

```sh
bun test tests --timeout 30000
```

Tests are local. They do not constitute native rendering, visual inspection, claim certification, or release approval.

## Public demo and privacy

`examples/public-demo/project.json` is wholly synthetic and uses fictional identities, original simple artwork, and a clearly fictional source. Do not copy private partners, names, assets, service-account IDs, production deck IDs, relationship notes, or proposals into this public package.
