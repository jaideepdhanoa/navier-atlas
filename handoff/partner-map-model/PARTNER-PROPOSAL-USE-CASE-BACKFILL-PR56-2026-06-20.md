# Partner proposal use-case backfill — PR 56 — 2026-06-20

## What changed

- Backfilled all `18` phase records that had truly empty `use_cases` arrays.
- Backfilled all `113` hub/sub-proposal markets with market-summary-level `use_cases`.
- Formalized market-level use cases in the partner proposal schema and renderer.
- Encoded the Phase 3 correction rule: every newly promoted partner-market bind needs at least two local use cases before it becomes proposal-ready; otherwise it stays display-only / economics-pending.

## Post-backfill checks

| Check | Result |
|---|---:|
| Empty phase `use_cases` arrays | 0 |
| Hub/sub-proposal markets without market-level `use_cases` | 0 |
| Phase 3 market gate failures | 0 |

## Backfilled phase records by partner

- `careem.json`: 1
- `didi.json`: 4
- `discovery-land.json`: 3
- `indrive.json`: 4
- `uber.json`: 3
- `yango.json`: 3

## Backfilled market-level summaries by partner

- `aman.json`: 6
- `bolt.json`: 14
- `didi.json`: 7
- `discovery-land.json`: 3
- `four-seasons.json`: 6
- `gojek.json`: 6
- `grab.json`: 13
- `indrive.json`: 4
- `kakao-mobility.json`: 4
- `line.json`: 3
- `lyft.json`: 6
- `ola.json`: 4
- `rapido.json`: 4
- `six-senses.json`: 6
- `soneva.json`: 2
- `uber.json`: 17
- `yango.json`: 8

## Gate language

New Phase 3 partner-market promotions are proposal-ready only when they carry at least two local use cases. If the local use cases are missing or fewer than two, the bind may still display, but it remains economics-pending / proposal-not-ready until authored.
