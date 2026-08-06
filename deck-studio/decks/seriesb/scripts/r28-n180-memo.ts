// R28 — Jaideep 2026-08-06: N220 → N180 ladder rename; slide 5 phase 05 back to Sampriti's
// "80–180 ft"; memo revision per Sampriti voice notes (future-we-see opening, night-freight
// pilot framing, N180); slide 23 lede + slide 31 milestone aligned.
import { invokeTool } from '@tasklet/tools/v2';
const SLIDES = 'conn_9qpjytrfnwhbgs2sd9cf', DRIVE = 'conn_t9cewrss13c4ycr82vyg';
const MASTER = '1g95_1hKvlz8Pfar-fmhoUsONcJyu6-zPPfhvRhPxu4k';
const TEASER = '1JJ-QWO5-W1K_GQaUu7NCARrY7_C3COAl0s-4HnUz8GY';
const MEMO = '10ba33SA2F6XhMgDJys1cqrGZYbC78RaT4QDmOtPaDl0';

async function slideIds(pres: string): Promise<string[]> {
  const g = await invokeTool({ connectionId: SLIDES, toolName: 'google_slides_get_presentation', args: { presentationId: pres } });
  if (!g.ok) throw new Error(String(g.error));
  return ((await g.json()) as any).slides.map((s: any) => s.objectId);
}
const mIds = await slideIds(MASTER);
const tIds = await slideIds(TEASER);

// --- Deck edits (page-scoped replaceAllText) ---
const deckJobs: [string, string, string, string, string][] = [
  // [pres, pageId, find, replace, label]
  [MASTER, mIds[4], '80–220 ft', '80–180 ft', 'master s5 phase05'],
  [MASTER, mIds[12], 'N120 — ocean ferry and cargo / contested logistics', 'N120 · N180 — ocean ferry and cargo / contested logistics', 'master s13 ladder'],
  [TEASER, tIds[9], 'N120 — ocean ferry and cargo / contested logistics', 'N120 · N180 — ocean ferry and cargo / contested logistics', 'teaser s10 ladder'],
  [MASTER, mIds[22], 'night freight on the passenger network is how it starts.', 'night freight on the passenger fleet is the pilot-phase test.', 'master s23 lede'],
  [MASTER, mIds[30], 'N120 Morpheus program — kickoff on contract', 'N180 program — kickoff on contract', 'master s31 milestone'],
];
for (const [pres, pageId, find, repl, label] of deckJobs) {
  const g = await invokeTool({ connectionId: SLIDES, toolName: 'google_slides_batch_update_presentation', args: { presentationId: pres, requests: [{ replaceAllText: { containsText: { text: find, matchCase: true }, replaceText: repl, pageObjectIds: [pageId] } }] } });
  if (!g.ok) { console.log(`DECK FAIL ${label}: ${g.error}`); continue; }
  const r: any = await g.json();
  const n = r.replies?.[0]?.replaceAllText?.occurrencesChanged ?? 0;
  console.log(`${label}: ${n} occurrence(s)`);
}

// --- Memo edits ---
const memoEdits: [string, string][] = [
  // Sampriti: open with "the future we see" — ships got bigger, not faster; others tried; disciplined path. Definition kept.
  ['The world moves at the speed and cost at which people and goods move — and energy determines both.\n\nNavier builds hydrofoiling vessels',
   'Everything has gotten faster — cars, planes, information — except ships, which have only gotten bigger. That gap is the future we see: the largest unclaimed lane in transportation.\n\nFast water transport has been tried before and failed — hull-first, control-last, the economics never closed. Navier is building it the other way: control first, one proven core, one network at a time.\n\nThe world moves at the speed and cost at which people and goods move — and energy determines both.\n\nNavier builds hydrofoiling vessels'],
  // Ladder now includes N180
  ['Three larger platforms (45 ft, 80 ft, 120 ft) are in design on the same core',
   'Four larger platforms (45 ft, 80 ft, 120 ft, 180 ft) are in design on the same core'],
  // Night freight = pilot-phase trial, cost-gated (Sampriti)
  ['The way in costs nothing new: night freight on the passenger fleet — same piers, same charging, same software — earns cargo revenue before the first freighter launches.',
   'The way in costs nothing new: in the pilot phase we trial night freight on the passenger fleet — same piers, same charging, same software — proving the cargo model corridor by corridor, where the economics clear, before the first freighter launches.'],
  ['night freight next, dedicated freighters (N80, N120) as the network scales',
   'night-freight trials next, dedicated freighters (N80–N180) as the network scales'],
  // §11 firewall-clean label now that N180 is a public rung
  ['Gulf 180-ft program kickoff, on contract',
   'N180 program kickoff (Gulf) — on contract'],
];
for (const [find, repl] of memoEdits) {
  const g = await invokeTool({ connectionId: DRIVE, toolName: 'google_drive_replace_text_in_document', args: { documentId: MEMO, targetText: find, replacementText: repl } });
  if (!g.ok) { console.log(`MEMO FAIL [${find.slice(0, 50)}…]: ${g.error}`); continue; }
  console.log(`memo edit ok: [${find.slice(0, 60)}…]`);
}
console.log('DONE');
