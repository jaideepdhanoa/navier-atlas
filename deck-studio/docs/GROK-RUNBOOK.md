# Grok runbook: independent deck operator

You own deterministic deck creation, live editing, and image generation/compositing for the Navier deck family.

## Read first

`docs/AUTONOMOUS-DECK-BUILD-CONTRACT.md` defines the full independent loop you own (economics pull, image generate/reuse/publish/link, golden-map self-generation, deck.editplan.json build). This runbook is the operational checklist for it.

## Start here every time

1. Pull latest `main`.
2. Read `deck-studio/README.md`, all files in `deck-studio/docs/`, and `deck-studio/docs/NO-REEMBED-LINKED-ASSET-RULE.md`.
3. Run `python -m deck_studio validate --root deck-studio`.
4. For the target deck, run `pull --mode summary` and compare slide counts/object IDs with the manifest.
5. **Resolve image roles.** Read the target deck's `image-manifest.json` **and**
   `decks/{deck}/slide-image-bindings.json` (authoritative slide→object→role wiring). Resolve each role
   through `deck-studio/assets/ASSET-REGISTRY.json` (`registry_key` → `local_path`/`drive_file_id`) per
   `deck-studio/assets/IMAGE-ROLE-CONTRACT.md`. Honor `status`: `checked_in`→ready/apply,
   `embedded_only`→background_pending (capture or regenerate first), `needs_generation`/`needs_sourcing`→blocked.
   Bind market backgrounds only on exact `atlas_city_id` match. Never guess an image.
   - **Deck hyperlinks (white + underlined).** See `docs/DECK-LINK-BINDINGS.md`. Wire via
     `decks/{deck}/slide-link-bindings.json` + `builders/deck_link_bindings.py`:
     - Slide **3** `Interactive link` → partner Atlas hub `/{partner_id}`
     - Slides **4–6, 14–18** `Interactive link` → market sub-proposal or city page
     - Slides **7–9, 19–23** `Model deepdive` → `economics_url` (auto from `economics-binding.json`)
     - Slide **10** `Detailed market sizing` → same `economics_url`
     - Slide **13** body phrase `Navier × {Partner} Atlas` → partner Atlas hub (`close_atlas_link`,
       `link_style: inline_phrase` — white underlined inline link in body; title stays plain)
     Run `python builders/deck_link_bindings.py validate-bindings --deck {deck}` then `apply`.
   - **Slide-family gate (Grab gold template).** `econ_market_bg` binds **only** to `navierBg_*` on slides
     7–9 and 19–23 (full-bleed market-specific landmark skyline). Slides 4–6 and 14–18 =
     `atlas_route_screenshot` (Atlas capture — no generation). Capture via
     `python builders/deck_bolt_wave2_images.py capture-atlas-screenshots --serve-dist`
     (Playwright; URLs from `slide-link-bindings.json`). Run
     `python builders/deck_bolt_wave2_images.py validate-bindings` before any image apply.
   - **Unit-economics header eyebrow (slides 7–9, 19–23).** `WHAT ONE BOAT EARNS · {MARKET_LABEL}`
     must use the **full** `market_label` — never truncate (`CRO`/`AZUR`). Canonical char budget is
     31 (Singapore geometry), not Bali/Phuket sample budgets on slides 8–9.
     `python builders/deck_bolt_wave2.py validate-econ-headers`
     `python builders/deck_bolt_wave2.py apply-econ-headers`
   - **Market-slide route lists (slides 4–6, 14–18).** Four marquee routes per slide from
     `decks/{deck}/market-route-bindings.json` (sourced from partner JSON `journeys_unlocked`).
     Styling: amber `▸` bullet only, white route text, blank line between routes. Validate then apply:
     `python builders/deck_bolt_wave2.py validate-market-routes`
     `python builders/deck_bolt_wave2.py apply-market-routes`
   - **Prompt tiers.** `econ_unit_landmark` (full-bleed recognizable landmark skyline edge-to-edge),
     `cover` / `value_prop` / `tam` / `partner_roles` per `N30-TIER-A-PROMPTS.md`. Vessel must be
     **hydrofoiling** (foils deployed, hull elevated) — not displacement sitting on the water.
   - **N30 reference rule.** Any generated/composited N30 must match `assets/n30/n30-reference-neutral.png`
     for hull color/form and `assets/n30/n30-reference.png` for pose. **Lighting is a plate property** —
     keep the vessel neutral and let the market plate set time-of-day. See `docs/IMAGE-RULES.md`.
   - **Partner logo on cover (slide 1).** The `partner_logo` role is **required** for named-partner covers. Resolve it
     from `assets/logos/partners/{partner}/` via the registry. If unresolved, status `needs_sourcing` → blocked
     (never ship a named-partner cover without the partner logo, never guess one). For territory/Navier-only decks
     (`partner_logo: null`, e.g. Caribbean, French Polynesia, Hong Kong), keep the cover Navier-only.
   - **No re-embedding.** Apply every image from a registry-resolved stable image URL (`source_url` / approved Drive URL)
     bound to a `registry_key`. Never use a one-off embedded binary or a temporary Slides `contentUrl` as the source.
     If an asset is `embedded_only` or lacks a stable URL, regenerate/capture it into the pack, publish a stable URL,
     update the registry, then apply.
