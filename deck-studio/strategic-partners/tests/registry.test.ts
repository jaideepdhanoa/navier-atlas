import { describe, expect, test } from 'bun:test';
import { createHash } from 'node:crypto';
import { mkdir, mkdtemp, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { buildRegistry, registryHtml, registryMarkdown, reuseReport, searchRegistry } from '../src/registry';

const hash = (bytes: Uint8Array) => createHash('sha256').update(bytes).digest('hex');
const image = Buffer.from('<svg xmlns="http://www.w3.org/2000/svg" width="20" height="10"><rect width="20" height="10"/></svg>');

function project(projectId: string, assetOverrides: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    schemaVersion: '1.0.0',
    meta: { projectId, revision: 'r1', title: `${projectId} fixture`, company: 'Fictional Co', partner: 'Fictional Partner', legalEntity: 'Fictional Co Ltd', audience: 'internal', archetype: 'industrial', objective: 'fixture', meetingAudience: 'fixture', date: '2026-09-18', classification: 'fictional test', fictional: true, footer: 'FICTIONAL', },
    sources: [], claims: [], opportunities: [], slides: [], policy: { forbiddenTerms: [], forbiddenPartnerNames: [], requiredPhrases: [], allowMissingLogosForInternalReview: true },
    assets: [{ id: 'shared_asset', title: 'Fictional boat', path: 'assets/boat.svg', sha256: hash(image), width: 20, height: 10, mimeType: 'image/svg+xml', kind: 'photograph', maturity: 'actual', vessel: 'Fictional N1', missions: ['passenger', 'service'], geography: ['fictional bay'], roles: ['hero', 'buyer gallery'], sourceIds: ['fictional-source'], visibility: 'public', clearedFor: ['public'], rightsNote: 'Original synthetic fixture; rights cleared.', caption: 'Fictional fixture image.', ...assetOverrides }],
  };
}

async function fixture(name: string, data: Record<string, unknown>, bytes = image): Promise<string> {
  const root = await mkdtemp(join(tmpdir(), `registry-${name}-`));
  await mkdir(join(root, 'assets'));
  await writeFile(join(root, 'assets', 'boat.svg'), bytes);
  const path = join(root, 'project.json');
  await writeFile(path, JSON.stringify(data));
  return path;
}

describe('cross-project asset registry', () => {
  test('preserves project bindings, detects id reuse, and never upgrades duplicate rights', async () => {
    const first = await fixture('first', project('fictional-a', { attachedMarks: [], clearedFor: ['public'] }));
    const second = await fixture('second', project('fictional-b', { rightsNote: 'Internal workflow use only; no external clearance.', visibility: 'internal', clearedFor: ['internal'] }));
    const registry = await buildRegistry([second, first]);
    expect(registry.assets).toHaveLength(2);
    expect(new Set(registry.assets.map(asset => asset.logicalId))).toEqual(new Set(['shared_asset']));
    expect(registry.assets[0].recordId).not.toBe(registry.assets[1].recordId);
    expect(registry.collisions).toHaveLength(1);
    expect(registry.collisions[0].reason).toBe('logical-id-reused');
    expect(registry.assets.find(asset => asset.project.projectId === 'fictional-a')?.attachments).toMatchObject({ status: 'known', attachedMarkAssetIds: [] });
    expect(registry.assets.find(asset => asset.project.projectId === 'fictional-b')?.attachments).toMatchObject({ status: 'unknown', attachedMarkAssetIds: null, hullLogoAssetIds: null });
    const reuse = reuseReport(registry);
    expect(reuse.reusableVersionCount).toBe(1);
    expect(reuse.groups[0].rightsStatus).toBe('held');
    expect(reuse.groups[0].effectiveClearedFor).toEqual([]);
  });

  test('uses observed bytes for exact versions and exposes stale declarations', async () => {
    const stale = await fixture('stale', project('fictional-stale', { sha256: 'f'.repeat(64) }));
    const registry = await buildRegistry([stale]);
    expect(registry.assets[0].observedSha256).toBe(hash(image));
    expect(registry.assets[0].exactVersionHash).toBe(hash(image));
    expect(registry.assets[0].hashStatus).toBe('mismatch');
  });

  test('filters by mission, vessel, geography, role, maturity, clearance and rights', async () => {
    const path = await fixture('search', project('fictional-search', { rightsStatus: 'held', maturity: 'concept', visibility: 'restricted', clearedFor: ['partner'], missions: ['cargo'], roles: ['cover'] }));
    const registry = await buildRegistry([path]);
    const result = searchRegistry(registry, { mission: 'cargo', vessel: 'N1', geography: 'bay', role: 'cover', maturity: 'concept', clearance: 'partner', rights: 'held' });
    expect(result.count).toBe(1);
    expect(searchRegistry(registry, { mission: 'passenger' }).count).toBe(0);
  });

  test('is deterministic and produces local-only contact sheets', async () => {
    const path = await fixture('deterministic', project('fictional-deterministic'));
    const one = await buildRegistry([path]);
    const two = await buildRegistry([path]);
    expect(JSON.stringify(one)).toBe(JSON.stringify(two));
    const out = join(path, '..', 'sheet.html');
    const html = registryHtml(one, one.assets, out);
    const markdown = registryMarkdown(one, one.assets, out.replace('.html', '.md'));
    expect(html).toContain('boat.svg');
    expect(html).not.toContain('http://');
    expect(html).not.toContain('https://');
    expect(markdown).toContain('boat.svg');
    expect(markdown).not.toContain('https://');
  });
});
