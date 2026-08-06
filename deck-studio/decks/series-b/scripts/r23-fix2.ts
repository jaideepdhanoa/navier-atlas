import { batch, segs, st, GOLD } from '../h.ts';
const SLATE = { red: 0.62, green: 0.639, blue: 0.678 };
await batch([
  ...segs('g3f6623c186e_4_154', [
    ['APPENDIX', st(8, 700, GOLD)],
    ['  ·  WHY PRIOR ATTEMPTS FAILED\n', st(8, 400, SLATE)],
  ]),
], 'fix2 slide41 appendix tracker');
