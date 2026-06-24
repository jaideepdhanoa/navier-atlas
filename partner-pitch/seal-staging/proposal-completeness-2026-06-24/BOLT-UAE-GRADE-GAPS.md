# Bolt — curate to 12 + bring all to "UAE grade"

**Date:** 2026-06-24 · **From:** Tasklet · **For:** Grok
**Reference grade = `uae` market:** full narrative (12/12 fields), 5 journeys, minted water geometry,
`map_promote` cities. Every kept market must reach this bar.

## A. Curation applied to `bolt.json` (this PR)
18 markets → **12 shown, 6 hidden.** Curation driven by two new fields per market:
`display_order` (render sequence) and `hidden: true` (suppress). Physical array order left unchanged
for a clean diff — **renderer must sort by `display_order` and drop `hidden:true`.**

| # | Shown (display_order) | id |
|---|---|---|
| 1 | Croatia | croatia |
| 2 | France — Côte d'Azur | france-riviera |
| 3 | East Africa | east-africa |
| 4 | Estonia | estonia |
| 5 | Greece — Saronic & Cyclades | greece |
| 6 | Italy — Amalfi, Capri & Venice | italy |
| 7 | Nigeria — Lagos | nigeria |
| 8 | Qatar — Doha Bay | qatar |
| 9 | Saudi Arabia — Jeddah & Eastern Province | ksa-commercial |
| 10 | Spain — Balearics & Costa Brava | spain |
| 11 | Thailand — Phuket & Phang Nga | thailand |
| 12 | UAE — Dubai & Abu Dhabi *(grade reference)* | uae |

**Hidden (6):** egypt, finland, ireland, portugal, south-africa, sweden.
**Label cleaned:** "Saudi Arabia (commercial) — …" → "Saudi Arabia — …". **`id`/`slug` kept stable**
(`ksa-commercial` is referenced by `yango.json` and the Bolt↔Yango crosswalk — renaming would break
those bindings). The "(commercial)" text only ever lived in the display label.

## B. Gaps to reach UAE grade — Grok corridor minting
"UAE grade" requires every journey leg minted to a real `route_id` and its cities promoted to
`map_promote` geometry (not cluster_dots). **38 corridor legs** are still unbuilt across the 12:

| Market | unbuilt / total | Legs to mint |
|---|---|---|
| Croatia | **6 / 6** | Split↔Trogir; Dubrovnik↔Elaphiti; Split↔Šolta; Dubrovnik↔Cavtat; Split↔Brač; **Dubrovnik↔Kotor (ME)** |
| France-Riviera | 4 / 9 | Nice Airport↔Monaco; St-Tropez↔Pampelonne; Cannes↔St-Tropez; Nice↔St-Tropez |
| East Africa | 1 / 2 | Mombasa↔Diani/Ukunda |
| Estonia | 1 / 5 | Tallinn↔Helsinki |
| Greece | **5 / 5** | Mykonos↔Delos; Glyfada↔Vouliagmeni; Naxos↔Paros; Piraeus↔Glyfada; **Rhodes↔Marmaris (TR)** |
| Italy | 4 / 5 | Venice↔Lido; San Marco↔Murano/Burano; S.Margherita↔Portofino; Positano↔Amalfi |
| Nigeria | **5 / 5** | CMS↔VI; Osborne↔CMS; CMS↔Apapa; CMS↔Ikorodu; Lekki↔Epe |
| Qatar | 1 / 4 | The Pearl↔Doha Corniche |
| Saudi Arabia | 1 / 5 | Dammam↔Tarout/Qatif |
| Spain | 4 / 6 | L'Estartit↔Medes; Marbella↔Puerto Banús; Sóller↔Sa Calobra; **Tarifa↔Tangier (MA)** |
| Thailand | **5 / 5** | Phuket↔Phang Nga; Phuket↔Koh Yao Noi; Phuket↔Phi Phi; Phuket↔Krabi; Phuket↔Koh Samui |
| UAE | 1 / 5 | Dubai Marina↔Abu Dhabi Corniche |

**Cross-border water gates needing explicit validation (international legs):** Dubrovnik↔Kotor (ME),
Rhodes↔Marmaris (TR), Tarifa↔Tangier (MA). Mint only if a clean water gate exists — **null beats
confidently-wrong**; otherwise mark seasonal/aspirational, don't fake the geometry.

**Map promotion:** Bolt has **23 cluster_dots vs 27 map_promote**. Promote the kept-market cities to
geometry as their legs mint; hidden-market dots can stay un-promoted.

## C. Narrative gap — East Africa is the shallow outlier
East Africa carries only **2 journeys** (vs UAE's 5) and is **missing 9 of 12 narrative fields**:
`partner_context, why_navier_now, differentiation, proof_points, objections, the_ask, close, end_state,
vessel_sizing`. The other 11 kept markets are field-complete. → **Tasklet authors the East Africa
narrative to UAE parity and adds journey legs (Dar↔Stone Town deepening, Mombasa↔Diani, Mafia, Pemba
hop) after Grok mints the geometry.**

## D. Sequence (fits the master work order)
1. **Grok** mints the 38 legs (validate the 3 cross-border gates), promotes kept-market cities to
   `map_promote`, hands back per batch.
2. **Tasklet** cascades the TAM ladder on the minted `route_id`s, authors East Africa to UAE parity,
   refreshes sheet/tracker/sidecar.
3. **Grok** reseals the Bolt page/map honoring `display_order` + `hidden`.

*Also fixes the 3 Bolt data bugs from the audit: floor rounding ($1.54M shown as "$2M"), stale
`careem-aggregate.json` rollup pointer, and the census-heavy ladder base.*
