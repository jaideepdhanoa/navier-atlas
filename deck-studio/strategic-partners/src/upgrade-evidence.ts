import {mkdir,readFile,writeFile,cp,access} from 'node:fs/promises';
import {dirname,resolve,join} from 'node:path';
import type {Project} from './types';
import {sha256} from './primitives';
/** A held authoring envelope, not a runnable project and never an evidence auto-fill. */
export async function upgradeEvidenceDraft(p:Project,sourcePath:string,out:string){
 if(!['2.0.0','2.1.0'].includes(p.schemaVersion))throw new Error('Evidence migration starts from a readable V2 project.');
 const root=resolve(out);try{await access(join(root,'v21-authoring-draft.json'));throw new Error('Refusing to overwrite an existing migration draft.');}catch(e){if((e as NodeJS.ErrnoException).code!=='ENOENT')throw e;}
 await mkdir(root,{recursive:true});
 const pending={status:'HELD',kind:'V21-EVIDENCE-DRAFT-NOT-A-PROJECT',sourceVersion:p.schemaVersion,sourceHash:sha256(p),originalProject:p,
  unresolved:{claimContext:p.claims.filter(c=>!c.provenance||!c.context||!c.topic||!c.dependsOn).map(c=>c.id),recipientGroups:p.meta.recipientIds??null,companionContinuity:p.sales?.brief.companions??null,leverTransfer:p.sales?.brief.leverTransfer??null,notes:p.slides.filter(s=>typeof s.notes==='string'&&s.notes.trim()).map(s=>s.key)},
  instructions:['No quantities, market basis, recipient permission, partner commitments or review approvals have been invented.','Author the missing records and exact visible claim/quantity bindings; keep credible models and concepts clearly framed.','Resolve previously shared documents by recipient and version; do not perpetuate prior mistakes.','Clear talk tracks separately; private notes are not automatically approved for partner export.','Create a new 2.1.0 project only after the two editorial rounds. Do not replay this draft over a live presentation.']};
 await writeFile(join(root,'source-project.json'),JSON.stringify(p,null,2)+'\n',{flag:'wx'});
 await writeFile(join(root,'v21-authoring-draft.json'),JSON.stringify(pending,null,2)+'\n',{flag:'wx'});
 for(const a of p.assets){const from=resolve(dirname(sourcePath),a.path),to=resolve(root,a.path);if(!to.startsWith(root+'/'))throw new Error('Unsafe asset path in migration.');await mkdir(dirname(to),{recursive:true});await cp(from,to,{errorOnExist:true,force:false});}
 await writeFile(join(root,'MIGRATION.md'),'# V2.1 evidence migration — HELD\n\nThe source project and assets are preserved. The authoring envelope is not compiler input. Complete claims, applicability, recipient continuity, note clearance and two editorial rounds before producing a separate review copy. No source or live deck was modified.\n',{flag:'wx'});
 return {status:'HELD',sourceHash:sha256(p),snapshot:join(root,'source-project.json'),draft:join(root,'v21-authoring-draft.json'),sourceUnchanged:true};
}
