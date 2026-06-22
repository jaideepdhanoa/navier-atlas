# N30 Deck Image Library — prompts + evals for every image type

Companion to `N30-IMAGE-INTEGRATION-ADDENDUM.md` (the why) and `N30-TIER-A-PROMPTS.md` (cover + slide 2).
This file covers **every other image archetype** in a partner deck so Grok can generate the whole set at
Grab-gold quality, not just the hero plates. **Tier A `image_edit` with `n30-reference-neutral.png` attached
is primary for every plate.** Each archetype below = **role → composition/safe-zone → prompt → negatives →
eval gate.**

---

## 0. Global rules (apply to EVERY plate — enforce in `qa_image_gate()`)
- **16:9**, render at **≥ 2560×1440** (crisp on 1080p+ projectors); never upscale a small gen.
- **N30 from the neutral reference** (Tier A), **foils down**, **in the water** with waterline + wake +
  reflection, **never pasted / no seam / no bounding box**, hull+cabin-glass+bow-V-mark **locked to ref**.
- **Exactly one vessel.** Scale/ambition is carried by **geography + light**, never by a fleet of boats.
- **Market lock + landmark denylist** (no Burj Khalifa/Al Arab, no Marina Bay Sands, no Grab/SEA residue;
  Gulf scenery only on explicitly-Gulf slides).
- **No baked logos or text** — partner logos and all copy are placed by the Slides renderer into a clean
  zone, never painted into the image. **No Atlas/map graphics** baked into a photo.
- **Deck coherence:** once the cover passes, **lock the grade + time-of-day + seed family** for the whole
  deck. Every plate in one deck should read as the same world (same golden-hour family), not a patchwork.
- **Minimal gold accents**; premium, photographic, not CGI/render-y.
- Save provenance (prompt, ref paths, provider, **tier**, seed) → `ASSET-REGISTRY.json`; publish to Drive
  for a **stable `source_url`**; **image-ops only** on re-apply (no editplan rebuild).

> **Safe zones**: every prompt names the region that must stay **clean/low-detail** so the renderer's text,
> KPIs, chart, ladder, or logo lockup lands on calm pixels. Treat the safe zone as a hard composition rule.

---

> **Slide order (after exec-summary insertion):** 1 cover → **2 exec-summary/thesis** → 3 convenience
> (booking-moment) → 4 market KPIs → econ slides → TAM → partner-roles. **Role is canonical; the numbers
> below are post-insertion.** The economics binding (`economics-binding.json`) is the source of truth for
> actual slide indices — every role from convenience onward shifts +1 vs the pre-insertion deck.

## A. Cover · slide 1 → see `N30-TIER-A-PROMPTS.md §1`
Safe zone: **upper-left third** clear for the headline. Eval: defects 1–3 fixed (opacity/single/market).

## A2. Executive-summary / thesis · slide 2
**Role:** the **strategic-story** backdrop behind the partner thesis (see `SPEC-deck-narrative.md` /
`gen_deck_narrative.py`). It carries the proposal's positioning + "Your World" beats, so it must read
**premium and confident but stay quiet** — a lot of distilled copy sits on top.
**Composition / safe zone:** vessel **lower-right, mid-distance** in the deck-locked market scene; the
**left ~55% and a calm lower band** stay open, low-detail, gently darkened for the headline + thesis + the
four "Your World" blocks + a stat strip. This is a **text-heavy** slide — protect the type more than the cover.

> Using the attached white hydrofoil vessel as the exact form/colour reference, produce a single
> photorealistic 16:9 photograph in the deck's locked grade. The vessel cruises calmly in the **lower-right
> third** with **{MARKET_SCENE}** softly behind it. The **left ~55% of the frame and a lower band are open,
> calm, low-detail water and sky with a soft dark gradient**, so a headline, several short paragraphs, and a
> row of stat chips overlaid there stay fully legible. Foils down, clean reflection, exactly one vessel,
> hull/cabin/V-mark exactly as the reference, in-water with no seam. Muted, premium, photographic — quiet
> enough to sit behind dense copy. Single integrated photograph, not a collage. No people, no logos, no text.

**Eval:** **left-55% + lower band** low mean luminance + low variance (auto histogram) → dense copy legible;
single vessel; **market lock** (same scene family as the cover, no leak); **no baked logos/text** (all copy +
the stat strip are renderer-placed from the narrative sidecar); grade matches the locked cover.

## B. Convenience · slide 3 (the booking-moment) → see `N30-TIER-A-PROMPTS.md §2`
Mandatory: **woman on the berth booking on her phone**, foreground left third. Eval: defect 4 present.

---

## C. Market-overview KPIs · slide 4
**Role:** market scene sitting **behind big KPI numbers/chips** (pax/day, route count, TAM headline).
**Composition / safe zone:** vessel + market in the **right third**; **left ~60%** is open, **darker**
low-detail water/sky so white KPI numerals stay legible.

> Using the attached white hydrofoil vessel as the exact form/colour reference, produce a single
> photorealistic 16:9 photograph. The vessel sits on calm water in the **right third** of the frame with
> **{MARKET_SCENE}** behind it. The **left ~60% of the frame is open, calm, low-detail water and sky with a
> soft dark gradient**, so white text overlaid there stays fully legible. Foils down, clean reflection,
> exactly one vessel, hull/cabin/V-mark exactly as the reference, in-water with no seam. Muted, slightly
> desaturated premium grade. Single integrated photograph, not a collage. No people, no logos, no text.

