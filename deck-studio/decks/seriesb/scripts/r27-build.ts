// R27 — Sampriti's new slides 4 & 5 rebuilt natively + slide 23 founder anecdote (2026-08-06)
// Slide 4: THE NETWORK SHIFT — from a few giant ships to thousands of fast ones (two-panel network diagram)
// Slide 5: THE MASTER PLAN — prove the system, then compound the network (6-phase timeline)
// Slide 23: "We live this gap" Türkiye shipping anecdote strip
// NOTE: phase 05 uses "80–220 ft" (public N80/N120/N220 ladder), NOT Sampriti's "80–180 ft" — LC-180 firewall.
import { PRES, PT, GOLD, LGOLD, GRAY, WHITE, DIM, batch, st, segs, box, rect, gline, darkBg } from '../h';
import { readFileSync } from 'node:fs';

const S4 = 'g3f6828eb436_1_110', S5 = 'g3f6828eb436_1_114', S23 = 'g3f6623c186e_4_294'.replace('294','78') && 'g3f6623c186e_4_78';
const S23id = 'g3f6623c186e_4_78'; // slide 23 pageObjectId
const BGC = { red: 0.055, green: 0.075, blue: 0.105 };
const PANEL = { red: 0.09, green: 0.114, blue: 0.157 };
const PANEL2 = { red: 0.106, green: 0.133, blue: 0.184 };
const TAGGRAY = { red: 0.62, green: 0.639, blue: 0.678 };

function dot(id: string, slide: string, cx: number, cy: number, r: number, color: any, alpha = 1) {
  return [
    { createShape: { objectId: id, shapeType: 'ELLIPSE', elementProperties: { pageObjectId: slide, size: { width: { magnitude: 2*r*PT, unit: 'EMU' }, height: { magnitude: 2*r*PT, unit: 'EMU' } }, transform: { scaleX: 1, scaleY: 1, translateX: (cx-r)*PT, translateY: (cy-r)*PT, unit: 'EMU' } } } },
    { updateShapeProperties: { objectId: id, shapeProperties: { shapeBackgroundFill: { solidFill: { color: { rgbColor: color }, alpha } }, outline: { propertyState: 'NOT_RENDERED' } }, fields: 'shapeBackgroundFill,outline' } },
  ];
}
function seg(id: string, slide: string, x1: number, y1: number, x2: number, y2: number, color: any, weightPt: number, alpha = 1) {
  const W = Math.max(Math.abs(x2-x1), 0.01), H = Math.max(Math.abs(y2-y1), 0.01);
  return [
    { createLine: { objectId: id, lineCategory: 'STRAIGHT', elementProperties: { pageObjectId: slide, size: { width: { magnitude: W*PT, unit: 'EMU' }, height: { magnitude: H*PT, unit: 'EMU' } }, transform: { scaleX: x2 >= x1 ? 1 : -1, scaleY: y2 >= y1 ? 1 : -1, translateX: x1*PT, translateY: y1*PT, unit: 'EMU' } } } },
    { updateLineProperties: { objectId: id, lineProperties: { lineFill: { solidFill: { color: { rgbColor: color }, alpha } }, weight: { magnitude: weightPt*PT, unit: 'EMU' } }, fields: 'lineFill,weight' } },
  ];
}
const center = (id: string) => ({ updateParagraphStyle: { objectId: id, textRange: { type: 'ALL' }, style: { alignment: 'CENTER' }, fields: 'alignment' } });
const right = (id: string) => ({ updateParagraphStyle: { objectId: id, textRange: { type: 'ALL' }, style: { alignment: 'END' }, fields: 'alignment' } });
const outlineGold = (id: string, alpha: number, wPt = 0.75) => ({ updateShapeProperties: { objectId: id, shapeProperties: { outline: { outlineFill: { solidFill: { color: { rgbColor: GOLD }, alpha } }, weight: { magnitude: wPt*PT, unit: 'EMU' } } }, fields: 'outline' } });
const outlineGray = (id: string, alpha: number, wPt = 0.75) => ({ updateShapeProperties: { objectId: id, shapeProperties: { outline: { outlineFill: { solidFill: { color: { rgbColor: DIM }, alpha } }, weight: { magnitude: wPt*PT, unit: 'EMU' } } }, fields: 'outline' } });
const midAlign = (id: string) => ({ updateShapeProperties: { objectId: id, shapeProperties: { contentAlignment: 'MIDDLE' }, fields: 'contentAlignment' } });

