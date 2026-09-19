import {readFile,writeFile,mkdir,stat} from 'node:fs/promises';
import {resolve} from 'node:path';
import type {Project,CompiledDeck,Binding,DeckSnapshot,ElementRole,PatchPlan,ReviewReceipt,SlidesRequest} from './types';
import {sha256,EMU} from './primitives';
import {assertValidProject} from './validate';
import {snapshotHash,elementsById,verifyPatchPlan,patchRequests,verifyPatchResult,makePatchPlan} from './revisions';

/** Inject an authenticated connection. This library itself contains no accounts, credentials or destination IDs. */
export interface NativePort {
  conditionalRevisions:boolean;
  snapshot(id:string):Promise<DeckSnapshot & {revisionId?:string}>;
  create(title:string):Promise<{presentationId:string;url?:string}>;
  duplicate(id:string,title:string):Promise<{presentationId:string;url?:string}>;
  batch(id:string,requests:SlidesRequest[],requiredRevision?:string):Promise<unknown>;
  exportPDF?(id:string,path:string):Promise<unknown>;
}
export interface StageReceipt {schemaVersion:'1.0.0';kind:'create-staging';projectId:string;inputHash:string;compiledHash:string;status:string;presentationId?:string;title:string;completedSlides:string[];afterHash?:string;notesApplied?:boolean;roleMap?:ElementRole[];url?:string;assetExceptions?:string[];bootstrap?:{slideId:string;beforeHash:string;removed?:boolean};}
const readJson=async(p:string)=>JSON.parse(await readFile(p,'utf8'));
const save=async(p:string,v:unknown)=>writeFile(p,JSON.stringify(v,null,2)+'\n');
async function exists(p:string){try{await stat(p);return true;}catch{return false;}}
export function validateCompiled(compiled:CompiledDeck){
  if(compiled.requests.some(r=>Object.keys(r).length!==1))throw new Error('Native requests require one operation per object.');
  if(compiled.warnings.some(w=>w.code==='UNRESOLVED_ASSET'||w.code==='OUT_OF_CANVAS'))throw new Error('Resolve assets and bounds before native staging.');
  for(const r of compiled.requests){const op=Object.keys(r)[0];if(['deleteObject','replaceAllText','updatePresentationProperties'].includes(op))throw new Error(`Create compiler cannot emit ${op}.`);const url=(r.createImage||r.replaceAllShapesWithImage)?.url||(r.replaceAllShapesWithImage)?.imageUrl;if(url&&(!url.startsWith('https://')||url.includes('example.invalid')))throw new Error('A native stage needs an exact verified HTTPS image URL.');}
}
const imageBounds=(e:any)=>{const unit=(u:string)=>u==='EMU'?EMU:u==='PT'?1:NaN;const t=e.transform??{},size=e.size??{};return{x:(t.translateX??0)/unit(t.unit),y:(t.translateY??0)/unit(t.unit),w:size.width?.magnitude/unit(size.width?.unit)*(t.scaleX??0),h:size.height?.magnitude/unit(size.height?.unit)*(t.scaleY??0)};};
/** Resolve generated native image IDs by slide + exact source URL + frame centre; never guess after an ambiguous match. */
export function bindRoles(compiled:CompiledDeck,after:DeckSnapshot):ElementRole[]{
  const map=elementsById(after),roles:ElementRole[]=[],used=new Set<string>();
  for(const s of compiled.slides){const page=after.slides.find(p=>p.objectId===s.objectId);if(!page)throw new Error(`Missing slide ${s.key}`);
    for(const role of s.elements){if(role.kind!=='image'){if(!map.has(role.objectId))throw new Error(`Missing editable object ${role.objectId}`);roles.push(role);continue;}
      const box=s.boxes.find(b=>b.objectId===role.objectId)!;const tag=`__SP_IMAGE_${role.objectId}__`;
      const req=s.requests.find(r=>r.replaceAllShapesWithImage?.containsText.text===tag)?.replaceAllShapesWithImage;
      const candidates=(page.pageElements??[]).filter((e:any)=>{if(!e.image||used.has(e.objectId))return false;if(e.image.sourceUrl&&e.image.sourceUrl!==req?.imageUrl)return false;const b=imageBounds(e);return Math.abs(b.x+b.w/2-box.x-box.w/2)<1.5&&Math.abs(b.y+b.h/2-box.y-box.h/2)<1.5;});
      if(candidates.length!==1)throw new Error(`Ambiguous/missing native image binding for ${s.key}/${role.role}: ${candidates.length}`);
      used.add(candidates[0].objectId);roles.push({...role,objectId:candidates[0].objectId});
    }
  }return roles;
}
function pageSizeValid(s:DeckSnapshot){if(!s.pageSize)return false;const v=(x:any)=>x?.magnitude/(x?.unit==='EMU'?EMU:1);return Math.abs(v(s.pageSize.width)-720)<.05&&Math.abs(v(s.pageSize.height)-405)<.05;}
export function verifyCompiledReadback(compiled:CompiledDeck,after:DeckSnapshot,roles:ElementRole[]){
  if(after.slides.length!==compiled.slides.length)throw new Error('Native slide count mismatch.');
  if(!pageSizeValid(after))throw new Error('Native canvas is not 720 × 405 pt.');
  const native=elementsById(after);
  for(const s of compiled.slides){for(const b of s.boxes.filter(b=>b.role==='text'&&b.text)){const e=native.get(b.objectId);const text=((e?.shape as any)?.text?.textElements??[]).map((x:any)=>x.textRun?.content??'').join('').replace(/\n$/,'');if(text!==b.text)throw new Error(`Native text mismatch at ${s.key}/${b.objectId}`);}}
  if(roles.filter(r=>r.kind==='image').length!==compiled.assetUses.length)throw new Error('Image binding count mismatch.');
}
export function requireReview(receipt:ReviewReceipt|undefined,stage:ReviewReceipt['stage'],hash:string){if(!receipt||receipt.stage!==stage||receipt.subjectHash!==hash||receipt.decision!=='approved'||!receipt.reviewer||!receipt.reviewedAt)throw new Error(`${stage} review is missing, stale or held.`);}

