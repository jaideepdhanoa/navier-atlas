// R26d — Jaideep 2026-08-06: rebase S34 premium payback P&L to $0.30/kWh mid-band.
// Energy $15K → $23K · running $220K → $228K · profit $752K → $744K · 10yr $7.5M → $7.4M ·
// leased operator $502K → $494K. Also fixes stale battery-reserve footnote (pre-R24 basis
// $810–830K → $694–714K) and notes the tariff in fn4.
// pl1n has TWO "$15K" values (energy line 3, marina line 7) → index-based edit for that element.
import { invokeTool } from '@tasklet/tools/v2';
const PRES = '1g95_1hKvlz8Pfar-fmhoUsONcJyu6-zPPfhvRhPxu4k';
const SLIDE = 'sb_premium';

// 1. Fetch slide, find pl1n, reconstruct text + paragraph offsets
const g = await invokeTool({ connectionId: 'conn_9qpjytrfnwhbgs2sd9cf', toolName: 'google_slides_get_presentation', args: { presentationId: PRES, mode: 'slides', slideIndices: [34] } });
if (!g.ok) { console.log('ERR get', g.error); process.exit(1); }
const pres: any = await g.json();
const page = pres.slides.find((s: any) => s.objectId === SLIDE);
function findEl(els: any[], id: string): any {
  for (const e of els ?? []) {
    if (e.objectId === id) return e;
    if (e.elementGroup) { const r = findEl(e.elementGroup.children, id); if (r) return r; }
  }
  return null;
}
const pl1n = findEl(page.pageElements, 'sb_premium_pl1n');
if (!pl1n?.shape?.text) { console.log('ERR pl1n not found'); process.exit(1); }
let full = '';
for (const te of pl1n.shape.text.textElements ?? []) if (te.textRun) full += te.textRun.content;
console.log('pl1n text:', JSON.stringify(full));

// Locate exact ranges of line 3 ("$15K" after "$85K\n") and line 10 ("$752K")
const lines = full.split('\n');
console.log('lines:', JSON.stringify(lines));
// compute start index of each line
const starts: number[] = []; let acc = 0;
for (const ln of lines) { starts.push(acc); acc += ln.length + 1; }
const energyLine = lines.findIndex((l, i) => l === '$15K' && i <= 4); // first $15K = energy
const profitLine = lines.findIndex(l => l === '$752K');
if (energyLine < 0 || profitLine < 0) { console.log('ERR lines not located', energyLine, profitLine); process.exit(1); }
const eStart = starts[energyLine], pStart = starts[profitLine];
console.log(`energy "$15K" @ ${eStart}, profit "$752K" @ ${pStart}`);

// 2. Batch: index edits (highest first) + scoped replaces
const requests: any[] = [
  // profit line first (higher index)
  { deleteText: { objectId: 'sb_premium_pl1n', textRange: { type: 'FIXED_RANGE', startIndex: pStart, endIndex: pStart + 5 } } },
  { insertText: { objectId: 'sb_premium_pl1n', insertionIndex: pStart, text: '$744K' } },
  { deleteText: { objectId: 'sb_premium_pl1n', textRange: { type: 'FIXED_RANGE', startIndex: eStart, endIndex: eStart + 4 } } },
  { insertText: { objectId: 'sb_premium_pl1n', insertionIndex: eStart, text: '$23K' } },
  // payback strip: 10-yr cumulative
  { replaceAllText: { pageObjectIds: [SLIDE], containsText: { text: '≈$7.5M cumulative', matchCase: true }, replaceText: '≈$7.4M cumulative' } },
  // narrative band: leased operator
  { replaceAllText: { pageObjectIds: [SLIDE], containsText: { text: 'the operator clears $502K a year', matchCase: true }, replaceText: 'the operator clears $494K a year' } },
  // operator card math
  { replaceAllText: { pageObjectIds: [SLIDE], containsText: { text: '$220K running costs − $108K network share = $502K a year', matchCase: true }, replaceText: '$228K running costs − $108K network share = $494K a year' } },
  // footnote: tariff note + stale battery-reserve fix
  { replaceAllText: { pageObjectIds: [SLIDE], containsText: { text: 'Energy & software from the live Maldives operating model', matchCase: true }, replaceText: 'Energy & software from the live Maldives operating model — electricity at the mid-band commercial tariff ($0.30/kWh)' } },
  { replaceAllText: { pageObjectIds: [SLIDE], containsText: { text: 'a $30–50K/yr reserve moves owner-operator profit to ~$810–830K', matchCase: true }, replaceText: 'a $30–50K/yr reserve moves owner-operator profit to ~$694–714K' } },
];
const b = await invokeTool({ connectionId: 'conn_9qpjytrfnwhbgs2sd9cf', toolName: 'google_slides_batch_update_presentation', args: { presentationId: PRES, requests } });
if (!b.ok) { console.log('ERR batch', b.error); process.exit(1); }
const res: any = await b.json();
const occ = (res.replies ?? []).map((r: any) => r.replaceAllText ? (r.replaceAllText.occurrencesChanged ?? 0) : '-');
console.log('replies:', JSON.stringify(occ));

// 3. Verify: re-fetch and print pl1n + key strings
const g2 = await invokeTool({ connectionId: 'conn_9qpjytrfnwhbgs2sd9cf', toolName: 'google_slides_get_presentation', args: { presentationId: PRES, mode: 'slides', slideIndices: [34] } });
const pres2: any = await g2.json();
const page2 = pres2.slides.find((s: any) => s.objectId === SLIDE);
function allText(els: any[]): string {
  let out = '';
  for (const e of els ?? []) {
    if (e.shape?.text) for (const te of e.shape.text.textElements ?? []) if (te.textRun) out += te.textRun.content;
    if (e.elementGroup) out += allText(e.elementGroup.children);
  }
  return out;
}
const t = allText(page2.pageElements);
for (const probe of ['$23K', '$744K', '$7.4M', '$494K', '$228K', '$0.30/kWh', '$694–714K']) console.log(probe, t.includes(probe) ? 'OK' : 'MISSING');
for (const gone of ['$752K', '$502K', '$7.5M', '$810–830K']) console.log('gone', gone, t.includes(gone) ? 'STILL PRESENT!' : 'OK');
// sum check
console.log('sum check: 1080-85-23-40-25-30-15-10-108 =', 1080-85-23-40-25-30-15-10-108);
