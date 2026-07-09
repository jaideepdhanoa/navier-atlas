# Contrast — July-3 (post-Yango-expansion) build vs current sealed

**Date:** 2026-07-06
**July-3 reference:** main @ `41cdc35` (after PR #177 Yango coverage-density + #178 roster correction merged July 3)
**Current:** sealed build `8ecd1227`
**Registers:** `handoff/LOST-CORRIDORS-JUL3-CLASSIFIED.json`, `handoff/LOST-OD-JUL3-BY-CLUSTER.json`

## Headline
| Metric | July-3 (post-expansion) | Current | Δ |
|---|---|---|---|
| Raw route features | 8,130 | 4,221 | −3,909 |
| Distinct city↔city corridors | 428 | 336 | **−92 net** |
| Distinct corridors lost | — | — | 116 |
| Distinct corridors gained | — | — | 24 |

## The cull was July 5–6, so July-3 ≈ July-2
The July-3 Yango expansion (PRs #177/#178) was **additive** (new cities/BPs/handoffs, no route removal). The corridor cull happened July 5–6 (UAE de-spaghetti PR #188, global geometry PR #189, reseal). So contrasting July-3 gives the **same lost set** as July-2 — this is a robustness check, and it holds.

## Classification of the 116 lost (stable across both references)
| Bucket | Count | Disposition |
|---|---|---|
| A — in-range 3–60 nm | 35 | **Restore** (coastal/island over-culls) |
| B — Q-LR 60–180 nm | 22 | **Restore** as Quanta-LR if water-clean |
| C — self-referential / <3 nm | 36 | **Correct drop** (hygiene) |
| D — out-of-range >180 nm | 23 | **Correct drop** (beyond N30/Q-LR) |
| | | **57 genuine restore · 59 correct drops** |

## Named examples — all confirmed present July-3 and culled
- **Phuket ↔ Langkawi** (90.7 nm) — bucket B, restore as Q-LR
- **Langkawi ↔ Penang** (6.8 nm) — bucket A, restore
- **Bangkok ↔ Hua Hin** (~76 nm) — bucket B, restore as Q-LR
- **Hua Hin** endpoints present July-3 (Anantara/Fishing Pier) → the `hua-hin-thailand` BP was removed in the July-5/6 locale cleanup; re-source + re-mint.

## Caveat on the restore lists
Distance classification is a first cut. A handful of bucket-A entries are still junk/business-POI endpoints (`Constant Wind`, `Lady K Sailing Cruises`, `None↔None`) or out-of-scope cross-border (`NEOM↔Sharm El Sheikh`) — Grok applies the endpoint-quality + water-clean filter before minting. Net genuine restore after that filter ≈ 45–55.

## Net-net
Same conclusion as the July-2 contrast: the big raw drop (−3,909 features) is overwhelmingly correct hygiene/de-dupe; the **real regression is ~57 distinct corridors** wrongly culled, concentrated in Indonesia, Thailand, Greece, UAE, Qatar, Italy, Cyprus. Restore lists stand in `GROK-SPEC-corridor-restore-JUL2-2026-07-06.md`.
