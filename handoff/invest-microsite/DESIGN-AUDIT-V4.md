# /invest — Design Audit v4 (binding) — 2026-08-17

Full pass over the live build (35,703 px, all 25 section blocks) at 1280 px + Jaideep's wide-screen capture.
Verdict: the plates that landed (Maldives hero, cargo lander, X-99 defense, fleet trio, Foundry B/W, pipeline map) prove the format. What remains is **(A) three systemic layout bugs, (B) a dead Network Shift interactive, (C) vessel-image canon violations, (D) per-section polish**. Every item below is a defect or a required improvement — nothing optional unless marked.

---

## A. Systemic defects (fix once, apply everywhere)

**S1 — Container is broken in both directions.**
- At ≤1280 px: section text sits at `x=0` — literally flush against the viewport edge, and in several places **clipped** (first glyph cut off).
- At wide screens (Jaideep capture): content column locks left, black void right.
- Fix: one shared section container — `max-width: 1200px (prose) / 1440px (media)`, `margin-inline: auto`, `padding-inline: clamp(24px, 5vw, 64px)`. Full-bleed plates (`100vw`) are the only exception. **No text element may ever render at x < 24px.**

**S2 — Clipped text (confirmed instances, all must be re-verified after S1):**
- Maldives plate caption renders "*1aldives — $100M signed…*" (first chars off-screen).
- Quanta stat band "~2,000 NMi" — first glyph clipped.
- EBITDA chart: "-112%" label clipped at plot top-left → add y-axis headroom / clip:false.
- Ask headline "$10M Series B-1 First Close of $100–150M+" — the `$` glyphs render with broken/overlapping vertical strokes (looks like a double-painted decorative dollar). Use the plain serif `$` from the same font, no ornament layer.

**S3 — Two-up media rows overflow.** Quanta section: Sampriti film card (left, flush at x=0) + camo Quanta render (right, clipped by viewport, vertically misaligned). Fix: proper 2-col grid inside the media container, equal heights (`object-fit: cover`), gap 24–32 px, stacks at <1024 px.

---

## B. Vessel-image canon (root of "wrong vessel" defects)

Hard rule: **the deck contains no photoreal N45, N80 or N180 render.** Never substitute another hull or a generic boat. The only canon multi-class artwork is the Cut s13 wireframe fleet. New assets now in repo (`assets/deck/`):

| File | Content | Use |
|---|---|---|
| `fleet-wireframe.png` (2048×1143) | All four hulls N30→N180, ascending | GMVP "one core, every vessel" hero (already live ✓) + ladder base |
| `fleet-wireframe-n30/-n45/-n80/-n180.png` | Per-class crops (receding sibling reads as depth) | Vessel-ladder explorer tabs |

- **Ladder explorer:** N80 tab currently shows a small cargo foiler — wrong hull, remove. Preferred spec: keep ONE full `fleet-wireframe.png` canvas and spotlight the active class (dim siblings to ~30%, hairline gold outline + spec card on the active hull). Fallback: the four crops above. Photography only on the N30 tab (it exists and flies); every other class labeled `RENDER — IN DEVELOPMENT` in small caps.
- **Photoreal N30 assets** (X-99, GMVP camo, Maldives livery, Pioneer) may only ever appear as N30/Quanta. The camo hull in the Quanta section is correct.
- N80 as *cargo freighter* render (lander plate) is canon for the cargo chapter only — never for the passenger ladder.

## C. Network Shift — full respec (current build is rejected)

As built: one flat dashed line, 2 gold dots, 3 grey rectangles on a near-black empty canvas. It reads as an unfinished chart, not a network. Rebuild to this spec:

1. **Canvas:** full-bleed (100vw × ~85vh), stylized dark coastline arc (two landmasses / an island group — simple bezier silhouettes, not a real map).
2. **State A — "SHIPPING TODAY":** 2 mega-port glyphs, 3–4 huge slow ship silhouettes crawling on a single thick trunk line. Everything grey, sparse, slow (8–10 s traversal).
3. **State B — "THE NAVIER NETWORK":** same geography; 25–35 small harbor nodes light up gold along both coastlines; 40–60 fast vessel dots animate on **many point-to-point great-arc routes** (thin gold polylines, 1.5–2 s traversals, staggered). Density and speed ARE the message.
4. **Transition:** scroll-scrubbed or toggle — trunk line dissolves, mesh blooms outward from harbors (stagger 30 ms/node). Respect `prefers-reduced-motion` (crossfade only).
5. Stat chips under each state: `2 ports · 20 kn · weekly` → `30+ harbors · 25–35 kn · continuous`. Kicker line stays: *"The internet did this to information. We are doing it to payloads."*
6. Implementation: inline SVG + requestAnimationFrame (or CSS motion-path). No canvas blur, no washed grey — palette = #0a0a0a field, #b99a5f gold, #6b7280 grey for State A only.

Acceptance: a cold viewer must describe State B as "a network lighting up." If it can be described as "a line with dots," it fails.

## D. Section-by-section (scroll order, offsets at 1280 px)

