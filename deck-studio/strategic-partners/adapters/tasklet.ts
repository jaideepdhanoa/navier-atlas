import type {NativePort} from '../src/lifecycle';
import type {DeckSnapshot,SlidesRequest} from '../src/types';

/** Supply approved connection IDs at runtime. Never save them in public fixtures. */
export interface TaskletConnections {slides:string;drive:string;}
export type ToolCaller=(request:{connectionId:string;toolName:string;args:Record<string,unknown>})=>Promise<{ok:boolean;error?:string;json():Promise<unknown>}>;

/** Thin optional adapter. The offline package imports no Tasklet runtime or credentials. */
export function makeTaskletNativePort(connections:TaskletConnections,invokeTool:ToolCaller):NativePort {
  if(!connections.slides?.trim()||!connections.drive?.trim())throw new Error('Explicit approved Slides and Drive connection IDs are required.');
  const call=async(service:keyof TaskletConnections,toolName:string,args:Record<string,unknown>)=>{
    const response=await invokeTool({connectionId:connections[service],toolName,args});
    if(!response.ok)throw new Error(response.error||`${toolName} failed`);
    return await response.json() as any;
  };
  return {
    // This Tasklet connection does not expose Google Slides writeControl.
    conditionalRevisions:false,
    async snapshot(id:string):Promise<DeckSnapshot>{
      const summary=await call('slides','google_slides_get_presentation',{presentationId:id,mode:'summary'});
      const count=summary.slideCount??summary.slides?.length;
      if(!Number.isInteger(count)||count<0)throw new Error('Invalid native slide-count response.');
      const slides:any[]=[];
      for(let start=1;start<=count;start+=2){
        const results=await Promise.all(Array.from({length:Math.min(2,count-start+1)},(_,j)=>call('slides','google_slides_get_presentation',{presentationId:id,mode:'slides',slideIndices:[start+j]})));
        for(const result of results){if(!Array.isArray(result.slides)||result.slides.length!==1)throw new Error('Incomplete native slide response.');slides.push(...result.slides);}
      }
      return {...summary,slides:slides.map((s,i)=>({...s,index:i+1}))};
    },
    async create(title:string){
      const r=await call('slides','google_slides_create_presentation',{title});
      if(!r.presentationId)throw new Error('Creation returned no presentation ID; reconcile, do not retry blindly.');
      return {presentationId:r.presentationId,url:r.webViewLink};
    },
    async duplicate(id:string,title:string){
      const r=await call('drive','google_drive_duplicate_file',{fileToCopyId:id,newFileName:title});
      if(!r.fileId)throw new Error('Copy returned no file ID; reconcile, do not retry blindly.');
      return {presentationId:r.fileId,url:r.webViewLink};
    },
    async batch(id:string,requests:SlidesRequest[],requiredRevision?:string){
      if(requiredRevision)throw new Error('Atomic conditional revisions are unavailable; live promotion is held.');
      return call('slides','google_slides_batch_update_presentation',{presentationId:id,requests});
    },
    async exportPDF(id:string,path:string){
      return call('drive','google_drive_download_file',{fileId:id,destinationPath:path,exportMimeType:'application/pdf'});
    },
  };
}
