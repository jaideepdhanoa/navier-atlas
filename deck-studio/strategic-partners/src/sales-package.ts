import type {Project,CompiledDeck,SalesAuthoring} from './types';
import {salesAudit,slideTitle,resolveBlock} from './authoring';
import {editorialTemplate} from './reviews';

export function emptySalesAuthoring():SalesAuthoring{return {
 brief:{role:'standalone',audienceDecision:'TO AUTHOR',partnerRelevance:'TO AUTHOR',partnerThesis:'TO AUTHOR',companyDifference:'TO AUTHOR',combinationAdvantage:'TO AUTHOR',strategicUpside:'TO AUTHOR',investmentBoundary:'TO AUTHOR',sourceIds:[],unresolvedQuestions:['Recover the approved brief, strongest source slides, audience, decision and disclosure boundary.'],companions:{status:'unknown',reason:'Recover the versioned documents each recipient already holds.',documents:[],reconciliations:[]},leverTransfer:{status:'unresolved',reason:'Assess whether the thesis relies on transferred economics or performance.',claimIds:[],sourceIds:[],result:'unresolved'}},
 sourceInventory:[],sourceDisposition:[],blocks:[],narrative:[],
};}
export function salesArtifacts(project:Project,compiled:CompiledDeck):Record<string,string>{
 if(!project.sales)return {};
 const {brief,sourceInventory,sourceDisposition,narrative}=project.sales;
 const markdown=['# Partner sales thesis','',`**Role:** ${brief.role}`,`**Audience decision:** ${brief.audienceDecision}`,'',...([
  ['Why this partner should care',brief.partnerRelevance],['The sales thesis',brief.partnerThesis],['What is differentiated',brief.companyDifference],['Why the combination wins',brief.combinationAdvantage],['Strategic upside',brief.strategicUpside],['Investment-deck boundary',brief.investmentBoundary],
 ] as [string,string][]).flatMap(([h,t])=>[`## ${h}`,t,'']),'## Unresolved questions',...brief.unresolvedQuestions.map(s=>'- '+s),'','> Internal authoring record. Not a partner commitment or release approval.'].join('\n');
 const preservation=['# Source-to-story preservation','',...sourceInventory.flatMap(item=>{
  const d=sourceDisposition.find(d=>d.sourceItemId===item.id)!;
  return [`## ${item.id} — ${item.importance}`,`Original: ${item.summary}`,`Source: ${item.sourceId}`,`Decision: **${d.action}** — ${d.reason}`,`Visual: ${d.visualDecision} — ${d.visualReason}`,`Destinations: ${d.destinationBlockIds.join(', ')||'Intentionally omitted'}`,...d.destinationBlockIds.map(id=>'- '+resolveBlock(project,id).text),''];
 })].join('\n');
 const storyboard=['# Sales storyboard','',`**Partner thesis:** ${brief.partnerThesis}`,'',...compiled.slides.flatMap((s,i)=>{
  const a=project.slides.find(v=>v.key===s.key)!,n=narrative.find(n=>n.slideKey===s.key)!;
  return [`## ${i+1}. ${slideTitle(project,a)}`,`**Job:** ${n.job} · **Chapter:** ${n.chapter} · **Placement:** ${n.placement}`,`**Takeaway:** ${n.takeaway}`,`**Transition:** ${n.transition}`,`**Composition:** ${a.layout==='sales'?a.composition:a.layout}`,`**Opportunities:** ${a.opportunityIds.join(', ')||'Opening/context'}`,'','### Actual emitted copy',...s.visibleText.map(t=>'- '+t),'','### Real image candidates',...compiled.assetUses.filter(u=>u.slideKey===s.key).map(u=>{const asset=project.assets.find(a=>a.id===u.assetId)!;return `- ${asset.path} — ${asset.caption}\n  Intended argument: ${asset.visualBrief?.argument??'See asset record.'}\n  Required: ${asset.visualBrief?.requiredFeatures.join('; ')??'See asset record.'}`;}),''];
 })].join('\n');
 const json=(x:unknown)=>JSON.stringify(x,null,2)+'\n';
 return {'sales-brief.md':markdown,'source-preservation.md':preservation,'storyboard.md':storyboard,'visible-bindings.json':json({inputHash:compiled.inputHash,blocks:compiled.slides.flatMap(s=>s.copyBindings??[])}),'sales-audit.json':json(salesAudit(project,compiled)),'sales-review-template.json':json(editorialTemplate(project,compiled))};
}
export function migrationDraft(project:Project){
 if(project.schemaVersion!=='1.0.0')throw new Error('Migration input must be a V1 project. Existing V2 projects do not need conversion.');
 return {status:'HELD',kind:'V2-AUTHORING-DRAFT-NOT-A-PROJECT',sourceVersion:project.schemaVersion,projectId:project.meta.projectId,
  sales:emptySalesAuthoring(),opportunityCases:project.opportunities.map(o=>({opportunityId:o.id,need:'',alternative:'',scaleBasis:'',mechanism:'',outcome:'',ambition:'',entryPoint:'',evidenceBoundary:'',demandStatus:null,readiness:null})),
  instructions:['The V1 snapshot remains runnable with the V1 compatibility path.','Author the partner thesis and original-source dispositions; do not infer them from empty fields.','Build real CopyBlocks; from references dereference opportunity values. Bind abbreviated authored copy explicitly.','Choose compositions by their explanatory job. Do not convert every old slide into the same layout.','Preserve human native edits by making a new staging/review copy, not replaying a build over a live deck.','For a new project use schemaVersion 2.1.0 after authoring the V2 sales story and the structured evidence, recipient continuity, safe talk tracks and two editorial rounds. This historical V2 story envelope is not compiler input.'],
 };
}
