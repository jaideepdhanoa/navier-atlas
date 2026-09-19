import { createHash } from 'node:crypto';
import type { Binding, DeckSnapshot, ElementSnapshot, PatchOperation, PatchPlan, SlideSnapshot, SlidesRequest } from './types';

/** Errors from the deliberately narrow, native-only revision adapter. */
export class RevisionSafetyError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'RevisionSafetyError';
  }
}

type AnyRecord = Record<string, any>;
type OperationInput = { revision: string; operations: PatchOperation[]; allowedObjectIds: string[] };
export type PatchVerification = { status: 'no-op' | 'applied'; plan: PatchPlan; afterHash?: string; requiresVisualReview?: boolean };

type NativeGeometry = {
  sizeWidth: number;
  sizeHeight: number;
  scaleX: number;
  scaleY: number;
  translateX: number;
  translateY: number;
  shearX: number;
  shearY: number;
};
type Bounds = { x: number; y: number; w: number; h: number };

const EPSILON = 1e-6;
const HASH_HEX = /^[a-f0-9]{64}$/;

function fail(message: string): never { throw new RevisionSafetyError(message); }
function isRecord(value: unknown): value is AnyRecord { return !!value && typeof value === 'object' && !Array.isArray(value); }
function finite(value: unknown): value is number { return typeof value === 'number' && Number.isFinite(value); }
function close(a: number, b: number) { return Math.abs(a - b) <= EPSILON * Math.max(1, Math.abs(a), Math.abs(b)); }
function own(value: unknown, key: string) { return isRecord(value) && Object.prototype.hasOwnProperty.call(value, key); }

/**
 * Canonical JSON used by the revision protocol. Only explicitly documented
 * volatile values are removed; key sorting makes the digest independent of
 * object construction order.
 */
function canonicalValue(value: unknown, path: string[], options: { ignoreImageContentUrl: boolean }): unknown {
  if (Array.isArray(value)) return value.map(item => canonicalValue(item, path, options));
  if (!isRecord(value)) return value;
  const out: AnyRecord = {};
  for (const key of Object.keys(value).sort()) {
    if (path.length === 0 && key === 'revisionId') continue;
    const lowerPath = path.map(part => part.toLowerCase());
    const underNotesPage = lowerPath.includes('notespage') || lowerPath.includes('notes_page');
    const noteThumbnailKey = ['thumbnail', 'pagethumbnail', 'thumbnailurl'].includes(key.toLowerCase());
    if (underNotesPage && noteThumbnailKey) continue;
    const underImage = lowerPath.includes('image') || lowerPath.includes('imageproperties') || lowerPath.includes('image_properties');
    if (options.ignoreImageContentUrl && key === 'contentUrl' && underImage) continue;
    out[key] = canonicalValue(value[key], [...path, key], options);
  }
  return out;
}
function digest(value: unknown, options: { ignoreImageContentUrl: boolean }) {
  return createHash('sha256').update(JSON.stringify(canonicalValue(value, [], options))).digest('hex');
}

/** Stable deck hash. Top-level revisionId, image contentUrl, and notes-page thumbnails are volatile. */
export function snapshotHash(snapshot: DeckSnapshot): string {
  return digest(snapshot, { ignoreImageContentUrl: true });
}

function pageElementsOf(snapshot: DeckSnapshot): unknown[] {
  if (!isRecord(snapshot) || !Array.isArray(snapshot.slides)) fail('Snapshot must contain an ordered slides array.');
  return snapshot.slides.flatMap((slide: any) => Array.isArray(slide?.pageElements) ? slide.pageElements : []);
}
function visitElement(value: unknown, out: Map<string, ElementSnapshot>) {
  if (!isRecord(value)) return;
  if (typeof value.objectId === 'string' && value.objectId.length > 0) {
    if (out.has(value.objectId)) fail(`Duplicate native object ID: ${value.objectId}`);
    out.set(value.objectId, value as ElementSnapshot);
  }
  const group = value.elementGroup;
  if (isRecord(group) && Array.isArray(group.children)) for (const child of group.children) visitElement(child, out);
}
/** Return every native page element, including children of element groups. */
export function elementsById(snapshot: DeckSnapshot): Map<string, ElementSnapshot> {
  const out = new Map<string, ElementSnapshot>();
  for (const element of pageElementsOf(snapshot)) visitElement(element, out);
  return out;
}

