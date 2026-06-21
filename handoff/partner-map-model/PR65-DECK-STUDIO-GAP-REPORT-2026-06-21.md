# PR #65 Deck Studio gap report — 2026-06-21

## Local validation (complete)

- `deck-studio validate` — **PASS** (all 11 #65 packages + golden decks)
- Local QA receipts written per deck: `deck-studio/decks/<deck>/qa-receipts/pr65-local-qa.json`
- Status: **pass_with_flags** on all #65 packages (expected: `deck_id` = `PENDING_GROK_CREATE_OR_BIND`)

## Packages validated

| Deck key | Config | Content source | Image manifest | Live deck ID |
|----------|--------|----------------|----------------|--------------|
| adani-ports | ✓ | ✓ | ✓ | PENDING |
| bolt | ✓ | ✓ | ✓ | PENDING |
| caribbean-mobility | ✓ | ✓ | ✓ | PENDING |
| noon | ✓ | ✓ | ✓ | PENDING |
| ola | ✓ | ✓ | ✓ | PENDING |
| rapido | ✓ | ✓ | ✓ | PENDING |
| reliance-industries | ✓ | ✓ | ✓ | PENDING |
| uber-india | ✓ | ✓ | ✓ | PENDING |
| uber-mena | ✓ | ✓ | ✓ | PENDING |
| yango | ✓ | ✓ | ✓ | PENDING |
| yassir | ✓ | ✓ | ✓ | PENDING |

## Blocked on human OAuth (not run in this lane)

Live Google Slides bind/create requires:

```bash
export GOOGLE_TOKEN_PATH=/path/to/oauth-token.json  # presentations + drive.readonly scopes
cd deck-studio
deck-studio pull --root . --deck yassir --mode full
deck-studio plan --root . --deck yassir --request requests/pr65-initial.md
deck-studio apply --root . --deck yassir --plan out/yassir-edit-plan.json
```

Repeat for each deck key above after writing `deck_id` back to `deck.config.json`.

## Next action

Provide `GOOGLE_TOKEN_PATH` (or service-account extension in `deck_studio/cli.py`) to complete live deck bind, pull inventory, Slides API apply, and image compositing passes.