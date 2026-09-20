import {mkdir,writeFile,cp} from 'node:fs/promises';
import {join,dirname,resolve} from 'node:path';
import {v21Fixture,addQuantity} from '../tests/v21-fixtures';
import {validateProject} from '../src/validate';
/** Fictional contract/render fixture only. Not a commercial template or verified claim. */
const root=resolve(dirname(import.meta.path),'..');
const p=await v21Fixture('energy-infrastructure');
p.meta.projectId='fictional_evidence_continuity';p.meta.title='Fictional V2.1 evidence and continuity fixture';
p.meta.footer='FICTIONAL WORKFLOW TEST — NOT FOR CIRCULATION';
p.meta.company='Tideframe'; // Short display name for the fictional cover; no real identity implied.
const caption=(v:any)=>{if(!v||typeof v!=='object')return;if(typeof v.assetId==='string'&&typeof v.caption==='string')v.caption='Fictional concept · not a deployed product.';for(const child of Object.values(v))if(child&&typeof child==='object')Array.isArray(child)?child.forEach(caption):caption(child);};
p.slides.forEach(caption);
const cover=p.slides.find(s=>s.layout==='cover');
if(cover?.layout==='cover'){cover.title='Coastal capacity,\nmade useful';cover.subtitle='A fictional portfolio\nfor an energy partner.';}
// Authored short-copy variants exercise the evidence-band layouts, not font shrinking.
const concise:Record<string,string>={
 'platform-banner':'One operating layer for coastal services',
 'platform-physical-0-body':'Coordinate vessel and crew handoffs.',
 'platform-physical-1-body':'Schedule cutoffs and handle exceptions.',
 'platform-physical-2-body':'Specify interfaces before production.',
 'platform-physical-3-body':'Separate power, compute and site roles.',
 'platform-ownership':'Tideframe develops the service; Asteris supplies local context.',
 'platform-software':'Shared scheduling connects customers, assets and operators.',
 'platform-revenue':'Separate customers. Explicit contracts and payment paths.',
 'production-value-benefit-0-body':'Common interfaces become a product that local facilities can evaluate.',
 'cargo-mission-benefit-1-body':'Shippers and depots buy a clearly bounded cargo service.',
 'cargo-mission-benefit-2-body':'One lane can become a repeatable coastal network.',
 'service-scale-benefit-1-body':'A recurring service can grow across adjacent partner markets.',
 'close-intro':'A portfolio to build together.'
};
for(const [id,text]of Object.entries(concise)){const b=p.sales!.blocks.find(b=>b.id===id);if(!b)throw Error('Missing authored fixture block '+id);b.text=text;delete b.from;}
for(const s of p.slides)if(s.layout==='sales')s.footnotes=[{id:'fixture-note',claimIds:[p.claims[0].id],sourceIds:[],text:'FICTIONAL WORKFLOW EXAMPLE · This page tests claim-linked notes and native spacing. No performance, economics, rights, customer commitment or operating approval is established by this synthetic material.'}];
const {c,s}=addQuantity(p);
s.footnotes![0].text='MODELED · Fixture hull A. Fictional design case, not a demonstrated result or partner operating promise. This illustration tests a bounded number, a visible evidence band and an audience-cleared talk track.';
const prior=structuredClone(c);prior.id='fixture-prior-range';prior.statement='Prior fictional range scenario, replaced by the current fictional design case.';prior.quantities![0].value=70;p.claims.push(prior);
p.sales!.brief.companions={status:'reviewed',reason:'Invented prior-document history exercises correction handling; no actual recipient document is asserted.',documents:[{id:'fictional-prior-proposal',sourceId:p.sources[0].id,version:'fictional-r0',asOf:'2000-01-01',heldBy:['fixture-partner'],claimIds:[prior.id]}],reconciliations:[{documentId:'fictional-prior-proposal',priorClaimId:prior.id,currentClaimIds:[c.id],action:'corrected',reason:'Explicit fictional correction; do not silently retain a changed quantity.',status:'resolved',sourceIds:[p.sources[0].id],owner:'Fictional author',reviewedAt:'2000-01-01T00:00:00Z'}]};
const checked=await validateProject(p);if(!checked.ok)throw Error(JSON.stringify(checked.issues.filter(i=>i.severity==='error')));
const out=join(root,'examples/evidence-continuity');await mkdir(out,{recursive:true});await cp(join(root,'examples/energy-infrastructure/assets'),join(out,'assets'),{recursive:true});
await writeFile(join(out,'project.json'),JSON.stringify(p,null,2)+'\n');
console.log(JSON.stringify({status:'fictional-fixture-only',slides:p.slides.length,out}));