function elementKind(element: ElementSnapshot): 'text' | 'image' | 'group' | 'shape' | 'other' {
  if (own(element, 'elementGroup')) return 'group';
  if (isRecord(element.image)) return 'image';
  if (isRecord(element.shape)) return element.shape.shapeType === 'TEXT_BOX' ? 'text' : 'shape';
  return 'other';
}
function requireElement(map: Map<string, ElementSnapshot>, id: string, operation: string): ElementSnapshot {
  if (typeof id !== 'string' || id.length === 0) fail(`${operation} requires a non-empty objectId.`);
  const element = map.get(id);
  if (!element) fail(`${operation} targets missing objectId ${id}.`);
  return element;
}
function requireUnit(value: unknown, expected: string, path: string): number {
  if (!isRecord(value) || value.unit !== expected || !finite(value.magnitude)) fail(`${path} must use finite ${expected} units.`);
  return value.magnitude;
}
function nativeGeometry(element: ElementSnapshot): NativeGeometry {
  if (elementKind(element) === 'group') fail(`Grouped object ${element.objectId} is not movable.`);
  const size = element.size;
  if (!isRecord(size)) fail(`Object ${element.objectId} has no native size.`);
  const sizeWidth = requireUnit(size.width, 'EMU', `${element.objectId}.size.width`);
  const sizeHeight = requireUnit(size.height, 'EMU', `${element.objectId}.size.height`);
  const transform = element.transform;
  if (!isRecord(transform) || transform.unit !== 'EMU') fail(`Object ${element.objectId} must have an EMU transform.`);
  for (const key of ['scaleX', 'scaleY']) if (!finite(transform[key])) fail(`Object ${element.objectId} has malformed transform.${key}.`);
  const translateX=transform.translateX??0,translateY=transform.translateY??0;
  if(!finite(translateX)||!finite(translateY))fail(`Object ${element.objectId} has malformed translation.`);
  const scaleX = transform.scaleX as number, scaleY = transform.scaleY as number;
  if (scaleX <= 0 || scaleY <= 0 || sizeWidth <= 0 || sizeHeight <= 0) fail(`Object ${element.objectId} must have positive native dimensions and scales.`);
  const shearX = transform.shearX === undefined ? 0 : transform.shearX;
  const shearY = transform.shearY === undefined ? 0 : transform.shearY;
  if (!finite(shearX) || !finite(shearY) || !close(shearX, 0) || !close(shearY, 0)) fail(`Object ${element.objectId} has rotation/skew and is outside the axis-aligned move scope.`);
  for (const candidate of [element.rotation, (element as any).rotate, (element.shape as any)?.rotation]) if (candidate !== undefined && (!finite(candidate) || !close(candidate, 0))) fail(`Object ${element.objectId} has rotation and is outside the axis-aligned move scope.`);
  return { sizeWidth, sizeHeight, scaleX, scaleY, translateX, translateY, shearX, shearY };
}
function boundsOf(geometry: NativeGeometry): Bounds { return { x: geometry.translateX, y: geometry.translateY, w: geometry.sizeWidth * geometry.scaleX, h: geometry.sizeHeight * geometry.scaleY }; }
function validBounds(value: unknown, path: string): Bounds {
  if (!isRecord(value) || !finite(value.x) || !finite(value.y) || !finite(value.w) || !finite(value.h) || value.w <= 0 || value.h <= 0) fail(`${path} must contain finite positive x/y/w/h native bounds.`);
  return { x: value.x, y: value.y, w: value.w, h: value.h };
}
function sameAspect(a: Bounds, b: Bounds) { return close(a.w / a.h, b.w / b.h); }

