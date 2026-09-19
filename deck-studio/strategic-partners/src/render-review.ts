import {readFile,writeFile,mkdir,mkdtemp,readdir,rm} from 'node:fs/promises';
import {join,resolve} from 'node:path';
import {tmpdir} from 'node:os';
import type {Project,CompiledDeck,DeckSnapshot,RenderReviewBundle,VisualInspection} from './types';
import {sha256} from './primitives';
import {snapshotHash} from './revisions';
import {bindRoles,verifyCompiledReadback} from './lifecycle';
import {visibleCopyHash} from './authoring';
import {byteHash} from './artifact-files';
const normalized=(text:string)=>text.normalize('NFKC').replace(/[\u2018\u2019]/g,"'").replace(/[\u201c\u201d]/g,'"').replace(/[\u2010-\u2015-]/g,'').replace(/[\s\u00ad]/g,'').toLowerCase();
async function command(args:string[]){const p=Bun.spawn(args,{stdout:'pipe',stderr:'pipe'});const [out,err,code]=await Promise.all([new Response(p.stdout).text(),new Response(p.stderr).text(),p.exited]);if(code!==0)throw new Error(`${args[0]} failed: ${err}`);return out;}
async function immutable(path:string,bytes:Uint8Array|string){try{const old=await readFile(path);const b=typeof bytes==='string'?Buffer.from(bytes):bytes;if(byteHash(old)!==byteHash(b))throw new Error('Refusing to overwrite a different review artifact: '+path);return;}catch(e){if((e as NodeJS.ErrnoException).code!=='ENOENT')throw e;}await writeFile(path,bytes,{flag:'wx'});}
/** Local proof harness for an ACTUAL exported native PDF. It does not produce an inspection or human approval. */
export async function collectRenderReview(project:Project,compiled:CompiledDeck,native:DeckSnapshot,pdfPath:string,out:string):Promise<RenderReviewBundle>{
 if(compiled.inputHash!==sha256(project))throw new Error('Review input is stale.');
 const roles=bindRoles(compiled,native);verifyCompiledReadback(compiled,native,roles);
 const info=await command(['pdfinfo',resolve(pdfPath)]);const pages=Number(info.match(/^Pages:\s+(\d+)/m)?.[1]);
 if(pages!==compiled.slides.length)throw new Error('PDF page count does not match compiled/native deck.');
 const raw=await command(['pdftotext','-layout',resolve(pdfPath),'-']);const pageText=raw.split('\f');
 const scratch=await mkdtemp(join(tmpdir(),'strategic-render-review-'));
 const root=resolve(out);await mkdir(join(root,'full'),{recursive:true});await mkdir(join(root,'phone'),{recursive:true});
 try{
  await Promise.all([command(['pdftoppm','-r','144','-png',resolve(pdfPath),join(scratch,'full')]),command(['pdftoppm','-scale-to-x','400','-scale-to-y','225','-png',resolve(pdfPath),join(scratch,'phone')])]);
  const files=await readdir(scratch);const numbered=(prefix:string)=>files.filter(f=>f.startsWith(prefix+'-')&&f.endsWith('.png')).sort((a,b)=>Number(a.match(/-(\d+)\.png$/)?.[1])-Number(b.match(/-(\d+)\.png$/)?.[1]));
  const full=numbered('full'),phone=numbered('phone');if(full.length!==pages||phone.length!==pages)throw new Error('Render outputs are incomplete.');
  const pdf=await readFile(pdfPath);await immutable(join(root,'deck.pdf'),pdf);
  const bundle:RenderReviewBundle={schemaVersion:'2.0.0',inputHash:compiled.inputHash,compiledHash:sha256(compiled),nativeHash:snapshotHash(native),nativePresentationId:native.presentationId,pdf:{path:'deck.pdf',sha256:byteHash(pdf)},pageCount:pages,visibleCopyHash:visibleCopyHash(compiled),pages:[],status:'ready-for-inspection',holds:[],inspected:false,externalRelease:'held'};
  for(let i=0;i<pages;i++){
   const texts=compiled.slides[i].visibleText.filter(t=>normalized(t).length>3);const actual=normalized(pageText[i]??'');const missing=texts.filter(t=>!actual.includes(normalized(t)));
   const key=String(i+1).padStart(2,'0'),fb=await readFile(join(scratch,full[i])),pb=await readFile(join(scratch,phone[i]));
   const f={path:`full/slide-${key}.png`,sha256:byteHash(fb)},p={path:`phone/slide-${key}.png`,sha256:byteHash(pb)};
   await immutable(join(root,f.path),fb);await immutable(join(root,p.path),pb);
   const coverage=texts.length?(texts.length-missing.length)/texts.length:0;
   bundle.pages.push({slideKey:compiled.slides[i].key,page:i+1,full:f,phone:p,textCoverage:coverage,missingText:missing});
   if(missing.length)bundle.holds.push(`PDF visible-text readback needs inspection: ${compiled.slides[i].key} (${missing.length} blocks).`);
  }
  if(bundle.holds.length)bundle.status='held';
  await immutable(join(root,'render-review.json'),JSON.stringify(bundle,null,2)+'\n');
  const template:VisualInspection={schemaVersion:'2.0.0',bundleHash:sha256(bundle),reviewer:{name:'',kind:'agent'},reviewedAt:'',decision:'revise',pages:bundle.pages.map(p=>({slideKey:p.slideKey,fullInspected:false,phoneInspected:false,headlineGist:'',findings:['Not inspected.']}))};
  await immutable(join(root,'visual-inspection-template.json'),JSON.stringify(template,null,2)+'\n');
  return bundle;
 }finally{await rm(scratch,{recursive:true,force:true});}
}