function pristineDefaultTitleSlide(s:DeckSnapshot):boolean {
  if(s.slides.length!==1)return false;
  const page=s.slides[0],els=page.pageElements??[];
  const types=els.map(e=>(e.shape as any)?.placeholder?.type).sort();
  const empty=(e:any)=>!((e.shape?.text?.textElements??[]).map((t:any)=>t.textRun?.content??'').join('').trim());
  if(els.length!==2||types.join(',')!=='CENTERED_TITLE,SUBTITLE'||els.some(e=>!e.shape||e.image||e.elementGroup||!empty(e)))return false;
  if((page as any).pageProperties?.pageBackgroundFill?.propertyState!=='INHERIT')return false;
  return (page.slideProperties?.notesPage?.pageElements??[]).every(empty);
}
export async function createStaging(project:Project,compiled:CompiledDeck,port:NativePort,options:{root:string;out:string;storyboard:ReviewReceipt;title?:string;verifiedAssetHashes:Record<string,string>;unverifiedInternalAssetIds?:string[];protectedIds?:string[];allowPristineTitleSlide?:boolean}):Promise<StageReceipt>{
  await assertValidProject(project,{projectRoot:options.root,checkFiles:true});validateCompiled(compiled);requireReview(options.storyboard,'storyboard',compiled.inputHash);
  if(compiled.inputHash!==sha256(project))throw new Error('Compiled project is stale.');
  for(const id of new Set(compiled.assetUses.map(u=>u.assetId))){const asset=project.assets.find(a=>a.id===id)!;if(options.verifiedAssetHashes[id]!==asset.sha256&&!(project.meta.audience==='internal'&&options.unverifiedInternalAssetIds?.includes(id)))throw new Error(`Remote image bytes not verified for ${id}.`);}
  await mkdir(options.out,{recursive:true});const receiptPath=resolve(options.out,'stage-receipt.json'),title=options.title??`[INTERNAL REVIEW] ${project.meta.title}`;
  let receipt:StageReceipt;
  if(await exists(receiptPath)){receipt=await readJson(receiptPath);if(receipt.inputHash!==compiled.inputHash||receipt.compiledHash!==sha256(compiled)||receipt.title!==title)throw new Error('Existing stage belongs to different input. Use a new revision directory.');if(!receipt.presentationId)throw new Error('Uncertain prior create: reconcile the recorded attempt, do not create a duplicate.');}
  else{receipt={schemaVersion:'1.0.0',kind:'create-staging',projectId:project.meta.projectId,inputHash:compiled.inputHash,compiledHash:sha256(compiled),status:'create-pending',title,completedSlides:[]};await save(receiptPath,receipt);const result=await port.create(title);receipt.presentationId=result.presentationId;receipt.url=result.url;receipt.status='created';await save(receiptPath,receipt);}
  const id=receipt.presentationId!;if(options.protectedIds?.includes(id))throw new Error('Protected destination.');
  let current=await port.snapshot(id);if(current.title!==title)throw new Error('Stage identity/title changed.');if(!pageSizeValid(current))throw new Error('New presentation has wrong page size; no content applied.');
  if(receipt.status==='complete'){if(snapshotHash(current)!==receipt.afterHash)throw new Error('Completed staging has human edits. Preserve it and start a new revision; never replay.');if(port.exportPDF&&!await exists(resolve(options.out,'export-receipt.json')))await save(resolve(options.out,'export-receipt.json'),await port.exportPDF(id,resolve(options.out,'deck.pdf')));return receipt;}
  // Some providers create a blank title page. Initialize only a deck created by this
  // journal, only with explicit opt-in, and only after archiving its pristine state.
  if(options.allowPristineTitleSlide&&receipt.completedSlides.length===0&&['created','bootstrap-pending'].includes(receipt.status)){
    if(pristineDefaultTitleSlide(current)){
      if(receipt.bootstrap&&receipt.bootstrap.beforeHash!==snapshotHash(current))throw new Error('Initial blank slide changed; preserve it.');
      receipt.bootstrap??={slideId:current.slides[0].objectId,beforeHash:snapshotHash(current)};
      await save(resolve(options.out,'bootstrap-before.json'),current);receipt.status='bootstrap-pending';await save(receiptPath,receipt);
      const fresh=await port.snapshot(id);if(snapshotHash(fresh)!==receipt.bootstrap.beforeHash)throw new Error('Initial blank slide changed; preserve it.');
      await port.batch(id,[{deleteObject:{objectId:receipt.bootstrap.slideId}}]);current=await port.snapshot(id);
      if(current.slides.length!==0)throw new Error('Native initialization did not produce an empty deck.');
      receipt.bootstrap.removed=true;receipt.status='initialized';await save(receiptPath,receipt);
    }else if(receipt.status==='bootstrap-pending'&&current.slides.length===0&&receipt.bootstrap){receipt.bootstrap.removed=true;receipt.status='initialized';await save(receiptPath,receipt);}
  }
  const allowed=new Set(compiled.slides.map(s=>s.objectId));if(current.slides.some(s=>!allowed.has(s.objectId)))throw new Error('Unexpected slide on staging; do not delete it.');
  for(const slide of compiled.slides){if(!current.slides.some(s=>s.objectId===slide.objectId)){receipt.status=`apply-pending:${slide.key}`;await save(receiptPath,receipt);await port.batch(id,slide.requests);}if(!receipt.completedSlides.includes(slide.key))receipt.completedSlides.push(slide.key);await save(receiptPath,receipt);}
  // Batches are atomic and deterministic IDs make interrupted creates resumable.
  // Read the full deck once, rather than refetch every prior slide after each page.
  current=await port.snapshot(id);
  const roleMap=bindRoles(compiled,current);verifyCompiledReadback(compiled,current,roleMap);
  if(!receipt.notesApplied){
    const requests:SlidesRequest[]=roleMap.filter(r=>r.kind==='image').map(r=>({updateImageProperties:{objectId:r.objectId,imageProperties:{outline:{propertyState:'NOT_RENDERED'}},fields:'outline'}}));
    for(const slide of compiled.slides){
      const native=current.slides.find(s=>s.objectId===slide.objectId)!;
      const noteId=native.slideProperties?.notesPage?.notesProperties?.speakerNotesObjectId;
      if(!noteId)throw new Error(`Native notes were not returned for ${slide.key}; notes gate held.`);
      const note=native.slideProperties?.notesPage?.pageElements?.find((e:any)=>e.objectId===noteId);
      const existing=(note?.shape?.text?.textElements??[]).map((e:any)=>e.textRun?.content??'').join('').replace(/\n$/,'');
      if(existing===slide.notes)continue;
      if(existing.trim())throw new Error(`Unexpected speaker notes on ${slide.key}; preserve human edits.`);
      // A fresh speaker-notes placeholder has no text range to delete.
      requests.push({insertText:{objectId:noteId,insertionIndex:0,text:slide.notes}});
    }
    if(requests.length)await port.batch(id,requests);receipt.notesApplied=true;await save(receiptPath,receipt);current=await port.snapshot(id);
  }
  for(const slide of compiled.slides){const page=current.slides.find(s=>s.objectId===slide.objectId)!;const noteId=page.slideProperties?.notesPage?.notesProperties?.speakerNotesObjectId;const note=page.slideProperties?.notesPage?.pageElements?.find((e:any)=>e.objectId===noteId);const text=(note?.shape?.text?.textElements??[]).map((e:any)=>e.textRun?.content??'').join('').replace(/\n$/,'');if(text!==slide.notes)throw new Error(`Speaker-note readback mismatch: ${slide.key}`);}
  receipt.status='complete';receipt.assetExceptions=options.unverifiedInternalAssetIds??[];receipt.afterHash=snapshotHash(current);receipt.roleMap=roleMap;await save(resolve(options.out,'native-after.json'),current);await save(receiptPath,receipt);
  const binding:Binding={schemaVersion:'1.0.0',projectId:project.meta.projectId,presentationId:id,expectedTitle:title,protectedPresentationIds:options.protectedIds??[],roleMap};await save(resolve(options.out,'binding.json'),binding);
  if(port.exportPDF)await save(resolve(options.out,'export-receipt.json'),await port.exportPDF(id,resolve(options.out,'deck.pdf')));
  return receipt;
}