function validateHttps(url: unknown) {
  if (typeof url !== 'string' || !url.startsWith('https://')) fail('replace-image requires an exact HTTPS URL.');
  let parsed: URL;
  try { parsed = new URL(url); } catch { fail('replace-image requires a parseable HTTPS URL.'); }
  if (parsed.protocol !== 'https:' || !parsed.hostname) fail('replace-image requires an exact HTTPS URL.');
}
function assertOperationTargets(snapshot: DeckSnapshot, operations: PatchOperation[], allowedObjectIds: string[]) {
  const map = elementsById(snapshot);
  if (!Array.isArray(operations) || operations.length === 0) fail('A patch plan requires at least one operation.');
  if (!Array.isArray(allowedObjectIds) || allowedObjectIds.length === 0) fail('A patch plan requires a non-empty object allowlist.');
  const allowed = new Set<string>();
  for (const id of allowedObjectIds) {
    if (typeof id !== 'string' || id.length === 0) fail('The object allowlist contains an invalid ID.');
    if (allowed.has(id)) fail(`Repeated identical allowlist ID: ${id}.`);
    allowed.add(id); requireElement(map, id, 'allowlist');
  }
  const touched = new Set<string>();
  for (const operation of operations) {
    if (!isRecord(operation) || typeof operation.kind !== 'string') fail('Malformed or unsupported patch operation.');
    if (typeof operation.objectId !== 'string' || operation.objectId.length === 0) fail(`${operation.kind} requires a non-empty objectId.`);
    if (touched.has(operation.objectId)) fail(`Repeated identical target ID: ${operation.objectId}.`);
    touched.add(operation.objectId);
    if (!allowed.has(operation.objectId)) fail(`Target ${operation.objectId} is outside the explicit object allowlist.`);
    const element = requireElement(map, operation.objectId, operation.kind);
    if (operation.kind === 'text') {
      if (elementKind(element) !== 'text') fail(`Text replacement target ${operation.objectId} is not a native text box.`);
      if (typeof operation.text !== 'string') fail('Text replacement requires a string.');
      if (operation.fontSize !== undefined && (!finite(operation.fontSize) || operation.fontSize <= 0)) fail('Text fontSize must be a positive point value.');
    } else if (operation.kind === 'move') {
      const before = boundsOf(nativeGeometry(element));
      const requested = validBounds(operation.bounds, `move ${operation.objectId}.bounds`);
      nativeGeometry(element);
      if (operation.preserveAspect !== false && !sameAspect(before, requested)) fail(`Move ${operation.objectId} changes aspect ratio; set preserveAspect:false explicitly.`);
      if (operation.attachedMarks !== undefined) {
        if (!Array.isArray(operation.attachedMarks)) fail('attachedMarks must be an array.');
        const seen = new Set<string>();
        for (const markId of operation.attachedMarks) {
          if (typeof markId !== 'string' || markId.length === 0 || seen.has(markId)) fail(`Invalid or repeated attached mark ID on ${operation.objectId}.`);
          seen.add(markId);
          if (markId === operation.objectId) fail('A move target cannot attach itself as a mark.');
          if (!allowed.has(markId)) fail(`Attached mark ${markId} is outside the explicit object allowlist.`);
          const mark = requireElement(map, markId, 'attached mark');
          nativeGeometry(mark);
          if (touched.has(markId)) fail(`Repeated identical target ID: ${markId}.`);
          touched.add(markId);
        }
      }
    } else if (operation.kind === 'replace-image') {
      if (elementKind(element) !== 'image') fail(`Image replacement target ${operation.objectId} is not a native image.`);
      validateHttps(operation.url);
      if (operation.crop !== undefined) fail('replace-image crop is unsupported; native replacement uses CENTER_CROP without a requested crop.');
      if (typeof operation.assetId !== 'string' || operation.assetId.length === 0) fail('replace-image requires a non-empty assetId.');
    } else {
      fail(`Unsupported patch operation ${(operation as any).kind}; delete-slide and full rebuild are not supported.`);
    }
  }
  for (const id of allowed) if (!touched.has(id)) fail(`Allowlist ID ${id} is not targeted by this patch.`);
  return map;
}

