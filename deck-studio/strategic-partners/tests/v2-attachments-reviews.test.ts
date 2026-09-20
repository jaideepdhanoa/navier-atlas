import {describe,test,expect} from 'bun:test';
import {attachmentFrame} from '../src/attachments';
import {salesIssues} from '../src/authoring';
import {editorialTemplate,editorialProblems} from '../src/reviews';
import {requireReview} from '../src/lifecycle';
import {sha256} from '../src/primitives';
import {clone,compileFixture,v2Projects} from './v2-fixtures';
import type {VisualAttachment,ReviewReceipt} from '../src/types';
const mark:VisualAttachment={assetId:'fixture-mark',parentSha256:'a'.repeat(64),assetSha256:'b'.repeat(64),region:{left:.4,top:.4,right:.6,bottom:.6},review:{status:'reviewed',reviewerKind:'fixture',reviewer:'Geometry test',reviewedAt:'2026-01-01T00:00:00Z'}};
describe('V2 visual attachments and distinct review gates',()=>{
 test('attached marks follow current parent geometry and clipped marks fail',()=>{
  expect(attachmentFrame({width:1600,height:900},{x:0,y:0,w:160,h:90},mark)).toEqual({x:64,y:36,w:31.999999999999993,h:17.999999999999996});
  const wide=attachmentFrame({width:1600,height:900},{x:10,y:20,w:320,h:180},mark);
  expect(wide.x).toBe(138);expect(wide.y).toBe(92);
  expect(()=>attachmentFrame({width:1600,height:900},{x:0,y:0,w:90,h:90},{...mark,region:{left:0,top:.1,right:.1,bottom:.2}})).toThrow('clipped');
 });
 test('attachment byte hashes and explicit review identity are mandatory',async()=>{
  const p=clone((await v2Projects())[0]);const s:any=p.slides.find(s=>'visual' in s);const a=p.assets.find(a=>a.id===s.visual.assetId)!;
  s.visual.attachments=[{...mark,assetId:a.id,parentSha256:'0'.repeat(64),assetSha256:a.sha256}];
  expect(salesIssues(p).some(i=>i.code==='ATTACHMENT_STALE')).toBe(true);
  s.visual.attachments[0].parentSha256=a.sha256;s.visual.attachments[0].review={...mark.review,reviewer:''};
  expect(salesIssues(p).some(i=>i.code==='ATTACHMENT_REVIEW')).toBe(true);
 });
 test('editorial templates remain unsigned and stale visible-copy reviews fail',async()=>{
  const p=(await v2Projects())[0],c=compileFixture(p),r=editorialTemplate(p,c);
  expect(r.decision).toBe('revise');expect(editorialProblems(p,c,r).length).toBeGreaterThan(0);
  r.subjectHash=sha256({wrong:'input'});expect(editorialProblems(p,c,r).some(s=>s.includes('stale'))).toBe(true);
 });
 test('agent, fixture and legacy receipts cannot impersonate human finished-deck/release approval',()=>{
  const r:ReviewReceipt={stage:'visual',subjectHash:'subject',reviewer:'Test agent',reviewedAt:'2026-01-01T00:00:00Z',decision:'approved',notes:'Fixture only',reviewerKind:'agent',purpose:'finished-deck'};
  expect(()=>requireReview(r,'visual','subject')).toThrow('human');
  expect(()=>requireReview({...r,reviewerKind:'fixture'},'visual','subject')).toThrow('human');
  expect(()=>requireReview({...r,stage:'release',purpose:'external-release'},'release','subject')).toThrow('human');
  expect(()=>requireReview({...r,reviewerKind:'human'},'visual','subject')).not.toThrow();
  expect(()=>requireReview({...r,stage:'release',reviewerKind:'human',purpose:'internal-readiness'},'release','subject')).toThrow('purpose');
 });
});
