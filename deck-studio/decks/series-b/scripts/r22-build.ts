// R22 — legibility redesign + plain-English arc + chrome normalization (Sampriti feedback 2026-08-05)
import { invokeTool } from '@tasklet/tools/v2';
import { batch, segs, st, box, rect, GOLD, LGOLD, GRAY, WHITE, DIM, PT, darkBg } from '/tasklet/agent/home/scripts/seriesb-rebuild/h.ts';

const RAW = 'https://raw.githubusercontent.com/jaideepdhanoa/navier-atlas/0bb7487248385431aa59fcdce9804d29164ca64a/deck-studio/assets/seriesb/r22/';
const TGRAY = { red: 0.62, green: 0.639, blue: 0.678 };
const CARD = { red: 0.075, green: 0.105, blue: 0.145 };

// 0) fetch standard bg + logo contentUrls from reference slide 16
const g = await invokeTool({ connectionId: 'conn_9qpjytrfnwhbgs2sd9cf', toolName: 'google_slides_get_presentation', args: { presentationId: '1g95_1hKvlz8Pfar-fmhoUsONcJyu6-zPPfhvRhPxu4k', mode: 'slides', slideIndices: [16] } });
if (!g.ok) { console.log('FAIL ref fetch', g.error); process.exit(1); }
const ref: any = await g.json();
function els(list: any[], out: any[] = []): any[] { for (const e of (list || [])) { out.push(e); if (e.elementGroup) els(e.elementGroup.children, out); } return out; }
const ee16 = els(ref.slides[0].pageElements);
const BG_URL = ee16.find((e: any) => e.objectId === 'g3f645480738_0_197')?.image?.contentUrl;
const LOGO_URL = ee16.find((e: any) => e.objectId === 'g3f645480738_0_200')?.image?.contentUrl;
if (!BG_URL || !LOGO_URL) { console.log('FAIL missing ref urls'); process.exit(1); }

const del = (ids: string[]) => ids.map(id => ({ deleteObject: { objectId: id } }));
const img = (id: string, slide: string, x: number, y: number, w: number, h: number, url: string) => ({
  createImage: { objectId: id, url, elementProperties: { pageObjectId: slide, size: { width: { magnitude: w * PT, unit: 'EMU' }, height: { magnitude: h * PT, unit: 'EMU' } }, transform: { scaleX: 1, scaleY: 1, translateX: x * PT, translateY: y * PT, unit: 'EMU' } } },
});
function bgReqs(slide: string, key: string) {
  return [darkBg(slide), img(`r22bg_${key}`, slide, 0, 0, 720, 405, BG_URL), { updatePageElementsZOrder: { pageElementObjectIds: [`r22bg_${key}`], operation: 'SEND_TO_BACK' } }];
}
function tracker(slide: string, key: string, goldPart: string, grayPart: string) {
  const id = `r22trk_${key}`;
  return [box(id, slide, 403.2, 33, 300, 16.5),
    ...segs(id, [[goldPart, st(8, 700, GOLD)], [grayPart + '\n', st(8, 400, TGRAY)]], false),
    { updateParagraphStyle: { objectId: id, textRange: { type: 'ALL' }, style: { alignment: 'END' }, fields: 'alignment' } }];
}
function footer(slide: string, key: string) {
  const id = `r22ftr_${key}`;
  return [box(id, slide, 15.5, 388, 130, 8), ...segs(id, [['© 2026 -  Navier - Private & Confidential\n', st(5, 400, WHITE)]], false)];
}
const logo = (slide: string, key: string) => img(`r22logo_${key}`, slide, 682.5, 376.3, 27.6, 17.4, LOGO_URL);
const title = (slide: string, key: string, parts: [string, any][]) => {
  const id = `r22ttl_${key}`;
  return [box(id, slide, 45.6, 36, 620, 30), ...segs(id, parts, false)];
};
const T = (t: string) => [[t + '\n', st(17, 600, WHITE)]] as [string, any][];

// ============ B1: S2 claim rebuild ============
await batch([
  ...del(['r20img_st_r19_claim', 'g3f6623c186e_4_75', 'st2_title', 'st2_body', 'st2_bandbg', 'st2_band']),
  ...bgReqs('st_r19_claim', 's2'),
  ...title('st_r19_claim', 's2', T('The Ocean Is the Last Transport Network Left to Build')),
  box('r22body_s2', 'st_r19_claim', 45.6, 96, 352, 260),
  ...segs('r22body_s2', [
    ['71% of the planet is water. Most of the world\u2019s great cities sit on it. Yet moving people and goods across it still means slow, diesel, heavily crewed boats \u2014 or no service at all.\n\n', st(10.5, 400, GRAY)],
    ['Roads got cars. The sky got airlines. The water never got its modern transport layer \u2014 because no vessel was fast, clean, and cheap enough to run frequent point-to-point service.\n\n', st(10.5, 400, GRAY)],
    ['Navier builds that vessel \u2014 small, fast, electric, software-driven \u2014 and the network it unlocks.\n', st(11, 700, LGOLD)],
  ], false),
  img('r22plate_s2', 'st_r19_claim', 425, 96, 250, 260, RAW + 's2-plate.jpg'),
  ...tracker('st_r19_claim', 's2', '01', '  \u00b7  THESIS & TEAM'),
  ...footer('st_r19_claim', 's2'), logo('st_r19_claim', 's2'),
], 'B1 S2');

