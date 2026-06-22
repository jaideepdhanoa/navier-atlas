# Image generation and compositing rules

Image generation is allowed for candidate backgrounds, moodboards, and market-specific context. Final deck images must be deterministic enough to recreate from saved inputs.

## Canonical approach

1. Select or generate a market-specific background.
2. Use the canonical N30 vessel reference from `assets/n30/` (see N30 reference rule below) or the referenced Drive asset registry.
3. Apply a saved mask if needed.
4. Composite with the deterministic helper in `builders/images/n30_composite.py`.
5. Save the output and provenance in the deck's `image-manifest.json`.
6. Apply to the live deck using Slides API image replacement only. Use a stable registry/Drive URL; never use embedded-only blobs or temporary Slides content URLs.

## N30 reference rule (canonical)

The canonical N30 is defined by the vessel already composited into our shipped market plates
(not by any uploaded investor/hospitality-deck render). It lives in `assets/n30/`:

- **`n30-reference-neutral.png`** — **FORM + COLOR** reference. Match the vessel to this:
  light/white hull, glass cabin with V-mark, foils down, daylight read.
- **`n30-reference.png`** — **POSE + STANCE** reference only (bow-left rear-quarter). It carries
  koh-samui dusk tint; **do not** match lighting to it.
- **`n30-reference-bowright.png`** — alternate **POSE** (bow-right), from langkawi.

**Lighting is a plate property, not a vessel property.** The dusk/sunset/navy tone comes from the
market background plate + the navy gradient overlay, applied per market. Generate/composite the N30
**neutral**, then let the market plate set the time-of-day. Never bake one market's sunset into the
vessel reference or into other decks. Provenance: `derived_from_shipped_plate` (reproducible).

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


## No-reembed linked-asset rule

Final images must be applied from a stable URL recorded in `assets/ASSET-REGISTRY.json` (`source_url` / approved Drive URL).
If an asset only has `local_path`, publish it to the approved linked-image location and record the resulting URL before
editing the live deck. If an asset is only visible as a live Slides `contentUrl`, it is **not reusable**; regenerate or
capture it into the asset pack first.