**Eval:** left-60% region has **low mean luminance + low variance** (auto: histogram) → text-legible;
single vessel; market lock; no seam; grade matches deck family.

## D. Unit-economics slides · econ keys (e.g. 7–9, 19–23)
**Role:** **full-bleed market-specific landmark skyline** behind unit-economics charts. Charts and OPEX
text overlay on the slide template — the image itself is a rich, recognizable local scene, not a muted
gradient or split composition.
**Composition:** edge-to-edge panoramic skyline/coastline/harbour; vessel **small in the lower-center**,
actively foiling.

> Using the attached white hydrofoil vessel as the exact form/colour reference, produce a single
> photorealistic 16:9 photograph: a **full-width panoramic view** of **{MARKET_LANDMARK}** filling the
> frame from left to right — unmistakable local skyline, coastline, and harbour detail at golden hour.
> A single white hydrofoil, small in the **lower-center** on open water, **foils deployed, hull elevated**
> above the waterline. Exactly one vessel, hull/cabin/V-mark exactly as the reference, in-water no seam.
> Cinematic, aspirational, premium. No people, no logos, no text, no artificial gradient panels.

**Eval:** **full-frame landmark detail** (auto variance check); single vessel; market lock; foiling not
displacement; deck-coherent grade.

## E. TAM / market-size · slide 11
**Role:** the **aspirational scale** plate behind the TAM ladder. Convey a *network of destinations* —
**without** a fleet (still one vessel). Scale comes from an expansive seascape + multiple distant
island/town silhouettes + optimistic light.
**Composition / safe zone:** panoramic horizon; vessel **lower-center, small**, heading toward a coastline
dotted with destinations; **upper two-thirds open sky** for the TAM-ladder rungs/numbers.

> Using the attached white hydrofoil vessel as the exact form/colour reference, produce a single
> photorealistic 16:9 photograph: a **wide, aspirational seascape at golden hour**. A **single** white
> hydrofoil, small in the **lower-center**, heads toward a coastline with **several distant island and town
> silhouettes** suggesting a network of destinations. **Expansive open sky fills the upper two-thirds** for a
> data overlay. Cinematic, optimistic, premium grade. Foils down, clean wake, hull/cabin/V-mark exactly as
> the reference, in-water no seam. **Exactly one vessel.** No map graphics, no people, no logos, no text.

**Eval:** **single vessel** (the easy place to violate); upper-two-thirds open (auto luminance check); a
**generic-premium or market-correct** coastline (no leak / no specific banned landmark); **no Atlas/map**
imagery; reads as scale/ambition.

## F. Partner-roles · slide 12
**Role:** the **partnership** — Navier vessel + the partner's network — **without cheesy handshakes**.
Vessel at a berth (optionally the booking-moment human), framed to leave a **clean lockup band** where the
renderer places the **partner logo + role columns** (Navier = vessels/charging; Partner = demand/app).
**Composition / safe zone:** vessel + berth on one side; **right third (or lower band) clean** sky/water for
the **logo + text lockup** — never bake the logo.

> Using the attached white hydrofoil vessel as the exact form/colour reference, produce a single
> photorealistic 16:9 photograph at a tidy modern berth in **{MARKET_SCENE}**: the white hydrofoil moored
> alongside, foils down, clean reflection. Frame so the **right third is clean, calm sky and water** for a
> logo-and-text lockup. Optional: a single traveler on the berth glancing at a phone, candid, not facing
> camera. Warm, premium daylight. Exactly one vessel, hull/cabin/V-mark exactly as the reference, in-water no
> seam. Single integrated photograph, not a collage. **No logos, no text, no brand signage.**

**Eval:** **clean lockup zone** present (auto luminance/variance in the right third); single vessel; **no
baked logos/text**; market lock; no seam.

## G. (Optional) Section dividers / closing CTA
Reuse the **cover grade + seed family**; vessel heading toward open water; **center kept clean** for a short
CTA line. Eval: deck-coherent grade, single vessel, clean center band, no leak.

---

## Eval matrix — what's automatable vs human
| Check | How | Auto? |
|---|---|---|
| 16:9 + ≥2560×1440 | dimensions | ✅ auto |
| Opacity 100% / no see-through hull | alpha + hull-region variance vs scene | ✅ auto |
| Single vessel | object detection count == 1 | ✅ auto (vision) |
| Safe-zone legibility | luminance + variance in the named region | ✅ auto |
| In-water / no seam | edge/gradient check at hull waterline | ⚠️ vision-assisted |
| Hull fidelity vs neutral ref | embedding/feature similarity to `n30-reference-neutral.png` | ⚠️ vision-assisted |
| Market lock + landmark denylist | vision classifier vs allowed scene + banned-landmark list | ⚠️ vision-assisted |
| Booking-moment present (slide 3) | person + phone in left third | ⚠️ vision-assisted |
| No baked logos/text | OCR == empty in image | ✅ auto (OCR) |
| Deck coherence (grade family) | grade/seed match the locked cover | ⚠️ human + metadata |
| **Final partner-quality** | **Grab-gold exemplar compare** | 👁️ **human spot-check (hard gate)** |

`qa_image_gate()` should **block `replaceImage`** until auto+vision checks pass, then write a machine-readable
**QA receipt** (per-check pass/fail) into `ASSET-REGISTRY.json`; the human thumbnail spot-check is the final
gate before the live deck is touched.
