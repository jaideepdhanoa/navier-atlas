# GROK SPEC — /story · The One-Link Outreach Proof Reel

**Date:** 2026-08-25 · **Owner:** Tasklet (content) / Grok (build) · **Approver:** Jaideep
**Contracts:** `handoff/story-microsite/contracts/{site.json, story.json, assets.json}`

## 1 · What this is

A third microsite tier below /teaser and /invest: the single link that replaces the
16-link list in investor outreach emails. **No password. Forwardable by design.**

**Disclosure rule (governs every string):** public record only. If a journalist or the
company has not already published it, it is not on this page. The defense boundary is
the company LinkedIn post of 2026-08-25 (linked in story.json) — nothing beyond it.

**Design center:** a proof reel, not an editorial scroll. Every section = one claim +
the footage that proves it. Text is captions, not paragraphs. An investor who watches
two loops and reads two press cards has seen the differentiation in under 60 seconds.

## 2 · Build rules

1. **Reuse the /invest template system** (section renderer, typography, dark plate).
   New section kinds: `hero-loop`, `claim-proof`, `vessel-row`, `film-shelf`, `cta`.
2. **Two video classes, strict:**
   - `ambient` — autoplay, muted, loop, no controls, ≤15s, play only in viewport
     (IntersectionObserver), pause off-screen. Poster-first on mobile / save-data.
   - `film` — click-to-play with poster (YouTube: `maxresdefault` thumb; self-hosted:
     extracted frame). Sound allowed. Never autoplay.
3. **Captions in clear bands — never text over footage.**
4. **FILMED / RENDER badge** on every visual, small corner chip, verbatim from
   assets.json. This is a feature, not a disclaimer.
5. **Page-weight budget:** lazy-load everything below the fold; hero loop ≤4 MB;
   total initial payload ≤8 MB. A proof reel that stutters proves the opposite.
6. **TE 26-3 montage:** native 826×720, dark letterbox, never upscale, never crop.
7. **No text under 24px at 1280/1440/2560. No ellipsis/truncation.**
8. **Renderer renders authored strings only** — no generated copy, no summaries.
9. `noindex,nofollow`, unlisted, no nav links from other sites to /story.
10. **Analytics:** Vercel + custom events (`section_view`, `video_play`,
    `video_complete`, `outbound_click`, `cta_click`), UTM passthrough. Per-section
    play data is the pre-call interest profile — it must actually fire.

## 3 · Leak scan (fail the build)

Scan the built HTML for every term in `story.json._leak_scan.terms` (31 terms:
energy/grid/node/data-center vocabulary, round terms, Gulf, program names, 2,400,
N30D, etc.). Any hit anywhere in rendered output = build fails.
Also: zero dollar figures other than $10M revenue and $100M Maldives.

## 4 · QA gate (before hand-back)

- Screenshots ≥10: every section at 1280/1440/2560 + mobile hero + mobile film shelf.
- Verify `loop_takeoff` actually shows displacement→foilborne takeoff (flagged
  `_verify` in assets.json); fallback is `hero-loop.mp4`.
- Interior plates depend on PR #400 (`employer-hub/assets/vessels/`); if unmerged,
  pull from branch `feat/employer-interiors`.
- All six press-wall links resolve; LinkedIn post link opens in new tab.
- Badges render on every visual; footnote `fn_directional` renders once.
- Video events visible in analytics debug.

## 5 · Explicit exclusions (decided, do not add)

- Energy / sea-grid / floating power / data centers — held even from /teaser.
- Quanta range figure — the superlative line (CEO-approved, verbatim) carries it.
- /defense link, defense program names, pipeline entities, round terms, valuations.
- Per-recipient codes — campaign UTMs only.
