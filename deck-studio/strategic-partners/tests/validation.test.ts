import { describe, expect, test } from 'bun:test';
import { validateProject, assertValidProject } from '../src/validate';
import type { Project } from '../src/types';

const hash = '0'.repeat(64);
const source = { id: 'src_demo', title: 'Public demonstration record', locator: 'https://example.invalid/source', asOf: '2026-09-18', visibility: 'public' as const };
const claim = { id: 'claim_demo', statement: 'The platform is demonstrated in evaluation work.', evidenceClass: 'demonstrated' as const, sourceIds: ['src_demo'], basis: 'Public demonstration record, subject to configuration and validation.', clearedFor: ['internal', 'partner', 'public'] };
const photo = (id: string) => ({ id, path: `assets/${id}.png`, sha256: hash, width: 1, height: 1, mimeType: 'image/png', kind: 'photograph' as const, maturity: 'actual' as const, missions: ['evaluation'], geography: [], roles: ['hero'], sourceIds: ['src_demo'], visibility: 'public' as const, clearedFor: ['internal', 'partner', 'public'], rightsNote: 'Synthetic fixture; rights cleared for tests.', caption: 'Demonstration photograph.' });
const visual = (assetId: string) => ({ assetId, caption: 'Demonstration photograph.' });
const base = (key: string, layout: string, extra: Record<string, unknown> = {}) => ({ key, layout, kicker: 'Evaluation', title: `${layout} title`, claimIds: ['claim_demo'], sourceIds: ['src_demo'], opportunityIds: [], notes: '', ...extra });

function fixture(): Project {
  return {
    schemaVersion: '1.0.0',
    meta: { projectId: 'project_demo', revision: 'r1', title: 'Neutral evaluation brief', company: 'Company Example', partner: 'Partner Example', legalEntity: 'Company Example Ltd', audience: 'internal', archetype: 'industrial', objective: 'Explore independent partnership hypotheses', meetingAudience: 'Working group', date: '2026-09-18', classification: 'internal', fictional: true, footer: 'Evaluation only' },
    sources: [source], claims: [claim], assets: [photo('photo_one'), photo('photo_two')], opportunities: [],
    slides: [base('cover_slide', 'cover', { visual: visual('photo_one'), subtitle: 'A hypothesis for discussion', body: 'No market selected; configuration and validation remain open.', pillars: ['Product fit'] }), base('close_slide', 'close', { visual: visual('photo_two'), intro: 'Choose one useful next step.', conversations: [{ title: 'Question', body: 'Which path merits a working session?' }], ask: 'Select a path to explore.', contact: 'Working group' })],
    policy: { forbiddenTerms: [], forbiddenPartnerNames: [], requiredPhrases: [], allowMissingLogosForInternalReview: true },
  };
}

describe('project validation', () => {
  test('accepts a bounded neutral internal hypothesis', async () => {
    const result = await validateProject(fixture());
    expect(result.ok).toBe(true);
    expect(result.releaseReady).toBe(false); // logo omission is an explicit internal-review hold
    expect(() => assertValidProject(fixture())).not.toThrow();
  });

  test('rejects missing claim and asset references', async () => {
    const project = fixture() as any;
    project.slides[0].claimIds = ['missing_claim'];
    project.slides[0].visual.assetId = 'missing_asset';
    const result = await validateProject(project);
    expect(result.issues.some(i => i.code === 'UNKNOWN_REFERENCE')).toBe(true);
  });

  test('rejects private material for public publication, including unused records', async () => {
    const project = fixture() as any;
    project.meta.audience = 'public'; project.meta.classification = 'public';
    project.sources[0].visibility = 'internal'; project.assets[0].visibility = 'internal';
    const result = await validateProject(project, { forPublication: true });
    expect(result.issues.some(i => i.code === 'PUBLIC_SOURCE_PRIVATE')).toBe(true);
    expect(result.issues.some(i => i.code === 'PUBLIC_ASSET_PRIVATE')).toBe(true);
  });

  test('enforces concept caption and normalized crop bounds', async () => {
    const project = fixture() as any;
    project.assets[0].maturity = 'concept'; project.assets[0].caption = 'Boat image'; project.assets[0].crop = { left: 0.8, top: 0, right: 0.2, bottom: 1.1 };
    const result = await validateProject(project);
    expect(result.issues.some(i => i.code === 'CONCEPT_CAPTION_MISSING')).toBe(true);
    expect(result.issues.some(i => i.code === 'CROP_OUT_OF_BOUNDS')).toBe(true);
    expect(result.issues.some(i => i.code === 'CROP_NOT_POSITIVE')).toBe(true);
  });

  test('checks count boundaries, long headlines, and false future readiness', async () => {
    const project = fixture() as any;
    project.slides[0].title = 'x'.repeat(96);
    project.slides[0].body = 'This is ready to launch now.';
    const options = base('options_slide', 'options', { options: [{ title: 'One', body: 'Explore.', revenue: 'Defined later.' }], status: 'Proposed', explore: 'Choose.' });
    project.slides.splice(1, 0, options);
    const result = await validateProject(project);
    expect(result.issues.some(i => i.code === 'TEXT_BUDGET')).toBe(true);
    expect(result.issues.some(i => i.code === 'COUNT_BOUNDARY')).toBe(true);
    expect(result.issues.some(i => i.code === 'FUTURE_READINESS_UNSUPPORTED')).toBe(true);
  });

  test('warns only when the same hero photograph repeats', async () => {
    const project = fixture() as any;
    project.slides[1].visual.assetId = 'photo_one';
    const result = await validateProject(project);
    expect(result.issues.some(i => i.code === 'REPEATED_HERO_PHOTO' && i.severity === 'warning')).toBe(true);
  });
});