/** Production promotion is fail-closed unless the port supports native atomic revision control. */
export async function promoteRevision(binding:Binding,plan:PatchPlan,port:NativePort,review:ReviewReceipt){
  if(!port.conditionalRevisions)throw new Error('LIVE_PROMOTION_HELD: this connection has no atomic conditional revision support. Review staging; do not claim a preflight hash is a lock.');
  requireReview(review,'visual',plan.planHash);const before=await port.snapshot(binding.presentationId);const gate=verifyPatchPlan(binding,before,plan);if(gate.status==='no-op')return gate;
  if(!before.revisionId)throw new Error('Native revision token is missing.');
  const backup=await port.duplicate(binding.presentationId,`${binding.expectedTitle} — before ${plan.revision}`);
  const finalBefore=await port.snapshot(binding.presentationId);verifyPatchPlan(binding,finalBefore,plan);if(!finalBefore.revisionId)throw new Error('Native revision token missing.');
  await port.batch(binding.presentationId,patchRequests(plan,finalBefore),finalBefore.revisionId);
  const after=await port.snapshot(binding.presentationId),result=verifyPatchResult(finalBefore,after,plan);
  binding.lastApplied={revision:plan.revision,planHash:plan.planHash,afterHash:snapshotHash(after)};return{result,backup,binding};
}

