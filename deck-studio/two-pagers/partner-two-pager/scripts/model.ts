import { z } from 'zod';
import { resolve, sep } from 'node:path';

const text = z.string().min(1).max(5000);
const date = z.string().regex(/^\d{4}-\d{2}-\d{2}$/);
const id = z.string().regex(/^[A-Za-z0-9_-]+$/);
const refs = z.array(id).min(1);
const rich = z.object({ text, claimIds: refs }).strict();
export const sourceSchema = z.object({
  id, title:text, locator:text, visibility:z.enum(['public','internal','restricted']), asOf:date,
}).strict();
const claim = z.object({
  id, statement:text, evidenceClass:z.enum(['measured','demonstrated','company-reported','reported','historical','preliminary','modeled','plan','proposed','illustrative']),
  sourceIds:refs, asOf:date, shareable:z.boolean(), basis:text,
}).strict();
const asset = z.object({
  id, path:text, kind:z.enum(['photograph','rendering','schematic','wordmark','map','placeholder']),
  description:text, source:text, visibility:z.enum(['public','internal','restricted']), reviewed:z.boolean(),
}).strict();
export const configSchema = z.object({
  schemaVersion:z.literal(1),
  meta:z.object({
    slug:id, title:text, company:text, partner:text, date, edition:text,
    classification:z.enum(['public-example','public','partner-confidential']),
    brandLine:text, footerLabel:text, contact:z.string().email(), storyUrl:z.string().url(),
  }).strict(),
  branding:z.object({logoAsset:id,mastheadAsset:id}).strict(),
  sources:z.array(sourceSchema).min(1), claims:z.array(claim).min(1), assets:z.array(asset).min(1),
  cover:z.object({
    headline:text, intro:rich, platformTitle:text, platformBody:rich,
    tilesKicker:text,
    tiles:z.array(z.object({asset:id,title:text,subtitle:text,position:z.string().regex(/^(?:100|[0-9]{1,2})% (?:100|[0-9]{1,2})%$/).optional()})).length(4),
    tileCaption:rich,
    tractionKicker:text,
    metrics:z.array(z.object({value:text,label:text,claimIds:refs})).min(3).max(6),
    tractionNote:rich,
    spotlight:z.object({kicker:text,title:text,body:rich,asset:id,imageCaption:text,
      stages:z.array(z.object({title:text,status:text,claimIds:refs})).length(3),
    }).strict(),
  }).strict(),
  partnership:z.object({
    kicker:text, headline:text, intro:rich,
    contributions:z.array(z.object({label:text,body:rich})).length(2),
    tracks:z.array(z.object({number:text,kicker:text,title:text,body:rich,value:text,start:text})).length(3),
    expansion:z.object({label:text,text}).strict(),
    ask:z.object({title:text,body:rich,steps:z.array(text).length(3)}).strict(),
    team:z.object({label:text,text}).strict(),
    citations:z.array(z.object({sourceId:id,label:text})).max(8),
  }).strict(),
  policy:z.object({
    requiredPhrases:z.array(text), forbiddenPatterns:z.array(text),
    maxWords:z.number().int().min(100).max(1500).default(1000),
  }).strict(),
}).strict();
export type Brief = z.infer<typeof configSchema>;
export function safeLocalPath(root:string, relative:string):string {
  if (/^[A-Za-z][A-Za-z0-9+.-]*:|^[/\\]/.test(relative)) throw new Error(`Asset path must be relative: ${relative}`);
  const full=resolve(root,relative), base=resolve(root);
  if(!full.startsWith(base+sep)) throw new Error(`Asset escapes project directory: ${relative}`);
  return full;
}
export function plain(s:string):string {
  return s.replace(/<br\s*\/?\s*>/gi,' ').replace(/<[^>]+>/g,'').replace(/&nbsp;/g,' ').replace(/&amp;/g,'&').replace(/\s+/g,' ').trim();
}
export function escape(s:string):string {
  return s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;').replaceAll("'",'&#39;');
}
export function richText(s:string):string {
  // Content is data, never executable HTML. Only four presentational tags survive.
  return escape(s).replace(/&lt;(\/?)(b|strong|em|i)&gt;/gi,'<$1$2>').replace(/&lt;br\s*\/?&gt;/gi,'<br>');
}
export function validateBrief(input:unknown):Brief {
  const c=configSchema.parse(input);
  const unique=(arr:{id:string}[],label:string)=>{if(new Set(arr.map(x=>x.id)).size!==arr.length)throw new Error(`Duplicate ${label} IDs`);};
  unique(c.sources,'source'); unique(c.claims,'claim'); unique(c.assets,'asset');
  const sources=new Map(c.sources.map(s=>[s.id,s])); const claims=new Map(c.claims.map(s=>[s.id,s]));
  const assetIds=new Set(c.assets.map(s=>s.id));
  for(const s of c.sources){
    if(s.visibility==='restricted')throw new Error(`Restricted source ${s.id}`);
    if(c.meta.classification!=='partner-confidential'&&s.visibility!=='public')throw new Error(`Internal source in public artifact: ${s.id}`);
    if(s.visibility==='public'&&!/^https?:\/\/[^\s]+$/.test(s.locator))throw new Error(`Public source needs an HTTP(S) locator: ${s.id}`);
  }
  for(const a of c.assets){
    safeLocalPath('/project',a.path);
    if(!a.reviewed || a.visibility==='restricted')throw new Error(`Unreviewed/restricted asset: ${a.id}`);
    if(c.meta.classification!=='partner-confidential'&&a.visibility!=='public')throw new Error(`Non-public asset in public artifact: ${a.id}`);
  }
  for(const cl of c.claims){
    if(!cl.shareable)throw new Error(`Claim not cleared for this audience: ${cl.id}`);
    for(const s of cl.sourceIds){
      const source=sources.get(s); if(!source)throw new Error(`Unknown source ${s} in ${cl.id}`);
      if(source.visibility==='restricted')throw new Error(`Restricted source ${s}`);
      if(c.meta.classification!=='partner-confidential'&&source.visibility!=='public')throw new Error(`Internal source in public artifact: ${s}`);
    }
  }
  const walk=(obj:any)=>{
    if(!obj||typeof obj!=='object')return;
    if(Array.isArray(obj)){obj.forEach(walk);return;}
    if(obj.claimIds) for(const ref of obj.claimIds) if(!claims.has(ref))throw new Error(`Unknown claim: ${ref}`);
    for(const [key,value] of Object.entries(obj)){
      if(['asset','logoAsset','mastheadAsset'].includes(key)&&!assetIds.has(String(value)))throw new Error(`Unknown asset: ${value}`);
      walk(value);
    }
  };
  walk(c.cover); walk(c.partnership); walk(c.branding);
  for(const cit of c.partnership.citations){const s=sources.get(cit.sourceId);if(!s||s.visibility!=='public'||!/^https:\/\//.test(s.locator))throw new Error(`Visible citation must be public HTTPS: ${cit.sourceId}`);}
  if(!/^https:\/\//.test(c.meta.storyUrl))throw new Error('Story URL must use HTTPS');
  return c;
}
export function scanText(text:string,c:Brief):{words:number,issues:string[]} {
  const normalized=plain(text),issues:string[]=[];
  const compact=(s:string)=>s.toLocaleLowerCase().replace(/\s+/g,'');
  for(const p of c.policy.requiredPhrases)if(!compact(normalized).includes(compact(p)))issues.push(`Missing required phrase: ${p}`);
  for(const p of c.policy.forbiddenPatterns)if(new RegExp(p,'iu').test(normalized))issues.push(`Forbidden content pattern: ${p}`);
  if(/\{\{[^}]*\}\}|\b(?:TODO|TBD|undefined|NaN)\b/.test(normalized))issues.push('Unresolved placeholder');
  const words=normalized.split(/\s+/).filter(Boolean).length;
  if(words>c.policy.maxWords)issues.push(`Word budget exceeded: ${words} > ${c.policy.maxWords}`);
  return {words,issues};
}
