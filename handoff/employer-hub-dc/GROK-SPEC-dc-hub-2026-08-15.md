# GROK SPEC — Employer Hub: Washington DC / Potomac (new hub)
**Date:** 2026-08-15 · **Owner:** Tasklet (spec) / Grok (deterministic build) · **Merge gate:** Jaideep

## Mandate
Add a **new `washington-dc` hub** to the existing employer-hub system in `jaideepdhanoa/navier-atlas` under `employer-hub/` — a **registry + template extension, NOT a rewrite**. Reuse everything the Bay/NY v2 build shipped: shared template, `employer-hub/registry.json`, `hubs/{hub}/hub.json`, phase toggle, line `type` styling (trunk/feeder/express/seasonal), interchange rings + transfer chips, catchment panel, trip planner, LOI intake. Canonical path/alias conventions unchanged: route `/employers/washington-dc`, alias `/dc-employers`.

## Inputs (this folder)
| File | What |
|---|---|
| `dc-hub-v1-stops-lines.json` | Tasklet-authored hub draft — 11 stops, 7 lines, phases, roles, catchment, watchlist, no_landing ledger, gates, copy directives. **Authoritative.** |
| `../DC-NODE-INVENTORY.md` | Source-verified node research (every landing cited; regulatory findings; ops caveats) |

## Division of labor (standing)
- **Tasklet authored:** stops, lines, phases, roles, catchment counts, copy directives, gates. Do not re-derive.
- **Grok owns (deterministic):** BP gazetteer ID-match → `resolved_bp_id`/`lng`/`lat` per stop; **water-only** `water_path` waypoints for every line; `water_min` per segment from sealed geometry; template work; registry entry; QA screenshots.
- **No invented landings.** Every stop maps to the exact named landing in `DC-NODE-INVENTORY.md`. If a stop cannot be ID-matched to a real BP, add it to the `bp_gap` ledger in the hub JSON with reason and render it only from the inventory-named coordinates — never guess.

## Hub-specific requirements (hard gates — fail closed)

1. **SPEED/WAKE HONESTY (the DC-defining gate).** Three regulatory speed regimes constrain this network:
   - Permanent no-wake zone **Memorial Bridge → Chain Bridge** — every Georgetown leg.
   - Strict no-wake in the **Washington Channel** — every Wharf approach.
   - **6 mph posted limit on the Anacostia** (river entrance → Benning Rd) — every Navy Yard / The Yards / James Creek leg.

   The authored JSON flags these at segment level: `segments[].speed_constrained: true`. On flagged segments, `water_min` must render as **"indicative — subject to DC harbor speed rules"** — never a bare number. **NO crossing-time claims for Georgetown or Navy Yard appear anywhere in copy** until regulatory engagement resolves. A zero-wake hydrofoil gets no automatic exemption; do not soften this in copy.

2. **HQ2 honesty.** Amazon HQ2 / National Landing is **shuttle-tier** from Washington Sailing Marina (Daingerfield Island, ~2.5 mi). Copy may say "shuttle connection to National Landing" — **never imply a dock at HQ2 or a planned one.** The `daingerfield` stop renders with its `shuttle to HQ2` tag; the shuttle leg is ground, not water, and must not render as a water path.

3. **Security zones internal only.** 33 CFR 165.508 material (zones, blackout days, reasons) lives in `note_internal` only. It must never surface in the rendered DOM or copy.

4. **Standard gates (inherited from v2):**
   - `dock_track` / `note_internal` stripped from the rendered DOM — strip from the bundle, not just hidden.
   - No invented landings; `bp_gap` ledger for any unresolved BP.
   - All times **indicative** until Atlas geometry seals them.
   - Phase toggle defaults to **"At launch"**; Phase 2/3 render dimmed with "planned" styling.
   - LOI framing is **non-binding** everywhere.
   - **No dock-negotiation language** anywhere in rendered copy (no NPS-permit, berthing-terms, or lease talk).
   - Launch timing honesty: service **not before end-2027**; the map is coverage narrative, not a service promise.

5. **Watchlist & no_landing are render-exclusion lists.** `watchlist` entries (Belle Haven, Mount Vernon, Bladensburg) and `no_landing` entries (National Landing, Rosslyn, DCA, closed Buzzard Point Marina, JBAB/Poplar Point, etc.) must NOT appear as stations, stops, or map markers in any phase. Do not create a National Landing/HQ2 stop, Rosslyn stop, DCA stop, or Buzzard Point stop under any circumstances.

6. **Geometry notes for water_path work:** DC-1 rounds Hains Point between the Washington Channel and the main-stem Potomac; DC-2/DC-5/DC-7 enter the Anacostia past Hains Point; DC-6 and the National Harbor legs pass the **Wilson Bridge navigation channel** — route through the channel, not the fixed spans. All paths water-only: Potomac, Washington Channel, Anacostia, Boundary Channel, Piscataway Creek, Occoquan River as applicable.

## Acceptance (QA report must show)
1. Hub renders all 7 lines with **water-only geometry — zero land crossings**, including around Hains Point and through the Wilson Bridge channel; phase toggle working; interchange ring on `old-town-alexandria` (primary) and `the-wharf`; transfer chips correct.
2. Every `speed_constrained: true` segment renders its time as "indicative — subject to DC harbor speed rules"; grep of rendered copy shows zero crossing-time claims for Georgetown or Navy Yard.
3. Catchment panel numbers match the authored `catchment` array **exactly** (4→10 for the five Phase-1 anchors; 0→10 for Pentagon and HQ2-via-shuttle).
4. No `watchlist` or `no_landing` entry appears on the map or in the DOM in any phase state.
5. Internal fields absent from the built bundle (grep for `dock_track`, `note_internal`, `165.508`).
6. Registry has the `washington-dc` entry; `/employers/washington-dc` and alias `/dc-employers` both resolve; LOI POST works end-to-end.
7. 0 invented landings; `bp_gap` ledger populated with reason for any unresolved BP.
8. Screenshots: hub at each phase state (At launch · +Phase 2 · Full network), catchment panel open, one speed-constrained segment tooltip.
9. Registry untouched except the new entry + version bump; bay-area and new-york hubs unaffected.
