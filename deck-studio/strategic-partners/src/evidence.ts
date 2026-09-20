import type {Project,Slide,Claim,ClaimUse,QuantityUse,ValidationIssue,OperatingContext} from './types';
import {blockIds,resolveBlock} from './authoring';
import {normalizeNumericDisplay} from './diagnostics';
import {talkTrackIssues} from './talk-track';
import {sha256} from './primitives';
const clean=(s:string)=>s.replace(/\s+/g,' ').trim().toLowerCase();
const nonempty=(x:unknown)=>typeof x==='string'&&x.trim().length>0;
const close=(a:number,b:number)=>Math.abs(a-b)<=1e-7*Math.max(1,Math.abs(a),Math.abs(b));
const displayPattern=(display:string)=>new RegExp('(?<![\\p{L}\\p{N}.,])'+display.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'(?![\\p{L}\\p{N}])','u');
export function contextKey(c:OperatingContext){return sha256({...c,conditions:[...c.conditions].map(({key,value,unit})=>({key,value,unit})).sort((a,b)=>a.key.localeCompare(b.key))});}
export function approvedException(p:Project,code:string,path:string,term?:string){return p.policy.approvedExceptions?.some(e=>e.code===code&&e.path===path&&(code!=='FORBIDDEN_CONTENT'||e.term===term)&&e.reviewer.trim()&&e.reason.trim()&&!Number.isNaN(Date.parse(e.reviewedAt)))??false;}
export function authoredTexts(p:Project,s:Slide):string[]{
 if(s.layout==='sales')return blockIds(s).map(id=>resolveBlock(p,id).text);
 const skip=new Set(['key','layout','notes','claimIds','sourceIds','opportunityIds','claimUses','quantityUses','footnotes','assetId','attachments']);
 const walk=(v:any):string[]=>typeof v==='string'?[v]:Array.isArray(v)?v.flatMap(walk):v&&typeof v==='object'?Object.entries(v).filter(([k])=>!skip.has(k)).flatMap(([,v])=>walk(v)):[];
 return walk(s);
}
export function usesForSlide(p:Project,s:Slide){return [
 {path:`slides.${s.key}`,text:[...authoredTexts(p,s),...(s.footnotes??[]).map(f=>f.text)].join('\n'),claimIds:s.claimIds,uses:s.claimUses??[],quantities:s.quantityUses??[]},
 ...blockIds(s).map(id=>{const b=resolveBlock(p,id);return {path:`sales.blocks.${id}`,text:b.text,claimIds:b.block.claimIds,uses:b.block.claimUses??[],quantities:b.block.quantityUses??[]};})
 ];}
