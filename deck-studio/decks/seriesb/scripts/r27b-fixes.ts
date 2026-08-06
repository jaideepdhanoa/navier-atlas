// R27b — render fixes: tag position, circle numerals, slide-23 strip length
import { PT, GOLD, LGOLD, GRAY, WHITE, DIM, batch, st, segs, box } from '../h';
const S4 = 'g3f6828eb436_1_110', S5 = 'g3f6828eb436_1_114', S23 = 'g3f6623c186e_4_78';
const BGC = { red: 0.055, green: 0.075, blue: 0.105 };
const TAGGRAY = { red: 0.62, green: 0.639, blue: 0.678 };
const center = (id: string) => ({ updateParagraphStyle: { objectId: id, textRange: { type: 'ALL' }, style: { alignment: 'CENTER' }, fields: 'alignment' } });
const moveY = (id: string, x: number, y: number) => ({ updatePageElementTransform: { objectId: id, transform: { scaleX: 1, scaleY: 1, translateX: x*PT, translateY: y*PT, unit: 'EMU' }, applyMode: 'ABSOLUTE' } });

const R: any[] = [];
// 1) chapter tags up to kicker line (y20), clear of 20pt titles
R.push(moveY('r27s4_tag', 403, 20));
R.push(moveY('r27s5_tag', 403, 20));
// 2) slide 5 circle numerals: strip in-shape text, overlay centered boxes
const CX = [100, 204, 308, 412, 516, 620], CY = 150;
const KIND = ['done','done','now','next','next','next'];
CX.forEach((cx, i) => {
  R.push({ deleteText: { objectId: `r27s5_c${i}`, textRange: { type: 'ALL' } } });
  const color = KIND[i] === 'next' ? TAGGRAY : BGC;
  const n = `0${i+1}`;
  R.push(box(`r27s5_c${i}_n`, S5, cx-20, CY-7.5, 40, 15));
  R.push(...segs(`r27s5_c${i}_n`, [[n, st(10.5, 700, color, { bold: true })]], false));
  R.push(center(`r27s5_c${i}_n`));
});
// 3) slide 23: single-line strip, revert source append
R.push(...segs('r27c23_tx', [
  ['We live this gap. ', st(9.5, 700, LGOLD, { bold: true })],
  ['Our own Türkiye→U.S. vessel shipments: ~$40K and ~40 days by sea — or ~$400K and 2–3 days by air.', st(9.5, 400, WHITE)],
], true));
R.push({ replaceAllText: { pageObjectIds: [S23], containsText: { text: 'shares, 2024) · Türkiye→U.S. shipment times & costs: Navier operating experience (2026)', matchCase: true }, replaceText: 'shares, 2024) · Türkiye→U.S. lane: Navier shipments (2026)' } });
await batch(R, 'r27b fixes');
console.log('done');
