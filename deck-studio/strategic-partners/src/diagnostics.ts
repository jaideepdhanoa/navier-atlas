import type { CompiledDeck, CompiledSlide, DeckSnapshot, Project } from './types';
import type { DensityRow, DiagnosticChecks, EvidenceDiagnostic, QuantityUse } from './evidence-types';
import { PAGE } from './primitives';

/**
 * A word as returned by a PDF text extractor.  x/y/width/height are in PDF
 * page points (top-left origin).  x0/y0/x1/y1 is accepted as a convenient
 * pdf.js/pdfplumber-style alternative.  A page or slideKey is needed when a
 * document contains more than one slide.
 */
export interface PdfWord {
  text: string;
  x?: number; y?: number; width?: number; height?: number;
  x0?: number; y0?: number; x1?: number; y1?: number;
  page?: number; slideIndex?: number; slideKey?: string;
  lineIndex?: number | string; lineId?: string;
}
export type PdfWords = PdfWord[];

type AnyRecord = Record<string, any>;
type Bounds = { x: number; y: number; w: number; h: number };
type Matrix = { a: number; b: number; c: number; d: number; e: number; f: number };
type NativeLeaf = { objectId: string; element: AnyRecord; bounds: Bounds; text: boolean; slideIndex: number };
const EMU = 12700;
const EPS = 0.25;

