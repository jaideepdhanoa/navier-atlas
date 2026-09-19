import type {Project,CompiledDeck,EditorialReview,ReviewReceipt,RenderReviewBundle,VisualInspection} from './types';
import {sha256} from './primitives';
import {salesAudit,visibleCopyHash} from './authoring';
import {validateProject} from './validate';
import {verifyRenderFiles} from './artifact-files';

const timestamp=(s:unknown)=>typeof s==='string'&&!Number.isNaN(Date.parse(s));
const text=(s:unknown)=>typeof s==='string'&&s.trim().length>0;
const ANSWERS=['partnerImportance','companyDifference','businesses','strategicUpside','invitation'] as const;
const TESTS=['partnerSpecificity','companyRemoval','sourceFidelity'] as const;
export function editorialTemplate(project:Project,compiled:CompiledDeck):EditorialReview{
 const blank=()=>({answer:'',slideKeys:[]});
 return {schemaVersion:'2.0.0',subjectHash:compiled.inputHash,visibleCopyHash:visibleCopyHash(compiled),reviewer:{name:'',kind:'agent'},reviewedAt:'',decision:'revise',answers:{partnerImportance:blank(),companyDifference:blank(),businesses:blank(),strategicUpside:blank(),invitation:blank()},tests:{partnerSpecificity:blank(),companyRemoval:blank(),sourceFidelity:blank()},findings:[{code:'UNREVIEWED',severity:'revise',detail:'Unsigned template. Read only the visible copy first; then compare source dispositions. This is not human or release approval.',slideKeys:[]}]};
}
export function editorialProblems(project:Project,compiled:CompiledDeck,review:EditorialReview|undefined):string[]{
 const problems:string[]=[];
 if(!review)return ['Fresh-reader sales review is missing.'];
 if(review.schemaVersion!=='2.0.0'||review.subjectHash!==compiled.inputHash||review.visibleCopyHash!==visibleCopyHash(compiled))problems.push('Fresh-reader review is stale or bound to another artifact.');
 if(!text(review.reviewer?.name)||!['human','agent','fixture'].includes(review.reviewer?.kind)||!timestamp(review.reviewedAt))problems.push('Editorial reviewer identity/date is missing.');
 if(review.reviewer?.kind==='fixture'&&!project.meta.fictional)problems.push('Fixture reviews cannot approve a real partner story.');
 if(review.decision!=='pass')problems.push('Fresh-reader review requests revision.');
 const keys=new Set(compiled.slides.map(s=>s.key));
 for(const [group,items] of [['answers',ANSWERS],['tests',TESTS]] as const)for(const key of items){const a=(review[group] as any)?.[key];if(!a||!text(a.answer)||!Array.isArray(a.slideKeys)||a.slideKeys.length===0||a.slideKeys.some((k:string)=>!keys.has(k)))problems.push(`Missing answer or valid visible-copy citations: ${group}.${key}.`);}
 if(!Array.isArray(review.findings)||review.findings.some(f=>f.severity==='revise'))problems.push('Unresolved editorial findings.');
 const audit=salesAudit(project,compiled);if(audit.findings.some(f=>f.severity==='revise'))problems.push('Sales audit has unresolved narrative/coverage findings.');
 return problems;
}
export function requireEditorialReview(project:Project,compiled:CompiledDeck,review:EditorialReview|undefined){const bad=editorialProblems(project,compiled,review);if(bad.length)throw new Error('EDITORIAL_REVIEW_HELD: '+bad.join(' '));}
export function visualInspectionProblems(bundle:RenderReviewBundle,review:VisualInspection|undefined):string[]{
 const bad:string[]=[];if(!review)return ['Full-page/phone inspection is missing.'];
 if(review.schemaVersion!=='2.0.0'||review.bundleHash!==sha256(bundle))bad.push('Visual inspection refers to a different export or render set.');
 if(!review.reviewer?.name||!['human','agent','fixture'].includes(review.reviewer.kind)||!timestamp(review.reviewedAt))bad.push('Visual reviewer identity/date is missing.');
 if(review.decision!=='pass')bad.push('Visual inspection requests revision.');
 if(!Array.isArray(review.pages)||review.pages.length!==bundle.pages.length||new Set(review.pages.map(p=>p.slideKey)).size!==bundle.pages.length)bad.push('Visual inspection must cover each page exactly once.');
 for(const page of bundle.pages){const r=review.pages?.find(r=>r.slideKey===page.slideKey);if(!r?.fullInspected||!r.phoneInspected||!text(r.headlineGist)||!Array.isArray(r.findings)||r.findings.length)bad.push(`Inspect/fix full and phone renders: ${page.slideKey}.`);}
 if(bundle.status!=='ready-for-inspection'||bundle.holds.length)bad.push('Render integrity bundle has unresolved holds.');
 return bad;
}
/** Human release is a distinct, fail-closed decision. Neither an agent review nor a fixture creates it. */
export async function releaseDecision(project:Project,compiled:CompiledDeck,input:{projectRoot:string;renderRoot?:string;editorial?:EditorialReview;bundle?:RenderReviewBundle;visual?:VisualInspection;finishedDeck?:ReviewReceipt;release?:ReviewReceipt}){
 const holds:string[]=[];
 if(project.meta.fictional||project.meta.audience==='internal')holds.push('Fictional/internal review artifacts are not external releases.');
 if(compiled.inputHash!==sha256(project))holds.push('Compiled input is stale.');
 const checked=await validateProject(project,{projectRoot:input.projectRoot,checkFiles:true});
 holds.push(...checked.issues.filter(i=>i.severity!=='warning'&&i.code!=='HUMAN_RELEASE_REQUIRED').map(i=>`${i.code}: ${i.message}`));
 holds.push(...editorialProblems(project,compiled,input.editorial));
 if(!input.bundle)holds.push('Reviewed export bundle is missing.');
 else{
  if(input.bundle.inputHash!==compiled.inputHash||input.bundle.compiledHash!==sha256(compiled)||input.bundle.visibleCopyHash!==visibleCopyHash(compiled))holds.push('Export bundle is stale.');
  holds.push(...visualInspectionProblems(input.bundle,input.visual));
  if(!input.renderRoot)holds.push('Render files must be rehashed before release.');
  else {try{holds.push(...await verifyRenderFiles(input.bundle,input.renderRoot));}catch(e){holds.push('Render file verification failed: '+String(e));}}
 }
 const finalHash=input.bundle?sha256(input.bundle):'';
 for(const [name,r,purpose] of [['Finished-deck approval',input.finishedDeck,'finished-deck'],['External-release permission',input.release,'external-release']] as const){
  if(!r||r.reviewerKind!=='human'||r.purpose!==purpose||r.decision!=='approved'||r.subjectHash!==finalHash||!r.reviewer||!timestamp(r.reviewedAt)||r.stage!==(purpose==='external-release'?'release':'visual'))holds.push(`${name} requires a named, dated human receipt bound to the reviewed render bundle.`);
 }
 return {status:holds.length?'held':'approved-for-external-circulation',holds:[...new Set(holds)],automaticSending:false};
}
