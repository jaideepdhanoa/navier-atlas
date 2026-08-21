# /defense v1 — Grok build notes (2026-08-21)

## Source
Tasklet PR #390 (`feat/defense-microsite-v1` @ `7a201a2`) — contract + Plainview archival + launch film.

## Built
- Route: `/defense` (noindex, unlisted; middleware password **`quanta`**, overridable via `DEFENSE_PASSWORD`)
- Renderer: `defense/defense.js` + `defense/defense.css` (invest visual system)
- Build: `scripts/build-defense.mjs` (wired into `build-site.mjs`) with **fail-the-build** word-bounded leak scan
- Asset path fix: `defense-sofweek-armed` / `defense-sas-officers-looking` → `.jpg` (files on main)

## QA receipt
See `qa/QA-RECEIPT-v1.json` + `qa/screenshots/` (≥12 named shots at 1440; field/team/plainview at 1280/2560).

| Gate | Result |
|---|---|
| Leak scan (rendered) | CLEAN |
| YouTube embed | none |
| Links to /invest or /teaser | none |
| robots noindex | yes |
| Launch film click → audio on | muted=false, playing |
| Advisor bio links | LeClair navy.mil + Cederholm Wikipedia |
