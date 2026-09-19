import {describe,test,expect} from 'bun:test';
import {readFile,writeFile,symlink} from 'node:fs/promises';
import {join} from 'node:path';
import {collectRenderReview} from '../src/render-review';
import {verifyRenderFiles} from '../src/artifact-files';
import {clone,compileFixture,nativeSnapshot,v2Projects,tempDir,writeActualPdf} from './v2-fixtures';

describe('V2 PDF integrity and held render review',()=>{
 test('actual text-bearing PDF and full/phone files are bound by hashes, not labeled inspected',async()=>{
  const p=(await v2Projects()).sort((a,b)=>a.slides.length-b.slides.length)[0];const c=compileFixture(p),s=nativeSnapshot(c),root=await tempDir('render');
  const pdf=join(root,'input.pdf');await writeActualPdf(c,pdf);
  const out=join(root,'review'),bundle=await collectRenderReview(p,c,s,pdf,out);
  expect(bundle.pageCount).toBe(p.slides.length);expect(bundle.inspected).toBe(false);expect(bundle.externalRelease).toBe('held');expect(bundle.holds).toEqual([]);
  expect(await verifyRenderFiles(bundle,out)).toEqual([]);
  await writeFile(join(out,bundle.pages[0].phone.path),'changed bytes');expect((await verifyRenderFiles(bundle,out)).length).toBeGreaterThan(0);
 });
 test('stale input, mismatched native text, unsafe paths and symlink escape fail closed',async()=>{
  const p=(await v2Projects()).sort((a,b)=>a.slides.length-b.slides.length)[0];const c=compileFixture(p),root=await tempDir('negative-render');const pdf=join(root,'input.pdf');await writeActualPdf(c,pdf);
  const stale=clone(p);stale.meta.revision='changed';await expect(collectRenderReview(stale,c,nativeSnapshot(c),pdf,join(root,'stale'))).rejects.toThrow('stale');
  const native=nativeSnapshot(c);native.slides[0].pageElements.find(e=>e.shape?.text?.textElements?.length)!.shape.text.textElements[0].textRun.content='unexpected';
  await expect(collectRenderReview(p,c,native,pdf,join(root,'wrong-native'))).rejects.toThrow('text mismatch');
  const out=join(root,'good'),bundle=await collectRenderReview(p,c,nativeSnapshot(c),pdf,out);
  const unsafe=clone(bundle);unsafe.pages[0].full.path='../input.pdf';expect((await verifyRenderFiles(unsafe,out)).some(s=>s.includes('unsafe'))).toBe(true);
  await symlink(pdf,join(out,'escaped.pdf'));const escaped=clone(bundle);escaped.pdf.path='escaped.pdf';expect((await verifyRenderFiles(escaped,out)).some(s=>s.includes('escapes'))).toBe(true);
 });
});
