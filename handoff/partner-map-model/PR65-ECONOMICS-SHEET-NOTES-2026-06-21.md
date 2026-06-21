# PR #65 economics sheet notes — 2026-06-21

## Why four decks were held-null

Deck Studio binds `economics_url` from `finance/economics_url_map.json`, which mirrors `finance/PARTNER-SHEET-IDS.json` (LB-83 transparent-sheet registry).

| Partner | Root cause |
|---------|------------|
| yassir | Had `agg-yassir.json` + local `yassir_unit_econ.xlsx` from PR #65 Grok lane, but **never registered** in `PARTNER-SHEET-IDS.json` — no stable Drive ID for deck chip / `model_link` wiring |
| caribbean-mobility | Same — `agg-caribbean-mobility.json` existed, no LB-83 entry |
| adani-ports | **LB-257 inheritance gap (fixed 2026-06-21)** — proposal geometry sealed via `india_corporate` / Rapido spine, but finance lane had not run scoped cascade + LB-83 publish |
| reliance-industries | Same — inherit India mobility corridor economics; operator narrative differs |

**Correction:** Adani/Reliance do **not** point at Rapido's sheet URL. They inherit Rapido's **scoped corridor rows** (LB-257), re-tagged to `adani-ports` / `reliance-industries`, then get **partner-owned** transparent sheets.

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

## India corporate inheritance (resolved 2026-06-21)

`regional-inheritance-manifest.json` → pack `india_corporate` (`reference_partner: rapido`).

```bash
python3 finance/build_scoped_corridors.py --partner adani-ports --out finance/recal/corridors-adani-ports.json
python3 finance/model/aggregate.py --partner adani-ports --corridors finance/recal/corridors-adani-ports.json --json finance/recal/agg-adani-ports.json
python3 finance/build_transparent_sheet.py --partner adani-ports --corridors finance/recal/corridors-adani-ports.json --out finance/_sheet_out/adani-ports_unit_econ.xlsx
# repeat for reliance-industries
```

| Partner | Sheet ID | URL |
|---------|----------|-----|
| adani-ports | `1nHiCS0crF7zdFvpZ5GhRjApknsvFDerAjIlRfB4kW5w` | https://docs.google.com/spreadsheets/d/1nHiCS0crF7zdFvpZ5GhRjApknsvFDerAjIlRfB4kW5w/edit |
| reliance-industries | `12A3sSM5HMOF1qoDm4lq8zOKQ5YU17VzlIQ9favraS8Y` | https://docs.google.com/spreadsheets/d/12A3sSM5HMOF1qoDm4lq8zOKQ5YU17VzlIQ9favraS8Y/edit |

Inherited markets (6): `india-mumbai-rapido`, `india-goa-rapido`, `india-kerala-rapido`, `india-andaman-rapido`, `india-kolkata-rapido`, `india-chennai-rapido` — 99 grounded corridors each after dedupe.