function unitVisible(text:string,unit:string){
 const aliases:Record<string,string[]>= {'%':['%','percent'],'nmi':['nmi','nm','nautical miles'],'kn':['kn','kt','knots'],'h':['h','hr','hours'],'count':[''],'ratio':['','×','x'],'kWh':['kwh']};
 const word=(u:string)=>{if(!u)return true;if(/^[^\p{L}\p{N}]+$/u.test(u))return text.includes(u);const escaped=clean(u).replace(/[.*+?^${}()|[\]\\]/g,'\\$&').replace(/ /g,'\\s+');return new RegExp(`(?:^|[^\\p{L}])${escaped}(?=$|[^\\p{L}\\p{N}])`,'iu').test(clean(text));};
 const [currency,...denominator]=unit.split('/');
 const symbols:Record<string,string[]>={USD:['$','usd'],EUR:['€','eur'],GBP:['£','gbp'],AED:['aed'],SAR:['sar']};
 if(symbols[currency]){if(!symbols[currency].some(word))return false;if(!denominator.length)return true;const suffix=denominator.join('/');return /\/|\bper\b/i.test(text)&&(aliases[suffix]??[suffix]).some(word);}
 return (aliases[unit]??[unit]).some(word);
}
function quantitativeTokens(text:string){return normalizeNumericDisplay(text.replace(/https?:\/\/\S+/g,'').replace(/\b\d{4}-\d{2}-\d{2}\b/g,'').replace(/\b(?:N|AW|R|V)\d+(?:[-.]\d+)*\b/gi,''));}
const framingPattern:Record<string,RegExp>={modeled:/\b(model(?:ed|led)?|scenario|estimate)\b/i,target:/\b(target|in[- ]design|design)\b/i,record:/\brecord\b/i,precedent:/\b(precedent|third[- ]party)\b/i,placeholder:/\bplaceholder\b/i,proposal:/\b(propos(?:ed|al)|concept|planned|future|in[- ]design|exploratory|intended)\b/i};
function requiredFraming(c:Claim):string|undefined{
 if(c.replacementPlan)return 'placeholder';
 if(c.provenance?.owner==='third-party')return 'precedent';
 if(c.quantities?.some(q=>q.statistic==='record'))return 'record';
 if(c.evidenceClass==='modeled')return 'modeled';
 if(['target','in-design'].includes(c.evidenceClass))return 'target';
 if(['proposed','planned','preliminary'].includes(c.evidenceClass))return 'proposal';
 return undefined;
}
/** Explicit record checks, not an assertion that software can prove meaning or factual truth. */
export function evidenceIssues(p:Project):ValidationIssue[]{
 if(p.schemaVersion!=='2.1.0')return [...talkTrackIssues(p),{severity:'warning',code:'EVIDENCE_UPGRADE_AVAILABLE',path:'schemaVersion',message:'Legacy input remains readable. Use the held V2.1 migration before claiming the new evidence/continuity checks are complete.'}];
 const out:ValidationIssue[]=[],add=(code:string,path:string,message:string,severity:ValidationIssue['severity']='error')=>{if(severity==='warning'&&approvedException(p,code,path))return;out.push({code,path,message,severity});};
 const claims=new Map(p.claims.map(c=>[c.id,c])),sources=new Map(p.sources.map(s=>[s.id,s]));
 const ref=(ids:string[],known:Map<string,unknown>,path:string)=>ids.forEach(id=>{if(!known.has(id))add('EVIDENCE_REFERENCE',path,`Unknown reference ${id}`);});
 const recipients=p.meta.recipientIds??[];
 if(p.meta.audience==='partner'&&!recipients.length)add('RECIPIENTS_REQUIRED','meta.recipientIds','Name the intended recipient groups; one partner audience flag is insufficient.');
 const used=new Set<string>();for(const s of p.slides){for(const row of usesForSlide(p,s)){row.claimIds.forEach(id=>used.add(id));row.uses.forEach(u=>used.add(u.claimId));row.quantities.forEach(u=>used.add(u.claimId));}for(const f of s.footnotes??[])f.claimIds.forEach(id=>used.add(id));if(typeof s.notes==='object')s.notes.claimIds.forEach(id=>used.add(id));}
 for(const id of used){const c=claims.get(id),path=`claims.${id}`;if(!c){add('EVIDENCE_REFERENCE',path,'Unknown used claim.');continue;}
  ref(c.sourceIds,sources,path);if(!c.sourceIds.length||!c.basis.trim())add('CLAIM_SUPPORT_REQUIRED',path,'A consequential claim requires sources and a basis.');if(!c.clearedFor.includes(p.meta.audience))add('CLAIM_AUDIENCE_UNCLEARED',path,'Claim is not cleared for the target audience.');
  if(!c.topic||!c.provenance||!c.context||!c.dependsOn){add('CLAIM_CONTEXT_REQUIRED',path,'V2.1 claims require topic, subject/reporter/owner, operating context and an explicit dependency list.');continue;}
  if(c.provenance.owner==='fictional'&&!p.meta.fictional)add('FICTIONAL_PROOF',path,'Fictional evidence cannot support a real partner deck.');
  for(const sid of c.sourceIds){const source=sources.get(sid);if(!source)continue;if(!source.kind)add('SOURCE_KIND_REQUIRED',`sources.${sid}`,'Classify each used source as primary or secondary.');
   if(p.meta.audience!=='internal'&&source.visibility!=='public'&&(!source.clearedFor?.includes(p.meta.audience)||(p.meta.audience==='partner'&&recipients.some(r=>!source.recipientIds?.includes(r)))))add('SOURCE_RECIPIENT_UNCLEARED',path,'Private source material is not approved for all intended recipients. Prior possession by another party is not authorization.');
  }
  if(c.topic==='entity-capability'&&!c.sourceIds.some(sid=>sources.get(sid)?.kind==='primary'))add('PRIMARY_SOURCE_REQUIRED',path,'Entity ownership/capability assertions require an appropriate primary source.');
  if(p.meta.audience==='partner'&&c.sourceIds.some(sid=>sources.get(sid)?.visibility!=='public')&&recipients.some(r=>!c.recipientIds?.includes(r)))add('CLAIM_RECIPIENT_UNCLEARED',path,'A claim based on private material needs recipient-specific approval.');
  const qs=c.quantities??[];if(new Set(qs.map(q=>q.id)).size!==qs.length)add('QUANTITY_ID_DUPLICATE',path,'Quantity IDs must be unique within a claim.');
  for(const q of qs){if(typeof q.value!=='number'&&q.value.min>q.value.max)add('QUANTITY_RANGE',path,'Range minimum exceeds maximum.');if(['target','scenario'].includes(q.statistic)&&['measured','tested','demonstrated'].includes(c.evidenceClass))add('FALSE_READINESS',path,'A target/scenario quantity cannot be labeled as a measured or tested result.');}
  for(const dep of c.dependsOn)if(!c.context.conditions.some(v=>v.key===dep))add('DEPENDENCY_MISSING',path,`Missing structured operating assumption: ${dep}`);
  for(const condition of c.context.conditions)if(typeof condition.value==='number'&&(!normalizeNumericDisplay(condition.display).some(v=>close(v,Number(condition.value)))||!unitVisible(condition.display,condition.unit)))add('CONDITION_DISPLAY_MISMATCH',path,`Display does not match the value/unit of ${condition.key}.`);
  if(qs.some(q=>/[$€£]|\b(?:USD|AED|SAR|EUR|GBP)\b/i.test(q.unit))&&!c.priceBasis)add('PRICE_BASIS_REQUIRED',path,'Currency quantities need category, currency, market, date and relevant rates; revenue is not a fuel tariff.');
  if(c.priceBasis){for(const q of qs){const currency=q.unit.match(/\b(USD|AED|SAR|EUR|GBP)\b/)?.[1];if(currency&&currency!==c.priceBasis.currency)add('PRICE_CURRENCY_MISMATCH',path,'The quoted unit and price-basis currency disagree.');if(c.priceBasis.category==='service-price'&&/\/(kg|ton|t|mile|nmi)\b/.test(q.unit))for(const dep of ['distance','payload','frequency'])if(!c.dependsOn.includes(dep))add('DEPENDENCY_MISSING',path,`Unit service economics require ${dep}, or do not present a point price.`);}
  if(c.priceBasis.geography!==c.context.geography&&c.applicability?.mode!=='supported-transfer')add('PRICE_BASIS_MISMATCH',path,'Price geography differs from the stated measurement/market context without a supported recalculation.');ref(c.priceBasis.rates.flatMap(r=>r.sourceIds),sources,path);}
  if(qs.length&&!c.applicability)add('APPLICABILITY_REQUIRED',path,'Numeric evidence needs an explicit same-context, supported-transfer, benchmark or unresolved assessment.');
  const a=c.applicability;
  if(a){ref(a.sourceIds,sources,path);if(a.mode==='same-context'&&contextKey(c.context)!==contextKey(a.target))add('CONTEXT_TRANSFER_MISMATCH',path,'A ratio, price or result cannot silently change geography, hull, mission or operating conditions.');if(a.mode==='supported-transfer'&&!a.sourceIds.length)add('TRANSFER_SUPPORT_REQUIRED',path,'A supported transfer/recalculation requires evidence, not only an assertion.');if(c.priceBasis&&a.mode==='supported-transfer'&&c.priceBasis.geography!==a.target.geography)add('PRICE_BASIS_MISMATCH',path,'Recalculated economics must use the target market price basis.');}
  if(c.replacementPlan&&!p.sales?.brief.unresolvedQuestions.includes(c.replacementPlan.question))add('REPLACEMENT_QUESTION_MISSING',path,'The replacement question must appear in the brief, with its owner retained in the claim.');
 }
 for(const s of p.slides){const path=`slides.${s.key}`,rows=usesForSlide(p,s),face=authoredTexts(p,s).join('\n'),allFace=face+'\n'+(s.footnotes??[]).map(f=>f.text).join('\n');
  if(s.footnotes?.length&&s.layout!=='sales')add('FOOTNOTE_LAYOUT',path,'The evidence band is reserved only in registered sales compositions. Use an inline qualification for a legacy/cover slide.');
  const fns=new Map((s.footnotes??[]).map(f=>[f.id,f]));if(fns.size!==(s.footnotes??[]).length)add('FOOTNOTE_ID_DUPLICATE',path,'Footnote IDs must be unique on a slide.');
  if((s.footnotes??[]).map(f=>f.text).join('  •  ').length>240)add('FOOTNOTE_BUDGET',path,'Claim-linked evidence band is limited to 240 characters. Move detail to the evidence manifest or split the slide; never hide essential context.');
  for(const f of s.footnotes??[]){ref(f.claimIds,claims,path);ref(f.sourceIds,sources,path);if(p.meta.audience!=='internal'&&(f.sourceIds.some(id=>sources.get(id)?.visibility!=='public')||/\/tasklet\/|avfs:\/\/|tasklet:\/\//.test(f.text)))add('FOOTNOTE_DISCLOSURE',path,'Visible footnotes may not expose private working sources/locators.');}
  let unboundFace=allFace;const slideUseIds=new Set(rows.flatMap(r=>r.uses.map(u=>u.claimId)));
  for(const f of s.footnotes??[])if(f.claimIds.some(id=>!slideUseIds.has(id)))add('FOOTNOTE_UNBOUND_CLAIM',path,'A footnote must qualify a claim directly bound on this slide; it cannot add unreviewed evidence on its own.');
  for(const row of rows){ref(row.claimIds,claims,row.path);for(const id of row.claimIds)if(!row.uses.some(u=>u.claimId===id))add('CLAIM_USE_REQUIRED',row.path,`Bind ${id} to a framing and use; slide/opportunity-wide citations do not establish the meaning of visible copy.`);
   for(const u of row.uses){const c=claims.get(u.claimId);if(!c){add('EVIDENCE_REFERENCE',row.path,'Unknown claim use.');continue;}if(!row.claimIds.includes(c.id))add('USE_WITHOUT_CLAIM',row.path,'Claim use must also be bound in claimIds.');
    const expected=requiredFraming(c);if(expected&&u.framing!==expected)add('CLAIM_FRAMING_MISMATCH',row.path,`${c.id} must be framed as ${expected}, not ${u.framing}.`);
    const q=u.qualification;let qualified='';
    if(q){if(q.channel==='inline'){if(!row.text.includes(q.text))add('QUALIFICATION_NOT_VISIBLE',row.path,'Inline qualification must occur in the actual visible copy.');else qualified=q.text;}else{const f=fns.get(q.footnoteId??'');if(!f||!f.claimIds.includes(c.id)||!f.text.includes(q.text))add('QUALIFICATION_NOT_VISIBLE',row.path,'Footnote qualification must exist, name this claim, and contain the authored qualification.');else qualified=f.text;}}
    if(expected&&(!q||!framingPattern[expected]?.test(qualified)))add('VISIBLE_QUALIFIER',row.path,`The ${expected} claim needs a claim-linked visible qualifier. A blanket status or hidden note is insufficient.`);
    if(c.evidenceClass==='modeled'&&!framingPattern.modeled.test(qualified))add('MODEL_QUALIFIER_MISSING',row.path,'Modeled third-party or record claims still need their model status visible.');
    if(c.quantities?.some(q=>q.statistic==='record')&&!framingPattern.record.test(qualified))add('RECORD_QUALIFIER_MISSING',row.path,'A record must be explicitly qualified as a record even when it is a precedent.');
    if(c.topic==='performance'&&(c.quantities?.length??0)>0&&c.context&&!allFace.includes(c.context.configuration))add('PERFORMANCE_CONFIG_NOT_VISIBLE',row.path,'The tested/modeled hull or configuration must remain visible with performance figures.');
    if(c.applicability?.mode==='benchmark'&&c.context&&!allFace.includes(c.priceBasis?.geography??c.context.geography))add('BENCHMARK_BASIS_NOT_VISIBLE',row.path,'A non-local benchmark must identify its actual source market on the face.');
    if(expected==='precedent'&&(!qualified.includes(c.provenance?.subject??'___')||!/(not ours|third[- ]party|precedent)/i.test(qualified)))add('PRECEDENT_ATTRIBUTION',row.path,'Name the third-party subject in its qualification; do not imply the result belongs to the company.');
    if(c.applicability?.mode==='benchmark'&&!['benchmark','historical'].includes(u.role))add('BENCHMARK_AS_PARTNER_RESULT',row.path,'A non-local benchmark must not be represented as partner economics or company proof.');
    if(c.applicability?.mode==='unresolved'&&u.role==='partner-result')add('UNRESOLVED_APPLICABILITY',row.path,'An unresolved transfer cannot be sold as the partner result.');
    if(c.replacementPlan&&p.meta.audience!=='internal'&&!c.replacementPlan.partnerVisibleApproval)add('PLACEHOLDER_EXTERNAL_HOLD',row.path,'Partner-visible placeholders require explicit approval and their actual basis; default them to the questionnaire.');
    for(const cond of c.context?.conditions??[])if(cond.material){if(!allFace.includes(cond.display))add('MATERIAL_BASIS_NOT_VISIBLE',row.path,`Keep the material ${cond.key} basis visible: ${cond.display}`);unboundFace=unboundFace.split(cond.display).join('');}
   }
   for(const u of row.quantities){const c=claims.get(u.claimId),q=c?.quantities?.find(q=>q.id===u.quantityId);if(!q){add('QUANTITY_REFERENCE',row.path,'Unknown claim quantity.');continue;}
    if(!row.uses.some(v=>v.claimId===u.claimId))add('QUANTITY_USE_WITHOUT_CLAIM_USE',row.path,'A numerical use requires its own claim framing.');
    if(!displayPattern(u.display).test(row.text))add('QUANTITY_NOT_VISIBLE',row.path,'The exact bound display is absent from actual copy.');
    const got=normalizeNumericDisplay(u.display),want=typeof q.value==='number'?[q.value]:[q.value.min,q.value.max];
    if(got.length!==want.length||got.some((v,i)=>!close(v,want[i])))add('QUANTITY_DISPLAY_MISMATCH',row.path,'Visible number disagrees with its structured quantity.');
    if(!unitVisible(u.display,q.unit))add('QUANTITY_UNIT_MISSING',row.path,'The quantity unit must be visible with the number.');unboundFace=unboundFace.replace(displayPattern(u.display),'');
   }
  }
  for(const f of s.footnotes??[])for(const id of f.sourceIds){const date=sources.get(id)?.asOf;if(date)unboundFace=unboundFace.replace(displayPattern(date.slice(0,4)),'');}
  const unbound=quantitativeTokens(unboundFace);
  if(unbound.length)add('UNBOUND_NUMBER',path,'Visible numerals have no explicit quantity/operating-basis binding: '+[...new Set(unbound)].join(', '));
  const precedents=[...slideUseIds].filter(id=>claims.get(id)?.provenance?.owner==='third-party');if(precedents.length>(p.policy.editorial?.maxPrecedents??1))add('PRECEDENT_DENSITY',path,'Multiple third-party precedents need a deliberate comparison/relevance review. This is not an unconditional ban.','warning');
  const hedges=(face.match(/\b(?:proposed|illustrative|preliminary|indicative|potential|could|might|may|subject to)\b/gi)??[]).length;if(hedges>(p.policy.editorial?.maxHedgeTokens??6))add('HEDGE_DENSITY',path,'Repeated qualification is crowding the proposition. Consolidate without deleting material meaning.','warning');
  const n=p.sales?.narrative.find(n=>n.slideKey===s.key);if(!n?.support)add('SPECIFICITY_REVIEW',path,'State the checkable proposition/mechanism/proposal and why it matters; do not add a decorative number.','release-hold');else{ref(n.support.claimIds,claims,path);if(n.support.kind==='evidence'&&!n.support.claimIds.some(id=>slideUseIds.has(id)))add('SPECIFICITY_REVIEW',path,'Evidence support must bind a claim used on this slide.','release-hold');}
 }
 const companions=p.sales?.brief.companions;
 if(!companions)add('COMPANION_INTAKE_REQUIRED','sales.brief','Record the versioned documents each recipient holds, or an explicit none/unknown status.');
 else{
  if(companions.status==='unknown')add('COMPANION_CONTINUITY_UNKNOWN','sales.brief.companions','Resolve prior-document access/continuity before external release.','release-hold');
  if(companions.status==='none'&&companions.documents.length)add('COMPANION_STATUS_CONFLICT','sales.brief.companions','Cannot declare no companion documents while listing held documents.');
  const docs=new Map(companions.documents.map(d=>[d.id,d]));if(docs.size!==companions.documents.length)add('COMPANION_DUPLICATE','sales.brief.companions','Companion document IDs must be unique.');
  for(const d of companions.documents){ref([d.sourceId],sources,'sales.brief.companions');ref(d.claimIds,claims,'sales.brief.companions');if(d.heldBy.some(id=>recipients.includes(id)))for(const id of d.claimIds){const rs=companions.reconciliations.filter(r=>r.documentId===d.id&&r.priorClaimId===id);if(rs.length!==1)add('COMPANION_RECONCILIATION_REQUIRED','sales.brief.companions',`Disposition ${d.id}/${id} exactly once for the intended recipient.`);}}
  for(const r of companions.reconciliations){const d=docs.get(r.documentId);if(!d||!d.claimIds.includes(r.priorClaimId))add('COMPANION_REFERENCE','sales.brief.companions','Reconciliation must point to a claim in that document.');ref(r.currentClaimIds,claims,'sales.brief.companions');ref(r.sourceIds,sources,'sales.brief.companions');if(r.status==='unresolved'&&d?.heldBy.some(id=>recipients.includes(id)))add('COMPANION_CONTRADICTION','sales.brief.companions','An unresolved material contradiction holds this recipient version.');if(['updated','corrected'].includes(r.action)&&(!r.sourceIds.length||!r.currentClaimIds.length))add('COMPANION_CORRECTION_BASIS','sales.brief.companions','Updates/corrections require a replacement claim and evidence.');if(['retained','updated','corrected'].includes(r.action)&&!r.currentClaimIds.some(id=>used.has(id)))add('COMPANION_DESTINATION','sales.brief.companions','A retained/updated/corrected claim needs a rendered or cleared-notes destination.');if(r.action==='notes-only'&&!r.currentClaimIds.some(id=>p.slides.some(s=>typeof s.notes==='object'&&s.notes.claimIds.includes(id))))add('COMPANION_DESTINATION','sales.brief.companions','Notes-only must actually bind to a cleared authored talk track.');if(r.action==='retained'){const prior=claims.get(r.priorClaimId);for(const id of r.currentClaimIds){const current=claims.get(id);if(prior?.context&&current?.context&&contextKey(prior.context)===contextKey(current.context))for(const q of prior.quantities??[]){const now=current.quantities?.find(v=>v.metric===q.metric&&v.unit===q.unit&&v.statistic===q.statistic);if(now&&JSON.stringify(now.value)!==JSON.stringify(q.value))add('COMPANION_FALSE_RETAINED','sales.brief.companions','A changed quantity cannot be marked retained; reconcile it as an evidenced update/correction.');}}}}
 }
 const lever=p.sales?.brief.leverTransfer;
 if(!lever)add('LEVER_REVIEW_REQUIRED','sales.brief.leverTransfer','Record whether the thesis relies on a transferable advantage; not-applicable with a reason is valid.');
 else{ref(lever.claimIds,claims,'sales.brief.leverTransfer');ref(lever.sourceIds,sources,'sales.brief.leverTransfer');const relying=p.claims.filter(c=>used.has(c.id)&&c.applicability?.mode==='supported-transfer');if(relying.length&&lever.status!=='assessed')add('LEVER_TRANSFER_UNASSESSED','sales.brief.leverTransfer','The argument uses transferred economics/performance without an assessed lever.');if(relying.some(c=>!lever.claimIds.includes(c.id)))add('LEVER_TRANSFER_COVERAGE','sales.brief.leverTransfer','Every transferred headline lever must be covered in the review.');if(lever.result==='reframed'&&!nonempty(lever.reframe))add('LEVER_REFRAME_REQUIRED','sales.brief.leverTransfer','Record the capability/operations reframe when the price advantage does not survive.');if(lever.status==='unresolved')add('LEVER_TRANSFER_HELD','sales.brief.leverTransfer','Resolve the thesis-relevant lever or reframe before release.','release-hold');}
 out.push(...talkTrackIssues(p));return out;
}
