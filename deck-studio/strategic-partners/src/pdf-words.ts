import type {PdfWords} from './diagnostics';
const decode=(s:string)=>s.replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"').replace(/&#39;/g,"'").replace(/&#(\d+);/g,(_,n)=>String.fromCodePoint(Number(n)));
/** Poppler bbox-layout output, not a guessed line wrap. Coordinates are PDF points. */
export function parsePdfWords(xml:string):PdfWords{
 const out:PdfWords=[];let page=0;
 for(const p of xml.matchAll(/<page\b[^>]*>([\s\S]*?)<\/page>/g)){page++;let line=0;for(const l of p[1].matchAll(/<line\b[^>]*>([\s\S]*?)<\/line>/g)){line++;for(const w of l[1].matchAll(/<word\b([^>]*)>([\s\S]*?)<\/word>/g)){
  const get=(key:string)=>Number(w[1].match(new RegExp('\\b'+key+'="([^"]+)"'))?.[1]);const x0=get('xMin'),y0=get('yMin'),x1=get('xMax'),y1=get('yMax');if([x0,y0,x1,y1].every(Number.isFinite))out.push({text:decode(w[2]),x0,y0,x1,y1,page,lineId:`${page}:${line}`});
 }}}
 return out;
}
