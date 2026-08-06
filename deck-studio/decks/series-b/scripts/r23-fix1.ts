import { batch, segs, st, LGOLD, GRAY, WHITE } from '../h.ts';
const hdr = st(15, 700, WHITE, { bold: true });
const big = st(24, 700, LGOLD, { bold: true });
const suf = st(13, 700, LGOLD, { bold: true });
const sub = st(10.5, 400, GRAY);
const gap = st(4, 400, GRAY);
await batch([
  ...segs('g3f6623c186e_4_84', [
    ['AIR\n', hdr],
    ['$2.50–4.50', big], [' /kg\n', suf],
    ['Hours — airport to airport only\n', sub],
    ['\n', gap],
    ['Carries 35% of world trade value on under 1% of its tonnage\n', sub],
  ]),
  ...segs('g3f6623c186e_4_86', [
    ['OCEAN\n', hdr],
    ['$0.03–0.50', big], [' /kg\n', suf],
    ['Weeks — plus port dwell time\n', sub],
    ['\n', gap],
    ['250M containers a year on fixed port-to-port schedules\n', sub],
  ]),
], 'fix1 price suffix');
