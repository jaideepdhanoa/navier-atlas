import type {Project,SalesSlide,Visual,CopyEmission} from './types';
import {NativeCanvas,COLORS as C,type TextStyle} from './primitives';
import {resolveBlock} from './authoring';

export type ImagePainter=(visual:Visual,frame:{x:number;y:number;w:number;h:number},role:string,caption?:'below'|'inside'|'none',fit?:'cover'|'contain')=>void;
const SEA='#8DBDC2';
/** All V2 compositions use this renderer. No partner-specific branches or invisible legacy copy fields. */
export function drawSales(c:NativeCanvas,s:SalesSlide,p:Project,index:number,image:ImagePainter):CopyEmission[]{
 const emitted:CopyEmission[]=[];
 const b=(id:string,x:number,y:number,w:number,h:number,size=12,max=120,color:string=C.body,weight=400,role='copy',url?:string)=>{
  const r=resolveBlock(p,id);if(r.text.length>max)throw new Error(`${s.key}/${id} exceeds ${max} characters for ${s.composition}. Edit copy or choose another composition; do not shrink the entire deck.`);
  const style:TextStyle={size,color,weight,lineSpacing:104,...(url?{url}:{})};
  const objectId=c.text('block_'+id,r.text,x,y,w,h,style,role);
  emitted.push({blockId:id,slideKey:s.key,objectId,text:r.text,claimIds:r.claimIds,bindings:r.bindings,placement:r.block.placement});
  return objectId;
 };
 const label=(key:string,text:string,x:number,y:number,w:number,color:string=C.gold)=>c.text(key,text,x,y,w,13,{size:7.5,weight:700,color,lineSpacing:100});
 const line=(key:string,x:number,y:number,x2:number,color:string=C.line)=>c.line(key,x,y,x2,y,color,.7);
 c.background();
 if(s.kicker.length>55)throw new Error(`${s.key}: shorten kicker to 55 characters.`);
 label('kicker',s.kicker,36,18,605);c.text('index',String(index).padStart(2,'0'),660,18,24,12,{size:8.2,color:C.muted,align:'END'});
 b(s.title,36,40,648,61,29,62,C.white,600,'headline');
 switch(s.composition){
  case 'partner-opportunity':{
   b(s.intro,36,107,648,27,12.6,125);
   const step=666/s.domains.length;
   s.domains.forEach((d,j)=>{const x=36+j*step,w=step-20;b(d.heading,x,143,w,23,16,32,C.white,600);b(d.body,x,171,w,44,10.9,90);});
   line('proof_rule',36,228,684);
   const step2=666/s.proof.length;
   s.proof.forEach((v,j)=>{const x=36+j*step2,w=step2-20;b(v.heading,x,246,w,35,21,32,C.paleGold,600);b(v.body,x,282,w,31,10.2,90);});
   c.shape('offer_panel',30,319,660,53,C.panel);
   label('offer_label','THE PARTNERSHIP OPPORTUNITY',42,325,630);
   b(s.offer,42,342,630,27,14.2,110,C.white,500);
   break;
  }
  case 'product-value':{
   b(s.mechanism,36,107,648,30,13.1,125);
   image(s.visual,{x:36,y:147,w:407,h:209},'product-hero','inside');
   s.benefits.forEach((v,j)=>{const y=148+j*105;b(v.heading,471,y,213,43,20,32,C.white,600);b(v.body,471,y+47,213,44,11.2,90);});
   line('proof_rule',36,360,684,C.gold);b(s.proof,36,366,648,13,9.2,120,C.paleGold,500);
   break;
  }
  case 'platform-architecture':{
   c.shape('platform_band',36,110,379,37,C.panel,C.line);b(s.banner,46,117,359,27,15.3,70,C.white,600);
   s.physical.forEach((v,j)=>{const x=36+(j%2)*194,y=160+Math.floor(j/2)*57;
    c.shape('physical_'+j,x,y,185,49,undefined,C.line);
    if(v.visual){image(v.visual,{x:x+4,y:y+4,w:52,h:41},'physical-'+j,'none','contain');b(v.heading,x+64,y+6,115,20,11.6,28,C.white,600);b(v.body,x+64,y+26,115,22,8.4,50);}
    else{b(v.heading,x+8,y+7,169,20,13.6,28,C.white,600);b(v.body,x+8,y+29,169,18,8.8,50);}
   });
   c.shape('ownership_band',36,278,379,33,C.panel);b(s.ownership,45,284,361,25,11.9,90,C.white,500);
   c.shape('software_band',36,318,379,29,undefined,C.gold);b(s.software,45,324,361,21,11.9,85,C.paleGold,500);
   b(s.revenue,36,355,379,23,10.6,100,C.paleGold,500);
   label('demand_label','CUSTOMERS & VALUE',446,112,238,SEA);
   s.demand.forEach((v,j)=>{const y=142+j*62;c.shape('demand_mark'+j,445,y+1,2,42,C.gold);b(v.heading,459,y,225,24,15.2,32,C.white,600);b(v.body,459,y+26,225,34,10.6,90);});
   line('takeaway_rule',446,337,684);b(s.takeaway,446,347,238,28,10.8,85,C.white,500);
   break;
  }
  case 'opportunity-portfolio':{
   b(s.intro,36,106,648,27,12.8,125);
   const n=s.programs.length,gap=16,w=(648-gap*(n-1))/n;
   s.programs.forEach((v,j)=>{const x=36+j*(w+gap);image(v.visual,{x,y:147,w,h:94},'program-'+j,'inside');b(v.heading,x,252,w,42,n===4?14.3:17,40,C.white,600);b(v.value,x,302,w,36,n===4?11:12.4,76,C.paleGold,500);});
   line('connection_rule',36,342,684,C.gold);b(s.connection,36,352,648,26,12.4,125,C.white,500);
   break;
  }
  case 'mission-hero':{
   b(s.need,36,107,648,31,12.1,125);
   image(s.visual,{x:36,y:148,w:414,h:214},'mission-product','inside');
   const step=s.benefits.length===3?75:109;
   s.benefits.forEach((v,j)=>{const y=147+j*step;b(v.heading,477,y,207,34,16.2,32,C.white,600);b(v.body,477,y+35,207,40,10.5,90);});
   b(s.payoff,36,368,414,12,8.6,98,C.paleGold,500);
   break;
  }
  case 'customer-alternative':{
   b(s.intro,36,106,648,28,12.7,125);
   const n=s.alternatives.length,gap=29,w=(648-gap*(n-1))/n;
   s.alternatives.forEach((v,j)=>{const x=36+j*(w+gap);if(v.emphasis)c.shape('differentiated_offer',x-10,146,w+20,164,C.panel,C.gold);line('alternative_rule'+j,x,160,x+w,v.emphasis?C.gold:C.line);b(v.heading,x,179,w,48,19,32,v.emphasis?C.paleGold:C.white,600);b(v.body,x,240,w,61,11.4,100);});
   b(s.jobs,36,322,648,23,13.8,95,C.white,500);b(s.advantage,36,351,648,23,11,125,C.paleGold,500);
   b(s.comparison.basisBlockId,36,371,648,10,6.9,170,C.muted);
   break;
  }
  case 'integrated-infrastructure':{
   b(s.intro,36,105,648,30,12.8,125);
   s.actions.forEach((v,j)=>{const y=151+j*61;b(v.heading,36,y,238,24,14,32,C.paleGold,600);b(v.body,36,y+26,238,37,10.8,90);});
   image(s.visual,{x:300,y:148,w:384,h:194},'integrated-system','inside');
   line('options_rule',36,348,684,C.gold);b(s.options,36,357,648,22,10.8,140,C.white,500);
   break;
  }
  case 'strategic-close':{
   b(s.intro,36,109,648,43,24,85,C.paleGold,500);
   s.stakes.forEach((v,j)=>{const y=170+j*62;b(v.heading,36,y,341,23,15.3,36,C.white,600);b(v.body,36,y+25,341,33,10.5,100);});
   image(s.visual,{x:414,y:174,w:270,h:171},'strategic-prize','inside');
   if(s.companion)b(s.companion.labelBlockId,414,352,270,18,9.3,58,C.paleGold,500,'companion-link',s.companion.url);
   b(s.invitation,36,365,648,15,11.5,110,C.paleGold,500);
   break;
  }
 }
 b(s.status,36,382,648,9,6.5,140,C.muted,400,'evidence-status');
 c.footer(p.meta.footer);
 return emitted;
}
