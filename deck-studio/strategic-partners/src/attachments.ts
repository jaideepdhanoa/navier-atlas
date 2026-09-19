import type {Asset,VisualAttachment} from './types';
export function attachmentFrame(asset:Pick<Asset,'width'|'height'>,frame:{x:number;y:number;w:number;h:number},mark:VisualAttachment,fit:'cover'|'contain'='cover'){
 const r=mark.region,values=[asset.width,asset.height,frame.x,frame.y,frame.w,frame.h,r.left,r.top,r.right,r.bottom];
 if(values.some(v=>!Number.isFinite(v))||asset.width<=0||asset.height<=0||frame.w<=0||frame.h<=0||r.left<0||r.top<0||r.right>1||r.bottom>1||r.left>=r.right||r.top>=r.bottom)throw Error('Invalid attachment geometry.');
 const scale=(fit==='contain'?Math.min:Math.max)(frame.w/asset.width,frame.h/asset.height);
 const w=asset.width*scale,h=asset.height*scale,x=frame.x+(frame.w-w)/2,y=frame.y+(frame.h-h)/2;
 const result={x:x+r.left*w,y:y+r.top*h,w:(r.right-r.left)*w,h:(r.bottom-r.top)*h};
 const epsilon=.001;
 if(result.x<frame.x-epsilon||result.y<frame.y-epsilon||result.x+result.w>frame.x+frame.w+epsilon||result.y+result.h>frame.y+frame.h+epsilon)throw Error('Attachment is clipped by the current parent image frame; review its crop.');
 return result;
}
