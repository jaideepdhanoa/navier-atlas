import { batch, rect } from '/tasklet/agent/home/scripts/seriesb-rebuild/h.ts';
const NAVY = { red: 0.055, green: 0.075, blue: 0.105 };
const R: any[] = [];
R.push(...rect('r21_46cov1', 'g3f556ac5e67_1_798', 0, 26, 720, 26, NAVY, 1));
R.push(...rect('r21_46cov2', 'g3f556ac5e67_1_798', 0, 370, 720, 35, NAVY, 1));
R.push({ updatePageElementsZOrder: { pageElementObjectIds: ['r21_46cov1', 'r21_46cov2'], operation: 'SEND_TO_BACK' } });
await batch(R, 'p40 layout-bleed covers');
