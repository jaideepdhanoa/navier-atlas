# Deck Studio — branch map (Grok-facing)

**Canonical source: `main`** (as of 2026-06-22).

All deck/asset/economics/logo work is consolidated on `main`. Grok reads from git on `main`, not from memory or stale branch names.

## Pinned SHAs (historical — now merged to main)

| Artifact | Original branch / commit | On `main` via |
|---|---|---|
| Logo bank + reconciled `LOGO-MANIFEST.json` | `tasklet/asset-pack-grab` @ `b42c312` | cherry-pick `b0b4806` |
| Autonomy contract + Grab economics-binding | `tasklet/deck-autonomy-contract` @ `d931362` | cherry-pick `d3377a7` |
| Asset pack expansion (N30, Careem, FP) | PR #71 | merge |
| Deck generation kickoff (queue, SPEC-REFRESH) | PR #72 | merge |

## Single sources of truth

| File | Role |
|---|---|
| `assets/logos/LOGO-MANIFEST.json` | Cover logo bind-gate (`status=="banked"` only) |
| `decks/grab/golden-template-map.json` | Target object IDs (630 elements, enriched with roles) |
| `decks/grab/economics-binding.json` | Field→object map for slides 3/7/10 + OPEX |
| `assets/ASSET-REGISTRY.json` | Image provenance + stable `source_url` |
| `docs/AUTONOMOUS-DECK-BUILD-CONTRACT.md` | Grok-owned build loop |
| `docs/TASKLET-RESIDUAL-ASK.md` | Narrow Tasklet advisory lane |

## Rules for Grok

1. **Read from `main` only.** Run `git pull` before every deck session.
2. Reconcile logo status from `LOGO-MANIFEST.json`, not queue markdown.
3. Never bind a cover logo unless manifest `status=="banked"`.
4. No Slides write until `deck.editplan.json` validates and is non-empty.
5. Run `python3 builders/deck_autonomy_sync.py` for hygiene steps (see script `--help`).

## Superseded branches

- `tasklet/asset-pack-grab` — merged content lives on `main`; do not branch new work from it.
- `tasklet/deck-studio-grok-handoff` (PR #64) — superseded for asset/deck builds.