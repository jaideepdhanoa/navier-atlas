# PR #65 economics sheet notes — 2026-06-21

## Why four decks were held-null

Deck Studio binds `economics_url` from `finance/economics_url_map.json`, which mirrors `finance/PARTNER-SHEET-IDS.json` (LB-83 transparent-sheet registry).

| Partner | Root cause |
|---------|------------|
| yassir | Had `agg-yassir.json` + local `yassir_unit_econ.xlsx` from PR #65 Grok lane, but **never registered** in `PARTNER-SHEET-IDS.json` — no stable Drive ID for deck chip / `model_link` wiring |
| caribbean-mobility | Same — `agg-caribbean-mobility.json` existed, no LB-83 entry |
| adani-ports | **No finance engine footprint** — zero rows in `corridors.json`, no `agg-adani-ports.json`. Deck lane is proposal-prep only |
| reliance-industries | Same as Adani — no corridors/aggregate; `economics_url: null` in partner JSON is correct |

Creating empty Google Sheets for Adani/Reliance would violate null-beats-confidently-wrong.

## Resolved today (Grok)

```bash
cd finance
python3 create_partner_sheets.py          # registered yassir + caribbean-mobility
python3 build_transparent_sheet.py --partner yassir --out _sheet_out/yassir_unit_econ.xlsx
python3 build_transparent_sheet.py --partner caribbean-mobility --out _sheet_out/caribbean-mobility_unit_econ.xlsx
python3 drive_upload.py _sheet_out/yassir_unit_econ.xlsx <yassir_sheet_id>
python3 drive_upload.py _sheet_out/caribbean-mobility_unit_econ.xlsx <caribbean_sheet_id>
```

| Partner | Sheet ID | URL |
|---------|----------|-----|
| yassir | `1ba9Zpap5hPAehDKFHgk2PwRq4xStr2rx_z1LGSY52Q4` | https://docs.google.com/spreadsheets/d/1ba9Zpap5hPAehDKFHgk2PwRq4xStr2rx_z1LGSY52Q4/edit |
| caribbean-mobility | `1J9rb-rAXkLnJPrKO8WhG7bLkofG-IB5En6hrjnwDyt0` | https://docs.google.com/spreadsheets/d/1J9rb-rAXkLnJPrKO8WhG7bLkofG-IB5En6hrjnwDyt0/edit |

Wired into: `partner-pitch/partners/*.json`, `data-clean/partners/*.json`, `deck-studio/decks/*/deck.config.json`.

## Still held-null — Tasklet path

For **adani-ports** and **reliance-industries**:

1. Seal/port geometry → scoped corridors in `finance/model/corridors.json`
2. `aggregate.py --partner <slug>` → `finance/recal/agg-<slug>.json`
3. `build_transparent_sheet.py --partner <slug>`
4. `create_partner_sheets.py` entry + `drive_upload.py` in-place publish
5. Add to `economics_url_map.json`; Grok re-runs deck economics bind