// ============ B2: S3 vision rebuild ============
await batch([
  ...del(['st3_hero', 'st3_scrim', 'st3_title', 'st3_sub']),
  ...bgReqs('st_r19_vision', 's3'),
  ...title('st_r19_vision', 's3', T('The World We\u2019re Building')),
  box('r22body_s3', 'st_r19_vision', 45.6, 96, 352, 260),
  ...segs('r22body_s3', [
    ['Thousands of small, fast, electric vessels running scheduled point-to-point routes along coastlines and between islands \u2014 moving people by day and cargo by night.\n\n', st(10.5, 400, GRAY)],
    ['One platform serving three markets: mobility, logistics, and defense.\n\n', st(10.5, 400, GRAY)],
    ['Every coastline becomes a network \u2014 every marina becomes a Navier hub.\n', st(11, 700, LGOLD)],
  ], false),
  img('r22plate_s3', 'st_r19_vision', 425, 96, 250, 260, RAW + 's3-plate.jpg'),
  ...footer('st_r19_vision', 's3'), logo('st_r19_vision', 's3'),
], 'B2 S3');

// ============ B3: S4 ladder rebuild as five segment cards ============
const CARDS = [
  ['1 \u00b7 RECREATIONAL', 'Validate the technology', 'N30 Pioneer \u2014 sold to early adopters. 10,000+ hours on the water.', 'IN SERVICE'],
  ['2 \u00b7 MOBILITY', 'Build the network', 'Electric water taxis on high-frequency city and resort routes. Maldives: 100 vessels, $100M signed.', 'SIGNED \u2014 $100M'],
  ['3 \u00b7 LONG RANGE', 'Extend the reach', 'Quanta \u2014 hybrid power, ~2,000 NMi at 20 kts. Coastal hops become intercity corridors.', 'IN SEA TRIALS'],
  ['4 \u00b7 CARGO', 'Fill the night shift', 'The same boats and routes carry urgent freight overnight. First corridor targeted 2027.', 'NEXT \u2014 2027'],
  ['5 \u00b7 DEFENSE', 'Serve strategic missions', 'The proven commercial platform, hardened for patrol, resupply, and ISR.', 'GROUNDWORK \u2014 U.S. NAVY'],
];
function card(i: number): any[] {
  const x = 45.6 + i * 128.5, y = 96, w = 118, h = 234;
  const [label, role, desc, status] = CARDS[i];
  const k = `c${i}`;
  return [
    ...rect(`r22cbg_${k}`, 'st_r19_ladder', x, y, w, h, CARD, 0.94),
    ...rect(`r22chl_${k}`, 'st_r19_ladder', x, y, w, 1.5, GOLD, 1),
    box(`r22clb_${k}`, 'st_r19_ladder', x + 10, y + 12, w - 20, 14),
    ...segs(`r22clb_${k}`, [[label + '\n', st(7.5, 700, GOLD)]], false),
    box(`r22crl_${k}`, 'st_r19_ladder', x + 10, y + 30, w - 20, 34),
    ...segs(`r22crl_${k}`, [[role + '\n', st(10.5, 600, WHITE)]], false),
    box(`r22cds_${k}`, 'st_r19_ladder', x + 10, y + 70, w - 20, 120),
    ...segs(`r22cds_${k}`, [[desc + '\n', st(8, 400, GRAY)]], false),
    ...rect(`r22csb_${k}`, 'st_r19_ladder', x, y + h - 22, w, 22, GOLD, 0.16),
    box(`r22cst_${k}`, 'st_r19_ladder', x + 4, y + h - 19, w - 8, 14),
    ...segs(`r22cst_${k}`, [[status + '\n', st(6.5, 700, LGOLD)]], false),
    { updateParagraphStyle: { objectId: `r22cst_${k}`, textRange: { type: 'ALL' }, style: { alignment: 'CENTER' }, fields: 'alignment' } },
  ];
}
await batch([
  ...del(['r20img_st_r19_ladder', 'r20scrim_st_r19_ladder', 'st4_title', 'st4_r1bg', 'st4_r1', 'st4_r2bg', 'st4_r2', 'st4_r3bg', 'st4_r3', 'st4_r4bg', 'st4_r4', 'st4_r5bg', 'st4_r5', 'st4_here', 'st4_kick', 'st4_lgbg', 'st4_lg']),
  ...bgReqs('st_r19_ladder', 's4'),
  ...title('st_r19_ladder', 's4', T('We Build in Stages \u2014 Each Market Funds the Next')),
  ...card(0), ...card(1), ...card(2),
], 'B3a S4');
await batch([
  ...card(3), ...card(4),
  box('r22kick_s4', 'st_r19_ladder', 45.6, 342, 630, 18),
  ...segs('r22kick_s4', [
    ['Every stage is a real business that funds and de-risks the next \u2014 ', st(10, 400, GRAY)],
    ['the first two are already earning.\n', st(10, 700, LGOLD)],
  ], false),
  box('r22strip_s4', 'st_r19_ladder', 45.6, 364, 630, 14),
  ...segs('r22strip_s4', [['Designed for U.S. defense supply chains \u00b7 Electric first, hybrid where range demands it \u00b7 Crewed today, autonomy-ready by design\n', st(7, 400, DIM)]], false),
  ...footer('st_r19_ladder', 's4'), logo('st_r19_ladder', 's4'),
], 'B3b S4');

