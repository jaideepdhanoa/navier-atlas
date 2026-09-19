import { describe, expect, test } from 'bun:test';
import { cp, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { join, dirname, resolve } from 'node:path';
import { initPackage, compilePackage, searchAssets, writeReviewTemplate, PackageError, validatePackage } from '../src/package';

const root = resolve(dirname(import.meta.path), '..');
const demo = join(root, 'examples/public-demo/project.json');
const assetRoot = join(root, 'examples/public-demo');

async function temp(name: string) { return mkdtemp(join('/tmp', `strategic-package-${name}-`)); }
async function copyDemo(out: string) { await cp(assetRoot, join(out, 'demo'), { recursive: true }); return join(out, 'demo/project.json'); }

 describe('local package entrypoint', () => {
  test('validates and compiles the seven-layout fictional demo deterministically', async () => {
    const checked = await validatePackage(demo, true);
    expect(checked.result.ok).toBe(true);
    expect(checked.project.slides).toHaveLength(7);
    const out = await temp('deterministic');
    const a = await compilePackage(demo, join(out, 'build'));
    const first = await readFile(join(out, 'build/build-manifest.json'), 'utf8');
    const b = await compilePackage(demo, join(out, 'build'));
    expect(a.manifest.inputHash).toBe(b.manifest.inputHash);
    expect(first).toBe(await readFile(join(out, 'build/build-manifest.json'), 'utf8'));
    await rm(out, { recursive: true, force: true });
  });

  test('image manifest uses the same project embedding URL as the compiled native requests', async () => {
    const out = await temp('image-urls');
    const project = await copyDemo(out);
    const value = JSON.parse(await readFile(project, 'utf8'));
    const selected = value.assets[0];
    selected.embeddingUrl = 'https://example.invalid/fixture-image.png';
    await writeFile(project, JSON.stringify(value, null, 2) + '\n');
    const result = await compilePackage(project, join(out, 'build'));
    const manifest = JSON.parse(await readFile(join(out, 'build/image-manifest.json'), 'utf8'));
    expect(manifest.images.find((a: any) => a.assetId === selected.id).resolvedUrl).toBe(selected.embeddingUrl);
    expect(JSON.stringify(result.compiled.requests)).toContain(selected.embeddingUrl);
    await rm(out, { recursive: true, force: true });
  });

  test('exercises two, three, and four gallery counts in the fixture', async () => {
    const project = (await validatePackage(demo, true)).project;
    expect(project.slides.find(s => s.layout === 'models')?.models).toHaveLength(2);
    expect(project.slides.find(s => s.layout === 'options')?.options).toHaveLength(3);
    expect(project.slides.find(s => s.layout === 'missions')?.cards).toHaveLength(4);
  });

  test('init creates an explicit hold and refuses overwrite or long display names', async () => {
    const out = await temp('init');
    const created = await initPackage(join(out, 'intake'), 'Example Vessel Company', 'Example Vessel Company Ltd');
    expect((await readFile(created.holdPath, 'utf8')).includes('INCOMPLETE-INTAKE')).toBe(true);
    await expect(initPackage(join(out, 'intake'), 'Example Vessel Company', 'Example Vessel Company Ltd')).rejects.toThrow('Refusing to overwrite');
    await expect(initPackage(join(out, 'too-long'), 'A'.repeat(43), 'Example Ltd')).rejects.toThrow('editorial display budget');
    await rm(out, { recursive: true, force: true });
  });

  test('stale build input and missing local assets are held or rejected without replacement', async () => {
    const out = await temp('stale');
    const project = await copyDemo(out);
    const build = join(out, 'build');
    await compilePackage(project, build);
    const changed = JSON.parse(await readFile(project, 'utf8'));
    changed.meta.revision = 'r2';
    await writeFile(project, JSON.stringify(changed, null, 2) + '\n');
    await expect(compilePackage(project, build)).rejects.toThrow('different input');
    const missing = await copyDemo(out);
    await rm(join(out, 'demo/assets/service-schematic.svg'));
    const result = await validatePackage(missing, true);
    expect(result.result.issues.some(i => i.code === 'ASSET_FILE_MISSING')).toBe(true);
    await rm(out, { recursive: true, force: true });
  });

  test('public validation rejects synthetic private records and review templates remain held', async () => {
    const out = await temp('privacy');
    const project = await copyDemo(out);
    const value = JSON.parse(await readFile(project, 'utf8'));
    value.sources[0].visibility = 'internal';
    await writeFile(project, JSON.stringify(value, null, 2) + '\n');
    const checked = await validatePackage(project, true);
    expect(checked.result.issues.some(i => i.code === 'PUBLIC_SOURCE_PRIVATE')).toBe(true);
    const template = await writeReviewTemplate(demo, 'release', join(out, 'review'));
    expect(template.status).toBe('HELD');
    expect(template.decision).toBe('held');
    expect(template.reviewer).toBe('');
    await rm(out, { recursive: true, force: true });
  });

  test('asset search returns compact matches and unknown terms do not invent assets', async () => {
    const found = await searchAssets(demo, 'SERVICE');
    expect(found.assets.length).toBeGreaterThan(0);
    expect((await searchAssets(demo, 'not-a-real-tag')).assets).toHaveLength(0);
    await expect(searchAssets(demo, '')).rejects.toThrow('must not be empty');
  });
 });
