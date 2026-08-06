import { batch, rect } from '/tasklet/agent/home/scripts/seriesb-rebuild/h.ts';
const NAVY = { red: 0.055, green: 0.075, blue: 0.105 };
const R: any[] = [...rect('r21_46cov3', 'g3f556ac5e67_1_798', 0, 6, 720, 22, NAVY, 1)];
R.push({ updatePageElementsZOrder: { pageElementObjectIds: ['r21_46cov3'], operation: 'SEND_TO_BACK' } });
await batch(R, 'p40 header rule cover');