/** A review copy, never the production destination. Caller persists returned receipts immediately. */
export async function stageRevision(binding:Binding,plan:PatchPlan,port:NativePort,out:string){
  await mkdir(out,{recursive:true});const receiptPath=resolve(out,'revision-receipt.json');
  if(await exists(receiptPath)){const r=await readJson(receiptPath);if(r.planHash!==plan.planHash)throw new Error('Revision receipt belongs to another plan.');if(r.status!=='complete')throw new Error('Prior staging attempt needs reconciliation; no automatic repeated side effect.');const s=await port.snapshot(r.stageId);if(snapshotHash(s)!==r.afterHash)throw new Error('Review copy has changed; preserve human edits.');return r;}
  const before=await port.snapshot(binding.presentationId);verifyPatchPlan(binding,before,plan);const journal:any={status:'backup-pending',planHash:plan.planHash,sourceHash:snapshotHash(before)};await save(receiptPath,journal);
  const backup=await port.duplicate(binding.presentationId,`${binding.expectedTitle} — before ${plan.revision}`);journal.backup=backup;await save(receiptPath,journal);
  const stage=await port.duplicate(binding.presentationId,`[REVISION REVIEW] ${binding.expectedTitle} — ${plan.revision}`);journal.stageId=stage.presentationId;journal.status='stage-created';await save(receiptPath,journal);
  const sourceAgain=await port.snapshot(binding.presentationId);verifyPatchPlan(binding,sourceAgain,plan);const stageBefore=await port.snapshot(stage.presentationId);
  const deckContent=(s:DeckSnapshot)=>snapshotHash({...s,presentationId:'copy-neutral',title:'copy-neutral'});if(deckContent(before)!==deckContent(stageBefore))throw new Error('Review copy differs from baseline; inspect and reconcile, do not apply.');
  const stageBinding={...binding,presentationId:stage.presentationId,expectedTitle:stageBefore.title!,lastApplied:undefined};const stagePlan=makePatchPlan(stageBinding,stageBefore,{revision:plan.revision,operations:plan.operations,allowedObjectIds:plan.allowedObjectIds});
  await save(resolve(out,'source-plan.json'),plan);await save(resolve(out,'staging-plan.json'),stagePlan);await save(resolve(out,'native-before.json'),stageBefore);
  journal.status='apply-pending';await save(receiptPath,journal);await port.batch(stage.presentationId,patchRequests(stagePlan,stageBefore));const after=await port.snapshot(stage.presentationId);const result=verifyPatchResult(stageBefore,after,stagePlan);
  const unchanged=await port.snapshot(binding.presentationId);if(snapshotHash(unchanged)!==snapshotHash(before))throw new Error('Source changed during review-copy work; reconcile before promotion.');
  Object.assign(journal,{status:'complete',result,afterHash:snapshotHash(after),sourceUnchanged:true,productionPromotion:port.conditionalRevisions?'requires-reviewed-promotion':'held-no-conditional-revisions'});await save(resolve(out,'native-after.json'),after);await save(receiptPath,journal);
  if(port.exportPDF)await save(resolve(out,'export-receipt.json'),await port.exportPDF(stage.presentationId,resolve(out,'deck.pdf')));return journal;
}
