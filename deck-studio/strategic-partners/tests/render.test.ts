import { describe, expect, test } from 'bun:test';
import { compileProject, RenderSafetyError } from '../src/render';
import { imagePlacement } from '../src/primitives';
import type { Project } from '../src/types';

const tx = { actors: ['Buyer', 'Supplier'], labels: ['price'], kind: 'payment' as const };
const asset = (id: string) => ({ id, path: `assets/${id}.png`, sha256: '0'.repeat(64), width: 1600, height: 900, mimeType: 'image/png', kind: 'photograph' as const, maturity: 'actual' as const, missions: ['evaluation'], geography: [], roles: ['hero', 'mission', 'visual'], sourceIds: [], visibility: 'public' as const, clearedFor: ['internal', 'partner', 'public'] as const, rightsNote: 'Fixture', caption: 'Fixture photograph.' });
const base = (key: string, layout: any, extra: any = {}) => ({ key, layout, kicker: 'WORKING HYPOTHESIS', title: `${layout} title`, claimIds: [], sourceIds: [], opportunityIds: [], notes: 'Notes', ...extra });
function project(slides: any[]): Project { return { schemaVersion: '1.0.0', meta: { projectId: 'neutral_project', revision: 'r1', title: 'Neutral brief', company: 'Company', partner: 'Partner', legalEntity: 'Company Ltd', audience: 'internal', archetype: 'industrial', objective: 'Explore', meetingAudience: 'Team', date: '2026-09-18', classification: 'internal', fictional: true, footer: 'Internal working draft' }, sources: [], claims: [], assets: [asset('a'), asset('b'), asset('c'), asset('d')], opportunities: [], slides, policy: { forbiddenTerms: [], forbiddenPartnerNames: [], requiredPhrases: [], allowMissingLogosForInternalReview: true } }; }
const visual = (assetId = 'a') => ({ assetId, caption: 'Fixture' });

describe('native strategic partner rendering', () => {
  test('compiles every layout with native requests and editable text', () => {
    const slides = [
      base('cover', 'cover', { visual: visual(), subtitle: 'Subtitle', body: 'Body', pillars: ['One', 'Two', 'Three'] }),
      base('fit', 'fit', { visual: visual('b'), companyHeadline: 'Contribution', companyBody: 'Body', partnerBody: 'Partner value', benefits: [{ title: 'Benefit', body: 'Body' }, { title: 'Benefit two', body: 'Body' }], takeaway: 'Explore.' }),
      base('options', 'options', { options: [{ title: 'Build', body: 'Body', schematic: 'manufacture', revenue: 'Defined later' }, { title: 'Service', body: 'Body', schematic: 'service', revenue: 'Defined later' }], payment: tx, status: 'Proposed', explore: 'Choose.' }),
      base('models', 'models', { models: [{ label: 'A', title: 'Product', body: 'Body', payments: tx, benefit: 'Benefit' }, { label: 'B', title: 'License', body: 'Body', payments: tx, benefit: 'Benefit' }], explore: 'Compare.' }),
      base('channels', 'channels', { scope: 'Scope', selection: 'Selection', criteria: 'Criteria', models: [{ label: 'Direct', benefit: 'Benefit', payments: tx }], serviceLabel: 'Service', service: 'Defined later', explore: 'Test.' }),
      base('missions', 'missions', { intro: 'Intro', status: 'Proposed', cards: [{ label: 'A', title: 'Short', description: 'Body', visual: visual() }, { label: 'B', title: 'Short', description: 'Body', visual: visual('b') }], explore: 'Discuss.' }),
      base('close', 'close', { visual: visual('c'), intro: 'Intro', conversations: [{ title: 'Conversation', body: 'Body' }], ask: 'Ask', contact: 'team@example.invalid' }),
    ];
    const out = compileProject(project(slides), { allowUnresolvedAssets: true });
    expect(out.slides).toHaveLength(7); expect(out.requests.filter(r => r.createSlide)).toHaveLength(7); expect(out.slides.every(s => s.elements.some(e => e.kind === 'text'))).toBe(true);
    const ids = out.requests.flatMap(r => Object.entries(r as any).flatMap(([k, v]: [string, any]) => k.startsWith('create') && v?.objectId ? [v.objectId] : [])); expect(new Set(ids).size).toBe(ids.length); expect(ids.every(id => id.length <= 50)).toBe(true);
    expect(JSON.stringify(out)).not.toContain('raster'); expect(out.warnings.some(w => w.code === 'UNRESOLVED_ASSET')).toBe(true);
  });
  test('is deterministic and preserves payment order', () => {
    const s = base('m', 'models', { models: [{ label: 'First', title: 'One', body: 'Body', payments: tx, benefit: 'Benefit' }, { label: 'Second', title: 'Two', body: 'Body', payments: { actors: ['Supplier', 'Buyer'], labels: ['fee'], kind: 'payment' }, benefit: 'Benefit' }], explore: 'Ask' });
    const a = compileProject(project([s]), { allowUnresolvedAssets: true }), b = compileProject(project([s]), { allowUnresolvedAssets: true }); expect(a.inputHash).toBe(b.inputHash); expect(a.requests).toEqual(b.requests); const labels = a.slides[0].visibleText.filter(x => x === 'First' || x === 'Second'); expect(labels).toEqual(['First', 'Second']);
  });
  test('supports 2, 3 and 4 mission cards and long titles', () => {
    for (const n of [2, 3, 4]) { const cards = Array.from({ length: n }, (_, i) => ({ label: `Mission ${i}`, title: 'Passenger transport network connection', description: 'Body', visual: visual(['a', 'b', 'c', 'd'][i]) })); expect(compileProject(project([base(`m${n}`, 'missions', { intro: 'Intro', status: 'Status', cards, explore: 'Ask' })]), { allowUnresolvedAssets: true }).slides[0].boxes.length).toBeGreaterThan(0); }
  });
  test('uses aspect-preserving crop, native masks and rejects title overflow', () => {
    const p = imagePlacement({ width: 2000, height: 1000, focalPoint: { x: .8, y: .5 } }, { x: 10, y: 10, w: 100, h: 160 }); expect(p.w / p.h).toBeCloseTo(2); expect(p.crop.left).toBeGreaterThan(0); const tooLong = project([base('bad', 'cover', { title: 'x'.repeat(96), visual: visual(), subtitle: 'x', body: 'x', pillars: ['x'] })]); expect(() => compileProject(tooLong, { allowUnresolvedAssets: true })).toThrow(RenderSafetyError);
  });
});
