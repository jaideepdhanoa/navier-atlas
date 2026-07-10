# Belgium + Switzerland Dott/Voi enrichment — status

**Audit date:** 2026-07-10  
**State:** research handoff ready for review; **not seal-complete**  
**Repository edits:** none

## Programmatic counts

- Lane current source rows reviewed: **45** (Dott 32; Voi 13)
- Marine-relevant rows: **21**
- Exact existing binds: **1** (Voi Switzerland country row → existing `switzerland` cluster only)
- Exact city-ID binds: **0**
- Unresolved marine rows: **20**
- Inland/non-marine exclusions: **24**
- Candidate named BPs: **21** (2 existing Atlas IDs; 19 not banked)
- Candidate canonical routes: **9**, all with `route_id: null`
- Proposed global clusters: **1**, not banked
- Proposed global city briefs: **8**, not banked

Classification totals: `{"existing_cluster_city_gap": 1, "existing_exact_id": 1, "inland_exclude": 24, "new_city_brief_needed": 12, "new_cluster_brief_needed": 7}`

## P0 review recommendations

1. **Brussels canal:** both Dott and Voi name Brussels. Add one reviewed global Belgium cluster/city, official Waterbus BPs, and one canonical local canal leg.
2. **Basel Rhine:** both partners name Basel; Dott also names Birsfelden and Muttenz. Use the official BPG landing chain and document aggregate-city membership.
3. **Lake Zürich:** both partners name Zürich. Use official ZSG landing evidence and seal one short domestic lake leg.

## P1 queue

- Antwerp Scheldt crossing (Voi).
- Ghent Graslei–Portus Ganda (Dott; exact landing/navigation QA required).
- Liège Guillemins–Fragnée (Dott); **Herstal stays on BP hold**.
- Nyon–Rolle (Voi) after Lake Geneva route-stamp repair and Nyon POI dedupe.
- Lake Constance Horn–Romanshorn–Rorschach (Dott); Goldach/Rorschacherberg municipal marinas require public-pickup/access QA.

## Key exactness findings

- Current Atlas has the `switzerland` cluster and aggregate city `lake-geneva-switzerland`; it has **no Belgium cluster**.
- The only exact row-level bind is Voi's country-level Switzerland row to cluster `switzerland`; country evidence does not establish service at every Atlas city.
- Nyon has two existing Atlas POIs under `lake-geneva-switzerland`, but the Voi Nyon row needs documented membership/alias and POI dedupe before binding.
- Every inspected existing Lake Geneva route (14/14) is stamped `cluster_id: indonesia`; this is a P0 canonical-integrity hold.
- All suggested identifiers occur only in `proposed_*` fields and are marked `not_banked`. No coordinates, demand, fares, economics, route IDs or current marine-operation claims were invented.

## Deterministic Grok handoff

Follow `CANONICAL-GEOGRAPHY-HANDOFF.json` in order: integrity repair → global briefs/aliases → cited BP banking → route geometry/water QA → canonical IDs → partner cluster inheritance → validation/render receipts. Do not author per-partner routes.
