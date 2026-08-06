// R23 — Jaideep Aug-6 edits: native slide 2, full-bleed slide 3, cargo slides 21/22 re-anchored
import { batch, segs, box, rect, gline, darkBg, st, PT, GOLD, LGOLD, GRAY, WHITE, DIM } from '../h.ts';
import { readFileSync } from 'node:fs';

const S2 = 'g3f673ef3b6b_2_0';   // new inserted slide (pasted image)
const S3 = 'st_r19_claim';       // full-bleed target
const C1 = 'g3f6623c186e_4_78';  // cargo gap
const C5 = 'sb_c5_prize';        // islands pay most

import { invokeTool } from '@tasklet/tools/v2';
// fresh logo contentUrl from reference slide 16 (g3f645480738_0_196)
const ref = await invokeTool({ toolName: 'google_slides_get_presentation', connectionId: 'conn_9qpjytrfnwhbgs2sd9cf', args: { presentationId: '1g95_1hKvlz8Pfar-fmhoUsONcJyu6-zPPfhvRhPxu4k', mode: 'slides', slideIndices: [16] } });
if (!ref.ok) { console.log('FAIL ref fetch', ref.error); process.exit(1); }
const refd: any = await ref.json();
const LOGO_URL = (refd.slides[0].pageElements || []).find((e: any) => e.objectId === 'g3f645480738_0_200')?.image?.contentUrl;
if (!LOGO_URL) { console.log('FAIL no logo url'); process.exit(1); }

const d = JSON.parse(readFileSync('/tmp/r23/slides.json', 'utf8'));
const slide = (id: string) => d.slides.find((s: any) => s.objectId === id);
const el = (sid: string, eid: string) => slide(sid).pageElements.find((e: any) => e.objectId === eid);

// clone a text box (geometry + per-run text/styles) onto another slide with a new id
function cloneTextBox(src: any, newId: string, pageId: string, newText?: string): any[] {
  const reqs: any[] = [{ createShape: { objectId: newId, shapeType: 'TEXT_BOX', elementProperties: { pageObjectId: pageId, size: src.size, transform: src.transform } } }];
  const runs: { text: string, style: any }[] = [];
  for (const t of (src.shape.text?.textElements || [])) if (t.textRun) runs.push({ text: t.textRun.content, style: t.textRun.style || {} });
  if (newText !== undefined) {
    // single-style clone: use first non-empty run's style
    const style = (runs.find(r => r.text.trim().length) || runs[0]).style;
    reqs.push({ insertText: { objectId: newId, insertionIndex: 0, text: newText } });
    const f = ['foregroundColor','bold','italic','fontFamily','fontSize','weightedFontFamily'].filter(k => style[k] !== undefined);
    reqs.push({ updateTextStyle: { objectId: newId, textRange: { type: 'ALL' }, style: Object.fromEntries(f.map(k => [k, style[k]])), fields: f.join(',') } });
  } else {
    const full = runs.map(r => r.text).join('');
    if (full.length) {
      reqs.push({ insertText: { objectId: newId, insertionIndex: 0, text: full } });
      let idx = 0;
      for (const r of runs) {
        const f = ['foregroundColor','bold','italic','fontFamily','fontSize','weightedFontFamily'].filter(k => r.style[k] !== undefined);
        if (r.text.trim().length && f.length) reqs.push({ updateTextStyle: { objectId: newId, textRange: { type: 'FIXED_RANGE', startIndex: idx, endIndex: idx + r.text.length }, style: Object.fromEntries(f.map(k => [k, r.style[k]])), fields: f.join(',') } });
        idx += r.text.length;
      }
    }
  }
  return reqs;
}

