# N30 Image Integration — Addendum for Grok (wave-2.1)

**Context:** Grok correctly diagnosed the *primary* failure (background+paste instead of
reference-guided integration). This addendum adds **four defects Grok's note did NOT name**, plus the
**explicit PASS/FAIL exemplar pair** that should anchor the visual QA loop. Source of truth for the look
is the **Grab gold deck**; the Bolt wave-2 plates are the counter-example.

The standing image rules still hold: **canonical N30 compositing, market-specific backgrounds, no
Atlas-generated images, minimal gold accents, no full-replace / PPTX round-trip, do not embed
inaccessible images (use stable URLs / true alpha assets, never a rectangle with its own scene inside).**

---

## The exemplar pair (pin these in the QA loop)

| | **PASS — Grab gold** | **FAIL — Bolt wave-2** |
|---|---|---|
| **Cover (slide 1)** | N30 fully integrated in Marina Bay (Singapore): foils down, **wake + waterline interaction + reflection**, warm dusk grade, **exactly one** vessel, correct local landmark (MBS). | "The water network for **Europe**" over an unmistakable **Dubai** skyline (Burj Khalifa + Burj Al Arab + Palm villas). **Two** vessels. A **translucent pasted rectangle** with a *different* (green-island) scene visible inside its bounding box. |
| **Slide 2 (Cost/Comfort/Convenience)** | Phang Nga / Andaman karsts, integrated N30, **and a woman standing on the berth looking at her phone — booking the ride.** The human booking-moment IS the slide. | Croatia marina, but the N30 is the same **see-through pasted rectangle** (you can read the dock through the hull), visible bounding box, **no human, no booking moment.** |

If a generated plate looks like the FAIL column in *any* respect, reject before Drive/replaceImage.

---

## The four defects beyond "paste vs integrate"

### 1. The neutral reference PNG still carries its own background → it can never be pasted cleanly
The translucency + the green tropical island visible *inside* the Bolt vessel is the tell: `n30-reference-neutral.png`
is a **rectangular plate with a scene baked in**, not an alpha-cut vessel. Two consequences:
- **Tier A (preferred):** feed it as a *form/colour reference* to an `image_edit`, never as a layer to paste.
- **Tier C fallback only:** if compositing at all, use a **true transparent-background alpha cutout** of the hull
  (no sky, no water, no island inside the silhouette) and composite at **100% opacity**. A see-through hull is an
  automatic fail. Produce/check in `n30-reference-neutral-ALPHA.png` (background fully removed) before any Tier-C run.

### 2. Geography must match the deck's market — and not leak a different region
"Europe" cover showing **Dubai** is both a geography-read failure **and** a Gulf-leak on a Europe surface. Lock a
**market→scene map per partner** and gate on it:
- **Bolt → recommended beachhead is Greece / the Aegean.** The cover should read **Santorini caldera / an Aegean
  island pier**, not the Gulf. (Bolt's Europe/Gulf baseline is source-backed, but the *cover* leads with the Greece/Aegean
  beachhead; Gulf scenes belong only on explicitly Gulf slides.) No Dubai, no Burj on a Europe cover.
- Add a **leak check** for skyline landmarks, not just text/logos: Burj Khalifa/Al Arab, Marina Bay Sands, Grab/SEA
  residue, etc. A recognizable wrong-market landmark = fail.

### 3. Exactly ONE N30 per scene
The Bolt cover has two boats (a roughly-integrated one at left **and** the pasted rectangle center). If the base plate
already contains a vessel, the integration step must **not** add another. One hull, every time.

### 4. Slide-2 prompt is missing the mandatory human booking-moment
This is a **template gap, not a one-off.** The slide-2 prompt must require:
> *A woman standing on the wooden berth/pier in the **foreground left third**, looking down at her phone **booking the
> ride** — natural candid posture, not facing camera, soft daylight. She anchors the "convenience / in your app" story.*
Without her, slide 2 loses its entire narrative point. Add this line to the slide-2 prompt for **every** partner deck
(it's already true in the Grab gold).

---

## Slide-family wiring (wave-2.1 lesson)
Wave-2.1 mis-bound `econ_market_bg` plates to **market side-panel** slides (4–6, 14–18) instead of
**unit-economics** full-bleed slots (`navierBg_s23`–`s39` on slides 7–9, 19–23). Fix: use
`decks/bolt/slide-image-bindings.json` as the single source of truth; run `validate-bindings` before apply.

| Wrong (wave-2.1) | Correct |
|---|---|
| Econ plate on slide 4 `g3eec5122801_0_107` | Atlas screenshot (human) on 4–6 |
| Econ plate on slide 14 `g3eec5122801_0_676` | `atlas_route_screenshot` (human capture) on 14–18 |
| — | `econ_market_bg` on `navierBg_s23`–`s39` (slides 7–9, 19–23) |

## Grading / integration spec (match the Grab gold)
- **Foils deployed** (in the water), hull **elevated** on foils, visible **foil wake** — actively hydrofoiling.
- **Warm golden-hour / dusk grade**; rim light on the hull consistent with the scene's sun direction.
- Hull form locked to the neutral reference: **white/light hull, glass cabin, V-mark, 8-seat Pioneer II scale.** No
  hull/cabin/V-mark drift.
- **16:9**, foreground subject placement that survives the slide crop and doesn't collide with the title text (the Bolt
  cover title overlaps the hull — keep the hull clear of the headline band).

## Quality gate (extend Grok's table)
Add to Grok's existing 5 checks:
- **Opacity** — hull is 100% opaque; nothing visible *through* it. (catches defect 1)
- **Single vessel** — exactly one N30 in frame. (defect 3)
- **Market lock** — scene matches the partner's beachhead market; no wrong-region landmark. (defect 2)
- **Human booking-moment** — present on slide 2. (defect 4)
- **No bounding box / seam** — no rectangular edge around the vessel.

## Process
- **Tier A** (reference-guided `image_edit` with the neutral N30 as form reference) is the primary path. The note that
  this environment's `GenerateImage` lacks `reference_image_paths` is exactly why wave-2 fell back to paste — run Tier A
  in the **Grok Build / Imagine** workflow that supports an attached reference.
- Save provenance per accepted plate (prompt + reference paths + provider + output) to `ASSET-REGISTRY.json`; mark the
  wave-2 paste plates `deprecated_paste_composite`.
- Human spot-check thumbnails **before** `replaceImage`. Image-ops only on re-apply — don't rebuild the editplan.

**Start with the Bolt Greece/Aegean cover as the bar-setter** (it fixes defects 1, 2, 3 at once), then slide 2 with the
human booking-moment, then roll the rest in market priority.
