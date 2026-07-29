// NYC EDC image bind — PR #342 SHA c36efe977a67fa6ba5aa1db5e06edcfbc85b4655
import { batch } from './h.ts';

const SHA = 'c36efe977a67fa6ba5aa1db5e06edcfbc85b4655';
const RAW = `https://raw.githubusercontent.com/jaideepdhanoa/navier-atlas/${SHA}/`;
const B = RAW + 'deck-studio/assets/backgrounds/decks/blade/';
const M = RAW + 'deck-studio/assets/nyc-edc/city-maps/';

const bg = (page: string, url: string) => ({
  updatePageProperties: {
    objectId: page,
    pageProperties: { pageBackgroundFill: { stretchedPictureFill: { contentUrl: url } } },
    fields: 'pageBackgroundFill',
  },
});
const img = (el: string, url: string, method: 'CENTER_INSIDE' | 'CENTER_CROP' = 'CENTER_INSIDE') => ({
  replaceImage: { imageObjectId: el, url, imageReplaceMethod: method },
});

const R: any[] = [
  bg('p1', B + 'blade-cover-hero-ny-harbor-v3.png'),                    // S1 cover
  bg('g3f94a5edd10_0_521', B + 'blade-slide10-partner_roles_bg-v2.png'), // S9 mandate
  bg('wnetslide', B + 'blade-econ-ny-harbor-bg-v2.png'),                 // S10 network today
  img('g3f4f11d95ee_0_238', M + 'edc-candidate-links-exact-route-map.png'), // S11 map
  bg('p11', B + 'blade-slide12-close_bg-v2.png'),                        // S15 approach
  img('g3f529cd9c8a_0_7', M + 'edc-horizon-today-exact-route-map.png'),  // S17 today
  img('g3f529cd9c8a_0_13', M + 'edc-horizon-tomorrow-exact-route-map.png'), // S17 tomorrow
  bg('g3f4f11d95ee_0_239', B + 'blade-slide12-close_bg-v3.png'),         // S19 close
];
await batch(R, 'image-bind');
console.log('DONE');