function bindingAndSnapshot(binding: Binding, snapshot: DeckSnapshot) {
  if (!isRecord(binding) || binding.schemaVersion !== '1.0.0') fail('Binding schema version is not supported.');
  if (typeof binding.projectId !== 'string' || typeof binding.presentationId !== 'string' || typeof binding.expectedTitle !== 'string') fail('Binding project, presentation, and title are required.');
  if (!isRecord(snapshot) || typeof snapshot.presentationId !== 'string' || typeof snapshot.title !== 'string') fail('Snapshot presentationId and title are required.');
  if (binding.projectId.length === 0 || binding.presentationId.length === 0 || binding.expectedTitle.length === 0) fail('Binding project, presentation, and title cannot be empty.');
  if (snapshot.presentationId !== binding.presentationId) fail('Snapshot presentationId does not match the binding.');
  if (snapshot.title !== binding.expectedTitle) fail('Snapshot title does not match the binding.');
  if ((binding.protectedPresentationIds || []).includes(snapshot.presentationId)) fail('Protected presentation IDs cannot be patched.');
}
function planBody(plan: Omit<PatchPlan, 'planHash'>) {
  return { schemaVersion: plan.schemaVersion, projectId: plan.projectId, presentationId: plan.presentationId, revision: plan.revision, baseHash: plan.baseHash, operations: plan.operations, allowedObjectIds: plan.allowedObjectIds };
}
function computedPlanHash(plan: PatchPlan) { return digest(planBody(plan), { ignoreImageContentUrl: false }); }
function validatePlanEnvelope(plan: PatchPlan) {
  if (!isRecord(plan) || plan.schemaVersion !== '1.0.0') fail('Patch plan schema version is not supported.');
  if (typeof plan.projectId !== 'string' || typeof plan.presentationId !== 'string' || typeof plan.revision !== 'string' || plan.revision.length === 0) fail('Patch plan identity and revision are required.');
  if (!HASH_HEX.test(plan.baseHash)) fail('Patch plan baseHash is malformed.');
  if (!HASH_HEX.test(plan.planHash)) fail('Patch plan planHash is malformed.');
  if (computedPlanHash(plan) !== plan.planHash) fail('Patch plan hash does not match its contents.');
}
function duplicateRevision(binding: Binding, plan: PatchPlan, currentHash: string): PatchVerification | undefined {
  const applied = binding.lastApplied;
  if (!applied || applied.revision !== plan.revision) return undefined;
  if (applied.planHash !== plan.planHash) fail('Revision already applied with a different plan.');
  if (applied.afterHash === currentHash) return { status: 'no-op', plan, afterHash: currentHash };
  fail('Duplicate revision is stale: current snapshot is not the recorded afterHash.');
}

/** Create a deterministic, baseline-bound plan after validating every target. */
export function makePatchPlan(binding: Binding, currentSnapshot: DeckSnapshot, input: OperationInput): PatchPlan {
  bindingAndSnapshot(binding, currentSnapshot);
  if (!isRecord(input) || typeof input.revision !== 'string' || input.revision.length === 0 || !Array.isArray(input.allowedObjectIds)) fail('A non-empty revision and object allowlist are required.');
  const allowedObjectIds = [...input.allowedObjectIds].sort();
  const map = assertOperationTargets(currentSnapshot, input.operations, allowedObjectIds); void map;
  const baseHash = snapshotHash(currentSnapshot);
  const plan: PatchPlan = { schemaVersion: '1.0.0', projectId: binding.projectId, presentationId: binding.presentationId, revision: input.revision, baseHash, operations: input.operations, allowedObjectIds, planHash: '' };
  plan.planHash = computedPlanHash(plan);
  const prior = binding.lastApplied;
  if (prior?.revision === plan.revision) {
    if (prior.planHash !== plan.planHash) fail('Revision already applied with a different plan.');
    if (prior.afterHash !== baseHash) fail('Duplicate revision is stale: current snapshot is not the recorded afterHash.');
  }
  return plan;
}

