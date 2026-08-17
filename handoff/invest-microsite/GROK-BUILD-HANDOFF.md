# Grok Build Handoff — Series B Investor Microsite (`/invest`)

**Date:** 2026-08-16 · **Route:** `/invest` on navier-atlas (Vercel demo: `navier-atlas.vercel.app/invest`)
**Authority docs:** `CONTENT-MAP-AND-SPEC.md` (architecture §2–§5, locked decisions §10) · `contracts/` (10 JSON files — ALL renderable content)

## The one rule

**Render authored data only.** Every string, number, name, and quote on the page comes from `contracts/*.json` renderable fields (non-underscore). Do not write, paraphrase, or "improve" any copy. Underscore-prefixed fields (`_internal`, `_qa-contracts.ts`) are never rendered. If a component needs a string that doesn't exist in a contract, leave it out and flag it in the PR — never invent.

## Page structure

Single scrollytelling route, six chapters + footer, sticky chapter nav with progress indicator (labels in `site.json.nav`). Contract → chapter mapping: `hero.json` → Hero · `claim.json` → 01 The Claim · `proof.json` → 02 The Proof · `product.json` → 03 The Product · `gtm.json` → 04 Go-to-Market · `money.json` → 05 The Money + finale + footer. Interactive data: `ladder.json` (Vessel Ladder Explorer, ch. 03) · `pipeline-map.json` (Pipeline Map, ch. 04) · `unitecon.json` (Unit-Econ Toggle, ch. 04).

## Design system

- Dark field, generous white space, gold accents per existing Navier microsite brand system (Playfair Display headlines / Exo 2 / Poppins body as used in employer microsites). Benchmark: SpaceX-IPO restraint + `/employers/boston` quality bar.
- **Text never sits on photo or video.** Media in dedicated plates or full-bleed solo; copy on clean dark field.
- Motion: scroll-triggered reveals, stat counters, the six-pill arc lighting sequentially (claim.json), the cargo-gap chart drawing itself (gtm.json), day/night flip (gtm.json). No parallax excess, no cursor effects, no autoplaying audio ever.
- Interactivity is capped at the three components above. Everything else is presentation motion.

## Video handling (v1 = YouTube)

- All embeds via `embed_url` (youtube-nocookie) with `poster` frame, click-to-play, lightbox or inline per each video object's `play_mode`. No YouTube branding surfaces before click beyond the poster.
- `proof.json` demo grid: v1 renders poster cards that open lightboxes — EXCEPT the self-hosted clip `assets/stabilization-juxtaposition.mp4` which renders as a native muted autoplay loop (`play_mode: "loop"`, `muted`, `playsinline`, lazy-loaded).
- Architecture must allow later swap of any YouTube grid card to a native mp4 loop without layout change (source files coming later).

## Pipeline map geometry

`pipeline-map.json` carries stats/tiers only. Bind map geometry from the repo's **existing Atlas global registry** — real corridors/cities only, subdued world-map treatment, no invented dots, no labels that resolve anonymized parties to countries or entities. If clean binding is not achievable in v1, ship the section with stats + tier table and a static world-map plate; do not fake geometry.

## Access & meta

- `noindex,nofollow` meta + exclusion from any sitemap. No gate, no analytics in v1.
- OG card: dark plate, "Navier — Series B" wordmark only. **No numbers in OG image or meta description.**
- Page title per `site.json`. Confidentiality line renders in the footer.

## QA gates (all mandatory before Jaideep review)

1. Side-by-side vs the Cut deck (`CUT-SLIDE-INVENTORY.md` in the same folder is the text reference) — every number identical.
2. Rendered-HTML scan: no banned terms (valuations, lead identity, LC-180, AD Ports, royal-office identity, Sergey Brin, N120, "2,400 NMi", "$600B", "not yet public"), no internal vocabulary, no `_internal` content leaked.
3. Legibility: no text over media, WCAG AA contrast, clean at 375 px mobile.
4. Performance: lazy-load all media below the fold; Lighthouse mobile ≥ 85; self-hosted loop ≤ 6 MB.
5. Screenshots of all six chapters (desktop + mobile) posted to the PR.

## Out of scope (do not build)

Email gate · analytics · custom domain · appendix content (Cut slides 37–53) · any native mp4 loops beyond the one shipped asset · Prarit CGI finale slot (reserved; ship finale with `money.json` finale plate as-is).