function record(value: unknown): value is AnyRecord { return !!value && typeof value === 'object' && !Array.isArray(value); }
function finite(value: unknown): value is number { return typeof value === 'number' && Number.isFinite(value); }
function unitFactor(unit: unknown): number | undefined {
  if (unit === 'EMU') return 1 / EMU;
  if (unit === 'PT' || unit === 'POINT' || unit === 'points' || unit === undefined) return 1;
  return undefined;
}
function words(text: string): number {
  // Thousands commas are presentation punctuation, not word boundaries.
  const normalized = text.replace(/(?<=\d),(?=\d)/g, '');
  return (normalized.match(/[\p{L}\p{N}][\p{L}\p{N}'’/_-]*/gu) || []).length;
}
function normalizeWhitespace(text: string): string { return text.replace(/\s+/g, ' ').trim(); }
function close(a: number, b: number): boolean { return Math.abs(a - b) <= 1e-6 * Math.max(1, Math.abs(a), Math.abs(b)); }
function matrixMultiply(a: Matrix, b: Matrix): Matrix {
  return { a: a.a * b.a + a.c * b.b, b: a.b * b.a + a.d * b.b, c: a.a * b.c + a.c * b.d, d: a.b * b.c + a.d * b.d, e: a.a * b.e + a.c * b.f + a.e, f: a.b * b.e + a.d * b.f + a.f };
}
function apply(m: Matrix, x: number, y: number): [number, number] { return [m.a * x + m.c * y + m.e, m.b * x + m.d * y + m.f]; }
const IDENTITY: Matrix = { a: 1, b: 0, c: 0, d: 1, e: 0, f: 0 };

function transformOf(value: unknown, limitations: string[], id: string): Matrix | undefined {
  if (!record(value)) return IDENTITY;
  const factor = unitFactor(value.unit);
  if (factor === undefined) { limitations.push(`Unsupported native transform unit on ${id}; its geometry was not checked.`); return undefined; }
  const n = (key: string, fallback: number) => value[key] === undefined ? fallback : value[key];
  const vals = ['scaleX', 'scaleY', 'shearX', 'shearY', 'translateX', 'translateY'].map(k => n(k, k.startsWith('scale') ? 1 : 0));
  if (!vals.every(finite)) { limitations.push(`Malformed native transform on ${id}; its geometry was not checked.`); return undefined; }
  return { a: vals[0], b: vals[3], c: vals[2], d: vals[1], e: vals[4] * factor, f: vals[5] * factor };
}
function dimension(value: unknown, limitations: string[], id: string): number | undefined {
  if (!record(value) || !finite(value.magnitude)) { limitations.push(`Missing native size on ${id}; its geometry was not checked.`); return undefined; }
  const factor = unitFactor(value.unit);
  if (factor === undefined) { limitations.push(`Unsupported native size unit on ${id}; its geometry was not checked.`); return undefined; }
  return value.magnitude * factor;
}
function nativeText(element: AnyRecord): string | undefined {
  const shape = element.shape;
  if (!record(shape) || shape.shapeType !== 'TEXT_BOX') return undefined;
  if (typeof shape.text === 'string') return shape.text;
  if (record(shape.text) && Array.isArray(shape.text.textElements)) return shape.text.textElements.map((part: any) => part?.textRun?.content || '').join('');
  return '';
}
function nativeFontSize(element: AnyRecord): number | undefined {
  const shape = element.shape;
  if (!record(shape) || shape.shapeType !== 'TEXT_BOX') return undefined;
  const runs = record(shape.text) && Array.isArray(shape.text.textElements) ? shape.text.textElements : [];
  const values = runs.flatMap((part: any) => finite(part?.textRun?.style?.fontSize?.magnitude) ? [part.textRun.style.fontSize.magnitude] : []);
  return values.length ? values.reduce((a: number, b: number) => a + b, 0) / values.length : undefined;
}
function nativePageSize(native: any): { width: number; height: number } {
  const p = native?.pageSize;
  const w = dimension(p?.width, [], 'page'), h = dimension(p?.height, [], 'page');
  return { width: w && w > 0 ? w : PAGE.width, height: h && h > 0 ? h : PAGE.height };
}
function collectLeaves(slide: any, slideIndex: number, limitations: string[]): NativeLeaf[] {
  const out: NativeLeaf[] = [];
  const visit = (element: any, parent: Matrix) => {
    if (!record(element) || typeof element.objectId !== 'string') return;
    const ownTransform = transformOf(element.transform, limitations, element.objectId);
    if (!ownTransform) return;
    const composed = matrixMultiply(parent, ownTransform);
    const group = record(element.elementGroup) && Array.isArray(element.elementGroup.children);
    if (group) {
      for (const child of element.elementGroup.children) visit(child, composed);
      return;
    }
    const w = dimension(element.size?.width, limitations, element.objectId), h = dimension(element.size?.height, limitations, element.objectId);
    if (w === undefined || h === undefined || w <= 0 || h <= 0) return;
    const corners = [[0, 0], [w, 0], [0, h], [w, h]].map(([x, y]) => apply(composed, x, y));
    const xs = corners.map(c => c[0]), ys = corners.map(c => c[1]);
    out.push({ objectId: element.objectId, element, bounds: { x: Math.min(...xs), y: Math.min(...ys), w: Math.max(...xs) - Math.min(...xs), h: Math.max(...ys) - Math.min(...ys) }, text: nativeText(element) !== undefined, slideIndex });
  };
  for (const element of Array.isArray(slide?.pageElements) ? slide.pageElements : []) visit(element, IDENTITY);
  return out;
}
function allNativeLeaves(native: any, limitations: string[]): NativeLeaf[] {
  if (!record(native) || !Array.isArray(native.slides)) { limitations.push('Native snapshot was not supplied in a supported DeckSnapshot shape; geometry was not checked.'); return []; }
  return native.slides.flatMap((slide: any, i: number) => collectLeaves(slide, i, limitations));
}

/**
 * Parse visible quantity representations. Commas are thousands separators;
 * k/K multiplies by 1,000 and an uppercase M by 1,000,000. Lowercase m
 * remains metres unless attached to a currency-prefixed number. GW (and
 * kW/MW) stays a unit suffix; unit consistency is checked separately.
 */
export function normalizeNumericDisplay(text: string): number[] {
  if (typeof text !== 'string') return [];
  const result: number[] = [];
  const numberPattern = /(?<![\p{L}\p{N}_.])(?:[$€£]\s*)?([-+]?((?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?|\.\d+))/gu;
  let match: RegExpExecArray | null;
  while ((match = numberPattern.exec(text))) {
    const raw = match[1].replace(/,/g, '');
    const value = Number(raw);
    if (!Number.isFinite(value)) continue;
    const after = text.slice(numberPattern.lastIndex).match(/^\s*([A-Za-zµ%]+)/)?.[1] || '';
    let multiplier = 1;
    if (/^[kK]$/.test(after)) multiplier = 1e3;
    else if (after === 'M' || (after === 'm' && /[$€£]/.test(match[0]))) multiplier = 1e6;
    result.push(value * multiplier);
  }
  return result;
}
function displayUnit(text: string): string | undefined {
  const match = text.match(/(?:^|[^\p{L}\p{N}_])(?:[$€£]\s*)?[-+]?(?:\d{1,3}(?:,\d{3})+|\d+|\.\d+)(?:\.\d+)?\s*([A-Za-zµ%][A-Za-zµ%0-9/²³-]*)/u);
  return match?.[1];
}
function unitKey(unit: string): string { return unit.replace(/[\s_]/g, '').toLowerCase(); }
function contextKey(claim: any, quantity: any): string {
  const c = claim?.context || {};
  const p = claim?.provenance || {};
  // statistic is deliberate: a record and a typical value may coexist.
  return JSON.stringify({ subject: p.subject || '', metric: quantity.metric || '', unit: unitKey(quantity.unit || ''), statistic: quantity.statistic || '', geography: c.geography || '', mission: c.mission || '', configuration: c.configuration || '', asOf: c.asOf || '', conditions: Array.isArray(c.conditions) ? c.conditions.map((x: any) => ({ key: x.key, value: x.value, unit: x.unit })).sort((a: any, b: any) => JSON.stringify(a).localeCompare(JSON.stringify(b))) : [] });
}
function quantityValue(quantity: any): number[] { return typeof quantity?.value === 'number' ? [quantity.value] : [quantity?.value?.min, quantity?.value?.max].filter(finite); }
function numbersFit(numbers: number[], quantity: any): boolean {
  if (!numbers.length) return false;
  const value = quantity?.value;
  if (typeof value === 'number') return numbers.length === 1 && close(numbers[0], value);
  if (record(value) && finite(value.min) && finite(value.max)) return numbers.every(n => n >= value.min - 1e-6 && n <= value.max + 1e-6);
  return false;
}
function visibleTextFor(compiled: CompiledSlide): string[] { return Array.isArray(compiled.visibleText) ? compiled.visibleText.filter((x): x is string => typeof x === 'string') : []; }
function visibleQuantityUses(project: any, compiled: CompiledDeck): { slide: CompiledSlide; use: QuantityUse; text: string }[] {
  const out: { slide: CompiledSlide; use: QuantityUse; text: string }[] = [];
  const slides = Array.isArray(project?.slides) ? project.slides : [];
  for (const compiledSlide of compiled?.slides || []) {
    const authored = slides.find((s: any) => s?.key === compiledSlide.key);
    const uses: any[] = [];
    if (Array.isArray(authored?.quantityUses)) uses.push(...authored.quantityUses);
    const blockIds = new Set((compiledSlide.copyBindings || []).map((b: any) => b.blockId));
    for (const block of project?.sales?.blocks || []) if (blockIds.has(block.id) && Array.isArray(block.quantityUses)) uses.push(...block.quantityUses);
    const seen = new Set<string>();
    for (const use of uses) {
      if (!use || typeof use.claimId !== 'string' || typeof use.quantityId !== 'string' || typeof use.display !== 'string') continue;
      const key = `${use.claimId}\u0000${use.quantityId}\u0000${use.display}`;
      if (seen.has(key)) continue;
      const text = visibleTextFor(compiledSlide).find(t => normalizeWhitespace(t).includes(normalizeWhitespace(use.display)));
      if (text !== undefined) { seen.add(key); out.push({ slide: compiledSlide, use, text }); }
    }
  }
  return out;
}
function claimQuantity(project: any, claimId: string, quantityId: string): { claim: any; quantity: any } | undefined {
  const claim = (project?.claims || []).find((c: any) => c?.id === claimId);
  const quantity = claim?.quantities?.find((q: any) => q?.id === quantityId);
  return claim && quantity ? { claim, quantity } : undefined;
}

/** A per-slide ledger based on emitted text and source-bound quantity uses. */
export function densityLedger(project: Project, compiled: CompiledDeck): DensityRow[] {
  const quantityBySlide = new Map<string, number>();
  for (const item of visibleQuantityUses(project as any, compiled)) quantityBySlide.set(item.slide.key, (quantityBySlide.get(item.slide.key) || 0) + 1);
  return (compiled?.slides || []).map((slide: any) => {
    const boxes = Array.isArray(slide.boxes) ? slide.boxes.filter((b: any) => b?.role === 'text' && typeof b.text === 'string') : [];
    let bodyWords = 0, finePrintWords = 0, hedgeTokens = 0;
    for (const box of boxes) {
      const n = words(box.text);
      const fine = finite(box.fontSize) && box.fontSize <= 8 || /footer|caption|fine|footnote/i.test(String(box.role || ''));
      if (fine) finePrintWords += n; else bodyWords += n;
      hedgeTokens += (box.text.match(/\b(?:may|might|could|potential(?:ly)?|proposed|target(?:ed)?|illustrative|indicative|approx(?:imately)?|expected|exploratory|unresolved|subject to|to be defined|up to)\b/gi) || []).length;
    }
    return { slideKey: slide.key, bodyWords, finePrintWords, quantityUses: quantityBySlide.get(slide.key) || 0, hedgeTokens, notesWords: words(typeof slide.notes === 'string' ? slide.notes : '') };
  });
}

/** Revision density deliberately has no claim ledger: native snapshots cannot know authored bindings. */
export function snapshotDensity(snapshot: DeckSnapshot): DensityRow[] {
  const limitations: string[] = [];
  return (snapshot?.slides || []).map((slide: any, i: number) => {
    const leaves = collectLeaves(slide, i, limitations).filter(x => x.text);
    let bodyWords = 0, finePrintWords = 0;
    for (const leaf of leaves) {
      const text = nativeText(leaf.element) || '', n = words(text), size = nativeFontSize(leaf.element);
      if ((finite(size) && size <= 8) || /footer|caption|footnote/i.test(String(leaf.element.objectId))) finePrintWords += n; else bodyWords += n;
    }
    return { slideKey: String(slide.slideKey || slide.objectId || i), bodyWords, finePrintWords, quantityUses: 0, hedgeTokens: 0, notesWords: 0 };
  });
}

/** Check only bound, visibly emitted quantities; unbound prose is not treated as evidence. */
export function numeralDiagnostics(project: Project, compiled: CompiledDeck): EvidenceDiagnostic[] {
  const diagnostics: EvidenceDiagnostic[] = [];
  const grouped = new Map<string, { item: ReturnType<typeof visibleQuantityUses>[number]; quantity: any }[]>();
  for (const item of visibleQuantityUses(project as any, compiled)) {
    const found = claimQuantity(project as any, item.use.claimId, item.use.quantityId);
    if (!found) continue; // malformed bindings belong to the parent evidence validator.
    const numbers = normalizeNumericDisplay(item.use.display);
    if (!numbers.length) continue;
    const expected = quantityValue(found.quantity);
    const expectedUnit = unitKey(String(found.quantity.unit || ''));
    const shownUnit = displayUnit(item.use.display);
    if (shownUnit && expectedUnit && unitKey(shownUnit) !== expectedUnit && !/^[kKmM]$/.test(shownUnit)) {
      diagnostics.push({ code: 'NUMERAL_UNIT_MISMATCH', severity: 'error', slideKeys: [item.slide.key], detail: `${item.use.display} uses unit ${shownUnit}, but ${item.use.quantityId} is authored in ${found.quantity.unit}.`, objectIds: [] });
    }
    if (!numbersFit(numbers, found.quantity)) {
      diagnostics.push({ code: 'NUMERAL_CONFLICT', severity: 'error', slideKeys: [item.slide.key], detail: `${item.use.display} does not match the bound quantity ${expected.join('–')} ${found.quantity.unit}.`, objectIds: [] });
    }
    const key = contextKey(found.claim, found.quantity);
    const bucket = grouped.get(key) || [];
    bucket.push({ item, quantity: found.quantity }); grouped.set(key, bucket);
  }
  for (const bucket of grouped.values()) {
    for (let i = 0; i < bucket.length; i++) for (let j = i + 1; j < bucket.length; j++) {
      const a = normalizeNumericDisplay(bucket[i].item.use.display), b = normalizeNumericDisplay(bucket[j].item.use.display);
      if (a.length === 1 && b.length === 1 && close(a[0], b[0]) && bucket[i].item.use.display !== bucket[j].item.use.display) {
        diagnostics.push({ code: 'NUMERAL_FORMAT', severity: 'warning', slideKeys: [...new Set([bucket[i].item.slide.key, bucket[j].item.slide.key])], detail: `Equivalent bound value is displayed as both “${bucket[i].item.use.display}” and “${bucket[j].item.use.display}”.` });
      } else if (a.length === 1 && b.length === 1 && !close(a[0], b[0])) {
        diagnostics.push({ code: 'NUMERAL_CONFLICT', severity: 'error', slideKeys: [...new Set([bucket[i].item.slide.key, bucket[j].item.slide.key])], detail: `Bound quantities with the same subject, metric, unit, statistic and context display ${a[0]} and ${b[0]}.` });
      }
    }
  }
  return diagnostics;
}

function compiledTextEntries(compiledSlide: any): { box: any; role: string }[] {
  const roles = new Map((compiledSlide.elements || []).map((e: any) => [e.objectId, String(e.role || '')]));
  return (compiledSlide.boxes || []).filter((b: any) => b?.role === 'text' && typeof b.objectId === 'string').map((box: any) => ({ box, role: roles.get(box.objectId) || '' }));
}
function intersects(a: Bounds, b: Bounds): boolean { return Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x) > EPS && Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y) > EPS; }
function intentional(role: string, box: any): boolean { return !!box?.intentionalClip || /background|attachment|attached|mask|intentional/i.test(role); }
function pdfBounds(word: PdfWord): Bounds | undefined {
  const x = finite(word.x) ? word.x : word.x0, y = finite(word.y) ? word.y : word.y0;
  const w = finite(word.width) ? word.width : finite(word.x1) && finite(x) ? word.x1 - x : undefined;
  const h = finite(word.height) ? word.height : finite(word.y1) && finite(y) ? word.y1 - y : undefined;
  return finite(x) && finite(y) && finite(w) && finite(h) && w >= 0 && h >= 0 ? { x, y, w, h } : undefined;
}
/** PDF pages are one-based, per Poppler. slideIndex is deliberately zero-based. */
export function pdfWordsForSlide(pdfWords: PdfWords, index: number, key: string, count: number): PdfWord[] {
  return pdfWords.filter(word => (word.slideKey !== undefined ? word.slideKey === key : word.slideIndex !== undefined ? word.slideIndex === index : word.page !== undefined ? word.page === index + 1 : count === 1));
}
function wordToken(text: string): string { return normalizeWhitespace(text).normalize('NFKC').toLocaleLowerCase().replace(/[^\p{L}\p{N}]+/gu, ''); }
function textTokens(text: string): string[] { return (text.normalize('NFKC').match(/[\p{L}\p{N}]+/gu) || []).map(x => x.toLocaleLowerCase()); }
function tokenCounts(tokens: string[]): Map<string, number> { const counts = new Map<string, number>(); for (const token of tokens) counts.set(token, (counts.get(token) || 0) + 1); return counts; }
function containsTokens(haystack: string, needles: string[]): boolean { const available = tokenCounts(textTokens(haystack)); for (const token of needles) { const n = available.get(token) || 0; if (!n) return false; available.set(token, n - 1); } return true; }
function containsPoint(bounds: Bounds, word: Bounds, padding = 2): boolean { const x = word.x + word.w / 2, y = word.y + word.h / 2; return x >= bounds.x - padding && x <= bounds.x + bounds.w + padding && y >= bounds.y - padding && y <= bounds.y + bounds.h + padding; }
type AttributedWord = { word: PdfWord; bounds: Bounds };
type NativeText = { objectId: string; bounds: Bounds; text: string; role: string; box: any };
function nativeTextEntries(compiledSlide: any, nativeById: Map<string, NativeLeaf>, limitations: string[]): NativeText[] {
  const out: NativeText[] = [];
  for (const { box, role } of compiledTextEntries(compiledSlide)) {
    if (intentional(role, box)) continue;
    const leaf = nativeById.get(box.objectId);
    if (!leaf) { limitations.push(`Native geometry for text object ${box.objectId} on ${compiledSlide.key} was unavailable; it was not inspected.`); continue; }
    const text = nativeText(leaf.element);
    if (text === undefined) { limitations.push(`Native text for ${box.objectId} on ${compiledSlide.key} was unavailable; PDF words cannot be attributed to it.`); continue; }
    out.push({ objectId: box.objectId, bounds: leaf.bounds, text, role, box });
  }
  return out;
}
/** Attribute words by both content and native geometry; box intersection alone is never glyph proof. */
function attributeWords(pdfWords: PdfWord[], nativeTexts: NativeText[], limitations: string[], slideKey: string): Map<string, AttributedWord[]> {
  const attributed = new Map(nativeTexts.map(entry => [entry.objectId, [] as AttributedWord[]]));
  const ambiguous = new Set<string>();
  for (const word of pdfWords) {
    const bounds = pdfBounds(word), token = wordToken(word.text);
    if (!bounds || !token) continue;
    const candidates = nativeTexts.filter(entry => containsTokens(entry.text, textTokens(word.text)) && containsPoint(entry.bounds, bounds));
    if (candidates.length === 1) attributed.get(candidates[0].objectId)!.push({ word, bounds });
    else if (candidates.length > 1) ambiguous.add(token);
  }
  if (ambiguous.size) limitations.push(`Some PDF words on ${slideKey} match multiple nearby native text objects (${[...ambiguous].slice(0, 5).join(', ')}); they were not used as rendered-text proof.`);
  return attributed;
}
function linesFor(items: AttributedWord[]): { y: number; items: AttributedWord[] }[] {
  const lines: { y: number; items: AttributedWord[] }[] = [];
  for (const item of [...items].sort((a, b) => a.bounds.y - b.bounds.y || a.bounds.x - b.bounds.x)) {
    const explicit = item.word.lineId ?? item.word.lineIndex;
    const line = explicit !== undefined ? lines.find(l => l.items.some(v => (v.word.lineId ?? v.word.lineIndex) === explicit)) : lines.find(l => Math.abs(l.y - item.bounds.y) <= Math.max(2, item.bounds.h * .65));
    if (line) { line.items.push(item); line.y = Math.min(line.y, item.bounds.y); } else lines.push({ y: item.bounds.y, items: [item] });
  }
  return lines.sort((a, b) => a.y - b.y);
}
function orphanDiagnostics(compiledSlide: any, attributed: Map<string, AttributedWord[]>): EvidenceDiagnostic[] {
  const out: EvidenceDiagnostic[] = [];
  for (const { box, role } of compiledTextEntries(compiledSlide)) {
    if (intentional(role, box)) continue;
    const lines = linesFor(attributed.get(box.objectId) || []);
    // Tiny captions and page furniture are not prose-wrap candidates.
    if (lines.length < 2 || textTokens(String(box.text || '')).length < 5) continue;
    const last = lines[lines.length - 1].items, previous = lines[lines.length - 2].items;
    const finalText = last.map(x => x.word.text || '').join(' ').trim();
    if (previous.length >= 2 && last.length <= 1 && finalText.length <= 28) out.push({ code: 'ORPHAN_WRAP', severity: 'warning', slideKeys: [compiledSlide.key], detail: `The rendered final line of ${box.objectId} contains only “${finalText}”; inspect the PDF line break.`, objectIds: [box.objectId] });
  }
  return out;
}

export interface PdfTextCoverage { coverage: number; missingText: string[]; limitations: string[]; }
/**
 * Verify each visible block in its own native text region. This avoids
 * pdftotext -layout's multi-column reading order while refusing to let words
 * elsewhere on a page satisfy a block.
 */
export function pdfTextCoverage(compiled: CompiledDeck, native: DeckSnapshot, pdfWords: PdfWords): Map<string, PdfTextCoverage> {
  const limitations: string[] = [], leaves = allNativeLeaves(native as any, limitations), byId = new Map(leaves.map(leaf => [leaf.objectId, leaf]));
  const output = new Map<string, PdfTextCoverage>();
  for (let index = 0; index < (compiled?.slides || []).length; index++) {
    const slide = compiled.slides[index], local: string[] = [];
    const entries = nativeTextEntries(slide, byId, local);
    const slideWords = pdfWordsForSlide(pdfWords, index, slide.key, compiled.slides.length);
    // Readback has a stable object binding. Match each authored block to that
    // native object, not to another block that happens to repeat its words.
    // Individual-word ambiguity remains in geometry diagnostics; it does not
    // invalidate a complete, region-bound block readback on its own.
    const missing: string[] = [];
    const expectedBlocks = compiledTextEntries(slide).filter(({box,role}) => !intentional(role,box) && textTokens(String(box.text || '')).length > 0);
    for (const {box} of expectedBlocks) {
      const text=String(box.text), expected=textTokens(text), entry=entries.find(e=>e.objectId===box.objectId);
      if (!entry || textTokens(entry.text).join(' ')!==expected.join(' ')) { local.push(`Visible text object ${box.objectId} on ${slide.key} could not be mapped to matching native copy; PDF coverage was not cleared.`); missing.push(text); continue; }
      const actual=slideWords.flatMap(word=>{const bounds=pdfBounds(word);return bounds&&containsPoint(entry.bounds,bounds)?textTokens(word.text):[];});
      if (!containsTokens(actual.join(' '), expected)) missing.push(text);
    }
    output.set(slide.key, { coverage: expectedBlocks.length ? (expectedBlocks.length - missing.length) / expectedBlocks.length : 1, missingText: missing, limitations: [...new Set(local)] });
  }
  return output;
}

/**
 * Native and rendered word-bound intersections are warnings only: a bounding
 * box cannot prove a glyph collision. Rendered out-of-page words can be errors
 * when attributed by content and geography. This is not visual inspection.
 */
export function geometryDiagnostics(compiled: CompiledDeck, native: DeckSnapshot, pdfWords?: PdfWords): { collisions: EvidenceDiagnostic[]; orphanLines: EvidenceDiagnostic[]; limitations: string[] } {
  const limitations: string[] = [];
  const leaves = allNativeLeaves(native as any, limitations), byId = new Map(leaves.map(leaf => [leaf.objectId, leaf]));
  const page = nativePageSize(native as any);
  const collisions: EvidenceDiagnostic[] = [], orphanLines: EvidenceDiagnostic[] = [];
  for (let index = 0; index < (compiled?.slides || []).length; index++) {
    const slide = compiled.slides[index], texts = nativeTextEntries(slide, byId, limitations);
    for (let i = 0; i < texts.length; i++) for (let j = i + 1; j < texts.length; j++) {
      const a = texts[i], b = texts[j];
      if (intersects(a.bounds, b.bounds)) collisions.push({ code: 'NATIVE_TEXT_BOX_OVERLAP', severity: 'warning', slideKeys: [slide.key], detail: `Native text boxes ${a.objectId} and ${b.objectId} overlap; padding or reserved space may be involved, so rendered glyphs were not presumed to collide.`, objectIds: [a.objectId, b.objectId] });
    }
    for (const entry of texts) if (entry.bounds.x < -EPS || entry.bounds.y < -EPS || entry.bounds.x + entry.bounds.w > page.width + EPS || entry.bounds.y + entry.bounds.h > page.height + EPS) collisions.push({ code: 'NATIVE_TEXT_BOX_OUT_OF_BOUNDS', severity: 'warning', slideKeys: [slide.key], detail: `Native text box ${entry.objectId} extends outside slide bounds; rendered glyph placement requires PDF corroboration.`, objectIds: [entry.objectId] });
    if (!pdfWords) { limitations.push(`PDF word geometry was not supplied for ${slide.key}; rendered collision, rendered out-of-bounds, and orphan-wrap checks were not checked.`); continue; }
    const attributed = attributeWords(pdfWordsForSlide(pdfWords, index, slide.key, compiled.slides.length), texts, limitations, slide.key);
    for (const entry of texts) for (const item of attributed.get(entry.objectId) || []) if (item.bounds.x < -EPS || item.bounds.y < -EPS || item.bounds.x + item.bounds.w > page.width + EPS || item.bounds.y + item.bounds.h > page.height + EPS) collisions.push({ code: 'RENDERED_TEXT_OUT_OF_BOUNDS', severity: 'error', slideKeys: [slide.key], detail: `Rendered word “${item.word.text}” from ${entry.objectId} extends outside page bounds.`, objectIds: [entry.objectId] });
    for (let i = 0; i < texts.length; i++) for (let j = i + 1; j < texts.length; j++) {
      const a = texts[i], b = texts[j];
      const found = (attributed.get(a.objectId) || []).some(aw => (attributed.get(b.objectId) || []).some(bw => intersects(aw.bounds, bw.bounds)));
      if (found) collisions.push({ code: 'RENDERED_TEXT_OVERLAP', severity: 'warning', slideKeys: [slide.key], detail: `Rendered word bounds attributed to ${a.objectId} and ${b.objectId} overlap; inspect glyph placement because word bounds do not prove a glyph collision.`, objectIds: [a.objectId, b.objectId] });
    }
    orphanLines.push(...orphanDiagnostics(slide, attributed));
  }
  return { collisions, orphanLines, limitations: [...new Set(limitations)] };
}

/** Aggregate diagnostics; `inspected` remains false because diagnostics do not perform human inspection. */
export function renderDiagnostics(project: Project, compiled: CompiledDeck, native: DeckSnapshot, pdfWords?: PdfWords): DiagnosticChecks {
  const geometry = geometryDiagnostics(compiled, native, pdfWords);
  return { density: densityLedger(project, compiled), numerals: numeralDiagnostics(project, compiled), collisions: geometry.collisions, orphanLines: geometry.orphanLines, inspected: false, limitations: geometry.limitations };
}
