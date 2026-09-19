# Native lifecycle and adapter boundary

The package's CLI is offline, but `src/lifecycle.ts` contains a native lifecycle library. It contains no credentials, accounts or destination IDs. A caller injects an authenticated `NativePort`.

`adapters/tasklet.ts` is an optional, account-neutral adapter for approved Tasklet Google Slides/Drive connections. The caller supplies the exact connection IDs and `invokeTool` function at runtime:

```ts
import { invokeTool } from '@tasklet/tools/v2';
import { makeTaskletNativePort } from './adapters/tasklet';

const port = makeTaskletNativePort(approvedConnectionsFromPrivateConfig, invokeTool);
```

Before using it in Tasklet, read the current connection instructions and tool declarations and obtain any needed permissions. Do not save connection IDs in the public package. Other environments implement `NativePort` using their own authorized integration.

## `NativePort`

A provider adapter implements:

```ts
interface NativePort {
  conditionalRevisions: boolean;
  snapshot(id: string): Promise<DeckSnapshot & { revisionId?: string }>;
  create(title: string): Promise<{ presentationId: string; url?: string }>;
  duplicate(id: string, title: string): Promise<{ presentationId: string; url?: string }>;
  batch(id: string, requests: SlidesRequest[], requiredRevision?: string): Promise<unknown>;
  exportPDF?(id: string, path: string): Promise<unknown>;
}
```

`snapshot` must return the complete native state needed by the revision checks, not a reduced visible-text representation. `batch` must honor `requiredRevision` when the provider supports conditional revisions. `exportPDF` is optional and is used only to record an export receipt after a successful stage.

## Create a new staging deck

`createStaging(project, compiled, port, options)` is for a new partner-bound staging destination. It:

- revalidates the project and compiled input;
- requires an approved storyboard `ReviewReceipt` matching `compiled.inputHash`;
- requires verified remote bytes for every selected asset, except explicitly listed internal-only exceptions;
- creates or resumes a journaled destination without replaying an uncertain create;
- checks title, page size, slide identity, deterministic requests, image bindings, notes, and readback; and
- writes a binding and receipts only after completion.

Use a fresh output directory per revision. `createStaging` refuses a directory belonging to different input, preserves a changed completed deck rather than replaying it, and will not silently delete unexpected slides. A pristine provider title slide may be removed only with the explicit `allowPristineTitleSlide` option and after it is archived.

Neutral usage shape (values must come from the caller's real project, compiled output, adapter, verified asset records, and human review):

```ts
import { createStaging } from './src/lifecycle';
import type { NativePort } from './src/lifecycle';
import type { Project, CompiledDeck, ReviewReceipt } from './src/types';

const project: Project = loadProjectFromYourPrivateWorkspace();
const compiled: CompiledDeck = loadCompiledOutput();
const storyboard: ReviewReceipt = loadHumanStoryboardReceipt();
const port: NativePort = makeAuthenticatedProviderAdapter();

const receipt = await createStaging(project, compiled, port, {
  root: projectRoot,
  out: stagingOutputDirectory,
  storyboard,
  verifiedAssetHashes: verifiedAssetHashesFromProviderOrArchive,
  // Use only for explicitly approved internal exceptions, never for public release.
  unverifiedInternalAssetIds: approvedInternalExceptions,
  protectedIds: protectedDestinationIds,
  title: stagingTitle,
  allowPristineTitleSlide: true,
});
```

The resulting `stage-receipt.json`, `binding.json`, `native-after.json`, and optional PDF are evidence of staging work, not an external release approval. The caller must inspect the actual rendered deck and record separate comprehension/visual and release decisions.

## Stage a narrow revision on a review copy

`stageRevision(binding, plan, port, out)` reads and verifies the current source, creates a backup and review copy, recomputes a plan for that copy, applies only the supported operations, verifies full readback, and confirms that the source stayed unchanged. It stops when the source or review copy differs unexpectedly. It is the recommended path for review before any production promotion.

```ts
import { stageRevision } from './src/lifecycle';
import { makePatchPlan } from './src/revisions';
import type { Binding, PatchOperation } from './src/types';

const binding: Binding = loadBindingFromPrivateProject();
const sourceSnapshot = await port.snapshot(binding.presentationId);
const operations: PatchOperation[] = requestedNarrowChanges;
const plan = makePatchPlan(binding, sourceSnapshot, {
  revision: nextRevisionLabel,
  operations,
  allowedObjectIds: explicitlyApprovedObjectIds,
});

const reviewCopy = await stageRevision(binding, plan, port, revisionOutputDirectory);
// Inspect the rendered review copy and obtain a human visual review receipt.
```

Do not turn a revision request into a full rebuild. Retain human image/crop/logo edits and keep the latest native snapshot as the baseline.

## Promote only with atomic conditional revisions

`promoteRevision(binding, plan, port, review)` is fail-closed when `port.conditionalRevisions` is false. It requires a visual review receipt matching `plan.planHash`, rechecks the source immediately before write, creates a backup, sends requests with the provider's revision token, verifies readback, and returns an updated binding. A duplicate matching revision is a safe no-op; a stale or changed baseline is an error.

```ts
import { promoteRevision } from './src/lifecycle';

if (!port.conditionalRevisions) {
  throw new Error('Production promotion held: adapter lacks atomic conditional revisions.');
}

const visual: ReviewReceipt = loadHumanVisualReviewReceiptFor(plan.planHash);
const result = await promoteRevision(binding, plan, port, visual);
```

The current Google Slides connection does not expose the required atomic conditional-revision primitive. Therefore production promotion is held there; a preflight snapshot hash cannot be presented as concurrency protection. A provider must supply real conditional revision support before this gate can open.

## Review and release meanings

A storyboard receipt records internal editorial approval of the thesis and layout. A comprehension or visual receipt records later human inspection of the relevant artifact. A release receipt records explicit approval for external circulation. Templates generated by the CLI are unsigned and held. None can be synthesized by passing validation or by completing a native batch.
