import type {Project,Slide,TalkTrack,ValidationIssue,CompiledDeck} from './types';
import {slideTitle,slideBlockClaims,notesBlocks} from './authoring';
const nonempty=(x:unknown)=>typeof x==='string'&&x.trim().length>0;
const text=(n:TalkTrack)=>[n.say,n.basis,n.guardrail,n.qa].filter(Boolean).join('\n');
export function talkTrackIssues(p:Project):ValidationIssue[]{
 const out:ValidationIssue[]=[],add=(code:string,path:string,message:string,severity:ValidationIssue['severity']='error')=>out.push({code,path,message,severity});
 if(p.meta.notesMode==='audit'&&p.meta.audience!=='internal')add('AUDIT_NOTES_PRIVATE','meta.notesMode','Audit notes are internal only; use a cleared talk track for any external audience.');
 for(const s of p.slides){const n=s.notes,path=`slides.${s.key}.notes`;
  if(typeof n==='string'){if(p.schemaVersion==='2.1.0'&&n.trim())add('TALK_TRACK_UNCLEARED',path,'Migrate legacy prose into an audience-reviewed talk track; do not automatically export it.',p.meta.audience==='internal'?'warning':'error');continue;}
  if(!n.clearedFor.includes(p.meta.audience))add('NOTES_AUDIENCE_UNCLEARED',path,'Speaker notes lack clearance for this audience.');
  if(!nonempty(n.review.reviewer)||Number.isNaN(Date.parse(n.review.reviewedAt))||!nonempty(n.review.reason))add('NOTES_REVIEW_MISSING',path,'Talk tracks require an explicit named, dated disclosure review.');
  if(p.meta.audience==='partner'&&(p.meta.recipientIds??[]).some(id=>!n.recipientIds.includes(id)))add('NOTES_RECIPIENT_UNCLEARED',path,'Speaker notes must be cleared for every intended recipient.');
  for(const id of n.claimIds){const c=p.claims.find(c=>c.id===id);if(!c)add('NOTES_REFERENCE',path,`Unknown claim ${id}`);else if(!c.clearedFor.includes(p.meta.audience))add('NOTES_CLAIM_UNCLEARED',path,`Claim ${id} is not cleared for this audience.`);}
  for(const id of n.sourceIds)if(!p.sources.some(v=>v.id===id))add('NOTES_REFERENCE',path,`Unknown source ${id}`);
  const all=text(n);
  if(p.meta.audience!=='internal'){
   if(/(?:\/tasklet\/|avfs:\/\/|tasklet:\/\/|\bBINDING\b|\bPRIVATE RELATIONSHIP\b)/i.test(all))add('NOTES_PRIVATE_LOCATOR',path,'Private working paths/binding dumps/relationship markers cannot be exported in notes.');
   for(const source of p.sources.filter(v=>v.visibility!=='public'))if(source.locator&&all.includes(source.locator))add('NOTES_PRIVATE_LOCATOR',path,'A private source locator appears in the talk track. Cite an approved public source or describe the basis without exposing it.');
   const ids=new Set([...n.sourceIds,...n.claimIds.flatMap(id=>p.claims.find(c=>c.id===id)?.sourceIds??[])]);
   for(const id of ids){const source=p.sources.find(v=>v.id===id);if(source&&source.visibility!=='public'&&(!source.clearedFor?.includes(p.meta.audience)||(p.meta.audience==='partner'&&(p.meta.recipientIds??[]).some(r=>!source.recipientIds?.includes(r)))))add('NOTES_SOURCE_UNCLEARED',path,'A non-public notes source is not cleared for all intended recipients.');}
  }
  if(all.split(/\s+/).filter(Boolean).length>(p.policy.editorial?.notesWordBudget??150))add('NOTES_DENSITY',path,'Talk track exceeds its advisory word budget; edit for usefulness without deleting a material guardrail.','warning');
 }
 return out;
}
/** Only audience-cleared authored prose is emitted. Full evidence stays in an external restricted manifest. */
export function renderTalkTrack(p:Project,s:Slide):string{
 const bad=talkTrackIssues(p).filter(i=>i.severity==='error'&&(i.path===`slides.${s.key}.notes`||i.path==='meta.notesMode'));
 if(bad.length)throw new Error(bad.map(i=>i.code+': '+i.message).join('; '));
 const n=s.notes,parts=[slideTitle(p,s)];
 if(typeof n==='string'){
  if(p.meta.audience==='internal')parts.push(n,...notesBlocks(p,s).map(b=>b.text));
 }else for(const [label,value]of [['SAY',n.say],['BASIS',n.basis],['GUARDRAIL',n.guardrail],['Q&A',n.qa]])if(value)parts.push(`${label}\n${value}`);
 if(p.meta.notesMode==='audit'&&p.meta.audience==='internal'){
  const ids=slideBlockClaims(p,s);parts.push('INTERNAL AUDIT\n'+p.claims.filter(c=>ids.includes(c.id)).map(c=>`${c.id} · ${c.evidenceClass}: ${c.basis}${c.limitations?' | '+c.limitations:''}`).join('\n'));
 }
 return parts.filter(Boolean).join('\n\n');
}
export function evidenceManifest(p:Project,c:CompiledDeck):string{
 return ['# Restricted evidence manifest','',`Input: ${c.inputHash}`,'','Internal working record — not partner speaker notes or a public source appendix. Do not publish this file with generic tooling.','',...p.slides.flatMap(s=>{
  const ids=new Set([...slideBlockClaims(p,s),...(typeof s.notes==='object'?s.notes.claimIds:[])]);
  return [`## ${s.key} — ${slideTitle(p,s)}`,...p.claims.filter(v=>ids.has(v.id)).flatMap(v=>[`### ${v.id} · ${v.evidenceClass}`,v.statement,`Basis: ${v.basis}`,`Limitations: ${v.limitations??'See source record.'}`,'```json',JSON.stringify({provenance:v.provenance,context:v.context,quantities:v.quantities,priceBasis:v.priceBasis,applicability:v.applicability,sourceIds:v.sourceIds},null,2),'```']), ''];
 }), '## Sources','```json',JSON.stringify(p.sources,null,2),'```','## Recipient continuity','```json',JSON.stringify(p.sales?.brief.companions??null,null,2),'```'].join('\n');
}
