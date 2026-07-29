// Revert S9/S10 page backgrounds to original solid dark (10,18,28); element photos stay
import { batch } from './h.ts';
const dark = { red: 10 / 255, green: 18 / 255, blue: 28 / 255 };
const solid = (page: string) => ({
  updatePageProperties: {
    objectId: page,
    pageProperties: { pageBackgroundFill: { solidFill: { color: { rgbColor: dark } } } },
    fields: 'pageBackgroundFill',
  },
});
await batch([solid('g3f94a5edd10_0_521'), solid('wnetslide')], 'bg-revert');
console.log('DONE');
