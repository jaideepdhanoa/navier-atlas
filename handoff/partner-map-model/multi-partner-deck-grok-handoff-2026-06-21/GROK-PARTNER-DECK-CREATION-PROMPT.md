# Grok prompt — create/bind partner decks from Tasklet Deck Studio handoffs

Batch: `multi-partner-deck-grok-handoff-2026-06-21`

## Mandate

Create or bind partner proposal decks for the nine partner deck keys in `partner-deck-grok-readiness-queue.json`:

- `bolt`
- `yango`
- `noon`
- `ola`
- `rapido`
- `uber-india`
- `uber-mena`
- `adani-ports`
- `reliance-industries`

Tasklet has prepared Deck Studio config, slide manifest, content source map, and image manifest for each. Your job is deterministic deck creation/binding and QA only.

## Required inputs

- `handoff/partner-map-model/multi-partner-deck-grok-handoff-2026-06-21/partner-deck-grok-readiness-queue.json`
- `handoff/partner-map-model/multi-partner-deck-grok-handoff-2026-06-21/partner-deck-source-map.json`
- `deck-studio/decks/*/deck.config.json`
- `deck-studio/decks/*/slide-manifest.json`
- `deck-studio/decks/*/content-source.json`
- `deck-studio/decks/*/image-manifest.json`
- source partner/economics files listed in each deck config

## Apply rules

1. Bind an existing live deck or create a new Google Slides deck for each deck key.
2. Pull summary and full object inventory before edits.
3. Apply via Slides API only. No PPTX round-trip, no full replacement.
4. Use the planned 11-slide sequence unless an approved live template requires object-preserving adaptation.
5. Use only claims mapped in `content-source.json` and the listed source files.
6. Do not invent route IDs, city IDs, boarding-point IDs, sheet URLs, economics values, or image provenance.
7. Preserve pending/null values where source evidence is absent.
8. For images: use canonical N30/N35 composites, market-specific source-approved backgrounds, minimal gold accents, and saved provenance. Atlas-generated images are forbidden.
9. Return unresolved items as a gap queue, not as deck copy.

## Partner-specific scope guards

- Bolt: preserve current constraints — no Mexico/Morocco; Malaysia only Penang + Sabah/Kota Kinabalu if reintroduced.
- Yango: existing baseline first; country/region seeds additive only; lead with Dubai-HQ Yango framing.
- Noon: UAE-first; KSA/Egypt narrative-only unless separately sealed and cascaded.
- Ola/Rapido/Uber India: high-value India consumer markets only; Kolkata and Chennai in scope; Priority B out of scope.
- Uber MENA: MENA/Gulf slice of `uber.json`; do not union global Uber markets.
- Adani Ports: user said “Andani”; normalize to existing `adani-ports`.
- Reliance: use existing `reliance-industries` source only.

## Return receipts

For each deck return:

- live deck ID and URL
- object inventory pull receipt
- Slides API apply receipt
- slide count and per-slide source-map coverage
- image provenance ledger
- route/render appendix receipt or explicit gap queue
- no-op replay receipt
- unresolved gaps separated by owner: Grok, Tasklet, human

## Acceptance

A deck is not done until create/bind/apply/render/image/source-map QA receipts are returned. Tasklet deck-prep artifacts are complete, but live deck completion remains pending your receipts.
