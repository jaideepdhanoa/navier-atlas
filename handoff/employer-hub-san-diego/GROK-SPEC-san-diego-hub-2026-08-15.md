# GROK SPEC — Employer Hub: San Diego Bay (new hub)
**Date:** 2026-08-15 · **Owner:** Tasklet (spec) / Grok (deterministic build) · **Merge gate:** Jaideep

## Mandate
Add a **new `san-diego` hub** to the existing employer-hub system in `jaideepdhanoa/navier-atlas` under `employer-hub/` — a **registry + template extension, NOT a rewrite**. Reuse everything the Bay/NY v2 build shipped: shared template, `employer-hub/registry.json`, `hubs/{hub}/hub.json`, phase toggle, line `type` styling (trunk/feeder/express/seasonal), interchange rings + transfer chips, catchment panel, trip planner, LOI intake. Canonical path/alias conventions unchanged: route `/employers/san-diego`, alias `/san-diego-employers`. San Diego is **ONE cluster** — no cluster fields, no cluster grouping UI.

## Inputs (this folder)
| File | What |
|---|---|
| `san-diego-hub-v1-stops-lines.json` | Tasklet-authored hub draft — 7 stops, 3 lines, phases, roles, catchment, watchlist, no_landing ledger, decision_ledger, gates, copy directives. **Authoritative.** |
| `../SAN-DIEGO-NODE-INVENTORY.md` | Source-verified node research (every landing cited; speed-zone and federal-waters findings; ops caveats) |

## Division of labor (standing)
- **Tasklet authored:** stops, lines, phases, roles, catchment counts, copy directives, gates, decision_ledger. Do not re-derive.
- **Grok owns (deterministic):** BP gazetteer ID-match → `resolved_bp_id`/`lng`/`lat` per stop; **water-only** `water_path` waypoints for every line; `water_min` per segment from sealed geometry; template work; registry entry; QA screenshots.
- **`routing` strings are build guidance only** — use them to shape `water_path` waypoints (channels, bridge spans, zones to stand clear of), then strip them: they must not appear in the built bundle or rendered DOM.
- **No invented landings.** Every stop maps to the exact named landing in `SAN-DIEGO-NODE-INVENTORY.md`. If a stop cannot be ID-matched to a real BP, add it to the `bp_gap` ledger in the hub JSON with reason and render it only from the inventory-named coordinates — never guess.

## Hub-specific requirements (hard gates — fail closed)

1. **SOUTH BAY SPEED HONESTY (the San Diego-defining speed gate).** The main channel and central bay carry **no general speed limit** for a passenger vessel (SDUPD Port Code §4.35(c)(3)) — mid-bay is genuinely fast water and copy may say so. Three constrained regimes bound the network:
   - **Posted 5 mph area, South San Diego Bay south of Loews Resort / Sweetwater Channel** — caps the first ~2–3 nm of every Chula Vista leg (pylon-marked wildlife-refuge water).
   - **5 mph in Glorietta Bay** — the Bridge Line's Coronado end.
   - **5 mph in the Bay Bridge mooring/roadstead area and designated anchorages** — route clear rather than through.

   The authored JSON flags these at segment level: `segments[].speed_constrained: true`. On flagged segments, `water_min` must render as **"indicative — subject to San Diego Bay speed rules"** — never a bare per-segment number. Whitelisted end-to-end ranges (always with an "indicative" qualifier): **South Bay Line ~30–40 min** (includes the 5 mph tail), **Point Loma Line ~15–25 min**. The **Bridge Line renders no numeric time claim at all.** Never imply a bay-wide speed limit exists; never hide the South Bay tail from the time model.

2. **INCUMBENT RESPECT (Flagship).** Flagship runs the Coronado ferry (free City-subsidized commuter runs at commute hours), a Convention Center↔Coronado shuttle, and the June 2026 Chula Vista↔Convention Center commuter ferry — and goes electric fall 2026. Hard consequences:
   - **NO Broadway↔Coronado line** exists in any phase — do not render, imply, or reserve it.
   - **Coronado Ferry Landing never renders as a station, stop, or marker** — it lives in `decision_ledger` only (lease in flux + incumbent = partner conversation first). The Coronado anchor is Glorietta Bay, Phase 3.
   - Zero displacement/head-to-head framing anywhere in rendered copy: no "faster than the ferry," no comparison tables, no operator criticism. Complement-and-add-seats language only, per the authored `copy` block.

