import { createHash } from 'node:crypto';
import { readFile, realpath, stat } from 'node:fs/promises';
import { dirname, isAbsolute, relative, resolve, sep } from 'node:path';
import type { Asset, Audience, Crop, Project, Visibility } from './types';

/**
 * A deliberately conservative, local-only catalogue.  The source project's
 * asset id remains the logical id; projectBinding and recordId keep the same
 * id from different projects from becoming one asset.
 */
export type RightsStatus = 'cleared' | 'held' | 'unknown';
export type AttachmentStatus = 'known' | 'unknown';
export type HashStatus = 'match' | 'mismatch' | 'missing' | 'unavailable';

export interface AttachmentRelations {
  status: AttachmentStatus;
  attachedMarkAssetIds: string[] | null;
  hullLogoAssetIds: string[] | null;
  /** The metadata keys that explicitly supplied the relation. */
  fields: string[];
}

export interface CropMetadata {
  focalPoint: { x: number; y: number } | null;
  protectedRegion: Crop | null;
  crop: Crop | null;
}

export interface RegistryProject {
  projectId: string;
  revision: string;
  title: string;
  projectPath: string;
  audience: Audience;
  classification: string;
  fictional: boolean;
}

export interface RegistryAsset {
  recordId: string;
  /** Asset.id from the source project. It is not globally unique. */
  logicalId: string;
  /** A readable project/id namespace; records are still not merged on this key. */
  projectBinding: string;
  project: RegistryProject;
  assetPath: string;
  /** Resolved only for local, safe paths; omitted when unavailable or unsafe. */
  localPath?: string;
  title: string;
  kind: Asset['kind'];
  maturity: Asset['maturity'];
  vessel?: string;
  missions: string[];
  geography: string[];
  roles: string[];
  sourceIds: string[];
  visibility: Visibility;
  clearedFor: Audience[];
  rightsStatus: RightsStatus;
  rightsNote: string;
  caption: string;
  declaredSha256: string;
  /** Exact bytes observed locally, when the source file was available. */
  observedSha256: string | null;
  /** The exact version used for duplicate/reuse matching. */
  exactVersionHash: string | null;
  hashStatus: HashStatus;
  crop: CropMetadata;
  /** Unknown is intentionally different from an explicit empty relation list. */
  attachments: AttachmentRelations;
  embeddingUrl?: string;
}

export interface RegistryCollision {
  logicalId: string;
  recordIds: string[];
  projectBindings: string[];
  exactVersionHashes: string[];
  reason: 'logical-id-reused';
}

export interface AssetReuseGroup {
  exactVersionHash: string;
  recordIds: string[];
  logicalIds: string[];
  projectBindings: string[];
  projectIds: string[];
  /** Most restrictive aggregate; source records remain unchanged. */
  rightsStatus: RightsStatus;
  visibility: Visibility;
  /** Intersection, never a union, to avoid upgrading clearance by duplication. */
  effectiveClearedFor: Audience[];
}

export interface AssetRegistry {
  schemaVersion: '1.0.0';
  projects: RegistryProject[];
  assets: RegistryAsset[];
  collisions: RegistryCollision[];
}

export interface RegistryQuery {
  mission?: string | string[];
  missions?: string[];
  vessel?: string;
  geography?: string | string[];
  role?: string | string[];
  roles?: string[];
  maturity?: Asset['maturity'] | Asset['maturity'][];
  clearance?: Audience | Audience[];
  rights?: RightsStatus | RightsStatus[];
  projectId?: string | string[];
  logicalId?: string | string[];
  exactVersionHash?: string;
}

export interface RegistrySearchResult {
  matches: RegistryAsset[];
  count: number;
}

const AUDIENCES: Audience[] = ['internal', 'partner', 'public'];
const VISIBILITY_ORDER: Record<Visibility, number> = { public: 0, internal: 1, restricted: 2 };
const RIGHTS_ORDER: Record<RightsStatus, number> = { cleared: 0, unknown: 1, held: 2 };
const HEX_64 = /^[a-f0-9]{64}$/i;

function asRecord(value: unknown): Record<string, any> {
  return value && typeof value === 'object' && !Array.isArray(value) ? value as Record<string, any> : {};
}