/** Verify identity, baseline, target types, and the deterministic plan digest. */
export function verifyPatchPlan(binding: Binding, currentSnapshot: DeckSnapshot, plan: PatchPlan): PatchVerification {
  bindingAndSnapshot(binding, currentSnapshot);
  validatePlanEnvelope(plan);
  if (plan.projectId !== binding.projectId || plan.presentationId !== binding.presentationId) fail('Patch plan identity does not match the binding.');
  const currentHash = snapshotHash(currentSnapshot);
  const priorResult = duplicateRevision(binding, plan, currentHash);
  if (priorResult) return priorResult;
  if (plan.baseHash !== currentHash) fail('Patch baseline changed since the plan was created.');
  assertOperationTargets(currentSnapshot, plan.operations, plan.allowedObjectIds);
  return { status: 'applied', plan };
}

function targetTransform(before: NativeGeometry, requested: Bounds): AnyRecord {
  const old = boundsOf(before);
  return { scaleX: before.scaleX * requested.w / old.w, scaleY: before.scaleY * requested.h / old.h, shearX: 0, shearY: 0, translateX: requested.x, translateY: requested.y, unit: 'EMU' };
}
function affineForMark(before: NativeGeometry, markBefore: NativeGeometry, requested: Bounds): AnyRecord {
  const oldTarget = boundsOf(before), sx = requested.w / oldTarget.w, sy = requested.h / oldTarget.h;
  return { scaleX: markBefore.scaleX * sx, scaleY: markBefore.scaleY * sy, shearX: 0, shearY: 0, translateX: markBefore.translateX * sx + requested.x - oldTarget.x * sx, translateY: markBefore.translateY * sy + requested.y - oldTarget.y * sy, unit: 'EMU' };
}
function moveRequests(op: Extract<PatchOperation, { kind: 'move' }>, map: Map<string, ElementSnapshot>): SlidesRequest[] {
  const target = requireElement(map, op.objectId, 'move');
  const before = nativeGeometry(target), requested = validBounds(op.bounds, `move ${op.objectId}.bounds`);
  const requests: SlidesRequest[] = [{ updatePageElementTransform: { objectId: op.objectId, transform: targetTransform(before, requested), applyMode: 'REPLACE' } }];
  for (const markId of op.attachedMarks || []) {
    const mark = requireElement(map, markId, 'attached mark');
    requests.push({ updatePageElementTransform: { objectId: markId, transform: affineForMark(before, nativeGeometry(mark), requested), applyMode: 'REPLACE' } });
  }
  return requests;
}
/** Compile only the narrow native requests represented by a verified plan. */
export function patchRequests(plan: PatchPlan, currentSnapshot: DeckSnapshot): SlidesRequest[] {
  validatePlanEnvelope(plan);
  if (plan.baseHash !== snapshotHash(currentSnapshot)) fail('Patch baseline changed before request compilation.');
  const map = assertOperationTargets(currentSnapshot, plan.operations, plan.allowedObjectIds);
  const requests: SlidesRequest[] = [];
  for (const operation of plan.operations) {
    if (operation.kind === 'text') {
      requests.push({ deleteText: { objectId: operation.objectId, textRange: { type: 'ALL' } } });
      if (operation.text.length > 0) requests.push({ insertText: { objectId: operation.objectId, insertionIndex: 0, text: operation.text } });
      if (operation.fontSize !== undefined) requests.push({ updateTextStyle: { objectId: operation.objectId, textRange: { type: 'ALL' }, style: { fontSize: { magnitude: operation.fontSize, unit: 'PT' } }, fields: 'fontSize' } });
    } else if (operation.kind === 'move') requests.push(...moveRequests(operation, map));
    else if (operation.kind === 'replace-image') requests.push({ replaceImage: { imageObjectId: operation.objectId, url: operation.url, imageReplaceMethod: 'CENTER_CROP' } });
  }
  return requests;
}

