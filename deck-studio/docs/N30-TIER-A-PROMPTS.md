# N30 Tier-A Prompt Strings — Bolt cover + slide 2 (+ reusable template)

Run these as **`image_edit`** with the **N30 neutral reference attached** (`n30-reference-neutral.png`,
bow-left; use `n30-reference-bowright.png` when a scene needs the opposite heading). The reference is a
**form/colour reference only** — never a layer to paste. Every prompt below ends in the same hard
constraints (single integrated photo, hull locked, in-water with reflection, no leak).

---

## 1. Bolt — Cover (slide 1) · Greece / Aegean beachhead
**Reference:** `n30-reference-neutral.png` (bow-left)

> Using the attached white hydrofoil vessel as the **exact form and colour reference**, produce a single
> photorealistic 16:9 photograph. Foreground: the vessel cruising on calm deep-blue Aegean water, **foils
> down**, with a light bow wake and a clean reflection on the water, seen in **rear three-quarter view, bow
> angled left**. Background: a classic Cycladic / Santorini caldera scene — white-washed buildings with
> blue domes terraced up volcanic cliffs, soft sea haze. **Warm golden-hour sunlight from the left**, gentle
> rim light along the white hull. Place the vessel in the **lower-center / left** of the frame and keep the
> **upper-left third clear** for a headline. **Exactly one vessel in frame.** Keep the hull form, glass cabin,
> and the small V-mark on the bow **exactly as the reference — do not alter the vessel design.** The boat must
> sit **in the water** with correct waterline contact and reflection, **never pasted on top**, no rectangular
> edge or seam. Single integrated photograph, not a collage. **No people, no logos, no text, no other boats.**
> Negative: no Dubai/Gulf skyline, no Burj Khalifa or Burj Al Arab, no Marina Bay Sands, no Grab/SEA signage.

## 2. Bolt — Slide 2 (Cost · Comfort · Convenience) · the human booking-moment
**Reference:** `n30-reference-neutral.png`

> Using the attached white hydrofoil vessel as the **exact form and colour reference**, produce a single
> photorealistic 16:9 photograph at an **Aegean island berth**. Foreground: a wooden/stone jetty with the
> white hydrofoil vessel **easing up to the berth** on calm blue water, **foils down**, clean reflection. In
> the **foreground left third**, a **woman stands on the berth looking down at her phone, booking the ride** —
> natural candid posture, light summer clothing, seen from **behind / three-quarter, not facing the camera**.
> Soft warm morning daylight. Behind: white Cycladic buildings and blue sea. **Exactly one vessel.** Keep the
> hull form, glass cabin, and bow V-mark **exactly as the reference — do not alter the vessel design.** The boat
> sits **in the water** with correct waterline and reflection, **never pasted**, no seam or bounding box. Single
> integrated photograph, not a collage. **No logos, no text, no brand signage, no other boats.**

---

## 3. Reusable per-market template (all partners)
Swap `{SCENE}` and `{LIGHT}`; keep everything else identical. Add the **booking-moment clause** for any
slide-2 / convenience plate.

> Using the attached white hydrofoil vessel as the **exact form and colour reference**, produce a single
> photorealistic 16:9 photograph. Foreground: the vessel on calm water, **foils down**, light wake + clean
> reflection, rear three-quarter view. Background: **{SCENE}**. **{LIGHT}.** Place the vessel lower-center,
> keep the upper-left clear for a headline. **Exactly one vessel.** Keep hull/glass cabin/bow V-mark **exactly
> as the reference — do not alter the design.** Boat sits **in the water** with correct waterline + reflection,
> **never pasted**, no seam. Single integrated photograph, not a collage. No logos, no text, no other boats.
> *(Slide-2 / convenience add:)* In the foreground left third, a person stands on the berth looking at their
> phone **booking the ride**, candid, not facing camera.

### Bolt market→scene map (geography lock + leak guard)
| Market | `{SCENE}` | Notes |
|---|---|---|
| **Greece / Aegean** *(cover + beachhead)* | Cycladic/Santorini caldera, white+blue-dome cliffs | **Lead with this.** |
| **Croatia** | Dalmatian coast — Hvar / Dubrovnik old-town stone waterfront, pine islets | |
| **Côte d'Azur** | Nice / Cannes / Monaco harbour, belle-époque façades, super-yachts | |
| **UAE / Gulf** | Dubai Marina towers | **Only on explicitly-Gulf slides** — never on a Europe cover. |

`{LIGHT}` default: *warm golden-hour sun from the left, soft rim light on the white hull.*

---

## 4. Prompt tiers by slide family (all partners on Grab gold template)

| Tier | Role | Slides | Look |
|---|---|---|---|
| `cover` / `value_prop` / `tam` / `partner_roles` | deck narrative | 1, 2, 10, 11 | Aspirational, golden-hour, iconic when applicable |
| `atlas_route_screenshot` | market side-panel | 4–6, 14–18 | **No generation** — screenshot from Vercel Navier Atlas |
| `econ_unit_landmark` | `econ_market_bg` | 7–9, 19–23 | Left 42% calm for charts; right 58% recognizable market landmark skyline; small foiling N30 lower-right |

**Foiling rule (all tiers with a vessel):** foils *deployed in the water*, hull *elevated above the
waterline*, visible struts and foil wake. Never depict a displacement ferry sitting low. “Foils down” in
legacy docs means foils lowered **into** the water for foiling — not retracted/displacement mode.

Wiring: `decks/{deck}/slide-image-bindings.json` + `builders/deck_slide_bindings.py`.

---

## Before apply
QA each plate against the gate in `N30-IMAGE-INTEGRATION-ADDENDUM.md` (opacity 100%, single vessel, market
lock, human booking-moment on slide 2, no seam, hull form matches the neutral reference). Save provenance to
`ASSET-REGISTRY.json`; human thumbnail spot-check before `replaceImage`. Image-ops only on re-apply.
