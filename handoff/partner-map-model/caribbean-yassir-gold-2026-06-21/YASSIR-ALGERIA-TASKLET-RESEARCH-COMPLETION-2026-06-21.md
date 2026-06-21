# Yassir Algeria Tasklet research completion — 2026-06-21

## Status
**Tasklet-owned Algeria research is complete for batch 1.** Route IDs, render checks, and exact geometry remain Grok-owned.

This fixes the previous ambiguous state: Algeria is no longer held behind *Tasklet city/BP research* or *Tasklet demand/fare assumptions*. It is held behind **Grok sealing** and then the **Tasklet economics cascade**.

## What Tasklet completed
- Yassir Algeria operating/city evidence from official Yassir sources.
- Coastal city triage and exclusions.
- Exact source-backed BP mint requests for Algiers, Béjaïa, Oran, and Mostaganem.
- Annaba kept as optional/backlog: city-supported, but not route/economics-ready.
- Route-level demand/fare assumptions with explicit nulls for weak candidates — no generic 30k placeholder.
- Algeria country-reference draft row ready to apply before cascade.

## Batch-1 cities
**Grok-ready:** `algiers-algeria`, `bejaia-algeria`, `oran-algeria`, `mostaganem-algeria`  
**Optional/backlog:** `annaba-algeria`, `skikda-algeria`, `boumerdes-algeria`, `ghazaouet-algeria_or_tlemcen-catchment`

## Selected route assumptions
| Candidate | Decision | Fare input | Demand input | Status |
|---|---:|---:|---:|---|
| Algiers Bay — La Pêcherie / Port d’Alger ↔ El Djamila / Aïn Bénian | primary model candidate after Grok seal | 500 DZD selected; 50/250/500/800 DZD sensitivity | 170,280 annual one-way pax selected; 103,200/170,280/240,800 sensitivity | ready after Grok seal + country row |
| Oran ↔ Mostaganem | secondary model candidate after recurrence check | 800 DZD sourced adult fare | 40,500 annual one-way pax selected; 18,000/40,500/72,000 sensitivity | hold until current recurrence + Grok seal |
| Béjaïa ↔ Algiers HSC | source/fare anchor only | 1,300 DZD sourced adult fare | null — no current capacity/load source | not initial N30 model; range-gate first |
| La Pêcherie ↔ Tamentfoust / Les Sablettes | mint queue only | null | null | no current schedule/fare source |
| Annaba passenger port | city/port backlog | null | null | exclude from batch-1 economics |

## Next owner split
1. **Grok:** mint/validate city IDs and BP node IDs; seal exact routes; return route IDs or `null`; range/land-crossing/render QA.
2. **Tasklet:** apply Algeria country-reference row; add only sealed Algeria corridors; cascade aggregate/growth/frontend/sheet/sidecar; update Yassir proposal/deck/data-clean.

## Artifacts
- `yassir-algeria-tasklet-research-completion-2026-06-21.json`
- `yassir-algeria-market-source-and-mint-queue.json`
- `yassir-algeria-route-source-hardening-batch-1.json`
- `algeria-country-reference-draft.json`
