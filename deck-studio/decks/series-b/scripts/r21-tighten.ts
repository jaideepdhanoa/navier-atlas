// R21 — Tighten + visual quality pass (Jaideep "do it" 2026-08-05)
// Cuts 12 slides (51→39), merges 7→8 and 45→46, rethemes 44/46 dark, micro-fixes.
import { batch, segs, st, box, rect, gline, darkBg, GOLD, LGOLD, GRAY, WHITE, DIM, PT } from '/tasklet/agent/home/scripts/seriesb-rebuild/h.ts';

const NAVY = { red: 0.09, green: 0.114, blue: 0.149 };   // card #171D26
const CARD = { red: 0.09, green: 0.114, blue: 0.149 };

// ---------- Batch A: text edits + bg normalization ----------
const A: any[] = [];

// bg normalize to deck navy
for (const s of ['g3f9515af747_0_0', 'g3f645480738_0_79', 'g3f93a1213f6_0_403', 'g3f556ac5e67_1_539', 'g3f556ac5e67_1_714', 'g3f556ac5e67_1_798']) A.push(darkBg(s));

// p2 body trim (one line shorter, bolded closer)
A.push(...segs('st2_body', [
  ['Data got packet switching. Goods got the container. The sky got hub-and-spoke aviation.\n\n', st(15, 700, WHITE, { bold: true })],
  ['The ocean — 71% of the planet, touching nearly every major city — never got its network. It moves in monoliths: big, slow, crewed, expensive — and the seas the monoliths leave dark are now contested. The missing layer is a national-security gap too.\n\n', st(13, 400, GRAY)],
  ['The unlock is the node: a small, fast, electric, autonomous vessel cheap enough to deploy by the hundred. ', st(13, 400, GRAY)],
  ['Networks are built from nodes — and no one else has one in service.', st(13, 700, WHITE, { bold: true })],
]));

// p8 merge: absorb slide 7 (costs + why-now)
A.push({ replaceAllText: { containsText: { text: 'Three Levers That Collapse All Three Costs', matchCase: true }, replaceText: 'Three Costs Kept Maritime Stuck. Three Levers Collapse Them.' } });
A.push(...segs('tc_lede', [
  ['A $1T industry moves ~90% of global trade on technology that hasn\u2019t fundamentally changed — vessels ', st(10, 400, GRAY)],
  ['expensive to build', st(10, 700, LGOLD, { bold: true })],
  [' (no shared platform), ', st(10, 400, GRAY)],
  ['expensive to move', st(10, 700, LGOLD, { bold: true })],
  [' (the 800\u00d7 speed penalty), ', st(10, 400, GRAY)],
  ['expensive to operate', st(10, 700, LGOLD, { bold: true })],
  [' (crew-heavy by design).', st(10, 400, GRAY)],
]));
A.push(...segs('tc_cta', [
  ['Speed and cost — no longer a trade-off. ', st(10, 700, LGOLD, { bold: true })],
  ['The window is open: idle waterways · coastal security back on the agenda · U.S. shipbuilding constrained.', st(10, 400, WHITE)],
]));

// p10: kill pre-definition GMVP jargon
A.push(...segs('g3f645480738_0_97', [
  ['2026\n', st(10, 600, GOLD)],
  ['Quanta prototype in sea trials. Expanding to Maldives + Cambodia; pipeline in UAE, Turkey, Caribbean, French Polynesia, others', st(10, 400, GRAY)],
]));

// p16: banner to one line
A.push(...segs('g3f645480738_0_17', [
  ['A capability the buyer does not have today — commercial fleets fund the platform that delivers it. In sea trials now.', st(9, 700, LGOLD, { bold: true })],
]));

// p20: formula band fixes (SW→software, double space, comma)
A.push(...segs('g3f93a1213f6_0_426', [
  ['Revenue = units delivered \u00d7 ASP   +   installed base \u00d7 recurring (software + maintenance + network share)\n', { weightedFontFamily: { fontFamily: 'Arial', weight: 700 }, fontSize: { magnitude: 13, unit: 'PT' }, foregroundColor: { opaqueColor: { rgbColor: LGOLD } }, bold: true }],
  ['Hardware sells once — software, maintenance, and the network share recur every year, on every vessel.', { weightedFontFamily: { fontFamily: 'Arial', weight: 700 }, fontSize: { magnitude: 12, unit: 'PT' }, foregroundColor: { opaqueColor: { rgbColor: WHITE } }, bold: true }],
]));

