// R25 — LC-180 storyline transfer (Jaideep Aug-6 round 3). Six items:
// 1 two-mode cargo logic (S23) · 2 infrastructure bypass (S23) · 3 mission economics (S35)
// 4 "hardest technology is control" (S10) · 5 USS Plainview precedent (S42) · 6 GMVP schedule-risk line (S11)
// Firewall: no LC-180 name, specs, program costs, fleet size, or AD Ports anywhere.
import { invokeTool } from '@tasklet/tools/v2';
import { batch, segs, st, box, rect, PRES, GOLD, LGOLD, GRAY, WHITE } from '/tasklet/agent/home/scripts/seriesb-rebuild/h.ts';

const CONN = 'conn_9qpjytrfnwhbgs2sd9cf';
const NAVY = { red: 0.039, green: 0.071, blue: 0.125 };

// ---- helper: fetch full text of an element (for insert-inherit edits) ----
async function elementText(slideIndex: number, objectId: string): Promise<string> {
  const g = await invokeTool({ connectionId: CONN, toolName: 'google_slides_get_presentation', args: { presentationId: PRES, mode: 'slides', slideIndices: [slideIndex] } });
  if (!g.ok) { console.log('FETCH FAIL', objectId, g.error); process.exit(1); }
  const d = await g.json();
  let found = '';
  function walk(list: any[]) {
    for (const e of (list || [])) {
      if (e.elementGroup) { walk(e.elementGroup.children); continue; }
      if (e.objectId === objectId) found = (e.shape?.text?.textElements || []).map((x: any) => x.textRun?.content || '').join('');
    }
  }
  walk(d.slides[0].pageElements);
  return found;
}

// ============ Item 4 — S10: control is the hardest technology ============
await batch([
  ...segs('g3f9515af747_0_233', [
    ['The Hardest Technology Is Control — and Navier Owns It\n', st(17, 600, WHITE)],
  ], true),
  ...segs('g3f9515af747_0_225', [
    ['NavierOS — The Brain\n', st(11, 400, GOLD)],
    ['Flight stabilization & autonomy\n', st(11, 400, WHITE)],
    ['Sense → estimate → act, many times a second\n', st(11, 400, WHITE)],
  ], true),
], 'S10 control title + NavierOS callout');

// ============ Item 6 — S11: GMVP schedule-risk line (insert-inherit) ============
{
  const t = await elementText(11, 'g3f97ee12203_2_11');
  const anchor = 'the R&D tax of traditional shipbuilding';
  const i = t.indexOf(anchor);
  if (i < 0) { console.log('S11 anchor not found — ABORT item 6'); process.exit(1); }
  await batch([
    { insertText: { objectId: 'g3f97ee12203_2_11', insertionIndex: i + anchor.length, text: ' — each new class reuses the validated core, cutting engineering time and schedule risk' } },
  ], 'S11 GMVP schedule-risk');
}

// ============ Items 1+2 — S23: two modes + any shore ============
await batch([
  ...segs('r24ch_k1', [
    ['TWO MODES\n', st(8, 700, GOLD)],
    ['Designed in two modes: urgent freight flies full-foil; heavy loads ride foil-assist, the foils carrying part of the weight to cut power.\n', st(8.5, 400, GRAY)],
  ], true),
  ...segs('r24ch_k2', [
    ['ANY SHORE\n', st(8, 700, GOLD)],
    ['Designed for drive-on, drive-off at any hard ramp — no cranes, no container terminal. Every jetty becomes a port.\n', st(8.5, 400, GRAY)],
  ], true),
], 'S23 two-mode + any-shore kickers');

// ============ Item 3 — S35: mission economics framing ============
await batch([
  ...segs('a1_par', [
    ['Measured the operator\u2019s way — missions per vessel-day and cost per kilogram, not brochure speed. ', st(11, 800, GOLD)],
    ['N45-class night shift · payload 1–2 t · 2–4 night legs · $0.75–1.50/kg (air $2.50–4.50, ocean $0.03–0.50) · 300 nights/yr.', st(11, 400, GRAY)],
  ], true),
  ...segs('a1_cost', [
    ['Incremental cost is energy and handling only — ', st(11, 400, WHITE)],
    ['hull, berth, insurance, and software are already carried by the day business. ', st(11, 700, LGOLD)],
    ['The test: more completed missions per vessel-day at lower cost per kilogram.', st(11, 400, WHITE)],
  ], true),
], 'S35 mission economics');

// ============ Item 5 — S42: USS Plainview precedent band ============
await batch([
  ...rect('r25pv_bg', 'g3f6623c186e_4_145', 40, 322, 640, 48, NAVY, 1),
  box('r25pv_txt', 'g3f6623c186e_4_145', 52, 326, 616, 42),
  ...segs('r25pv_txt', [
    ['THE PHYSICS WAS PROVEN IN 1969 — WHAT WAS MISSING WAS CONTROL\n', st(8.5, 800, LGOLD)],
    ['USS Plainview (AGEH-1): the U.S. Navy\u2019s 212-ft, 310-ton hydrofoil flew at 40 knots on jet-derived turbines. Lift at scale was never the blocker — affordable control was. Control is software now, and Navier owns that layer.', st(8.5, 400, GRAY)],
  ], false),
], 'S42 Plainview band');

// source-line append (insert-inherit)
{
  const t = await elementText(42, 'g3f6623c186e_4_153');
  const anchor = 'CB Insights';
  const i = t.indexOf(anchor);
  if (i < 0) { console.log('S42 source anchor not found — ABORT'); process.exit(1); }
  await batch([
    { insertText: { objectId: 'g3f6623c186e_4_153', insertionIndex: i + anchor.length, text: ' · U.S. Navy records / Int\u2019l Hydrofoil Society (USS Plainview, 1969)' } },
  ], 'S42 source line');
}

console.log('R25 build complete');
