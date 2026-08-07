// R28b — Jaideep 2026-08-06: explain the air/ocean freight bands (floor→ceiling) on slide 23,
// mirror in memo §cargo, add Q36 to Q&A bank. One-pager carries no bands — exempt.
import { invokeTool } from '@tasklet/tools/v2';
import { readFileSync } from 'node:fs';

const SLIDES = 'conn_9qpjytrfnwhbgs2sd9cf', DRIVE = 'conn_t9cewrss13c4ycr82vyg';
const MASTER = '1g95_1hKvlz8Pfar-fmhoUsONcJyu6-zPPfhvRhPxu4k';
const MEMO = '10ba33SA2F6XhMgDJys1cqrGZYbC78RaT4QDmOtPaDl0';
const QA = '1KLMMdMuJSq8hmC1RTKM5lT54BD-wMnTNh08m9ZBW0So';

const AIR_LINE = '$2.50 dense trunk lanes → $4.50 thin and urgent lanes\n';
const OCEAN_LINE = '$0.03 full containers on trunk lanes → $0.50 parcels on island lanes\n';
const SMALL_STYLE = {
  foregroundColor: { opaqueColor: { rgbColor: { red: 0.827451, green: 0.827451, blue: 0.827451 } } },
  bold: false, italic: false, fontFamily: 'Exo 2',
  fontSize: { magnitude: 10.5, unit: 'PT' },
  weightedFontFamily: { fontFamily: 'Exo 2', weight: 400 },
};
const FIELDS = 'foregroundColor,bold,italic,fontFamily,fontSize,weightedFontFamily';

// 1) Slide 23 — insert explainer line right under each big number
const reqs = [
  { insertText: { objectId: 'g3f6623c186e_4_84', insertionIndex: 19, text: AIR_LINE } },
  { updateTextStyle: { objectId: 'g3f6623c186e_4_84', textRange: { type: 'FIXED_RANGE', startIndex: 19, endIndex: 19 + AIR_LINE.length }, style: SMALL_STYLE, fields: FIELDS } },
  { insertText: { objectId: 'g3f6623c186e_4_86', insertionIndex: 21, text: OCEAN_LINE } },
  { updateTextStyle: { objectId: 'g3f6623c186e_4_86', textRange: { type: 'FIXED_RANGE', startIndex: 21, endIndex: 21 + OCEAN_LINE.length }, style: SMALL_STYLE, fields: FIELDS } },
];
const r1 = await invokeTool({ connectionId: SLIDES, toolName: 'google_slides_batch_update_presentation', args: { presentationId: MASTER, requests: reqs } });
console.log('SLIDE 23:', r1.ok ? 'OK' : 'FAIL — ' + r1.error);

// 2) Memo — band qualifiers, element-scoped exact strings
const memoSubs: [string, string][] = [
  ['air freight ($8 trillion of goods a year at $2.50–4.50 per kilogram)',
   'air freight ($8 trillion of goods a year at $2.50–4.50 per kilogram — dense trunk lanes at the floor, thin and urgent lanes at the ceiling)'],
  ['container shipping ($7 trillion at cents per kilogram)',
   'container shipping ($7 trillion at $0.03–0.50 per kilogram — full containers on trunk lanes at the floor, small parcels on island lanes at the ceiling)'],
];
for (const [find, replace] of memoSubs) {
  const r = await invokeTool({ connectionId: DRIVE, toolName: 'google_drive_replace_text_in_document', args: { documentId: MEMO, targetText: find, replacementText: replace } });
  if (!r.ok) { console.log('MEMO FAIL:', find.slice(0, 50), '—', r.error); continue; }
  const j = await r.json();
  console.log('MEMO OK:', find.slice(0, 45), '→ replacements:', JSON.stringify(j).slice(0, 120));
}

// 3) Q&A bank — append Q36
const q36 = readFileSync('/tmp/r28/q36.md', 'utf8');
const r3 = await invokeTool({ connectionId: DRIVE, toolName: 'google_drive_append_text_to_document', args: { documentId: QA, text: q36 } });
console.log('QA Q36:', r3.ok ? 'OK' : 'FAIL — ' + r3.error);
