import { createHash } from 'node:crypto';
import { access, mkdir, readFile, writeFile } from 'node:fs/promises';
import { dirname, join, resolve, basename } from 'node:path';
import type { Project, Asset, ReviewReceipt, CompiledDeck } from './types';
import { compileProject } from './render';
import { sha256 } from './primitives';
import { validateProject } from './validate';

export const PACKAGE_VERSION = '1.0.0';
export const DISPLAY_NAME_LIMIT = 42;
export const LEGAL_ENTITY_LIMIT = 64;

export class PackageError extends Error {
  constructor(message: string) { super(message); this.name = 'PackageError'; }
}

export function canonicalJson(value: unknown): string {
  const sort = (v: unknown): unknown => Array.isArray(v) ? v.map(sort) : v && typeof v === 'object' ? Object.fromEntries(Object.keys(v as Record<string, unknown>).sort().map(k => [k, sort((v as Record<string, unknown>)[k])])) : v;
  return JSON.stringify(sort(value));
}
export function digest(value: unknown): string { return createHash('sha256').update(typeof value === 'string' ? value : canonicalJson(value)).digest('hex'); }

async function exists(path: string): Promise<boolean> { try { await access(path); return true; } catch { return false; } }
async function json(path: string): Promise<any> {
  try { return JSON.parse(await readFile(path, 'utf8')); }
  catch (error) { throw new PackageError(`Cannot read JSON project ${path}: ${error instanceof Error ? error.message : String(error)}`); }
}
export async function readProject(path: string): Promise<Project> {
  const value = await json(resolve(path));
  if (!value || typeof value !== 'object') throw new PackageError(`Project ${path} is not a JSON object.`);
  return value as Project;
}
async function writeNew(path: string, content: string): Promise<void> {
  if (await exists(path)) {
    const old = await readFile(path, 'utf8');
    if (old !== content) throw new PackageError(`Refusing to overwrite existing file: ${path}`);
    return;
  }
  await mkdir(dirname(path), { recursive: true });
  await writeFile(path, content, { flag: 'wx' });
}
export async function writeDeterministicJson(path: string, value: unknown): Promise<void> { await writeNew(path, JSON.stringify(value, null, 2) + '\n'); }

function displayName(value: string, label: string, max: number): string {
  const clean = value.trim();
  if (!clean) throw new PackageError(`${label} is required.`);
  if (clean.length > max) throw new PackageError(`${label} is ${clean.length} characters; the editorial display budget is ${max}. Shorten it rather than shrinking text.`);
  return clean;
}

function intakeProject(partner: string, entity: string): Project {
  return {
    schemaVersion: '1.0.0',
    meta: {
      projectId: 'intake_replace_me', revision: 'r0', title: 'Incomplete strategic partnership intake',
      company: 'Company name to replace', partner, legalEntity: entity, audience: 'internal', archetype: 'strategic',
      objective: 'Replace this fictional intake with an approved objective and evidence.',
      meetingAudience: 'Internal working group', date: '2000-01-01', classification: 'INCOMPLETE INTAKE', fictional: true,
      footer: 'FICTIONAL INTAKE — REPLACE BEFORE PRODUCTION',
    },
    sources: [], claims: [], assets: [], opportunities: [], slides: [],
    policy: { forbiddenTerms: [], forbiddenPartnerNames: [], requiredPhrases: [], allowMissingLogosForInternalReview: true },
  };
}

export async function initPackage(out: string, partnerInput: string, entityInput: string): Promise<{ projectPath: string; holdPath: string; project: Project }> {
  const partner = displayName(partnerInput, 'Partner display name', DISPLAY_NAME_LIMIT);
  const entity = displayName(entityInput, 'Legal entity display name', LEGAL_ENTITY_LIMIT);
  const root = resolve(out);
  const projectPath = join(root, 'project.json');
  const holdPath = join(root, 'INCOMPLETE-INTAKE.md');
  const holdJsonPath = join(root, 'INCOMPLETE-INTAKE.json');
  for (const path of [projectPath, holdPath, holdJsonPath]) if (await exists(path)) throw new PackageError(`Refusing to overwrite existing file: ${path}`);
  const project = intakeProject(partner, entity);
  const hold = {
    status: 'HELD', kind: 'INCOMPLETE-INTAKE', fictional: true,
    message: 'This scaffold contains no real claims, assets, approvals, partner binding, or production-ready content.',
    requiredBeforeProduction: ['Replace every fictional field and demo identity.', 'Add source-linked claims and locally archived assets.', 'Run validation, editorial review, comprehension review, visual review, and native QA.', 'Do not present this scaffold as ready for a real partner.'],
  };
  await mkdir(root, { recursive: true });
  await writeNew(projectPath, JSON.stringify(project, null, 2) + '\n');
  await writeNew(holdPath, '# INCOMPLETE-INTAKE — HELD\n\nThis is a fictional scaffold only. Replace demo data before production; it is not ready for a real partner.\n\n- No real claims or evidence are present.\n- No assets or logos are present.\n- No approval, native render, or QA has occurred.\n- Replace every fictional field, then validate and review.\n');
  await writeDeterministicJson(holdJsonPath, hold);
  return { projectPath, holdPath, project };
}

