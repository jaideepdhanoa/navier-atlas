# Tasklet punch list — invest round-6i (`seriesb/invest-microsite-2026-08-16`)

**From:** Grok review of tip `a34dc3ba` vs `origin/main`  
**Date:** 2026-08-21  
**Verdict:** Financials in `money.json` v4 look solid — **please do not treat the branch as merge-ready** until the items below are cleaned. Several are out-of-scope regressions relative to the stated “515 hulls + money v4” delta.

---

## Please fix on the branch (blocking)

### 1. Money chapter title (`money.json` · `operating-plan`)
`operating-plan` lost `"title": "The Ramp, Year by Year"`.  
`/invest` renderer still assumes that title lives on the KPI `stat-band` section, not on `ramp-charts` (which intentionally does not paint `s.title`).

**Ask:** Restore the title on `operating-plan`, **or** confirm you want a paired renderer change (we can do that on our side once you pick).

### 2. The Round column headings (`money.json` · `the-round` ↔ `invest.js`)
New column titles:
- `$20M SERIES B-1 — CLOSING SEPTEMBER 2026`
- `$100M SERIES B-2 — TARGETING Q4 2026`

do not match the legacy eyebrow parser (`NOW` / `18–24 months` / special-case `$10M SERIES B-1`). Result on render:
- authored timing eyebrows never appear
- title-case turns **`$20M` → `$20m`**, **`$100M` → `$100m`**

**Ask (preferred):** Author separate fields, e.g. `eyebrow` + Title Case `title` (`$20M Series B-1` / `Series B Program`), matching your own `render_notes`.  
**Alt:** We extend the parser — say which you want.

B-2 use-of-funds **$45M + $28M + $27M = $100M** ✓ — keep.

### 3. Maldives regressions (`gtm.json`) — out of stated 6i scope
Commit message says only the 515-hulls line changed in `gtm.json`, but the same commit also:
- strips Maldives `press[].url` (WSJ / Wallpaper / Robb Report become non-links)
- deletes the entire `players` / `players_label` strip

**Ask:** Restore `players` / `players_label` and the three press URLs from `origin/main`. Keep only the intentional market-floor edit (`515` / `<8%`).

### 4. `coastal-network-model` resurrected (`gtm.json`)
Section was deleted on main as redundant with Maldives + players. It is **not** in `TEASER_EXCLUDE`, so it returns on both `/invest` and `/teaser`. Four-role renderer also drops `earns`.

**Ask:** Delete `coastal-network-model` again unless product deliberately reopened it (if so, say so + teaser policy).

### 5. Contact flip still VERIFY (`money.json` finale / go-deeper)
`investors@navierboat.com` → `sampriti@navierboat.com` with `_internal` still noting `VERIFY-CONTACT: confirm … before ship`. Outside GROK-ROUND-6I stated deltas; ships on `/teaser` go-deeper too.

**Ask:** Explicit approval to ship `sampriti@`, **or** revert to `investors@` and clear/update the VERIFY note.

### 6. Defense `click-to-play` vs renderer (`gtm.json`)
`secondary_videos[].behavior: click-to-play` (+ rules that only the lead autoplays), but `defense-panel` in `invest.js` still always emits `muted … autoplay`.

**Ask:** Revert contract wording to autoplay to match renderer, **or** request a renderer change (we can implement).

---

## Please also update (non-blocking but will fail gates)

### 7. `_qa-contracts.ts` golden spots
Still requires `$512M`, `567`, `$10M Series B-1`, `$100-150M+`, appendix `$127M EBITDA`. After v4 those are gone from contracts → QA will fail / teach wrong goldens.

**Ask:** Retarget spots to `$571M`, `515`, `$20M Series B-1`, `$100M Series B-2` / `$120M` program.

### 8. Dead / duplicate binaries on the branch
- `deck-studio/assets/series-b/photos/cover-hero-loop.gif` (~23MB) — no in-repo reference found  
- `deck-studio/assets/series-b/photos/team-kenneth-jensen.png` (~5MB) — Kenneth already exists for invest at `handoff/invest-microsite/assets/deck/team-kenneth-jensen.png`  
- `deck-studio/assets/finmodel/*-v361.png` — OK as **deck-studio reference only** (not wired into `/invest`; PNG ban holds). Confirm intentional.

**Ask:** Drop or wire the GIF/headshot restore so we do not carry ~28MB of unreferenced weight.

### 9. Go-deeper closing-image notes
`treatment` / `render_notes` reverted toward “full-bleed solo plate” while live renderer still does equal-tile-beside-film. Align notes with shipped layout (or flag a paired CSS change).

### 10. Trailing newline
`gtm.json` lost its final newline — restore for cleaner diffs.

---

## What looks good (no action)
- `money.json` v4 Board Plan figures: **$571M / 7% / 515**, ramp series, **$20M B-1 + $100M B-2 = $120M**
- Old raise/ramp firewall strings cleared from money/gtm (`$10M`, `100–150`, `512M`, `567`)
- Finmodel PNGs not wired into microsite charts

---

## Suggested reply shape from Tasklet
For each of **#1–#6**, either:
1. push a fix commit on `seriesb/invest-microsite-2026-08-16`, or  
2. one-line decision (“revert X” / “Grok owns renderer for Y”).

Once 1–6 are clean we will implement any agreed renderer follow-ups and land round-6i on `main`.
