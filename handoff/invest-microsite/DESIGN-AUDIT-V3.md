# /invest — Section-by-Section Audit & Upgrade Plan v3 (binding)

**Status:** BINDING — supersedes DESIGN-REMEDIATION-V2.md. Audited 2026-08-17 against the live build (browser pass, full 27,354 px page + DOM image-map extraction) and Jaideep's wide-screen capture.
**Definition of done:** every defect below fixed + fresh full-page screenshots (1440 px AND 2560 px viewports) posted on PR #387.

---

## 0 · Global defects (fix first — these change everything)

| ID | Defect (verified) | Fix |
|---|---|---|
| **G1** | **Page left-locks on wide screens.** Content shell is ~1265 px max-width but not centered — at 2000 px+ viewports the whole site sits left with a black void right (confirmed in Jaideep's capture). This alone causes most of the "squeezed" feeling. | Center the shell (`margin-inline:auto`). Full-bleed elements (hero, dividers, close, Network Shift band, pipeline map) must span **100vw at every viewport**, not cap at 1265 px. |
| **G2** | Media rendered at column width: demo videos 544 px, CTO/Quanta films 534 px, Atlantic map 534 px, Maldives plate 534 px, charts 544 px. Everything reads as thumbnails. | New layout grammar: prose column 720–840 px · media grid 1200–1360 px · plates/interactives full-bleed. No meaningful visual below ~620 px wide on desktop. |
| **G3** | **Renderer bug:** a raw JSON object (`{"label":"THE TEN-YEAR FLOOR…"}`) prints as literal text in the Opportunity/TAM section. | Render the object's fields (label + value + note) as the styled gold floor-band. Add a QA grep: no `{"` may appear in rendered HTML. |
| **G4** | Blurry upscales: money charts are 355×254 source PNGs stretched to 544 px+. | **Rebuild both charts natively in code** (data already in `contracts/money.json`, conservative case): revenue-by-segment stacked bars + EBITDA margin line, gold-on-dark, animate on scroll-enter. PNGs become fallback only. |
| **G5** | Asset duplication: `n30-pioneer-at-sea.png` renders in 3 places (Three-Costs plate, proof divider, ladder N30). | One asset = one home (see per-section map below). |
| **G6** | Type scale too small for the medium; sections feel dense despite a 27k px page. | Scale up: H1 `clamp(3.5rem,6vw,6rem)`, H2 `clamp(2.5rem,4vw,3.75rem)`, body 1.125rem/1.75. Section padding 140–180 px. Chapter dividers 70–80vh. |
| **G7** | Motion absent: page is static; counters, reveals, and scroll-lit sequences from the handoff not implemented. | Implement: fade/rise on section enter (12–16 px, 400 ms), stat counters count up once on first view, slide-5 arc phases light sequentially, chart draw-in. `prefers-reduced-motion` → static. |
| **G8** | Team pedigree exists in contracts but **zero team visuals render**. | Full team section build — §3 below. Assets now shipped. |

---

## 1 · Hero — "OWN THE EDGE"

**Now:** hero-loop.mp4 plays ✓, but the text block floats mid-left at modest size; scrim weak; boat can exit frame behind the text; "Watch the film" pill does nothing obvious.
**Fix:**
- Full-viewport (100vw × 100svh) video, headline **bottom-left** on a real scrim (bottom 45% gradient), headline at G6 H1 scale — "OWN THE EDGE" should span ~40% of viewport width.
- Sub-line + one CTA. **"Watch the film" opens a lightbox playing the narrator film (`aavaIZPkDyk`)** — this is the only place the hero film lives.
- Small "SCROLL" cue bottom-center. Nothing else composited.

## 2 · Claim opener — fleet lineup plate + "About Navier"

**Now:** fleet-family-lineup.png renders ✓ but capped at shell width; caption is tiny gray italic; "About Navier" is two short floating paragraphs.
**Fix:** plate full-bleed (100vw, ~75vh). Caption chip below-left. Merge the two paragraphs into one large-type manifesto block (max 720 px, 1.5–1.75rem serif), the "5× less energy, run by software" phrase in gold.

## 3 · The Team — **NEW BUILD** (currently text-missing entirely)

Assets shipped in this commit (`assets/deck/`): `team-sampriti-bhattacharyya.png` (960×1198) · `team-kenneth-jensen.png` · `team-dan-dorsch.png` · `team-dotan-feldman.png` · `team-jaideep-dhanoa.png` · `team-paul-bieker.png` + pedigree logos `team-logo-01..11.png` (NASA, GoogleX, MIT, Berkeley, Columbia, Bosch, Grab, McKinsey, et al. — all hi-res).
**Build (in chapter 01, after About Navier):**
- Lede: "30+ roboticists, aerospace & marine engineers · 40+ manufacturing specialists".
- Sampriti featured card (portrait, larger) + 5 cards: photo, name, role, credential line — **exact name↔photo mapping per filename; verified against slide geometry, do not swap**.
- Pedigree logo strip: uniform ~28 px height, white/grayscale treatment, subtle opacity.
- "BACKED BY" row from `claim.json` (text list, small caps).

## 4 · The Network Shift — **flagship interactive** (Jaideep priority)

**Now:** WRONG image — `world-pipeline-map.png` (the GTM pipeline map) at 534×292 beside two small cards. This is the core-thesis visual and it's the weakest section on the page.
**Build — full-bleed scroll-driven interactive (sticky container, ~200vh scroll length, canvas or SVG):**
- **State A — "SHIPPING TODAY":** dark sea field, 2 mega-port nodes, 3 large slow ship silhouettes crawling a single lane. Chip: *"A handful of mega-ports — 20 knots · infrequent departures · fixed terminals."*
- **Scroll scrub → State B — "THE NAVIER NETWORK":** 25–35 harbor nodes light up gold along the same coastline; dozens of small fast vessel dots run point-to-point routes. Chip: *"Every harbor and marina becomes a hub — 35 knots · departures all day · direct routes."*
- Kicker centered below, large serif: *"The internet did this to information. We are doing it to payloads."*
- `prefers-reduced-motion` / mobile fallback: the two states as static side-by-side frames.
- Copy verbatim from `claim.json` — no invented numbers, no invented city names on the field.

## 5 · Slide-5 arc — "Prove the system. Sell vessels, then platforms…"

**Fix:** six phases as a scroll-lit vertical progression — each phase row: slim gold-outlined pill + one line + small plate thumb (Pioneer → Quanta → GMVP wireframe crop → Maldives → globe → network). Phases illuminate sequentially as they enter viewport; previous dims to 60%.

## 6 · Three Costs (fifty years stuck)

**Now:** divider reuses `n30-pioneer-at-sea.png` (duplicate, thematically wrong — it's the proof image).
**Fix:** divider = **`shipyard-heritage-bw.png`** full-bleed (the b/w heritage plate is thematically exact: maritime frozen in time). Three cost cards get big gold numerals (01/02/03), title, one line — 3-up at grid width. "Why now — the window is open" as a distinct gold-ruled band, four window conditions as chips.

## 7 · Proof — "Don't take our word for it" (demo grid)

**Now:** five 544×305 cards, generic; stabilization mp4 present ✓ but same tiny size; no play affordance hierarchy.
**Fix:**
- 2-up grid at full grid width (~660 px/card): poster + duration chip + gold play ring; click → lightbox autoplay.
- **Stabilization juxtaposition mp4 = the anchor: one full-width row (~1360 px), native `autoplay muted loop`**, caption: side-by-side stabilization vs a conventional hull.
- One-line physics caption under each card (from `proof.json`).
- Chapter divider (proof) becomes `n30-pioneer-at-sea.png` full-bleed — its only home besides the ladder.

## 8 · Traction — Speed & Capital Efficiency

**Fix:** stat counters (vessels delivered, sea-trial hours, $ raised-to-date figures from `proof.json`) count up on enter, gold numerals at 3–4rem. `quanta-dark-seascape.png` stays as the section plate — full-bleed.

## 9 · Control / software-defined vessel (CTO film)

**Now:** S7WB91FvSFI card at 534 px beside text.
**Fix:** 2-col at grid width: film card ≥720 px (lightbox) + pull-quote column ("The hardest technology is control"). Keep Kenneth's film here only.

## 10 · GMVP + Foundry

**Now:** wireframe at 1110 ✓ good; foundry + heritage squeezed into 546 px side stack.
**Fix:** wireframe stays (its only home). **`foundry-interior-flag.png` becomes a full-bleed plate** closing the section ("Built in America — the Foundry"), heritage b/w moves to §6. Ashlee Vance film stays in Go-deeper (§17), not here.

## 11 · Vessel ladder explorer

**Now:** works; active image 651×406; inactive preloads (1×1) fine.
**Fix:** stage grows to ~1200×560 (16:9), hull tabs with silhouette + name + one-line mission; spec rows (length · pax/payload · speed · range · ASP band where public) animate per selection; Quanta tab carries "in sea trials" chip — **no "not yet public" language**. Assets per manifest (N30=pioneer photo, Quanta=LR render, N45=city skyline, N80=cargo-foiler-miami, N180=morpheus).

## 12 · Quanta unlocks (four pillars + Atlantic map)

**Now:** atlantic-run-map at 534 px; Sampriti's film currently sits in the GMVP section.
**Fix:** 2-col at grid width — Atlantic map ≥720 px with the ~2,000 NMi @ 20 kts route callout; four-pillar chips (range · stability · quiet · dual-use). **Move Sampriti's Quanta film (QhiaYVgXMf0) here** — it is the Quanta/resilience narrative. `quanta-defense-camo.png` stays as the section's second visual.

## 13 · Competitive — "The Field Trades Off. Quanta Doesn't."

**Now:** **WRONG plate — `maldives-overwater.png`** (a GTM image) opens a competitive-table section.
**Fix:** no photo plate here at all — this is a clean dark-field table section (SpaceX restraint). Table at grid width, gold checks, sourcing-date footnote. Maldives plate moves to §14.

## 14 · GTM — Maldives + Coastal-Network Model

**Now:** Maldives renders one 534 px lagoon image; Coastal-Network Model opens with **WRONG plate `air-vs-ocean-cargo.png`** (the cargo juxtaposition).
**Fix:** chapter opens **full-bleed `maldives-overwater.png`** with stat chips below: $100M · 100 vessels · 10-yr contract. `n45-lagoon-dusk.png` = inset beside the model explanation. Four Seasons 18-second film gets a compact card here (its second natural home; primary stays §7 grid). Coastal-Network Model = diagram-style band (hub → routes → app → recurring lines), no plate.

## 15 · GTM — Cargo, Service fleets, Defense

- **Cargo opener = `air-vs-ocean-cargo.png` full-bleed** (moved from §14) with the caption already in the manifest. `cargo-foiler-island-pier.png` stays ✓; night pair (`night-pier-containers` + `night-dock-ops`) as a 2-up "night freight is the wedge" row.
- **Service fleets:** `offshore-ctv-hero-v3.png` from 534 px → ≥720 px 2-col.
- **Defense:** `navy-foiler-night.png` full-bleed with the Leidos quote overlaid on the dark sky area (only permitted text-on-photo exception — dark field, high contrast); `quanta-defense-camo-2.png` inset. US Navy · Leidos · Gulf naval evaluation chips.

## 16 · Opportunity (TAM) + Pipeline + Money

- **TAM:** fix G3 JSON bug; ladder bars animate to width on enter; ten-year floor as the gold band.
- **Pipeline "Signed — and In Motion":** `world-pipeline-map.png` full-bleed (~85vh) — its ONLY home (removed from §4). Four gold stat-band numbers count up ($100M signed/100 boats · 250–300 Gulf named · $300M+ US defense potential · ~$3:$1).
- **Money:** native charts (G4). Five-market thesis board ("One platform · five markets"): each row gets a 96 px plate thumb (pioneer/maldives/quanta-lr/cargo-n80-profile/navy-foiler crop) + status chip — no longer text-only.
- **The Round:** two cards stay; add gold allocation bars inside B-1 card; "Request the data room" → mailto per contract.

## 17 · Close + Go deeper

**Now:** closing-loop.mp4 present; "Go deeper" = small left-aligned Vance card + sparse right column.
**Fix:** close = full-viewport video, "Every coastline a network — OWN THE EDGE" centered on scrim. Go deeper = centered band: Vance film card ~860 px + Contact button + confidential line, symmetric.

---

## Asset placement map v3 (one asset, one home)

| Asset | Home |
|---|---|
| hero-loop.mp4 | §1 hero |
| fleet-family-lineup | §2 claim opener |
| team-* (6+11) | §3 team |
| *(interactive, no image)* | §4 Network Shift |
| shipyard-heritage-bw | §6 divider |
| n30-pioneer-at-sea | §7 proof divider + §11 ladder N30 (permitted pair) |
| stabilization mp4 + 4 posters | §7 grid |
| quanta-dark-seascape | §8 plate |
| S7WB91FvSFI | §9 |
| gmvp-wireframe, foundry-interior-flag | §10 |
| ladder set (5) | §11 |
| atlantic-run-map, QhiaYVgXMf0, quanta-defense-camo | §12 |
| *(no plate)* | §13 competitive |
| maldives-overwater, n45-lagoon-dusk, htUWE3AJUbc | §14 |
| air-vs-ocean-cargo, cargo-foiler-island-pier, night pair | §15 cargo |
| offshore-ctv-hero-v3 | §15 service |
| navy-foiler-night, quanta-defense-camo-2 | §15 defense |
| world-pipeline-map | §16 pipeline (only home) |
| native charts (+PNG fallback) | §16 money |
| cargo-n80-profile (thumb) | §16 thesis board |
| closing-loop.mp4, ZNgh39DM_Jg | §17 |

## QA gates (all mandatory before review)
1. No `{"` in rendered HTML anywhere.
2. Every asset above renders in its home; no asset renders anywhere else (DOM img-map diff).
3. Page centered at 1440 and 2560 px; full-bleed elements span 100vw.
4. Banned-term scan on rendered HTML (unchanged list).
5. Screenshots per chapter at both viewports posted to PR #387.
