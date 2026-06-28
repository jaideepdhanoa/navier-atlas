# AirAsia MOVE deck — Grok handoff status

**Batch:** airasia-move-2026-06-28 · **Author:** Tasklet · **Status:** `deck-prep-complete / grok-create-or-bind-needed`

## Tasklet-owned (DONE)
- `deck-studio/decks/airasia-move/deck.config.json` — identity, visual base/reference, source paths, economics basis (model-pass-pending), logo status `needs_sourcing`.
- `deck-studio/decks/airasia-move/slide-manifest.json` — 11-slide mobility spine, `object_inventory_status: stale_requires_pull`.
- `deck-studio/decks/airasia-move/content-source.json` — per-slide source map to the partner JSON + holds.
- `deck-studio/decks/airasia-move/image-manifest.json` — 8 image roles; partner logo `needs_sourcing`; every placeholder `provenance_required: true`.
- Batch handoff: readiness queue, source map, Grok creation prompt, this status note.

## Grok-owned (HELD)
- Create/bind live `deck_id`; pull full object inventory; apply via Slides API; return QA receipts.
- Source + bank the AirAsia MOVE cover logo (`needs_sourcing` → `banked` with `LOGO-SOURCE.json`).
- Economics numbers — **only after the arriving-seat model pass** (`growth_case` stays `model-pass-pending`).
- 18 Philippines corridor route_ids — Phase 2 seal (`handoff/GROK-SPEC-airasia-phase2-seal.md`).
- `partner_copy_lint.py` blocking gate green before seal.

## Explicit nulls / holds
- `deck_id` = pending-grok-create-or-bind
- `economics_url` = null · `growth_case` numerics = null (model-pass-pending)
- AirAsia MOVE partner logo = needs_sourcing
- 18 PH corridors route_id = null (mint-pending)

> Deck-ready ≠ proposal-complete. This package makes Grok able to create the live deck; the deck is done only after create/bind/apply/render QA receipts return.
