import { describe, expect, test } from 'bun:test';
import type { Binding, DeckSnapshot, ElementSnapshot } from '../src/types';
import { assertUnchangedOutside, elementsById, makePatchPlan, patchRequests, RevisionSafetyError, snapshotHash, verifyPatchPlan, verifyPatchResult } from '../src/revisions';

const emu = (magnitude: number) => ({ magnitude, unit: 'EMU' });
const transform = (translateX = 0, translateY = 0, scaleX = 1, scaleY = 1) => ({ scaleX, scaleY, shearX: 0, shearY: 0, translateX, translateY, unit: 'EMU' });
const text = (objectId: string, content = 'old'): ElementSnapshot => ({ objectId, size: { width: emu(100), height: emu(50) }, transform: transform(), shape: { shapeType: 'TEXT_BOX', text: content } });
const image = (objectId: string, x = 0, y = 0): ElementSnapshot => ({ objectId, size: { width: emu(100), height: emu(50) }, transform: transform(x, y), image: { sourceUrl: 'https://example.invalid/old.png', contentUrl: 'https://volatile.invalid/old', imageProperties: { cropProperties: { leftOffset: .1 } } } });
const baseSnapshot = (): DeckSnapshot => ({ presentationId: 'deck_fixture', title: 'Neutral Fixture Deck', revisionId: 'volatile_a', slides: [{ objectId: 'slide_a', pageElements: [text('text_a'), image('image_a', 10, 20), image('logo_a', 30, 40)] }] });
const binding = (lastApplied?: Binding['lastApplied']): Binding => ({ schemaVersion: '1.0.0', projectId: 'project_fixture', presentationId: 'deck_fixture', expectedTitle: 'Neutral Fixture Deck', protectedPresentationIds: ['locked_deck'], ...(lastApplied ? { lastApplied } : {}) });
const planFor = (snapshot: DeckSnapshot, extra: any = {}) => makePatchPlan(binding(), snapshot, { revision: 'rev_1', operations: [{ kind: 'text', objectId: 'text_a', text: 'new' }], allowedObjectIds: ['text_a'], ...extra });

function clone<T>(value: T): T { return structuredClone(value); }

