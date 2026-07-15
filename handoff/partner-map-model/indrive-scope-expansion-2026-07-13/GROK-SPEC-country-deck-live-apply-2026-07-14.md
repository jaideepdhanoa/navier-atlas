# GROK SPEC — DiDi/inDrive country-deck live apply (new locked spine)

**Date:** 2026-07-14
**Owner handoff:** Tasklet → Grok (deterministic model-to-deck live apply)
**Decks:** DiDi Brazil, DiDi Mexico, inDrive Brazil, inDrive Egypt
**Trigger:** builder bug fix + package regeneration (this PR). Live decks still carry the OLD 16-slide structure and MUST be restructured to the new locked spine.

## Why this is needed (literal state)
- `deck-studio/builders/build_country_mobility_review.py` crashed at runtime (`null` used where Python needs `None`, indrive-egypt TAM rung 3). It could not run, so the corrected packages from PR #264/#266/#268 were never regenerated.
- The committed `deck-studio/decks/{deck}/*` packages and all four LIVE decks therefore still show the abolished structure: per-city alternating economics slides, four Rio routes rendered as four city chapters, and the old TAM chart.
- This PR fixes the builder and regenerates all four package sets to the new locked spine. Live Slides still need the deterministic apply below.

## New locked spine (per merged builder)
cover → why-partner → ONE market overview → ONE slide per canonical city → ONE unit-economics slide → TAM ladder → integration → rollout → ask → close

| Deck | Live deck ID | Slides | City slides |
|---|---|---|---|
| DiDi Brazil | `1OixKrHjQbWu0Plkvj-57SQyTFxPL5Ii8l3K6Q9umJOk` | 12 | Rio de Janeiro; Angra dos Reis & Ilha Grande (held); Florianópolis (held) |
| DiDi Mexico | `1XwKRuJtMrou8NtBdc1oY3LL2Dk83dCs9MCLvNKgwq0c` | 13 | Cancún & Isla Mujeres; Playa del Carmen & Cozumel; Puerto Vallarta (held); Los Cabos (held) |
| inDrive Brazil | `1QImIe6KAee0Eajsokgh9NmH0I29lir4l2LV63e-9OxE` | 12 | Rio de Janeiro; Angra dos Reis & Ilha Grande (held); Florianópolis (held) |
| inDrive Egypt | `1Nn3BRKUahikp87zC84JMdEVrcJYppm9ZXHgndAuzsEk` | 11 | Hurghada; Sharm El Sheikh |

## Apply steps (deterministic, Slides API only)
1. **Refresh economics.** Run `deck-studio/decks/gen_deck_economics.py` for each deck against the current aggregate/routes/binding so `generated-deck-economics.json` is regenerated and its `source_sha256` hashes are current. inDrive Brazil shares the canonical Brazil route/cost basis with DiDi Brazil — figures must be identical; any Brazil-reference revision cascades to BOTH.
2. **Preflight.** Run `deck-studio/qa/preflight_country_mobility_review.py` on all four package dirs → must be PASS before touching live Slides.
3. **Duplicate/bind the approved Grab mobility reference** and restructure each live deck to the spine above. Do NOT wholesale-replace; Slides API only; no PPTX. Remove the abolished alternating per-city economics slides and the old TAM chart.
4. **Bind text** from each `deck.editplan.json` `slide_text` map; bind economics values from `generated-deck-economics.json` (never hand-typed).
5. **inDrive Egypt unit-economics slide:** render ONLY the anchor Jaideep selects (Giftun `rn-b06f6971ed47` OR Ras Mohammed `rn-c16a1627130f`). Do NOT render the word "pending" or "Jaideep's choice" on the partner-facing slide — that phrase is a source note only. Hold the slide until the selection is provided.
6. **Egypt TAM slide:** render the 3-rung ladder exactly — Rung 1 floor ($8.50M pool / ~$7.65M Navier rev, "this is the FLOOR, not the market"); Rung 2 Red Sea day-trip SAM ($21.3M–$33.4M Hurghada alone, labelled 35–55% participation band on sourced UNWTO arrivals); Rung 3 held null (Nile + Alexandria). Never present the floor as the TAM; never use "below tourism economy → no inflation."
7. **Atlas route screenshot slots** stay unpopulated — human insertion only. Automation must not fill `asset_ref`/`asset_path`/`registry_key`/`target_object_id`. No visible placeholder text/labels/build instructions on any partner-facing slide.
8. **Partner logos** on cover per each `deck.config.json` `cover_logos` (banked DiDi / inDrive white cover logo + Navier wordmark).
9. **Copy gate.** Run `scripts/audit_partner_copy.py` and the deck copy lint as BLOCKING gates — zero internal process vocabulary; visible capitalized archetype chips limited to tourism / essential_mobility / luxury / super_app / ride_hail.
10. **Readback.** Pull each live deck inventory after apply, set each `deck.editplan.json` `apply_status` to `applied_and_live_inventory_read_back`, sync slide manifests to live object IDs, and return a QA receipt (deck ID, slide count, image provenance ledger, source-map coverage, unresolved gaps, no-op replay).

## Discipline
- Exact ID matching only; unsupported values `null`; no invented geography/piers/route IDs/demand/economics.
- No external release clearance claimed. Jaideep controls merge and final release.
- Immutable canonical totals: Brazil $23,404,822 / 113 vessels (4 routes); Mexico $14,759,160 / 88 vessels (3 routes); Egypt floor $8.50M pool / ~$7.65M Navier rev / ~20 vessels (2 captive routes).