| # | Section | State | Required fixes / improvements |
|---|---|---|---|
| 1 | Hero (0) | Good — full-bleed SF plate, OWN THE EDGE, Watch-the-film | Verify lightbox plays `aavaIZPkDyk`; headline could go one step larger (clamp 56→88px); keep sub-line width ≤ 60ch |
| 2 | Network Shift (~1.2k) | **Rejected** | Rebuild per §C |
| 3 | Slide-5 arc (~1.9k) | Structurally right (6 steps, NOW badge), visually flat | Scroll-lit progression (past=dim, active=gold ring + lit text, future=faint); slim outlined market pills per phase (dark fill, hairline gold border, small white caps — never chunky arrows); step 03 "Sell vessels" must visibly carry the defense emphasis (`GMVP · DUAL-USE, DEFENSE LEADS`) |
| 4 | About / fleet trio (~2.8k) | Plate good | Caption "One platform. Every mission." is 9px flush at edge → move into container, 12–13px, grey; **verify "5× less energy" against Cut s3 wording — if the deck says a different multiple, the deck wins** |
| 5 | Team (~3.4k) | Present, names/photos correctly mapped ✓ | Second row ragged (2 cards + void): use Sampriti feature-left + tidy 2×3 grid right, equal card heights; **investor/pedigree logo strip is illegible grey smudge** → replace with either re-fetched hi-res wordmarks (min 120px wide, white/mono versions) or drop the image strip entirely and keep the clean "Backed by" text block (which already reads well) |
| 6 | Foundry B/W plate (~4.6k) | Good | Keep caption "Fifty years, fundamentally unchanged." inside container |
| 7 | Three Costs (~5k) | Cards fine | Headline flush-left (S1); card kickers currently near-clipped at card top — add padding-top |
| 8 | N30 Pioneer proof (~6.5k) | Good | — |
| 9 | Demo grid + stabilization (~7.5k) | Good — anchor clip + 2×2 captioned grid | Grid can widen to the 1440 media container; keep captions |
| 10 | Quanta (~14k) | Content right, layout broken | S3 two-up fix (film + camo render); stat band into container; **verify "35 kts dash" against Cut s10 — canon range line is ~2,000 NMi at 20 kts ✓ (already correct)**; four-pillar frame (stable · quiet · defense · long-range commercial) should read in the lede |
| 11 | Control stack / Mission Layer (~12.8k) | Typing card OK | Ensure the three-layer stack (Mission/Autonomy/Flight control) all render; verify no text on photo |
| 12 | GMVP (~11.8k) | **Fixed** — wireframe fleet live ✓ | Let the plate breathe: full-bleed or 1440 container (currently inset in a card with dead margins); headline "(GMVP)" keep within container |
| 13 | Vessel ladder explorer | **N80 tab wrong image** | Rebuild per §B (spotlight spec) |
| 14 | Maldives (~17.5k) | Hero plate excellent | Caption clip (S2); "The Maldives" heading into container |
| 15 | Revenue lines (~19.8k) | Numbered cards + math-bridge callout good | Headline into container. Note: "Three Revenue Lines" matches deck s21 — leave until the open three-vs-four-lines decision is made (do not silently change) |
| 16 | Maldives unit econ (~20.4k) | Class toggle present | Verify both panels render the deviations-only table (N30 vs Targa 32 · N45 vs Princess 55), software row lists Navier modules; energy at $0.30/kWh, 7×/13× multiples |
| 17 | Coastal-Network Model / $100M (~22k) | Heading flush at x=0 | S1; keep signed-roles table inside container |
| 18 | Cargo (~23.1k) | Lander plate excellent; Wedge cards good | Landing-craft stat band (180 FT · 25–30+ KN · 250–1,000 T) flush-left → container; serif pull-quotes into container; firewall check clean ✓ (no LC-180 name, no counterparty, no timeline) |
| 19 | Defense (~26.5k) | X-99 plate + USMI quote — best section on the page | Caption/quote block is fine on-photo *as a full-bleed plate lower-third* — keep scrim ≥ 60% for legibility |
| 20 | TAM ladder (~28.2k) | Coded bars, right-aligned values — good bones | Rows into container; add ~8px label→bar gap; **verify per-row vessel counts against Cut s24 (three rows all read "1,500–3,000 vessels" — suspicious copy-fill)** |
| 21 | Pipeline map + tables (~29.9k) | Strong — real Atlas-style map, clustered counts, two tables, $3:$1 line | Confirm the four gold stat-band numbers from deck s30 appear ($100M signed/100 boats · 250–300 Gulf named · $300M+ US defense expansion · ~$3:$1); Gulf rows stay anonymized ✓ |
| 22 | Money stats + charts (~30.8k) | Native coded charts ✓ (no more PNG upscales) | "-112%" clip (S2); widen both chart cards to the 1440 media container; legend inside plot corner; stat band into container |
| 23 | Milestones 12–18 mo (~31.6k) | Four-card timeline good | "Every milestone is funded by this round." — keep as gold kicker |
| 24 | The Round (~33.3k) | Two-panel use-of-funds good | `$` glyph artifact (S2); headline + serif kickers into container |
| 25 | Close (~34.4k) | Thesis line + Go-deeper video + Contact | Rebuild as symmetric close: full-bleed `assets/closing-loop.mp4` under "Every coastline a network — OWN THE EDGE"; then Go-deeper (Ashlee Vance `ZNgh39DM_Jg`) + Contact + data-room CTA; footer confidential line stays |

## E. QA gate for the next build

1. Zero text at x < 24px anywhere on the page (scripted DOM scan, all breakpoints: 1280 / 1440 / 2560).
2. Zero clipped glyphs (visual pass on every headline, caption, chart label).
3. Every image slot matches `contracts/assets.json` v4 `used_in` — one asset, one home.
4. Vessel identity check: no hull ever labeled as a class it isn't; no generic boats.
5. Network Shift passes the cold-viewer test (§C acceptance).
6. Chapter screenshots at 1440 AND 2560 posted to the PR before review is requested.
7. Kill-scan: no internal vocabulary, no LC-180/counterparty/valuation/round-terms beyond deck canon.
