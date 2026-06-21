# PR #65 Deck Studio gap report — 2026-06-21

## Status summary

| Phase | Status |
|-------|--------|
| Local validate | **PASS** (all 11 #65 + golden decks) |
| Live bind (Slides OAuth) | **COMPLETE** — 11 sandbox decks from Grab template |
| Content apply + 11-slide trim | **COMPLETE** — partner text from `content-source.json` |
| Economics URL bind | **11/11 bound** — India corporate inherit published 2026-06-21 |
| Route/render QA ledgers | **COMPLETE** — `decks/<deck>/ledgers/route-render-qa.json` |
| N30 image compositing | **HELD-NULL** — no approved backgrounds or `n30.png` in repo |
| Schema validate post-content | **PASS** |

Lane report: `deck-studio/out/pr65-content-lane-report.json`

## Packages — live deck IDs + content QA

| Deck key | Slides | Economics URL | Route QA | Content QA |
|----------|--------|---------------|----------|------------|
| adani-ports | 11 | [Sheet](https://docs.google.com/spreadsheets/d/1nHiCS0crF7zdFvpZ5GhRjApknsvFDerAjIlRfB4kW5w/edit) | PASS_WITH_FLAGS | pass |
| bolt | 11 | [Sheet](https://docs.google.com/spreadsheets/d/1XkD0x-PfDyY34ZBy5jX2u1LqoibAd_xMiyO-Re2UWUk/edit) | PASS | pass |
| caribbean-mobility | 11 | [Sheet](https://docs.google.com/spreadsheets/d/1J9rb-rAXkLnJPrKO8WhG7bLkofG-IB5En6hrjnwDyt0/edit) | PASS | pass |
| noon | 11 | [Sheet](https://docs.google.com/spreadsheets/d/1v0ywhNFk_fA1JRVhizWlz89RKgQWlID9RD3LfBhVB2Y/edit) | PASS | pass |
| ola | 11 | [Sheet](https://docs.google.com/spreadsheets/d/1pNwq_GQd2Fdem8O4o2GNNoKxBPxXOPDh1qfbhGFGkaQ/edit) | PASS | pass |
| rapido | 11 | [Sheet](https://docs.google.com/spreadsheets/d/1ujRCwCKNFcfUbVL5B312fjcYmtvsDVhBtK2hsTHo-qA/edit) | PASS | pass |
| reliance-industries | 11 | [Sheet](https://docs.google.com/spreadsheets/d/12A3sSM5HMOF1qoDm4lq8zOKQ5YU17VzlIQ9favraS8Y/edit) | PASS_WITH_FLAGS | pass |
| uber-india | 11 | [Sheet](https://docs.google.com/spreadsheets/d/1L6StDXDjdR26l_bIqRRH150B1rTeT9pHk76JKkG3rqw/edit) | PASS | pass |
| uber-mena | 11 | [Sheet](https://docs.google.com/spreadsheets/d/19VtRN0U6Gggq_RQlRuSxmiIxnp2KgGEIvXOW72RQHIQ/edit) | PASS | pass |
| yango | 11 | [Sheet](https://docs.google.com/spreadsheets/d/1fvB_tc8IWUTlKMWjPcoJde_uPnGKVqoCxxsgd5IL1rM/edit) | PASS | pass |
| yassir | 11 | [Sheet](https://docs.google.com/spreadsheets/d/1ba9Zpap5hPAehDKFHgk2PwRq4xStr2rx_z1LGSY52Q4/edit) | PASS | pass |

Live deck links unchanged from bind pass (`deck-studio/out/pr65-deck-bind-report.json`).

## What ran (content lane)

```bash
cd deck-studio
export GOOGLE_TOKEN_PATH=~/.config/google-drive-mcp/tokens.json
export PYTHONPATH=builders
python -m deck_studio.pr65_content_lane
```

Per deck:
1. Bind `economics_url` / `economics_sheet_id` from `finance/economics_url_map.json` where available
2. Run `scripts/audit_partner_page_qa.py --partner <slug>` → route/render ledger
3. Write image provenance ledger (held-null — no approved assets)
4. Build + apply Slides API edit plan (partner title/body text on slides 1–11)
5. Delete slides 12–23 (Grab sandbox trim)
6. Re-pull full inventory + `pr65-content-qa.json` receipt

## Remaining gaps

### Economics

All 11 decks bound. See `handoff/partner-map-model/PR65-ECONOMICS-SHEET-NOTES-2026-06-21.md`.

- **adani-ports** / **reliance-industries** — LB-257 scoped inherit from Rapido India corridor markets (`india_corporate` pack), partner-owned sheets (not Rapido's URL)

### N30 images (all 11 decks)

`decks/<deck>/ledgers/image-provenance-ledger.json` — status `held_null_pending_approved_assets`.

Blocked until:
- Source-approved market backgrounds checked in under `deck-studio/assets/backgrounds/`
- Canonical `assets/n30/n30.png` (or Drive registry entry per `assets/n30/README.md`)

IMAGE-RULES forbid Atlas-generated or generic decorative imagery.

### Content polish (non-blocking)

- Grab-template layout slots ≠ final brand layouts; text applied to largest title/body shapes per slide
- Slide 10 appendix includes page-QA summary + sourced journey rows; full route-ID seal receipts still partner-specific
- Human review required before external send (per `LIVE-DECK-RULES.md`)

## Auth

`deck_studio/cli.py` loads MCP OAuth: `GOOGLE_TOKEN_PATH` + `GOOGLE_CLIENT_PATH` (default `~/.config/google-drive-mcp/`).