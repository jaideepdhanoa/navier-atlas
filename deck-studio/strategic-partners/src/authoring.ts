import type {Project,Slide,ValidationIssue,CompiledDeck,CopyBlock,OpportunityBinding,SalesSlide,Visual,ReviewFinding} from './types';
import {sha256} from './primitives';

export const COMPOSITION_NAMES=['partner-opportunity','product-value','platform-architecture','opportunity-portfolio','mission-hero','customer-alternative','integrated-infrastructure','strategic-close'] as const;
export const CORE_SALES_FIELDS=['salesCase.need','salesCase.alternative','product','customer','salesCase.mechanism','salesCase.outcome','partnerBenefit','salesCase.ambition'] as const;
export const DETAIL_FIELDS=['payer','commercialLogic','companyContribution','partnerContribution','salesCase.entryPoint','salesCase.evidenceBoundary','nextQuestion'] as const;
const unique=<T>(x:T[])=>[...new Set(x)];
const nonempty=(x:unknown)=>typeof x==='string'&&x.trim().length>0;

export function bindingsFor(block:CopyBlock):OpportunityBinding[]{
 const all=[...(block.from?[block.from]:[]),...block.bindings];
 return all.filter((b,i)=>all.findIndex(a=>a.opportunityId===b.opportunityId&&a.field===b.field)===i);
}
export function resolveBlock(project:Project,id:string){
 const block=project.sales?.blocks.find(b=>b.id===id);
 if(!block)throw new Error(`Unknown copy block ${id}`);
 let text=block.text;
 if(block.from){const o=project.opportunities.find(o=>o.id===block.from!.opportunityId);if(!o)throw new Error(`Unknown opportunity ${block.from.opportunityId}`);text=block.from.field.startsWith('salesCase.')?o.salesCase?.[block.from.field.slice(10) as keyof NonNullable<typeof o.salesCase>]:(o as unknown as Record<string,string>)[block.from.field];}
 if(!nonempty(text))throw new Error(`Copy block ${id} resolves to no authored text; do not invent missing sales copy.`);
 const bindings=bindingsFor(block);
 const claimIds=unique([...block.claimIds,...(project.schemaVersion==='2.1.0'?[]:bindings.flatMap(b=>project.opportunities.find(o=>o.id===b.opportunityId)?.claimIds??[]))]);
 return {block,text:text!+(block.qualification?'\n'+block.qualification:''),claimIds,bindings};
}
export function blockIds(slide:Slide):string[]{
 if(slide.layout!=='sales')return [];
 const s=slide,base=[s.title,s.status],pairs=(v:{heading:string;body:string}[])=>v.flatMap(x=>[x.heading,x.body]);
 switch(s.composition){
  case 'partner-opportunity':return [...base,s.intro,...pairs(s.domains),...pairs(s.proof),s.offer];
  case 'product-value':return [...base,s.mechanism,...pairs(s.benefits),s.proof];
  case 'platform-architecture':return [...base,s.banner,...pairs(s.physical),s.ownership,s.software,s.revenue,...pairs(s.demand),s.takeaway];
  case 'opportunity-portfolio':return [...base,s.intro,...s.programs.flatMap(x=>[x.heading,x.value]),s.connection];
  case 'mission-hero':return [...base,s.need,...pairs(s.benefits),s.payoff];
  case 'customer-alternative':return [...base,s.intro,...pairs(s.alternatives),s.jobs,s.advantage,s.comparison.basisBlockId];
  case 'integrated-infrastructure':return [...base,s.intro,...pairs(s.actions),s.options];
  case 'strategic-close':return [...base,s.intro,...pairs(s.stakes),s.invitation,...(s.companion?[s.companion.labelBlockId]:[])];
 }
}
/** Evidence/status and fine-print slots cannot carry the core sales argument by themselves. */
export function isArgumentBlock(slide:Slide,id:string):boolean {
 if(slide.layout!=='sales'||id===slide.status)return false;
 if(slide.composition==='customer-alternative'&&id===slide.comparison.basisBlockId)return false;
 if(slide.composition==='product-value'&&id===slide.proof)return false;
 if(slide.composition==='mission-hero'&&id===slide.payoff)return false;
 if(slide.composition==='strategic-close'&&id===slide.companion?.labelBlockId)return false;
 if(slide.composition==='platform-architecture'&&slide.physical.some(p=>p.body===id))return false;
 return blockIds(slide).includes(id);
}
export function slideTitle(project:Project,s:Slide):string{return s.layout==='sales'?resolveBlock(project,s.title).text:s.title;}
export function slideBlockClaims(project:Project,s:Slide):string[]{return unique([...s.claimIds,...blockIds(s).flatMap(id=>resolveBlock(project,id).claimIds)]);}
export function collectVisuals(value:unknown,out:Visual[]=[]):Visual[]{
 if(Array.isArray(value))value.forEach(v=>collectVisuals(v,out));
 else if(value&&typeof value==='object'){
  const v=value as Record<string,unknown>;
  if(typeof v.assetId==='string'&&typeof v.caption==='string')out.push(v as unknown as Visual);
  else Object.values(v).forEach(v=>collectVisuals(v,out));
 }
 return out;
}
export function visibleCopyHash(compiled:CompiledDeck){return sha256(compiled.slides.map(s=>({key:s.key,text:s.visibleText})));}
export function notesBlocks(project:Project,slide:Slide){
 if(!project.sales)return [];
 return project.sales.blocks.filter(b=>b.placement==='notes'&&bindingsFor(b).some(x=>slide.opportunityIds.includes(x.opportunityId))).map(b=>resolveBlock(project,b.id));
}

