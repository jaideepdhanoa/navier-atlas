import { describe, expect, test } from 'bun:test';
import { readFile, rm } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';
import type { Binding, CompiledDeck, DeckSnapshot, ElementSnapshot, Project, ReviewReceipt, SlidesRequest } from '../src/types';
import { createStaging, promoteRevision, stageRevision, type NativePort } from '../src/lifecycle';
import { compileProject } from '../src/render';
import { EMU, sha256 } from '../src/primitives';
import { elementsById, makePatchPlan, snapshotHash } from '../src/revisions';

const root = resolve(dirname(import.meta.path), '..');
const fixturePath = join(root, 'examples/public-demo/project.json');
const fixtureRoot = dirname(fixturePath);
const emu = (magnitude: number) => ({ magnitude, unit: 'EMU' as const });
const nativeTransform = (translateX = 0, translateY = 0, scaleX = 1, scaleY = 1) => ({ scaleX, scaleY, shearX: 0, shearY: 0, translateX, translateY, unit: 'EMU' as const });
const pageSize = { width: emu(720 * EMU), height: emu(405 * EMU) };

function clone<T>(value: T): T { return structuredClone(value); }
function textRuns(value: string) { return { textElements: [{ textRun: { content: value } }] }; }
function textElement(objectId: string, value = ''): ElementSnapshot {
  return { objectId, size: { width: emu(100), height: emu(40) }, transform: nativeTransform(), shape: { shapeType: 'TEXT_BOX', text: textRuns(value) } };
}
function findElement(snapshot: DeckSnapshot, objectId: string): ElementSnapshot {
  const element = elementsById(snapshot).get(objectId);
  if (!element) throw new Error(`missing fake native object ${objectId}`);
  return element;
}
function allElements(snapshot: DeckSnapshot): ElementSnapshot[] {
  const out: ElementSnapshot[] = [];
  for (const slide of snapshot.slides) out.push(...(slide.pageElements || []));
  return out;
}

/** A deliberately small native adapter: requests mutate realistic snapshots, while duplicate preserves slide/object IDs. */
class FakeNativePort implements NativePort {
  conditionalRevisions = true;
  presentations = new Map<string, DeckSnapshot>();
  creates = 0;
  duplicates = 0;
  batches = 0;
  nextId = 1;
  failCreateAfterSideEffect = false;
  defaultTitleSlide = false;
  defaultTitleText = '';
  failBackupAfterSideEffect = false;
  failBatchNumber?: number;
  alterDuplicateNumber?: number;
  alterObjectId?: string;
  mutateSourceOnSnapshotNumber?: number;
  private snapshots = 0;
  private failedBatch = false;

