import { batch, segs, box, st, rect, GOLD, GRAY, WHITE } from './h.ts';
const B = 'sg_coastal_13';
const R: any[] = [
  { deleteObject: { objectId: 'cl_pnl_bg' } },
  { deleteObject: { objectId: 'cl_pnl_tick' } },
  { deleteObject: { objectId: 'cl_pnl' } },
];
R.push(...rect('cl_pnl_bg2', B, 664, 372, 268, 126, { red: 0.055, green: 0.075, blue: 0.105 }, 0.9));
R.push(...rect('cl_pnl_tick2', B, 664, 372, 3, 126, GOLD, 1));
R.push(box('cl_pnl2', B, 680, 382, 240, 108));
R.push(...segs('cl_pnl2', [
  ['FIVE STOPS, ONE RIGHT-OF-WAY\n', st(11.5, 800, GOLD, { bold: true })],
  ['Commuters at the peaks — islands and the waterfront the rest of the day. Same boats, same charging points, one network.\n', st(10.5, 400, GRAY)],
  ['Starts with two boats. Grows stop by stop.\n', st(10.5, 700, WHITE, { bold: true })],
], false));
await batch(R, 'cl panel fix');
console.log('PANEL FIXED');
