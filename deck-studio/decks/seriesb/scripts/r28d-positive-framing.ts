// R28d — Jaideep 2026-08-06: drop "not ocean crossings" everywhere; focus on what we do.
import { invokeTool } from '@tasklet/tools/v2';
const SLIDES = 'conn_9qpjytrfnwhbgs2sd9cf', DRIVE = 'conn_t9cewrss13c4ycr82vyg';
const MASTER = '1g95_1hKvlz8Pfar-fmhoUsONcJyu6-zPPfhvRhPxu4k';
const MEMO = '10ba33SA2F6XhMgDJys1cqrGZYbC78RaT4QDmOtPaDl0';
const S23 = 'g3f6623c186e_4_78';

// 1) deck: slide 23 lede -> Jaideep's exact positive phrasing
const r1 = await invokeTool({ connectionId: SLIDES, toolName: 'google_slides_batch_update_presentation', args: { presentationId: MASTER, requests: [
  { replaceAllText: { containsText: { text: 'Short-sea and island freight — regional corridors, not ocean crossings.', matchCase: true },
    replaceText: 'Dedicated foiling freighters for short-sea and island corridors.', pageObjectIds: [S23] } },
] } });
if (!r1.ok) throw new Error('deck: ' + r1.error);
console.log('DECK occurrences:', JSON.stringify(((await r1.json()) as any).replies?.map((x: any) => x.replaceAllText?.occurrencesChanged)));

// 2) memo live: fold scope into the play sentence, delete the negative sentence
const FIND = 'This is a short-sea play — islands, coasts, and regional corridors; on ocean crossings, ships carrying thousands of containers are unbeatable on cost, and we do not compete there. The play is dedicated foiling freighters on the same proven core';
const REPL = 'The play is dedicated foiling freighters for short-sea and island corridors, built on the same proven core';
const r2 = await invokeTool({ connectionId: DRIVE, toolName: 'google_drive_replace_text_in_document', args: { documentId: MEMO, targetText: FIND, replacementText: REPL } });
console.log('MEMO live:', r2.ok ? 'OK' : 'FAIL: ' + r2.error);
