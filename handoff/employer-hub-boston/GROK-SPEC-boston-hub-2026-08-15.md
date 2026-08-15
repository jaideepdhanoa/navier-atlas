# GROK SPEC — Employer Hub: Boston Harbor (new hub)
**Date:** 2026-08-15 · **Owner:** Tasklet (spec) / Grok (deterministic build) · **Merge gate:** Jaideep

## Mandate
Add a **new `boston` hub** to the existing employer-hub system in `jaideepdhanoa/navier-atlas` under `employer-hub/` — a **registry + template extension, NOT a rewrite**. Reuse everything the Bay/NY v2 build shipped: shared template, `employer-hub/registry.json`, `hubs/{hub}/hub.json`, phase toggle, line `type` styling (trunk/feeder/express/seasonal), interchange rings + transfer chips, catchment panel, trip planner, LOI intake. Canonical path/alias conventions unchanged: route `/employers/boston`, alias `/boston-employers`.

## Inputs (this folder)
| File | What |
|---|---|
| `boston-hub-v1-stops-lines.json` | Tasklet-authored hub draft — 18 stops, 9 lines, phases, roles, catchment, decision_ledger, watchlist, no_landing ledger, gates, copy directives. **Authoritative.** |
| `../BOSTON-NODE-INVENTORY.md` | Source-verified node research (every landing cited; regulatory findings; ops caveats) |

## Division of labor (standing)
- **Tasklet authored:** stops, lines, phases, roles, catchment counts, copy directives, gates, decision_ledger. Do not re-derive.
- **Grok owns (deterministic):** BP gazetteer ID-match → `resolved_bp_id`/`lng`/`lat` per stop; **water-only** `water_path` waypoints for every line; `water_min` per segment from sealed geometry; template work; registry entry; QA screenshots.
- **`routing` extension (standing since Miami):** the authored JSON carries `segments[].routing` — Tasklet-authored water-path directives (channels, boundaries, exclusions). They are **binding directives for Grok's `water_path` work**, not coordinates: honor every named channel, boundary crossing, and exclusion when drawing geometry.
- **No invented landings.** Every stop maps to the exact named landing in `BOSTON-NODE-INVENTORY.md`. If a stop cannot be ID-matched to a real BP, add it to the `bp_gap` ledger in the hub JSON with reason and render it only from the inventory-named coordinates — never guess.

## Hub-specific requirements (hard gates — fail closed)

1. **INNER-HARBOR NO-WAKE HONESTY (the Boston-defining gate).** Boston Inner Harbor is a no-wake zone beginning at the **NW corner of Logan Airport**. A hydrofoil is foil-borne only **outside** the inner harbor (President Roads / Nantasket Roads / Broad Sound); every inner-harbor leg runs at displacement speed like everyone else. The authored JSON flags this at segment level: `segments[].speed_constrained: true`. On flagged segments, `water_min` must render as **"indicative — subject to Boston Harbor speed rules"** — never a bare number, and every published trip time must model the displacement leg. **NO "foiling into downtown" or foil-speed-to-the-dock claims anywhere in copy.** A zero-wake hydrofoil gets no automatic exemption; do not soften this in copy. Lines **BOS-6** (Inner Harbor Shuttle) and **BOS-9** (Riverside Shuttle) are all-no-wake: render them with **zero speed/time-advantage language** — seats, frequency, experience only.

2. **SEA-STATE HONESTY (North Shore / outer legs).** Salem, Beverly, Lynn, and Scituate legs cross Broad Sound / open Massachusetts Bay — semi-open Atlantic; the incumbent Salem Ferry cancels for rough seas multiple days at a time. **No all-weather or every-day claims for these legs.** Rendered copy includes the weather-cancellation-policy language and the commuter-rail fallback note for Salem and Beverly (per authored `copy.sections.north_shore_weather`). Winter/ice discussion is internal-only — never rendered.

3. **INCUMBENT RESPECT.** MBTA/Massport are respected incumbents and potential partners, never displacement targets. Render Navier strictly as a **premium employer-sponsored tier plus unserved marina-grade stations** (Salem, year-round Marina Bay, Beverly). The MBTA proof points in `gates.incumbent_respect.usable_public_proof_points` (1.5M riders 2025, year-round F10 loop, best OTP/farebox) ARE usable in rendered copy. Grep of rendered copy must show zero replace/beat/compete-with-MBTA framing.

4. **LOGAN — decision_ledger, NOT rendered.** The Logan dock is verified PASS but Boston↔Logan is a **held corridor**: there is **no Logan stop, line, or map marker in any phase, under any circumstances**. The top-level `decision_ledger` array is internal-only — strip it from the built bundle like `note_internal`. Water paths for Salem/Lynn/Winthrop legs pass Logan's frontage geometrically (per `routing`); no marker or label appears there. Include-on-microsite is a Jaideep decision — do not pre-empt it.

