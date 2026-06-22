# Partner Deck Grok Handoff Playbook

This repo copy mirrors the workspace skill `partner-deck-grok-handoff`. Use it when existing partner/economics assets need deterministic Deck Studio artifacts for Grok to create or bind a live deck.

> **2026-06-21 upgrade — read this first.** The first Grok-built decks (e.g. the Bolt sandbox) failed parity: they were whole-file copies of the gold Grab deck with a few text boxes poked, leaving Grab's logo, Grab's Singapore routes, and Grab's economics numbers in place, with brand fonts reset to Arial-black and text overflowing. Root cause was **not** a Grok capability gap — it was that the handoff told Grok *what* to say but not *how* to edit. Going forward, Tasklet emits a deterministic **object-keyed edit plan** and Grok applies it verbatim. See `DECK-PARITY-DIAGNOSIS-2026-06-21.md` and `DETERMINISTIC-DECK-EDIT-PLAN-CONTRACT.md`.

## Steps

1. Read partner JSON, data-clean partner JSON, finance/growth assets, economics Sheet URL, and current handoff status.
2. Build `deck.config.json` with pending or live deck ID, source paths, rules, and economics URL if known.
3. Build `slide-manifest.json` and `content-source.json` (narrative source map).
4. Build `image-manifest.json` with per-object image classes (`brand_logo` vs `market_background`/`n30_composite`), `ASSET-REGISTRY.json` keys, fallbacks, and mandatory provenance.
5. **Build `deck.editplan.json`** — the deterministic, object-keyed Slides API batchUpdate plan, validated against `schemas/deck-editplan.schema.json`. This is the artifact Grok applies. It must:
   - reference `golden-template-map.json` (extracted once from the gold deck);
   - use the **style-preserving replace** form (deleteText → insertText → updateTextStyle per run → updateParagraphStyle) so brand fonts/colors survive;
   - keep every captured `autofit` unchanged;
   - keep every string within its object `char_budget`;
   - rebuild multi-run KPI lines from the economics sidecar (never hand-typed, never left as the gold partner's numbers);
   - mark every gold slide `edit | hold | remove` (no silent truncation);
   - swap brand logos (hard requirement) and either composite/replace market backgrounds or fall back to the approved generic Navier hero — **never inherit the prior partner's image**;
   - attach a `qa.leak_denylist` and `qa.expected_object_ids` for Grok's gates.
6. Add batch queue/status/prompt files under `handoff/partner-map-model/{batch}/`.
7. Validate all Deck Studio JSON schemas.
8. Tell Grok: copy gold deck → assert object-id baseline (drift gate) → apply `deck.editplan.json` via Slides API batchUpdate verbatim → run the six QA gates → return a receipt with deck id, op count, leak/style/budget/image scan results, and slide thumbnails.

## Non-negotiables

- No PPTX round-trip or full replace.
- No Atlas-generated images.
- No invented route IDs, city IDs, BPs, economics, sheet URLs, or market claims.
- Null beats confidently wrong — a held/neutral slide always beats a leaked prior-partner route or number.
- A deck must never carry another partner's logo, routes, economics, or market name.
- Brand fonts (Exo 2 / Poppins) and captured colors must survive every edit; no Arial-14-black resets.
- Deck-prep complete is not proposal complete.

## QA gates Grok must pass (returned in the receipt)

1. Drift gate — all plan object ids exist on the fresh copy.
2. Leak scan — zero hits on `qa.leak_denylist`.
3. Style-reset scan — no Arial-14/default-black runs where the golden map specifies Exo 2/Poppins.
4. Budget scan — no edited text exceeds `char_budget`.
5. Image-inheritance scan — no image still resolves to the gold deck's source asset.
6. Render thumbnails attached for human spot-check.
