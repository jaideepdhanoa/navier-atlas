---
name: partner-deck-grok-handoff
description: Prepare Grok-ready partner deck packages from existing Navier proposal/economics assets. Use when a partner needs Deck Studio configs, slide briefs, image manifests, and deterministic deck creation instructions.
---

# Partner Deck Grok Handoff Playbook

Use this skill when the partner proposal/economics lane already exists and the next job is to prepare Grok to create or bind a live partner deck. This skill does **not** declare the full proposal complete; it creates a deterministic deck handoff that Grok can apply through live Google Slides only.

## Operating rules

1. **Source of truth first:** read the repo-native partner JSON, data-clean partner JSON, finance/growth files, sheet binding, existing Deck Studio files, and handoff status before writing deck artifacts.
2. **No route invention:** route IDs, city IDs, boarding points, and corridor geometry remain null or pending unless already sealed by ID. Grok handles deterministic ID sealing/render QA.
3. **Existing economics, not guessed economics:** deck copy can reference existing aggregate/growth/sheet assets. Missing economics URL or sidecar becomes a deck gap, not a made-up number.
4. **Slides API only:** live deck edits must be via Slides API. No PPTX round-trip, no full replacement, and no manual visual drift.
5. **Image discipline:** canonical N30/N35 compositing, market-specific source-approved backgrounds, minimal gold accents, no Atlas-generated images, and saved provenance for every image.
   - **N30 reference:** the canonical N30 is the vessel composited into our shipped market plates, banked in `deck-studio/assets/n30/`. Match hull/form to `n30-reference-neutral.png` and pose to `n30-reference.png`. **Lighting is a plate property, not a vessel property** — keep the N30 neutral and let the market plate set time-of-day. Do not use uploaded investor/hospitality-deck renders as the N30 reference.
   - **Save-to-repo + reuse:** save every generated/sourced asset into the repo by market/deck under `deck-studio/assets/`, register it in `ASSET-REGISTRY.json`, and reuse it for future decks. Use existing market assets as the reference for new ones. Embedded-only visuals must be captured into checked-in/registry-resolved assets — never re-embedded.
   - **Partner logo on cover:** every *named-partner* deck must carry the partner's logo on the cover (slide 1), banked under `assets/logos/partners/{partner}/` with a `LOGO-SOURCE.json` provenance file. Required, not optional; `needs_sourcing` (blocked) if it cannot be sourced cleanly — never guess a logo. **No-logo exception:** territory/tourism decks with **no named partner** (e.g. Caribbean, French Polynesia, Hong Kong) ship a **Navier-only cover** (wordmark + title, `partner_logo: null`) — do not invent or badge a government/tourism logo. Per-deck status lives in `assets/logos/LOGO-MANIFEST.json` and the `cover_logos.partner_logo.status` field of each `deck.config.json` (`banked` / `needs_sourcing` / `no-logo` / `needs_decision`).
6. **Exactness over coverage:** null beats confidently wrong. Country/region-supported claims can be narrative-only; slide-level claims need source paths.
7. **Deck-ready is not proposal-complete:** use `deck-prep-complete / grok-create-or-bind-needed` for Tasklet deck artifacts. Use `proposal-complete` only when proposal parity, seal/render QA, economics cascade, sidecar, and delivery receipts all exist.

## Required per-partner artifacts

Create or update these under `deck-studio/decks/{deck_key}/`:

- `deck.config.json` — deck identity, pending or live deck ID, source paths, rules, economics URL if known.
- `slide-manifest.json` — planned slide sequence and object-inventory status. If no live deck inventory is pulled, mark `stale_requires_pull`.
- `content-source.json` — narrative source map from partner JSON/economics/handoff artifacts to each planned slide.
- `image-manifest.json` — image placeholders, N30/N35 composite requirements, background rules, and provenance requirements.

Create or update batch handoff artifacts under `handoff/partner-map-model/{batch}/`:

- `partner-deck-grok-readiness-queue.json`
- `partner-deck-source-map.json`
- `GROK-PARTNER-DECK-CREATION-PROMPT.md`
- `PARTNER-DECK-GROK-HANDOFF-STATUS.md`

## Deck archetypes

Pick the archetype before building the sequence — it sets the route rule, economics frame, and slide content:

- **Mobility / super-app distributor** (Grab, Bolt, Careem, Yango): use the **Standard deck sequence** below as-is. City-mobility TAM, contested capture band, airport/commute/premium use cases.
- **Hotel/resort operator-developer** (Minor, Aman, Four Seasons, Constance, …): use [`OPERATOR-DEVELOPER-ARCHETYPE.md`](./OPERATOR-DEVELOPER-ARCHETYPE.md). Captive property-graph routes only (gateway→property, property↔property, property→excursion), captive economics (capture ~0.85–0.90, LB-254), headroom = WIDTH (keys/openings/clusters). It keeps the 11-slide skeleton and all base rules, and overrides only the content frame of slides 2, 3, 4, 5, 7, 9.

