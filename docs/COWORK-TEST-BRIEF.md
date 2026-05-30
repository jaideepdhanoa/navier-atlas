# Claude Cowork — Test Brief (round 2)
_2026-05-30 · re-test after the route-render fix ships_

**URL:** https://navier-atlas.vercel.app · **Role:** demanding first-time partner-facing viewer; observe-and-report only.

## Why round 2
Round 1 was excellent and surfaced one blocker that masked everything: **F-01 — route lines never rendered**
(MapLibre rejected the route line layers). Claude Code is fixing F-01, F-02 (camera deep-links), and the
layout/declutter items. Most route-correctness checks were therefore **blocked** last round. This round
re-runs them now that lines should draw.

## Gate to start (do this first)
1. Open site → click **Singapore** → confirm **route lines now draw** (Pioneer II solid + Quanta-LR amber dashed).
   - If still no lines → STOP, report "F-01 not resolved" — the rest stays blocked.
2. Confirm camera deep-link works: paste `…/#camera=103.850,1.290,12.00` → should land on Singapore (F-02).
   - If it works, **cite all findings by camera deep-link** this round (round 1 had to use action paths).

## The 5 previously-blocked route-correctness checks (priority)
For Singapore, Dubai, Abu Dhabi (deep) + Bali, Phuket (single pass):
1. **Land-crossing** — does any route line cross over land/islands? (Tasklet gates 0/N, but verify visually.)
2. **Dangling/floating ends** — does every line terminate on a real marker (BP/city), not empty water?
3. **Curve quality** — marine-plausible smooth curves vs jagged/over-clipped; smoothing must not re-clip land.
4. **Trunk-vs-capillary density** — do high-demand trunks read heavier than local capillaries? Does it feel like a network?
5. **Trip-purpose colour** — commuter/business/tourism/luxury/local/mixed legible per the legend.

## Also re-verify (round-1 findings)
- F-04 legend↔map parity (every swatch maps to something drawn) · F-05 toggles now visibly add/remove lines.
- F-06/F-07/F-08 first-load layout (network is hero; stats not occluded; side panel context-correct at city zoom).
- F-10 Singapore city-dot vs ferry-glyph declutter · F-09 orphan dots gone (lines connect them).
- F-11 route count now **stable** across reloads (should equal `SEAL.json` count).
- F-13 cold-load perf on a real device/network.

## Data-side spot-checks (flag to Tasklet, not Claude)
- **Boarding-point placement (F-03)** — Tasklet is running a BP-on-water gate. Spot-check that previously-inland
  pins are now on water: Dubai (no ferry terminal in the street grid; marinas on the Creek), Abu Dhabi (no hotel
  jetty at Khalifa City), Phuket (no ferry triangle near Thalang). Report any remaining inland marine pins.

## Deliverable
Same format as round 1: ranked findings with severity + lane (`[RENDER]` = Claude Code, `[DATA]` = Tasklet),
reproduction path, and per-market partner-ready verdicts (Grab/Careem/RTA/ITC/LTA-MPA).
