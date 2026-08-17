# Invest v6 gate results (DESIGN-AUDIT-V6)

## Binding source
PR #387 commits 8388bf4…7c8218a + binding comment on PR #388 (v6 audit).

## Doctrine applied
- Slide-stage CSS: stage-section, stage-grid, stage-kicker, h2 clamp(36px–60px) max 2 lines (22ch)
- Reveal defaults **visible** (`reveal-pending` only when motion enabled)
- section-inner / media-inner retained (clip scan still 0)

## New assets wired
| Asset | Use |
|---|---|
| traction-foundry-floor | Traction hero |
| control-wireframe-clean | Control centerpiece + callouts |
| gulf-hero | Gulf stage |
| cargo-play-skyline / shipscale / wedge | Cargo stages |
| n45-mobility-render | Ladder N45 |
| n30-pioneer | Ladder N30 + Quanta |
| fleet-wireframe-n80 | Ladder N80 (n80-render-v1 pending approval) |
| shipscale-hero | Ladder N180 + ship scale stage |
| logos/* | Coastal-Network Model players |

## QA (local)
- Clip scan 1280/1440/2560: **0** failures
- Manifest string scan: no "opener full-bleed" / "_internal" in DOM text
- G3 JSON: clean
- Network Shift canvas + setNetworkMix present

## Not fully done (scope / gates)
- Live Atlas embed for pipeline (kept world-pipeline-map plate; Atlas overlay is follow-up)
- Three-costs full deck morph pair (improved layout; not full two-stage morph)
- FY26–30 multi-year ramp chart (contract has FY30 chips only — native metrics charts ship without invented series)
- N80 photoreal tab gated until Jaideep approves n80-render-v1
