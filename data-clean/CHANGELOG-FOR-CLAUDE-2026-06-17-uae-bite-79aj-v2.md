# Gold #79aj-v2 — UAE bite work, forward delta on #79ai

**Base:** #79ai canonical (5,199 routes)
**This seal:** #79aj-v2 (5,199 routes, no new mints; 40 UAE routes geometry-patched)

## Patches applied

1. **LB-210b** — `rn-creek-harbour-dubai-harbour-79ai` distance_nm fixed to 26.9nm
2. **Emirates Palace → Saadiyat Beach Club** — 7-WP Lulu west-channel path (sinuosity 1.05, 10.1nm)
3. **Dubai Harbour Marina → Al Khan Lagoon** — squiggle resolved (sinuosity 1.36)
4. **+37 other UAE coastal routes** — geometry forward-patched from the (rejected) #79aj for sinuosity/no-cross compliance against parity-v2 `uae_gulf_land.wkb` overlay

## Explicitly NOT included from rejected #79aj

- 192 polluting "new mints" from a prior staged delta (not part of LB-208/209/210/Sharjah/headline bite work)
- 19 `ics-*` defects from the (also rejected) #79ak

## Banked for next seal

- LB-208a: Palm 9 intra-hops need per-route hand-authored channel selection
- LB-211: 15 of 20 residual-band routes need seaward candidates
- LB-221 follow-up: Hudayriyat/Khalifa Port polygons in `uae_gulf_land.wkb`
- LB-224: BP seaward-nudge — needs BP-coord store design

## SEAL bytes-truth

All `file_hashes` + `blobs` recomputed from actual on-disk bytes (LB-212 pattern).
