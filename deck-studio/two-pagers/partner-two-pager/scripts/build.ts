import { chromium } from 'playwright';
import { readFile, writeFile, mkdir, mkdtemp, cp, readdir, rm, realpath, stat } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { dirname, resolve, join, extname, sep } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { tmpdir } from 'node:os';
import { execFileSync } from 'node:child_process';
import { validateBrief, safeLocalPath, scanText } from './model';
import { renderHtml } from './template';

const args=process.argv.slice(2), opt=(n:string)=>{const i=args.indexOf(n);return i>=0?args[i+1]:undefined;};
if(!opt('--config')||!opt('--out'))throw new Error('Usage: bun -i scripts/build.ts --config /path/content.json --out /path/exports');
const configPath=resolve(opt('--config')!),project=dirname(configPath),out=resolve(opt('--out')!);
const toolkit=resolve(dirname(fileURLToPath(import.meta.url)),'..');
if(project===out||project.startsWith(out+sep)||toolkit===out||toolkit.startsWith(out+sep))throw new Error('Output cannot be the source/toolkit folder or an ancestor of it.');
const raw=await readFile(configPath,'utf8'),c=validateBrief(JSON.parse(raw));
const hash=(data:string|Buffer)=>createHash('sha256').update(data).digest('hex');
const css=await readFile(join(toolkit,'templates/brief.css'),'utf8');
const stage=await mkdtemp(join(tmpdir(),'partner-brief-'));
await mkdir(join(stage,'assets')); await cp(join(toolkit,'fonts'),join(stage,'fonts'),{recursive:true});
const assetPaths=new Map<string,string>(),assetManifest:any[]=[];
const realProject=await realpath(project);
for(const a of c.assets){
 const source=safeLocalPath(project,a.path), physical=await realpath(source);
 if(source===out||source.startsWith(out+sep))throw new Error('Output would replace source assets.');
 if(!physical.startsWith(realProject+sep))throw new Error(`Asset symlink escapes project: ${a.id}`);
 const data=await readFile(source),extension=extname(a.path).toLowerCase();
 if(!['.jpg','.jpeg','.png','.webp','.svg'].includes(extension))throw new Error(`Unsupported asset type ${extension}`);
 if(extension==='.svg'){
  const svg=data.toString();
  if(/<script\b|<foreignObject\b|\bon\w+\s*=|@import|url\(\s*["']?(?!#)/i.test(svg))throw new Error(`Active SVG content: ${a.id}`);
  for(const match of svg.matchAll(/(?:href|src)\s*=\s*["']([^"']*)/gi))if(!/^(?:#|data:image\/(?:png|jpeg|webp);base64,)/.test(match[1]))throw new Error(`External SVG reference: ${a.id}`);
 }
 const dest=`assets/${a.id}${extension}`;await writeFile(join(stage,dest),data);assetPaths.set(a.id,dest);
 assetManifest.push({...a,sha256:hash(data),bytes:data.length,stagedPath:dest});
}
const launch:any={headless:true,args:['--no-sandbox','--allow-file-access-from-files']};
if(process.env.CHROME_BIN)launch.executablePath=process.env.CHROME_BIN;
const browser=await chromium.launch(launch);
const reports:any[]=[];const texts:string[]=[];const failedRequests:string[]=[];
try{
 for(const theme of ['dark','light'] as const){
  const name=`${c.meta.slug}-${theme}`,html=renderHtml(c,css,theme,assetPaths);
  await writeFile(join(stage,`${name}.html`),html);
  const page=await browser.newPage({viewport:{width:816,height:1056},deviceScaleFactor:1});
  await page.route('**/*',route=>{
   const url=route.request().url();
   if(/^(file:|data:|about:)/.test(url))return route.continue();
   failedRequests.push(url);return route.abort();
  });
  await page.emulateMedia({media:'print'});
  await page.goto(pathToFileURL(join(stage,`${name}.html`)).href,{waitUntil:'load'});
  await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode().catch(()=>undefined)));});
  const inspection=await page.evaluate(()=>{
   const pages=[...document.querySelectorAll<HTMLElement>('.page')];
   const errors:string[]=[];
   if(pages.length!==2)errors.push(`Expected two page elements, found ${pages.length}`);
   const boxes=pages.map((p,i)=>{
    const b=p.getBoundingClientRect(),body=p.querySelector<HTMLElement>('.body-area')!.getBoundingClientRect(),f=p.querySelector<HTMLElement>('.footer')!.getBoundingClientRect();
    if(Math.abs(b.width-816)>1||Math.abs(b.height-1056)>1)errors.push(`Page ${i+1}: not Letter CSS size`);
    if(body.bottom>f.top+.5)errors.push(`Page ${i+1}: body overlaps footer`);
    if(f.bottom>b.bottom+.5)errors.push(`Page ${i+1}: footer clipped by ${(f.bottom-b.bottom).toFixed(1)}px`);
    const walker=document.createTreeWalker(p,NodeFilter.SHOW_TEXT);
    let node:Node|null;
    while(node=walker.nextNode()){
     if(!node.textContent?.trim())continue;
     const range=document.createRange();range.selectNodeContents(node);
     for(const r of range.getClientRects()){
      if(r.top<b.top-1||r.bottom>b.bottom+1||r.left<b.left-1||r.right>b.right+1)errors.push(`Page ${i+1}: text outside page: ${node.textContent.slice(0,70)}`);
      let ancestor=node.parentElement;
      while(ancestor&&ancestor!==p){
       const style=getComputedStyle(ancestor);
       if(['hidden','clip'].includes(style.overflow)){
        const ar=ancestor.getBoundingClientRect();
        if(r.left<ar.left-1||r.right>ar.right+1||r.top<ar.top-1||r.bottom>ar.bottom+1)errors.push(`Page ${i+1}: clipped text: ${node.textContent.slice(0,70)}`);
       }
       ancestor=ancestor.parentElement;
      }
     }
    }
    const topSections=[...p.querySelector<HTMLElement>('.body-area')!.children].filter(x=>getComputedStyle(x).position!=='absolute');
    for(let j=1;j<topSections.length;j++){
     const prev=topSections[j-1].getBoundingClientRect(),next=topSections[j].getBoundingClientRect();
     if(next.top<prev.bottom-.5)errors.push(`Page ${i+1}: adjacent sections overlap`);
    }
    return {page:i+1,width:b.width,height:b.height,bodyBottom:body.bottom-b.top,footerTop:f.top-b.top,freeSpace:f.top-body.bottom};
   });
   const missing=[...document.images].filter(x=>!x.complete||x.naturalWidth===0).map(x=>x.getAttribute('src'));
   if(missing.length)errors.push(`Missing images: ${missing.join(', ')}`);
   const fontFamilies=[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family);
   for(const family of ['Inter','Playfair Display'])if(!fontFamilies.includes(family))errors.push(`Font not loaded: ${family}`);
   return {errors:[...new Set(errors)],boxes,images:document.images.length,fontFamilies:[...new Set(fontFamilies)],text:document.body.innerText};
  });
  const contentCheck=scanText(inspection.text,c);
  if(inspection.errors.length||contentCheck.issues.length)throw new Error(JSON.stringify({theme,geometry:inspection,contentCheck},null,2));
  const pdfPath=join(stage,`${name}.pdf`);
  await page.pdf({path:pdfPath,format:'Letter',printBackground:true,preferCSSPageSize:true,displayHeaderFooter:false,tagged:true});
  await page.close();
  const info=execFileSync('pdfinfo',[pdfPath],{encoding:'utf8'});
  if(!/^Pages:\s+2\s*$/m.test(info)||!/^Page size:\s+612 x 792 pts/m.test(info))throw new Error(`PDF page-count/Letter check failed: ${name}`);
  const pdfText=execFileSync('pdftotext',['-layout',pdfPath,'-'],{encoding:'utf8'}).replace(/\f/g,' ');
  const pdfCheck=scanText(pdfText,c);if(pdfCheck.issues.length)throw new Error(JSON.stringify({name,pdfCheck}));
  const fonts=execFileSync('pdffonts',[pdfPath],{encoding:'utf8'});
  if(fonts.split('\n').slice(2).filter(Boolean).some(line=>/\bno\s+(?:yes|no)\s+(?:yes|no)\s+\d+\s+\d+\s*$/.test(line)))throw new Error('Unembedded PDF font');
  execFileSync('pdftoppm',['-png','-r','160',pdfPath,join(stage,name)],{stdio:'pipe'});
  for(let i=1;i<=2;i++)execFileSync('magick',[join(stage,`${name}-${i}.png`),'-resize','400x',join(stage,`${name}-phone-${i}.png`)]);
  await writeFile(join(stage,`${name}.txt`),pdfText);
  texts.push(pdfText.replace(/\s+/g,' ').trim());
  reports.push({theme,name,geometry:inspection.boxes,images:inspection.images,fontFamilies:inspection.fontFamilies,wordCount:contentCheck.words,pdfExtractedWords:pdfCheck.words,contentScan:'CLEAN',pdfPages:2,pageSize:'Letter',fontEmbedding:'PASS',pdfSha256:hash(await readFile(pdfPath)),visualReview:'REQUIRED: inspect actual PDF and phone PNGs'});
 }
}finally{await browser.close();}
if(failedRequests.length)throw new Error(`External network resource attempted: ${failedRequests.join(', ')}`);
if(texts[0]!==texts[1])throw new Error('Dark/light PDF copy differs');
const buildSources=['scripts/build.ts','scripts/model.ts','scripts/template.ts','templates/brief.css'];
const sourceHashes:Record<string,string>={};for(const file of buildSources)sourceHashes[file]=hash(await readFile(join(toolkit,file)));
const fontHashes:Record<string,string>={};for(const file of await readdir(join(stage,'fonts')))fontHashes[file]=hash(await readFile(join(stage,'fonts',file)));
const manifest={version:1,builtAt:new Date().toISOString(),slug:c.meta.slug,classification:c.meta.classification,configSha256:hash(raw),sourceHashes,fontHashes,assets:assetManifest,reports,darkLightTextParity:'PASS',externalResourceRequests:0,visualReview:'PENDING',evidenceScope:'Structural checks and disclosure rules; not independent engineering validation or external-sharing approval.'};
await writeFile(join(stage,'build-manifest.json'),JSON.stringify(manifest,null,2));
await writeFile(join(stage,'source-content.json'),raw);
try{const old=await stat(out);if(!old.isDirectory())throw new Error('Output exists as a file');await cp(out,`${out}-archive-${new Date().toISOString().replace(/[:.]/g,'-')}`,{recursive:true,errorOnExist:true,force:false});await rm(out,{recursive:true});}catch(err:any){if(err.code!=='ENOENT')throw err;}
await mkdir(dirname(out),{recursive:true});await cp(stage,out,{recursive:true});
console.log(JSON.stringify({out,classification:c.meta.classification,pdfs:reports.map(x=>`${x.name}.pdf`),reports,copyParity:'PASS',manifest:join(out,'build-manifest.json')},null,2));
