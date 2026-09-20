import type {Project,SalesSlide,Visual,CopyEmission} from './types';
import {NativeCanvas,COLORS as C,type TextStyle} from './primitives';
import {resolveBlock} from './authoring';

export type ImagePainter=(visual:Visual,frame:{x:number;y:number;w:number;h:number},role:string,caption?:'below'|'inside'|'none',fit?:'cover'|'contain')=>void;
const SEA='#8DBDC2';
/** Registered compositions, with explicit evidence-band variants. No partner-specific renderer or font shrinking. */
export function drawSales(c:NativeCanvas,s:SalesSlide,p:Project,index:number,image:ImagePainter):CopyEmission[]{
 const emitted:CopyEmission[]=[];
 const evidence=!!s.footnotes?.length;
 const y=(normal:number,withEvidence:number)=>evidence?withEvidence:normal;
 const b=(id:string,x:number,top:number,w:number,h:number,size=12,max=120,color:string=C.body,weight=400,role='copy',url?:string)=>{
  const r=resolveBlock(p,id);if(r.text.length>max)throw new Error(`${s.key}/${id} exceeds ${max} characters for ${s.composition}${evidence?' with an evidence band':''}. Edit copy or choose another composition; do not shrink the entire deck.`);
  const style:TextStyle={size,color,weight,lineSpacing:104,...(url?{url}:{})};
  const objectId=c.text('block_'+id,r.text,x,top,w,h,style,role);
  emitted.push({blockId:id,slideKey:s.key,objectId,text:r.text,claimIds:r.claimIds,bindings:r.bindings,placement:r.block.placement});
  return objectId;
 };
 const label=(key:string,text:string,x:number,top:number,w:number,color:string=C.gold)=>c.text(key,text,x,top,w,13,{size:7.5,weight:700,color,lineSpacing:100});
 const line=(key:string,x:number,top:number,x2:number,color:string=C.line)=>c.line(key,x,top,x2,top,color,.7);
 c.background();
 if(s.kicker.length>55)throw new Error(`${s.key}: shorten kicker to 55 characters.`);
 label('kicker',s.kicker,36,18,605);c.text('index',String(index).padStart(2,'0'),660,18,24,12,{size:8.2,color:C.muted,align:'END'});
 b(s.title,36,40,648,61,29,62,C.white,600,'headline');
 switch(s.composition){
  case 'partner-opportunity':{
   b(s.intro,36,107,648,27,12.6,125);
   const step=666/s.domains.length;
   s.domains.forEach((d,j)=>{const x=36+j*step,w=step-20;b(d.heading,x,143,w,23,16,32,C.white,600);b(d.body,x,171,w,44,10.9,90);});
   line('proof_rule',36,y(228,225),684);
   const step2=666/s.proof.length;
   s.proof.forEach((v,j)=>{const x=36+j*step2,w=step2-20;b(v.heading,x,y(246,234),w,35,21,32,C.paleGold,600);b(v.body,x,y(282,273),w,y(31,25),10.2,90);});
   c.shape('offer_panel',30,y(319,304),660,y(53,45),C.panel);
   label('offer_label','THE PARTNERSHIP OPPORTUNITY',42,y(325,309),630);
   b(s.offer,42,y(342,325),630,y(27,23),14.2,y(110,100),C.white,500);
   break;
  }
  case 'product-value':{
   b(s.mechanism,36,107,648,30,13.1,125);
   image(s.visual,{x:36,y:147,w:407,h:y(209,181)},'product-hero','inside');
   s.benefits.forEach((v,j)=>{const top=148+j*y(105,91);b(v.heading,471,top,213,43,20,32,C.white,600);b(v.body,471,top+47,213,y(44,40),11.2,y(90,82));});
   line('proof_rule',36,y(360,334),684,C.gold);b(s.proof,36,y(366,341),648,13,9.2,120,C.paleGold,500);
   break;
  }
  case 'platform-architecture':{
   c.shape('platform_band',36,110,379,y(37,38),C.panel,C.line);b(s.banner,46,117,359,y(27,31),15.3,y(70,60),C.white,600);
   s.physical.forEach((v,j)=>{const x=36+(j%2)*194,top=y(160,154)+Math.floor(j/2)*y(57,55);
    c.shape('physical_'+j,x,top,185,49,undefined,C.line);
    if(v.visual){image(v.visual,{x:x+4,y:top+4,w:52,h:41},'physical-'+j,'none','contain');b(v.heading,x+64,top+6,115,20,11.6,y(28,21),C.white,600);b(v.body,x+64,top+26,115,22,8.4,y(50,44));}
    else{b(v.heading,x+8,top+7,169,20,13.6,28,C.white,600);b(v.body,x+8,top+29,169,18,8.8,50);}
   });
   c.shape('ownership_band',36,y(278,264),379,y(33,30),C.panel);b(s.ownership,45,y(284,269),361,25,11.9,y(90,78),C.white,500);
   c.shape('software_band',36,y(318,299),379,y(29,29),undefined,C.gold);b(s.software,45,y(324,304),361,y(21,24),11.9,y(85,78),C.paleGold,500);
   b(s.revenue,36,y(355,336),379,y(23,16),10.6,y(100,65),C.paleGold,500);
   label('demand_label','CUSTOMERS & VALUE',446,112,238,SEA);
   s.demand.forEach((v,j)=>{const top=y(142,136)+j*y(62,55);c.shape('demand_mark'+j,445,top+1,2,42,C.gold);b(v.heading,459,top,225,24,15.2,32,C.white,600);b(v.body,459,top+26,225,y(34,29),10.6,y(90,82));});
   line('takeaway_rule',446,y(337,318),684);b(s.takeaway,446,y(347,326),238,y(28,26),10.8,y(85,78),C.white,500);
   break;
  }
  case 'opportunity-portfolio':{
   b(s.intro,36,106,648,27,12.8,125);
   const n=s.programs.length,gap=16,w=(648-gap*(n-1))/n;
   s.programs.forEach((v,j)=>{const x=36+j*(w+gap);image(v.visual,{x,y:147,w,h:y(94,83)},'program-'+j,'inside');b(v.heading,x,y(252,240),w,42,n===4?14.3:17,40,C.white,600);b(v.value,x,y(302,285),w,36,n===4?11:12.4,76,C.paleGold,500);});
   line('connection_rule',36,y(342,326),684,C.gold);b(s.connection,36,y(352,334),648,y(26,20),12.4,y(125,108),C.white,500);
   break;
  }
  case 'mission-hero':{
   b(s.need,36,107,648,31,12.1,125);
   image(s.visual,{x:36,y:148,w:414,h:y(214,186)},'mission-product','inside');
   const step=s.benefits.length===3?y(75,65):y(109,92);
   s.benefits.forEach((v,j)=>{const top=147+j*step;b(v.heading,477,top,207,y(34,30),16.2,y(32,25),C.white,600);b(v.body,477,top+y(35,33),207,y(40,30),10.5,y(90,65));});
   b(s.payoff,36,y(368,341),414,12,8.6,98,C.paleGold,500);
   break;
  }
  case 'customer-alternative':{
   b(s.intro,36,106,648,28,12.7,125);
   const n=s.alternatives.length,gap=29,w=(648-gap*(n-1))/n;
   s.alternatives.forEach((v,j)=>{const x=36+j*(w+gap);if(v.emphasis)c.shape('differentiated_offer',x-10,146,w+20,y(164,145),C.panel,C.gold);line('alternative_rule'+j,x,160,x+w,v.emphasis?C.gold:C.line);b(v.heading,x,179,w,y(48,44),19,32,v.emphasis?C.paleGold:C.white,600);b(v.body,x,y(240,230),w,y(61,58),11.4,100);});
   b(s.jobs,36,y(322,298),648,23,13.8,95,C.white,500);b(s.advantage,36,y(351,326),648,y(23,18),11,125,C.paleGold,500);
   b(s.comparison.basisBlockId,36,y(371,340),648,y(10,9),6.9,170,C.muted);
   break;
  }
  case 'integrated-infrastructure':{
   b(s.intro,36,105,648,30,12.8,125);
   s.actions.forEach((v,j)=>{const top=151+j*y(61,57);b(v.heading,36,top,238,24,14,32,C.paleGold,600);b(v.body,36,top+26,238,y(37,29),10.8,90);});
   image(s.visual,{x:300,y:148,w:384,h:y(194,177)},'integrated-system','inside');
   line('options_rule',36,y(348,329),684,C.gold);b(s.options,36,y(357,337),648,y(22,18),10.8,y(140,130),C.white,500);
   break;
  }
  case 'strategic-close':{
   b(s.intro,36,109,648,43,24,y(85,70),C.paleGold,500);
   s.stakes.forEach((v,j)=>{const top=y(170,163)+j*y(62,56);b(v.heading,36,top,341,23,15.3,36,C.white,600);b(v.body,36,top+25,341,y(33,27),10.5,y(100,92));});
   image(s.visual,{x:414,y:y(174,169),w:270,h:y(171,147)},'strategic-prize','inside');
   if(s.companion)b(s.companion.labelBlockId,414,y(352,322),270,y(18,13),9.3,58,C.paleGold,500,'companion-link',s.companion.url);
   b(s.invitation,36,y(365,340),648,15,11.5,y(110,100),C.paleGold,500);
   break;
  }
 }
 b(s.status,36,382,648,9,6.5,140,C.muted,400,'evidence-status');
 c.footer(p.meta.footer);
 return emitted;
}
