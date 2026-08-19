# /invest — Design Audit v6 (binding) — 2026-08-17

Fourth pass. Sources: Jaideep's 16 observations + his deck-slide references (uploads
435–445) + live DOM measurement + media-placement map. This audit changes the design
doctrine, drops 13 new canon assets into the repo, and prescribes per-section fixes.

---

## §A · Doctrine — how the site beats the deck while staying consistent

**Diagnosis.** The build treats /invest as a long-form article: a narrow text column
(headlines are hard-locked to **580 px at 51 px type** — measured live; that is why
every title wraps 3–5 lines and eats vertical space) with images dropped between
paragraphs. The deck, by contrast, composes every slide as a weighted 16:9 stage.
The article grammar is why the site reads worse than the deck.

**Doctrine: the slide-stage.** Every section becomes a full-viewport stage that uses
its deck slide's composition as the skeleton, then exceeds it with web-native depth:

1. `section = stage`: `min-height: 100vh`, full width, `padding: clamp(48px,6vw,96px)`,
   content laid out in a 12-col grid inside — **never a 580 px column**.
2. Headline rule: `font-size: clamp(36px, 3.6vw, 60px)`, width auto up to ~22ch,
   **maximum 2 lines at any viewport** — acceptance-tested.
3. Kicker top-left (`01 · THE CLAIM` style, mirroring the deck's corner tags), gold
   hairline under the title — the deck's grammar, kept everywhere.
4. Weighted grids copied from the referenced slide (see §C) — title zone, media zone,
   stat rail. Images live INSIDE their section's grid, never floated above it.
5. Web-native surplus: motion on scroll, video where the deck had stills, animated
   callouts where the deck had static labels, native charts, the Atlas embed.
6. **Scroll-reveal must default to visible** (JS adds `.reveal` enhancement; without it
   content shows). Full-page captures currently render black below the fold — that is
   how broken the current reveal is.

## §B · New canon assets (pushed this commit, `assets/deck/` + `assets/logos/`)

| File | Source | Target |
|---|---|---|
| `traction-foundry-floor.png` (2048px) | Cut s10 | Traction hero — replaces `quanta-dark-seascape` |
| `control-wireframe-clean.png` (2048px) | Cut s11 | Control section centerpiece (no baked text) |
| `gulf-hero.png` (1920px) | Cut s19 | Gulf full-bleed plate — currently NO gulf image exists |
| `cargo-play-skyline.png` (2048px) | Cut s25 | The Play stage image |
| `shipscale-hero.png` (1900px) | Cut s26 | Ship scale stage hero AND N180 ladder tab |
| `shipscale-variants-grid.png` | Cut s26 | Ship scale secondary (4 payload variants) |
| `wedge-day-night.png` (1920px) | Cut s27 | The Wedge stage image (day/night composite) |
| `n45-mobility-render.png` (1420px) | city-transport microsite render, neutral crop | N45 ladder tab |
| `n80-render-v1.png` (1920px) | **newly generated render** — wireframe-guided, family design language | N80 ladder tab — **PENDING JAIDEEP APPROVAL**; label "render — in development" |
| `logos/logo-navier.png` `logo-jih.png` `logo-harim.png` `logo-visit-maldives.png` | Cut s22 | Coastal-Network Model player logos |

## §C · Section-by-section prescription (deck slide = layout reference)

1. **Slide-5 arc ("Prove the system…")** — headline wraps 5 lines today and the six
   phases read as disconnected cards. Rebuild as ONE connected horizontal rail in a
   single stage: six slim pills joined by a continuous gold progress line that draws
   on scroll, active pill lit, market pill under each. The connecting line IS the
   grand plan; without it the plan disappears. Headline one line of the three verbs.
2. **Three costs (ref 435/436)** — rebuild as the deck pair: stage 1 = left rail cost
   list (EXPENSIVE TO BUILD/MOVE/OPERATE, weighted bold lead-ins) + right photo stack
   (three vessel photos, "Different missions. Same constraints."); scroll morphs to
   stage 2 = three lever columns (CHEAP TO BUILD/MOVE/OPERATE) each with its image and
   gold payoff stat. This is the visually-weighted comparison the deck already solved.
3. **Traction (ref 437)** — `traction-foundry-floor.png` as the stage hero (dim ≤20%
   only behind text zones), stat stack left (10,000+ hrs · 10 vessels · $10M rev on
   $33M · $100M Maldives), gold timeline 2022→2026 right with milestones at deck size,
   not microtext. The dark ocean image leaves the section.
4. **Control (ref 438)** — `control-wireframe-clean.png` centered large; recreate the
   deck's seven callouts as HTML/SVG hairline labels that draw in sequentially on
   scroll (NavierOS — the Brain · autonomy sensor stack · fully retractable foils ·
   ride height sensors · carbon fiber hull · computer-controlled active foil 60–70% ·
   electric/hybrid powertrain 20–30%). Exceeds the deck: the diagram assembles itself.
5. **GMVP (ref 439/440)** — two-beat stage: beat 1 = platform-tier table (Mission
   Layer / Software Tier 2 / Hardware Tier 1) beside the N30 render with "Single
   Platform. Multiple Use Cases." beat 2 = fleet wireframe full-bleed with the four
   class captions. **The hangar image moves out of GMVP entirely → Traction.**
6. **Vessel ladder** — N30 AND Quanta LR tabs both use `n30-pioneer-at-sea` (one
   photo; Quanta is the same hull — drop `quanta-lr-render`); N45 =
   `n45-mobility-render.png`; N80 = `n80-render-v1.png` (approval pending, labeled
   render); N180 = `shipscale-hero.png`. Wireframe crops retire from tabs.
7. **Maldives** — drop the Four Seasons video from this section (it stays in the Proof
   demo grid only); the overwater plate appears exactly once (hero). Keep press quote
   + signing chips.
8. **Gulf** — add `gulf-hero.png` as the stage plate (golden-hour skyline, matches the
   deck's Gulf slide). Anonymized copy unchanged.
9. **Coastal-Network Model** — replace text-only role cards with the four player
   logos (`logos/`) + role captions (Navier — platform & vessels · JIH — capital ·
   HARIM — hotels & resorts · Visit Maldives — demand). White logos on dark field.
10. **Cargo opener** — `air-vs-ocean-cargo.png` must never crop the plane/ship:
    `object-fit: contain` against the dark field (or max-height 80vh). **The caption
    "opener full-bleed with manifest caption" is my internal manifest note rendered
    verbatim — renderer must NEVER print manifest/usage/`_`/note metadata. Add a
    scripted scan for manifest strings to QA.**
11. **Islands pay the most** — same stage grammar as its neighbor (kicker + 2-line max
    headline + stat chips); today it renders as a bare 21px header, format break.
12. **Play / Ship scale / Wedge** — one stage each, image INSIDE its stage:
    Play = `cargo-play-skyline.png` + the deck's three chips (TWO MODES · ANY SHORE ·
    NETWORK-READY); Ship scale = `shipscale-hero.png` + 180FT / 25–30+KN / 250–1,000T
    gold stats + `shipscale-variants-grid.png` secondary; Wedge = `wedge-day-night.png`
    + SAME VESSEL · SAME NETWORK · NEW REVENUE chips. Firewall check: no LC-180 name,
    no counterparty, no program details — deck s26 copy only.
13. **Dual-use** — adopt the deck's split composition: defense column | commercial
    column over the X-99 plate, USMI quote as the bridge. (General rule §A.4 fixes
    "layout of elements not ideal" across remaining sections.)
14. **From One Nation bars** — native horizontal bar chart, ≥14px axis labels, gold
    bars on dark, values at bar ends. No PNG.
15. **Signed — and In Motion** — replace the static `world-pipeline-map.png` with the
    **live Atlas** (same repo: embed the Atlas map component/route with a pipeline
    overlay preset — signed/named nodes only, no internal partner data), and tie the
    pipeline cards to it: hover/tap a pipeline row highlights its node. Signed/named
    tiers separated by weight (T1 signed gold · named pipeline outlined). This is the
    money moment and the single strongest better-than-deck opportunity.
16. **Money** — restore the annual ramp: native line/area chart FY26→FY30
    (Conservative: revenue to $512M, EBITDA margin line to ~25%), FY30 chips as
    secondary, not the headline. Charts from contract JSON, site tokens, draw on
    scroll. PNG charts remain banned.

## §D · Acceptance (gate to review request)

1. Zero headlines >2 lines at 1280 / 1440 / 2560 (scripted, output pasted in PR).
2. Zero text at left <24 px at the same widths (carryover, still unmet).
3. Zero manifest/internal strings rendered (scripted scan for "manifest", "full-bleed
   with", "_internal", "note:").
4. Full-page screenshot with JS disabled shows every section visible (reveal fallback).
5. Per-section screenshot pairs (site vs deck slide 435/436/437/438/439/440/443/442/445)
   posted at 1440 and 2560.
6. N80 tab ships only after Jaideep approves `n80-render-v1.png`.


---
## Status addendum — 2026-08-17 10:52 PT (Jaideep)
- §C-2 three-costs two-stage morph: **v1-BLOCKING** (deferral reversed by Jaideep).
- §C-14 live Atlas pipeline embed: **v1-BLOCKING** (plate allowed only as motion-reduced/JS-off fallback).
- N80 render n80-render-v1: **APPROVED** — photoreal on ladder tab.
- Money contract v2 (`39a9400`): FY26–FY30 ramp series authored; native charts unblocked.
