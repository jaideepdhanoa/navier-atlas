# GROK SEAL — Grab Thailand slide 11 TAM-ladder background

## Why
Slide 11 (the TAM ladder, slide object `g3eec5122801_0_562`) now carries a
**user-inserted Phang Nga Bay dusk aerial** as its background. It was dropped onto the
deck as a raw image object (`g3f253f18ba8_1_0`) with **no `sourceUrl`** — i.e. an
embedded blob backed only by a transient `slidesz` render URL. Per our image discipline,
final deck images must be **registry-resolved stable assets**, never re-embedded one-offs.

Tasklet has captured the live render into a checked-in asset and registered it. Grok owns
the Drive publish + stable rebind.

## Asset (already checked in by Tasklet)
- Registry key: **`grab-thailand-tam_bg`** (role `tam_bg`, deck `grab-thailand`)
- Local path: `deck-studio/assets/backgrounds/decks/grab-thailand/grab-thailand-tam_bg-phang-nga.png`
- Dimensions: `1920x1088` · sha16 `395469456a80c17a`
- `drive_file_id`: `null` · `status`: `needs_drive_publish`
- Live object captured from: `g3f253f18ba8_1_0`

## Grok steps (deterministic)
1. **Publish** `grab-thailand-tam_bg-phang-nga.png` to Drive (Navier deck-assets folder);
   record `drive_file_id` + `source_url` (`https://drive.google.com/uc?export=download&id=…`)
   back into the `grab-thailand-tam_bg` registry entry; flip `status` → `banked` and clear
   the `open_gaps.grab_thailand_tam_bg` note.
2. **Rebind** slide 11's background to the registry-resolved image so it no longer depends on
   the embedded blob:
   - Replace the embedded image object `g3f253f18ba8_1_0` with a registry-resolved
     `createImage`/`replaceImage` from the stable `source_url` (full-bleed,
     `CENTER_CROP`, behind the ladder text + Navier wordmark `g3eec5122801_0_588`).
   - Slides-API only. No PPTX round-trip, no full-deck replace, preserve all other object IDs.
3. **Optional (nice-to-have):** add a slide-11 `bg_oid` binding to
   `deck-studio/builders/deck_grab_thailand.py` keyed to `grab-thailand-tam_bg` so a future
   from-scratch rebuild binds this background automatically (today the builder writes the
   ladder text but does not manage the slide-11 background).
4. Re-run `deck-studio/qa/partner_copy_lint.py` (must stay green) and return a render receipt
   (deck id, slide 11 thumbnail, image provenance ledger showing the stable `source_url`).

## Guardrails
- This is an image publish/rebind only — **do not** rebuild the deck or touch the corrected
  econ slides (8/9/10) or the Samui map slide; those were directly edited and persisted in
  source (PR #102).
- Market-specific background, minimal gold accents, canonical N30 rules unaffected (no N30 in
  this plate). Do not substitute an Atlas-generated image.