/** Add semantic constraints on top of JSON Schema. This is not a test of persuasion or factual accuracy. */
export function salesIssues(project:Project):ValidationIssue[]{
 if(!['2.0.0','2.1.0'].includes(project.schemaVersion))return [];
 const result:ValidationIssue[]=[],add=(code:string,path:string,message:string,severity:ValidationIssue['severity']='error')=>result.push({code,path,message,severity});
 const sales=project.sales;if(!sales){add('SALES_REQUIRED','sales','V2 requires sales authoring.');return result;}
 const blocks=new Map(sales.blocks.map(b=>[b.id,b]));
 const sources=new Set(project.sources.map(s=>s.id)),claims=new Map(project.claims.map(c=>[c.id,c])),opps=new Map(project.opportunities.map(o=>[o.id,o]));
 const check=(values:string[],known:Set<string>|Map<string,unknown>,path:string)=>values.forEach(v=>{if(!known.has(v))add('UNKNOWN_REFERENCE',path,`Unknown reference ${v}`);});
 const dup=(values:string[],path:string)=>{if(new Set(values).size!==values.length)add('DUPLICATE_ID',path,'Duplicate identity is not allowed.');};
 dup(sales.blocks.map(b=>b.id),'sales.blocks');dup(project.slides.map(s=>s.key),'slides');dup(sales.sourceInventory.map(s=>s.id),'sales.sourceInventory');dup(sales.sourceDisposition.map(s=>s.sourceItemId),'sales.sourceDisposition');dup(sales.narrative.map(s=>s.slideKey),'sales.narrative');
 check(sales.brief.sourceIds,sources,'sales.brief.sourceIds');
 const positions=new Map(project.slides.map((s,i)=>[s.key,i]));
 if(sales.narrative.map(n=>n.slideKey).join('|')!==project.slides.map(s=>s.key).join('|'))add('NARRATIVE_SEQUENCE','sales.narrative','Narrative must describe every slide in exact rendering order.');
 const rendered=new Map<string,{slide:Slide;placement:string}[]>();
 const coreArgument=(id:string)=>(rendered.get(id)??[]).some(u=>u.placement==='core'&&isArgumentBlock(u.slide,id));
 for(const s of project.slides){
  const n=sales.narrative.find(n=>n.slideKey===s.key);
  if(n){check(n.opportunityIds,opps,`sales.narrative.${s.key}.opportunityIds`);if(n.opportunityIds.some(id=>!s.opportunityIds.includes(id)))add('NARRATIVE_OPPORTUNITY_MISMATCH',`slides.${s.key}`,'Narrative and slide opportunities disagree.');}
  for(const id of blockIds(s)){
   check([id],blocks,`slides.${s.key}`);
   const uses=rendered.get(id)??[];uses.push({slide:s,placement:n?.placement??'core'});rendered.set(id,uses);
   const b=blocks.get(id);if(b&&b.placement!==(n?.placement??'core'))add('BLOCK_PLACEMENT',`sales.blocks.${id}`,'Visible blocks must match their narrative core/appendix placement; notes never render as core copy.');
  }
  if(s.layout==='sales'&&s.composition==='opportunity-portfolio'){
   check(s.programs.map(x=>x.opportunityId),opps,`slides.${s.key}.programs`);
   if(s.programs.some(x=>!s.opportunityIds.includes(x.opportunityId)))add('PORTFOLIO_BINDING',`slides.${s.key}`,'Portfolio program is not declared in slide opportunityIds.');
  }
  if(s.layout==='sales'&&s.composition==='platform-architecture'&&!s.physical.some(x=>x.visual))add('PLATFORM_PRODUCT_VISUAL',`slides.${s.key}`,'Platform architecture needs an actual product/context/concept visual, not only empty boxes.');
  if(s.layout==='sales'&&s.composition==='customer-alternative'){
   check(s.comparison.claimIds,claims,`slides.${s.key}.comparison`);
   if(s.alternatives.filter(a=>a.emphasis).length!==1)add('COMPARISON_FOCUS',`slides.${s.key}`,'Highlight one differentiated offer; do not mark every alternative as the winner.');
   if(s.comparison.kind!=='qualitative'&&!s.comparison.claimIds.some(id=>claims.get(id)?.evidenceClass===s.comparison.kind))add('COMPARISON_EVIDENCE',`slides.${s.key}`,'Measured/modelled comparison must cite the matching evidence class.');
  }
 }
 for(const b of sales.blocks){
  check(b.claimIds,claims,`sales.blocks.${b.id}.claimIds`);
  const bindings=bindingsFor(b);check(bindings.map(x=>x.opportunityId),opps,`sales.blocks.${b.id}.bindings`);
  if(b.placement==='notes'&&!nonempty(b.placementReason))add('DETAIL_PLACEMENT_REASON',`sales.blocks.${b.id}`,'Notes-only detail needs a reason; do not silently bury the proposition.');
  if(b.placement!=='notes'&&!rendered.has(b.id))add('UNRENDERED_COPY',`sales.blocks.${b.id}`,'Core/appendix copy has no rendered destination. Remove it deliberately or put it in notes with a reason.');
  for(const use of rendered.get(b.id)??[])if(bindings.some(v=>!use.slide.opportunityIds.includes(v.opportunityId)))add('BLOCK_OPPORTUNITY_MISMATCH',`slides.${use.slide.key}`,'Visible copy is bound to an opportunity missing from this slide.');
  try{
   const r=resolveBlock(project,b.id);
   if(/\d[\d.,]*\s*(%|km|nm|kWh|MW|vessels?|passengers?|\$)|\$\s*\d/i.test(r.text)&&r.claimIds.length===0)add('BLOCK_CLAIM_MISSING',`sales.blocks.${b.id}`,'Quantitative copy needs its own claim binding, not an unrelated slide-wide citation.');
   const qualifierPatterns:Record<string,RegExp>={
    modeled:/\b(?:modeled|modelled|model|estimat(?:e|ed|ion)|scenario|illustrative)\b/i,
    preliminary:/\b(?:preliminary|indicative|initial|early|illustrative|unverified)\b/i,
    planned:/\b(?:planned|proposed|proposal|concept|target(?:ed)?|in[- ]design|hypothesis|illustrative|exploratory|future|intended)\b/i,
    proposed:/\b(?:proposed|proposal|concept|target(?:ed)?|in[- ]design|hypothesis|illustrative|exploratory|future|intended)\b/i,
   };
   const uncertain=unique(r.claimIds.map(id=>claims.get(id)?.evidenceClass??'').filter(kind=>kind in qualifierPatterns));
   if(project.schemaVersion!=='2.1.0'&&uncertain.length&&rendered.has(b.id)){
    for(const use of rendered.get(b.id)??[]){
     const status=use.slide.layout==='sales'?resolveBlock(project,use.slide.status).text:'';
     for(const kind of uncertain)if(!qualifierPatterns[kind].test(r.text+' '+status))add('VISIBLE_QUALIFIER',`sales.blocks.${b.id}`,`A ${kind} claim needs a matching visible qualification; a generic concept label, confidentiality note or speaker note is not enough.`);
    }
   }
  }catch(e){add('BLOCK_RESOLUTION',`sales.blocks.${b.id}`,String((e as Error).message));}
 }
 const sourceItems=new Map(sales.sourceInventory.map(i=>[i.id,i]));
 sales.sourceInventory.forEach(i=>{
  check([i.sourceId],sources,`sales.sourceInventory.${i.id}`);
  const disposition=sales.sourceDisposition.find(d=>d.sourceItemId===i.id);
  if(!disposition)add('SOURCE_UNDISPOSITIONED',`sales.sourceInventory.${i.id}`,'Every original proposition/reference slide needs a keep, strengthen, qualify or omit decision.');
 });
 sales.sourceDisposition.forEach(d=>{
  check([d.sourceItemId],sourceItems,'sales.sourceDisposition');check(d.destinationBlockIds,blocks,`sales.sourceDisposition.${d.sourceItemId}`);
  if(d.action==='omit'){
   if(d.destinationBlockIds.length)add('OMIT_WITH_DESTINATION',`sales.sourceDisposition.${d.sourceItemId}`,'An omitted item cannot claim a rendered destination.');
  }else if(!d.destinationBlockIds.length||d.destinationBlockIds.every(id=>!rendered.has(id)))add('SOURCE_NOT_VISIBLE',`sales.sourceDisposition.${d.sourceItemId}`,'A retained proposition must survive in rendered copy, not merely reference the source.');
  if(sourceItems.get(d.sourceItemId)?.importance==='core'&&d.action!=='omit'&&!d.destinationBlockIds.some(id=>blocks.get(id)?.placement==='core'&&coreArgument(id)))add('CORE_SOURCE_BURIED',`sales.sourceDisposition.${d.sourceItemId}`,'Important source ideas must remain in main core copy, not evidence/status or fine print, or be explicitly omitted.');
 });
 for(const o of project.opportunities){
  if(!o.salesCase){add('SALES_CASE_REQUIRED',`opportunities.${o.id}`,'Every V2 opportunity needs a differentiated sales case.');continue;}
  for(const field of [...CORE_SALES_FIELDS,...DETAIL_FIELDS]){
   const matches=sales.blocks.filter(b=>bindingsFor(b).some(v=>v.opportunityId===o.id&&v.field===field));
   const core=(CORE_SALES_FIELDS as readonly string[]).includes(field);
   if(!matches.some(b=>core?b.placement==='core'&&coreArgument(b.id):(b.placement==='notes'&&nonempty(b.placementReason))||rendered.has(b.id)))add('SALES_COPY_COVERAGE',`opportunities.${o.id}.${field}`,`${core?'Core sales argument must reach main visible copy, not status/caption/fine print':'Commercial detail must reach a rendered block or explicitly justified notes'}.`);
  }
  if(o.salesCase.ambition===o.salesCase.entryPoint)add('AMBITION_EQUALS_ENTRY',`opportunities.${o.id}.salesCase`,'The first engagement is not the full business opportunity.');
  if(o.salesCase.demandStatus==='partner-demand'&&!project.meta.fictional&&!o.claimIds.some(id=>['measured','demonstrated','historical','company-reported'].includes(claims.get(id)?.evidenceClass??'')))add('PARTNER_DEMAND_EVIDENCE',`opportunities.${o.id}`,'Partner demand cannot be inferred solely from market context or a proposal.');
 }
 const corePlan=sales.narrative.filter(n=>n.placement==='core');
 const firstDeep=corePlan.findIndex(n=>n.job==='opportunity');
 for(const job of ['partner-relevance','company-advantage'] as const){const at=corePlan.findIndex(n=>n.job===job);if(at<0||firstDeep>=0&&at>firstDeep)add('PITCH_BEFORE_PROGRAMS','sales.narrative',`${job} must precede opportunity deep dives.`);}
 if(project.opportunities.length>1){const at=corePlan.findIndex(n=>n.job==='portfolio');if(at<0||firstDeep>=0&&at>firstDeep)add('PORTFOLIO_BEFORE_CHAPTERS','sales.narrative','Introduce multiple businesses before jumping into their chapters.');
  const introduced=new Set(project.slides.filter(s=>s.layout==='sales'&&s.composition==='opportunity-portfolio').flatMap(s=>(s as Extract<SalesSlide,{composition:'opportunity-portfolio'}>).programs.map(p=>p.opportunityId)));
  for(const o of project.opportunities)if(!introduced.has(o.id))add('PORTFOLIO_MISSING_BUSINESS',`opportunities.${o.id}`,'Opportunity is missing from the portfolio introduction.');
 }
 if(!corePlan.some(n=>n.job==='invitation'))add('INVITATION_MISSING','sales.narrative','Close with a commercial/strategic invitation, not only a work schedule.');
 const selected=new Set(collectVisuals(project.slides).flatMap(v=>[v.assetId,...(v.attachments??[]).map(a=>a.assetId)]));
 for(const a of project.assets.filter(a=>selected.has(a.id)&&a.kind!=='logo')){
  const v=a.visualBrief;
  if(!v){add('VISUAL_ARGUMENT_REQUIRED',`assets.${a.id}`,'V2 imagery needs its intended argument, required features and prohibited implications.');continue;}
  check(v.referenceSourceIds,sources,`assets.${a.id}.visualBrief`);
  if(v.sourceSlide)check([v.sourceSlide.sourceId],sources,`assets.${a.id}.visualBrief.sourceSlide`);
  if(v.review.assetSha256!==a.sha256)add('VISUAL_REVIEW_STALE',`assets.${a.id}`,'Visual review refers to different image bytes.');
  if(v.review.status==='pending')add('VISUAL_TRUTH_REVIEW',`assets.${a.id}`,'Required features, crop and prohibited implications need actual visual inspection.','release-hold');
  else if(!v.review.reviewer||!v.review.reviewedAt||Number.isNaN(Date.parse(v.review.reviewedAt)))add('VISUAL_REVIEW_IDENTITY',`assets.${a.id}`,'Reviewed images need a named, dated reviewer; this is not rights clearance.');
  if(a.maturity==='concept'&&(!v.architectureOptions.length||!v.unresolvedChoices.length))add('CONCEPT_ARCHITECTURE_CHOICES',`assets.${a.id}`,'Concepts need explicit options and unresolved choices so a picture does not select an architecture.');
 }
 for(const v of collectVisuals(project.slides))for(const mark of v.attachments??[]){
  const parent=project.assets.find(a=>a.id===v.assetId),child=project.assets.find(a=>a.id===mark.assetId);
  if(!parent||!child){add('ATTACHMENT_UNKNOWN','slides','Attachment parent/mark asset is missing.');continue;}
  if(mark.parentSha256!==parent.sha256||mark.assetSha256!==child.sha256)add('ATTACHMENT_STALE','slides','Attachment coordinates are bound to different source bytes.');
  if(mark.region.right<=mark.region.left||mark.region.bottom<=mark.region.top)add('ATTACHMENT_REGION','slides','Attachment region must have positive area.');
  if(mark.review.status!=='reviewed'||!mark.review.reviewer||Number.isNaN(Date.parse(mark.review.reviewedAt)))add('ATTACHMENT_REVIEW','slides','Attached hull/brand marks need a named, dated visual review before rendering.');
 }
 return result;
}