function maskAllowed(value: unknown, allowed: Set<string>, inElements = false): unknown {
  if (Array.isArray(value)) return value.map(item => maskAllowed(item, allowed, inElements));
  if (!isRecord(value)) return value;
  if (inElements && typeof value.objectId === 'string' && allowed.has(value.objectId)) return { objectId: value.objectId };
  const out: AnyRecord = {};
  for (const key of Object.keys(value)) out[key] = maskAllowed(value[key], allowed, inElements || key === 'pageElements' || (inElements && key === 'children'));
  return out;
}
function outsideDigest(snapshot: DeckSnapshot, allowed: Set<string>) {
  return digest(maskAllowed(snapshot, allowed), { ignoreImageContentUrl: true });
}
/** Ensure no page element or deck metadata outside the explicit allowlist changed. */
export function assertUnchangedOutside(before: DeckSnapshot, after: DeckSnapshot, allowedObjectIds: string[]): void {
  const allowed = new Set<string>(allowedObjectIds);
  if (allowed.size !== allowedObjectIds.length) fail('The object allowlist contains duplicate IDs.');
  elementsById(before); elementsById(after);
  if (outsideDigest(before, allowed) !== outsideDigest(after, allowed)) fail('Readback changed an object, slide order, logo/crop, note, or other data outside the explicit allowlist.');
}

function stripTransform(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(stripTransform);
  if (!isRecord(value)) return value;
  const out: AnyRecord = {};
  for (const key of Object.keys(value)) if (key !== 'transform') out[key] = stripTransform(value[key]);
  return out;
}
function stripImageUrls(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(stripImageUrls);
  if (!isRecord(value)) return value;
  const out: AnyRecord = {};
  for (const key of Object.keys(value)) {
    if (key === 'contentUrl' || key === 'sourceUrl') continue;
    out[key] = stripImageUrls(value[key]);
  }
  return out;
}
function cloneForImageCheck(element:ElementSnapshot):AnyRecord {
  const value=stripImageUrls(element) as AnyRecord;
  return {...value,size:undefined,transform:undefined,image:{...value.image,imageProperties:{...value.image?.imageProperties,cropProperties:undefined}}};
}
function textContent(element: ElementSnapshot): string | undefined {
  const shape = element.shape;
  if (!isRecord(shape) || shape.shapeType !== 'TEXT_BOX') return undefined;
  if (typeof shape.text === 'string') return shape.text;
  const runs = isRecord(shape.text) && Array.isArray(shape.text.textElements) ? shape.text.textElements : [];
  return runs.map((run: any) => run?.textRun?.content || '').join('');
}
function textFontSizes(element: ElementSnapshot): number[] {
  const shape = element.shape;
  if (!isRecord(shape) || !isRecord(shape.text) || !Array.isArray(shape.text.textElements)) return [];
  return shape.text.textElements.flatMap((part: any) => {
    const magnitude = part?.textRun?.style?.fontSize?.magnitude;
    return finite(magnitude) ? [magnitude] : [];
  });
}
function compareExceptTransform(before: ElementSnapshot, after: ElementSnapshot, ignoreImageUrls = false) {
  const b = ignoreImageUrls ? stripImageUrls(stripTransform(before)) : stripTransform(before);
  const a = ignoreImageUrls ? stripImageUrls(stripTransform(after)) : stripTransform(after);
  return JSON.stringify(canonicalValue(b, [], { ignoreImageContentUrl: true })) === JSON.stringify(canonicalValue(a, [], { ignoreImageContentUrl: true }));
}
function verifyTransform(expected: AnyRecord, actual: ElementSnapshot, id: string) {
  const geometry = nativeGeometry(actual), transform = actual.transform as AnyRecord;
  for (const key of ['scaleX', 'scaleY', 'translateX', 'translateY']) if (!close(transform[key]??0, expected[key])) fail(`Readback transform for ${id} does not match the planned affine move.`);
  if (!close(geometry.shearX, 0) || !close(geometry.shearY, 0)) fail(`Readback transform for ${id} contains rotation/skew.`);
}