  private newId(prefix: string) { return `${prefix}_${this.nextId++}`; }
  private nativeNotes(slideId: string) {
    const noteId = `note_${slideId}`;
    return {
      notesProperties: { speakerNotesObjectId: noteId },
      pageElements: [textElement(noteId, '')],
    };
  }
  private emptyPresentation(id: string, title: string): DeckSnapshot {
    return { presentationId: id, title, pageSize: clone(pageSize), revisionId: 'r0', slides: [] };
  }
  async snapshot(id: string): Promise<DeckSnapshot & { revisionId?: string }> {
    this.snapshots++;
    const value = this.presentations.get(id);
    if (!value) throw new Error(`unknown fake presentation ${id}`);
    if (this.mutateSourceOnSnapshotNumber === this.snapshots) {
      const first = value.slides[0]?.pageElements?.[0];
      if (first?.shape?.text) first.shape.text = textRuns('concurrent source edit');
    }
    return clone(value) as DeckSnapshot & { revisionId?: string };
  }
  async create(title: string) {
    this.creates++;
    const presentationId = this.newId('deck');
    const empty = this.emptyPresentation(presentationId, title);
    if (this.defaultTitleSlide) empty.slides.push({objectId:'default-page',index:0,pageElements:[{...textElement('default-title',this.defaultTitleText),shape:{shapeType:'TEXT_BOX',text:textRuns(this.defaultTitleText),placeholder:{type:'CENTERED_TITLE'}}},{...textElement('default-subtitle'),shape:{shapeType:'TEXT_BOX',placeholder:{type:'SUBTITLE'}}}],slideProperties:{notesPage:this.nativeNotes('default-page')},pageProperties:{pageBackgroundFill:{propertyState:'INHERIT'}}});
    this.presentations.set(presentationId, empty);
    if (this.failCreateAfterSideEffect) {
      this.failCreateAfterSideEffect = false;
      throw new Error('simulated timeout after native create');
    }
    return { presentationId, url: `https://native.invalid/${presentationId}` };
  }
  async duplicate(id: string, title: string) {
    this.duplicates++;
    const source = this.presentations.get(id);
    if (!source) throw new Error(`unknown fake source ${id}`);
    const presentationId = this.newId('copy');
    const copy = clone(source);
    copy.presentationId = presentationId;
    copy.title = title;
    copy.revisionId = 'r0';
    this.presentations.set(presentationId, copy);
    if (this.alterDuplicateNumber === this.duplicates) {
      const first = this.alterObjectId ? this.locate(copy, this.alterObjectId) : copy.slides[0]?.pageElements?.[0];
      if (first?.shape?.text) first.shape.text = textRuns('altered review copy');
    }
    if (this.failBackupAfterSideEffect && this.duplicates === 1) throw new Error('simulated timeout after backup duplicate');
    return { presentationId, url: `https://native.invalid/${presentationId}` };
  }
  private pageFor(snapshot: DeckSnapshot, pageObjectId: string) {
    const page = snapshot.slides.find(s => s.objectId === pageObjectId);
    if (!page) throw new Error(`unknown fake page ${pageObjectId}`);
    return page;
  }
  private locate(snapshot: DeckSnapshot, objectId: string): ElementSnapshot {
    try { return findElement(snapshot, objectId); }
    catch {
      for (const slide of snapshot.slides) {
        const note = slide.slideProperties?.notesPage?.pageElements?.find((e: ElementSnapshot) => e.objectId === objectId);
        if (note) return note;
      }
      throw new Error(`missing fake native object ${objectId}`);
    }
  }
  private replaceImage(page: any, placeholderId: string, url: string, mode: string) {
    const index = page.pageElements.findIndex((e: any) => e.objectId === placeholderId);
    if (index < 0) throw new Error(`unknown placeholder ${placeholderId}`);
    const placeholder = page.pageElements[index];
    const imageId = this.newId('native-image');
    page.pageElements[index] = {
      objectId: imageId,
      size: clone(placeholder.size),
      transform: clone(placeholder.transform),
      image: { sourceUrl: url, contentUrl: `https://volatile.invalid/${imageId}`, imageProperties: { imageReplaceMethod: mode } },
    };
    // The real service omits numeric zero translations in native responses.
    if(page.pageElements[index].transform.translateX===0)delete page.pageElements[index].transform.translateX;
    if(page.pageElements[index].transform.translateY===0)delete page.pageElements[index].transform.translateY;
  }
  async batch(id: string, requests: SlidesRequest[], requiredRevision?: string) {
    const deck = this.presentations.get(id);
    if (!deck) throw new Error(`unknown fake presentation ${id}`);
    if (requiredRevision && requiredRevision !== deck.revisionId) throw new Error('fake revision mismatch');
    this.batches++;
    if (this.failBatchNumber === this.batches && !this.failedBatch) {
      this.failedBatch = true;
      throw new Error('simulated batch failure before native side effect');
    }
    for (const request of requests) {
      const [operation, body] = Object.entries(request)[0];
      if (operation === 'deleteObject') {
        const i=deck.slides.findIndex(s=>s.objectId===body.objectId);
        if(i<0)throw new Error('fake delete target is not a slide');
        deck.slides.splice(i,1);
      } else if (operation === 'createSlide') {
        const slideId = body.objectId;
        deck.slides.push({ objectId: slideId, index: deck.slides.length, pageElements: [], slideProperties: { notesPage: this.nativeNotes(slideId) } });
      } else if (operation === 'createShape') {
        const page = this.pageFor(deck, body.elementProperties.pageObjectId);
        page.pageElements.push({ objectId: body.objectId, size: clone(body.elementProperties.size), transform: clone(body.elementProperties.transform), shape: { shapeType: body.shapeType, text: textRuns('') } });
      } else if (operation === 'createLine') {
        const page = this.pageFor(deck, body.elementProperties.pageObjectId);
        page.pageElements.push({ objectId: body.objectId, size: clone(body.elementProperties.size), transform: clone(body.elementProperties.transform), line: { lineCategory: body.lineCategory } });
      } else if (operation === 'insertText') {
        const element = this.locate(deck, body.objectId);
        if (!element.shape) throw new Error('fake insert target is not a shape');
        element.shape.text = textRuns(body.text);
      } else if (operation === 'deleteText') {
        const element = this.locate(deck, body.objectId);
        if (!element.shape) throw new Error('fake delete target is not a shape');
        if(!(element.shape.text?.textElements??[]).some((e:any)=>e.textRun?.content?.length))throw new Error('The startIndex 0 must be less than the endIndex 0');
        element.shape.text = textRuns('');
      } else if (operation === 'updateTextStyle') {
        const element = this.locate(deck, body.objectId);
        const parts = element.shape?.text?.textElements || [];
        for (const part of parts) if (part.textRun) part.textRun.style = clone(body.style);
      } else if (operation === 'updatePageElementTransform') {
        const element = this.locate(deck, body.objectId);
        element.transform = clone(body.transform);
      } else if (operation === 'replaceAllShapesWithImage') {
        const tag = body.containsText.text;
        for (const page of deck.slides) {
          const placeholder = page.pageElements.find((e: any) => e.shape?.text?.textElements?.some((part: any) => part.textRun?.content === tag));
          if (placeholder) { this.replaceImage(page, placeholder.objectId, body.imageUrl, body.imageReplaceMethod); break; }
        }
      } else if (operation === 'replaceImage') {
        const element = this.locate(deck, body.imageObjectId);
        if (!element.image) throw new Error('fake replace target is not an image');
        element.image.sourceUrl = body.url;
      } else if (operation === 'updateImageProperties') {
        const element=this.locate(deck,body.objectId);element.image.imageProperties={...element.image.imageProperties,...clone(body.imageProperties)};
      } else if (operation === 'updatePageProperties' || operation === 'updateShapeProperties' || operation === 'updateParagraphStyle' || operation === 'updateLineProperties') {
        // Styling does not affect lifecycle safety assertions in this adapter.
      } else throw new Error(`fake adapter does not implement ${operation}`);
    }
    deck.revisionId = `r${this.batches}`;
    deck.slides.forEach((slide, index) => { slide.index = index; });
    return {};
  }
  async exportPDF(id: string, path: string) { return { presentationId: id, path, status: 'exported' }; }
}

