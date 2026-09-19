import { cp, readFile, writeFile, stat } from 'node:fs/promises';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
const [slug,partner,destination]=process.argv.slice(2);
if(!slug||!partner||!destination||!/^[a-z0-9-]+$/.test(slug))throw new Error('Usage: bun -i scripts/init.ts partner-slug "Partner Name" /new/project/directory');
const out=resolve(destination);
try{await stat(out);throw new Error('Destination already exists; initializer will not overwrite it.');}catch(e:any){if(e.code!=='ENOENT')throw e;}
const source=fileURLToPath(new URL('../examples/public-demo/',import.meta.url));
await cp(source,out,{recursive:true});
const c=JSON.parse(await readFile(`${out}/content.json`,'utf8'));
c.meta.slug=`${slug}-two-pager`;c.meta.partner=partner;c.meta.title=`${partner} — Illustrative partner brief`;
await writeFile(`${out}/content.json`,JSON.stringify(c,null,2));
console.log(JSON.stringify({out,status:'ILLUSTRATIVE STARTER ONLY',next:'Replace example content, claim/source records, audience classification and images before external use.'}));
