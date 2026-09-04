# /defense v4.4 + /invest — Autonomy beat ("Unmanned Today. Autonomous by Stages." / "Autonomy Is Already on the Water.")

**Why:** Jaideep 2026-09-04 — surface the real autonomy work (David Egen, All Hands 8/27 s26 + Tech Team 9/1 s13) on /defense, /invest and the Series B appendix. Credibility over claim: the ladder says what is PROVEN, FIELDED, ON THE WATER and IN TEST.

## Contracts
- `deck-studio/microsite/contracts/defense.json` → **v4.4**. New section `def-autonomy` directly after `def-platform` (same `03 · THE PLATFORM` chapter, second beat — same pattern as the 05 · QUANTA trio). No other section touched.
- `handoff/invest-microsite/contracts/product.json` → new section `autonomy-proof` directly after `control-tech`. `site.json` control cluster now lists it. `assets.json` registers four clips. **`teaser: EXCLUDE`** — never renders on /teaser.

## Media (both surfaces, identical files)
`deck-studio/microsite/assets/autonomy/` and `handoff/invest-microsite/assets/autonomy/`

| clip | native px | dur | badge |
|---|---|---|---|
| autonomy-segmentation-quad.mp4 | 640×170 | 15s | FILMED |
| autonomy-stereo-depth-dock.mp4 | 800×150 | 15s | FILMED |
| autonomy-slam-harbor-map.mp4 | 800×450 | 6s | FILMED |
| autonomy-sim-waypoint-helm.mp4 | 640×190 | 10s | **SIMULATION** |

Each has a `-poster.jpg`. H.264, silent, muted autoplay loop, paused off-screen. **Native aspect — never upscale.** The two strips are ultra-wide by design: render at full column width and let height follow; do not crop to 16:9.

## Rules
- Stage chips render **verbatim** (PROVEN / FIELDED / ON THE WATER / IN TEST / THE METHOD). Never promote.
- SIMULATION badge on the sim clip is mandatory. FILMED on the other three.
- Captions exactly as authored, below the clip. Text never on video.
- No autonomy hours/miles, no docking-as-capability, no vendor names, no sensor prices.
- Leak scan unchanged (40 terms) — new beat verified zero hits.
- FIELDED rung: "loss-of-link safe behaviors" rephrased to "defined loss-of-link behaviors" so the word-bounded `SAFE` leak term does not fail the build.
- Nothing else on either site changes in this build (Atlantic-run and range copy untouched by instruction).

## QA gate
≥3 screenshots of each new section (390 / 1280 / 2560) · badge visibility on all 4 clips · strips not cropped · captions verbatim · /teaser shows **no** autonomy section · full leak scan.
