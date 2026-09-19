import { createHash } from 'node:crypto';
import type { Asset, Box, ElementRole, SlidesRequest, Crop } from './types';

export const EMU = 12700;
export const PAGE = { width: 720, height: 405 } as const;
export const COLORS = {
  bg:'#0C141E', ink:'#142330', paper:'#F3F2ED', panel:'#14212D', line:'#334555',
  gold:'#D4B57A', paleGold:'#E2CEA7', white:'#F5F5F2', body:'#D3DDE3', muted:'#8E9EAB', darkMuted:'#60707C',
} as const;
export const rgb = (hex:string) => ({red:parseInt(hex.slice(1,3),16)/255,green:parseInt(hex.slice(3,5),16)/255,blue:parseInt(hex.slice(5,7),16)/255});
export const geom = (x:number,y:number,w:number,h:number) => ({size:{width:{magnitude:Math.round(w*EMU),unit:'EMU'},height:{magnitude:Math.round(h*EMU),unit:'EMU'}},transform:{scaleX:1,scaleY:1,translateX:Math.round(x*EMU),translateY:Math.round(y*EMU),unit:'EMU'}});
export const canonicalize = (value:unknown):unknown => Array.isArray(value) ? value.map(canonicalize) : value && typeof value === 'object' ? Object.fromEntries(Object.keys(value as any).sort().map(k=>[k,canonicalize((value as any)[k])])) : value;
export const sha256 = (value:unknown) => createHash('sha256').update(typeof value==='string'?value:JSON.stringify(canonicalize(value))).digest('hex');
export function stableId(projectId:string,slideKey:string,part:string,ordinal=0):string {
  const clean=(s:string)=>s.replace(/[^A-Za-z0-9_-]/g,'_');
  const full=`sp_${clean(projectId)}_${clean(slideKey)}_${clean(part)}_${ordinal}`;
  return full.length<=50?full:`${full.slice(0,29)}_${sha256(full).slice(0,20)}`;
}
export interface NormalizedCrop {left:number;top:number;right:number;bottom:number;}
export interface ImagePlacement {crop:NormalizedCrop;x:number;y:number;w:number;h:number;frame:{x:number;y:number;w:number;h:number};scale:number;}
const clamp=(n:number,a=0,b=1)=>Math.max(a,Math.min(b,n));
export function normalizeCrop(crop?:Crop):NormalizedCrop {
  const c=crop??{left:0,top:0,right:1,bottom:1};
  const left=clamp(c.left),top=clamp(c.top),right=clamp(c.right),bottom=clamp(c.bottom);
  return right>left&&bottom>top?{left,top,right,bottom}:{left:0,top:0,right:1,bottom:1};
}
/** Editorial crop planning only. Native CENTER_CROP does not implement arbitrary focal offsets. */
export function imagePlacement(asset:Pick<Asset,'width'|'height'|'crop'|'focalPoint'>,frame:{x:number;y:number;w:number;h:number}):ImagePlacement {
  const aw=Math.max(1,asset.width),ah=Math.max(1,asset.height),base=normalizeCrop(asset.crop),target=frame.w/Math.max(frame.h,.001);
  let cw=base.right-base.left,ch=base.bottom-base.top;
  if(cw*aw/(ch*ah)>target)cw=ch*ah*target/aw;else ch=cw*aw/(target*ah);
  const f=asset.focalPoint??{x:(base.left+base.right)/2,y:(base.top+base.bottom)/2};
  const cx=clamp(f.x,base.left+cw/2,base.right-cw/2),cy=clamp(f.y,base.top+ch/2,base.bottom-ch/2);
  const crop={left:cx-cw/2,top:cy-ch/2,right:cx+cw/2,bottom:cy+ch/2},scale=Math.max(frame.w/(aw*cw),frame.h/(ah*ch));
  return {crop,x:frame.x+frame.w/2-cx*aw*scale,y:frame.y+frame.h/2-cy*ah*scale,w:aw*scale,h:ah*scale,frame,scale};
}
export type TextStyle={size?:number;weight?:number;color?:string;align?:string;lineSpacing?:number;italic?:boolean;url?:string;};
export class NativeCanvas {
  requests:SlidesRequest[]=[];boxes:Box[]=[];elements:ElementRole[]=[];assetUses:{assetId:string;slideKey:string;role:string;objectId:string}[]=[];
  private used=new Set<string>();private seq=0;
  constructor(public readonly page:string,public readonly projectId:string,public readonly slideKey:string){}
  id(part:string){let id=stableId(this.projectId,this.slideKey,part,this.seq++);while(this.used.has(id))id=stableId(this.projectId,this.slideKey,part,this.seq++);this.used.add(id);return id;}
  addBox(box:Box){this.boxes.push(box);}
  background(color:string=COLORS.bg){this.requests.push({updatePageProperties:{objectId:this.page,pageProperties:{pageBackgroundFill:{solidFill:{color:{rgbColor:rgb(color)},alpha:1}}},fields:'pageBackgroundFill'}});}
  shape(part:string,x:number,y:number,w:number,h:number,fill?:string,stroke?:string,shapeType='RECTANGLE',role:'shape'|'mask'='shape',alpha=1){
    const id=this.id(part);
    this.requests.push({createShape:{objectId:id,shapeType,elementProperties:{pageObjectId:this.page,...geom(x,y,w,h)}}},{updateShapeProperties:{objectId:id,shapeProperties:{shapeBackgroundFill:fill?{solidFill:{color:{rgbColor:rgb(fill)},alpha}}:{propertyState:'NOT_RENDERED'},outline:stroke?{outlineFill:{solidFill:{color:{rgbColor:rgb(stroke)},alpha:1}},weight:{magnitude:.65,unit:'PT'}}:{propertyState:'NOT_RENDERED'}},fields:'shapeBackgroundFill,outline'}});
    this.addBox({objectId:id,slideKey:this.slideKey,role,x,y,w,h,intentionalClip:role==='mask'});this.elements.push({objectId:id,slideKey:this.slideKey,role,kind:'shape'});return id;
  }
  text(part:string,text:string,x:number,y:number,w:number,h:number,style:TextStyle={},role='text'){
    if(!text)return '';const id=this.id(part),size=style.size??12,weight=style.weight??400,pad=3.6;
    this.requests.push(
      {createShape:{objectId:id,shapeType:'TEXT_BOX',elementProperties:{pageObjectId:this.page,...geom(x-pad,y-pad,w+pad*2,h+pad*2)}}},
      {insertText:{objectId:id,insertionIndex:0,text}},
      {updateTextStyle:{objectId:id,textRange:{type:'ALL'},style:{fontFamily:'Exo 2',weightedFontFamily:{fontFamily:'Exo 2',weight},fontSize:{magnitude:size,unit:'PT'},foregroundColor:{opaqueColor:{rgbColor:rgb(style.color??COLORS.body)}},bold:weight>=700,italic:style.italic??false,...(style.url?{link:{url:style.url},underline:false}:{})},fields:'fontFamily,weightedFontFamily,fontSize,foregroundColor,bold,italic'+(style.url?',link,underline':'')}},
      {updateParagraphStyle:{objectId:id,textRange:{type:'ALL'},style:{alignment:style.align??'START',lineSpacing:style.lineSpacing??104,spaceAbove:{magnitude:0,unit:'PT'},spaceBelow:{magnitude:0,unit:'PT'},indentStart:{magnitude:0,unit:'PT'},indentEnd:{magnitude:0,unit:'PT'},indentFirstLine:{magnitude:0,unit:'PT'}},fields:'alignment,lineSpacing,spaceAbove,spaceBelow,indentStart,indentEnd,indentFirstLine'}},
      {updateShapeProperties:{objectId:id,shapeProperties:{shapeBackgroundFill:{propertyState:'NOT_RENDERED'},outline:{propertyState:'NOT_RENDERED'},contentAlignment:'TOP',autofit:{autofitType:'NONE'}},fields:'shapeBackgroundFill,outline,contentAlignment,autofit.autofitType'}}
    );
    this.addBox({objectId:id,slideKey:this.slideKey,role:'text',x:x-pad,y:y-pad,w:w+pad*2,h:h+pad*2,text,fontSize:size});this.elements.push({objectId:id,slideKey:this.slideKey,role:role==='text'?part:role,kind:'text'});return id;
  }
  line(part:string,x1:number,y1:number,x2:number,y2:number,color:string=COLORS.line,width=.7,arrow=false){
    const id=this.id(part);this.requests.push({createLine:{objectId:id,lineCategory:'STRAIGHT',elementProperties:{pageObjectId:this.page,size:{width:{magnitude:EMU,unit:'EMU'},height:{magnitude:EMU,unit:'EMU'}},transform:{scaleX:x2-x1,scaleY:y2-y1,translateX:Math.round(x1*EMU),translateY:Math.round(y1*EMU),unit:'EMU'}}}},{updateLineProperties:{objectId:id,lineProperties:{lineFill:{solidFill:{color:{rgbColor:rgb(color)},alpha:1}},weight:{magnitude:width,unit:'PT'},startArrow:'NONE',endArrow:arrow?'FILL_ARROW':'NONE'},fields:'lineFill,weight,startArrow,endArrow'}});
    this.addBox({objectId:id,slideKey:this.slideKey,role:'line',x:Math.min(x1,x2),y:Math.min(y1,y2),w:Math.abs(x2-x1),h:Math.abs(y2-y1)});this.elements.push({objectId:id,slideKey:this.slideKey,role:part,kind:'line'});return id;
  }
  /** Shape replacement gives true native clipping without distortion or spill into neighbouring cards.
   * Google mints image IDs: resolve placeholder roles against fresh native objects before any revision.
   */
  image(part:string,asset:Asset,url:string,frame:{x:number;y:number;w:number;h:number},role='visual',explicitCrop?:Crop,fit:'cover'|'contain'='cover'){
    if(explicitCrop)throw new Error('Explicit focal crops require an archived crop derivative or a reviewed native crop; they cannot be silently replaced by CENTER_CROP.');
    const id=this.id(part),tag=`__SP_IMAGE_${id}__`,mode=asset.kind==='logo'||fit==='contain'?'CENTER_INSIDE':'CENTER_CROP';
    this.requests.push({createShape:{objectId:id,shapeType:'RECTANGLE',elementProperties:{pageObjectId:this.page,...geom(frame.x,frame.y,frame.w,frame.h)}}},{insertText:{objectId:id,insertionIndex:0,text:tag}},{replaceAllShapesWithImage:{containsText:{text:tag,matchCase:true},pageObjectIds:[this.page],imageUrl:url,imageReplaceMethod:mode}});
    this.addBox({objectId:id,slideKey:this.slideKey,role:'image',...frame});this.elements.push({objectId:id,slideKey:this.slideKey,role,kind:'image',assetId:asset.id});this.assetUses.push({assetId:asset.id,slideKey:this.slideKey,role,objectId:id});return id;
  }
  footer(text:string){this.text('footer',text,36,390,648,9,{size:6.1,color:COLORS.muted,lineSpacing:100});}
  header(kicker:string,title:string,index:number,size=28){this.text('kicker',kicker,36,17,610,14,{size:8.4,weight:700,color:COLORS.gold,lineSpacing:100});this.text('index',String(index).padStart(2,'0'),660,17,24,14,{size:8.4,color:COLORS.muted,align:'END',lineSpacing:100});this.text('title',title,36,39,648,62,{size,weight:600,color:COLORS.white,lineSpacing:99});}
  explore(text:string){this.line('explore_rule',36,360,684,360,COLORS.line,.65);this.text('explore_label','EXPLORE',36,368,52,15,{size:8,weight:700,color:COLORS.gold,lineSpacing:100});this.text('explore',text,97,366,587,20,{size:10.8,weight:500,color:COLORS.white,lineSpacing:100});}
  payment(part:string,transaction:{actors:string[];labels:string[]},x:number,y:number,w:number,size=10.5){
    const n=transaction.actors.length;if(n<2||n>3||transaction.labels.length!==n-1)throw new Error('Payment diagrams require 2–3 actors and one payment label per arrow.');
    const aw=w*(n===3?.235:.29),gap=(w-n*aw)/(n-1);
    this.text(`${part}_kind`,'PROPOSED PAYMENTS',x,y-28,w,12,{size:6.5,weight:700,color:COLORS.muted,lineSpacing:100});
    transaction.actors.forEach((actor,i)=>this.text(`${part}_actor${i}`,actor,x+i*(aw+gap),y,aw,28,{size,weight:600,color:COLORS.white,align:'CENTER',lineSpacing:100}));
    transaction.labels.forEach((label,i)=>{const x1=x+i*(aw+gap)+aw+3,x2=x+(i+1)*(aw+gap)-3;this.text(`${part}_price${i}`,label,x1-12,y-15,x2-x1+24,15,{size:7.2,color:COLORS.gold,align:'CENTER',lineSpacing:100});this.line(`${part}_arrow${i}`,x1,y+10,x2,y+10,COLORS.gold,.9,true);});
  }
}
export function textCapacity(text:string,w:number,h:number,fontSize:number):number{return Math.max(1,Math.floor(w/(fontSize*.52))*Math.max(1,Math.floor(h/(fontSize*1.2))));}
export function outOfCanvas(box:Pick<Box,'x'|'y'|'w'|'h'>):boolean{return box.x< -1||box.y< -1||box.x+box.w>PAGE.width+1||box.y+box.h>PAGE.height+1;}
