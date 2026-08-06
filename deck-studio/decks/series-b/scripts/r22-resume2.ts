// R22 resume — B4'..B8' adapted to live IDs (scaled title boxes replaced, not edited)
import { invokeTool } from '@tasklet/tools/v2';
import { batch, segs, st, box, rect, GOLD, LGOLD, GRAY, WHITE, DIM, PT, darkBg } from '/tasklet/agent/home/scripts/seriesb-rebuild/h.ts';

const RAW = 'https://raw.githubusercontent.com/jaideepdhanoa/navier-atlas/0bb7487248385431aa59fcdce9804d29164ca64a/deck-studio/assets/seriesb/r22/';
const TGRAY = { red: 0.62, green: 0.639, blue: 0.678 };
const CARD = { red: 0.075, green: 0.105, blue: 0.145 };

const g = await invokeTool({ connectionId: 'conn_9qpjytrfnwhbgs2sd9cf', toolName: 'google_slides_get_presentation', args: { presentationId: '1g95_1hKvlz8Pfar-fmhoUsONcJyu6-zPPfhvRhPxu4k', mode: 'slides', slideIndices: [16] } });
if (!g.ok) { console.log('FAIL ref', g.error); process.exit(1); }
const ref: any = await g.json();
function els(list: any[], out: any[] = []): any[] { for (const e of (list || [])) { out.push(e); if (e.elementGroup) els(e.elementGroup.children, out); } return out; }
const ee16 = els(ref.slides[0].pageElements);
const BG_URL = ee16.find((e: any) => e.objectId === 'g3f645480738_0_197')?.image?.contentUrl;
const LOGO_URL = ee16.find((e: any) => e.objectId === 'g3f645480738_0_200')?.image?.contentUrl;
if (!BG_URL || !LOGO_URL) { console.log('no ref urls'); process.exit(1); }

const del = (ids: string[]) => ids.map(id => ({ deleteObject: { objectId: id } }));
const img = (id: string, slide: string, x: number, y: number, w: number, h: number, url: string) => ({
  createImage: { objectId: id, url, elementProperties: { pageObjectId: slide, size: { width: { magnitude: w * PT, unit: 'EMU' }, height: { magnitude: h * PT, unit: 'EMU' } }, transform: { scaleX: 1, scaleY: 1, translateX: x * PT, translateY: y * PT, unit: 'EMU' } } },
});
const bgReqs = (slide: string, key: string) => [darkBg(slide), img(`r22bg_${key}`, slide, 0, 0, 720, 405, BG_URL), { updatePageElementsZOrder: { pageElementObjectIds: [`r22bg_${key}`], operation: 'SEND_TO_BACK' } }];
function tracker(slide: string, key: string, goldPart: string, grayPart: string) {
  const id = `r22trk_${key}`;
  return [box(id, slide, 403.2, 33, 300, 16.5), ...segs(id, [[goldPart, st(8, 700, GOLD)], [grayPart + '\n', st(8, 400, TGRAY)]], false),
    { updateParagraphStyle: { objectId: id, textRange: { type: 'ALL' }, style: { alignment: 'END' }, fields: 'alignment' } }];
}
const footer = (slide: string, key: string) => {
  const id = `r22ftr_${key}`;
  return [box(id, slide, 15.5, 388, 130, 8), ...segs(id, [['© 2026 -  Navier - Private & Confidential\n', st(5, 400, WHITE)]], false)];
};
const logo = (slide: string, key: string) => img(`r22logo_${key}`, slide, 682.5, 376.3, 27.6, 17.4, LOGO_URL);
const title = (slide: string, key: string, parts: [string, any][]) => {
  const id = `r22ttl_${key}`;
  return [box(id, slide, 45.6, 36, 620, 30), ...segs(id, parts, false)];
};
const T = (t: string) => [[t + '\n', st(17, 600, WHITE)]] as [string, any][];