/** Verify native readback, including operation-specific target changes and a visual-review hold for images. */
export function verifyPatchResult(before: DeckSnapshot, after: DeckSnapshot, plan: PatchPlan): { requiresVisualReview: boolean } {
  validatePlanEnvelope(plan);
  if (snapshotHash(before) !== plan.baseHash) fail('Readback verification used a baseline different from the plan.');
  assertOperationTargets(before, plan.operations, plan.allowedObjectIds);
  assertUnchangedOutside(before, after, plan.allowedObjectIds);
  const beforeMap = elementsById(before), afterMap = elementsById(after);
  let requiresVisualReview = false;
  for (const operation of plan.operations) {
    const oldElement = requireElement(beforeMap, operation.objectId, operation.kind), newElement = requireElement(afterMap, operation.objectId, operation.kind);
    if (operation.kind === 'text') {
      const returnedText = textContent(newElement);
      const textMatches = returnedText === operation.text || returnedText === `${operation.text}\n`;
      if (elementKind(newElement) !== 'text' || !textMatches) fail(`Readback text for ${operation.objectId} does not match the requested replacement.`);
      if (operation.fontSize !== undefined) {
        const sizes = textFontSizes(newElement);
        if (sizes.length > 0 && sizes.some(size => !close(size, operation.fontSize!))) fail(`Readback font size for ${operation.objectId} does not match the request.`);
      }
      const oldCopy = { ...oldElement, shape: { ...(oldElement.shape as AnyRecord), text: undefined } };
      const newCopy = { ...newElement, shape: { ...(newElement.shape as AnyRecord), text: undefined } };
      if (digest(oldCopy,{ignoreImageContentUrl:true})!==digest(newCopy,{ignoreImageContentUrl:true})) fail(`Readback changed non-text properties of ${operation.objectId}.`);
    } else if (operation.kind === 'move') {
      const oldGeometry = nativeGeometry(oldElement), requested = validBounds(operation.bounds, `move ${operation.objectId}.bounds`);
      if (!compareExceptTransform(oldElement, newElement)) fail(`Readback changed non-transform properties of moved object ${operation.objectId}.`);
      verifyTransform(targetTransform(oldGeometry, requested), newElement, operation.objectId);
      for (const markId of operation.attachedMarks || []) {
        const oldMark = requireElement(beforeMap, markId, 'attached mark'), newMark = requireElement(afterMap, markId, 'attached mark');
        if (!compareExceptTransform(oldMark, newMark)) fail(`Readback changed non-transform properties of attached mark ${markId}.`);
        verifyTransform(affineForMark(oldGeometry, nativeGeometry(oldMark), requested), newMark, markId);
      }
    } else if (operation.kind === 'replace-image') {
      if (elementKind(newElement) !== 'image') fail(`Readback image target ${operation.objectId} is no longer an image.`);
      // CENTER_CROP intentionally recomputes crop and native intrinsic size for the new
      // source. The displayed frame and all other image properties must stay unchanged.
      const oldBounds=boundsOf(nativeGeometry(oldElement)),newBounds=boundsOf(nativeGeometry(newElement));
      for(const key of ['x','y','w','h'] as const)if(!close(oldBounds[key],newBounds[key]))fail(`Readback changed the displayed image frame of ${operation.objectId}.`);
      const stableImage=(e:ElementSnapshot)=>{const value=cloneForImageCheck(e);return digest(value,{ignoreImageContentUrl:true});};
      if(stableImage(oldElement)!==stableImage(newElement))fail(`Readback changed non-source image styling of ${operation.objectId}.`);
      const image = newElement.image as AnyRecord;
      if (own(image, 'sourceUrl') && image.sourceUrl !== operation.url) fail(`Readback sourceUrl for ${operation.objectId} does not match the exact requested URL.`);
      requiresVisualReview = true;
    }
  }
  return { requiresVisualReview };
}
