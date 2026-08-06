import { invokeTool } from '@tasklet/tools/v2';
import { PRES } from '/tasklet/agent/home/scripts/seriesb-rebuild/h.ts';
const rep = (text: string, replaceText: string, pageObjectIds: string[]) => ({
  replaceAllText: { containsText: { text, matchCase: true }, replaceText, pageObjectIds },
});
const requests = [
  // Slide 5 — card 4: dedicated cargo is the strategy; night freight is the seed
  rep('Fill the night shift', 'Move the freight', ['st_r19_ladder']),
  rep(
    'The same boats and routes carry urgent freight overnight. First corridor targeted 2027.',
    'Dedicated cargo vessels loading at any ramp — seeded by night freight on the passenger fleet.',
    ['st_r19_ladder'],
  ),
  // Slide 22 — cargo chapter lede: stop leading with the night shift
  rep(
    'Passenger networks run 16 hours a day — then sleep. Cargo is the night shift.',
    'Dedicated foiling freighters are the play; night freight on the passenger network is how it starts.',
    ['g3f6623c186e_4_78'],
  ),
];
const g = await invokeTool({ connectionId: 'conn_9qpjytrfnwhbgs2sd9cf', toolName: 'google_slides_batch_update_presentation', args: { presentationId: PRES, requests } });
if (!g.ok) { console.log('ERR', g.error); process.exit(1); }
const d: any = await g.json();
console.log('occurrences:', (d.replies ?? []).map((r: any) => r.replaceAllText?.occurrencesChanged ?? 0).join(','));
