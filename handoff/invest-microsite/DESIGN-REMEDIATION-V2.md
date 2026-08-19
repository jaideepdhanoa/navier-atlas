# /invest — Design Remediation v2 (binding)

**Status:** The v1 build fails the quality bar. It renders the contracts as a wall of thin gray text cards with almost no imagery. This document is a **binding defect list** — v2 is done when every item below passes. `contracts/assets.json` is now part of the contract set and every slot in it must render.

**Benchmark unchanged:** SpaceX-IPO restraint + `/employers/boston` polish. The deck this site replaces is visually rich — the site must **at minimum match the deck plate-for-plate**, then exceed it with motion and video.

---

## Defects and required fixes

### D1 — Hero (worst defect)
**Now:** a collage of two stills with press-headline text colliding through the "OWN THE EDGE" headline. Violates the text-never-on-photo rule and looks broken.
**Fix:** Single full-bleed background video `assets/hero-loop.mp4` (the deck's own animated cover — N30 foiling past the SF skyline), autoplay muted loop, poster `assets/hero-poster.jpg`. Dark scrim from bottom. Headline + one sub-line + one CTA, bottom-left, on the scrim only. Nothing else in the viewport. Delete the collage entirely.

### D2 — No imagery
**Now:** zero deck plates on the page.
**Fix:** Render every slot in `assets.json`. Each chapter opens with its full-bleed divider plate. Long text runs are broken by plates — never more than two consecutive text sections without a visual.

### D3 — Ladder explorer repeats one wireframe
**Now:** the same blueprint graphic for all five hulls.
**Fix:** Per-hull imagery per `assets.json` (`product.ladder.*`). The wireframe appears once, in the GMVP architecture section only.

### D4 — Demo videos are postage stamps
**Now:** ~240px thumbnails in a cramped grid.
**Fix:** Large 16:9 cards — 2-up on desktop, 1-up mobile, ≥480px height desktop. Official YouTube posters per `assets.json`. The stabilization clip is a **native `<video>` muted loop** (`assets/stabilization-juxtaposition.mp4`), not a YouTube card. Hover = subtle scale + play affordance. Captions below the card, never on it.

### D5 — Dead-space layout
**Now:** all content locked to a narrow left column; right half of every section is empty.
**Fix:** Centered content column, `max-width ~1160px`. Stat bands and tables use the full column. Media plates go full-bleed (100vw). Asymmetry only as a deliberate two-column pattern (text left / plate right and alternating), never text + void.

### D6 — Stat chips are gray boxes
**Now:** identical thin-border boxes; numbers don't land.
**Fix:** Match the deck's stat band: large gold serif numerals (Playfair), small white caps label below, hairline gold rule above the group, **no boxes**. 4-up desktop, 2-up mobile.

### D7 — Money chapter has no charts
**Fix:** Render `chart-revenue-by-segment.png` + `chart-ebitda-margin.png` as clean plates on the dark field (conservative case, from the deck). Native rebuild with identical data permitted later; raster ships in v2.

### D8 — Foundry/Product texture
**Fix:** Foundry section renders factory interior + b/w shipyard heritage pair per `assets.json`. Quanta section renders the defense camo plate + Atlantic-run map. Dark seascape plate opens the Product chapter.

### D9 — Chapter rhythm
**Fix:** Repeating visual grammar per chapter: full-bleed divider plate → headline → stat band → content blocks interleaved with plates → transition. Scroll-triggered reveals (fade/rise, 300–500 ms, once) on headlines and stat bands. No parallax gimmicks.

### D10 — Close
**Fix:** Full-bleed `closing-loop.mp4`, same scrim treatment as hero, closing line: "Every coastline a network — OWN THE EDGE." + data-room CTA. Current text-only footer close is flat.

---

## Unchanged rules
- Render authored data only — all copy stays exactly as in contracts; this pass is visual only.
- Text never sits on a photo (scrim-band hero/close are the only exceptions, text on scrim not image detail).
- No generated imagery, no stock, no upscaling past container width.
- QA gates from GROK-BUILD-HANDOFF.md §QA all still apply; add: **every `assets.json` slot verified rendered** + updated chapter screenshots on the PR.