// B4' — S5 graveyard reskin (tracker already exists as g3f6623c186e_4_98)
await batch([
  ...del(['r20img_sb_c3_grave', 'c3_title']),
  ...bgReqs('sb_c3_grave', 's5'),
  ...title('sb_c3_grave', 's5', T('It\u2019s Been Tried. The Sequence Was Wrong.')),
  ...footer('sb_c3_grave', 's5'), logo('sb_c3_grave', 's5'),
], 'B4 S5');

// B5' — slide 24 (g3f6623c186e_4_78) C1 gap reskin
await batch([
  ...del(['g3f6623c186e_4_79', 'g3f6623c186e_4_81', 'g3f6623c186e_4_92', 'g3f6623c186e_4_82']),
  ...bgReqs('g3f6623c186e_4_78', 'c1'),
  ...title('g3f6623c186e_4_78', 'c1', T('Cargo \u2014 The Gap Between Air and Ocean')),
  box('r22lede_c1', 'g3f6623c186e_4_78', 45.6, 70, 620, 16),
  ...segs('r22lede_c1', [
    ['Passenger networks run 16 hours a day \u2014 then sleep. ', st(10, 400, GRAY)],
    ['Cargo is the night shift.\n', st(10, 700, LGOLD)],
  ], false),
  ...tracker('g3f6623c186e_4_78', 'c1', 'THE SECOND ACT', '  \u2014  CARGO'),
  ...footer('g3f6623c186e_4_78', 'c1'), logo('g3f6623c186e_4_78', 'c1'),
], 'B5 C1');

// B6' — slide 25 (sb_c2_night) rebuild as split day/night
await batch([
  ...del(['c2_hero', 'c2_scrim', 'c2_title', 'c2_sub', 'c2_ch1bg', 'c2_ch1', 'c2_ch2bg', 'c2_ch2', 'c2_ch3bg', 'c2_ch3', 'c2_lbl']),
  ...bgReqs('sb_c2_night', 'c2'),
  ...title('sb_c2_night', 'c2', T('People by Day. Cargo by Night.')),
  box('r22lede_c2', 'sb_c2_night', 45.6, 70, 620, 30),
  ...segs('r22lede_c2', [
    ['The same hull earns twice \u2014 same corridors, same chargers, same software, no added capex. ', st(10, 400, GRAY)],
    ['Night hours are idle today; a modular hold turns them into freight revenue.\n', st(10, 700, LGOLD)],
  ], false),
  img('r22plate_c2', 'sb_c2_night', 45.6, 112, 420, 238, RAW + 'c2-plate.jpg'),
  ...rect('r22tagbg_c2', 'sb_c2_night', 375, 118, 84, 14, { red: 0.03, green: 0.045, blue: 0.065 }, 0.85),
  box('r22tag_c2', 'sb_c2_night', 377, 119.5, 80, 11),
  ...segs('r22tag_c2', [['CONCEPT RENDER\n', st(6, 600, DIM)]], false),
  { updateParagraphStyle: { objectId: 'r22tag_c2', textRange: { type: 'ALL' }, style: { alignment: 'CENTER' }, fields: 'alignment' } },
  ...rect('r22k1bg_c2', 'sb_c2_night', 480, 112, 195, 70, CARD, 0.94),
  box('r22k1_c2', 'sb_c2_night', 492, 122, 172, 52),
  ...segs('r22k1_c2', [['SAME VESSEL\n', st(8, 700, GOLD)], ['Modular hold \u2014 concept in design; no added capex on the hull.\n', st(8.5, 400, GRAY)]], false),
  ...rect('r22k2bg_c2', 'sb_c2_night', 480, 196, 195, 70, CARD, 0.94),
  box('r22k2_c2', 'sb_c2_night', 492, 206, 172, 52),
  ...segs('r22k2_c2', [['SAME NETWORK\n', st(8, 700, GOLD)], ['Piers, charging, and software already built and paid for by passengers.\n', st(8.5, 400, GRAY)]], false),
  ...rect('r22k3bg_c2', 'sb_c2_night', 480, 280, 195, 70, CARD, 0.94),
  box('r22k3_c2', 'sb_c2_night', 492, 290, 172, 52),
  ...segs('r22k3_c2', [['NEW REVENUE\n', st(8, 700, GOLD)], ['Freight rides on marginal cost \u2014 energy and handling only.\n', st(8.5, 400, GRAY)]], false),
  ...tracker('sb_c2_night', 'c2', 'THE SECOND ACT', '  \u2014  CARGO'),
  ...footer('sb_c2_night', 'c2'), logo('sb_c2_night', 'c2'),
], 'B6 C2');

