# Kakao Mobility — economics sheet hold

**As of:** 2026-07-10  
**Partner:** `kakao-mobility`  
**Spine:** Korea Hangang network (41 corridors, `country: South Korea`)

## Decision

**Do not create or publish a Google Sheet** until `South Korea` exists in  
`finance/model/country-reference.json`.

Building now would re-run the Swing failure mode: silent (now bannered) **Singapore** opex on a full Korea network.

## Current wiring

| Field | Value |
|-------|--------|
| `PARTNER-SHEET-IDS.json` | no `kakao-mobility` / `kakao` key |
| `economics_url` | null / absent |
| `_economics_status` | `held_pending_korea_country_opex` (see partner JSON) |
| Agg / growth | may exist for spine; not cascade-sealed to a sheet |

## When South Korea is sealed

1. `python3 finance/lint_country_opex.py --partner kakao-mobility` → exit 0  
2. Create Drive sheet + register ID in `finance/PARTNER-SHEET-IDS.json`  
3. `build_transparent_sheet.py --partner kakao-mobility`  
4. Publish; set `economics_url` on `data-clean/partners/kakao-mobility.json` + pitch mirror  
5. Clear hold in `_economics_status`  

Use `finance/create_partner_sheets.py` / Drive tools only after step 1 is green.
