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
   - **Slide-family gate (Grab gold template).** `econ_market_bg` binds **only** to `navierBg_*` on slides
     7–9 and 19–23. Slides 4–6 = `atlas_route_screenshot` (human Atlas capture). Slides 14–18 =
     `market_showcase_bg` (iconic Tier-A scene). Run
     `python builders/deck_bolt_wave2_images.py validate-bindings` before any image apply.
   - **Prompt tiers.** `econ_unit` (muted chart backdrop + soft landmark), `market_showcase` (iconic +
     foiling), `cover` / `value_prop` / `tam` / `partner_roles` per `N30-TIER-A-PROMPTS.md`. Vessel must be
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

## Stop conditions

Stop and request human review if:

- a requested edit requires external sending,
- a source claim conflicts with the model/Sheet,
- a live deck has a different slide count from the manifest and the difference is not explained,
- an edit would replace the whole deck,
- an image lacks reproducible provenance,
- or a route/economics value cannot be sourced.
