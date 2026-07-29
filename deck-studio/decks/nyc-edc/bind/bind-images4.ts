// Rebind S11 candidate map with v2 plate (commit 23007047)
import { batch } from './h.ts';
const SHA = '23007047cb1746b88c96fb0f8ad6dc190daaab95';
const url = `https://raw.githubusercontent.com/jaideepdhanoa/navier-atlas/${SHA}/deck-studio/assets/nyc-edc/city-maps/edc-candidate-links-exact-route-map.png`;
await batch([
  { replaceImage: { imageObjectId: 'g3f4f11d95ee_0_238', url, imageReplaceMethod: 'CENTER_CROP' } },
], 's11-map-v2');
console.log('DONE');