// p24: calm the map — scrim behind panels, above map images
A.push(...rect('r21scrim_24', 'g3f97ee12203_5_43', 0, 0, 720, 405, { red: 0.012, green: 0.031, blue: 0.055 }, 0.38));
A.push({ updatePageElementsZOrder: { pageElementObjectIds: ['r21scrim_24'], operation: 'SEND_TO_BACK' } });
A.push({ updatePageElementsZOrder: { pageElementObjectIds: ['g3f97ee12203_5_69'], operation: 'SEND_TO_BACK' } });
A.push({ updatePageElementsZOrder: { pageElementObjectIds: ['g3f97ee12203_5_70'], operation: 'SEND_TO_BACK' } });

// p25: fail-closed — drop unsourced Arc/Saronic comparatives, keep Navier's own sourced ratio
A.push(...segs('pla_cmp', [
  ['CONTRACTED DEMAND PER DOLLAR RAISED — ', st(9, 700, WHITE, { bold: true })],
  ['~$3 of signed demand per $1 raised', st(9, 700, LGOLD, { bold: true })],
  [' ($100M signed network on $33M raised to date).', st(9, 400, GRAY)],
]));

// p6 typos (scoped to slide)
for (const [f, t] of [['Ph.D ,', 'Ph.D,'], ['Ph.D,  Ferrari', 'Ph.D, Ferrari'], ['Naval Officer,  Management', 'Naval Officer, Management']] as [string, string][])
  A.push({ replaceAllText: { containsText: { text: f, matchCase: true }, replaceText: t, pageObjectIds: ['g3f9515af747_0_0'] } });

// ---------- Batch B: p44 TRL/MRL — dark typographic rebuild ----------
const S44 = 'g3f556ac5e67_1_714';
const B: any[] = [];
B.push({ deleteObject: { objectId: 'g3f556ac5e67_1_717' } }, { deleteObject: { objectId: 'g3f556ac5e67_1_718' } }, { deleteObject: { objectId: 'g3f556ac5e67_1_719' } }, { deleteObject: { objectId: 'g3f556ac5e67_1_723' } });
B.push({ updateTextStyle: { objectId: 'g3f556ac5e67_1_720', textRange: { type: 'ALL' }, style: st(17, 600, WHITE), fields: 'weightedFontFamily,fontSize,foregroundColor' } });
B.push({ updateTextStyle: { objectId: 'g3f556ac5e67_1_722', textRange: { type: 'ALL' }, style: { foregroundColor: { opaqueColor: { rgbColor: DIM } } }, fields: 'foregroundColor' } });
B.push(box('r21_44eye', S44, 46, 14, 400, 14));
B.push(...segs('r21_44eye', [['APPENDIX — TECHNOLOGY MATURITY', st(9, 700, GOLD, { bold: true })]], false));

