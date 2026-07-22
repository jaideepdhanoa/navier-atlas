// Jaideep R2 visual pass 2026-07-22: text-free plates + native titles/legends,
// coastal-line breakthrough slide, MOT reframe, SG closing composite.
import { batch, segs, box, st, gline, rect, GOLD, LGOLD, GRAY, WHITE, PT } from './h.ts';
import { readFile } from 'node:fs/promises';

const BASE = 'https://raw.githubusercontent.com/jaideepdhanoa/navier-atlas/6ca1ebf28cf00d5ab64531296d266e0bf9922066/deck-studio/assets/singapore-mpa';
const NAVY = { red: 0.055, green: 0.075, blue: 0.105 };
const FOOT = { red: 0.62, green: 0.65, blue: 0.68 };

// ---------- pass 1: image swaps ----------
const swaps: [string, string][] = [
  ['wnet_bg', 'sg-network-today-v2.png'],            // S13 your network today
  ['g3f58907cd6f_0_17', 'sg-candidate-links-v2.png'],// S14 the opportunity
  ['cl_map', 'sg-coastal-express-v2.png'],           // S16 coastal line
  ['g3f529cd9c8a_0_7', 'sg-horizon-today-v2.png'],   // S20 today
  ['g3f529cd9c8a_0_13', 'sg-horizon-tomorrow-v2.png'],// S20 tomorrow
  ['g3f4f11d95ee_0_240', 'sg-closing-n30-marina-dusk.png'], // S23 closing (top layer)
  ['g3f58907cd6f_0_87', 'sg-closing-n30-marina-dusk.png'],  // S23 closing (base layer)
];
for (const [id, f] of ([] as [string,string][])) {
  await batch([{ replaceImage: { imageObjectId: id, imageReplaceMethod: 'CENTER_CROP', url: `${BASE}/${f}` } }], `img ${f}`);
}

// ---------- pass 2: native titles + legends ----------
const R: any[] = [];
const S13 = 'wnetslide', S14 = 'g3f58907cd6f_0_0', S16 = 'sg_coastal_13', S17 = 'sg_agencies_14';

// S13 — map plate title/legend (was baked into PNG)
R.push(box('wnet_mt', S13, 378, 108, 420, 18));
R.push(...segs('wnet_mt', [['WATER TRANSPORT TODAY\n', st(11, 800, LGOLD, { bold: true })]], false));
R.push(box('wnet_ml', S13, 378, 126, 480, 14));
R.push(...segs('wnet_ml', [['Ferries & bumboats · green = the electric ferry already running daily\n', st(8.5, 400, FOOT)]], false));
R.push(box('wnet_mc', S13, 640, 420, 300, 12));
R.push(...segs('wnet_mc', [['Illustrative — approximate anchors\n', st(7, 400, FOOT)]], false));

// S14 — candidate links title/legend + caption (was baked into PNG)
R.push(box('opp_mt', S14, 268, 110, 520, 20));
R.push(...segs('opp_mt', [['CANDIDATE LINKS TO STUDY TOGETHER\n', st(12, 800, LGOLD, { bold: true })]], false));
R.push(box('opp_ml', S14, 268, 130, 620, 14));
R.push(...segs('opp_ml', [['Gold = candidate links · Grey dash = running today · Green dash = electric ferry today\n', st(8.5, 400, FOOT)]], false));
R.push(box('opp_mc', S14, 650, 500, 290, 12));
R.push(...segs('opp_mc', [['Illustrative — pending joint study with MPA\n', st(7, 400, FOOT)]], false));

// S16 — standard header + subtitle + gold rule (plate now text-free)
R.push(box('cl_hd', S16, 61, 48, 640, 28));
R.push(...segs('cl_hd', [['THE COASTAL LINE\n', st(23, 600, WHITE)]], false));
R.push(...gline('cl_rule', S16, 61, 91, 80));
R.push(box('cl_sub', S16, 61, 102, 840, 26));
R.push(...segs('cl_sub', [['A coast-hugging express on a right-of-way that already exists — five stops, zero land take.\n', st(15, 400, GRAY)]], false));

// S16 — breakthrough chips (honest, computed from route geometry + N30 cruise spec)
const chips: [string, string, string][] = [
  ['cl_ch0', '≈ 15 MIN', 'EAST COAST ↔ CBD, PIER TO PIER'],
  ['cl_ch1', '~56 KM', 'OF OPEN RIGHT-OF-WAY, FIVE STOPS'],
  ['cl_ch2', 'ZERO', 'LAND TAKE · NO TUNNELLING'],
];
chips.forEach(([id, num, cap], i) => {
  const x = 61 + i * 200;
  R.push(...rect(id + '_bg', S16, x, 458, 186, 46, NAVY, 0.92));
  R.push(...rect(id + '_tk', S16, x, 458, 186, 2.5, GOLD, 1));
  R.push(box(id, S16, x + 12, 464, 166, 36));
  R.push(...segs(id, [
    [num + '  ', st(14, 800, GOLD, { bold: true })],
    [cap + '\n', st(9, 700, WHITE, { bold: true })],
  ], false));
});

// S16 — sources line now must carry the time-estimate method
R.push(...segs('cl_src', [['Sources: Navier network study — corridor illustrative, anchors at existing piers · times estimated pier-to-pier at N30 cruise speed (20 kn) · alignment and stops pending joint study with MPA\n', st(7.5, 400, FOOT)]]));

// S17 — MOT reframe (verified: MPA + LTA are statutory boards under MOT)
R.push(...segs('g3f58907cd6f_0_28', [['ONE WATERWAY, TWO MANDATES, ONE MINISTRY\n', st(23, 600, WHITE)]]));
R.push(...segs('ag_sub', [['MPA and LTA answer to one ministry — Transport. The coastal line serves both agendas, and it starts with the MPA.\n', st(15, 400, GRAY)]]));
R.push(...segs('ag_bandtx', [
  ['THE SEQUENCE\n', st(9.5, 600, LGOLD)],
  ['START INSIDE MPA\u2019S MANDATE', st(13.5, 700, WHITE, { bold: true })],
  ['   ·   ', st(13.5, 700, GOLD, { bold: true })],
  ['PROVE IT ON THE WATER', st(13.5, 700, WHITE, { bold: true })],
  ['   ·   ', st(13.5, 700, GOLD, { bold: true })],
  ['BRING LTA AND MOT IN WITH DATA\n', st(13.5, 700, WHITE, { bold: true })],
]));

await batch(R, 'native titles + breakthrough + MOT');

// ---------- pass 3: add Changi Point ↔ East Coast to the S14 candidate list ----------
const live = JSON.parse(await readFile('live.json', 'utf8'));
let content = '';
outer: for (const s of live.slides) {
  for (const e of s.pageElements ?? []) {
    if (e.objectId === 'g3f58907cd6f_0_18') {
      content = (e.shape?.text?.textElements ?? []).map((t: any) => t.textRun?.content ?? '').join('');
      break outer;
    }
  }
}
const marker = 'Changi Point ↔ Pulau Ubin\n';
const at = content.indexOf(marker);
if (at < 0) throw new Error('marker not found in candidate list');
const insertionIndex = at + marker.length;
await batch([{ insertText: { objectId: 'g3f58907cd6f_0_18', insertionIndex, text: 'Changi Point ↔ East Coast\n' } }], 'candidate list +1');

console.log('R2 VISUAL PASS DONE');