const sourceProject = JSON.parse(await readFile(fixturePath, 'utf8')) as Project;
function makeProject(_slideCount = 2): Project {
  // Lifecycle validates the complete project contract, including canonical cover→close order.
  // Keep the fixture's seven-slide sequence intact; tests can still inject failures by batch number.
  const project = clone(sourceProject);
  project.meta.audience = 'internal';
  return project;
}
function compile(project: Project): CompiledDeck {
  const urls = Object.fromEntries(project.assets.map(a => [a.id, `https://assets.invalid/${a.id}.svg`]));
  return compileProject(project, { assetUrls: urls });
}
function review(stage: ReviewReceipt['stage'], subjectHash: string): ReviewReceipt {
  return { stage, subjectHash, reviewer: 'test reviewer', reviewedAt: '2026-09-18T20:00:00Z', decision: 'approved', notes: 'simulated approval' };
}
async function stagingOptions(project: Project, compiled: CompiledDeck, out: string) {
  return { root: fixtureRoot, out, storyboard: review('storyboard', compiled.inputHash), verifiedAssetHashes: Object.fromEntries(project.assets.map(a => [a.id, a.sha256])) };
}


describe('lifecycle native staging and revision protocol', () => {
  test('initializes only an explicitly opted-in pristine provider title slide', async () => {
    const project=makeProject(),compiled=compile(project),port=new FakeNativePort();port.defaultTitleSlide=true;
    const out=`/tmp/lifecycle-bootstrap-${Date.now()}`;
    const opts={...await stagingOptions(project,compiled,out),allowPristineTitleSlide:true};
    const receipt=await createStaging(project,compiled,port,opts);
    expect(receipt.bootstrap?.removed).toBe(true);
    expect(receipt.bootstrap?.slideId).toBe('default-page');
    expect(JSON.parse(await readFile(join(out,'bootstrap-before.json'),'utf8')).slides[0].objectId).toBe('default-page');
    expect((await port.snapshot(receipt.presentationId!)).slides).toHaveLength(compiled.slides.length);
    await rm(out,{recursive:true,force:true});
  });
  test('never removes a nonempty title slide or an unapproved default page', async () => {
    const project=makeProject(),compiled=compile(project);
    for(const optIn of [false,true]){
      const port=new FakeNativePort();port.defaultTitleSlide=true;port.defaultTitleText=optIn?'human draft':'';
      const out=`/tmp/lifecycle-bootstrap-hold-${Date.now()}-${optIn}`;
      await expect(createStaging(project,compiled,port,{...await stagingOptions(project,compiled,out),allowPristineTitleSlide:optIn})).rejects.toThrow('Unexpected slide');
      expect(port.batches).toBe(0);
      await rm(out,{recursive:true,force:true});
    }
  });
  test('stages text, notes, page size, and rebinding of generated native images by URL and frame center', async () => {
    const project = makeProject(2); const compiled = compile(project); const port = new FakeNativePort();
    const out = `/tmp/lifecycle-image-rebind-${Date.now()}`;
    const receipt = await createStaging(project, compiled, port, await stagingOptions(project, compiled, out));
    expect(receipt.status).toBe('complete');
    const staged = await port.snapshot(receipt.presentationId!);
    expect(staged.pageSize).toEqual(pageSize);
    expect(staged.slides).toHaveLength(compiled.slides.length);
    expect(receipt.notesApplied).toBe(true);
    expect(receipt.roleMap).toHaveLength(compiled.slides.flatMap(s => s.elements).length);
    expect(receipt.roleMap!.filter(r => r.kind === 'image')).toHaveLength(compiled.assetUses.length);
    for (const role of receipt.roleMap!.filter(r => r.kind === 'image')) {
      const original = compiled.slides.flatMap(s => s.elements).find(e => e.objectId === role.objectId);
      // Every image role now points at a minted native image ID, not its placeholder ID.
      expect(original).toBeUndefined();
      const native = findElement(staged, role.objectId);
      const use = compiled.assetUses.find(u => u.assetId === role.assetId && u.slideKey === role.slideKey && u.role === role.role)!;
      const sourceAsset = project.assets.find(a => a.id === use.assetId)!;
      expect(native.image?.sourceUrl).toBe(`https://assets.invalid/${sourceAsset.id}.svg`);
      const sourceSlide = compiled.slides.find(s => s.key === role.slideKey)!;
      const sourceBox = sourceSlide.boxes.find(b => b.objectId === use.objectId)!;
      const actualCenterX = (native.transform!.translateX ?? 0) / EMU + native.size!.width.magnitude / EMU * native.transform!.scaleX / 2;
      const actualCenterY = (native.transform!.translateY ?? 0) / EMU + native.size!.height.magnitude / EMU * native.transform!.scaleY / 2;
      expect(actualCenterX).toBeCloseTo(sourceBox.x + sourceBox.w / 2, 4);
      expect(actualCenterY).toBeCloseTo(sourceBox.y + sourceBox.h / 2, 4);
    }
    for (const slide of compiled.slides) {
      const native = staged.slides.find(s => s.objectId === slide.objectId)!;
      const noteId = native.slideProperties!.notesPage.notesProperties?.speakerNotesObjectId || native.slideProperties!.notesPage.speakerNotesObjectId;
      const actualNoteId = native.slideProperties!.notesPage.notesProperties.speakerNotesObjectId;
      const note = native.slideProperties!.notesPage.pageElements!.find((e: ElementSnapshot) => e.objectId === actualNoteId)!;
      const noteText = note.shape?.text?.textElements.map((e: any) => e.textRun?.content || '').join('').replace(/\n$/, '');
      expect(noteId).toBe(actualNoteId);
      expect(noteText).toBe(slide.notes);
    }
    await rm(out, { recursive: true, force: true });
  });

  test('resumes an interrupted create without overwriting or replaying completed slides, then is idempotent', async () => {
    const project = makeProject(2); const compiled = compile(project); const port = new FakeNativePort(); port.failBatchNumber = 2;
    const out = `/tmp/lifecycle-resume-${Date.now()}`;
    await expect(createStaging(project, compiled, port, await stagingOptions(project, compiled, out))).rejects.toThrow('simulated batch failure');
    expect(port.creates).toBe(1); const receipt = JSON.parse(await readFile(join(out, 'stage-receipt.json'), 'utf8'));
    expect(receipt.completedSlides).toEqual([compiled.slides[0].key]);
    const resumed = await createStaging(project, compiled, port, await stagingOptions(project, compiled, out));
    expect(resumed.status).toBe('complete'); expect(port.creates).toBe(1);
    const batchCount = port.batches; const again = await createStaging(project, compiled, port, await stagingOptions(project, compiled, out));
    expect(again.afterHash).toBe(resumed.afterHash); expect(port.creates).toBe(1); expect(port.batches).toBe(batchCount);
    const edited = await port.snapshot(resumed.presentationId!); const editable = edited.slides[0].pageElements.find((e: ElementSnapshot) => e.shape?.shapeType === 'TEXT_BOX')!;
    editable.shape!.text = textRuns('human edit after completion'); port.presentations.set(resumed.presentationId!, edited);
    await expect(createStaging(project, compiled, port, await stagingOptions(project, compiled, out))).rejects.toThrow('human edits');
    await rm(out, { recursive: true, force: true });
  });

  test('fails closed after uncertain create side effect instead of creating a duplicate', async () => {
    const project = makeProject(1); const compiled = compile(project); const port = new FakeNativePort(); port.failCreateAfterSideEffect = true;
    const out = `/tmp/lifecycle-uncertain-create-${Date.now()}`;
    await expect(createStaging(project, compiled, port, await stagingOptions(project, compiled, out))).rejects.toThrow('timeout after native create');
    await expect(createStaging(project, compiled, port, await stagingOptions(project, compiled, out))).rejects.toThrow('Uncertain prior create');
    expect(port.creates).toBe(1); await rm(out, { recursive: true, force: true });
  });

  test('stageRevision checks baseline and copy identity, preserves source, and rejects altered review copies', async () => {
    const project = makeProject(1); const compiled = compile(project); const sourcePort = new FakeNativePort();
    const sourceOut = `/tmp/lifecycle-stage-source-${Date.now()}`;
    const staged = await createStaging(project, compiled, sourcePort, await stagingOptions(project, compiled, sourceOut));
    const sourceId = staged.presentationId!; const source = await sourcePort.snapshot(sourceId);
    const sourceBinding: Binding = { schemaVersion: '1.0.0', projectId: project.meta.projectId, presentationId: sourceId, expectedTitle: staged.title, protectedPresentationIds: [], roleMap: staged.roleMap! };
    const textRole = sourceBinding.roleMap.find(r => r.kind === 'text')!;
    const plan = makePatchPlan(sourceBinding, source, { revision: 'r2', operations: [{ kind: 'text', objectId: textRole.objectId, text: 'reviewed replacement' }], allowedObjectIds: [textRole.objectId] });
    const reviewOut = `/tmp/lifecycle-stage-review-${Date.now()}`;
    const journal = await stageRevision(sourceBinding, plan, sourcePort, reviewOut);
    expect(journal.status).toBe('complete'); expect(journal.sourceUnchanged).toBe(true); expect(journal.productionPromotion).toBe('requires-reviewed-promotion');
    expect(snapshotHash(await sourcePort.snapshot(sourceId))).toBe(snapshotHash(source));
    const reviewDeck = await sourcePort.snapshot(journal.stageId); expect(findElement(reviewDeck, textRole.objectId).shape?.text?.textElements[0].textRun.content).toBe('reviewed replacement');
    findElement(reviewDeck, textRole.objectId).shape!.text = textRuns('human edit in review copy'); sourcePort.presentations.set(journal.stageId, reviewDeck);
    await expect(stageRevision(sourceBinding, plan, sourcePort, reviewOut)).rejects.toThrow('Review copy has changed');

    const alteredPort = new FakeNativePort();
    const alteredSourceOut = `/tmp/lifecycle-altered-source-${Date.now()}`;
    const alteredStaged = await createStaging(project, compiled, alteredPort, await stagingOptions(project, compiled, alteredSourceOut));
    const alteredSource = await alteredPort.snapshot(alteredStaged.presentationId!);
    const alteredBinding: Binding = { ...sourceBinding, presentationId: alteredStaged.presentationId!, roleMap: alteredStaged.roleMap! };
    const alteredRole = alteredBinding.roleMap.find(r => r.kind === 'text')!;
    const alteredPlan = makePatchPlan(alteredBinding, alteredSource, { revision: 'r3', operations: [{ kind: 'text', objectId: alteredRole.objectId, text: 'another replacement' }], allowedObjectIds: [alteredRole.objectId] });
    alteredPort.alterDuplicateNumber = 2; alteredPort.alterObjectId = alteredRole.objectId;
    await expect(stageRevision(alteredBinding, alteredPlan, alteredPort, `/tmp/lifecycle-altered-review-${Date.now()}`)).rejects.toThrow('Review copy differs');
    await rm(sourceOut, { recursive: true, force: true }); await rm(reviewOut, { recursive: true, force: true }); await rm(alteredSourceOut, { recursive: true, force: true });
  });

  test('rejects a stale source baseline and refuses uncertain backup duplicate replay', async () => {
    const project = makeProject(1); const compiled = compile(project); const port = new FakeNativePort();
    const sourceOut = `/tmp/lifecycle-baseline-${Date.now()}`; const staged = await createStaging(project, compiled, port, await stagingOptions(project, compiled, sourceOut));
    const sourceId = staged.presentationId!; const source = await port.snapshot(sourceId);
    const binding: Binding = { schemaVersion: '1.0.0', projectId: project.meta.projectId, presentationId: sourceId, expectedTitle: staged.title, protectedPresentationIds: [], roleMap: staged.roleMap! };
    const role = binding.roleMap.find(r => r.kind === 'text')!;
    const plan = makePatchPlan(binding, source, { revision: 'r4', operations: [{ kind: 'text', objectId: role.objectId, text: 'baseline replacement' }], allowedObjectIds: [role.objectId] });
    const changed = await port.snapshot(sourceId); findElement(changed, role.objectId).shape!.text = textRuns('concurrent edit'); port.presentations.set(sourceId, changed);
    await expect(stageRevision(binding, plan, port, `/tmp/lifecycle-stale-${Date.now()}`)).rejects.toThrow('baseline changed');

    const uncertain = new FakeNativePort(); const uncertainOut = `/tmp/lifecycle-uncertain-backup-${Date.now()}`;
    const uncertainStaged = await createStaging(project, compiled, uncertain, await stagingOptions(project, compiled, uncertainOut));
    const uncertainSource = await uncertain.snapshot(uncertainStaged.presentationId!); const uncertainBinding: Binding = { ...binding, presentationId: uncertainStaged.presentationId!, roleMap: uncertainStaged.roleMap! };
    const uncertainRole = uncertainBinding.roleMap.find(r => r.kind === 'text')!;
    const uncertainPlan = makePatchPlan(uncertainBinding, uncertainSource, { revision: 'r5', operations: [{ kind: 'text', objectId: uncertainRole.objectId, text: 'backup replacement' }], allowedObjectIds: [uncertainRole.objectId] });
    uncertain.failBackupAfterSideEffect = true;
    const uncertainReviewOut = `/tmp/lifecycle-uncertain-backup-review-${Date.now()}`;
    await expect(stageRevision(uncertainBinding, uncertainPlan, uncertain, uncertainReviewOut)).rejects.toThrow('timeout after backup duplicate');
    await expect(stageRevision(uncertainBinding, uncertainPlan, uncertain, uncertainReviewOut)).rejects.toThrow('Prior staging attempt needs reconciliation');
    expect(uncertain.duplicates).toBe(1);
    await rm(sourceOut, { recursive: true, force: true }); await rm(uncertainOut, { recursive: true, force: true }); await rm(uncertainReviewOut, { recursive: true, force: true });
  });

  test('holds live promotion when native conditional revision support is unavailable', async () => {
    const port = new FakeNativePort(); port.conditionalRevisions = false;
    const binding: Binding = { schemaVersion: '1.0.0', projectId: 'project_fixture', presentationId: 'prod', expectedTitle: 'Production', protectedPresentationIds: [], roleMap: [] };
    const plan = { schemaVersion: '1.0.0', projectId: 'project_fixture', presentationId: 'prod', revision: 'r1', baseHash: '0'.repeat(64), operations: [], allowedObjectIds: [], planHash: '0'.repeat(64) } as any;
    await expect(promoteRevision(binding, plan, port, review('visual', plan.planHash))).rejects.toThrow('LIVE_PROMOTION_HELD');
    expect(port.creates).toBe(0); expect(port.duplicates).toBe(0); expect(port.batches).toBe(0);
  });
});