const cols = [
  { x: 45, id: 'a', head: 'N30 PIONEER — THE REFERENCE', sub: 'IN SERVICE · SYSTEM TRL 9', rows: [
    ['Overall system', 'TRL 9 — deployed & operational'],
    ['Active foils', 'TRL 9 — 4,000+ hrs on foils within 10,000+ ops hrs'],
    ['NavierOS', 'TRL 9 — flight control, telemetry, diagnostics'],
    ['All-electric powertrain', 'TRL 9 — validated at sea'],
    ['Manufacturing', 'MRL 9 — pilot production established'],
  ] },
  { x: 272, id: 'b', head: 'QUANTA — HYBRID LONG-RANGE', sub: 'IN SEA TRIALS · SYSTEM TRL 6', rows: [
    ['Overall system', 'TRL 6 — prototype complete, on the water'],
    ['Foil & software core', 'TRL 9 — carried over from the N30 architecture'],
    ['Hybrid-electric powertrain', 'TRL 5 — component validation complete'],
    ['Manufacturing', 'MRL 6 — moving to low-rate initial production'],
  ] },
  { x: 499, id: 'c', head: 'N120 MORPHEUS — MICRO-CARRIER', sub: 'DESIGN PHASE · SYSTEM TRL 4', rows: [
    ['Overall system', 'TRL 4 — analytical & experimental proof of concept'],
    ['Foil architecture', 'TRL 4 — scale-up design on N30 flight data'],
    ['NavierOS kernel', 'TRL 9 — same core intelligence across the fleet'],
    ['Powertrain', 'TRL 3 — high-fidelity design & selection'],
    ['Manufacturing', 'MRL 2/3 — concept & advanced-material study'],
  ] },
];
for (const c of cols) {
  B.push(...rect(`r21_44bar_${c.id}`, S44, c.x, 88, 176, 3, GOLD, 1));
  B.push(...rect(`r21_44bg_${c.id}`, S44, c.x, 91, 176, 252, CARD, 1));
  B.push(box(`r21_44tx_${c.id}`, S44, c.x + 9, 99, 160, 238));
  const parts: [string, any][] = [
    [c.head + '\n', st(10.5, 700, WHITE, { bold: true })],
    [c.sub + '\n\n', st(8, 700, GOLD, { bold: true })],
  ];
  c.rows.forEach((r, i) => {
    parts.push([r[0] + ':  ', st(8, 600, WHITE)]);
    parts.push([r[1] + (i < c.rows.length - 1 ? '\n\n' : ''), st(8, 400, GRAY)]);
  });
  B.push(...segs(`r21_44tx_${c.id}`, parts, false));
}
B.push(...rect('r21_44bandbg', S44, 45, 356, 630, 24, { red: 0.129, green: 0.11, blue: 0.071 }, 1));
B.push(box('r21_44band', S44, 57, 359, 610, 18));
B.push(...segs('r21_44band', [
  ['One TRL-9 software core carries every new hull up the ladder — ', st(9.5, 700, LGOLD, { bold: true })],
  ['each platform inherits the brain; it doesn\u2019t restart.', st(9.5, 400, WHITE)],
], false));

// ---------- Batch C: p46 merged defense-validation slide ----------
const S46 = 'g3f556ac5e67_1_798';
const C: any[] = [];
C.push(...segs('g3f556ac5e67_1_802', [['Trusted by the U.S. Navy. Validated in Leidos Operations.', st(17, 600, WHITE)]]));
C.push(...gline('r21_46rule', S46, 23, 68, 130));
C.push(box('r21_46eye', S46, 23, 14, 400, 14));
C.push(...segs('r21_46eye', [['APPENDIX — DEFENSE VALIDATION', st(9, 700, GOLD, { bold: true })]], false));
C.push(...segs('g3f556ac5e67_1_804', [
  ['\u201CYour team has met all deliverables and provided a product and service that has exceeded all expectations\u2026 the support of the Navier team has been outstanding and has contributed to meeting aggressive programmatic schedules.\u201D\n\n', { weightedFontFamily: { fontFamily: 'Playfair Display', weight: 400 }, fontSize: { magnitude: 13.5, unit: 'PT' }, italic: true, foregroundColor: { opaqueColor: { rgbColor: WHITE } } }],
  ['— LETTER FROM USMI (UNITED STATES MARINE, INC.) · NAVIER\u2019S FIRST DOD WORK, SUPPORTING THE U.S. NAVY', st(8.5, 700, GOLD, { bold: true })],
]));
C.push(box('r21_leidos', S46, 23, 318, 310, 70));
C.push(...segs('r21_leidos', [
  ['Leidos', st(9.5, 700, WHITE, { bold: true })],
  [' — a defense prime spanning advanced maritime systems, autonomy, and national security — now runs Navier technology in its operations. Commercial fleets fund the platform; defense proves it where the standards are highest.', st(9.5, 400, GRAY)],
], false));

// ---------- Batch D: deletions (12 slides) ----------
const DEL = ['g3f93a1213f6_0_177', 'g3f604bf42eb_0_138', 'sb_c4_path', 'g3f606b3ce3e_0_162', 'g3f93a1213f6_0_0', 'g3f93a1213f6_0_252', 'g3f556ac5e67_1_790', 'g3f556ac5e67_1_805', 'g3f97ee12203_5_120', 'g3f94dd1a8d3_0_0', 'sb_sfnetwork', 'g3f646843d3c_0_0'];
const D = DEL.map(id => ({ deleteObject: { objectId: id } }));

await batch(A, 'A text+bg');
await batch(B, 'B p44 rebuild');
await batch(C, 'C p46 merge');
await batch(D, 'D deletions');
console.log('R21 tighten complete — deck should be 39 slides');
