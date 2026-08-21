# Follow-on migration — Boston, Miami, Washington DC, San Diego, Seattle

Not for the same PR as the template change. Sequenced after the v3 renderer ships and Bay Area /
New York are verified live.

## Target: all fifteen cities read the same way

| City | Today | After |
|---|---|---|
| **Seattle** | 16 rows authored to v3 already | **No data change.** The renderer fix alone makes it correct. Seattle is the shape everything else moves toward. |
| **Miami** | 10 rows, `note` on every row, all headcounts null | **No data change.** Renderer fix alone. |
| **Washington DC** | 8 rows, `note` on every row, 2 of 8 have `headcount` | Convert those 2 numbers to `value` strings (`17000` → `"~17,000 federal personnel"`, `8000` → `"8,000 today, 14,000 planned"`). The DC notes already carry the walk/shuttle truth. |
| **Boston** | 9 rows, `headcount` + per-row `seats`, `city_total_seats` 1,350 | Convert `headcount` to `value` strings; **drop the per-row `seats` column**, keep the city total with an explicit capture label. Add the walk/shuttle `note` each row currently lacks. |
| **San Diego** | stop/cluster rows in an employer-shaped table | Either author real employer rows from the San Diego tracker, or set `table_variant: "stop"`. It has a tracker, so employer rows are available — worth doing properly rather than falling back to the stop variant. |

## Why drop Boston's per-row seats

Boston is the only city rendering a per-employer `seats` figure, and every one of them is exactly
`headcount × 3%`. That presents a modelled number in the same visual weight as an observed one, nine
times over. A single city total, labelled "3% of the headcounts shown", makes the same point once and
makes the assumption inspectable. Bay Area and New York are authored that way; Boston should follow so
the quality bar stays consistent.

Boston's city total would be unchanged at 1,350.

## Nine stop-led cities

Istanbul, Bahrain, Abu Dhabi, Dubai, Jeddah, Ras Al Khaimah, Red Sea Global, Saudi Eastern Province —
set `table_variant: "stop"`. These are tourism- and authority-led markets with no employer-commute
demand pool behind them; the blank Employer column is the symptom of borrowing a US template. Bahrain
already has a `DEMAND-POOLS-BAHRAIN.md` behind it and may deserve its own row shape later.

## Separate observation, not part of this work

Two line names render on public pages and contain banned jargon: **Peninsula Trunk**, **East Bay Trunk**
and **East River Feeder**. The plain-English gate bans "trunk" and "feeder" in external copy, but these
are the canonical line names in `hub.json`, so they appear on maps, line lists and now demand tables.
Renaming them is a network-wide change with map, deck and microsite fallout — flagging it, not doing it.