function vline(id: string, pageId: string, x: number, y: number, h: number, color: any, weightPt: number) {
  return [
    { createLine: { objectId: id, lineCategory: 'STRAIGHT', elementProperties: { pageObjectId: pageId, size: { width: { magnitude: 1, unit: 'EMU' }, height: { magnitude: h * PT, unit: 'EMU' } }, transform: { scaleX: 1, scaleY: 1, translateX: x * PT, translateY: y * PT, unit: 'EMU' } } } },
    { updateLineProperties: { objectId: id, lineProperties: { lineFill: { solidFill: { color: { rgbColor: color }, alpha: 1 } }, weight: { magnitude: Math.round(weightPt * PT), unit: 'EMU' } }, fields: 'lineFill,weight' } },
  ];
}
function hline(id: string, pageId: string, x: number, y: number, w: number, color: any, weightPt: number) {
  return [
    { createLine: { objectId: id, lineCategory: 'STRAIGHT', elementProperties: { pageObjectId: pageId, size: { width: { magnitude: w * PT, unit: 'EMU' }, height: { magnitude: 1, unit: 'EMU' } }, transform: { scaleX: 1, scaleY: 1, translateX: x * PT, translateY: y * PT, unit: 'EMU' } } } },
    { updateLineProperties: { objectId: id, lineProperties: { lineFill: { solidFill: { color: { rgbColor: color }, alpha: 1 } }, weight: { magnitude: Math.round(weightPt * PT), unit: 'EMU' } }, fields: 'lineFill,weight' } },
  ];
}
const center = (id: string) => ({ updateParagraphStyle: { objectId: id, textRange: { type: 'ALL' }, style: { alignment: 'CENTER' }, fields: 'alignment' } });
const endAlign = (id: string) => ({ updateParagraphStyle: { objectId: id, textRange: { type: 'ALL' }, style: { alignment: 'END' }, fields: 'alignment' } });

// ---------- PART A: slide 2 native rebuild ----------
{
  const s3 = slide(S3);
  const title = el(S3, 'g3f6623c186e_4_221');
  const trk = el(S3, 'r22trk_s2');
  const ftr = el(S3, 'r22ftr_s2');
  const logo = el(S3, 'r22logo_s2');
  const AXIS = { red: 0.32, green: 0.37, blue: 0.45 };
  const reqs: any[] = [
    { deleteObject: { objectId: 'g3f673ef3b6b_2_3' } },
    darkBg(S2),
    ...cloneTextBox(title, 'r23title_s2n', S2, 'The World Runs at the Speed Goods Move\n'),
    ...gline('r23uline_s2n', S2, 45.5, 68.4, 157.5),
    ...cloneTextBox(trk, 'r23trk_s2n', S2),
    ...cloneTextBox(ftr, 'r23ftr_s2n', S2),
    { createImage: { objectId: 'r23logo_s2n', url: LOGO_URL, elementProperties: { pageObjectId: S2, size: logo.size, transform: logo.transform } } },
    // lede
    box('r23lede_s2n', S2, 46, 84, 520, 22),
    ...segs('r23lede_s2n', [["On the ocean, that speed hasn't changed in 70 years.\n", st(13, 400, GRAY)]], false),
    // chart: axes + flat gold line
    ...vline('r23yaxis', S2, 200, 150, 158, AXIS, 1),
    ...hline('r23xaxis', S2, 200, 308, 420, AXIS, 1),
    ...hline('r23flat', S2, 200, 200, 420, GOLD, 2.5),
    // labels
    box('r23ylab', S2, 120, 192, 72, 16),
    ...segs('r23ylab', [['20 knots\n', st(11, 600, WHITE)]], false), endAlign('r23ylab'),
    box('r23x1', S2, 198, 316, 60, 16),
    ...segs('r23x1', [['1956\n', st(11, 400, GRAY)]], false),
    box('r23x2', S2, 562, 316, 58, 16),
    ...segs('r23x2', [['2026\n', st(11, 400, GRAY)]], false), endAlign('r23x2'),
    box('r23xmid', S2, 300, 316, 220, 16),
    ...segs('r23xmid', [['average speed of a container ship\n', st(10, 400, DIM)]], false), center('r23xmid'),
    box('r23cap', S2, 160, 348, 500, 20),
    ...segs('r23cap', [['Ships got bigger. They never got faster.\n', st(12.5, 600, LGOLD)]], false), center('r23cap'),
  ];
  await batch(reqs, 'A slide2 native rebuild');
}

