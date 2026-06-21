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
