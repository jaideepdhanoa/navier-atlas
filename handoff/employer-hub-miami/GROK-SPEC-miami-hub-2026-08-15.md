# GROK SPEC — Employer Hub: Miami & Fort Lauderdale (new hub)
**Date:** 2026-08-15 · **Owner:** Tasklet (spec) / Grok (deterministic build) · **Merge gate:** Jaideep

## Mandate
Add a **new `miami` hub** to the existing employer-hub system in `jaideepdhanoa/navier-atlas` under `employer-hub/` — a **registry + template extension, NOT a rewrite**. Reuse everything the Bay/NY/DC builds shipped: shared template, `employer-hub/registry.json`, `hubs/{hub}/hub.json`, phase toggle, line `type` styling (trunk/feeder/express/seasonal), interchange rings + transfer chips, catchment panel, trip planner, LOI intake. Canonical path/alias conventions unchanged: route `/employers/miami`, alias `/miami-employers`. Hub label: **"Miami & Fort Lauderdale"**.

## Inputs (this folder)
| File | What |
|---|---|
| `miami-hub-v1-stops-lines.json` | Tasklet-authored hub draft — 16 stops in 2 clusters, 10 lines, phases, roles, catchment, watchlist, no_landing ledger, gates, copy directives. **Authoritative.** |
| `../MIAMI-NODE-INVENTORY.md` | Source-verified node research (every landing cited; manatee/speed-zone regulatory findings; corridor foil-credibility verdicts; ops caveats) |

## Division of labor (standing)
- **Tasklet authored:** stops, lines, phases, roles, clusters, catchment counts, copy directives, gates. Do not re-derive.
- **Grok owns (deterministic):** BP gazetteer ID-match → `resolved_bp_id`/`lng`/`lat` per stop; **water-only** `water_path` waypoints for every line; `water_min` per segment from sealed geometry; template work; registry entry; QA screenshots.
- **No invented landings.** Every stop maps to the exact named landing in `MIAMI-NODE-INVENTORY.md`. If a stop cannot be ID-matched to a real BP, add it to the `bp_gap` ledger in the hub JSON with reason and render it only from the inventory-named coordinates — never guess.
- **Schema note:** segments carry an additional `routing` string field (deterministic geometry directives, e.g. Norris Cut). Treat it as build input for `water_path`; it may render in tooltips only where it contains no internal/negotiation content.

## Hub-specific requirements (hard gates — fail closed)

1. **TWO-CLUSTER RENDERING (the Miami-defining gate).** One hub, two independent networks: every stop and line carries `cluster: "miami"` or `cluster: "fort-lauderdale"`. The map must make unmistakably clear these are **two separate networks** — there is **NO inter-city water link in any phase**. Zero cross-cluster segments; no phantom connector line, dotted "future" link, or shared corridor between the clusters. Implementation is Grok's choice per template capability — cluster toggle OR split/dual-viewport map — and **the choice made must be flagged in the QA report**. The top-level `no_intercity_link` object explains why (25–30 nm, hard slow zones on both routings, Brightline wins on time); the renderable version of that message is the authored `copy.sections.two_networks` — use it verbatim, nothing stronger.

2. **SPEED-ZONE HONESTY (manatee zones).** The authored JSON flags constrained water at segment level: `segments[].speed_constrained: true`. On flagged segments, `water_min` must render as **"indicative — subject to local speed zones"** — never a bare number. Crossing-time claims appear **ONLY** on the whitelisted foil-credible corridors (see `gates.speed_zone_honesty.time_claim_whitelist`): Island Line (20–25 min), Grove Line Dinner Key↔Brickell leg (15–20 min), Beach Line via Norris Cut (20–25 min), and the two north-bay 30-mph ICW legs. **Zero time claims anywhere for: all Fort Lauderdale legs, the downtown-idle tails (Venetian→Bayside), the Brickell→EPIC hop, the Bay Line, and Aventura.** A zero-wake hydrofoil gets no automatic exemption from posted manatee zones; do not soften this in copy.

3. **GEOMETRY DIRECTIVES (water-only, zone-aware):**
   - **Beach Line MUST route via Norris Cut** — exit Miami Beach Marina through the Government Cut RNA slow water, then Norris Cut to open bay. **Never route via Fisherman's Channel.** No geometry through or over **Fisher Island** (closed private community, also in `no_landing`).
   - Island Line: open unzoned bay; route **around** the year-round no-entry zone west of Virginia Key — never cross it; through the Rickenbacker bridge pocket at the marked passage.
   - **Never route anything up the Miami River** (idle all year + drawbridge curfews). EPIC Marina is served on its **bayside face** only.
   - North-bay lines (MIA-4/5/6/7) follow the designated 30/35-mph channels and the ICW; the Venetian→Bayside tail follows the downtown ICW channel (idle water — expected).
   - FTL lines: ICW channel throughout; Hollywood Commuter transits the Port Everglades entrance channel; downtown legs go ICW → New River junction → upriver to the Riverwalk city docks (past the 3rd Ave/Andrews Ave drawbridges).
   - All paths water-only: Biscayne Bay, Norris Cut, ICW, New River as applicable. Zero land crossings; zero cross-cluster segments.

