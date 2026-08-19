# /invest — Design Audit v5 (binding) — 2026-08-17

Third full review pass: Jaideep's wide capture (3) tile-by-tile + live walk + DOM scans
+ ladder tab probe + clipping scan. Build under review: page height 33,710–34,343 px
(redeployed mid-review; findings verified against the latest state).

## Verdict

Real progress — hero is full-bleed video, team section exists with correct name↔photo
mapping, GMVP hero is the canon fleet wireframe, the vessel ladder is canon-correct
(photos only where photos exist: N30 `n30-pioneer-at-sea`, Quanta `quanta-lr-render`;
wireframes for N45/N80/N180), stabilization clip is wide, cargo and defense plates land.

Two things still sink the site: **the container/clipping defect was never fixed**, and
**the Network Shift is rejected for the third time**. This audit ships a working
reference implementation for the latter — drop it in, do not reinterpret it.

---

## P0-1 · Container / text clipping — STILL OPEN (third audit in a row)

Scripted scan at 1280 px: **~25 text elements at x=0 or x=−7**, including chapter
kickers, section headlines, and stat numerals. Every one of these renders flush against
or beyond the left viewport edge:

`One platform. Every mission.` (x=−7) · `THE NETWORK SHIFT` (0) · `Prove the system…` (0)
· `The Team` (0) · `Fifty years, fundamentally unchanged.` (−7) · `N30 Pioneer —
delivered…` (−7) · `10,000+` (0) · `Traction: Speed & Capital Efficiency` (0) ·
`GMVP: One core, every vessel.` (0) · `Built in America — the Foundry.` (−7) … and more.

**Fix (one shared primitive, applied to every section):**
```css
.section-inner { max-width: 1200px; margin-inline: auto;
                 padding-inline: clamp(24px, 5vw, 64px); }
.media-inner   { max-width: 1440px; margin-inline: auto;
                 padding-inline: clamp(24px, 4vw, 48px); }
```
Full-bleed (100vw) is reserved for hero, Network Shift, chapter plates, closing loop.
**Acceptance: scripted scan returns ZERO text elements with left < 24 px at 1280 / 1440
/ 2560.** Run the scan; paste its output in the PR. Do not eyeball this.

## P0-2 · Network Shift — REJECTED ×3 → reference implementation provided

As-built state A is a grey horizontal line with two dots and four lozenges; state B is
random gold dust with dashed horizontal streaks. Neither reads as anything.

**`docs/invest/reference-impl/network-shift.html` is now the binding artifact.**
Self-contained (zero dependencies, canvas 2D, deterministic seeded layout, DPR-aware).
Built and visually verified in a real browser this session. What it renders:

- A **coastline** (irregular bays/headlands, land mass distinctly lighter than sea,
  shore glow) + **5 islands** — the world is instantly readable as a map.
- **State A — Shipping today:** 2 ringed mega-ports on the coast, one grey trunk lane,
  3 giant slow container-ship silhouettes with long wakes. Empty, sparse, grey.
- **State B — The Navier network:** ~30 gold harbors bloom progressively along coast
  and islands (staggered thresholds — the network *lights up*, it doesn't pop),
  thin gold sea arcs (never crossing land, never plunging), **58 fast vessel dots with
  fading trails** running harbor-to-harbor, hub nodes larger with pulse.
- Smooth blend between states; caption chips + pill toggles included and styled.

**Integration contract:**
- Bind scroll progress of the section to `window.setNetworkMix(m)`, m∈[0,1]
  (0 → state A at section entry, 1 → state B by ~70 % through; pin section 150–200 vh).
- Keep the toggle pills as a manual override; keep both caption chips.
- Headline stays: *From a few giant slow ships to thousands of fast electric vessels* /
  kicker *The internet did this to information. We are doing it to payloads.*
- Port the file's canvas + logic verbatim into the site component. Restyle text to the
  site's tokens if needed; **do not redesign the drawing code**.

## P0-3 · "Backed by" logo row — now absent entirely

v4 flagged illegible grey smudges; the build's answer was to delete the strip. The
pedigree signal (deck s6) must return. Two acceptable forms:
1. Hi-res wordmarks ≥120 px wide each on the dark field (assets exist in
   `assets/deck/team-*` extraction set — re-request if needed), or
2. A clean typographic row: `BACKED BY — [investor names from Cut s6]`, small caps,
   gold separators. **Verify names against Cut s6; do not guess.**

## P1-4 · Money charts still PNG upscales

`chart-revenue-by-segment.png` / `chart-ebitda-margin.png` render at 587 px from 355 px
sources — soft and unreadable, in the money chapter of all places. v4 requirement
stands: rebuild as native coded charts from the contract JSON (bars: revenue by segment
FY26–FY30; line: EBITDA margin), site tokens, animate on scroll-enter, label the
Conservative basis. PNG charts are banned from this page.

## P1-5 · Remaining consistency items

- Plate widths: full-bleed plates alternate 1280 / 1137 / 1135 arbitrarily —
  pick the `media-inner` width for framed plates and 100vw for chapter plates; no
  in-between one-offs.
- Demo film grid thumbnails 556 px — acceptable floor, but at ≥1440 the grid should
  widen with `media-inner`, not stay locked.
- Duplicate `htUWE3AJUbc` (Four Seasons 18 s) appears in both Proof demo grid and
  Maldives section — keep Maldives, swap the Proof grid slot for `93MCRJYsD_8`
  (turning) if not already distinct, or drop to 3 films.
- Thesis-board thumbs at 94 px are fine; ensure hover states enlarge to ~240 px.

## Definition of done (gate to review request)

1. Clipping scan output pasted in PR (zero <24 px at 3 widths).
2. Network Shift = reference implementation, scroll-bound; screen-recording or two
   state screenshots posted.
3. Backed-by row restored (form 1 or 2), names verified against Cut s6.
4. Native charts in money chapter; PNGs deleted from the build.
5. Chapter-by-chapter screenshots at 1440 AND 2560 posted to the PR.
