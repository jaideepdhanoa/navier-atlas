# Invest v5 gate results (DESIGN-AUDIT-V5)

## P0-1 Clipping scan
Command: `node scripts/invest-clip-scan.mjs http://127.0.0.1:8799/invest`

| Width | count left&lt;24 | minLeft |
|------:|----------------:|--------:|
| 1280 | **0** | none |
| 1440 | **0** | none |
| 2560 | **0** | none |

Full JSON: `CLIP-SCAN-V5.json`

## P0-2 Network Shift
- Source: `docs/invest/reference-impl/network-shift.html` (Tasklet d59f244)
- Ported to `invest/network-shift.js` — drawing geometry unchanged
- API: `window.setNetworkMix(m)` bound to `.ns-pin` scroll (0→1 by ~70% through pin)
- Toggle pills retained as override
- Chips from `claim.json` panel_before / panel_after verbatim
- Screenshot: `screenshots/v5-desktop-ns-b.png`

## P0-3 Backed by
- Typographic row from `claim.json` `backers_label` + `backers_line` (Cut s6 names)
- Gold separators; no smudge logos

## P1-4 Money charts
- Chart PNGs removed from DOM (`chartPng: false`)
- Native SVG: operating-plan metrics bars + margin bar from money contract stats only

## Smoke
- section-inner count ~34, media-inner ~8
- canvas present, setNetworkMix is function