function asStrings(value: unknown): string[] {
  if (!Array.isArray(value)) return [];
  return value.filter((item): item is string => typeof item === 'string' && item.length > 0);
}

function normalizedList(value: string | string[] | undefined): string[] {
  const list = Array.isArray(value) ? value : value === undefined ? [] : [value];
  return list.map(item => item.toLocaleLowerCase()).filter(Boolean);
}

function unique(values: string[]): string[] { return [...new Set(values)]; }

function pathIsSafe(value: string): boolean {
  if (!value || value.includes('\0') || isAbsolute(value) || /^[/\\]/.test(value) || /^[a-zA-Z]:[\\/]/.test(value)) return false;
  if (/^[a-zA-Z][a-zA-Z0-9+.-]*:/.test(value)) return false;
  return !value.replaceAll('\\', '/').split('/').includes('..');
}

function inside(root: string, candidate: string): boolean {
  const rel = relative(root, candidate);
  return rel === '' || (rel !== '..' && !rel.startsWith(`..${sep}`) && !isAbsolute(rel));
}

function issueText(value: unknown): string {
  return typeof value === 'string' ? value : '';
}

function explicitRightsStatus(asset: Record<string, any>): RightsStatus | undefined {
  const direct = asset.rightsStatus ?? asRecord(asset.rights).status;
  if (direct === 'cleared' || direct === 'held' || direct === 'unknown') return direct;
  if (asset.rightsCleared === true) return 'cleared';
  if (asset.rightsCleared === false) return 'held';
  return undefined;
}

function classifyRights(asset: Record<string, any>): RightsStatus {
  const explicit = explicitRightsStatus(asset);
  if (explicit) return explicit;
  const note = issueText(asset.rightsNote).toLocaleLowerCase();
  // These phrases are only conservative holds; absence of a phrase is not clearance.
  if (/\b(hold|held|internal workflow use only|no external clearance|not cleared|confirm (?:reuse|permission)|permission (?:is )?limited|external circulation)/i.test(note)) return 'held';
  if (/\b(rights? cleared|cleared for (?:external|partner|public)|original synthetic|permission granted|approved for reuse)/i.test(note)) return 'cleared';
  return 'unknown';
}

function stringRefs(value: unknown): string[] {
  if (!Array.isArray(value)) return typeof value === 'string' && value ? [value] : [];
  return value.map(item => {
    if (typeof item === 'string') return item;
    const record = asRecord(item);
    return issueText(record.assetId ?? record.id ?? record.ref);
  }).filter(Boolean);
}

function attachmentRelations(asset: Record<string, any>): AttachmentRelations {
  const markKeys = ['attachedMarks', 'attachedMarkAssetIds'];
  const hullKeys = ['hullLogoAssetIds', 'attachedHullLogos', 'hullLogoAssetId'];
  const markKey = markKeys.find(key => Object.prototype.hasOwnProperty.call(asset, key));
  const hullKey = hullKeys.find(key => Object.prototype.hasOwnProperty.call(asset, key));
  const markValue = markKey ? asset[markKey] : undefined;
  const hullValue = hullKey ? asset[hullKey] : undefined;
  const fields = [markKey, hullKey].filter((x): x is string => Boolean(x));
  if (!fields.length) return { status: 'unknown', attachedMarkAssetIds: null, hullLogoAssetIds: null, fields: [] };
  return {
    status: 'known',
    attachedMarkAssetIds: markKey ? unique(stringRefs(markValue)) : null,
    hullLogoAssetIds: hullKey ? unique(stringRefs(hullValue)) : null,
    fields,
  };
}

function cropMetadata(asset: Record<string, any>): CropMetadata {
  const focal = asRecord(asset.focalPoint);
  const focalPoint = Number.isFinite(focal.x) && Number.isFinite(focal.y) ? { x: Number(focal.x), y: Number(focal.y) } : null;
  const crop = asRecord(asset.crop);
  const protectedRegion = asRecord(asset.keepRegion ?? asset.protectedRegion);
  const asCrop = (value: Record<string, any>): Crop | null => {
    const values = ['left', 'top', 'right', 'bottom'].map(key => Number(value[key]));
    return values.every(Number.isFinite) ? { left: values[0], top: values[1], right: values[2], bottom: values[3] } : null;
  };
  return { focalPoint, protectedRegion: asCrop(protectedRegion), crop: asCrop(crop) };
}

