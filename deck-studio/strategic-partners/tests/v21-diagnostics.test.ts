import { describe, expect, test } from 'bun:test';
import type { CompiledDeck, DeckSnapshot, Project } from '../src/types';
import { densityLedger, geometryDiagnostics, normalizeNumericDisplay, numeralDiagnostics, pdfTextCoverage, pdfWordsForSlide, snapshotDensity } from '../src/diagnostics';

const emu = (magnitude: number) => ({ magnitude: magnitude * 12700, unit: 'EMU' });
const transform = (x = 0, y = 0) => ({ scaleX: 1, scaleY: 1, shearX: 0, shearY: 0, translateX: x * 12700, translateY: y * 12700, unit: 'EMU' });
const textNative = (objectId: string, x: number, y: number, w: number, h: number, content: string, size = 12): any => ({ objectId, size: { width: emu(w), height: emu(h) }, transform: transform(x, y), shape: { shapeType: 'TEXT_BOX', text: { textElements: [{ textRun: { content, style: { fontSize: { magnitude: size, unit: 'PT' } } } }] } } });
const compiled = (key: string, boxes: any[], visibleText = boxes.map(box => box.text || '')): any => ({ key, objectId: `${key}_page`, layout: 'cover', requests: [], elements: boxes.filter(box => box.role === 'text').map(box => ({ objectId: box.objectId, slideKey: key, role: 'text', kind: 'text' })), boxes, visibleText, notes: 'Fictional notes' });
const deck = (slides: any[]): CompiledDeck => ({ schemaVersion: '1.0.0', projectId: 'fictional_diagnostics', revision: 'r1', inputHash: '0'.repeat(64), pageSize: { width: 720, height: 405 }, slides, requests: [], assetUses: [], warnings: [] });
const native = (...slides: any[]): DeckSnapshot => ({ presentationId: 'fictional', slides: slides.map((pageElements, index) => ({ objectId: `s${index}`, index, pageElements })) } as any);
const word = (text: string, x: number, y: number, page = 1, lineId?: string): any => ({ text, x, y, width: Math.max(4, text.length * 4), height: 8, page, lineId });
const project = (slides: any[], claims: any[] = []): Project => ({ schemaVersion: '1.0.0', meta: { projectId: 'fictional_diagnostics', revision: 'r1', title: 'Fictional diagnostics', company: 'Fictional Company', partner: 'Fictional Partner', legalEntity: 'Fictional Company Ltd', audience: 'internal', archetype: 'industrial', objective: 'Test evidence', meetingAudience: 'Fictional reviewers', date: '2026-09-20', classification: 'internal', fictional: true, footer: 'Fictional fixture' }, sources: [], claims, assets: [], opportunities: [], slides, policy: { forbiddenTerms: [], forbiddenPartnerNames: [], requiredPhrases: [], allowMissingLogosForInternalReview: true } });
const claim = (id: string, value: number, context: any = {}, statistic = 'typical', unit = 'MW', subject = 'Fictional vessel') => ({ id, statement: 'Fictional result', evidenceClass: 'measured', sourceIds: [], basis: 'Fictional test', clearedFor: ['internal'], topic: 'performance', provenance: { subject, reportedBy: 'Fictional Lab', owner: 'fictional' }, context: { geography: 'Fictional Bay', mission: 'commute', configuration: 'alpha', asOf: '2026-01-01', conditions: [], ...context }, quantities: [{ id: 'q', metric: 'range', value, unit, statistic }], dependsOn: [] });
const use = (claimId: string, display: string) => ({ claimId, quantityId: 'q', display });

