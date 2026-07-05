# GROK SPEC — Caspian + Maghreb enrichment (route-mint seal)

**Date:** 2026-07-05
**Owner handoff:** Tasklet → Grok (Atlas / render-graph lane)
**Status:** research-complete / **seal-needed**
**Partner context:** Yango (all four markets are confirmed Yango ridehail markets)

## Mandate
Deepen four thin/shallow Yango markets into credible real networks by minting the sourced
boarding points and short-hop corridors below. Every BP is a real, source-cited place; every
corridor carries an explicit **hand-waypoint note to prevent land crossings**. This is the
Jaideep directive: *"nothing held to credible starter networks — every touched market built to
real-world scale."*

## Scope (35 BP candidates · 23 corridors · 4 markets)
| Market | Cluster | Cities touched | New BPs | Corridors |
|---|---|---|---|---|
| Azerbaijan | azerbaijan-caspian | Baku (+Absheron nodes) | 6 | 4 |
| Kazakhstan | (Aktau/Mangystau) | Aktau, Kuryk | 4 | 3 |
| Tunisia | tunisia | Tunis, Bizerte*, Hammamet*, Sousse*, Monastir*, Djerba | 9 | 6 |
| Algeria | algeria | Algiers, Oran, (Bejaia/Mostaganem honest-thin) | 6 | 4 |
| Morocco | morocco | Tangier, M'diq/Tetouan*, Al-Hoceima, Rabat-Sale, Mohammedia* | 10 | 6 |

`*` = new sourced city (legitimate registry addition, not invention — each has a source URL).

## Input files (authoritative)
- `caspian-enrichment-2026-07-05.json` + `caspian-briefs-2026-07-05.json`
- `tunisia-enrichment-2026-07-05.json` + `tunisia-briefs-2026-07-05.json`
- `algeria-enrichment-2026-07-05.json` + `algeria-briefs-2026-07-05.json`
- `morocco-enrichment-2026-07-05.json` + `morocco-briefs-2026-07-05.json`

Each enrichment JSON has, per corridor: `from`, `to`, `approx_nm`, `desc`,
`hand_waypoint_required`, `hand_waypoint_note`. Each briefs JSON has partner-neutral city +
cluster briefs to seal into the render graph.

## Deterministic tasks (Grok lane only)
1. **ID-match / gazetteer promote** each BP candidate to a real coordinate + stable `bp_id`.
   Reuse existing anchors where flagged (`existing: true` / `existing_id_hint`) — e.g.
   `bp-85bc806add` (Marina Djerba), the existing Baku Boulevard pier, Port d'Alger, Al-Hoceima port.
2. **Mint new cities** where `id_hint` given (bizerte, hammamet, sousse, monastir, mdiq-tetouan,
   mohammedia) with country-suffixed slugs matching the naming gotcha (`{city}-{country}`).
3. **Build BP↔BP corridors** exactly as listed — inherit `route_id` from the graph 1:1; **never
   invent a route_id — null beats wrong.** Do not curate a subset; mint every listed corridor.
4. **Apply the hand-waypoints.** Every `hand_waypoint_required: true` corridor must route through
   the offshore waypoint described so the geometry has **zero land crossings**. Critical cases:
   - **Baku → Sea Breeze/Bilgah:** round the **eastern tip of the Absheron peninsula** offshore —
     Baku is south shore, the resorts are north shore. NEVER cross the peninsula.
   - **Aktau → Kuryk:** round the headland offshore across the bay.
   - **Djerba (Houmt Souk → Ajim):** stay OUTSIDE the Gulf of Gabès sandbanks; respect the depth mask.
   - **Morocco:** all Mediterranean corridors route offshore/**south of Ceuta & Melilla** (Spanish
     enclaves = no-go); Atlantic corridors clear the surf line.
   - **Algiers bay:** round the Sidi Fredj peninsula + Cap Matifou headland.
5. **Respect closed-sea range guards** (context-only, DO NOT mint): Baku↔Aktau cross-Caspian
   (~250 nm), Algiers↔Oran/Bejaia (>70 nm), Morocco Atlantic↔Mediterranean, Tunis↔Djerba super-corridor.
6. **Seal briefs** into the render graph (cluster + city briefs, partner-neutral).

## Acceptance gate (Grok QA report must show)
- 0 land crossings post-waypoint (hard gate).
- 0 silent BP drops — every candidate sealed as POI or in a drop-ledger with a reason.
- Every new city carries country-suffixed slug + real coords + source id.
- Every minted corridor carries a real `route_id` or is null (never invented).
- Depth/enclave masks respected (Gulf of Gabès, Ceuta/Melilla).
- Before→after POI counts per city; corridor counts built vs culled.

## What Tasklet still owns (NOT Grok)
- Re-adding Azerbaijan + Tunisia to the Yango partner surface (`yango.json` `_map_scope`,
  `network_footprint`, CLUSTERS/FEATURES tags) — separate Tasklet PR.
- Finance corridors for these markets in `finance/model/corridors.json` — separate finance lane.
