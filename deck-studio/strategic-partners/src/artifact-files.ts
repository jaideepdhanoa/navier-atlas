import {readFile,realpath} from 'node:fs/promises';
import {resolve,isAbsolute,sep} from 'node:path';
import {createHash} from 'node:crypto';
import type {RenderArtifact,RenderReviewBundle} from './types';
export const byteHash=(bytes:Uint8Array)=>createHash('sha256').update(bytes).digest('hex');
/** Re-open exact local bytes; reject traversal, absolute paths and symlink escapes. */
export async function verifyRenderFiles(bundle:RenderReviewBundle,root:string):Promise<string[]>{
 const base=await realpath(resolve(root)),problems:string[]=[];
 const files:RenderArtifact[]=[bundle.pdf,...bundle.pages.flatMap(page=>[page.full,page.phone])];
 const seen=new Set<string>();
 for(const file of files){
  try{
   if(!file?.path||isAbsolute(file.path)||file.path.split(/[\\/]/).includes('..'))throw Error('unsafe relative path');
   if(seen.has(file.path))throw Error('duplicate artifact path');seen.add(file.path);
   const target=await realpath(resolve(base,file.path));
   if(!target.startsWith(base+sep))throw Error('artifact escapes review root');
   if(byteHash(await readFile(target))!==file.sha256)throw Error('byte hash changed');
  }catch(error){problems.push(`Render artifact ${file?.path??'(missing)'}: ${String(error)}`);}
 }
 return problems;
}
