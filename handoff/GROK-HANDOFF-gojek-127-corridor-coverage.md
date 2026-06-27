# GROK HANDOFF — Gojek (#127): Indonesia corridor-model coverage gap (depth root cause)

**Owner: Grok (model + geometry lane).** Additive to Issue #127 (Korea-contamination rebind +
census re-base). This handoff carries the *root cause* surfaced by Tasklet's corridor-inheritance
audit: Gojek reads shallow vs Grab Thailand **because Indonesia is under-modeled in
`finance/model/corridors.json`** — not because of authoring effort.

Filed as the second comment on Issue #127 (2026-06-27). This file restates it in the channel Grok's
intake drains.

## Finding — deterministic inheritance is starved at the source
Each region in `finance/model/corridors.json` is the inheritance source: every corridor already carries
from/to/distance/vessel/archetype and (mostly) its own `route_id`, so binding is automatic. Tasklet's
job is to inherit every real corridor per region 1:1, attach the inherited `route_id`, and author the
`today`/`with_navier` prose. **Tasklet does not invent corridors.**

Inheriting honestly today (self-loop / network placeholder rows dropped):

| Gojek cluster | region | real corridors | route_id-bound | null (need bind) |
|---|---|---|---|---|
| jakarta | `jakarta` | 3 | 3 | 0 |
| bali-nusa-gili | `bali` | 9 | 8 | 1 |
| singapore | `singapore` | 12 | 2 | **10** |
| riau-singapore | `cross-border` | 4 | 3 | 1 |
| eastern-indonesia | `borneo` | 3 | 3 | 0 |
| **komodo-flores** | **(none)** | **0** | — | — |
| **TOTAL** | | **31** | | **12** |

By contrast Grab Thailand inherits dozens (phuket 11, koh-samui 7, penang 14, langkawi 13, bangkok 2…).
You cannot inherit depth the model does not contain — komodo-flores has **zero** modeled corridors, and
jakarta/eastern-indonesia are thin.

## Grok asks (model lane)
1. **Mint corridors for the under-modeled Indonesian regions** so the named clusters can inherit honestly:
   - `komodo-flores` — Labuan Bajo ↔ Komodo / Rinca / Padar (currently **0**).
   - Thicken `jakarta` (Thousand Islands beyond the current 3) and `borneo`/eastern-indonesia.
   - Optionally Lombok/Gili, Raja Ampat, Sumba if in scope.
2. **Mint the 12 missing `route_id`s** on modeled-but-unbound corridors (10 Singapore, 1 Bali, 1
   cross-border) so inheritance binds automatically with no null-pending.
3. **Derive the top-level rebind from the corrected per-region inheritance** — the `journeys_unlocked` /
   `phases` rebind in #127 Bug A should be sourced from this corrected pool, not the current thin set.

## Sequencing
- This is additive to #127 Bug A (Korea rebind) and Bug B (census re-base) — same partner, same reseal.
- **Tasklet holds** until corridors + route_ids land, then inherits 1:1, authors prose, and cascades
  everything (copy + Indonesia deck) in **one** Gojek PR. No piecemeal PRs, no invented corridors.

## Handback required (standing rule)
Branch name, PR link, commit SHA, exact files changed, validation receipt (new corridor count per region,
route_id null-count = 0 on the named clusters), and explicit nulls/held items. No self-certified
completion or line-range audits.

Refs: Issue #127 (body + 2026-06-27 comment); `partner-model-cascade` golden rules;
`grok-seal-handoff` two-worlds rule; `handoff/GROK-BACKLOG-PENDING.md` §2.6.
