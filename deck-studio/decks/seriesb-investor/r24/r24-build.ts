// R24 — Jaideep Aug-6 round 2: 10% network share on payback P&L; cargo hierarchy inverted
// (dedicated vessels = the play, night wedge demoted); islands slide re-sourced to SIDS-specific stats.
import { batch, segs, st, box, rect, GOLD, LGOLD, GRAY, WHITE, DIM } from '/tasklet/agent/home/scripts/seriesb-rebuild/h.ts';

const HERO = 'https://raw.githubusercontent.com/jaideepdhanoa/navier-atlas/c2ce9dcca9f7aff68d800d8301d01ee9fdcfa1ba/deck-studio/assets/seriesb/r24/cargo-hero-v1.jpg';
const P = 'sb_premium';

// ============ A. Payback slide — Navier network share 10% ============
const labels = [
  'Revenue — 4 paid legs × 4.0 seats × $225',
  'Crew & operations',
  'Energy — electric, all 8 legs',
  'Maintenance subscription',
  'Parts & consumables',
  'Insurance',
  'Marina & berth',
  'Navier software — entry tier',
  'Navier network share — 10% of revenue',
  'Operating profit',
];
const vals = ['$1.08M', '$85K', '$15K', '$40K', '$25K', '$30K', '$15K', '$10K', '$108K', '$752K'];
const B = (i: number) => i === 0 || i === 9;
const a: any[] = [];
a.push(...segs(`${P}_pl0n`, labels.map((l, i) => [l + '\n', st(8, B(i) ? 700 : 400, B(i) ? WHITE : GRAY)] as [string, any]), true));
a.push(...segs(`${P}_pl1n`, vals.map((v, i) => [v + '\n', st(8, B(i) ? 800 : 500, B(i) ? LGOLD : WHITE)] as [string, any]), true));
for (const id of [`${P}_pl0n`, `${P}_pl1n`]) a.push({ updateParagraphStyle: { objectId: id, textRange: { type: 'ALL' }, style: { lineSpacing: 112, spaceAbove: { magnitude: 0, unit: 'PT' }, spaceBelow: { magnitude: 0, unit: 'PT' } }, fields: 'lineSpacing,spaceAbove,spaceBelow' } });
a.push(...segs(`${P}_pb`, [
  ['PAYBACK ~16 MONTHS\n', st(14, 800, LGOLD)],
  ['\u2248$7.5M cumulative operating profit over 10 years\n', st(7.5, 400, GRAY)],
], true));
a.push(...segs(`${P}_wr0v2`, [
  ['OPERATOR', st(9, 800, LGOLD)], [' — keeps the topline, carries the risk\n', st(9, 700, WHITE)],
  ['$1.08M revenue \u2212 $250K lease \u2212 $220K running costs \u2212 $108K network share = $502K a year.\n', st(7.5, 400, GRAY)],
], true));
a.push(...segs(`${P}_wr2v2`, [
  ['NAVIER', st(9, 800, LGOLD)], [' — earns on every hull, and on every fare\n', st(9, 700, WHITE)],
  ['A 10% network share on every fare booked, the $1M sale, then recurring software from ~$10K/yr (single vessel) to $60K\u2013120K/yr (fleet tier), plus maintenance subscription and parts. The P&L opposite shows the entry tier.\n', st(7.5, 400, GRAY)],
], true));
a.push(...segs(`${P}_bandtn`, [
  ['Own and operate: after Navier\u2019s 10% network share, the boat pays for itself in ~16 months. ', st(10, 800, LGOLD)],
  ['Leased: the operator clears $502K a year, the asset holder recovers the hull in 4 years and keeps ~6 more years of profit, and Navier earns on every hull — fleets form without Navier holding assets. Illustrative — terms flex with who carries the risk.\n', st(10, 400, GRAY)],
], true));
await batch(a, 'A payback network share');

