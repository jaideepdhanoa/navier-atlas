// R28c — Jaideep 2026-08-06 evening: slide 23 de-verbose + Sampriti short-sea positioning;
// slide 28 realigned to $1.1T+ after Jaideep reverted appendix TAM slide to original.
import { invokeTool } from '@tasklet/tools/v2';
const SLIDES = 'conn_9qpjytrfnwhbgs2sd9cf', DRIVE = 'conn_t9cewrss13c4ycr82vyg';
const MASTER = '1g95_1hKvlz8Pfar-fmhoUsONcJyu6-zPPfhvRhPxu4k';
const MEMO = '10ba33SA2F6XhMgDJys1cqrGZYbC78RaT4QDmOtPaDl0';
const QA = '1KLMMdMuJSq8hmC1RTKM5lT54BD-wMnTNh08m9ZBW0So';
const S23 = 'g3f6623c186e_4_78', S28 = 'g3f6623c186e_4_268';

// --- 1) compute delete ranges for the two explainer lines on slide 23 ---
const g = await invokeTool({ connectionId: SLIDES, toolName: 'google_slides_get_presentation', args: { presentationId: MASTER, mode: 'slides', slideIndices: [23] } });
if (!g.ok) throw new Error('fetch s23: ' + g.error);
const page: any = ((await g.json()) as any).slides[0];
function shapeText(id: string): string {
  const el = (page.pageElements as any[]).find(e => e.objectId === id);
  return (el.shape.text.textElements as any[]).map((te: any) => te.textRun?.content || '').join('');
}
function lineRange(id: string, needle: string): { start: number; end: number } {
  const t = shapeText(id);
  const start = t.indexOf(needle);
  if (start < 0) throw new Error(`"${needle.slice(0, 30)}" not found in ${id}`);
  const nl = t.indexOf('\n', start);
  return { start, end: nl >= 0 ? nl + 1 : t.length }; // include trailing newline
}
const airDel = lineRange('g3f6623c186e_4_84', '$2.50 dense trunk lanes');
const oceanDel = lineRange('g3f6623c186e_4_86', '$0.03 full containers on trunk lanes');
console.log('delete ranges:', JSON.stringify({ airDel, oceanDel }));

// --- 2) deck batch: deletes + element-safe text replacements ---
const rep = (find: string, replaceText: string, pages: string[]) => ({ replaceAllText: { containsText: { text: find, matchCase: true }, replaceText, pageObjectIds: pages } });
const reqs: any[] = [
  { deleteText: { objectId: 'g3f6623c186e_4_84', textRange: { type: 'FIXED_RANGE', startIndex: airDel.start, endIndex: airDel.end } } },
  { deleteText: { objectId: 'g3f6623c186e_4_86', textRange: { type: 'FIXED_RANGE', startIndex: oceanDel.start, endIndex: oceanDel.end } } },
  rep('Navier Cargo — Addressing The Gap Between Air & Ocean Freight', 'Navier Cargo — The Gap Between Air & Ocean', [S23]),
  rep('Dedicated foiling freighters are the play; night freight on the passenger fleet is the pilot-phase test.', 'Short-sea and island freight — regional corridors, not ocean crossings.', [S23]),
  rep('Nothing on water is both fast and affordable. Every island, coast, and short-sea corridor lives in this gap — paying air prices or waiting on ocean time.', 'Islands and coasts pay air prices — or wait on ocean time.', [S23]),
  // keep the bold "We live this gap." lead-in untouched; swap only the regular-weight remainder
  rep('Our own Türkiye→U.S. vessel shipments:', 'Shipping our own vessels overseas:', [S23]),
  rep('Top-down ceiling: $600B+ across water mobility, logistics & defense', 'Top-down ceiling: $1.1T+ across mobility, logistics & security', [S28]),
];
const r1 = await invokeTool({ connectionId: SLIDES, toolName: 'google_slides_batch_update_presentation', args: { presentationId: MASTER, requests: reqs } });
if (!r1.ok) throw new Error('deck batch: ' + r1.error);
const j1: any = await r1.json();
const occ = (j1.replies || []).map((r: any) => r.replaceAllText?.occurrencesChanged ?? '—');
console.log('DECK OK — replies:', JSON.stringify(occ));

// --- 3) memo: short-sea scoping sentence + pilot framing already in place ---
const memoSubs: [string, string][] = [
  ['The play is dedicated foiling freighters on the same proven core',
   'This is a short-sea play — islands, coasts, and regional corridors; on ocean crossings, ships carrying thousands of containers are unbeatable on cost, and we do not compete there. The play is dedicated foiling freighters on the same proven core'],
];
for (const [find, replace] of memoSubs) {
  const r = await invokeTool({ connectionId: DRIVE, toolName: 'google_drive_replace_text_in_document', args: { documentId: MEMO, targetText: find, replacementText: replace } });
  console.log('MEMO', r.ok ? 'OK' : 'FAIL: ' + r.error);
}

// --- 4) Q&A bank: Q37 (Sampriti's transatlantic point, in the bank) ---
const q37 = `

**Q37 — Why can't you compete with container ships? What about transatlantic lanes?**
We don't try. A container ship moving 10,000+ boxes across an ocean is unbeatable on cost per kilogram — and large freighter aircraft own the urgent end of trunk lanes. Both modes need scale and infrastructure that only exist on trunk routes. Navier cargo is a short-sea play: islands, coasts, and regional corridors, typically 30–100 nm, where neither megaship nor freighter jet operates — the freight moves on slow feeder boats or expensive small planes, at the worst prices in either band. That is the gap we price inside ($0.75–1.50/kg), and it is exactly where our passenger networks already put piers, chargers, and software. Never claim trunk-lane or transoceanic economics.
`;
const r4 = await invokeTool({ connectionId: DRIVE, toolName: 'google_drive_append_text_to_document', args: { documentId: QA, text: q37 } });
console.log('QA', r4.ok ? 'OK' : 'FAIL: ' + r4.error);
