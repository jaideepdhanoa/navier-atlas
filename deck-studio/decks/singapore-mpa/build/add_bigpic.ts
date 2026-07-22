// Bigger-picture arc — 3 slides into chapter 03 after "WHAT A SMALL LAYER ADDS"
import { batch, segs, box, st, gline, rect, darkBg, GOLD, LGOLD, GRAY, WHITE, PT } from './h.ts';
const PLATE = 'https://raw.githubusercontent.com/jaideepdhanoa/navier-atlas/9d6c0b0c99695ebead35b73aadf34dd4109495a8/deck-studio/assets/singapore-mpa/sg-coastal-express.png';
const FOOT = { red: 0.62, green: 0.65, blue: 0.68 };
const tracker = (id: string, sid: string) => [
  box(id, sid, 538, 44, 400, 22),
  ...segs(id, [['03  ·  THE SINGAPORE OPPORTUNITY\n', st(10, 700, LGOLD, { bold: true })]], false),
];
const src = (id: string, sid: string, text: string) => [
  box(id, sid, 55, 506, 760, 20),
  ...segs(id, [[text + '\n', st(7.5, 400, FOOT)]], false),
];

const R: any[] = [];

// ---------- SLIDE A · sg_bigpic_12 · A TRANSIT LINE WITHOUT LAND ----------
const A = 'sg_bigpic_12';
R.push({ createSlide: { objectId: A, insertionIndex: 11, slideLayoutReference: { predefinedLayout: 'BLANK' } } });
R.push(darkBg(A));
R.push(box('bp_hd', A, 61, 48, 640, 28));
R.push(...segs('bp_hd', [['A TRANSIT LINE WITHOUT LAND\n', st(23, 600, WHITE)]], false));
R.push(...gline('bp_rule', A, 61, 91, 80));
R.push(...tracker('bp_trk', A));
R.push(box('bp_sub', A, 61, 102, 840, 26));
R.push(...segs('bp_sub', [['Every new land corridor is bought with land, money and years of construction. The water is already there.\n', st(15, 400, GRAY)]], false));
// three stat cards
const cards: [string, string, string][] = [
  ['12%', 'of Singapore\u2019s land is already roads \u2014 about as much as all housing.', 'bp_c1'],
  ['S$25B', 'the cost of the newest rail line, the Thomson\u2013East Coast Line.', 'bp_c2'],
  ['360 km', 'the rail network target by the early 2030s \u2014 built underground, km by km.', 'bp_c3'],
];
cards.forEach(([num, cap, id], i) => {
  const x = 61 + i * 293;
  R.push(...rect(id + '_bg', A, x, 158, 273, 150, { red: 0.09, green: 0.115, blue: 0.15 }, 1));
  R.push(...rect(id + '_tick', A, x, 158, 273, 3, GOLD, 1));
  R.push(box(id + '_n', A, x + 18, 176, 237, 44));
  R.push(...segs(id + '_n', [[num + '\n', st(30, 800, GOLD, { bold: true })]], false));
  R.push(box(id + '_t', A, x + 18, 226, 237, 74));
  R.push(...segs(id + '_t', [[cap + '\n', st(11.5, 400, GRAY)]], false));
});
// body
R.push(box('bp_body', A, 61, 330, 840, 100));
R.push(...segs('bp_body', [
  ['The waterway is a right-of-way that already exists', st(15, 700, WHITE, { bold: true })],
  [' \u2014 wrapping the island from Changi to the west coast, reaching the door of the CBD. No tunnelling, no land acquisition, no years of construction. Electric, quiet and with near-zero wake, the same clean harbour craft that serve the islands can carry commuters at the peaks.\n', st(15, 400, GRAY)],
], false));
// bottom band
R.push(...rect('bp_band', A, 0, 456, 960, 65, { red: 0.09, green: 0.115, blue: 0.15 }, 1));
R.push(box('bp_bandtx', A, 61, 462, 860, 52));
R.push(...segs('bp_bandtx', [
  ['THE BIGGER PICTURE\n', st(9.5, 600, LGOLD)],
  ['ZERO LAND TAKE', st(13.5, 700, WHITE, { bold: true })],
  ['   ·   ', st(13.5, 700, GOLD, { bold: true })],
  ['NO TUNNELLING', st(13.5, 700, WHITE, { bold: true })],
  ['   ·   ', st(13.5, 700, GOLD, { bold: true })],
  ['SERVICE IN MONTHS, NOT DECADES\n', st(13.5, 700, WHITE, { bold: true })],
], false));
R.push(...src('bp_src', A, 'Sources: LTA (roads \u224812% of total land area; rail expansion to ~360 km by the early 2030s) \u00b7 CNA / LTA (Thomson\u2013East Coast Line \u2248 S$25 billion)'));

// ---------- SLIDE B · sg_coastal_13 · THE COASTAL LINE (map) ----------
const B = 'sg_coastal_13';
R.push({ createSlide: { objectId: B, insertionIndex: 12, slideLayoutReference: { predefinedLayout: 'BLANK' } } });
R.push(darkBg(B));
R.push({ createImage: { objectId: 'cl_map', url: PLATE, elementProperties: {
  pageObjectId: B,
  size: { width: { magnitude: 960 * PT, unit: 'EMU' }, height: { magnitude: 540 * PT, unit: 'EMU' } },
  transform: { scaleX: 1, scaleY: 1, translateX: 0, translateY: 0, unit: 'EMU' },
} } });
R.push(...tracker('cl_trk', B));
// right-bottom panel over open water
R.push(...rect('cl_pnl_bg', B, 636, 330, 290, 150, { red: 0.055, green: 0.075, blue: 0.105 }, 0.88));
R.push(...rect('cl_pnl_tick', B, 636, 330, 3, 150, GOLD, 1));
R.push(box('cl_pnl', B, 652, 342, 262, 130));
R.push(...segs('cl_pnl', [
  ['FIVE STOPS, ONE RIGHT-OF-WAY\n', st(12, 800, GOLD, { bold: true })],
  ['\n', st(5, 400, GRAY)],
  ['Commuters at the peaks \u2014 islands and the waterfront the rest of the day. Same boats, same charging points, one network.\n', st(11, 400, GRAY)],
  ['\n', st(5, 400, GRAY)],
  ['Starts with two boats. Grows stop by stop.\n', st(11, 700, WHITE, { bold: true })],
], false));
R.push(...src('cl_src', B, 'Sources: Navier network study \u2014 corridor illustrative, anchors at existing piers \u00b7 alignment and stops pending joint study with MPA'));

