# GROK SPEC — Employer Hub v2: Metro-Style Network Expansion (Bay Area + New York)
**Date:** 2026-08-13 · **Owner:** Tasklet (spec) / Grok (deterministic build) · **Merge gate:** Jaideep

## Mandate
Rebuild both employer-hub microsites from isolated corridors into **connected, metro-style networks**, per Jaideep 2026-08-13. Build **on top of the shared template + registry you already shipped** (`employer-hub/registry.json`, `hubs/*/hub.json`, water-only waypoints, LOI intake) — this is a v2 data + template-extension pass, not a rewrite. Canonical paths and aliases stay unchanged.

## Inputs (this folder)
| File | What |
|---|---|
| `inputs/NETWORK-V2-ARCHITECTURE.md` | The approved network design — line structure, phasing, interchange logic, catchment tables, honesty flags. **Authoritative.** |
| `inputs/bay-area-hub-v2-stops-lines.json` | Bay v2 stops/lines/catchment draft (17 stops, 6 lines) |
| `inputs/new-york-hub-v2-stops-lines.json` | NY v2 stops/lines/catchment draft (33 stops, 9 lines incl. CT + Glen Cove + Hamptons seasonal) |
| `inputs/BAY-NODE-INVENTORY.md` / `inputs/NY-NODE-INVENTORY.md` | Source-verified node research (79 landings, every row cited) |
| `inputs/MARINA-GAP-CHECK.md` | Why Palo Alto/Foster City/Fremont/Long Beach stay OFF the map |

## Division of labor (standing)
- **Tasklet authored:** stops, lines, phases, roles, catchment counts, copy directives, gates. Do not re-derive.
- **Grok owns (deterministic):** BP gazetteer ID-match → `resolved_bp_id`/`lng`/`lat` per stop; **water-only** `water_path` waypoints for every new line; `water_min` per segment from sealed geometry; template extensions; QA screenshots.
- **No invented landings.** Every stop maps to the exact named landing in the inventories. If a stop cannot be ID-matched to a real BP, add it to a `bp_gap` ledger in the hub JSON and render it only from the inventory-named coordinates — never guess.

## Template extensions (shared — both hubs inherit)
1. **Line `type`:** `trunk | feeder | express | seasonal` — visual weight: trunks heavy, feeders lighter, express dashed-solid, seasonal dotted with a ☀ badge.
2. **Phasing:** every stop and line carries `phase` (1/2/3). UI gets a **phase toggle** (`At launch · +Phase 2 · Full network`) defaulting to Phase 1. Phase 2/3 render dimmed with "planned" styling — the map must never imply day-one service everywhere.
3. **Interchanges:** `role: interchange*` stops render with the metro double-ring; a small transfer chip lists lines that call there.
4. **`tag` support:** e.g. Mission Bay "opens 2027" — solid hub styling + tag pill, NOT dashed. (Jaideep: launch is end-2027 at earliest, so Mission Bay is a day-one hub.)
5. **Catchment panel (new section):** per employer anchor render "X stations at launch → Y at full network" from the `catchment` array, with a tap-to-highlight of reachable stations. This replaces the corridor-list pitch as the hero proof block.
6. **Seasonal overlay:** NY-S renders as its own layer, toggleable, with the approved fares ($625 Sag Harbor · $645 Montauk) shown as premium chips.
7. **Locked numbers, calculator, LOI flow, launch-trigger copy: unchanged.** Seat economics still gate corridor launch (60–72 committed seats); the network map is coverage narrative, not a service promise.

## Hard gates (fail closed)
- **Dock status never surfaces externally.** `dock_track`, `note_internal`, and the LGA dock situation are internal fields — strip from rendered DOM, not just hidden.
- **Williamsburg stops stay HELD** — do not add to NY hub in any phase.
- **NY-C honesty gate:** no raw-speed claims vs Metro-North anywhere in copy. Positioning: door-to-door for waterfront-origin riders + guaranteed working seat.
- **Monmouth County (Seastreak market):** not a station in any phase.
- All times marked **indicative** until Atlas geometry seals them.
- `stop_migrations` (Bay): split `alameda-jack-london` → `oakland-jls` + `alameda-main` without breaking existing line references or LOI records.

## Acceptance (QA report must show)
1. Both hubs render all v2 lines with **water-only geometry** (0 land crossings), phase toggle working, interchange rings + transfer chips correct.
2. Catchment panel numbers match the `catchment` arrays exactly.
3. 0 invented landings; `bp_gap` ledger for any unresolved BP with reason.
4. Internal fields absent from rendered DOM (grep the built bundle for `dock_track`, `note_internal`).
5. Aliases `/bay-employers` and `/ny-employers` still resolve; LOI POST still works.
6. Screenshots: each hub at each phase state + seasonal toggle on/off.
7. Registry untouched except version bumps.
