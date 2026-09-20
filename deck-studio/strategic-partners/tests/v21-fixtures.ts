import {readFile} from 'node:fs/promises';
import {join} from 'node:path';
import {repoRoot} from './v2-fixtures';
import type {Project,Claim,ClaimUse,OperatingContext} from '../src/types';
export const fixtureContext:OperatingContext={geography:'Fictional Coast',mission:'Fictional observation route',configuration:'Fixture hull A',asOf:'2000-01-01',conditions:[]};
export async function v21Fixture(source='research-network'):Promise<Project>{
 const p=JSON.parse(await readFile(join(repoRoot,'examples',source,'project.json'),'utf8')) as Project;
 p.schemaVersion='2.1.0';p.meta.recipientIds=['fixture-partner'];p.meta.notesMode='talk-track';
 p.sources.forEach(s=>s.kind='primary');
 p.claims.forEach(c=>Object.assign(c,{topic:'proposal',provenance:{subject:p.meta.company,reportedBy:'Fictional author',owner:'fictional'},context:structuredClone(fixtureContext),dependsOn:[]}));
 const use=(id:string):ClaimUse=>({claimId:id,framing:'fact',role:'market-context'});
 for(const b of p.sales!.blocks)b.claimUses=b.claimIds.map(use);
 for(const s of p.slides){s.claimUses=s.claimIds.map(use);s.notes={say:'Fictional talk track for this proposed service.',basis:'Synthetic fixture only.',guardrail:'No real performance, demand or approval is asserted.',qa:'Who would use the service?',claimIds:[],sourceIds:[],clearedFor:['internal','partner','public'],recipientIds:['fixture-partner'],review:{reviewer:'Fixture reviewer',reviewedAt:'2000-01-01T00:00:00Z',reason:'Synthetic audience-safe test copy.'}};}
 for(const n of p.sales!.narrative)n.support={kind:'mechanism',proposition:n.takeaway,whyItMatters:'Explains the fictional service and payment relationship.',claimIds:[],rationale:'Deliberately qualitative workflow fixture, not a numerical proof claim.'};
 p.sales!.brief.companions={status:'none',reason:'Fictional first-contact fixture.',documents:[],reconciliations:[]};
 p.sales!.brief.leverTransfer={status:'not-applicable',reason:'Qualitative fictional research-service model does not transfer a price or performance advantage.',claimIds:[],sourceIds:[],result:'not-applicable'};
 return p;
}
export function addQuantity(p:Project){
 const s=p.slides.find(s=>s.layout==='sales'&&s.composition==='mission-hero')!;
 if(s.layout!=='sales'||s.composition!=='mission-hero')throw Error('Missing fixture mission');
 const b=p.sales!.blocks.find(b=>b.id===s.benefits[0].body)!;
 // This test adds an evidence band, so use the tighter authored body variants.
 const short:Record<string,string>={'observation-mission-benefit-1-body':'Research teams buy a service contract and a clear data handoff.','observation-mission-benefit-2-body':'Shared continuity preserves scientific ownership.'};
 for(const [id,text]of Object.entries(short)){const block=p.sales!.blocks.find(v=>v.id===id);if(block){block.text=text;delete block.from;}}
 const c:Claim={id:'fixture-range',statement:'Fictional modeled range: 80 nmi for Fixture hull A.',evidenceClass:'modeled',sourceIds:[p.sources[0].id],basis:'Synthetic model; not measured and not a claim about any real product.',clearedFor:['internal','partner','public'],topic:'performance',provenance:{subject:p.meta.company,reportedBy:'Fictional engineering author',owner:'company'},context:structuredClone(fixtureContext),quantities:[{id:'range',metric:'route-range',value:80,unit:'nmi',statistic:'scenario'}],dependsOn:[],applicability:{mode:'same-context',target:structuredClone(fixtureContext),rationale:'Identical explicitly fictional model context.',sourceIds:[]}};
 p.claims.push(c);b.text='80 nmi range for Fixture hull A.';delete b.from;b.claimIds.push(c.id);
 b.claimUses!.push({claimId:c.id,framing:'modeled',role:'company-proof',qualification:{channel:'footnote',text:'MODELED',footnoteId:'range-note'}});
 b.quantityUses=[{claimId:c.id,quantityId:'range',display:'80 nmi'}];
 s.footnotes=[{id:'range-note',claimIds:[c.id],sourceIds:[],text:'MODELED · Fixture hull A. Synthetic design case, not a demonstrated result.'}];
 return {s,b,c,use:b.claimUses!.at(-1)!};
}