3. **Navy honesty.** No military base is served dockside anywhere; base-adjacent access is bike/base-shuttle tier via public landings only, and none of that detail renders. All base names, installation headcounts, security-zone citations, and the shipyard shift-change material live in `note_internal` / `no_landing` / `decision_ledger` / `watchlist` only — never in the rendered DOM or copy. Rendered copy is limited to honest generic phrasing ("Coronado and South Bay employers").

4. **Render-exclusion lists.** `watchlist` entries (Navy Pier/Freedom Park, B Street Pier, Pepper Park, Cesar Chavez Park float), `no_landing` entries (all 8), and every `decision_ledger` item must NOT appear as stations, stops, or map markers in any phase. Do not create a Coronado Ferry Landing stop, Pier 32/National City stop, Barrio Logan stop, airport stop, or Mission Bay/Oceanside anything under any circumstances.

5. **Standard gates (inherited from v2):**
   - `dock_track` / `note_internal` / `routing` / `decision_ledger` stripped from the rendered DOM — strip from the bundle, not just hidden.
   - No invented landings; `bp_gap` ledger for any unresolved BP.
   - All times **indicative** until Atlas geometry seals them.
   - Phase toggle defaults to **"At launch"**; Phase 2/3 render dimmed with "planned" styling.
   - LOI framing is **non-binding** everywhere.
   - **No dock-negotiation language** anywhere in rendered copy (no Port-permit, berthing-terms, tideland, lease, or city-agreement talk — `port_single_landlord_internal` and `coronado_lease_internal` are internal context only).
   - Launch timing honesty: service **not before end-2027**; the map is coverage narrative, not a service promise.

6. **Geometry notes for water_path work (all paths water-only):**
   - SD-1 passes under the **Coronado Bridge navigation span** and holds the **marked channel through the posted South Bay 5 mph zone** (wildlife refuges and shoals outside the channel — never cut the pylon line).
   - Stand clear of the **33 CFR 165.1101 Naval Station security-zone waters off the 32nd St shore**, the **§165.1102 Point Loma shore zone**, **§334.870 restricted areas** (Bravo Pier 100-ft standoff; degaussing-station most-direct-transit; Ballast Point–Zuniga rules), and **§334.880 naval anchorages** — route in/near the marked channels, which are legally navigable end-to-end. None of this regulatory material renders.
   - SD-2 rounds the Shelter Island mole between the guest docks and America's Cup Harbor, then runs the north-bay main channel east via the Harbor Island basin to Broadway Pier.
   - SD-3 exits Glorietta Bay, crosses via the Coronado Bridge span, and stands clear of the Bay Bridge mooring/roadstead area.

## Acceptance (QA report must show)
1. Hub renders all 3 lines with **water-only geometry — zero land crossings**, through the Coronado Bridge navigation span and the marked South Bay channel, standing clear of the security-zone shores, restricted areas, and anchorages listed above; phase toggle working; interchange ring on `broadway-pier` (primary) and `fifth-avenue-landing`; transfer chips correct.
2. Every `speed_constrained: true` segment renders its time as "indicative — subject to San Diego Bay speed rules"; only the whitelisted end-to-end ranges (South Bay ~30–40 min, Point Loma ~15–25 min) appear as numbers, each with an "indicative" qualifier; grep of rendered copy shows **zero numeric time claims for the Bridge Line**.
3. **No Broadway↔Coronado line and no Coronado Ferry Landing station/marker anywhere**; grep of rendered copy for "Coronado Ferry Landing" = zero hits; zero head-to-head or displacement framing versus the incumbent ferry.
4. Catchment panel numbers match the authored `catchment` array **exactly** (2→6 for the three Phase-1 anchors; 0→6 for Point Loma/Shelter Island and Coronado/Glorietta Bay).
5. No `watchlist`, `no_landing`, or `decision_ledger` entry appears on the map or in the DOM in any phase state.
6. Internal fields absent from the built bundle — greps all zero: `dock_track`, `note_internal`, `routing`, `decision_ledger`, `165.1101`, `navy` (case-insensitive), `NASNI`, `NBSD`, `NASSCO`, `security zone`, `port_single`, `coronado_lease`, `TWIC` (case-sensitive — rendered copy legitimately contains the word "twice").
7. Registry has the `san-diego` entry; `/employers/san-diego` and alias `/san-diego-employers` both resolve; LOI POST works end-to-end.
8. 0 invented landings; `bp_gap` ledger populated with reason for any unresolved BP.
9. Screenshots: hub at each phase state (At launch · +Phase 2 · Full network), catchment panel open, the South Bay speed-constrained segment tooltip.
10. Registry untouched except the new entry + version bump; bay-area, new-york, and all other hubs unaffected.