4. **SEASONAL AVENTURA (honest label).** `aventura-loggerhead` and line MIA-7 (`type: "seasonal"`) must render with the honest regulatory label: **"summer season only (May 1–Nov 14) — the Intracoastal channel here is a slow-speed manatee zone Nov 15–Apr 30."** Do NOT restyle as a summer-premium/resort product (no Hamptons ☀ framing) — the season is set by rule, not demand.

5. **INCUMBENT RESPECT (copy gate).** Fort Lauderdale copy positions Navier as a commuter-hours **complement** to Water Taxi FTL (they own leisure 10:00–22:00) — never displacement, never disparagement; line name is "Hollywood Commuter" (never "Hollywood Express" — incumbent's brand). The free Miami Beach city water taxi (Jan 2026, 20-min crossing) is a **public proof point**: copy may use "Miami Beach already runs a commuter water taxi — we make it a network" and cite its 20-minute crossing; never imply Navier replaces the free city service.

6. **Internal only — never rendered:** Maurice Gibb city dock agreement / incumbent contract; Vice City Marina berthing diligence; all marina/city negotiation material; hurricane-season ops planning; Bill Bird construction verification; drawbridge schedule-risk items. All live in `note_internal` and must be **stripped from the built bundle, not just hidden**.

7. **Standard gates (inherited from v2):**
   - `dock_track` / `note_internal` stripped from the rendered DOM and bundle.
   - No invented landings; `bp_gap` ledger for any unresolved BP.
   - All times **indicative** until Atlas geometry seals them (whitelisted claims render with the inventory ranges + an "indicative" qualifier).
   - Phase toggle defaults to **"At launch"**; Phase 2 renders dimmed with "planned" styling; seasonal styling for MIA-7.
   - LOI framing is **non-binding** everywhere.
   - **No dock-negotiation language** anywhere in rendered copy.
   - Launch timing honesty: service **not before end-2027**; the map is coverage narrative, not a service promise.

8. **Watchlist & no_landing are render-exclusion lists.** `watchlist` entries (Ferré Park deepwater slip, Rickenbacker Marina, Island Gardens/Yacht Haven Grande, Sands Harbor P6) and all 11 `no_landing` entries (Brickell Key, Mount Sinai, Margaret Pace Park, North Bay Village, Key Biscayne village center, Fisher Island, PortMiami/Royal Caribbean, Aventura Mall/Hospital, Hollywood CBD, Government Cut pier, Wynwood/Midtown/Design District) must NOT appear as stations, stops, or map markers in any phase. Do not create a Brickell Key stop, a Mount Sinai stop, or a PortMiami stop under any circumstances.

## Acceptance (QA report must show)
1. Hub renders all 10 lines with **water-only geometry — zero land crossings and zero cross-cluster segments**; Beach Line demonstrably routes via **Norris Cut** (not Fisherman's Channel) and no path touches **Fisher Island** or crosses the Virginia Key no-entry zone; nothing routes up the Miami River.
2. Two-cluster rendering verified: the chosen mechanism (toggle or split map) is stated in the QA report; no connector of any style exists between clusters; each cluster's interchange rings render (`vice-city-marina` primary + `epic-marina` in Miami; `venetian-marina` for the north-bay group; `seventeenth-st` in Fort Lauderdale) with correct transfer chips.
3. Every `speed_constrained: true` segment renders its time as "indicative — subject to local speed zones"; grep of rendered copy shows crossing-time claims ONLY on the whitelisted corridors and zero time claims for any FTL leg, the Bay Line, the EPIC hop, the downtown tails, or Aventura.
4. Aventura renders with the honest seasonal label (regulatory reason visible); MIA-7 styled `seasonal`.
5. Catchment panel numbers match the authored `catchment` array **exactly** (Brickell 4→4, Downtown Miami 0→5, Coconut Grove 4→4, Miami Beach 4→4, FTL downtown 3→4, Hollywood 3→4) with the per-sub-network counting rule respected.
6. No `watchlist` or `no_landing` entry appears on the map or in the DOM in any phase state.
7. Internal fields absent from the built bundle (grep for `dock_track`, `note_internal`, `Maurice Gibb agreement`, `berthing`, `hurricane`).
8. Registry has the `miami` entry; `/employers/miami` and alias `/miami-employers` both resolve; LOI POST works end-to-end.
9. 0 invented landings; `bp_gap` ledger populated with reason for any unresolved BP.
10. Screenshots: **each cluster at each phase state** (At launch · +Phase 2), catchment panel open, one speed-constrained segment tooltip, the Aventura seasonal label, and the two-network view.
11. Registry untouched except the new entry + version bump; bay-area, new-york, and washington-dc hubs unaffected.
