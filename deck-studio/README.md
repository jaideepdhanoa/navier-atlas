# Deck Studio — Grok handoff for Navier decks

This folder turns Navier deck creation, live-slide editing, and deck image generation into a repo-native workflow that Grok can run without Tasklet context.

It captures the current golden deck family:

- `french-polynesia` — French Polynesia × Navier
- `careem` — Careem x Navier
- `grab` — Grab × Navier

The operating principle is simple: **the repo is the memory**. Grok should not depend on chat history, Tasklet files, or unstated conventions. Every deck edit should be planned, validated, applied through the Google Slides API, and backed by QA receipts.

## Quick start

```bash
cd deck-studio
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
deck-studio validate --root .
deck-studio pull --root . --deck careem --mode summary
deck-studio qa --root . --deck careem
```

To plan/apply a live edit:

```bash
deck-studio plan --root . --deck grab --request requests/example-edit.md --out out/grab-edit-plan.json
deck-studio apply --root . --deck grab --plan out/grab-edit-plan.json
deck-studio qa --root . --deck grab --receipt out/grab-qa-receipt.json
```

`apply` is intentionally strict: it only accepts Slides API operations, refuses full deck replacement, and requires every object-targeted edit to reference known slide/object IDs or a fresh inventory pulled from Google Slides.

## What lives here

- `docs/` — doctrine, rules, runbooks, and the Grok prompt.
- `decks/<deck>/` — deck config, slide manifest, source map, image manifest, and QA receipt directory.
- `schemas/` — JSON schemas for configs, manifests, edit plans, image jobs, and QA receipts.
- `builders/` — portable Python CLI and deterministic image compositor helpers.
- `assets/` — asset registry locations and placeholders for logos, fonts, N30, backgrounds, masks, and references.
- `examples/` — example edit plans, image jobs, and QA receipts.

## Non-negotiables

1. Edit live decks with the Google Slides API only.
2. No PPTX round-trip.
3. No full-replace of live decks.
4. Preserve slide and object IDs unless a manifest explicitly allows replacement.
5. Canonical N30 compositing; no Atlas-generated images.
6. Every number or claim in the deck points to a source, Sheet, or explicit assumption.
7. Final external outreach stays human-reviewed.
