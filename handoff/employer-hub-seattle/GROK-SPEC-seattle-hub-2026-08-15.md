# GROK SPEC — Employer Hub: Seattle / Lake Washington & Puget Sound (new hub)
**Date:** 2026-08-15 · **Owner:** Tasklet (spec) / Grok (deterministic build) · **Merge gate:** Jaideep

## Mandate
Add a **new `seattle` hub** to the existing employer-hub system in `jaideepdhanoa/navier-atlas` under `employer-hub/` — a **registry + template extension, NOT a rewrite**. Reuse everything the Bay/NY v2 build shipped: shared template, `employer-hub/registry.json`, `hubs/{hub}/hub.json`, phase toggle, line `type` styling (trunk/feeder/express/seasonal), interchange rings + transfer chips, catchment panel, trip planner, LOI intake. This is a **two-cluster hub** — follow the `miami` hub pattern exactly: top-level `clusters` array, per-stop `cluster` field, per-line `cluster` field, and a top-level no-connector rule (here `no_intercluster_link`). Canonical path/alias conventions unchanged: route `/employers/seattle`, alias `/seattle-employers`.

## Inputs (this folder)
| File | What |
|---|---|
| `seattle-hub-v1-stops-lines.json` | Tasklet-authored hub draft — 14 stops (5 lake, 9 sound), 8 lines, two clusters, phases, roles, catchment, watchlist, no_landing + decision_ledger, gates, copy directives. **Authoritative.** |
| `../SEATTLE-NODE-INVENTORY.md` | Source-verified node research (every landing cited; regulatory verdict first; ops caveats; fail-closed unknowns) |

## Division of labor (standing)
- **Tasklet authored:** stops, lines, phases, roles, catchment counts, copy directives, gates. Do not re-derive.
- **Grok owns (deterministic):** BP gazetteer ID-match → `resolved_bp_id`/`lng`/`lat` per stop; **water-only** `water_path` waypoints for every line; `water_min` per segment from sealed geometry; template work; registry entry; QA screenshots.
- **`routing` extension (from Miami):** `segments[].routing` strings are Tasklet's geometry guidance for your `water_path` work (buffers, bridge navigation spans, traffic lanes to avoid). They are **build guidance only — strip them from the rendered bundle** (they are listed in `internal_fields_stripped_from_dom`).
- **No invented landings.** Every stop maps to the exact named landing in `SEATTLE-NODE-INVENTORY.md`. If a stop cannot be ID-matched to a real BP, add it to the `bp_gap` ledger in the hub JSON with reason and render it only from the inventory-named coordinates — never guess.

## Hub-specific requirements (hard gates — fail closed)