// N logo url harvested from live slide 7 (Slides re-hosts on insert)
let LOGO_URL = '';
try { const s7 = JSON.parse(readFileSync('/tmp/r27/slide7.json', 'utf8')); LOGO_URL = s7.pageElements.find((e: any) => e.objectId === 'g3f6828eb436_1_274')?.image?.contentUrl ?? ''; } catch {}

function chrome(slide: string, p: string) {
  const R: any[] = [];
  R.push(box(`${p}_tag`, slide, 403, 33, 300, 16));
  R.push(...segs(`${p}_tag`, [['01', st(8, 700, GOLD, { bold: true })], ['  ·  THESIS & TEAM', st(8, 500, TAGGRAY)]], false));
  R.push(box(`${p}_ftr`, slide, 16, 388, 130, 8));
  R.push(...segs(`${p}_ftr`, [['© 2026 -  Navier - Private & Confidential', st(5, 400, DIM)]], false));
  if (LOGO_URL) R.push({ createImage: { objectId: `${p}_logo`, url: LOGO_URL, elementProperties: { pageObjectId: slide, size: { width: { magnitude: 28*PT, unit: 'EMU' }, height: { magnitude: 17*PT, unit: 'EMU' } }, transform: { scaleX: 1, scaleY: 1, translateX: 683*PT, translateY: 376*PT, unit: 'EMU' } } } });
  return R;
}

// ============ SLIDE 4 ============
const r4: any[] = [];
r4.push({ deleteObject: { objectId: 'g3f6828eb436_1_113' } });
r4.push({ deleteObject: { objectId: 'g3f6828eb436_1_332' } });
r4.push(darkBg(S4));
r4.push(box('r27s4_kick', S4, 39, 20, 300, 14));
r4.push(...segs('r27s4_kick', [['THE NETWORK SHIFT', st(9, 700, GOLD, { bold: true })]], false));
r4.push(box('r27s4_title', S4, 38, 36, 660, 30));
r4.push(...segs('r27s4_title', [
  ['From a few giant ships to ', st(20, 600, WHITE)],
  ['thousands of fast ones.', st(20, 600, LGOLD)],
], false));
r4.push(...gline('r27s4_ul', S4, 40, 72, 158));
// left panel — shipping today
r4.push(...rect('r27s4_pl', S4, 40, 88, 310, 240, PANEL, 1));
r4.push(outlineGray('r27s4_pl', 0.35));
r4.push(box('r27s4_pll', S4, 55, 100, 280, 12));
r4.push(...segs('r27s4_pll', [['SHIPPING TODAY', st(8.5, 700, DIM, { bold: true })]], false));
r4.push(box('r27s4_plh', S4, 55, 114, 280, 16));
r4.push(...segs('r27s4_plh', [['A handful of mega-ports.', st(12.5, 600, WHITE)]], false));
// sparse legacy network
const LN: [number, number, number][] = [[95,200,9],[300,185,8],[185,222,5],[118,275,7],[278,272,7]];
const LE: [number, number][] = [[0,1],[0,2],[2,1],[0,3],[3,4],[4,1],[0,4]];
LE.forEach(([a,b], i) => r4.push(...seg(`r27s4_le${i}`, S4, LN[a][0], LN[a][1], LN[b][0], LN[b][1], DIM, 2.2, 0.75)));
LN.forEach(([cx,cy,r], i) => r4.push(...dot(`r27s4_ln${i}`, S4, cx, cy, r, DIM, 0.95)));
r4.push(box('r27s4_plc', S4, 55, 306, 280, 12));
r4.push(...segs('r27s4_plc', [['20 knots · infrequent departures · fixed terminals', st(8, 400, GRAY)]], false));
// right panel — navier network
r4.push(...rect('r27s4_pr', S4, 370, 88, 310, 240, PANEL, 1));
r4.push(outlineGold('r27s4_pr', 0.45));
r4.push(box('r27s4_prl', S4, 385, 100, 280, 12));
r4.push(...segs('r27s4_prl', [['THE NAVIER NETWORK', st(8.5, 700, LGOLD, { bold: true })]], false));
r4.push(box('r27s4_prh', S4, 385, 114, 280, 16));
r4.push(...segs('r27s4_prh', [['Every harbor and marina becomes a hub.', st(12.5, 600, WHITE)]], false));
// dense navier mesh
const RN: [number, number, number][] = [
  [400,182,4],[450,163,4],[500,192,4],[553,165,4],[607,180,4],[655,200,4],
  [413,235,4],[467,255,4],[522,236,4],[577,257,4],[640,242,4],
  [443,290,3],[557,292,3],[615,287,3],[527,152,2.5],[663,268,2.5],
];
const RE: [number, number][] = [
  [0,1],[1,2],[2,3],[3,4],[4,5],[6,7],[7,8],[8,9],[9,10],
  [11,7],[11,6],[12,9],[12,8],[13,10],[13,9],[0,6],[1,6],[2,8],[3,8],[4,9],[5,10],[2,7],[14,3],[15,10],[4,10],
];
RE.forEach(([a,b], i) => r4.push(...seg(`r27s4_re${i}`, S4, RN[a][0], RN[a][1], RN[b][0], RN[b][1], GOLD, 0.9, 0.4)));
RN.forEach(([cx,cy,r], i) => r4.push(...dot(`r27s4_rn${i}`, S4, cx, cy, r, GOLD, 1)));
r4.push(box('r27s4_prc', S4, 385, 306, 280, 12));
r4.push(...segs('r27s4_prc', [['30 knots · departures all day · direct routes', st(8, 400, GRAY)]], false));
// bottom lines
r4.push(box('r27s4_bl', S4, 40, 342, 390, 30));
r4.push(...segs('r27s4_bl', [['Marinas are the nodes, vessels are the links, containers and passengers are the packets — and NavierOS is the protocol.', st(9, 400, GRAY, { italic: true })]], false));
r4.push(box('r27s4_br', S4, 430, 348, 250, 26));
r4.push(...segs('r27s4_br', [['The internet did this to information.\nWe are doing it to payloads.', st(9.5, 500, LGOLD, { italic: true })]], false));
r4.push(right('r27s4_br'));
r4.push(...chrome(S4, 'r27s4'));

