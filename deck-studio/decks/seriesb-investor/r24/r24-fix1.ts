import { batch, rect } from '/tasklet/agent/home/scripts/seriesb-rebuild/h.ts';
await batch([
  ...rect('r24ch_trkbg', 'r24_cargo_hero', 528, 30.5, 178, 16, { red: 0.03, green: 0.045, blue: 0.065 }, 0.8),
  { updatePageElementsZOrder: { pageElementObjectIds: ['SLIDES_API579993857_7'], operation: 'BRING_TO_FRONT' } },
], 'tracker chip');