1. **TWO CLUSTERS, NO PHANTOM CONNECTOR (the Seattle-defining gate #1).** The Lake Washington and Puget Sound clusters are independent networks. **Zero cross-cluster segments** in any geometry, any phase — do not render, imply, dash, or "future-plan" a Lake↔Sound connector, and never route anything through the Ballard Locks. Reason (internal): locks are first-come queue-based, 10–15 min cycles best case with 1–4 hr documented waits, plus the blanket 7-kn Ship Canal. The map may show both clusters on one canvas; the trip planner must refuse cross-cluster itineraries.

2. **SHIP CANAL IS FORBIDDEN GEOMETRY (the Seattle-defining gate #2).** No `water_path` vertex may fall in the Ship Canal system: **Union Bay west of Webster Point, Montlake Cut, Portage Bay, Lake Union, Salmon Bay, the Ship Canal itself, or the Ballard Locks/approaches** (blanket 7-kn zone, SMC 16.20.130). No line touches this water; no South Lake Union or UW stop exists; **no SLU/UW service claim appears anywhere in rendered copy.** The SLU employer cluster (Amazon SLU, Google SLU, Fred Hutch, Gates Foundation) lives in internal fields only and must never surface as a served anchor.

3. **SHORE-BUFFER TIME MODELING.** There is no lake-wide speed limit — but every terminal approach crosses a slow shore buffer (7-kn/100-yd Seattle, 8-mph/100-yd King County, 8-kn Renton, 300-ft Bellevue/Mercer Island buoys, 200-yd Elliott Bay, 3-kn marinas). `water_min` on every segment must model these buffer legs, and **all times render as indicative until Atlas geometry seals them.** Whitelisted lake ranges (Bridge Bypass 12–15 · Boeing Line 25–30 end-to-end · Kirkland Direct 15–18) render with an "indicative" qualifier; **Sound-cluster lines render no bare numbers.** Never imply a lake speed limit exists, and never hide the buffer legs.

4. **EMPLOYER-TIER HONESTY.** Expedia (Elliott Bay Marina) and Boeing Renton/Southport (Coulon) are genuine walk-tier waterfront. **Amazon Bellevue / Downtown Bellevue = 15–20 min uphill from Meydenbauer — render as "longer walk / shuttle-tier," never walk-tier. Google Kirkland = ~0.9 mi inland — shuttle-tier, never "waterfront."** Carillon Point's Microsoft tag is a ground shuttle — never a water path, never a Microsoft dock.

5. **Internal-only material stripped from the built bundle (strip, not hide):** `dock_track`, `note_internal`, `routing`, and the entire `decision_ledger`. That removes: orca/SRKW protocol material (RCW 77.15.740 — internal ops only), all parks/port dock-permission and berthing-negotiation content (Coulon, Leschi/Lakewood, Marina Park, Seacrest, Luther Burbank, Jerisich, Port of Seattle/Kingston/Edmonds), incumbent dock-sharing posture, and the SLU/Pier-50/Tacoma-exclusion decisions.

6. **Render-exclusion lists.** `watchlist` (Kenmore, Port of Everett, Luther Burbank, Madison Park new-dock play), `no_landing` (UW/Union Bay, Madison Park today, Medina/Hunts Point/Yarrow Point, Microsoft Redmond, Meta Spring District, T-Mobile/Costco, Boeing Everett), and `decision_ledger` entries must NOT appear as stations, stops, or map markers in any phase. Do not create an SLU, UW, Madison Park, Pier 50, Colman Dock, Mercer Island, Kenmore, or Everett stop under any circumstances.

7. **Incumbent respect.** WSF / Kitsap Fast Ferries / King County Water Taxi are proven-market proof points and potential partners — copy may cite their ridership and the 2022 Des Moines pilot, but nothing may read as displacement or criticism. Colman Dock (WSF) and Pier 50 (KCWT/Kitsap) never render as Navier stations; Bell Harbor Pier 66 is the downtown gate.

8. **Standard gates (inherited from v2):** no invented landings + `bp_gap` ledger; all times indicative until sealed; phase toggle defaults to **"At launch"** with Phase 2/3 dimmed "planned"; LOI framing non-binding everywhere; **no dock-negotiation language** in rendered copy; launch timing honesty — service **not before end-2027**, map is coverage narrative, not a service promise.

9. **Geometry notes for water_path work (all water-only):** Bridge Bypass crosses mid-lake between the SR-520 and I-90 bridges (no bridge crossing). Kirkland↔Meydenbauer and Carillon↔Leschi cross the **SR-520 floating bridge at its navigable elevated span**; Meydenbauer↔Coulon runs the **East Channel east of Mercer Island through the fixed I-90 East Channel bridge's navigation span** — verify span locations against chart; floating bridge pontoons are barriers everywhere else. Route around (never through) marked swim/park restricted areas. Sound cluster: Elliott Bay legs stand off the 200-yd pier-line buffer and clear of WSF/Kitsap/KCWT lanes at Colman/Pier 50; Sound Gate and Kingston Line keep clear of the WSF Bainbridge and Edmonds–Kingston crossing lanes; Narrows Shuttle routes Gig Harbor → Tacoma Narrows → Thea Foss Waterway with **no link to the Seattle group**.

## Acceptance (QA report must show)
1. Hub renders all 8 lines with **water-only geometry — zero land crossings**, correct cluster assignment, floating-bridge crossings only at navigable spans; phase toggle working; interchange ring on `meydenbauer` (primary, lake) and `bell-harbor` (sound), with `leschi` ringed as an interchange at full network; transfer chips correct.
2. **Zero Ship Canal incursions:** programmatic check of every `water_path` against the forbidden water list (Union Bay W of Webster Point, Montlake Cut, Portage Bay, Lake Union, Salmon Bay, Locks) = 0 vertices.
3. **Zero cross-cluster segments** in any phase; trip planner refuses Lake↔Sound itineraries; no connector rendered or implied.
4. Whitelisted lake times render with the authored ranges + "indicative" qualifier; grep of rendered copy shows **zero bare time numbers on Sound-cluster lines** and zero SLU/UW/South Lake Union service claims.
5. Catchment panel numbers match the authored `catchment` array **exactly** (2→6 for the two Sound anchors; 3→4 for the three Lake anchors).
6. No `watchlist`, `no_landing`, or `decision_ledger` entry appears on the map or in the DOM in any phase state.
7. Internal fields absent from the built bundle — grep for `dock_track`, `note_internal`, `routing`, `decision_ledger`, `orca`, `77.15.740`, `parks_dock_permission`, `KMC 14.36`: all zero hits.
8. Employer-tier grep: "walk-tier" never co-occurs with Amazon Bellevue or Google Kirkland; "waterfront" never describes Google Kirkland; Microsoft renders only as a shuttle tag.
9. Registry has the `seattle` entry; `/employers/seattle` and alias `/seattle-employers` both resolve; LOI POST works end-to-end; 0 invented landings; `bp_gap` ledger populated with reason for any unresolved BP (likely candidates: Eagle Harbor berth, Southport alternate gate).
10. Screenshots: each phase state (At launch · +Phase 2 · Full network) **per cluster**, catchment panel open, one lake-time tooltip showing the "indicative" qualifier, and the two-cluster full-canvas view showing no connector.
11. Registry untouched except the new entry + version bump; bay-area, new-york, washington-dc, and miami hubs unaffected.
