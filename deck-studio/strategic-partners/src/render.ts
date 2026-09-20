import type { Asset, CompiledDeck, CompiledSlide, Project, Slide, Visual, Transaction } from './types';
import { COLORS, NativeCanvas, PAGE, outOfCanvas, sha256, stableId } from './primitives';
import type {CopyEmission} from './types';
import {drawSales} from './compositions';
import {assertSchema} from './schema';
import {salesIssues,slideTitle,slideBlockClaims,notesBlocks} from './authoring';
import {attachmentFrame} from './attachments';
import {evidenceIssues} from './evidence';
import {renderTalkTrack} from './talk-track';
import {drawEvidenceFootnotes} from './footnotes';
import {densityLedger,numeralDiagnostics} from './diagnostics';
export interface RenderOptions {assetUrls?:Record<string,string>;allowUnresolvedAssets?:boolean;}
export class RenderSafetyError extends Error {constructor(message:string){super(message);this.name='RenderSafetyError';}}
type Warning=CompiledDeck['warnings'][number];
const warn=(warnings:Warning[],code:string,path:string,message:string,severity:Warning['severity']='warning')=>warnings.push({code,path,message,severity});
const budget=(text:unknown,max:number,path:string)=>{if(typeof text==='string'&&text.length>max)throw new RenderSafetyError(`${path} exceeds ${max} characters; edit the copy or choose a different composition.`);};
function checkBudgets(s:Slide){
  if(s.layout==='sales')return;
  budget(s.title,95,`${s.key}.title`);budget(s.kicker,70,`${s.key}.kicker`);
  const v=(v:Visual|undefined,max=110)=>v&&budget(v.caption,max,`${s.key}.caption`);
  if(s.layout==='cover'){budget(s.title,52,`${s.key}.title`);budget(s.subtitle,72,`${s.key}.subtitle`);budget(s.body,135,`${s.key}.body`);s.pillars.forEach(x=>budget(x,42,`${s.key}.pillar`));v(s.visual);}
  if(s.layout==='fit'){budget(s.companyHeadline,67,`${s.key}.companyHeadline`);budget(s.companyBody,115,`${s.key}.companyBody`);budget(s.partnerBody,105,`${s.key}.partnerBody`);s.benefits.forEach(b=>{budget(b.title,34,`${s.key}.benefit.title`);budget(b.body,80,`${s.key}.benefit.body`);});v(s.visual);}
  if(s.layout==='options')s.options.forEach(o=>{budget(o.title,35,`${s.key}.option.title`);budget(o.body,105,`${s.key}.option.body`);budget(o.revenue,43,`${s.key}.option.revenue`);v(o.visual,70);});
  if(s.layout==='models')s.models.forEach(m=>{budget(m.title,37,`${s.key}.model.title`);budget(m.body,132,`${s.key}.model.body`);budget(m.benefit,88,`${s.key}.model.benefit`);v(m.visual,80);});
  if(s.layout==='channels'){budget(s.selection,74,`${s.key}.selection`);budget(s.criteria,112,`${s.key}.criteria`);budget(s.service,80,`${s.key}.service`);v(s.visual);}
  if(s.layout==='missions'){budget(s.title,48,`${s.key}.title`);budget(s.intro,100,`${s.key}.intro`);s.cards.forEach(c=>{budget(c.title,s.cards.length===4?44:56,`${s.key}.card.title`);budget(c.description,s.cards.length===4?70:116,`${s.key}.card.description`);v(c.visual,s.cards.length===4?65:100);});}
  if(s.layout==='close'){budget(s.title,51,`${s.key}.title`);budget(s.intro,70,`${s.key}.intro`);budget(s.ask,83,`${s.key}.ask`);budget(s.contact,50,`${s.key}.contact`);s.conversations.forEach(c=>{budget(c.title,36,`${s.key}.conversation.title`);budget(c.body,96,`${s.key}.conversation.body`);});v(s.visual);}
  if('explore'in s)budget(s.explore,110,`${s.key}.explore`);
}
function footer(p:Project){return p.meta.footer||`${p.meta.company} · ${p.meta.partner}`;}
function visual(c:NativeCanvas,p:Project,warnings:Warning[],assets:Map<string,Asset>,urls:Map<string,string>,v:Visual|undefined,frame:{x:number;y:number;w:number;h:number},role:string,caption:'below'|'inside'|'none'='below',fit:'cover'|'contain'='cover'){
  if(!v)return;const a=assets.get(v.assetId);if(!a)throw new RenderSafetyError(`Unknown asset ${v.assetId}`);
  if(v.crop||a.crop)throw new RenderSafetyError(`Explicit crop for ${a.id} must be supplied as an archived derivative or set in a reviewed native deck; silent crop fallback is forbidden.`);
  if(a.focalPoint&&(Math.abs(a.focalPoint.x-.5)>.01||Math.abs(a.focalPoint.y-.5)>.01))warn(warnings,'FOCAL_REVIEW',`assets.${a.id}`,'Native CENTER_CROP is used. Inspect the focal region in the actual render; noncentral crops require a reviewed native edit or archived derivative.');
  if(a.keepRegion)warn(warnings,'KEEP_REGION_REVIEW',`assets.${a.id}`,'Check the protected region against actual native crop before approval.');
  const parentId=c.image(`${role}_${a.id}`,a,urls.get(a.id)!,frame,role,undefined,fit);
  for(const mark of v.attachments??[]){const child=assets.get(mark.assetId);if(!child||mark.parentSha256!==a.sha256||mark.assetSha256!==child.sha256||mark.review.status!=='reviewed')throw new RenderSafetyError('Unreviewed or stale image attachment.');const box=attachmentFrame(a,frame,mark,a.kind==='logo'?'contain':fit);const id=c.image(`${role}_attachment_${child.id}`,child,urls.get(child.id)!,box,role+'-attachment',undefined,'contain');const binding=c.elements.find(e=>e.objectId===id)!;binding.parentObjectId=parentId;}
  if(caption!=='none'){
    const small=frame.w<200,size=small?6.3:6.8,y=caption==='inside'?frame.y+frame.h-22:frame.y+frame.h+4;
    if(caption==='inside')c.shape(`${role}_caption_field`,frame.x,y-3,frame.w,25,COLORS.bg,undefined,'RECTANGLE','mask',.82);
    c.text(`${role}_caption`,v.caption,frame.x+(caption==='inside'?8:0),y,frame.w-(caption==='inside'?16:0),19,{size,color:COLORS.muted,lineSpacing:100},'visual-caption');
  }
  void p;
}
function logos(c:NativeCanvas,p:Project,assets:Map<string,Asset>,urls:Map<string,string>){
  const ids=[p.meta.companyLogoAssetId,p.meta.partnerLogoAssetId];
  ids.forEach((id,i)=>{if(id){const a=assets.get(id);if(!a)throw new RenderSafetyError(`Unknown logo ${id}`);c.image(`logo_${i}`,a,urls.get(id)!,{x:36+i*130,y:21,w:114,h:33},'logo');}});
  if(!ids[0])c.text('company_name',p.meta.company,36,26,115,30,{size:17,weight:600,color:COLORS.white});
  if(!ids[1])c.text('partner_name',p.meta.partner,166,25,132,39,{size:10.5,weight:500,color:COLORS.white,lineSpacing:103});
}
function draw(c:NativeCanvas,s:Slide,p:Project,a:Map<string,Asset>,u:Map<string,string>,w:Warning[],index:number):CopyEmission[]{
  const image=(v:Visual|undefined,box:{x:number;y:number;w:number;h:number},role:string,cap:'below'|'inside'|'none'='below',fit:'cover'|'contain'='cover')=>visual(c,p,w,a,u,v,box,role,cap,fit);
  if(s.layout==='sales')return drawSales(c,s,p,index,image);
  c.background();
  if(s.layout==='cover'){
    image(s.visual,{x:318,y:72,w:402,h:265},'cover','inside');logos(c,p,a,u);
    c.text('cover_kicker',s.kicker,36,91,264,25,{size:8.2,weight:700,color:COLORS.gold,lineSpacing:100});
    c.text('cover_title',s.title,36,124,270,83,{size:31,weight:600,color:COLORS.white,lineSpacing:99});
    c.text('cover_subtitle',s.subtitle,36,214,270,62,{size:22,weight:500,color:COLORS.paleGold,lineSpacing:101});
    c.text('cover_body',s.body,36,291,265,43,{size:10.7,color:COLORS.body,lineSpacing:108});
    const step=648/s.pillars.length;s.pillars.forEach((x,i)=>{const px=36+i*step;c.text(`pillar_n${i}`,String(i+1).padStart(2,'0'),px,359,19,14,{size:8.2,weight:700,color:COLORS.gold});c.text(`pillar_${i}`,x,px+25,357,step-38,29,{size:10.3,weight:500,color:COLORS.white,lineSpacing:101});});
  }else if(s.layout==='fit'){
    c.header(s.kicker,s.title,index);c.text('company_label',s.companyLabel,36,112,375,16,{size:8.2,weight:700,color:COLORS.gold});
    image(s.visual,{x:36,y:135,w:375,h:137},'fit');c.text('company_headline',s.companyHeadline,36,302,375,39,{size:16,weight:500,color:COLORS.white,lineSpacing:101});c.text('company_body',s.companyBody,36,347,375,24,{size:9.4,color:COLORS.body,lineSpacing:102});
    c.text('partner_label',s.partnerLabel,450,112,234,17,{size:8.2,weight:700,color:COLORS.gold});c.text('partner_body',s.partnerBody,450,137,234,43,{size:11.6,color:COLORS.body,lineSpacing:105});c.line('fit_rule',450,188,684,188,COLORS.gold,.8);
    s.benefits.forEach((b,i)=>{const y=199+i*53;c.text(`benefit_n${i}`,String(i+1).padStart(2,'0'),450,y+3,23,16,{size:8,weight:700,color:COLORS.gold});c.text(`benefit_title${i}`,b.title,479,y,205,22,{size:13.9,weight:500,color:COLORS.white});c.text(`benefit_body${i}`,b.body,479,y+24,205,29,{size:9.4,color:COLORS.body,lineSpacing:103});});c.text('takeaway',s.takeaway,36,374,648,14,{size:8.7,color:COLORS.paleGold});
  }else if(s.layout==='options'){
    c.header(s.kicker,s.title,index,27.5);const n=s.options.length,gap=15,width=(648-gap*(n-1))/n;
    s.options.forEach((o,i)=>{const x=36+i*(width+gap);c.text(`option_title${i}`,o.title,x,112,width,26,{size:15,weight:600,color:COLORS.white});c.text(`option_body${i}`,o.body,x,144,width,37,{size:10.2,color:COLORS.body,lineSpacing:105});
      if(o.visual)image(o.visual,{x,y:190,w:width,h:90},`option${i}`,'below','contain');else{c.shape(`diagram_field${i}`,x,190,width,90,COLORS.paper);const label=o.schematic==='manufacture'?'Design → manufacture':o.schematic==='hybrid'?'Engine + electric drive':'Local support + service';c.shape(`diagram_a${i}`,x+17,207,width*.27,31,undefined,COLORS.ink);c.shape(`diagram_b${i}`,x+width*.61,207,width*.27,31,COLORS.ink);c.line(`diagram_arrow${i}`,x+width*.35,223,x+width*.58,223,COLORS.ink,1,true);c.text(`diagram_label${i}`,label,x+8,249,width-16,22,{size:9,color:COLORS.ink,align:'CENTER'});c.text(`diagram_caption${i}`,'Illustrative workflow — not a system design',x,284,width,15,{size:6.4,color:COLORS.muted});}
      c.text(`option_revenue${i}`,o.revenue,x,307,width,20,{size:10.7,weight:500,color:COLORS.paleGold});});
    if(s.payment)c.payment('powertrain_payment',s.payment,158,339,408,10.5);c.text('option_status',s.status,36,327,116,29,{size:6.6,color:COLORS.muted,lineSpacing:101});c.explore(s.explore);
  }else if(s.layout==='models'){
    c.header(s.kicker,s.title,index,27.5);c.line('model_divider',360,111,360,351,COLORS.line,.75);
    s.models.forEach((m,i)=>{const x=i?386:36,width=i?298:305;c.text(`model_label${i}`,m.label,x,111,width,17,{size:8.3,weight:700,color:COLORS.gold});c.text(`model_title${i}`,m.title,x,137,width,28,{size:19,weight:600,color:COLORS.white});c.text(`model_body${i}`,m.body,x,168,width,35,{size:10.4,color:COLORS.body,lineSpacing:105});
      if(m.visual){image(m.visual,{x,y:208,w:width*.62,h:77},`model${i}`,'none');c.text(`model_image_caption${i}`,m.visual.caption,x+width*.67,227,width*.33,45,{size:8.2,color:COLORS.muted,lineSpacing:103});}else{c.shape(`model_boundary${i}`,x+8,221,width-16,49,undefined,COLORS.muted);c.text(`model_technology${i}`,m.technologyLabel||'Product / service scope to define',x+20,235,width-40,28,{size:10.8,weight:500,color:COLORS.white,align:'CENTER'});c.text(`model_caption${i}`,'Proposed commercial model',x,275,width,14,{size:6.7,color:COLORS.muted});}
      c.payment(`model_pay${i}`,m.payments,x,317,width,10.4);c.text(`model_benefit${i}`,m.benefit,x,346,width,18,{size:8.2,color:COLORS.paleGold,lineSpacing:101});});c.explore(s.explore);
  }else if(s.layout==='channels'){
    c.header(s.kicker,s.title,index,27.5);if(s.visual)image(s.visual,{x:36,y:124,w:292,h:183},'scope','inside');else c.shape('scope_field',36,124,292,214,COLORS.panel);
    c.text('scope_label',s.scope,53,142,257,17,{size:8.3,weight:700,color:COLORS.gold});c.text('selection',s.selection,53,173,257,69,{size:22,weight:500,color:COLORS.white,lineSpacing:101});c.text('criteria',s.criteria,53,267,257,46,{size:11,color:COLORS.body,lineSpacing:105});
    c.line('channels_divider',348,118,348,348,COLORS.line,.75);s.models.forEach((m,i)=>{const y=120+i*95;c.text(`channel_label${i}`,m.label,369,y,315,17,{size:8.3,weight:700,color:COLORS.gold});c.text(`channel_benefit${i}`,m.benefit,369,y+21,315,23,{size:13.8,weight:500,color:COLORS.white});c.payment(`channel_pay${i}`,m.payments,369,y+70,315,10.4);});
    c.line('service_rule',369,321,684,321,COLORS.line,.7);c.text('service_label',s.serviceLabel,369,329,315,14,{size:7.9,weight:700,color:COLORS.gold});c.text('service',s.service,369,345,315,14,{size:9.8,color:COLORS.white});c.explore(s.explore);
  }else if(s.layout==='missions'){
    c.header(s.kicker,s.title,index,27.5);c.text('missions_intro',s.intro,36,84,406,31,{size:10.8,color:COLORS.body,lineSpacing:104});c.text('missions_status',s.status,463,84,221,31,{size:7.4,color:COLORS.muted,align:'END',lineSpacing:104});
    const n=s.cards.length,gap=n===4?12:15,width=(648-gap*(n-1))/n,h=n===4?110:125;
    s.cards.forEach((card,i)=>{const x=36+i*(width+gap);image(card.visual,{x,y:125,w:width,h},`mission${i}`);const labelY=125+h+26;c.text(`mission_label${i}`,card.label,x,labelY,width,15,{size:n===4?6.4:7.1,weight:700,color:COLORS.gold,lineSpacing:100});c.text(`mission_title${i}`,card.title,x,labelY+17,width,35,{size:n===4?12.7:15.1,weight:500,color:COLORS.white,lineSpacing:99});c.text(`mission_desc${i}`,card.description,x,labelY+55,width,24,{size:n===4?8.1:9,color:COLORS.body,lineSpacing:102});});c.explore(s.explore);
  }else if(s.layout==='close'){
    image(s.visual,{x:0,y:155,w:396,h:224},'close','inside');c.text('close_kicker',s.kicker,36,26,330,18,{size:8.2,weight:700,color:COLORS.gold});c.text('close_title',s.title,36,56,330,81,{size:29,weight:600,color:COLORS.white,lineSpacing:100});
    c.text('close_intro',s.intro,414,55,270,68,{size:21,weight:500,color:COLORS.white,lineSpacing:103});s.conversations.forEach((v,i)=>{const y=151+i*56;c.text(`conversation_n${i}`,String(i+1).padStart(2,'0'),414,y+2,23,18,{size:8.3,weight:700,color:COLORS.gold});c.text(`conversation_title${i}`,v.title,444,y,240,23,{size:13.8,weight:500,color:COLORS.white});c.text(`conversation_body${i}`,v.body,444,y+24,240,29,{size:9.8,color:COLORS.body,lineSpacing:104});});c.line('close_rule',414,327,684,327,COLORS.gold,.8);c.text('close_ask',s.ask,414,340,270,29,{size:10.6,weight:500,color:COLORS.paleGold});c.text('contact',s.contact,414,374,270,13,{size:8.6,color:COLORS.white,url:s.contact.includes('@')?`mailto:${s.contact}`:undefined});
  }
  c.footer(footer(p));
  return [];
}
export function compileProject(project:Project,options:RenderOptions={}):CompiledDeck{
  if(['2.0.0','2.1.0'].includes(project.schemaVersion)){assertSchema(project);const bad=[...salesIssues(project),...evidenceIssues(project)].filter(i=>i.severity==='error');if(bad.length)throw new RenderSafetyError(bad.slice(0,12).map(i=>`${i.code} ${i.path}: ${i.message}`).join('; '));}
  const warnings:Warning[]=[],assets=new Map(project.assets.map(a=>[a.id,a])),used=new Set<string>();
  const visit=(x:any)=>{if(Array.isArray(x))x.forEach(visit);else if(x&&typeof x==='object')Object.entries(x).forEach(([k,v])=>{if(k==='assetId'&&typeof v==='string')used.add(v);else visit(v);});};project.slides.forEach(visit);[project.meta.companyLogoAssetId,project.meta.partnerLogoAssetId].forEach(id=>id&&used.add(id));
  const urls=new Map<string,string>();for(const id of used){const asset=assets.get(id);if(!asset)throw new RenderSafetyError(`Unknown asset ${id}`);const url=options.assetUrls?.[id]||asset.embeddingUrl;if(url)urls.set(id,url);else if(options.allowUnresolvedAssets){urls.set(id,`asset://${id}`);warn(warnings,'UNRESOLVED_ASSET',`assets.${id}`,'Resolve to a verified image URL before native staging.');}else throw new RenderSafetyError(`No embedding URL for asset ${id}`);}
  const slides:CompiledSlide[]=[],requests:any[]=[],seen=new Set<string>();
  project.slides.forEach((s,i)=>{checkBudgets(s);const id=stableId(project.meta.projectId,s.key,'page'),c=new NativeCanvas(id,project.meta.projectId,s.key);c.requests.push({createSlide:{objectId:id,slideLayoutReference:{predefinedLayout:'BLANK'}}});const copyBindings=draw(c,s,project,assets,urls,warnings,i+1);drawEvidenceFootnotes(c,project,s);
    for(const r of c.requests){if(Object.keys(r).length!==1)throw new RenderSafetyError('Each Slides request must contain exactly one operation.');for(const[k,v]of Object.entries(r)as any){if(k.startsWith('create')&&v.objectId){if(seen.has(v.objectId))throw new RenderSafetyError(`Duplicate native ID ${v.objectId}`);seen.add(v.objectId);}}}
    c.boxes.forEach(b=>{if(outOfCanvas(b)&&!b.intentionalClip)warn(warnings,'OUT_OF_CANVAS',`slides.${s.key}.${b.objectId}`,'Element extends beyond canvas.');});
    slides.push({key:s.key,objectId:id,layout:s.layout,requests:c.requests,elements:c.elements,boxes:c.boxes,visibleText:c.boxes.filter(b=>b.role==='text'&&b.text).map(b=>b.text!),notes:renderTalkTrack(project,s),...(s.layout==='sales'?{copyBindings}:{})});requests.push(...c.requests);
  });
  const compiled:CompiledDeck={schemaVersion:'1.0.0',projectId:project.meta.projectId,revision:project.meta.revision,inputHash:sha256(project),pageSize:PAGE,slides,requests,assetUses:slides.flatMap(s=>s.elements.filter(e=>e.kind==='image'&&e.assetId).map(e=>({assetId:e.assetId!,slideKey:s.key,role:e.role,objectId:e.objectId}))),warnings};
  if(project.schemaVersion==='2.1.0'){for(const issue of numeralDiagnostics(project,compiled)){if(issue.severity==='error')throw new RenderSafetyError(issue.code+': '+issue.detail);warn(warnings,issue.code,issue.slideKeys.join(','),issue.detail);}for(const row of densityLedger(project,compiled)){const slide=project.slides.find(s=>s.key===row.slideKey)!;const name=slide.layout==='sales'?slide.composition:slide.layout;const max=project.policy.editorial?.bodyWordBudgets?.[name]??115;if(row.bodyWords>max)warn(warnings,'BODY_DENSITY',`slides.${row.slideKey}`,`${row.bodyWords} body words exceeds the advisory ${max}-word budget. Edit for argument density, not fact count.`);}}
  return compiled;
}