describe('V2.1 evidence diagnostics', () => {
  test('normalizes numeric aliases without silently treating units as multipliers', () => {
    expect(normalizeNumericDisplay('55k')).toEqual([55000]);
    expect(normalizeNumericDisplay('55,000')).toEqual([55000]);
    expect(normalizeNumericDisplay('1.8 GW')).toEqual([1.8]);
    expect(normalizeNumericDisplay('1.2M')).toEqual([1200000]);
  });

  test('reports same-context conflicts but preserves distinct evidence contexts', () => {
    const slides: any[] = [{ key: 'a', quantityUses: [use('c1', '1.8 MW')] }, { key: 'b', quantityUses: [use('c2', '1.9 MW')] }, { key: 'c', quantityUses: [use('c3', '1.9 MW')] }];
    const p = project(slides, [claim('c1', 1.8), claim('c2', 1.9), claim('c3', 1.9, { geography: 'Fictional Harbor' })]);
    const diagnostics = numeralDiagnostics(p, deck(slides.map((slide, index) => compiled(slide.key, [{ objectId: `t${index}`, role: 'text', text: slide.quantityUses[0].display }]))));
    expect(diagnostics.filter(d => d.code === 'NUMERAL_CONFLICT')).toHaveLength(1);
  });

  test('uses unambiguous one-based PDF page assignment, never the adjacent page', () => {
    const words = [word('first', 10, 10, 1), word('second', 10, 10, 2)];
    expect(pdfWordsForSlide(words, 0, 'one', 2).map(item => item.text)).toEqual(['first']);
    expect(pdfWordsForSlide(words, 1, 'two', 2).map(item => item.text)).toEqual(['second']);
  });

  test('marks padded native-box overlap as potential, not a rendered collision', () => {
    const slide = compiled('padded', [{ objectId: 'a', role: 'text', text: 'Alpha' }, { objectId: 'b', role: 'text', text: 'Beta' }]);
    const result = geometryDiagnostics(deck([slide]), native([textNative('a', 10, 10, 100, 40, 'Alpha'), textNative('b', 80, 10, 100, 40, 'Beta')]), [word('Alpha', 15, 15), word('Beta', 150, 15)]);
    expect(result.collisions.some(item => item.code === 'NATIVE_TEXT_BOX_OVERLAP' && item.severity === 'warning')).toBe(true);
    expect(result.collisions.some(item => item.code === 'RENDERED_TEXT_OVERLAP')).toBe(false);
  });

  test('marks corroborated rendered word-bound overlap as a potential glyph collision', () => {
    const slide = compiled('collision', [{ objectId: 'a', role: 'text', text: 'Alpha' }, { objectId: 'b', role: 'text', text: 'Beta' }]);
    const result = geometryDiagnostics(deck([slide]), native([textNative('a', 10, 10, 100, 40, 'Alpha'), textNative('b', 10, 10, 100, 40, 'Beta')]), [word('Alpha', 15, 15), word('Beta', 16, 15)]);
    expect(result.collisions.some(item => item.code === 'RENDERED_TEXT_OVERLAP' && item.severity === 'warning')).toBe(true);
  });

  test('finds an actual prose orphan but ignores small captions and a single-line page number', () => {
    const slide = compiled('wrap', [
      { objectId: 'body', role: 'text', text: 'This sentence has an orphan' },
      { objectId: 'caption', role: 'text', text: 'Source Fictional' },
      { objectId: 'page', role: 'text', text: '9' },
    ]);
    const words = [word('This', 12, 12, 1, 'body-1'), word('sentence', 35, 12, 1, 'body-1'), word('has', 70, 12, 1, 'body-1'), word('an', 92, 12, 1, 'body-1'), word('orphan', 12, 28, 1, 'body-2'), word('Source', 12, 60, 1, 'caption-1'), word('Fictional', 12, 75, 1, 'caption-2'), word('9', 160, 160, 1, 'page-1')];
    const result = geometryDiagnostics(deck([slide]), native([textNative('body', 10, 10, 150, 30, 'This sentence has an orphan'), textNative('caption', 10, 58, 100, 25, 'Source Fictional', 6), textNative('page', 150, 150, 20, 20, '9')]), words);
    expect(result.orphanLines.map(item => item.objectIds?.[0])).toEqual(['body']);
  });

  test('checks multi-column coverage by native region and fails closed on a genuinely missing word', () => {
    const slide = compiled('columns', [{ objectId: 'left', role: 'text', text: 'North column words' }, { objectId: 'right', role: 'text', text: 'South column words' }]);
    const d = deck([slide]), n = native([textNative('left', 10, 10, 150, 30, 'North column words'), textNative('right', 400, 10, 150, 30, 'South column words')]);
    const full = [word('North', 12, 12), word('South', 402, 12), word('column', 38, 12), word('column', 428, 12), word('words', 80, 12), word('words', 470, 12)];
    expect(pdfTextCoverage(d, n, full).get('columns')).toMatchObject({ coverage: 1, missingText: [] });
    const missing = full.filter(item => !(item.text === 'words' && item.x === 470));
    expect(pdfTextCoverage(d, n, missing).get('columns')).toMatchObject({ coverage: .5, missingText: ['South column words'] });
  });

  test('hyphenated PDF words and repeated short labels keep their exact native bindings', () => {
    const slide=compiled('bound',[{objectId:'label',role:'text',text:'Fictional concept'},{objectId:'detail',role:'text',text:'Fictional concept uses claim-linked evidence.'}]);
    const d=deck([slide]),n=native([textNative('label',10,10,140,25,'Fictional concept'),textNative('detail',10,60,400,25,'Fictional concept uses claim-linked evidence.')]);
    const ws=[word('Fictional',12,12),word('concept',50,12),word('Fictional',12,62),word('concept',50,62),word('uses',84,62),word('claim-linked',106,62),word('evidence.',160,62)];
    expect(pdfTextCoverage(d,n,ws).get('bound')).toMatchObject({coverage:1,missingText:[],limitations:[]});
    expect(pdfTextCoverage(d,n,ws.filter(w=>w.text!=='claim-linked')).get('bound')?.missingText).toEqual(['Fictional concept uses claim-linked evidence.']);
  });

  test('density and snapshot ledgers keep quantity bindings distinct from native facts', () => {
    const slide: any = { key: 'density', quantityUses: [use('c', '55,000 seats')] };
    const p = project([slide], [claim('c', 55000, {}, 'typical', 'seats')]);
    expect(densityLedger(p, deck([compiled('density', [{ objectId: 'body', role: 'text', text: 'A proposed result' }, { objectId: 'fine', role: 'text', text: '55,000 seats', fontSize: 6 }])]))[0]).toMatchObject({ quantityUses: 1, finePrintWords: 2 });
    expect(snapshotDensity(native([textNative('t', 0, 0, 100, 20, 'Native fact')]))[0].quantityUses).toBe(0);
  });
});
