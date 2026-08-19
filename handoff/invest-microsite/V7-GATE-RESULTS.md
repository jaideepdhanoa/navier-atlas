# V7 gate results — 2026-08-17

Tasklet tip commits reviewed:
- `39a94007` money FY26–FY30 ramp series
- `f40964e1` N80 render approval (message; tip assets.json had regressed ladder paths — rebased onto v6.1)
- `ae9130b5` v6 status addendum (morph + Atlas embed v1-blocking)

## Shipped
1. **Money ramp** — `native-line-charts` from money v2: revenue / EBITDA / fleet, exact contract points (10.5→512.1, −11.8→127, 14→567). FY30 stat-band secondary.
2. **N80** — `n80-render-v1.png` photoreal on ladder tab + `RENDER — IN DEVELOPMENT` chip.
3. **Three-costs morph** — sticky two-stage scroll (costs pillars → lever columns); reduced-motion shows both static.
4. **Live Atlas pipeline** — MapLibre dark basemap + 334 atlas cities + pipeline nodes; row hover/focus highlights node. Plate fallback for reduced-motion / JS-off / load fail.

## Gates
- Clip-scan 1280/1440/2560: **0 failures** (`CLIP-SCAN-V5.json`)
- Headless DOM: ramp values {10.5, 512.1, −11.8, 127, 567}; costs-morph present; 12 pipe rows; N80 meta + render chip
- Screenshot: `screenshots/v7-full-1440.png`

## Note on Tasklet assets tip
`f40964e1`/`ae9130b5` assets.json reset ladder to pre-v6 paths. Implementation keeps **v6.1** one-home map with N80 approved path only.