describe('partner-neutral revision safety', () => {
  test('hash ignores only documented volatile values and elementsById includes nested children', () => {
    const a = baseSnapshot();
    const b = clone(a); b.revisionId = 'volatile_b'; (b.slides[0].pageElements[1] as any).image.contentUrl = 'https://volatile.invalid/new'; (b as any).notesPage = { thumbnail: 'thumb_b', body: 'same' }; (a as any).notesPage = { thumbnail: 'thumb_a', body: 'same' };
    expect(snapshotHash(a)).toBe(snapshotHash(b));
    const group: any = { objectId: 'group_a', elementGroup: { children: [text('child_a')] } }; (a.slides[0].pageElements as any[]).push(group);
    expect(elementsById(a).has('child_a')).toBe(true);
    (a.slides[0].pageElements as any[]).push(text('child_a'));
    expect(() => elementsById(a)).toThrow(/Duplicate native object ID/);
  });

  test('rejects protected decks, wrong decks, and non-text targets', () => {
    const s = baseSnapshot();
    expect(() => makePatchPlan({ ...binding(), presentationId: 'locked_deck' }, s, { revision: 'r', operations: [{ kind: 'text', objectId: 'text_a', text: 'x' }], allowedObjectIds: ['text_a'] })).toThrow(RevisionSafetyError);
    expect(() => makePatchPlan(binding(), { ...s, presentationId: 'other_deck' }, { revision: 'r', operations: [{ kind: 'text', objectId: 'text_a', text: 'x' }], allowedObjectIds: ['text_a'] })).toThrow(/presentationId/);
    expect(() => makePatchPlan(binding(), s, { revision: 'r', operations: [{ kind: 'text', objectId: 'image_a', text: 'x' }], allowedObjectIds: ['image_a'] })).toThrow(/not a native text box/);
  });

  test('moves an axis-aligned object and attached mark with the same affine transformation', () => {
    const s = baseSnapshot();
    (s.slides[0].pageElements as any[]).push({ objectId: 'mark_a', size: { width: emu(20), height: emu(10) }, transform: transform(15, 25, 1, 1), shape: { shapeType: 'RECTANGLE' } });
    const plan = makePatchPlan(binding(), s, { revision: 'move_1', operations: [{ kind: 'move', objectId: 'image_a', bounds: { x: 110, y: 120, w: 200, h: 100 }, attachedMarks: ['mark_a'] }], allowedObjectIds: ['image_a', 'mark_a'] });
    const requests = patchRequests(plan, s);
    expect(requests).toHaveLength(2);
    expect((requests[0] as any).updatePageElementTransform.transform).toMatchObject({ translateX: 110, translateY: 120, scaleX: 2, scaleY: 2, unit: 'EMU' });
    expect((requests[1] as any).updatePageElementTransform.transform).toMatchObject({ translateX: 120, translateY: 130, scaleX: 2, scaleY: 2, unit: 'EMU' });
    const after = clone(s); const map = elementsById(after); (map.get('image_a')!.transform as any) = transform(110, 120, 2, 2); (map.get('mark_a')!.transform as any) = transform(120, 130, 2, 2);
    expect(verifyPatchResult(s, after, plan).requiresVisualReview).toBe(false);
  });

  test('rejects group, rotation, malformed units, and aspect changes by default', () => {
    const s = baseSnapshot();
    (s.slides[0].pageElements as any[]).push({ objectId: 'group_a', elementGroup: { children: [] }, size: { width: emu(10), height: emu(10) }, transform: transform() });
    expect(() => makePatchPlan(binding(), s, { revision: 'r', operations: [{ kind: 'move', objectId: 'group_a', bounds: { x: 0, y: 0, w: 10, h: 10 } }], allowedObjectIds: ['group_a'] })).toThrow(/Grouped/);
    const rotated = clone(s); (elementsById(rotated).get('image_a')!.transform as any).shearX = .2;
    expect(() => makePatchPlan(binding(), rotated, { revision: 'r', operations: [{ kind: 'move', objectId: 'image_a', bounds: { x: 0, y: 0, w: 100, h: 50 } }], allowedObjectIds: ['image_a'] })).toThrow(/rotation\/skew/);
    expect(() => makePatchPlan(binding(), s, { revision: 'r', operations: [{ kind: 'move', objectId: 'image_a', bounds: { x: 0, y: 0, w: 100, h: 40 } }], allowedObjectIds: ['image_a'] })).toThrow(/aspect ratio/);
    const badUnits = clone(s); (elementsById(badUnits).get('image_a')!.size!.width as any).unit = 'PT';
    expect(() => makePatchPlan(binding(), badUnits, { revision: 'r', operations: [{ kind: 'move', objectId: 'image_a', bounds: { x: 0, y: 0, w: 100, h: 50 } }], allowedObjectIds: ['image_a'] })).toThrow(/EMU/);
  });

  test('handles replacement URL policy, preserves the frame, and requires review of the new native crop', () => {
    const s = baseSnapshot();
    expect(() => makePatchPlan(binding(), s, { revision: 'r', operations: [{ kind: 'replace-image', objectId: 'image_a', assetId: 'asset_a', url: 'http://example.invalid/new.png' }], allowedObjectIds: ['image_a'] })).toThrow(/HTTPS/);
    expect(() => makePatchPlan(binding(), s, { revision: 'r', operations: [{ kind: 'replace-image', objectId: 'image_a', assetId: 'asset_a', url: 'https://example.invalid/new.png', crop: { left: 0, top: 0, right: 1, bottom: 1 } }], allowedObjectIds: ['image_a'] })).toThrow(/crop is unsupported/);
    const plan = makePatchPlan(binding(), s, { revision: 'r', operations: [{ kind: 'replace-image', objectId: 'image_a', assetId: 'asset_a', url: 'https://example.invalid/new.png' }], allowedObjectIds: ['image_a'] });
    expect(patchRequests(plan, s)[0]).toEqual({ replaceImage: { imageObjectId: 'image_a', url: 'https://example.invalid/new.png', imageReplaceMethod: 'CENTER_CROP' } });
    const after = clone(s); const newImage = elementsById(after).get('image_a')!.image as any; newImage.sourceUrl = 'https://example.invalid/new.png'; newImage.contentUrl = 'https://volatile.invalid/new';
    expect(verifyPatchResult(s, after, plan).requiresVisualReview).toBe(true);
    // Native CENTER_CROP changes crop metadata and may change intrinsic size.
    // The displayed frame remains fixed; this must be visually reviewed, not rejected.
    newImage.imageProperties.cropProperties.leftOffset = .2;
    const replaced = elementsById(after).get('image_a')!;
    replaced.size = { width: emu(200), height: emu(100) };
    replaced.transform = transform(10, 20, .5, .5);
    expect(verifyPatchResult(s, after, plan).requiresVisualReview).toBe(true);
    const moved = clone(after); (elementsById(moved).get('image_a')!.transform as any).translateX = 12;
    expect(() => verifyPatchResult(s, moved, plan)).toThrow(/displayed image frame/);
    const styled = clone(after); (elementsById(styled).get('image_a')!.image as any).imageProperties.transparency = .5;
    expect(() => verifyPatchResult(s, styled, plan)).toThrow(/non-source image styling/);
    const wrongSource = clone(after); (elementsById(wrongSource).get('image_a')!.image as any).sourceUrl = 'https://example.invalid/wrong.png';
    expect(() => verifyPatchResult(s, wrongSource, plan)).toThrow(/sourceUrl/);
  });

  test('detects logo, crop, notes, ordering, and out-of-scope changes', () => {
    const s = baseSnapshot(); const plan = planFor(s); const after = clone(s); (elementsById(after).get('logo_a')!.image as any).imageProperties.cropProperties.leftOffset = .3;
    expect(() => verifyPatchResult(s, after, plan)).toThrow(/outside/);
    const reordered = clone(s); reordered.slides[0].pageElements.reverse(); expect(() => assertUnchangedOutside(s, reordered, ['text_a'])).toThrow(/outside/);
    const noted = clone(s); (noted as any).notesPage = { body: 'changed', thumbnail: 'new' }; expect(() => assertUnchangedOutside(s, noted, ['text_a'])).toThrow(/outside/);
  });

  test('supports idempotent no-op, rejects tampering and same-revision alternate plans', () => {
    const s = baseSnapshot(); const plan = planFor(s); const after = clone(s); (elementsById(after).get('text_a')!.shape as any).text = 'new';
    const recorded = binding({ revision: plan.revision, planHash: plan.planHash, afterHash: snapshotHash(after) });
    expect(verifyPatchPlan(recorded, after, plan).status).toBe('no-op');
    const tampered = { ...plan, operations: [{ kind: 'text', objectId: 'text_a', text: 'tampered' }] as any };
    expect(() => verifyPatchPlan(binding(), s, tampered)).toThrow(/hash/);
    expect(() => verifyPatchPlan(recorded, after, { ...plan, operations: [{ kind: 'text', objectId: 'text_a', text: 'other' }] as any })).toThrow(/hash/);
    expect(() => makePatchPlan(recorded, after, { revision: plan.revision, operations: [{ kind: 'text', objectId: 'text_a', text: 'other' }], allowedObjectIds: ['text_a'] })).toThrow(/different plan/);
  });

  test('rejects a concurrent changed baseline instead of claiming a race-free preflight', () => {
    const s = baseSnapshot(); const plan = planFor(s); const concurrent = clone(s); (elementsById(concurrent).get('logo_a')!.image as any).imageProperties.cropProperties.leftOffset = .8;
    expect(() => verifyPatchPlan(binding(), concurrent, plan)).toThrow(/baseline changed/);
  });
});
