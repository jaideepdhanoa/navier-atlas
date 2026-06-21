# PR #65 Grok Execution Report — 2026-06-21

- Lane: `grok/execute_pr65_yassir_caribbean`
- Partners: yassir, caribbean-mobility

## Summary

| Gate | Count |
|------|------:|
| Country refs promoted | 6 |
| Yassir corridors sealed | 11 |
| Yassir corridors held | 6 |
| Algeria corridors added | 3 |
| Algeria display routes | 3 |
| Caribbean corridors sealed | 4 |
| Caribbean corridors held | 1 |
| Yassir cards sealed | 13 |
| Caribbean cards sealed | 0 |
| Finance cascaded | yassir, caribbean-mobility |

## Country references promoted

- Algeria
- Bahamas
- Puerto Rico
- U.S. Virgin Islands
- British Virgin Islands
- Barbados

## Post-lane QA (after relink + journey field repair)

| Partner | Page QA | Featured geom | Journey geom |
|---------|---------|---------------|--------------|
| yassir | **PASS** | 15/24 | 5/8 |
| caribbean-mobility | **PASS** | 72/96 | 0/15 (linked; held-null OK) |

## Algeria mint (full batch)

- Cities minted: `algiers-algeria`, `bejaia-algeria`, `oran-algeria`, `mostaganem-algeria`
- Routes minted: 3 (Algiers Bay, Oran–Mostaganem, Béjaïa–Alger HSC)
- Long HSC leg flagged `_land_crossing_review` where coastal solver crosses headlands

## Deck Studio

- Local validate + QA receipts: see `PR65-DECK-STUDIO-GAP-REPORT-2026-06-21.md`
- Live Slides bind blocked: no `GOOGLE_TOKEN_PATH` in environment

## Artifacts

- `handoff/partner-map-model/algeria-yassir-mint-report.json`
- `partner-pitch/partners/yassir.json`
- `partner-pitch/partners/caribbean-mobility.json`
- `data-clean/partners/yassir.json`
- `data-clean/partners/caribbean-mobility.json`
- `finance/recal/agg-yassir.json`, `finance/recal/agg-caribbean-mobility.json`
- `finance/growth-yassir.json`, `finance/growth-caribbean-mobility.json`
