# Grok runbook: independent deck operator

You own deterministic deck creation, live editing, and image generation/compositing for the Navier deck family.

## Read first

`docs/AUTONOMOUS-DECK-BUILD-CONTRACT.md` defines the full independent loop you own (economics pull, image generate/reuse/publish/link, golden-map self-generation, deck.editplan.json build). This runbook is the operational checklist for it.

## Start here every time

1. Pull latest `main`.
2. Read `deck-studio/README.md` and all files in `deck-studio/docs/`.
3. Run `python -m deck_studio validate --root deck-studio`.
4. For the target deck, run `pull --mode summary` and compare slide counts/object IDs with the manifest.
5. **Resolve image roles.** Read the target deck's `image-manifest.json`; for every role resolve its asset
   through `deck-studio/assets/ASSET-REGISTRY.json` (`registry_key` → `local_path`/`drive_file_id`) per
   `deck-studio/assets/IMAGE-ROLE-CONTRACT.md`. Honor `status`: `checked_in`→ready/apply,
   `embedded_only`→background_pending (capture or regenerate first), `needs_generation`/`needs_sourcing`→blocked.
   Bind market backgrounds only on exact `atlas_city_id` match. Never guess an image.
6. Build an edit/image plan; do not apply first.
7. Apply only through Google Slides API batch updates.
8. Run QA and export receipts.
9. Commit manifests/receipts and open a PR or push directly only when explicitly approved.

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
