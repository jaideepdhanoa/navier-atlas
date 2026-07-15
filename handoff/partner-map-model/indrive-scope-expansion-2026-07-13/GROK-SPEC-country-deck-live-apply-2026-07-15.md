# GROK SPEC — DiDi/inDrive country-deck live apply (new locked spine, two-anchor Egypt)

**Date:** 2026-07-15 (supersedes 2026-07-14 spec)
**Owner handoff:** Tasklet → Grok (deterministic model-to-deck live apply)
**Decks:** DiDi Brazil, DiDi Mexico, inDrive Brazil, inDrive Egypt
**Source state:** PR #271 (builder fix + regeneration) and PR #275 (inDrive Egypt two-anchor economics) are **both merged to `main`**. Package sources are canonical and preflight-green. Live decks still carry the OLD abolished 16-slide structure and MUST be restructured to the new locked spine.

## Why this is needed (literal state)
- The four committed package sets in `deck-studio/decks/{deck}/*` are regenerated to the new locked spine and pass local preflight.
- All four LIVE decks still show the abolished structure: per-city alternating economics slides, four Rio routes rendered as four city chapters, and the old TAM chart. The deterministic live apply below has not yet run.
- inDrive Egypt now renders **two** unit-economics slides (both approved Red Sea anchors), extending its spine from 11 → 12 slides (per PR #275).

## New locked spine (per merged builder)
cover → why-partner → ONE market overview → ONE slide per canonical city → **one-or-more contiguous unit-economics slide(s)** → TAM ladder → integration → rollout → ask → close

| Deck | Live deck ID | Slides | City slides | Econ slides |
|---|---|---|---|---|
| DiDi Brazil | `1OixKrHjQbWu0Plkvj-57SQyTFxPL5Ii8l3K6Q9umJOk` | 12 | Rio de Janeiro; Angra dos Reis & Ilha Grande (held); Florianópolis (held) | 1 |
| DiDi Mexico | `1XwKRuJtMrou8NtBdc1oY3LL2Dk83dCs9MCLvNKgwq0c` | 13 | Cancún & Isla Mujeres; Playa del Carmen & Cozumel; Puerto Vallarta (held); Los Cabos (held) | 1 |
| inDrive Brazil | `1QImIe6KAee0Eajsokgh9NmH0I29lir4l2LV63e-9OxE` | 12 | Rio de Janeiro; Angra dos Reis & Ilha Grande (held); Florianópolis (held) | 1 |
| inDrive Egypt | `1Nn3BRKUahikp87zC84JMdEVrcJYppm9ZXHgndAuzsEk` | **12** | Hurghada; Sharm El Sheikh | **2 (both anchors)** |

## Apply steps (deterministic, Slides API only)
1. **Refresh economics.** Run `deck-studio/decks/gen_deck_economics.py` for each deck against the current aggregate/routes/binding so `generated-deck-economics.json` is regenerated and its `source_sha256` hashes are current. inDrive Brazil shares the canonical Brazil route/cost basis with DiDi Brazil — figures must be identical; any Brazil-reference revision cascades to BOTH.
2. **Preflight.** Run `deck-studio/qa/preflight_country_mobility_review.py` on all four package dirs → must be PASS before touching live Slides. The gate now allows one-or-more contiguous unit-economics slides positioned after the city slides and before TAM; it still enforces exactly one market-overview and one TAM slide and rejects zero econ slides / wrong order.
3. **Duplicate/bind the approved Grab mobility reference** and restructure each live deck to the spine above. Do NOT wholesale-replace; Slides API only; no PPTX. Remove the abolished alternating per-city economics slides and the old TAM chart.
4. **Bind text** from each `deck.editplan.json` `slide_text` map; bind economics values from `generated-deck-economics.json` (never hand-typed).
5. **inDrive Egypt unit-economics slides (BOTH, two slides — no longer a single selection):**
   - **Giftun** `rn-b06f6971ed47` — 6.6 nm, N30 Pioneer II, $32 fare, $243,072 rev/boat, 70% margin, 3.55-yr payback.
   - **Ras Mohammed** `rn-c16a1627130f` — 11.7 nm, N30 Pioneer II, $50 fare, $298,440 rev/boat, 75% margin, 2.68-yr payback.
   - Both resolve `supported` from the canonical aggregate; render them as two contiguous slides in the order above (Giftun then Ras Mohammed), immediately after Sharm El Sheikh and before the TAM ladder. Do NOT render any "pending"/"Jaideep's choice" language.
6. **Egypt TAM slide:** render the 3-rung ladder exactly — Rung 1 floor ($8.50M pool / ~$7.42M Navier rev; label it the floor, not the market); Rung 2 Red Sea day-trip SAM ($21.3M–$33.4M Hurghada alone, 35–55% participation band on sourced arrivals); Rung 3 held null (Nile + Alexandria) in plain English. Never present the floor as the TAM; never use "below tourism economy → no inflation."
7. **Atlas route screenshot slots** stay unpopulated — human insertion only. Automation must not fill `asset_ref`/`asset_path`/`registry_key`/`target_object_id`. No visible placeholder text/labels/build instructions on any partner-facing slide.
8. **Partner logos** on cover per each `deck.config.json` `cover_logos` (banked DiDi / inDrive white cover logo + Navier wordmark).
9. **Copy gate.** Run `scripts/audit_partner_copy.py` and the deck copy lint as BLOCKING gates — zero internal process vocabulary; visible capitalized archetype chips limited to tourism / essential_mobility / luxury / super_app / ride_hail.
10. **Readback.** Pull each live deck inventory after apply, set each `deck.editplan.json` `apply_status` to `applied_and_live_inventory_read_back`, sync slide manifests to live object IDs, and return a QA receipt (deck ID, slide count, image provenance ledger, source-map coverage, unresolved gaps, no-op replay).

## Discipline
- Exact ID matching only; unsupported values `null`; no invented geography/piers/route IDs/demand/economics.
- No external release clearance claimed. Jaideep controls merge and final release.
- Immutable canonical totals: Brazil $23,404,822 / 113 vessels (4 routes); Mexico $14,759,160 / 88 vessels (3 routes); Egypt floor $8.50M pool / ~$7.42M Navier rev / 20 vessels (2 captive routes; Giftun + Ras Mohammed).
