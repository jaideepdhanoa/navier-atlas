import { readFile, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { resolve, join } from 'node:path';
const args=process.argv.slice(2),get=(n:string)=>args[args.indexOf(n)+1];
if(!args.includes('--out')||!args.includes('--reviewer')||!args.includes('--notes'))throw new Error('After inspecting all true PDF renders: bun -i scripts/record-review.ts --out /exports --reviewer "Reviewer" --notes "What was checked; any limitations"');
const out=resolve(get('--out')),m=JSON.parse(await readFile(join(out,'build-manifest.json'),'utf8'));
const hash=(b:Buffer)=>createHash('sha256').update(b).digest('hex');
const reviewed:any[]=[];
for(const report of m.reports){
 const pdf=await readFile(join(out,`${report.name}.pdf`));
 if(hash(pdf)!==report.pdfSha256)throw new Error('PDF changed since structural QA. Rebuild before review.');
 for(let p=1;p<=2;p++)for(const suffix of [`-${p}.png`,`-phone-${p}.png`]){
  const name=report.name+suffix;reviewed.push({file:name,sha256:hash(await readFile(join(out,name)))});
 }
}
const receipt={reviewedAt:new Date().toISOString(),reviewer:get('--reviewer'),notes:get('--notes'),status:'VISUALLY REVIEWED',buildConfigSha256:m.configSha256,pdfs:m.reports.map((r:any)=>({file:r.name+'.pdf',sha256:r.pdfSha256})),renders:reviewed,scope:'Records an actual reviewer inspection. Does not certify engineering performance, partner agreement or permission to publish.'};
await writeFile(join(out,'visual-review.json'),JSON.stringify(receipt,null,2));
console.log(JSON.stringify({out,status:receipt.status,reviewedRenderFiles:reviewed.length}));