// ============ B4: S5 graveyard reskin ============
await batch([
  ...del(['r20img_sb_c3_grave', 'r20scrim_sb_c3_grave']),
  ...bgReqs('sb_c3_grave', 's5'),
  ...segs('c3_title', T('It\u2019s Been Tried. The Sequence Was Wrong.')),
  ...tracker('sb_c3_grave', 's5', '01', '  \u00b7  THESIS & TEAM'),
  ...footer('sb_c3_grave', 's5'), logo('sb_c3_grave', 's5'),
], 'B4 S5');

// ============ B5: S24 C1 gap reskin ============
await batch([
  ...del(['r20img_sb_c1_gap', 'r20scrim_sb_c1_gap', 'c1_eye', 'c1_bridge']),
  ...bgReqs('sb_c1_gap', 'c1'),
  ...segs('c1_title', T('Cargo \u2014 The Gap Between Air and Ocean')),
  box('r22lede_c1', 'sb_c1_gap', 45.6, 70, 620, 16),
  ...segs('r22lede_c1', [
    ['Passenger networks run 16 hours a day \u2014 then sleep. ', st(10, 400, GRAY)],
    ['Cargo is the night shift.\n', st(10, 700, LGOLD)],
  ], false),
  ...tracker('sb_c1_gap', 'c1', 'THE SECOND ACT', '  \u2014  CARGO'),
  ...footer('sb_c1_gap', 'c1'), logo('sb_c1_gap', 'c1'),
], 'B5 C1');

// ============ B6: S25 rebuild as C2 day/night ============
await batch([
  ...del(['g3f6623c186e_4_79', 'g3f6623c186e_4_80', 'g3f6623c186e_4_81', 'g3f6623c186e_4_82', 'g3f6623c186e_4_83', 'g3f6623c186e_4_84', 'g3f6623c186e_4_85', 'g3f6623c186e_4_86', 'g3f6623c186e_4_87', 'g3f6623c186e_4_88', 'g3f6623c186e_4_89', 'g3f6623c186e_4_90', 'g3f6623c186e_4_91', 'g3f6623c186e_4_92']),
  ...bgReqs('g3f6623c186e_4_78', 'c2'),
  ...title('g3f6623c186e_4_78', 'c2', T('People by Day. Cargo by Night.')),
  box('r22lede_c2', 'g3f6623c186e_4_78', 45.6, 70, 620, 30),
  ...segs('r22lede_c2', [
    ['The same hull earns twice \u2014 same corridors, same chargers, same software, no added capex. ', st(10, 400, GRAY)],
    ['Night hours are idle today; a modular hold turns them into freight revenue.\n', st(10, 700, LGOLD)],
  ], false),
  img('r22plate_c2', 'g3f6623c186e_4_78', 45.6, 112, 420, 238, RAW + 'c2-plate.jpg'),
  ...rect('r22tagbg_c2', 'g3f6623c186e_4_78', 375, 118, 84, 14, { red: 0.03, green: 0.045, blue: 0.065 }, 0.85),
  box('r22tag_c2', 'g3f6623c186e_4_78', 377, 119.5, 80, 11),
  ...segs('r22tag_c2', [['CONCEPT RENDER\n', st(6, 600, DIM)]], false),
  { updateParagraphStyle: { objectId: 'r22tag_c2', textRange: { type: 'ALL' }, style: { alignment: 'CENTER' }, fields: 'alignment' } },
  ...rect('r22k1bg_c2', 'g3f6623c186e_4_78', 480, 112, 195, 70, CARD, 0.94),
  box('r22k1_c2', 'g3f6623c186e_4_78', 492, 122, 172, 52),
  ...segs('r22k1_c2', [['SAME VESSEL\n', st(8, 700, GOLD)], ['Modular hold \u2014 concept in design; no added capex on the hull.\n', st(8.5, 400, GRAY)]], false),
  ...rect('r22k2bg_c2', 'g3f6623c186e_4_78', 480, 196, 195, 70, CARD, 0.94),
  box('r22k2_c2', 'g3f6623c186e_4_78', 492, 206, 172, 52),
  ...segs('r22k2_c2', [['SAME NETWORK\n', st(8, 700, GOLD)], ['Piers, charging, and software already built and paid for by passengers.\n', st(8.5, 400, GRAY)]], false),
  ...rect('r22k3bg_c2', 'g3f6623c186e_4_78', 480, 280, 195, 70, CARD, 0.94),
  box('r22k3_c2', 'g3f6623c186e_4_78', 492, 290, 172, 52),
  ...segs('r22k3_c2', [['NEW REVENUE\n', st(8, 700, GOLD)], ['Freight rides on marginal cost \u2014 energy and handling only.\n', st(8.5, 400, GRAY)]], false),
  ...tracker('g3f6623c186e_4_78', 'c2', 'THE SECOND ACT', '  \u2014  CARGO'),
  ...footer('g3f6623c186e_4_78', 'c2'), logo('g3f6623c186e_4_78', 'c2'),
], 'B6 C2');