async function localHash(projectPath: string, assetPath: string): Promise<{ path?: string; observedSha256: string | null; status: HashStatus }> {
  if (!pathIsSafe(assetPath)) return { observedSha256: null, status: 'unavailable' };
  const root = dirname(projectPath);
  const candidate = resolve(root, assetPath);
  if (!inside(root, candidate)) return { observedSha256: null, status: 'unavailable' };
  try {
    const resolved = await realpath(candidate);
    if (!inside(root, resolved) || !(await stat(resolved)).isFile()) return { observedSha256: null, status: 'missing' };
    const bytes = await readFile(resolved);
    return { path: resolved, observedSha256: createHash('sha256').update(bytes).digest('hex'), status: 'match' };
  } catch {
    return { observedSha256: null, status: 'missing' };
  }
}

function recordId(projectPath: string, projectId: string, logicalId: string, versionHash: string | null, ordinal: number): string {
  return createHash('sha256').update([projectPath, projectId, logicalId, versionHash ?? 'no-version-hash', String(ordinal)].join('\0')).digest('hex').slice(0, 24);
}

async function loadProject(projectPathInput: string): Promise<{ projectPath: string; project: Project }> {
  const projectPath = await realpath(resolve(projectPathInput));
  const parsed = JSON.parse(await readFile(projectPath, 'utf8')) as Project;
  if (!parsed || !parsed.meta || !Array.isArray(parsed.assets)) throw new Error(`Invalid project file (expected meta and assets): ${projectPathInput}`);
  return { projectPath, project: parsed };
}

export async function buildRegistry(projectPaths: string[]): Promise<AssetRegistry> {
  if (!projectPaths.length) throw new Error('At least one project path is required.');
  const loadedRaw = await Promise.all(projectPaths.map(loadProject));
  // Repeating the same canonical path in a list must not manufacture a second binding.
  const loaded = [...new Map(loadedRaw.map(item => [item.projectPath, item])).values()];
  loaded.sort((a, b) => a.projectPath.localeCompare(b.projectPath));
  const projects: RegistryProject[] = [];
  const assets: RegistryAsset[] = [];
  for (const { projectPath, project } of loaded) {
    const projectRecord: RegistryProject = {
      projectId: issueText(project.meta.projectId), revision: issueText(project.meta.revision), title: issueText(project.meta.title),
      projectPath, audience: project.meta.audience, classification: issueText(project.meta.classification), fictional: Boolean(project.meta.fictional),
    };
    projects.push(projectRecord);
    const ordinals = new Map<string, number>();
    for (const sourceAsset of project.assets) {
      const asset = asRecord(sourceAsset);
      const logicalId = issueText(asset.id);
      const ordinal = ordinals.get(logicalId) ?? 0;
      ordinals.set(logicalId, ordinal + 1);
      const declaredSha256 = issueText(asset.sha256).toLowerCase();
      const local = await localHash(projectPath, issueText(asset.path));
      const exactVersionHash = local.observedSha256 ?? (HEX_64.test(declaredSha256) ? declaredSha256 : null);
      const hashStatus: HashStatus = local.observedSha256 ? (HEX_64.test(declaredSha256) && local.observedSha256 !== declaredSha256 ? 'mismatch' : 'match') : local.status;
      const binding = `${projectRecord.projectId}:${logicalId}`;
      assets.push({
        recordId: recordId(projectPath, projectRecord.projectId, logicalId, exactVersionHash, ordinal), logicalId, projectBinding: binding,
        project: projectRecord, assetPath: issueText(asset.path), ...(local.path ? { localPath: local.path } : {}), title: issueText(asset.title),
        kind: asset.kind, maturity: asset.maturity, ...(asset.vessel ? { vessel: issueText(asset.vessel) } : {}), missions: asStrings(asset.missions),
        geography: asStrings(asset.geography), roles: asStrings(asset.roles), sourceIds: asStrings(asset.sourceIds), visibility: asset.visibility,
        clearedFor: asStrings(asset.clearedFor) as Audience[], rightsStatus: classifyRights(asset), rightsNote: issueText(asset.rightsNote),
        caption: issueText(asset.caption), declaredSha256, observedSha256: local.observedSha256, exactVersionHash, hashStatus,
        crop: cropMetadata(asset), attachments: attachmentRelations(asset), ...(asset.embeddingUrl ? { embeddingUrl: issueText(asset.embeddingUrl) } : {}),
      });
    }
  }
  assets.sort((a, b) => a.project.projectPath.localeCompare(b.project.projectPath) || a.logicalId.localeCompare(b.logicalId) || a.recordId.localeCompare(b.recordId));
  const byLogical = new Map<string, RegistryAsset[]>();
  for (const asset of assets) byLogical.set(asset.logicalId, [...(byLogical.get(asset.logicalId) ?? []), asset]);
  const collisions: RegistryCollision[] = [...byLogical.entries()].filter(([, records]) => records.length > 1).map(([logicalId, records]) => ({
    logicalId, recordIds: records.map(record => record.recordId), projectBindings: unique(records.map(record => record.projectBinding)),
    exactVersionHashes: unique(records.map(record => record.exactVersionHash).filter((hash): hash is string => Boolean(hash))), reason: 'logical-id-reused',
  }));
  return { schemaVersion: '1.0.0', projects, assets, collisions };
}