export async function validatePackage(projectPath: string, publicMode = false) {
  const project = await readProject(projectPath);
  const result = await validateProject(project, { projectRoot: dirname(resolve(projectPath)), checkFiles: true, forPublication: publicMode || project.meta?.audience === 'public' });
  return { project, result };
}

function collectAssetIds(value: unknown, output = new Set<string>()): Set<string> {
  if (Array.isArray(value)) value.forEach(v => collectAssetIds(v, output));
  else if (value && typeof value === 'object') for (const [key, child] of Object.entries(value)) key === 'assetId' && typeof child === 'string' ? output.add(child) : collectAssetIds(child, output);
  return output;
}
function selectedAssets(project: Project, compiled: CompiledDeck): Asset[] {
  const ids = new Set(compiled.assetUses.map(u => u.assetId));
  return [...ids].map(id => project.assets.find(a => a.id === id)).filter((a): a is Asset => !!a);
}
function visibleMarkdown(compiled: CompiledDeck): string {
  return ['# Visible copy', '', '> Offline package output. This is not a native render or visual QA.', '', ...compiled.slides.flatMap((s, i) => [`## ${i + 1}. ${s.key} (${s.layout})`, '', ...s.visibleText.map(t => `- ${t}`), ''])].join('\n');
}
function storyboardMarkdown(project: Project, compiled: CompiledDeck): string {
  const byId = new Map(project.assets.map(a => [a.id, a]));
  const logoIds = [project.meta.companyLogoAssetId, project.meta.partnerLogoAssetId].filter((id): id is string => !!id);
  const logoLines = logoIds.map(id => byId.get(id)).filter((a): a is Asset => !!a).map(a => `- \`${basename(a.path)}\` — ${a.caption}`);
  return ['# Storyboard', '', '> Offline storyboard only. Asset URLs may be unresolved `asset://` placeholders; native render and QA have not occurred.', '', '## Selected deck marks', ...(logoLines.length ? logoLines : ['- none']), '', ...compiled.slides.flatMap((s, i) => {
    const source = project.slides.find(x => x.key === s.key)!;
    const ids = [...collectAssetIds(source)];
    const assets = ids.map(id => byId.get(id)).filter((a): a is Asset => !!a);
    const refs = `Claims: ${(source.claimIds || []).join(', ') || 'none'} | Sources: ${(source.sourceIds || []).join(', ') || 'none'} | Opportunities: ${(source.opportunityIds || []).join(', ') || 'none'}`;
    const asks = [source.layout === 'close' ? source.ask : undefined, 'explore' in source ? source.explore : undefined].filter(Boolean).join(' / ') || 'No ask recorded.';
    return [`## ${i + 1}. ${s.key}`, `- Layout: ${s.layout}`, `- ${refs}`, `- Ask / exploration: ${asks}`, `- Selected assets: ${assets.length ? assets.map(a => `\`${basename(a.path)}\` — ${a.caption}`).join('; ') : 'none'}`, ''];
  })].join('\n');
}
function contentSource(project: Project) {
  return { schemaVersion: '1.0.0', projectId: project.meta.projectId, fictional: project.meta.fictional, sources: project.sources, claims: project.claims, opportunities: project.opportunities, note: 'Claims and source locators are editorial inputs; this package does not certify them.' };
}
function imageManifest(project: Project, compiled: CompiledDeck, urls: Record<string, string>) {
  return { schemaVersion: '1.0.0', images: selectedAssets(project, compiled).map(a => ({ assetId: a.id, filename: basename(a.path), path: a.path, sha256: a.sha256, width: a.width, height: a.height, mimeType: a.mimeType, caption: a.caption, resolvedUrl: urls[a.id] || a.embeddingUrl || `asset://${a.id}`, uses: compiled.assetUses.filter(u => u.assetId === a.id).map(u => ({ slideKey: u.slideKey, role: u.role })) })) };
}
function reviewTemplate(project: Project, stage: ReviewReceipt['stage'], subjectHash = digest(project)) {
  return { schemaVersion: '1.0.0', stage, subjectHash, decision: 'held', status: 'HELD', reviewer: '', reviewedAt: '', notes: 'Unsigned template only. A human must perform and record the review; this file is never an approval.', signature: null, fictional: project.meta.fictional };
}

export async function compilePackage(projectPath: string, out: string, urlsPath?: string): Promise<{ compiled: CompiledDeck; manifest: any; out: string }> {
  const project = await readProject(projectPath);
  const result = await validateProject(project, { projectRoot: dirname(resolve(projectPath)), checkFiles: true, forPublication: project.meta?.audience === 'public' });
  if (!result.ok) throw new PackageError(`Project validation failed: ${result.issues.filter(i => i.severity === 'error').slice(0, 8).map(i => `${i.code} at ${i.path}`).join('; ')}`);
  let urls: Record<string, string> = {};
  if (urlsPath) { const value = await json(urlsPath); if (!value || typeof value !== 'object' || Array.isArray(value)) throw new PackageError('--urls must point to a JSON object mapping asset IDs to URLs.'); urls = value; }
  const compiled = compileProject(project, { assetUrls: urls, allowUnresolvedAssets: true });
  const projectHash = sha256(project), compiledHash = sha256(compiled);
  const assets = selectedAssets(project, compiled);
  const holds = [
    ...result.issues.filter(i => i.severity !== 'warning').map(i => `${i.severity.toUpperCase()}: ${i.code} at ${i.path} — ${i.message}`),
    ...compiled.warnings.map(w => `${w.code} at ${w.path} — ${w.message}`),
    ...assets.filter(a => !urls[a.id] && !a.embeddingUrl).map(a => `UNRESOLVED_ASSET at assets.${a.id} — offline asset://${a.id} placeholder remains`),
    'NATIVE_RENDER_NOT_PERFORMED — compile output is not a native deck or visual QA result.',
  ];
  const root = resolve(out);
  if (await exists(join(root, 'build-manifest.json'))) {
    const old = await json(join(root, 'build-manifest.json'));
    if (old.inputHash && old.inputHash !== projectHash) throw new PackageError(`Existing build belongs to different input (${old.inputHash}); use a new build directory.`);
  }
  const artifacts: Record<string, string> = {
    'compiled.json': JSON.stringify(compiled, null, 2) + '\n',
    'visible-copy.md': visibleMarkdown(compiled),
    'storyboard.md': storyboardMarkdown(project, compiled),
    'content-source.json': JSON.stringify(contentSource(project), null, 2) + '\n',
    'image-manifest.json': JSON.stringify(imageManifest(project, compiled, urls), null, 2) + '\n',
    'review-template.json': JSON.stringify(reviewTemplate(project, 'storyboard', compiled.inputHash), null, 2) + '\n',
  };
  const artifactHashes = Object.fromEntries(Object.entries(artifacts).map(([name, value]) => [name, digest(value)]));
  const manifest = { schemaVersion: '1.0.0', packageVersion: PACKAGE_VERSION, projectId: project.meta.projectId, revision: project.meta.revision, inputHash: projectHash, compiledHash, artifactHashes, status: holds.length ? 'HELD' : 'READY_FOR_REVIEW', holds, nativeRender: 'not-performed', visualQa: 'not-performed' };
  artifacts['build-manifest.json'] = JSON.stringify(manifest, null, 2) + '\n';
  for (const [name, value] of Object.entries(artifacts)) await writeNew(join(root, name), value);
  return { compiled, manifest, out: root };
}

export async function searchAssets(projectPath: string, term: string): Promise<{ query: string; assets: unknown[] }> {
  const project = await readProject(projectPath);
  if (!Array.isArray(project.assets)) throw new PackageError('Project assets catalogue is missing or invalid.');
  const q = term.trim().toLocaleLowerCase();
  if (!q) throw new PackageError('Asset query must not be empty.');
  const matches = project.assets.filter(a => [a.title, a.vessel, ...a.missions, ...a.geography, ...a.roles].filter(Boolean).some(v => String(v).toLocaleLowerCase().includes(q)));
  return { query: term, assets: matches.map(a => ({ id: a.id, filename: basename(a.path), title: a.title, kind: a.kind, maturity: a.maturity, missions: a.missions, vessel: a.vessel, geography: a.geography, roles: a.roles, caption: a.caption, sha256: a.sha256, width: a.width, height: a.height })) };
}

export async function writeReviewTemplate(projectPath: string, stage: ReviewReceipt['stage'], out: string): Promise<any> {
  if (!['storyboard', 'comprehension', 'visual', 'release'].includes(stage)) throw new PackageError(`Unknown review stage ${stage}; use storyboard, comprehension, visual, or release.`);
  const { project, result } = await validatePackage(projectPath, false);
  if (!result.ok) throw new PackageError(`Project validation failed: ${result.issues.filter(i => i.severity === 'error').slice(0, 8).map(i => `${i.code} at ${i.path}`).join('; ')}`);
  const value = reviewTemplate(project, stage);
  await writeDeterministicJson(join(resolve(out), 'review-template.json'), value);
  return value;
}

export function cliUsage(): string {
  return 'Usage:\n  bun src/cli.ts init --out <new-dir> --partner <name> --entity <legal entity>\n  bun src/cli.ts validate --project <project.json> [--public]\n  bun src/cli.ts compile --project <project.json> --out <new-build-dir> [--urls <asset-url-map.json>]\n  bun src/cli.ts assets --project <project.json> --query <term>\n  bun src/cli.ts review-template --project <project.json> --stage storyboard|comprehension|visual|release --out <dir>';
}
