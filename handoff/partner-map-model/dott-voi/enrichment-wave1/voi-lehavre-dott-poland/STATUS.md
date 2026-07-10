# Dott / Voi canonical geography enrichment — lane status

**Lane:** Voi Le Havre / Seine estuary plus Dott Baltic Poland  
**Date:** 2026-07-10  
**Repository snapshot:** `feddb5845114719352e93ec905f01ec942e0a7f0` (`main`, inspected only)  
**Status:** **review-ready research handoff**; research is still needed for the listed terminal/BP holds, then seal is needed. **Not seal-complete.**

## Programmatic counts

| Metric | Count |
|---|---:|
| Source rows reviewed | 86 |
| Current rows | 86 |
| Dott Poland rows | 85 |
| Voi Le Havre rows | 1 |
| Marine-relevant rows | 18 |
| Inland/non-lane exclusions | 68 |
| Accepted exact Atlas binds | 0 |
| Unresolved marine rows | 18 |
| Proposed global clusters (`not_banked`) | 9 |
| Proposed city/locale records (`not_banked`) | 19 |
| Candidate BPs (`not_banked`) | 17 |
| Candidate routes (`route_id: null`) | 8 |

Classification totals: `{"inland_exclude": 68, "new_city_brief_needed": 9, "new_cluster_brief_needed": 9}`. Priority totals: `{"P0": 6, "P1": 8, "P2": 4}`.

## Exact-bind result

The current Atlas contains 109 clusters, 312 unique cluster-member city IDs, 248 city features, 51 priority-city features, 37 locale features, 269 indexed city-brief anchors and 6,251 canonical routes. Exact indexes were built from cluster members, city/priority-city/locale IDs and labels, briefs, and route endpoint city IDs.

No assigned lane row has an acceptable existing Atlas stable-ID or documented-alias bind. Nulls were preserved; no fuzzy binding was performed. Name accent-folding was used only to find candidates, never to accept a bind.

## P0 recommendations

1. **Le Havre / Seine estuary — Voi only.** Create the global Le Havre system after review, anchored on the specific Vedettes Baie de Seine landing at Digue Charles Olsen / Port de plaisance du Havre. The Le Havre–Port-Deauville candidate has official destination/operator precedent. Do **not** attribute Le Havre to Dott.
2. **Gdańsk Bay / Tricity — Dott.** Prioritize Gdańsk, Gdynia and Sopot. Start with the City of Gdańsk's named F5/F6 water stops, Marina Yacht Park and Marina Sopot. Resolve Sobieszewo as city versus locale before banking.
3. **Szczecin / Świnoujście — Dott.** Bank the two anchor cities and official marinas only after route QA. The through-lagoon candidate is a hold until distance/range/channel QA; do not force one long route.

P1 follows with Elbląg–Krynica Morska (Vistula Lagoon), Mielno/Lake Jamno, and evidence-backed Kołobrzeg, Łeba and Ustka BPs. P2 rows lacking exact BP evidence remain held.

## Guardrails applied

- Geography and routes are global, never partner-specific.
- Voi is Europe-only. No MENA scope was created. Dott UAE policy is untouched.
- Partner city evidence is not represented as proof of boat pickup or partner marine operation.
- No cluster/city/BP/route IDs were banked. Suggested IDs exist only in `proposed_*` fields with `bank_status: not_banked`.
- No coordinates, geometry, demand, fares or economics were invented or promoted.
- Every candidate route has `route_id: null` and `geometry: null`.

## Files

- `EXACT-BIND-LEDGER.json` — all 86 source rows with source evidence, exact-index result, relevance and classification.
- `CANONICAL-GEOGRAPHY-HANDOFF.json` — proposed global systems/cities, 17 candidate BPs, 8 null-ID routes, citations, holds and deterministic Grok actions.
- `FAILED-SOURCES.md` — failed/weak source attempts and explicit holds.
