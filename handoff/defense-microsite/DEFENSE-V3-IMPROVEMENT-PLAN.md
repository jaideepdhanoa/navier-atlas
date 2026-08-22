# /defense v3 — Improvement Plan (founder review of live v2 build, 2026-08-22)

**Contract of record:** `contracts/defense.json` **v3** (this branch). Build from it verbatim.
**Prime directive: reuse /invest components.** Every fix below names the /invest component to port.
Rebuilding these from scratch is what produced the v2 defects — port, don't recreate.

---

## Fix 1 — Chapter 01 "An American Maritime Company." (CRITICAL)

**Defect:** The live build renders one bridge paragraph floating in dead space — no title, no thesis,
no film. And that paragraph claimed Navier "designs and builds … in the United States," which is not
approved language. Identity is **"an American maritime company"** — never a blanket US-manufacturing claim.

**Fix (contract `def-navier`):**
- **Port the /invest `01 · Thesis` full-viewport stage component** — identical type scale, spacing, kicker-above-title.
- Render `thesis_paragraphs` verbatim (they are locked to /invest's Core Thesis), para 1 at lead weight.
- The new one-line `body` ("One core — foils, powertrain, autonomy, fleet software — configured across
  commercial and defense missions from day one.") renders as a short bridge line under the thesis. The
  old US-build sentence is gone from the contract; it must be gone from the page.
- **Launch film is the chapter centerpiece:** `assets/navier-launch-film-1080p.mp4` (new 1080p asset on
  this branch — replaces the 540p file; the ≤960px cap is lifted, render up to 1280px). Click-to-play
  **with sound**, poster = opening frame, centered play affordance. The YouTube version stays banned on /defense.

## Fix 2 — Chapter 02 "The Mission Problem" — REMOVED

Founder verdict: the copy didn't land and the argument is made better by the dual-use industrial
chapter. The section is deleted from the contract. All chapters renumber (02 · WHY NOW … 12 · THE CLOSE);
nav labels must match the new numbering. Do not leave a stale "PROBLEM" nav item.

## Fix 3 — Proof in Flight: stray fourth video

**Defect:** an oversized fourth video floats left below the three-up grid.
**Fix:** the `videos` array is exhaustive — exactly three equal tiles in one centered row. Remove any
other media element in this chapter. (If that fourth video was the stabilization loop, it already has a
home in `03 · THE PLATFORM` per the contract.)

## Fix 4 — The Family: GMVP first, military N30, no trailing hero

- **Port the GMVP intro block from /invest `03 · PRODUCT`** — wireframe plate
  (`assets/deck/gmvp-wireframe-family.png`) + THREE LAYERS cards (Mission Layer / Software / Hardware),
  same component and styling. It opens the chapter (new `gmvp_intro` object), before the four-hull ladder.
- **N30 ladder thumbnail** = `assets/deck/defense-sofweek-armed.png` (military Quanta-D), replacing the
  commercial Pioneer/Golden Gate photo. Deliberate for this audience.
- **Remove the large trailing Quanta-D image** after the ladder (`media_extra` is deleted from the contract).

## Fix 5 — Team headshots broken (CRITICAL)

Live build shows alt text instead of photos for all nine tiles. The same headshots render fine on
/invest — **port the /invest team grid component and its exact asset resolution**. Nine tiles: 7 team +
2 advisors (LeClair, Cederholm) with linked names (new tab). **FAIL condition:** any tile rendering alt text.

## Fix 6 — New Chapter 12 · The Close

The current ending (bare email line + photo) is far below the /invest standard.
**Port the /invest close** (`OWN THE EDGE` full-viewport hero + GO DEEPER strip + confidential footer):
- Background: `assets/closing-loop.mp4`, dimmed, poster `assets/hero-poster.jpg`.
- Line: *"The commercial network builds the industrial base. The defense fleet rides on top."*
- Display title: **OWN THE LITTORAL** · gold CTA button **"Arrange a briefing"** → `mailto:sampriti@navierboat.com`.
- GO DEEPER strip: Ashlee Vance film tile (embed `ZNgh39DM_Jg`, lightbox, same tile as /invest) +
  `assets/deck/goldenhour-bow.jpg` photo with its caption.
- The old team-chapter CTA and golden-hour image are superseded by this chapter — team ends at the grid.

---

## Unchanged gates (all still fail-the-build)

Password `quanta` · noindex/unlisted both directions · **zero financial content** · 14-term leak scan ·
jargon kill-scan · US flag visible at 1280/1440/2560 · advisor bio links click through (navy.mil URL
untouched — it 403s bots, resolves in browsers) · every video has a poster frame (no dead black boxes) ·
no text on photos · no text under 24px · no clipping at 1280/1440/2560.

## QA deliverables on the PR

≥12 named screenshots at 1440 (plus 1280/2560 on: thesis stage, video wall, family ladder, close hero),
including: 01 thesis stage w/ film poster · film playing (audio badge) · 04 three-up grid ·
09 GMVP intro + ladder w/ military N30 · 11 team grid with all nine photos rendering · 12 close hero +
Go Deeper. Plus leak/jargon/clip scan outputs and gate/noindex confirmation.
