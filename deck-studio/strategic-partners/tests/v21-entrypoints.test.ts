import {test,expect} from 'bun:test';
import {cp,readFile,writeFile} from 'node:fs/promises';
import {join} from 'node:path';
import {v21Fixture,addQuantity} from './v21-fixtures';
import {repoRoot,tempDir} from './v2-fixtures';
import {evidenceIssues} from '../src/evidence';
import {normalizeNumericDisplay} from '../src/diagnostics';
import {compileProject} from '../src/render';
const errors=(p:any)=>evidenceIssues(p).filter(i=>i.severity==='error').map(i=>i.code);
async function cli(args:string[]){const child=Bun.spawn([process.execPath,join(repoRoot,'src/cli.ts'),...args],{cwd:repoRoot,stdout:'pipe',stderr:'pipe'});const [stdout,stderr,code]=await Promise.all([new Response(child.stdout).text(),new Response(child.stderr).text(),child.exited]);return {stdout,stderr,code};}

test('the documented V2.1 CLI scaffold is held and cannot overwrite an intake',async()=>{
 const dir=await tempDir('v21-cli-intake'),out=join(dir,'intake');
 const r=await cli(['init2.1','--out',out,'--partner','Fictional Partner','--entity','Fictional Partner Ltd']);
 expect(r.code).toBe(0);expect(JSON.parse(r.stdout).status).toBe('HELD');
 const p=JSON.parse(await readFile(join(out,'project.json'),'utf8'));expect(p.schemaVersion).toBe('2.1.0');expect(p.sales.brief.companions.status).toBe('unknown');expect(p.claims).toEqual([]);
 expect((await cli(['init','--out',out,'--partner','Fictional Partner','--entity','Fictional Partner Ltd'])).code).toBe(1);
 expect((await cli(['validate','--project',join(out,'project.json')])).code).toBe(2);
});

test('serialized V2.1 CLI validation, compilation and legacy migration use the real commands',async()=>{
 const dir=await tempDir('v21-cli-production');await cp(join(repoRoot,'examples/research-network/assets'),join(dir,'assets'),{recursive:true});
 const p=await v21Fixture();addQuantity(p);const path=join(dir,'project.json');await writeFile(path,JSON.stringify(p));
 const checked=await cli(['validate','--project',path]);expect(checked.code).toBe(0);expect(JSON.parse(checked.stdout).ok).toBe(true);
 const built=await cli(['compile','--project',path,'--out',join(dir,'build')]);expect(built.code).toBe(0);expect(JSON.parse(built.stdout).status).toBe('HELD');
 for(const file of ['density-ledger.json','numeral-review.json','manifests/evidence.md','sales-review-template.json'])expect((await readFile(join(dir,'build',file),'utf8')).length).toBeGreaterThan(0);
 const before=await readFile(join(repoRoot,'examples/research-network/project.json'),'utf8');const migrated=await cli(['migrate','--project',join(repoRoot,'examples/research-network/project.json'),'--out',join(dir,'migration')]);expect(migrated.code).toBe(0);expect(JSON.parse(migrated.stdout).status).toBe('HELD');expect(await readFile(join(repoRoot,'examples/research-network/project.json'),'utf8')).toBe(before);
});

test('one bound number cannot conceal another assertion that reuses the same numeral',async()=>{
 const p=await v21Fixture(),{b}=addQuantity(p);b.text+=' Carries 80 people.';expect(errors(p)).toContain('UNBOUND_NUMBER');
 b.text='180 nmi range for Fixture hull A.';expect(errors(p)).toContain('QUANTITY_NOT_VISIBLE');expect(errors(p)).toContain('UNBOUND_NUMBER');
});

test('quantity unit tokens are not satisfied by words or other text on the slide',async()=>{
 const p=await v21Fixture(),{b,c}=addQuantity(p);c.quantities![0].unit='kn';b.quantityUses![0].display='80 known vessels';b.text='80 known vessels for Fixture hull A.';expect(errors(p)).toContain('QUANTITY_UNIT_MISSING');
 c.quantities![0].unit='nmi';b.quantityUses![0].display='80';b.text='80 km range for Fixture hull A. Other figures use nmi.';expect(errors(p)).toContain('QUANTITY_UNIT_MISSING');
 c.quantities![0].unit='m';b.quantityUses![0].display='80 m';b.text='80 m range for Fixture hull A.';expect(errors(p)).toEqual([]);
 expect(normalizeNumericDisplay('80 m; 1.2M; $1.2m; 1.8 GW')).toEqual([80,1200000,1200000,1.8]);
});

test('evidence bands are refused on non-sales layouts before native output',async()=>{
 const p=await v21Fixture();const s=p.slides.find(s=>s.layout==='cover')!;s.footnotes=[{id:'cover-evidence',claimIds:[p.claims[0].id],sourceIds:[],text:'Synthetic claim note.'}];
 expect(errors(p)).toContain('FOOTNOTE_LAYOUT');expect(()=>compileProject(p,{allowUnresolvedAssets:true})).toThrow('FOOTNOTE_LAYOUT');
});

test('the serialized evidence fixture compiles every evidence-band composition without shrinking type',async()=>{
 const p=JSON.parse(await readFile(join(repoRoot,'examples/evidence-continuity/project.json'),'utf8'));
 const c=compileProject(p,{allowUnresolvedAssets:true});const sales=p.slides.filter((s:any)=>s.layout==='sales');
 expect(new Set(sales.map((s:any)=>s.composition)).size).toBe(8);
 for(const s of sales){const slide=c.slides.find(sl=>sl.key===s.key)!;const note=slide.elements.find(e=>e.role==='evidence-footnote')!;const box=slide.boxes.find(b=>b.objectId===note.objectId)!;expect(box.fontSize).toBe(8);expect(box.y).toBeCloseTo(357.4);}
 expect(c.warnings.filter(w=>w.code==='OUT_OF_CANVAS')).toEqual([]);
});

test('footnote-only private claims are not an export escape and rendered separators count',async()=>{
 const p=await v21Fixture(),{s,c}=addQuantity(p);p.meta.audience='partner';const privateClaim=structuredClone(c);privateClaim.id='private-note-only';privateClaim.clearedFor=['internal'];p.claims.push(privateClaim);s.footnotes!.push({id:'private-note',claimIds:[privateClaim.id],sourceIds:[],text:'Internal-only additional conclusion.'});
 expect(errors(p)).toContain('CLAIM_AUDIENCE_UNCLEARED');expect(errors(p)).toContain('FOOTNOTE_UNBOUND_CLAIM');
 s.footnotes=[{id:'range-note',claimIds:[c.id],sourceIds:[],text:'MODELED '+'.'.repeat(111)},{id:'second',claimIds:[c.id],sourceIds:[],text:'.'.repeat(118)}];
 expect(s.footnotes.map(f=>f.text).join(' ').length).toBeLessThanOrEqual(240);expect(errors(p)).toContain('FOOTNOTE_BUDGET');
});
