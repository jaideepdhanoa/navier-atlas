# PR #65 Deck Studio gap report — 2026-06-21

## Live bind pass (complete)

- `GOOGLE_TOKEN_PATH=/Users/jaideep/.config/google-drive-mcp/tokens.json` — Slides + Drive OAuth verified
- `deck-studio validate` — **PASS** (all 11 #65 packages + golden decks)
- Live decks created from Grab template copy (PR65 sandbox copies)
- Per deck: `pull --mode full` → `plan` → `apply` (no-op) → `qa`
- Live QA receipts: `deck-studio/decks/<deck>/qa-receipts/pr65-live-qa.json`
- Status: **pass** on all 11 #65 packages (23 slides each, full object inventory pulled)

## Packages — live deck IDs

| Deck key | Config | Content source | Image manifest | Live deck ID | QA |
|----------|--------|----------------|----------------|--------------|-----|
| adani-ports | ✓ | ✓ | ✓ | `1WKRo-A3DamjYBT_dmuMazw8s7K9PHinFZFilkbwlb7c` | pass |
| bolt | ✓ | ✓ | ✓ | `1sQNF5P3OjhAlSh917yO6If1OPBGnwOBvrBzGXcYZh4c` | pass |
| caribbean-mobility | ✓ | ✓ | ✓ | `1FL4B_AxahPoyQRCHfjUy_GwzxcNyZquoXRP1v5O0EgA` | pass |
| noon | ✓ | ✓ | ✓ | `10yH0aMKJsSDhz2epxyZb9hMCyDSRYJp4DrPDYJQZ38A` | pass |
| ola | ✓ | ✓ | ✓ | `1unu9eU1kfIdq9zU7lEm33P5JMDLeEvViQ7FcdCAEgYI` | pass |
| rapido | ✓ | ✓ | ✓ | `1EU_W3HEEUHDY91XwVHDX3e7Hv2D3nhY7VHgVe369gFM` | pass |
| reliance-industries | ✓ | ✓ | ✓ | `1Nvphyjr1rHmgM4YMqLnfj9lGDm4_sDPJHwZ4j9c279Y` | pass |
| uber-india | ✓ | ✓ | ✓ | `1I-QTXOLN2KExoR7e6qYFqL03lBo2MAA45sw3zMkw1Kg` | pass |
| uber-mena | ✓ | ✓ | ✓ | `1-COtUkEqZE8QfbBI1YXPqeY0xbTnCOQUOjB2UHPMuqk` | pass |
| yango | ✓ | ✓ | ✓ | `1A-ElNhMyvyRLzidj1r3J5ibLaqi746TSLJMvJlkts78` | pass |
| yassir | ✓ | ✓ | ✓ | `1fqwFDPrLklNbxrS_0ibo5MsXa-iGT43uLZNMCvU4wMo` | pass |

Bind report artifact: `deck-studio/out/pr65-deck-bind-report.json`

## Remaining gaps (content, not bind)

These decks are **bound and inventory-pulled** but still carry Grab-template placeholder content. Next passes:

1. Partner-specific text edits via Slides API edit plans (sourced from each `content-source.json`)
2. N30 image compositing per `image-manifest.json` + provenance receipts
3. Economics sheet URL binding where `economics_url` is still null
4. Slide-count alignment: planned outlines were 10–11 slides; live copies are 23-slide Grab sandboxes — trim or restructure in a follow-up edit plan
5. Route/render QA for route appendix slides

## Auth note

`deck_studio/cli.py` now loads MCP OAuth the same way as `finance/drive_upload.py`: token from `GOOGLE_TOKEN_PATH` (default `~/.config/google-drive-mcp/tokens.json`) plus client keys from `GOOGLE_CLIENT_PATH` (default `~/.config/google-drive-mcp/gcp-oauth.keys.json`). Token refresh is persisted back to the token file.