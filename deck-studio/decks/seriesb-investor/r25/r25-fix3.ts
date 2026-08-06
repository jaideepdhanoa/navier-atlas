import { invokeTool } from '@tasklet/tools/v2';
import { batch, segs, st, PRES, LGOLD, GRAY, DIM } from '/tasklet/agent/home/scripts/seriesb-rebuild/h.ts';
const CONN = 'conn_9qpjytrfnwhbgs2sd9cf';

// 1. revert source-line append (it wrapped into the footer)
const g = await invokeTool({ connectionId: CONN, toolName: 'google_slides_get_presentation', args: { presentationId: PRES, mode: 'slides', slideIndices: [42] } });
const d = await g.json();
let txt = '';
function walk(list: any[]) { for (const e of (list || [])) { if (e.elementGroup) { walk(e.elementGroup.children); continue; } if (e.objectId === 'g3f6623c186e_4_153') txt = (e.shape?.text?.textElements || []).map((x: any) => x.textRun?.content || '').join(''); } }
walk(d.slides[0].pageElements);
const ins = ' \u00b7 U.S. Navy records / Int\u2019l Hydrofoil Society (USS Plainview, 1969)';
const i = txt.indexOf(ins);
if (i < 0) { console.log('inserted text not found — already reverted?'); } else {
  await batch([{ deleteText: { objectId: 'g3f6623c186e_4_153', textRange: { type: 'FIXED_RANGE', startIndex: i, endIndex: i + ins.length } } }], 'S42 revert source append');
}

// 2. band rewrite with in-band source line
await batch([
  ...segs('r25pv_txt', [
    ['THE PHYSICS WAS PROVEN IN 1969 — WHAT WAS MISSING WAS CONTROL\n', st(8.5, 800, LGOLD)],
    ['USS Plainview (AGEH-1): the U.S. Navy\u2019s 212-ft, 310-ton hydrofoil flew at 40 knots on jet-derived turbines. Lift at scale was never the blocker — affordable control was. Control is software now, and Navier owns that layer.\n', st(8.5, 400, GRAY)],
    ['Source: U.S. Navy records \u00b7 International Hydrofoil Society \u00b7 sourced Aug 2026.', st(6.5, 400, DIM)],
  ], true),
], 'S42 band + in-band source');