function matchesAny(value: string | undefined, query: string | string[]): boolean {
  if (!value) return false;
  const terms = normalizedList(query);
  return terms.some(term => value.toLocaleLowerCase() === term || value.toLocaleLowerCase().includes(term));
}
function listMatches(values: string[], query: string | string[]): boolean {
  const terms = normalizedList(query);
  return terms.some(term => values.some(value => value.toLocaleLowerCase() === term || value.toLocaleLowerCase().includes(term)));
}
function enumMatches(value: string, query: string | string[] | undefined): boolean { return query === undefined || normalizedList(query).includes(value.toLocaleLowerCase()); }

export function searchRegistry(registry: AssetRegistry, query: RegistryQuery = {}): RegistrySearchResult {
  const missions = query.missions ?? query.mission;
  const roles = query.roles ?? query.role;
  const geography = query.geography;
  const clearances = query.clearance;
  const projectIds = query.projectId;
  const logicalIds = query.logicalId;
  const matches = registry.assets.filter(asset =>
    (!missions || listMatches(asset.missions, missions)) && (!query.vessel || matchesAny(asset.vessel, query.vessel)) &&
    (!geography || listMatches(asset.geography, geography)) && (!roles || listMatches(asset.roles, roles)) &&
    enumMatches(asset.maturity, query.maturity) && enumMatches(asset.rightsStatus, query.rights) &&
    (!clearances || listMatches(asset.clearedFor, clearances)) && (!projectIds || matchesAny(asset.project.projectId, projectIds)) &&
    (!logicalIds || matchesAny(asset.logicalId, logicalIds)) && (!query.exactVersionHash || asset.exactVersionHash === query.exactVersionHash.toLowerCase())
  );
  return { matches, count: matches.length };
}

function restrictiveRights(statuses: RightsStatus[]): RightsStatus { return statuses.reduce((best, status) => RIGHTS_ORDER[status] > RIGHTS_ORDER[best] ? status : best, 'cleared'); }
function restrictiveVisibility(values: Visibility[]): Visibility { return values.reduce((best, value) => VISIBILITY_ORDER[value] > VISIBILITY_ORDER[best] ? value : best, 'public'); }
function intersection<T extends string>(lists: T[][]): T[] { return lists.length ? lists[0].filter(value => lists.every(list => list.includes(value))) : []; }