// ============ B. New dedicated-cargo hero slide (dup of night slide chrome) ============
await batch([
  { duplicateObject: { objectId: 'sb_c2_night', objectIds: {
    sb_c2_night: 'r24_cargo_hero',
    'g3f6623c186e_4_212': 'r24ch_img',
    'g3f6623c186e_4_227': 'r24ch_ttl',
    r22lede_c2: 'r24ch_lede',
    r22k1_c2: 'r24ch_k1',
    r22k2_c2: 'r24ch_k2',
    r22k3_c2: 'r24ch_k3',
  } } },
], 'B1 duplicate');

await batch([
  { updateSlidesPosition: { slideObjectIds: ['r24_cargo_hero'], insertionIndex: 22 } },
  { replaceImage: { imageObjectId: 'r24ch_img', url: HERO, imageReplaceMethod: 'CENTER_CROP' } },
  { replaceAllText: { pageObjectIds: ['r24_cargo_hero'], containsText: { text: 'People by Day. Cargo by Night.', matchCase: true }, replaceText: 'The Play: Dedicated Cargo Vessels' } },
  ...segs('r24ch_lede', [
    ['Purpose-built foiling freighters — the hull designed around the hold, not adapted from a passenger boat. ', st(10, 400, GRAY)],
    ['Same foils, same drivetrain, same autonomy and software as every Navier vessel.\n', st(10, 700, LGOLD)],
  ], true),
  ...segs('r24ch_k1', [['PURPOSE-BUILT\n', st(8, 700, GOLD)], ['A freight hull designed around the hold — payload, loading, and range set by island logistics.\n', st(8.5, 400, GRAY)]], true),
  ...segs('r24ch_k2', [['ONE PLATFORM\n', st(8, 700, GOLD)], ['The same proven core as the passenger fleet — no re-invention to reach freight.\n', st(8.5, 400, GRAY)]], true),
  ...segs('r24ch_k3', [['NETWORK-READY\n', st(8, 700, GOLD)], ['Launches on corridors, piers, and chargers the passenger business already paid for.\n', st(8.5, 400, GRAY)]], true),
  ...rect('r24ch_tagbg', 'r24_cargo_hero', 620, 358, 84, 14, { red: 0.03, green: 0.045, blue: 0.065 }, 0.85),
  box('r24ch_tag', 'r24_cargo_hero', 622, 359.5, 80, 11),
  ...segs('r24ch_tag', [['CONCEPT RENDER\n', st(6, 600, DIM)]], false),
  { updateParagraphStyle: { objectId: 'r24ch_tag', textRange: { type: 'ALL' }, style: { alignment: 'CENTER' }, fields: 'alignment' } },
], 'B2 hero content');

// ============ C. Night slide demoted to the wedge ============
await batch([
  { replaceAllText: { pageObjectIds: ['sb_c2_night'], containsText: { text: 'People by Day. Cargo by Night.', matchCase: true }, replaceText: 'The Wedge: People by Day, Cargo by Night' } },
  ...segs('r22lede_c2', [
    ['Before the first dedicated freighter launches, cargo revenue can start on the passenger network — an optional modular hold turns idle night hours into freight. ', st(10, 400, GRAY)],
    ['One way in, not the model — the dedicated fleet does the heavy lifting.\n', st(10, 700, LGOLD)],
  ], true),
], 'C night wedge');

// ============ D. Islands slide — SIDS-specific stats ============
await batch([
  ...segs('c5_s1', [
    ['2×\n', st(26, 800, LGOLD)],
    ['what small island states pay for the international transport of their imports, compared with developed countries\n\n', st(10.5, 400, WHITE)],
    ['UNCTAD, 2021', st(8.5, 400, DIM)],
  ], true),
  ...segs('c5_s3', [
    ['29 of 50\n', st(26, 800, LGOLD)],
    ['of the world\u2019s least-connected shipping economies are small island states — the longest ship turnaround times and lowest service frequencies\n\n', st(10.5, 400, WHITE)],
    ['UNCTAD / UN-OHRLLS, 2021', st(8.5, 400, DIM)],
  ], true),
], 'D islands SIDS');

console.log('R24 build complete');