// B7' — S26 C5 prize reskin
await batch([
  ...del(['r20img_sb_c5_prize', 'c5_eye', 'c5_title']),
  ...bgReqs('sb_c5_prize', 'c5'),
  ...title('sb_c5_prize', 'c5', T('Islands Pay the Most for the Slowest Service')),
  ...tracker('sb_c5_prize', 'c5', 'THE SECOND ACT', '  \u2014  CARGO'),
  ...footer('sb_c5_prize', 'c5'), logo('sb_c5_prize', 'c5'),
], 'B7 C5');

// B8' — chrome pass
await batch([
  ...segs('r21_wiw_title', T('The World Is Watching')),
  ...tracker('r21_wiw', 'wiw', '05', '  \u00b7  FINANCIALS & THE ASK'),
  logo('r21_wiw', 'wiw'),
  ...del(['sta_title']),
  ...title('st_r19_ask', 'ask', [['$10M Series B-1', st(17, 600, WHITE)], [' \u2014 First Close of ', st(17, 600, WHITE)], ['$100\u2013150M Series B\n', st(17, 700, LGOLD)]]),
  ...tracker('st_r19_ask', 'ask', '05', '  \u00b7  FINANCIALS & THE ASK'),
  ...footer('st_r19_ask', 'ask'), logo('st_r19_ask', 'ask'),
  ...del(['a1_eye', 'a1_title']),
  ...title('sb_cargo_econ', 'a1', T('Night Cargo \u2014 Parametric Economics')),
  ...tracker('sb_cargo_econ', 'a1', 'APPENDIX', '  \u00b7  ILLUSTRATIVE'),
  ...footer('sb_cargo_econ', 'a1'), logo('sb_cargo_econ', 'a1'),
  ...del(['r21_46eye']),
  ...tracker('g3f556ac5e67_1_798', 'a40', 'APPENDIX', '  \u00b7  DEFENSE VALIDATION'),
  ...footer('g3f556ac5e67_1_798', 'a40'), logo('g3f556ac5e67_1_798', 'a40'),
  ...del(['r21_44eye']),
  ...tracker('g3f556ac5e67_1_714', 'a39', 'APPENDIX', '  \u00b7  TECHNOLOGY MATURITY'),
  ...segs('g3f9515af747_0_117', [['APPENDIX', st(8, 700, GOLD)], ['  \u00b7  MARKET SIZING\n', st(8, 400, TGRAY)]]),
  ...tracker('sb_premium', 'a33', 'APPENDIX', '  \u00b7  UNIT ECONOMICS'),
  logo('sb_premium', 'a33'),
  ...tracker('g3f6623c186e_4_1', 'a35', 'APPENDIX', '  \u00b7  COMPETITIVE FIELD'),
  ...tracker('sb_prod_scale', 'a37', 'APPENDIX', '  \u00b7  PRODUCTION'),
  logo('sb_prod_scale', 'a37'),
  ...tracker('sb_prod_cost', 'a38', 'APPENDIX', '  \u00b7  PRODUCTION'),
  logo('sb_prod_cost', 'a38'),
  logo('sb_roadmap', 'a29'),
], 'B8 chrome');

console.log('R22 resume complete');
