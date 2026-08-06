// R26 — N45 electric bottom-up (Jaideep 2026-08-06): rename N45 hybrid → electric on Maldives
// unit-econ slide, bottom-up energy (285 kWh / 70 nm = 4.07 kWh/nm × 16 nm × $0.20 × 2,400 legs
// = $31.3K/yr), ratio 630/31.3 = 20×, saved $599K. Master stat 8–11× → 11–20× (slides 6 & 15).
import { invokeTool } from '@tasklet/tools/v2';
import { PRES } from '/tasklet/agent/home/scripts/seriesb-rebuild/h.ts';

const S20 = ['sb_unitecon40'];
const rep = (text: string, replaceText: string, pageObjectIds?: string[]) => ({
  replaceAllText: { containsText: { text, matchCase: true }, replaceText, ...(pageObjectIds ? { pageObjectIds } : {}) },
});

const requests = [
  // Slide 20 — panel B goes electric, bottom-up
  rep('N45 — HYBRID', 'N45 — ELECTRIC', S20),
  rep('$78.7K', '$31.3K', S20),
  rep('$248.7K', '$201.3K', S20),
  rep('8× less energy — $448K/yr saved', '20× less energy — $599K/yr saved', S20),
  // Explainer band — plural + why the bigger boat shows the bigger multiple
  rep('Where the multiple comes from', 'Where the multiples come from', S20),
  rep(
    ' — foiling cuts drag ~6×, the electric drivetrain does the rest. Physics, not pricing.',
    ' — foiling cuts drag ~6×, cheap electricity does the rest — and the thirstier the diesel it replaces, the bigger the multiple. Physics, not pricing.',
    S20,
  ),
  // Footnote — add both energy-intensity bases
  rep(
    'diesel $1.50/L (STO Maldives).',
    'diesel $1.50/L (STO Maldives). N30 at 1.6 kWh/nm (114 kWh / 70 nm); N45 modelled at 4.1 kWh/nm — the same energy intensity scaled to the 20-seat hull.',
    S20,
  ),
  // Master stat — slides 6 (pillar) and 15 (moat) in one pass
  rep('8–11× less energy per mile vs diesel', '11–20× less energy per mile vs diesel'),
];

const g = await invokeTool({
  connectionId: 'conn_9qpjytrfnwhbgs2sd9cf',
  toolName: 'google_slides_batch_update_presentation',
  args: { presentationId: PRES, requests },
});
if (!g.ok) { console.log('ERR', g.error); process.exit(1); }
const d: any = await g.json();
const counts = (d.replies ?? []).map((r: any) => r.replaceAllText?.occurrencesChanged ?? 0);
console.log('occurrences per request:', counts.join(','));
// Expected: 1,1,1,1,1,1,1,2
