import { describe, expect, test } from 'bun:test';
import { createHash } from 'node:crypto';
import { mkdtemp, mkdir, symlink, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { findAssets, verifyAssetFiles } from '../src/assets';
import type { Project } from '../src/types';

// A valid 1x1 PNG keeps the test independent of parent fixtures or image packages.
const png = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=', 'base64');
const hash = (b: Uint8Array) => createHash('sha256').update(b).digest('hex');
function project(asset: any): Project { return { schemaVersion: '1.0.0', meta: { projectId: 'p', revision: 'r1', title: 't', company: 'c', partner: 'p', legalEntity: 'c', audience: 'internal', archetype: 'industrial', objective: 'o', meetingAudience: 'm', date: '2026-09-18', classification: 'internal', fictional: true, footer: 'f' }, sources: [], claims: [], assets: [asset], opportunities: [], slides: [], policy: { forbiddenTerms: [], forbiddenPartnerNames: [], requiredPhrases: [], allowMissingLogosForInternalReview: true } }; }
function asset(path: string, sha256 = hash(png)): any { return { id: 'a', path, sha256, width: 1, height: 1, mimeType: 'image/png', kind: 'logo', maturity: 'brand', missions: [], geography: [], roles: ['brand'], sourceIds: [], visibility: 'public', clearedFor: ['internal'], rightsNote: 'Fixture rights cleared.', caption: 'Fixture logo.' }; }

describe('asset utilities', () => {
  test('filters by all requested metadata dimensions', () => {
    const first = asset('a.png'); first.id = 'a1'; first.roles = ['hero']; first.missions = ['commute']; first.vessel = 'v1'; first.geography = ['bay']; first.clearedFor = ['partner'];
    const second = { ...first, id: 'a2', roles: ['logo'] };
    const found = findAssets(project(first), { roles: ['hero'], missions: ['commute'], vessel: 'v1', geography: ['bay'], audience: 'partner' });
    expect(found.map(x => x.id)).toEqual(['a1']);
    expect(findAssets(project(second), { roles: ['hero'] })).toHaveLength(0);
  });

  test('checks hash, dimensions, and binary MIME', async () => {
    const root = await mkdtemp(join(tmpdir(), 'strategic-assets-'));
    await writeFile(join(root, 'good.png'), png);
    const good = asset('good.png');
    const issues = await verifyAssetFiles(project(good), root);
    expect(issues).toHaveLength(0);
    const bad = asset('good.png', 'f'.repeat(64));
    const badIssues = await verifyAssetFiles(project(bad), root);
    expect(badIssues.some(i => i.code === 'ASSET_HASH_MISMATCH')).toBe(true);
  });

  test('rejects traversal and symlink escape', async () => {
    const root = await mkdtemp(join(tmpdir(), 'strategic-assets-'));
    const outside = await mkdtemp(join(tmpdir(), 'strategic-outside-'));
    await writeFile(join(outside, 'secret.png'), png);
    await mkdir(join(root, 'assets'));
    await symlink(join(outside, 'secret.png'), join(root, 'assets', 'link.png'));
    const traversal = await verifyAssetFiles(project(asset('../secret.png')), root);
    expect(traversal.some(i => i.code === 'ASSET_PATH_UNSAFE')).toBe(true);
    const escaped = await verifyAssetFiles(project(asset('assets/link.png')), root);
    expect(escaped.some(i => i.code === 'ASSET_SYMLINK_ESCAPE')).toBe(true);
  });
});
