// R21b — restore "The World Is Watching" close (rebuilt from PDF render after wrong-slide cut)
// + swap brightened C5 island plate
import { batch, segs, st, box, rect, gline, darkBg, GOLD, LGOLD, GRAY, WHITE, DIM, PT } from '/tasklet/agent/home/scripts/seriesb-rebuild/h.ts';

const SHA = '3a76546203d241ecd9e6ab6b827d29cbbed99a74';
const RAW = `https://raw.githubusercontent.com/jaideepdhanoa/navier-atlas/${SHA}/deck-studio/assets/seriesb/r21/`;
const S = 'r21_wiw';

const R: any[] = [];
R.push({ createSlide: { objectId: S, insertionIndex: 29, slideLayoutReference: { predefinedLayout: 'BLANK' } } });
R.push(darkBg(S));
// title + gold rule
R.push(box('r21_wiw_title', S, 46, 30, 500, 30));
R.push(...segs('r21_wiw_title', [['The World Is Watching', st(20, 600, WHITE)]], false));
R.push(...gline('r21_wiw_rule', S, 46, 64, 130));
// press collage (single plate, 1920x825 → 628x270pt at 46,80)
R.push({ createImage: { objectId: 'r21_wiw_img', url: RAW + 'wiw-collage.png', elementProperties: { pageObjectId: S, size: { width: { magnitude: 628 * PT, unit: 'EMU' }, height: { magnitude: 270 * PT, unit: 'EMU' } }, transform: { scaleX: 1, scaleY: 1, translateX: 46 * PT, translateY: 80 * PT, unit: 'EMU' } } } });
// full-circle close band (R20 P3 line, restored verbatim)
R.push(box('r21_wiw_band', S, 40, 358, 640, 34));
R.push(...segs('r21_wiw_band', [
  ['People by day. Cargo by night. Defense on the same platform. ', st(12, 700, WHITE, { bold: true })],
  ['Every coastline a network — every marina a Navier hub.', st(12, 700, LGOLD, { bold: true })],
], false));
R.push({ updateParagraphStyle: { objectId: 'r21_wiw_band', textRange: { type: 'ALL' }, style: { alignment: 'CENTER' }, fields: 'alignment' } });
// footer
R.push(box('r21_wiw_foot', S, 16, 386, 220, 14));
R.push(...segs('r21_wiw_foot', [['\u00A9 2026 \u2013 Navier \u2013 Private & Confidential', st(6, 400, DIM)]], false));
// C5 brightened plate swap
R.push({ replaceImage: { imageObjectId: 'r20img_sb_c5_prize', imageReplaceMethod: 'CENTER_CROP', url: RAW + 'c5-prize-v2.jpg' } });

await batch(R, 'R21b restore close + C5 swap');
console.log('done');
