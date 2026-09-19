import { readFile } from 'node:fs/promises';
const [sourcePath,factPath]=process.argv.slice(2);
if(!sourcePath)throw new Error('Usage: bun -i scripts/check-sources.ts sources.json [facts.json]');
const data=JSON.parse(await readFile(sourcePath,'utf8')),rows=Array.isArray(data)?data:data.sources;
if(!Array.isArray(rows))throw new Error('sources must be an array');
const ids=new Set<string>(),urls=new Set<string>(),errors:string[]=[];
for(const r of rows){
 if(!r.id||ids.has(r.id))errors.push(`Missing/duplicate ID: ${r.id}`);ids.add(r.id);
 if(r.primary_citation===false)continue;
 if(!/^https?:\/\/[^\s;]+$/.test(r.url??''))errors.push(`Invalid single public URL: ${r.id}`);else urls.add(r.url);
 if(!/^\d{4}-\d{2}-\d{2}$/.test(r.access_date??''))errors.push(`Missing access date: ${r.id}`);
 if(r.publication_date&&!/^\d{4}-\d{2}-\d{2}$/.test(r.publication_date))errors.push(`Invalid publication date: ${r.id}`);
 if(r.visibility&&r.visibility!=='public')errors.push(`Non-public source: ${r.id}`);
}
if(data.unique_public_urls!==undefined&&data.unique_public_urls!==urls.size)errors.push('Declared unique primary-URL count differs from computed count');
let facts=0;
if(factPath){const f=JSON.parse(await readFile(factPath,'utf8'));for(const row of f.facts){facts++;for(const id of row.source_ids)if(!ids.has(id))errors.push(`Unresolved fact citation ${id}`);}}
console.log(JSON.stringify({sourceRecords:rows.length,primaryUniqueUrls:urls.size,facts,errors}));
if(errors.length)process.exit(1);