## Standard deck sequence

Use this 11-slide base (mobility/super-app archetype) unless a partner has an approved different live template:

1. Hero: why this partner × Navier now. **Cover must carry both the Navier logo and the partner logo** (`navier_logo` + `partner_logo` roles), plus the market-anchored N30 cover hero.
2. Why this partner: distribution, demand, and strategic fit.
3. Market overview KPIs + validated footprint: source-backed market-overview KPIs (`market_overview_kpis` role — market size, fleet/route counts, demand/fare anchors, resolved from the economics sidecar/transparent sheet) alongside source-backed markets and explicit holds. Never leave the KPI block stale.
4. Launch-market candidates: exact-bound markets first, candidate markets second.
5. Use cases and journeys unlocked: airport/waterfront, commute, premium transfer, logistics/commerce, or authority use case as appropriate.
6. Navier product and fleet fit: N30/N35 for ≤70nm, Quanta-LR only for range-gated roadmap legs.
7. Economics: aggregate/growth/sheet/sidecar references; no unsupported numbers.
8. Partner integration model: demand, booking/payment, operating split, and go-to-market.
9. Rollout plan: prove → scale → mature, using existing phase economics where present.
10. Grok-sealed route appendix: route IDs, render receipts, duplicate checks, unresolved gaps.
11. Next steps: bind/create deck, pull inventory, apply via Slides API, return QA receipts.

## Grok handoff checklist

The Grok prompt must instruct Grok to:

- bind or create the live Google Slides deck ID;
- pull the full slide/object inventory before edits;
- apply the planned deck through Slides API only;
- preserve existing live deck objects unless explicitly instructed;
- use only source-backed partner JSON/economics/handoff claims;
- leave unknown route IDs, city IDs, sheet IDs, and images as pending/null;
- include the partner logo on the cover (`partner_logo`, required) and populate the slide-3 market-overview KPIs from the economics sidecar;
- run `deck-studio/qa/partner_copy_lint.py` as a **blocking** gate (same status as the land-crossing gate) — no internal taxonomy in rendered slide text; do not apply/seal until green;
- apply every image as a registry-resolved element; never re-embed a one-off binary (capture + register embedded-only assets first);
- use N30/N35 composites only with market-specific approved backgrounds, matching the N30 reference (neutral hull/form; lighting set by the plate);
- return a QA receipt with deck ID, slide count, image provenance ledger, source-map coverage, render receipts, unresolved gaps, and no-op replay result.

## Unit-economics OPEX (6-line) rule

The run-cost table on the economics slide has **six flush OPEX lines** in order: Energy · Captain/crew · Marina+overhead · Maintenance · **Insurance** · **Charging berth** · (Total run cost/yr). Insurance and Charging berth must be flush-left in the same label column — never indented as Maintenance sub-items.

If a line renders indented, do not patch its paragraph indent: delete and recreate a flush duplicate of a correctly-formatted line (label + value), matching the run-cost column transform and Exo 2 / Poppins style. Recreating a line mints a **new object-id family** (deck-native `g3eec…` vs recreated `g3f21…`), so OPEX object IDs must be **read live per slide before any edit** — never assumed across slides. `null` beats a confidently-wrong ID. Record per-slide OPEX IDs in `deck-econ/econ-field-ids.<deck>.json`. New decks (Careem, French Polynesia, …) must emit all six lines flush from the start.

## Validation gate

Before reporting the batch as Tasklet deck-prep complete:

- all JSON files parse;
- `deck.config.json`, `slide-manifest.json`, and `image-manifest.json` pass the Deck Studio schemas;
- every deck has source paths to partner JSON and economics artifacts where they exist;
- every slide has a content-source entry;
- every image placeholder has `provenance_required: true`;
- the status file names remaining Grok-owned holds separately from Tasklet-owned deck prep.

## Reporting language

Good: “Tasklet deck-prep artifacts are complete for these partners; Grok create/bind/render QA remains.”

Bad: “The partner decks are complete” before live decks, render receipts, image provenance, and QA receipts exist.

## Definition of done for this skill

Tasklet is done with the deck-prep lane when each requested partner has schema-valid Deck Studio artifacts, a batch handoff prompt, a source map, a readiness queue, and a status note. The deck itself is done only after Grok or the live deck workflow returns create/bind/apply/render QA receipts.
