# GROK — Create the AirAsia MOVE × Navier partner deck

**Deck key:** `airasia-move` · **Archetype:** mobility / super-app distributor · **Visual treatment:** luxury × mobility hybrid
**Status handed over:** Tasklet deck-prep complete → Grok create/bind/apply/QA needed.
**Deck-prep artifacts:** `deck-studio/decks/airasia-move/{deck.config.json, slide-manifest.json, content-source.json, image-manifest.json}`

## What this deck is
The arriving-seat thesis in a deck: *AirAsia already flies the traveller in — Navier carries them the last leg over the water, pre-booked inside MOVE at flight checkout.* It is the **Grab Thailand 11-slide mobility spine** (structure + brand system) **dressed in destination-cinematic full-bleed imagery** (Minor Hotels deck is the visual reference for the luxury dressing — **dressing only, not the hospitality content frame**).

## Build instructions (Slides API only)
1. **Create/bind** the live Google Slides deck from the **Grab Thailand gold base** (`11WCun1Xk1flPmqvvtYrYZXsL5yRb5KQoe0xvTQSppKo`). Write the real `deck_id` back into `deck.config.json` + `slide-manifest.json` (replace `pending-grok-create-or-bind`).
2. **Pull the full object inventory first.** Map planned slide content to real object IDs before any edit. Never assume OIDs.
3. **Apply through Slides API only** — no PPTX round-trip, no full replacement, no manual visual drift. Preserve existing objects unless explicitly instructed.
4. **Copy:** source every rendered claim from `partner-pitch/partners/airasia-move.json` (+ data-clean mirror) per `content-source.json`. Plain English. No internal taxonomy (SOM/SAM/TAM/GMV/route_id/etc.) in any rendered title/subtitle/caption/label.
5. **Economics slide (7):** **arriving-seat distribution-capture basis ONLY — no numbers.** `growth_case` is `model-pass-pending`. Do not invent TAM/capture/revenue figures. If one bound corridor illustration is wanted, use a Singapore cross-border leg (real bound route_id) — otherwise keep it frame-only.
6. **Images:** apply every image as a registry-resolved element (never re-embed a one-off binary). Canonical N30/N35 composites with market-specific approved backgrounds; destination-cinematic full-bleed dressing; minimal gold accents; **no Atlas-generated images.** Match the N30 reference (neutral hull; lighting set by the plate).
7. **Partner logo:** AirAsia MOVE cover logo is **`needs_sourcing`** — source the official mark, bank under `assets/logos/partners/airasia-move/` with `LOGO-SOURCE.json`, register it, then set `banked`. **Do not guess a logo.** Cover ships Navier + AirAsia MOVE.
8. **Route appendix (10):** bound route_ids for TH/ID/MY (sealed) + Singapore's 4 cross-border legs; **18 Philippines corridors are mint-pending** (see `handoff/GROK-SPEC-airasia-phase2-seal.md`). Mark holds explicitly.

## Blocking gates
- `deck-studio/qa/partner_copy_lint.py` — **blocking**, same status as the land-crossing gate. No internal taxonomy in rendered text. Do not seal until green.
- No fabricated economics. No invented route/city/BP IDs — pending/null stays pending/null.

## Handback contract (required)
branch name · PR link · commit SHA · exact files changed · deck_id · slide count · image provenance ledger · source-map coverage · render receipts · `partner_copy_lint` result · unresolved gaps/holds · no-op replay result. No self-certified completion, no line-range audits.