// ============ B7: S26 C5 prize reskin ============
await batch([
  ...del(['r20img_sb_c5_prize', 'r20scrim_sb_c5_prize', 'c5_eye']),
  ...bgReqs('sb_c5_prize', 'c5'),
  ...segs('c5_title', T('Islands Pay the Most for the Slowest Service')),
  ...tracker('sb_c5_prize', 'c5', 'THE SECOND ACT', '  \u2014  CARGO'),
  ...footer('sb_c5_prize', 'c5'), logo('sb_c5_prize', 'c5'),
], 'B7 C5');

// ============ B8: chrome pass on 30/31/34/40/39/36/33/35/37/38/29 ============
await batch([
  // 30 close
  ...segs('r21_wiw_title', T('The World Is Watching')),
  ...tracker('r21_wiw', 'wiw', '05', '  \u00b7  FINANCIALS & THE ASK'),
  logo('r21_wiw', 'wiw'),
  // 31 ask
  ...segs('sta_title', [['$10M Series B-1', st(17, 600, WHITE)], [' \u2014 First Close of ', st(17, 600, WHITE)], ['$100\u2013150M Series B\n', st(17, 700, LGOLD)]]),
  ...tracker('st_r19_ask', 'ask', '05', '  \u00b7  FINANCIALS & THE ASK'),
  ...footer('st_r19_ask', 'ask'), logo('st_r19_ask', 'ask'),
  // 34 cargo econ appendix
  ...del(['a1_eye']),
  ...segs('a1_title', T('Night Cargo \u2014 Parametric Economics')),
  ...tracker('sb_cargo_econ', 'a1', 'APPENDIX', '  \u00b7  ILLUSTRATIVE'),
  ...footer('sb_cargo_econ', 'a1'), logo('sb_cargo_econ', 'a1'),
  // 40 navy validation
  ...del(['r21_46eye']),
  ...tracker('g3f556ac5e67_1_798', 'a40', 'APPENDIX', '  \u00b7  DEFENSE VALIDATION'),
  ...footer('g3f556ac5e67_1_798', 'a40'), logo('g3f556ac5e67_1_798', 'a40'),
  // 39 TRL/MRL
  ...del(['r21_44eye']),
  ...tracker('g3f556ac5e67_1_714', 'a39', 'APPENDIX', '  \u00b7  TECHNOLOGY MATURITY'),
  // 36 opportunity — stale 02 tracker → APPENDIX
  ...segs('g3f9515af747_0_117', [['APPENDIX', st(8, 700, GOLD)], ['  \u00b7  MARKET SIZING\n', st(8, 400, TGRAY)]]),
  // 33 premium econ
  ...tracker('sb_premium', 'a33', 'APPENDIX', '  \u00b7  UNIT ECONOMICS'),
  logo('sb_premium', 'a33'),
  // 35 competitive field
  ...tracker('g3f6623c186e_4_1', 'a35', 'APPENDIX', '  \u00b7  COMPETITIVE FIELD'),
  // 37/38 production
  ...tracker('sb_prod_scale', 'a37', 'APPENDIX', '  \u00b7  PRODUCTION'),
  logo('sb_prod_scale', 'a37'),
  ...tracker('sb_prod_cost', 'a38', 'APPENDIX', '  \u00b7  PRODUCTION'),
  logo('sb_prod_cost', 'a38'),
  // 29 roadmap logo
  logo('sb_roadmap', 'a29'),
], 'B8 chrome');

console.log('R22 build complete');