// ============ SLIDE 5 ============
const r5: any[] = [];
r5.push({ deleteObject: { objectId: 'g3f6828eb436_1_117' } });
r5.push(darkBg(S5));
r5.push(box('r27s5_kick', S5, 39, 20, 300, 14));
r5.push(...segs('r27s5_kick', [['THE MASTER PLAN', st(9, 700, GOLD, { bold: true })]], false));
r5.push(box('r27s5_title', S5, 38, 36, 660, 30));
r5.push(...segs('r27s5_title', [
  ['Prove the system. ', st(20, 600, WHITE)],
  ['Then compound the network.', st(20, 600, LGOLD)],
], false));
r5.push(...gline('r27s5_ul', S5, 40, 72, 158));
// timeline
const CX = [100, 204, 308, 412, 516, 620], CY = 150, R = 16;
r5.push(...seg('r27s5_cl1', S5, CX[0], CY, CX[2], CY, GOLD, 1.2, 0.9));       // progress
r5.push(...seg('r27s5_cl2', S5, CX[2], CY, CX[5], CY, DIM, 1, 0.5));          // remaining
const PHASES = [
  { n: '01', name: 'Prove flight', desc: 'Foils · controls ·\nmanufacturing', tag: 'PIONEER', kind: 'done' },
  { n: '02', name: 'Prove endurance', desc: 'Hybrid · range ·\nreliability', tag: 'QUANTA', kind: 'done' },
  { n: '03', name: 'Prove network', desc: 'First fleet ·\nfirst geography', tag: 'MALDIVES', kind: 'now' },
  { n: '04', name: 'Add throughput', desc: '45 ft · people +\nexpress cargo', tag: 'REGIONAL', kind: 'next' },
  { n: '05', name: 'Scale corridors', desc: '80–220 ft · ferries +\nlogistics', tag: 'GLOBAL', kind: 'next' },
  { n: '06', name: 'Own the nodes', desc: 'Ports · energy ·\nservice', tag: 'NETWORK', kind: 'next' },
];
PHASES.forEach((ph, i) => {
  const cx = CX[i], id = `r27s5_c${i}`;
  const fill = ph.kind === 'done' ? GOLD : ph.kind === 'now' ? WHITE : PANEL;
  r5.push(...dot(id, S5, cx, CY, R, fill, 1));
  if (ph.kind === 'now') r5.push(outlineGold(id, 1, 1.5));
  if (ph.kind === 'next') r5.push(outlineGray(id, 0.7, 1));
  const numColor = ph.kind === 'next' ? TAGGRAY : BGC;
  r5.push({ insertText: { objectId: id, insertionIndex: 0, text: ph.n } });
  r5.push({ updateTextStyle: { objectId: id, textRange: { type: 'ALL' }, style: st(10.5, 700, numColor, { bold: true }), fields: 'weightedFontFamily,fontSize,foregroundColor,bold' } });
  r5.push(center(id));
  r5.push(midAlign(id));
  r5.push(box(`${id}_nm`, S5, cx-55, 176, 110, 14));
  r5.push(...segs(`${id}_nm`, [[ph.name, st(9.5, 700, WHITE, { bold: true })]], false));
  r5.push(center(`${id}_nm`));
  r5.push(box(`${id}_ds`, S5, cx-55, 191, 110, 26));
  r5.push(...segs(`${id}_ds`, [[ph.desc, st(7.5, 400, GRAY)]], false));
  r5.push(center(`${id}_ds`));
  r5.push(box(`${id}_tg`, S5, cx-55, 222, 110, 12));
  r5.push(...segs(`${id}_tg`, [[ph.tag, st(7.5, 700, LGOLD, { bold: true })]], false));
  r5.push(center(`${id}_tg`));
});
r5.push(box('r27s5_now', S5, CX[2]-25, 116, 50, 12));
r5.push(...segs('r27s5_now', [['NOW', st(8, 700, GOLD, { bold: true })]], false));
r5.push(center('r27s5_now'));
// bottom bar
r5.push(...rect('r27s5_bar', S5, 40, 292, 640, 56, PANEL2, 1));
r5.push(outlineGold('r27s5_bar', 0.55));
r5.push(...rect('r27s5_barg', S5, 40, 292, 2, 56, GOLD, 1));
r5.push(box('r27s5_barl', S5, 60, 306, 430, 30));
r5.push(...segs('r27s5_barl', [
  ['The vessel creates the route. ', st(13, 700, WHITE, { bold: true })],
  ['The route creates the node.', st(13, 700, LGOLD, { bold: true })],
], false));
r5.push(box('r27s5_barr', S5, 495, 302, 172, 38));
r5.push(...segs('r27s5_barr', [['Each phase lowers risk and expands the addressable network.', st(8, 400, GRAY)]], false));
r5.push(right('r27s5_barr'));
r5.push(...chrome(S5, 'r27s5'));

// ============ SLIDE 23 — founder anecdote strip ============
const r23: any[] = [];
r23.push(...rect('r27c23_bar', S23id, 40, 336, 640, 26, PANEL2, 1));
r23.push(...rect('r27c23_g', S23id, 40, 336, 1.5, 26, GOLD, 1));
r23.push(box('r27c23_tx', S23id, 52, 341, 620, 17));
r23.push(...segs('r27c23_tx', [
  ['We live this gap. ', st(9.5, 700, LGOLD, { bold: true })],
  ['Shipping one vessel from our Türkiye factory to the U.S.: ~$40K and ~40 days by sea — or ~$400K and 2–3 days by air. Nothing in between.', st(9.5, 400, WHITE)],
], false));
r23.push({ replaceAllText: { pageObjectIds: [S23id], containsText: { text: 'shares, 2024)', matchCase: true }, replaceText: 'shares, 2024) · Türkiye→U.S. shipment times & costs: Navier operating experience (2026)' } });

await batch(r4, 'slide 4 native rebuild');
await batch(r5, 'slide 5 native rebuild');
await batch(r23, 'slide 23 anecdote strip');
console.log('R27 build complete');