6. **Slide 3 (market overview KPIs).** Resolve the slide-3 KPI block from the deck's manifest/economics
   sidecar (see `IMAGE-ROLE-CONTRACT.md` slide-3 row); render the market-overview KPIs, do not leave stale.
7. Build an edit/image plan; do not apply first.
8. Apply only through Google Slides API batch updates.
9. Run QA and export receipts.
10. Commit manifests/receipts and open a PR or push directly only when explicitly approved.

## Context boundaries

- The repo is the source of truth for deck rules and current known deck IDs.
- Google Slides is the source of truth for live slide/object structure.
- Partner JSON, finance recal outputs, and live Google Sheets are sources of truth for claims/economics.
- The asset registry (`assets/ASSET-REGISTRY.json`) is the source of truth for image provenance and reuse.
- Do not ask Tasklet for hidden history. If something is missing, add it to this folder or mark it held-null.

## Deck IDs

- French Polynesia × Navier: `1u1_p8hOT3cNYZsucAEnCypowJV8BduXR5ytGsm1LtO0`
- Careem x Navier: `1Mut8qzpW-8Pd989hGS7fgskY1SuQICxVflIlHP-zonQ`
- Grab × Navier: `18yDAgO0Sj9PJlgf6paxtgni8Pk1xRAmNwE2TD_NCdSs`

## Hospitality / single-market decks (Ocean Whisperer pattern)

Do **not** treat hospitality as “text-only.” The same **deck-level image roles** as Bolt are mandatory:

| Step | Command / artifact |
|------|-------------------|
| Gap check vs Bolt | `decks/{deck}/WAVE2-GAP-MATRIX.md` |
| Slide 2 insert | `python builders/deck_{deck}.py insert-slide2` |
| Deck plates (cover, slide2, Three C's, TAM, partner-roles) | `deck_{deck}_images.py generate-all` + `publish` |
| Slide 2 narrative | `narrative-binding.json` + `deck_narrative_slide2.build_narrative_paint_ops` (gold `narr2_*` style pins — never flat 11pt) |
| Slide 3 KPI captions | Center-align caption object_ids (`g3eec5122801_0_7/_11/_16/_19`); values stay as-is |
| Market route lists (5–7, 12) | `market-route-bindings.json` + `deck_market_routes.py` — amber `▸`, white body, `\n\n` between blocks, distance lines **not bold** |
| Single-market econ bg | Tier-A integrated vessel (`econ-{market}-v1`) on **all** `navierBg_s23`–`s25` — **never** paste-composite overlay; repaint corridor economics from `agg-*.json` |
| Close slide (14) | **Only** `close_atlas_link.body_text` from `slide-link-bindings.json` — never concatenate partner `close.body` prose |
| Atlas side-panels | `slide-image-bindings.json` + `capture_atlas_screenshots.py` |
| Hyperlinks | `slide-link-bindings.json` + `deck_link_bindings.py` |

**Failure mode we hit on OW:** only slide 7 bg + text; slides 8–9 kept Grab Phuket/Bali paintbrush plates; slide 10 TAM text without `tam_bg`; slide 11 partner-roles without `partner_roles_bg`; no cover hero; no slide 2.

## Stop conditions

Stop and request human review if:

- a requested edit requires external sending,
- a source claim conflicts with the model/Sheet,
- a live deck has a different slide count from the manifest and the difference is not explained,
- an edit would replace the whole deck,
- an image lacks reproducible provenance,
- or a route/economics value cannot be sourced.
