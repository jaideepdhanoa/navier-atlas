# Image generation and compositing rules

Image generation is allowed for candidate backgrounds, moodboards, and market-specific context. Final deck images must be deterministic enough to recreate from saved inputs.

## Canonical approach

1. Select or generate a market-specific background.
2. Use the canonical N30/N35 vessel asset from `assets/n30/` or the referenced Drive asset registry.
3. Apply a saved mask if needed.
4. Composite with the deterministic helper in `builders/images/n30_composite.py`.
5. Save the output and provenance in the deck's `image-manifest.json`.
6. Apply to the live deck using Slides API image replacement only.

## Forbidden

- No Atlas-generated images.
- No untracked generated images in final decks.
- No prompt-only provenance; save prompt, seed if available, provider, source files, mask, compositor args, and output path.
- No watermarks, logos, UI chrome, fantasy vessels, or impossible hull/scale depictions.

## Deterministic final asset rule

The generative step can produce candidates. The accepted deck image is the result of a saved source image + saved vessel image + saved mask + deterministic compositor settings.

## Asset registry & role contract (authoritative)

Every deck's images are governed by two files:

- **`assets/IMAGE-ROLE-CONTRACT.md`** — the fixed per-deck image roles: `cover_hero` (slide 1),
  `navier_logo` (slide 1), `partner_logo` (slide 1), `value_prop_bg` (slide 2), `tam_bg` (slide 10),
  `partner_roles_bg` (slide 11), and `econ_market_bg` (slides 7–9, 19–23, reusable by Atlas city ID).
- **`assets/ASSET-REGISTRY.json`** — the master index. Each `image_key` carries `role`, `scope`,
  `atlas_city_id` (exact-bind only; null ⇒ not yet bindable), `local_path` / `drive_file_id` / `source_url`,
  `provenance`, `license`, and `status`.

### Resolution rule (deck edit plans)

A `deck.editplan.json` object's `image.registry_key` MUST resolve to an `ASSET-REGISTRY.json` `image_key`.
Map the registry `status` to the plan `image.status`:

| registry status | plan status | meaning |
|---|---|---|
| `checked_in` | `ready` | binary present under `assets/`, apply via Slides API |
| `embedded_only` | `background_pending` | image exists on live deck but has no stable/reproducible source — capture or regenerate before re-applying |
| `needs_generation` / `needs_sourcing` | `blocked` | no asset yet; never guess, leave null |

Reusable market backgrounds bind to a slide **only** on exact `atlas_city_id` match (null beats confidently-wrong).
Logos are the only non-composite assets and live under `assets/logos/`.
