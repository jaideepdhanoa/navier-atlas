import {readFile,readdir} from 'node:fs/promises';
import {validateProject} from '../src/validate';
import {compileProject} from '../src/render';
import {salesAudit} from '../src/authoring';
const root=new URL('../examples/',import.meta.url).pathname;
let failed=false;
for(const entry of await readdir(root,{withFileTypes:true})){
 if(!entry.isDirectory())continue;
 const path=root+entry.name+'/project.json';let project:any;try{project=JSON.parse(await readFile(path,'utf8'));}catch{continue;}
 if(project.schemaVersion!=='2.0.0')continue;
 const valid=await validateProject(project,{checkFiles:true,projectRoot:root+entry.name});
 try{const compiled=compileProject(project,{allowUnresolvedAssets:true});const audit=salesAudit(project,compiled);const errors=valid.issues.filter(i=>i.severity==='error');const findings=audit.findings.filter(i=>i.severity==='revise');failed||=errors.length>0||findings.length>0;console.log(JSON.stringify({name:entry.name,valid:valid.ok,slides:compiled.slides.length,opportunities:project.opportunities.length,errors,findings,releaseHolds:valid.issues.filter(i=>i.severity==='release-hold').length}));}
 catch(error){failed=true;console.log(JSON.stringify({name:entry.name,error:String(error)}));}
}
if(failed)process.exitCode=1;