5. **ENCORE / RIVERSIDE displacement-only rendering.** Every BOS-9 segment is `speed_constrained: true` (entire Mystic reach no-wake + Alford Street Route 99 drawbridge). Render BOS-9 as a feeder with no time advantage implied; its geometry transits the drawbridge and terminates at Encore (Amelia Earhart Dam is upstream — never route above Encore). Lovejoy Wharf is **harbor-side of the Charles River Dam** — never route into the Charles basin or the Gridley Locks (entire basin is off-network per `no_landing`).

6. **Standard gates (inherited from v2):**
   - `dock_track` / `note_internal` / `decision_ledger` stripped from the rendered DOM — strip from the bundle, not just hidden.
   - No invented landings; `bp_gap` ledger for any unresolved BP.
   - All times **indicative** until Atlas geometry seals them.
   - Phase toggle defaults to **"At launch"**; Phase 2/3 render dimmed with "planned" styling (incl. the Beverly, Commonwealth Pier, and Central Wharf infill stops on Phase-1 lines).
   - LOI framing is **non-binding** everywhere.
   - **No dock-negotiation language** anywhere in rendered copy (no Chapter 91/DEP, DCR/Massport terms, harbormaster-berth, or lease talk — the Marblehead berth workstream stays internal).
   - **No fares anywhere** — seat-price band renders as a program band only ("Boston-specific pricing TBD"); line-level `note_internal` fare anchors never render.
   - Launch timing honesty: service **not before end-2027**; the map is coverage narrative, not a service promise.

7. **Watchlist & no_landing are render-exclusion lists.** `watchlist` entries (Marblehead, Swampscott, Cohasset, Gloucester, Chelsea Admiral's Hill) and `no_landing` entries (Assembly Row, Chelsea public dock, Kendall/entire Charles basin, GE Lynn plant, Salem Hospital, MGH, Fort Point Channel interior) must NOT appear as stations, stops, or map markers in any phase. Do not create a Marblehead stop, an Assembly Row stop, a Kendall/Charles-basin stop, or a Logan stop under any circumstances.

8. **Geometry notes for water_path work:** honor `segments[].routing` exactly. Key constraints: North Shore legs run Salem Sound → past Marblehead/Nahant → Broad Sound → President Roads → no-wake boundary at Logan's NW corner; South Shore legs run Hingham Bay → Nantasket Roads → President Roads; Winthrop legs route **around Logan's runway-approach areas** via President Roads with no Logan call; Quincy legs cross Dorchester Bay to President Roads; Scituate runs outside-harbor past Minot Ledge; BOS-9 transits the Alford Street drawbridge and never enters the Charles basin; never route into Fort Point Channel interior. All paths water-only.

## Acceptance (QA report must show)
1. Hub renders all 9 lines with **water-only geometry — zero land crossings**, routed per the `routing` directives: through President Roads, around Logan's runway approaches (no Logan marker), through the Alford Street drawbridge on BOS-9, and with zero incursions into the Charles basin or Fort Point Channel interior. Phase toggle working; interchange ring on `long-wharf` (primary), `fan-pier`, and `rowes-wharf`; transfer chips correct.
2. Every `speed_constrained: true` segment renders its time as "indicative — subject to Boston Harbor speed rules"; grep of rendered copy shows zero "foiling into downtown"/foil-speed-to-dock claims and zero speed/time-advantage language for BOS-6 and BOS-9.
3. Grep of rendered copy shows zero MBTA/Massport displacement framing (no replace/beat/compete language); the authored incumbent proof points render as written.
4. Catchment panel numbers match the authored `catchment` array **exactly** (6→17 for the four Phase-1 anchors: Seaport, Financial District, Salem/North Shore, Quincy/South Shore; 0→17 for Charlestown and East Boston).
5. No `watchlist`, `no_landing`, or `decision_ledger` entry appears on the map or in the DOM in any phase state — explicitly: no Marblehead, no Logan, no Kendall/Charles basin, no Assembly Row.
6. Internal fields absent from the built bundle (grep for `dock_track`, `note_internal`, `decision_ledger`, and for the fare anchors `$65` / `$70`).
7. Registry has the `boston` entry; `/employers/boston` and alias `/boston-employers` both resolve; LOI POST works end-to-end.
8. 0 invented landings; `bp_gap` ledger populated with reason for any unresolved BP.
9. Screenshots: hub at each phase state (At launch · +Phase 2 · Full network), catchment panel open, one speed-constrained segment tooltip (inner harbor) and the BOS-9 line rendered.
10. Registry untouched except the new entry + version bump; bay-area, new-york, washington-dc, and miami hubs unaffected.