// ---------- SLIDE C · sg_agencies_14 · ONE WATERWAY, TWO MANDATES ----------
const C = 'sg_agencies_14';
R.push({ createSlide: { objectId: C, insertionIndex: 13, slideLayoutReference: { predefinedLayout: 'BLANK' } } });
R.push(darkBg(C));
R.push(box('ag_hd', C, 61, 48, 640, 28));
R.push(...segs('ag_hd', [['ONE WATERWAY, TWO MANDATES\n', st(23, 600, WHITE)]], false));
R.push(...gline('ag_rule', C, 61, 91, 80));
R.push(...tracker('ag_trk', C));
R.push(box('ag_sub', C, 61, 102, 840, 26));
R.push(...segs('ag_sub', [['The coastal line serves two public agendas at once \u2014 and it starts inside yours.\n', st(15, 400, GRAY)]], false));
// left column — MPA
R.push(box('ag_lh', C, 61, 152, 380, 24));
R.push(...segs('ag_lh', [['MPA \u2014 THE FRONT DOOR\n', st(13, 800, GOLD, { bold: true })]], false));
R.push(...gline('ag_lul', C, 61, 180, 48));
R.push(box('ag_lb', C, 61, 192, 400, 230));
R.push(...segs('ag_lb', [
  ['\u203a  ', st(12, 800, GOLD, { bold: true })], ['Regulates every vessel on Singapore water\n', st(12, 400, GRAY)],
  ['\n', st(6, 400, GRAY)],
  ['\u203a  ', st(12, 800, GOLD, { bold: true })], ['Wrote the 2030 clean harbour-craft rule\n', st(12, 400, GRAY)],
  ['\n', st(6, 400, GRAY)],
  ['\u203a  ', st(12, 800, GOLD, { bold: true })], ['Published the charging standard (TR 136) \u2014 first point already live at Marina South Pier\n', st(12, 400, GRAY)],
  ['\n', st(6, 400, GRAY)],
  ['\u203a  ', st(12, 800, GOLD, { bold: true })], ['Funds the transition \u2014 MINT co-funding, green-port incentives\n', st(12, 400, GRAY)],
  ['\n', st(8, 400, GRAY)],
  ['This proposal starts, and stays, inside MPA\u2019s mandate.\n', st(10.5, 400, FOOT)],
], false));
// divider
R.push(...rect('ag_dv', C, 490, 152, 1.4, 268, GOLD, 0.55));
// right column — LTA
R.push(box('ag_rh', C, 521, 152, 400, 24));
R.push(...segs('ag_rh', [['LTA \u2014 THE BENEFICIARY\n', st(13, 800, GOLD, { bold: true })]], false));
R.push(...gline('ag_rul', C, 521, 180, 48));
R.push(box('ag_rb', C, 521, 192, 400, 230));
R.push(...segs('ag_rb', [
  ['\u203a  ', st(12, 800, GOLD, { bold: true })], ['Its 2040 plan targets a 45-minute city and 20-minute towns\n', st(12, 400, GRAY)],
  ['\n', st(6, 400, GRAY)],
  ['\u203a  ', st(12, 800, GOLD, { bold: true })], ['Roads already take 12% of the island\u2019s land \u2014 every new corridor competes for space\n', st(12, 400, GRAY)],
  ['\n', st(6, 400, GRAY)],
  ['\u203a  ', st(12, 800, GOLD, { bold: true })], ['The coastal line adds peak capacity toward those targets with zero land take\n', st(12, 400, GRAY)],
  ['\n', st(8, 400, GRAY)],
  ['When the pilot has data, the commuter case reaches LTA already proven.\n', st(10.5, 400, FOOT)],
], false));
// bottom band
R.push(...rect('ag_band', C, 0, 456, 960, 65, { red: 0.09, green: 0.115, blue: 0.15 }, 1));
R.push(box('ag_bandtx', C, 61, 462, 880, 52));
R.push(...segs('ag_bandtx', [
  ['THE SEQUENCE\n', st(9.5, 600, LGOLD)],
  ['START INSIDE MPA\u2019S MANDATE', st(13.5, 700, WHITE, { bold: true })],
  ['   ·   ', st(13.5, 700, GOLD, { bold: true })],
  ['PROVE IT ON THE WATER', st(13.5, 700, WHITE, { bold: true })],
  ['   ·   ', st(13.5, 700, GOLD, { bold: true })],
  ['BRING LTA IN WITH DATA\n', st(13.5, 700, WHITE, { bold: true })],
], false));
R.push(...src('ag_src', C, 'Sources: LTA Land Transport Master Plan 2040 \u00b7 LTA / MOT (road land share) \u00b7 MPA (2030 harbour-craft rule, TR 136, MINT Fund, Maritime Singapore Green Initiative)'));

await batch(R, 'bigger-picture arc');
console.log('BIGPIC DONE');
