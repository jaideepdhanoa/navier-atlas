# Deck Studio — Branch Map & Consolidation (single Grok-facing source)

**Decision: `tasklet/asset-pack-grab` is the canonical Grok-facing deck-studio branch.**
All deck/asset/economics/logo work converges here. This PR's branch
(`tasklet/deck-autonomy-contract-2026-06-22`) is cut **from** `asset-pack-grab` and
adds the autonomy artifacts (golden map, economics binding, logo manifest, schema fix,
autonomous build contract). Merge target is `asset-pack-grab` (then onward to `main`).

## Why this was confusing
Grok's review referenced files — `golden-template-map.json`, `LOGO-MANIFEST.json`,
`CONSOLIDATED-DECK-GENERATION-QUEUE`, `DETERMINISTIC-DECK-EDIT-PLAN-CONTRACT.md`,
`SPEC-REFRESH.json` — that **did not exist on any pushed branch**. They lived only in a
local working copy that was never pushed. That is the root cause of the "half-finished"
feeling. This PR materializes the real, missing artifacts in the repo so Grok reads
from git, not from memory.

## Branch roles
| Branch | Role | Decks | Verdict |
|---|---|---|---|
| `tasklet/asset-pack-grab` | **Canonical** deck-studio base: 14 deck scaffolds, ASSET-REGISTRY, market backgrounds, CLI, handoff playbook | 14 | **Use this.** Base for all deck work. |
| `tasklet/deck-autonomy-contract-2026-06-22` | This PR — autonomy artifacts on top of canonical | 14 | Merge into `asset-pack-grab`. |
| `tasklet/deck-studio-grok-handoff` (PR #72) | Earlier tidy subset: 3 decks + doc set | 3 | **Superseded** for asset work; do not branch deck builds from it. |

## Rules for Grok
1. **Read from `asset-pack-grab`** (or its merged successor on `main`), never a local-only copy.
2. `LOGO-MANIFEST.json` (this PR) **supersedes** any "needs_sourcing" logo list in queue docs. Reconcile against the manifest, not the markdown.
3. `golden-template-map.json` is the only source of target object IDs. Never invent IDs.
4. `economics-binding.json` says **where**; the partner sheet (content-source.json pointers) says **what**. Never hand-type economics.
5. No live Slides application until a deck's `deck.editplan.json` validates (see AUTONOMOUS-DECK-BUILD-CONTRACT.md).
