# GROK QUEUE DRAIN — open issue queue pointer (2026-06-27)

**Why this file exists:** Grok's intake is **PR-triggered** ("idle on PR intake — will process
automatically when Tasklet opens #127+"). All current model/geometry/deck work for Grok is filed as
**GitHub Issues**, so the automated loop has been sitting idle while the issue queue went undrained.
This PR is the trigger: **drain the full open Grok-lane issue queue this pass**, in priority order.

`handoff/GROK-BACKLOG-PENDING.md` remains the living detail; this is the one-screen pointer.

## Open Grok-lane issues (drain all)

| Issue | Title | State on GitHub | Detail |
|---|---|---|---|
| **#127** | Gojek Korea contamination + census re-base + **corridor-coverage** | 🔴 OPEN | `GROK-HANDOFF-gojek-127-corridor-coverage.md` (this PR) + §2.6 |
| **#121** | Maldives 3 wrong-jetty repoints (crown-champa / villa-hotels / sun-siyam) | 🔴 OPEN | §2.4 |
| **#119** | `bp_on_water` gate + gold re-seal (Tasklet signs off after) | 🔴 OPEN | §2.3 |
| **#118** | Grab deck KPI refresh + SOM/SAM/TAM label de-jargon (generator fix) | 🔴 OPEN | §2.5 |
| **#112** | Unified deck builder — hospitality profile (Grok half) | 🟡 OPEN | deck-studio lane |
| **#104** | Bolt Bug C — greenfield census rebase + reseal | 🔴 OPEN | `GROK-HANDOFF-bolt-bugC-census-rebase.md` |
| **#115** | Bite 2 ladder cascade (36 partners) | ✅ CLOSED | 32/36 bound; 4 deferred → `GROK-BACKLOG-PENDING.md` §2.1 |
| **#124** | FE-2 POI follow-through | ✅ CLOSED | Core done on `65df120f`; ~193 dedup tail → §2.8 |

**State-sync (2026-06-27):** #115 and #124 closed on GitHub with Grok handback receipts. Residual tails tracked in backlog, not as open issues.

## Suggested execution order (unchanged from backlog §4)
1. **#127 Gojek** — HIGH, live partner-facing contamination + corridor coverage (this PR's handoff)
2. **#121 Maldives jetties** — confidently-wrong geometry on 3 partners
3. **#119 `bp_on_water`** — unblocks Tasklet's formal SEAL sign-off
4. **#118 Grab labels + deck KPI**
5. **#112 unified deck builder** (hospitality profile)
6. **#104 Bolt Bug C census**
7. **#115 / #124 tails** — close or itemize residual

## Handback (standing rule, per issue)
Branch name, PR link, commit SHA, exact files changed, validation receipt, explicit nulls/held items.
No self-certified completion or line-range audits.

— Tasklet seat · PRs are Jaideep's merge call; this pointer only trips Grok's intake.
