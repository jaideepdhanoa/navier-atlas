# Partner Deck Grok Handoff Playbook

This repo copy mirrors the workspace skill `partner-deck-grok-handoff`. Use it when existing partner/economics assets need deterministic Deck Studio artifacts for Grok to create or bind a live deck.

## Steps

1. Read partner JSON, data-clean partner JSON, finance/growth assets, economics Sheet URL, and current handoff status.
2. Build `deck.config.json` with pending or live deck ID, source paths, rules, and economics URL if known.
3. Build `slide-manifest.json` using the 11-slide proposal sequence: hero, why partner, footprint, launch markets, use cases, fleet fit, economics, integration, rollout, Grok appendix, next steps.
4. Build `content-source.json` mapping each slide to exact source fields and economics files.
5. Build `image-manifest.json` with N30/N35 composite placeholders, market-specific background requirements, and mandatory provenance.
6. Add batch queue/status/prompt files under `handoff/partner-map-model/{batch}/`.
7. Validate Deck Studio JSON schemas.
8. Tell Grok: bind/create deck, pull full object inventory, apply via Slides API only, return QA receipts and unresolved gaps.

## Non-negotiables

- No PPTX round-trip or full replace.
- No Atlas-generated images.
- No invented route IDs, city IDs, BPs, economics, sheet URLs, or market claims.
- Null beats confidently wrong.
- Deck-prep complete is not proposal complete.
