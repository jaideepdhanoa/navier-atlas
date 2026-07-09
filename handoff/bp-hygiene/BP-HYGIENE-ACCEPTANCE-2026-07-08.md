# BP Hygiene — Post-Reseal Acceptance Check (2026-07-08)

**Verdict: NOT ACCEPTED — 361 residual flags (target: 0).** Grok apply-pass required.

Scanner: `bp_hygiene.py` re-run against sealed `data-clean/ROUTES.json` @ main `b4e49263` (4,126 unique corridor BPs).

## Residuals vs pre-reseal register (2026-07-06)

| Disposition | Pre-reseal | Post-reseal | Resolved | Newly flagged |
|---|---|---|---|---|
| DROP_junk | 43 | **48** | 18 | 23 |
| RELABEL_aggregate | 1 | **1** | 0 | 0 |
| RETAG_city_mismatch | 208 | **209** | 149 | 150 |
| DUP_coord | 154 | **103** | 122 | 71 |
| **Total** | 406 | **361** | | |

## Reading

- **DUP_coord is the only category the reseal genuinely improved** (154 → 103).
- **RETAG churned but did not shrink** (149 resolved, 150 newly minted) — reseal passes keep minting BPs with wrong `city_id` stamps. Worst offenders: Batam terminals stamped `jakarta-indonesia` (~858 km off), Bodrum/Çeşme stamped `istanbul-turkey`, Old Doha Port stamped `dubai-uae`. Consistent with the known WS-4 spatial-anchor mis-stamp defect — the retag fix must go into the **minting path**, not just data cleanup, or the count will regrow every pass.
- **DROP_junk grew** (43 → 48): new junk BPs entered via the UAE emirates sourcing wave (jet-ski operators, LLC trading companies, medical centers, helipads, seaplane bases).

## Scanner fix in this pass (false-positive rescue)

The junk regex previously caught **legitimate marine transit piers**: "…Water Bus Station" (Dubai RTA), "Waterbus Station/Stop" (Ho Chi Minh, Rotterdam), "Harbour Bus Stop" (Copenhagen). Regex now word-bounds `bus` and excludes `water/harbour/harbor` prefixes. 7 real piers rescued from the drop list; the only remaining bus-labeled junk flag is a genuine land bus terminal (Phuket Bus Terminal 2).

## Grok apply-pass (operating model: Tasklet flags, Grok applies, nobody invents a pier)

1. **DROP_junk (48):** remove BP + drop/reroute corridors touching them (junk endpoints ⇒ corridor is junk too unless other endpoint pairs to a real neighbor pier).
2. **RETAG_city_mismatch (209):** restamp `city_id`/labels from geometry (register carries nearest-centroid suggestion per BP). Also patch the WS-4 minting path so new BPs stamp from spatial anchor, not batch context.
3. **DUP_coord (103):** merge exact-coordinate duplicate BPs to one canonical id; rewire corridors.
4. Re-run `bp_hygiene.py` post-apply — acceptance = 0 residual.

Register: `BP-CLEANUP-REGISTER-2026-07-08.json` (same folder). No invented corrections — null/flag beats wrong.
