// R26c — Jaideep 2026-08-06: efficiency row above energy line; reprice electricity $0.20 → $0.30/kWh (STELCO mid-band)
// N30: 1.63 kWh/nm ×16nm ×$0.30 ×2400 = $18.8K · Targa $140.5K → 7× (7.49)
// N45: 4.07 kWh/nm ×16nm ×$0.30 ×2400 = $46.9K · Princess $630.0K → 13× (13.4)
// Totals: A $103.8K vs $183.5K (saved $80K) · B $216.9K vs $697.1K (saved $480K) — "saved" = all-three-lines delta, both panels
import { invokeTool } from '@tasklet/tools/v2';
const PRES = '1g95_1hKvlz8Pfar-fmhoUsONcJyu6-zPPfhvRhPxu4k';
const GOLD = { red: 0.8784314, green: 0.79607844, blue: 0.56078434 };
const WHITE = { red: 0.9529412, green: 0.9529412, blue: 0.9529412 };
const GRAY = { red: 0.827451, green: 0.827451, blue: 0.827451 };

type Style = { bold?: boolean; color?: any };
function box(objectId: string, lines: string[], base: Style, overrides: Record<number, Style>, fontSize = 8.5) {
  const text = lines.join('\n');
  const reqs: any[] = [
    { deleteText: { objectId, textRange: { type: 'ALL' } } },
    { insertText: { objectId, insertionIndex: 0, text } },
    { updateTextStyle: { objectId, textRange: { type: 'ALL' }, style: {
        fontFamily: 'Exo 2', fontSize: { magnitude: fontSize, unit: 'PT' }, bold: base.bold ?? false,
        foregroundColor: { opaqueColor: { rgbColor: base.color } } },
      fields: 'fontFamily,fontSize,bold,foregroundColor' } },
  ];
  let idx = 0;
  lines.forEach((ln, i) => {
    const o = overrides[i];
    if (o) reqs.push({ updateTextStyle: { objectId, textRange: { type: 'FIXED_RANGE', startIndex: idx, endIndex: idx + ln.length }, style: {
      ...(o.bold !== undefined ? { bold: o.bold } : {}),
      ...(o.color ? { foregroundColor: { opaqueColor: { rgbColor: o.color } } } : {}) },
      fields: [o.bold !== undefined ? 'bold' : null, o.color ? 'foregroundColor' : null].filter(Boolean).join(',') } });
    idx += ln.length + 1;
  });
  reqs.push({ updateParagraphStyle: { objectId, textRange: { type: 'ALL' }, style: { lineSpacing: 138 }, fields: 'lineSpacing' } });
  return reqs;
}
function delta(objectId: string, parts: [string, any][]) {
  const text = parts.map(p => p[0]).join('');
  const reqs: any[] = [
    { deleteText: { objectId, textRange: { type: 'ALL' } } },
    { insertText: { objectId, insertionIndex: 0, text } },
    { updateTextStyle: { objectId, textRange: { type: 'ALL' }, style: {
        fontFamily: 'Exo 2', fontSize: { magnitude: 14, unit: 'PT' }, bold: true,
        foregroundColor: { opaqueColor: { rgbColor: WHITE } } },
      fields: 'fontFamily,fontSize,bold,foregroundColor' } },
  ];
  let idx = 0;
  for (const [s, color] of parts) {
    if (color) reqs.push({ updateTextStyle: { objectId, textRange: { type: 'FIXED_RANGE', startIndex: idx, endIndex: idx + s.length }, style: { foregroundColor: { opaqueColor: { rgbColor: color } } }, fields: 'foregroundColor' } });
    idx += s.length;
  }
  return reqs;
}

const labels = ['Energy use per mile', 'Energy or fuel', 'Maintenance & servicing', 'Navier software', 'All three lines, total'];
const requests: any[] = [
  // Panel A — 30-ft class
  ...box('u5_pa_c0', labels, { color: GRAY }, { 4: { bold: true, color: WHITE } }),
  ...box('u5_pa_c1', ['1.6 kWh/nm', '$18.8K', '$25.0K', '$60.0K', '$103.8K'], { color: WHITE }, { 0: { color: GRAY }, 4: { bold: true, color: GOLD } }),
  ...box('u5_pa_c2', ['2.4 L/nm', '$140.5K', '$43.0K', '—', '$183.5K'], { color: WHITE }, { 0: { color: GRAY }, 4: { bold: true } }),
  // Panel B — 45–55 ft class
  ...box('u5_pb_c0', labels, { color: GRAY }, { 4: { bold: true, color: WHITE } }),
  ...box('u5_pb_c1', ['4.1 kWh/nm', '$46.9K', '$50.0K', '$120.0K', '$216.9K'], { color: WHITE }, { 0: { color: GRAY }, 4: { bold: true, color: GOLD } }),
  ...box('u5_pb_c2', ['10.9 L/nm', '$630.0K', '$67.1K', '—', '$697.1K'], { color: WHITE }, { 0: { color: GRAY }, 4: { bold: true } }),
  // Delta strips — "saved" = all-three-lines delta on both panels now
  ...delta('u5_pa_delta', [['7×', GOLD], [' less energy — ', null], ['$80K/yr saved', GOLD]]),
  ...delta('u5_pb_delta', [['13×', GOLD], [' less energy — ', null], ['$480K/yr saved', GOLD]]),
  // Footnote — mid-band tariff + both diesel burn bases
  { deleteText: { objectId: 'u5_foot', textRange: { type: 'ALL' } } },
  { insertText: { objectId: 'u5_foot', insertionIndex: 0, text: 'Energy priced in-market: electricity $0.30/kWh (mid of STELCO Maldives commercial band $0.21–$0.43) · diesel $1.50/L (STO Maldives). N30 at 1.6 kWh/nm (114 kWh / 70 nm); N45 modelled at 4.1 kWh/nm — the same energy intensity scaled to the 20-seat hull. Targa 32 at 2.4 L/nm (dealer sea trial, 25 kn); Princess 55 at ~10.9 L/nm (measured burn).' } },
  { updateTextStyle: { objectId: 'u5_foot', textRange: { type: 'ALL' }, style: { fontFamily: 'Exo 2', fontSize: { magnitude: 6.3, unit: 'PT' }, bold: false, foregroundColor: { opaqueColor: { rgbColor: GRAY } } }, fields: 'fontFamily,fontSize,bold,foregroundColor' } },
  // Master stat — slides 7 (pillars) and 15 (moat)
  { replaceAllText: { containsText: { text: '11–20× less energy per mile vs diesel', matchCase: true }, replaceText: '7–13× lower energy cost per mile vs diesel' } },
];

const g = await invokeTool({ connectionId: 'conn_9qpjytrfnwhbgs2sd9cf', toolName: 'google_slides_batch_update_presentation', args: { presentationId: PRES, requests } });
if (!g.ok) { console.log('ERR', g.error); process.exit(1); }
const d: any = await g.json();
const replies = d.replies ?? [];
const rat = replies.filter((r: any) => r?.replaceAllText).map((r: any) => r.replaceAllText.occurrencesChanged);
console.log('requests applied:', requests.length, '| replaceAllText occurrences:', JSON.stringify(rat));
