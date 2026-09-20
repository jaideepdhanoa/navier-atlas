import {describe,test,expect} from 'bun:test';
import {readFile} from 'node:fs/promises';
import {join} from 'node:path';
import {schemaIssues} from '../src/schema';
import {validateProject} from '../src/validate';
import {migratePackage} from '../src/package';
import {clone,compileFixture,v2Projects,repoRoot,tempDir} from './v2-fixtures';

describe('V2 contract, migration and compatibility',()=>{
 test('all fictional V2 inputs share the strict schema and production renderer',async()=>{
  const projects=await v2Projects();expect(projects.length).toBe(3);
  for(const p of projects){expect(schemaIssues(p)).toEqual([]);expect((await validateProject(p)).ok).toBe(true);expect(compileFixture(p).slides.length).toBe(p.slides.length);}
 });
 test('unknown fields and unknown compositions fail, not silently disappear',async()=>{
  const p=clone((await v2Projects())[0]) as any;
  const s=p.slides.find((s:any)=>s.layout==='sales');s.secretPartnerOnlyField='unsupported';
  expect(schemaIssues(p).length).toBeGreaterThan(0);expect(()=>compileFixture(p)).toThrow();
  delete s.secretPartnerOnlyField;s.composition='partner-custom-fork';expect(schemaIssues(p).length).toBeGreaterThan(0);
 });
 test('V1 migration preserves original bytes and is a held draft, not a story rewrite',async()=>{
  const source=join(repoRoot,'examples/public-demo/project.json');const before=await readFile(source,'utf8');
  expect(schemaIssues(JSON.parse(before))).toEqual([]);
  const out=await tempDir('migration');const result=await migratePackage(source,out);
  expect(result.status).toBe('HELD');expect(await readFile(source,'utf8')).toBe(before);
  expect(JSON.parse(await readFile(join(out,'project-v1.json'),'utf8'))).toEqual(JSON.parse(before));
  const draft=JSON.parse(await readFile(result.draft,'utf8'));expect(draft.kind).toBe('V2-AUTHORING-DRAFT-NOT-A-PROJECT');
  expect((await validateProject(draft)).ok).toBe(false);
 });
 test('validation can never supply human release permission',async()=>{
  for(const p of await v2Projects()){const r=await validateProject(p);expect(r.releaseReady).toBe(false);expect(r.issues.some(i=>i.code==='HUMAN_RELEASE_REQUIRED')).toBe(true);}
 });
});