export function salesAudit(project:Project,compiled:CompiledDeck){
 const findings:ReviewFinding[]=[];
 if(!project.sales)return {status:'legacy-no-sales-audit',findings,visibleCopyHash:visibleCopyHash(compiled),humanApproval:false};
 for(const n of project.sales.narrative){const s=compiled.slides.find(s=>s.key===n.slideKey);if(!s)continue;
  const authored=project.slides.find(s=>s.key===n.slideKey)!;
  const headline=slideTitle(project,authored);
  if(['partner-relevance','company-advantage','opportunity'].includes(n.job)&&/^(?:scope|scoping|study|studies|workshop|requirements|evaluation plan|phase|workstream)\b/i.test(headline))findings.push({code:'PROCESS_BEFORE_PRIZE',severity:'revise',detail:'This sales chapter leads with development process rather than the business or customer outcome.',slideKeys:[n.slideKey]});
 }
 const emitted=compiled.slides.flatMap(s=>(s.copyBindings??[]).map(b=>{
  const authored=project.slides.find(a=>a.key===s.key)!;
  const fontSize=s.boxes.find(x=>x.objectId===b.objectId)?.fontSize??0;
  return {...b,fontSize,prominent:fontSize>=10&&isArgumentBlock(authored,b.blockId)};
 }));
 const coverage=project.opportunities.map(o=>({opportunityId:o.id,fields:Object.fromEntries([...CORE_SALES_FIELDS,...DETAIL_FIELDS].map(field=>[field,emitted.filter(b=>b.bindings.some(x=>x.opportunityId===o.id&&x.field===field)).map(b=>({slideKey:b.slideKey,objectId:b.objectId,blockId:b.blockId,placement:b.placement,fontSize:b.fontSize,prominent:b.prominent}))]))}));
 for(const row of coverage)for(const field of CORE_SALES_FIELDS)if(!(row.fields[field]??[]).some(x=>x.placement==='core'&&x.prominent))findings.push({code:'EMITTED_COVERAGE_MISSING',severity:'revise',detail:`${row.opportunityId}.${field} did not reach main core copy at a readable argument size. Status/caption/fine print is not the sales pitch.`,slideKeys:[]});
 for(const item of project.sales.sourceInventory.filter(i=>i.importance==='core')){
  const d=project.sales.sourceDisposition.find(d=>d.sourceItemId===item.id);
  if(d&&d.action!=='omit'&&!emitted.some(b=>d.destinationBlockIds.includes(b.blockId)&&b.placement==='core'&&b.prominent))findings.push({code:'EMITTED_SOURCE_BURIED',severity:'revise',detail:`${item.id} survives only outside the main visible argument.`,slideKeys:[]});
 }
 return {status:findings.some(f=>f.severity==='revise')?'revise':'requires-editorial-review',inputHash:compiled.inputHash,visibleCopyHash:visibleCopyHash(compiled),coverage,sourceDisposition:project.sales.sourceDisposition,findings,humanApproval:false,note:'Traceability and heuristics do not prove persuasion or factual meaning. A fresh reader must assess the visible copy.'};
}
