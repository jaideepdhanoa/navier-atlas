// NYC EDC image bind v2 — replace full-bleed IMAGE ELEMENTS (chassis uses elements, not page fills)
import { batch } from './h.ts';

const SHA = 'c36efe977a67fa6ba5aa1db5e06edcfbc85b4655';
const RAW = `https://raw.githubusercontent.com/jaideepdhanoa/navier-atlas/${SHA}/`;
const B = RAW + 'deck-studio/assets/backgrounds/decks/blade/';

const img = (el: string, url: string, method: 'CENTER_INSIDE' | 'CENTER_CROP') => ({
  replaceImage: { imageObjectId: el, url, imageReplaceMethod: method },
});

const R: any[] = [
  img('g3f94a5edd10_0_3', B + 'blade-cover-hero-ny-harbor-v3.png', 'CENTER_CROP'),      // S1 cover element
  img('g3f94a5edd10_0_522', B + 'blade-slide10-partner_roles_bg-v2.png', 'CENTER_CROP'), // S9 mandate element
  img('wnet_bg', B + 'blade-econ-ny-harbor-bg-v2.png', 'CENTER_CROP'),                   // S10 network element
  img('appr_bg', B + 'blade-slide12-close_bg-v2.png', 'CENTER_CROP'),                    // S15 approach element
  img('g3f4f11d95ee_0_240', B + 'blade-slide12-close_bg-v3.png', 'CENTER_CROP'),         // S19 close element
];
await batch(R, 'image-bind-v2');
console.log('DONE');
