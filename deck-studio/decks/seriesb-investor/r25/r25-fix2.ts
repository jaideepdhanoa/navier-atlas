import { batch, segs, st, GOLD, GRAY } from '/tasklet/agent/home/scripts/seriesb-rebuild/h.ts';
await batch([
  ...segs('a1_par', [
    ['Measured the operator\u2019s way — missions per vessel-day and cost per kilogram, not brochure speed.\n', st(11, 800, GOLD)],
    ['N45-class night shift · payload 1–2 t · 2–4 night legs · $0.75–1.50/kg (air $2.50–4.50, ocean $0.03–0.50) · 300 nights/yr.', st(11, 400, GRAY)],
  ], true),
], 'S35 par two-line');
