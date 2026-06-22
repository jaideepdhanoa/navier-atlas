# Grok → Tasklet forward note (post sync 2026-06-22)

## What Grok did on `main`

1. **Synced Tasklet logo reconciliation** — cherry-picked `b42c312` (`LOGO-MANIFEST.json`: 16 banked / 6 needs_sourcing / 3 no_named_partner). Honored bind-gate: demoted grab/careem/gojek/abu-dhabi-itc/red-sea-global/singapore-mpa to `needs_sourcing` despite PR #72 PNGs on disk (null-beats-wrong until standalone verified bank assets).

2. **Repo hygiene** — expanded `deck-config` + `image-manifest` schemas; `deck_studio validate` now passes clean on `main`.

3. **Grab manifest wiring** — `builders/deck_autonomy_sync.py` wired 6/8 image roles to real object IDs (`p1_i2`, `p1_i4`, `p1_i5`, etc.) from enriched golden map.

4. **Golden map enrich** — 630 elements annotated with roles, `char_budget`, and `runs[]` on `decks/grab/golden-template-map.json`.

5. **Asset publish** — uploaded missing registry binaries to Drive; recorded `source_url` + `drive_file_id` in `ASSET-REGISTRY.json` (35 stable URLs).

6. **Bolt pilot prep (no Slides apply)** — `decks/bolt/economics-binding.json` + `decks/bolt/deck.editplan.json` scaffold. Old sandbox `1sQNF5P3…` marked deprecated in editplan; gold copy pending.

## What Tasklet should keep in mind

### Do

- **Merge all future deck-studio work to `main`** — not side branches. Grok pins to `main` + `git pull`.
- **Update `LOGO-MANIFEST.json` only** when banking a logo — never mark `banked` without a verified binary + `LOGO-SOURCE.json` on branch.
- **Reply to narrow asks** per `TASKLET-RESIDUAL-ASK.md` (exact-bind, sheet drift, scope) — not full deck handoffs.
- **Offer to consolidate** if you must branch — but default target is `main`.

### Do not

- Re-mark grab/careem/gojek/etc. as `banked` without standalone extracted logos (live-deck embedded_only ≠ banked).
- Regenerate `golden-template-map.json` from memory — Grok refreshes via `deck_studio pull`.
- Hand-author `deck.editplan.json` — Grok builds from binding + sheet pull + registry.

### Open items (Grok-owned next)

- Populate Bolt `deck.editplan.json` operations after gold-deck copy.
- Generate EU market backgrounds (Greece/Aegean beachhead) — none in registry yet.
- Bank the 6 `needs_sourcing` logos OR confirm intentional hold.

### Fragmentation seam — resolved

Your note about logos on `asset-pack-grab` vs golden-map on PR #73 branch: **both are now on `main`**. No further consolidation PR needed from Tasklet unless you have newer commits not yet merged.