export function reuseReport(registry: AssetRegistry): { groups: AssetReuseGroup[]; reusableVersionCount: number; reusedRecordCount: number } {
  const groups = new Map<string, RegistryAsset[]>();
  for (const asset of registry.assets) if (asset.exactVersionHash) groups.set(asset.exactVersionHash, [...(groups.get(asset.exactVersionHash) ?? []), asset]);
  const report = [...groups.entries()].map(([exactVersionHash, records]) => ({
    exactVersionHash, recordIds: records.map(record => record.recordId), logicalIds: unique(records.map(record => record.logicalId)),
    projectBindings: unique(records.map(record => record.projectBinding)), projectIds: unique(records.map(record => record.project.projectId)),
    rightsStatus: restrictiveRights(records.map(record => record.rightsStatus)), visibility: restrictiveVisibility(records.map(record => record.visibility)),
    effectiveClearedFor: intersection(records.map(record => record.clearedFor)),
  })).sort((a, b) => a.exactVersionHash.localeCompare(b.exactVersionHash));
  return { groups: report, reusableVersionCount: report.filter(group => group.recordIds.length > 1).length, reusedRecordCount: report.filter(group => group.recordIds.length > 1).reduce((n, group) => n + group.recordIds.length, 0) };
}

function htmlEscape(value: unknown): string {
  return String(value ?? '').replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#39;');
}
function localThumbnail(record: RegistryAsset, outputPath: string): string | null {
  if (!record.localPath) return null;
  const path = relative(dirname(outputPath), record.localPath).split(sep).join('/');
  return path && !/^[a-zA-Z][a-zA-Z0-9+.-]*:/.test(path) ? path : null;
}

export function registryMarkdown(registry: AssetRegistry, records = registry.assets, outputPath?: string): string {
  const lines = ['# Local asset registry shortlist', '', `Assets: ${records.length}`, '', '| Asset | Project | Maturity | Rights | Clearance | Missions | Version |', '|---|---|---|---|---|---|---|'];
  for (const record of records) {
    const thumb = outputPath ? localThumbnail(record, outputPath) : null;
    const title = thumb ? `[${record.title || record.logicalId}](${thumb})` : (record.title || record.logicalId);
    lines.push(`| ${title.replaceAll('|', '\\|')} | ${record.project.projectId} | ${record.maturity} | ${record.rightsStatus} | ${record.clearedFor.join(', ') || 'none'} | ${record.missions.join(', ') || '—'} | ${(record.exactVersionHash ?? 'unavailable').slice(0, 12)} |`);
  }
  return lines.join('\n') + '\n';
}

export function registryHtml(registry: AssetRegistry, records = registry.assets, outputPath = 'contact-sheet.html'): string {
  const cards = records.map(record => {
    const thumb = localThumbnail(record, outputPath);
    const image = thumb ? `<img src="${htmlEscape(thumb)}" alt="${htmlEscape(record.caption || record.title)}" loading="lazy">` : '<div class="no-image">No local thumbnail</div>';
    return `<article><div class="thumb">${image}</div><h2>${htmlEscape(record.title || record.logicalId)}</h2><p><b>${htmlEscape(record.project.projectId)}</b> · ${htmlEscape(record.logicalId)}</p><p>${htmlEscape(record.maturity)} · ${htmlEscape(record.rightsStatus)} · ${htmlEscape(record.visibility)}</p><p>${htmlEscape(record.missions.join(', ') || 'No mission tag')}<br>${htmlEscape(record.roles.join(', ') || 'No role tag')}</p><small>version ${htmlEscape(record.exactVersionHash ?? 'unavailable')}<br>attachments: ${htmlEscape(record.attachments.status)}</small></article>`;
  }).join('\n');
  return `<!doctype html><meta charset="utf-8"><title>Local asset registry shortlist</title><style>body{font:14px system-ui;background:#101216;color:#eee;margin:24px}main{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}article{background:#1b1e25;border:1px solid #383d48;border-radius:8px;padding:12px;overflow:hidden}.thumb{height:150px;background:#0b0d10;display:grid;place-items:center}.thumb img{max-width:100%;max-height:150px;object-fit:contain}h2{font-size:17px;margin:12px 0 6px}p{line-height:1.35;margin:6px 0}.no-image{color:#9097a5}small{color:#b7bfcb;word-break:break-word}</style><h1>Local asset registry shortlist</h1><p>${records.length} asset records · local files only · no rights decision implied</p><main>${cards}</main>`;
}

export function summarizeRegistry(registry: AssetRegistry): Record<string, unknown> {
  const reuse = reuseReport(registry);
  return { schemaVersion: registry.schemaVersion, projects: registry.projects.length, assets: registry.assets.length, collisions: registry.collisions.length, reusableVersions: reuse.reusableVersionCount, reusedRecords: reuse.reusedRecordCount };
}