// ---------- PART B: slide 3 full bleed ----------
{
  const bg = el(S3, 'r22bg_s2');
  const W = bg.size.width.magnitude;   // 31600 EMU
  const H = bg.size.height.magnitude;  // 21200 EMU
  const sc = 9144000 / W;              // full-bleed width
  const ty = Math.round((5143500 - H * sc) / 2);
  const reqs: any[] = [
    { deleteObject: { objectId: 'r22plate_s2' } },
    { updatePageElementProperties: undefined } as any, // placeholder removed below
  ].filter((r: any) => r.updatePageElementProperties === undefined ? r.deleteObject : true);
  const reqs2: any[] = [
    { deleteObject: { objectId: 'r22plate_s2' } },
    { updatePageElementTransform: { objectId: 'r22bg_s2', applyMode: 'ABSOLUTE', transform: { scaleX: sc, scaleY: sc, translateX: 0, translateY: ty, unit: 'EMU' } } },
    ...rect('r23panel_s3', S3, 34, 86, 386, 272, { red: 0.043, green: 0.059, blue: 0.086 }, 0.68),
    { updatePageElementsZOrder: { pageElementObjectIds: ['r23panel_s3'], operation: 'SEND_TO_BACK' } },
    { updatePageElementsZOrder: { pageElementObjectIds: ['r22bg_s2'], operation: 'SEND_TO_BACK' } },
  ];
  await batch(reqs2, 'B slide3 fullbleed');
}

// ---------- PART C: slide 21 cargo gap — feature price per kg ----------
{
  const hdr = st(15, 700, WHITE, { bold: true });
  const big = st(24, 700, LGOLD, { bold: true });
  const sub = st(10.5, 400, GRAY);
  const smallGap = st(4, 400, GRAY);
  const reqs: any[] = [
    ...segs('g3f6623c186e_4_84', [
      ['AIR\n', hdr],
      ['$2.50–4.50/kg\n', big],
      ['Hours — airport to airport only\n', sub],
      ['\n', smallGap],
      ['Carries 35% of world trade value on under 1% of its tonnage\n', sub],
    ]),
    ...segs('g3f6623c186e_4_86', [
      ['OCEAN\n', hdr],
      ['$0.03–0.50/kg\n', big],
      ['Weeks — plus port dwell time\n', sub],
      ['\n', smallGap],
      ['250M containers a year on fixed port-to-port schedules\n', sub],
    ]),
    ...segs('g3f6623c186e_4_91', [
      ['Sources: Freightos Air Index (Aug 2026) · industry ocean rate surveys 2025–26 · IATA / ICAO (air trade value & tonnage shares, 2024)\n', st(8, 400, DIM)],
    ]),
  ];
  await batch(reqs, 'C slide21 price-first');
}

// ---------- PART D: slide 22 islands — label global, evidence "slowest" ----------
{
  const big = st(24, 700, LGOLD, { bold: true });
  const sub = st(10.5, 400, GRAY);
  const src = st(9, 400, DIM);
  const gap = st(5, 400, GRAY);
  const reqs: any[] = [
    ...segs('c5_s2', [
      ['$5,563/TEU\n', big],
      ['what small islands paid per container in H1 2024 — the highest freight rates of any country grouping, after a 137% spike\n', sub],
      ['\n', gap],
      ['UNCTAD, 2024\n', src],
    ]),
    ...segs('c5_s3', [
      ['70% longer\n', big],
      ['the wait for a berth in developing-economy ports — 10.9 hours vs 6.4 in developed ones. Highest prices, slowest service.\n', sub],
      ['\n', gap],
      ['UNCTAD, 2025\n', src],
    ]),
    ...segs('c5_band', [
      ['The world pays airlines ', st(12, 400, WHITE)],
      ['$141–157B a year', st(12, 700, LGOLD, { bold: true })],
      [' to escape slow ocean freight (IATA, global). No vessel has ever priced that gap — ', st(12, 400, WHITE)],
      ['the network that already earns on passengers is the first that can.', st(12, 700, LGOLD, { bold: true })],
    ]),
  ];
  await batch(reqs, 'D slide22 clarity');
}
console.log('R23 build complete');
