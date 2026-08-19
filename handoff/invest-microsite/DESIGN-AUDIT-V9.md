# /invest — Design Audit v9 (binding) — 2026-08-17, round 5
Supersedes v8 where in conflict. Sources: Jaideep round-5 directives #1–#14 (two messages, 2026-08-17 18:31 + 19:02 PT), live-build scan (work/v9/V9-SCAN-FINDINGS.md), master deck S17, measured schematic anchors.

## A. v8 close-out (verified on live build)
10 FIXED · 5 PARTIAL · 0 NOT FIXED. Partials are closed by items below: reflow flicker (→ #2), schematic stubs (→ #6), GMVP connectors (→ #7 note b), TAM FLEET TODAY column (→ B-12'), chart series labels (→ #13). C1 label clip → global clip-scan rule; C3 GMVP kicker → gmvp contract.

## B. Round-5 directives — all contract-bound
1. **Arc phases drop in sequentially** — reveal choreographed to the gold rail draw, ~150ms stagger (claim.json).
2. **Costs→levers rebuilt for coherence** — (a) NO-REFLOW: flip may not change document height (the +49px reflow IS the flicker); (b) each lever card carries an authored causal `bridge` line answering its cost; (c) Why-Now and the closing trade-off line hidden until AFTER the levers land, then float in (claim.json).
3. **Pioneer hero = video** — `assets/pioneer-hero-loop.mp4`, autoplay muted loop, poster fallback = prior static image. File is inbound (Drive 503s all evening — follow-up commit); bind now with poster fallback (proof.json + assets.json `pending-upload`).
4. **"flies stabilized"** caption applied; stabilization clip demoted into the equal-weight clip grid with honest Quanta subcaption ("same NavierOS control stack that flies the Pioneer fleet"). Recommendation adopted: click-to-play posters, NO parallel autoplay (heavy/busy); section lead media = the new Pioneer hero video (proof.json).
5. **Traction kicker** → "One platform — mobility, logistics, defense." (proof.json).
6. **Control schematic — authored anchor map.** Bow faces RIGHT natively (never mirror). Seven callouts with normalized coordinates measured on the exact asset (2048×983), label sides assigned, interactive spec: dots ON parts, hairline gold leaders, hover focus dims others. HARD FAIL: leader into empty space, any clipped label, any mirroring (product.json `schematic`).
7. **N45 mockup swapped** — `n45-mockup-v2.png` (golden-hour NYC, 2752×1536, Jaideep-supplied) binds to the ladder N45 tab + any GMVP N45 mockup; registered approved in assets.json. GMVP layer boxes get visible connectors + kicker.
8. **Quanta intro reordered** — adopts the "What the Quanta Unlocks" pattern: image ≥60% width, chips ≥260px each, dead space closed (product.json).
9. **Benchmark restored from master S17 verbatim** — 10 spec rows + vessel-type band, Quanta vs Saronic Corsair / Saildrone Voyager / BlackSea GARC, takeaway "Speed, range, efficiency — pick two, until now.", optics/slamming explainer, "Public sources, August 2026." (product.json `competitive`).
10. **Maldives** — redundant lagoon image removed, press cards rebalanced; player-logo strip (Navier·JIH·HARIM·Visit Maldives) MOVES into Maldives under the tracker; removed from Coastal-Network Model (gtm.json).
11. **Ship-scale balanced** — top hero width == four-image row width; variants grid gets a 1408×768-aspect container (kills the 367px letterbox); metrics full-width band ≥260px/stat (gtm.json).
12. **Pipeline fully visible** — nested scroll region banned; all rows visible at all widths (gtm.json + global rule).
13. **Money** — "The Ramp, Year by Year" is the section heading at top (eyebrow → title → KPI band → charts); "Mobility sold direct (~$1M) · defense sold as platform to partner shipyards." DELETED; every chart series labeled (money.json).
14. **Five markets** — Title Case ("One Platform · Five Markets · All in Motion"); hover keeps enlarged image but text must reflow — zero overlap at any width (money.json).

## C. Fresh scan findings (P1–P8) — bound
P1 five-markets caps (→ #14) · P2 flip reflow (→ #2) · P3 ask-card headings → Title Case + eyebrow ("NOW" / "18–24 MONTHS") · P4 pipeline nested scroll (→ #12) · P5 dead-air budget: no >200px empty band in any stage (Quanta ~500px, ship-scale ~370px, Islands ~300px all closed by items above + rule) · P6 teal series label (→ #13) · P7 network-pin canvas recomposed to fill · P8 chip no-wrap rule.

## D. New global render rules (site.json)
No-reflow · no nested scroll · all-caps only for kickers/eyebrows/stat labels · dead-air budget 200px · chip no-wrap · clip scan at 1280/1440/2560 includes schematic labels.

## E. Grok review-request gate (paste in PR)
Screenshots: (1) costs state + (2) levers state with Why-Now visible + proof no doc-height delta; (3) annotated schematic at 1440 with all 7 leaders landing on parts; (4) benchmark table full; (5) Quanta intro new layout; (6) Maldives with logos strip, no lagoon image; (7) ship-scale balanced; (8) pipeline all rows, no inner scrollbar; (9) money top-of-section heading + labeled series; (10) five-markets hover with no text overlap; (11) N45 ladder tab with new mockup; (12) Pioneer hero video (or poster fallback if mp4 not yet landed). Plus: clip scan, ellipsis scan, all-caps scan, banned-term scan outputs.

## F. Open items
- `pioneer-hero-loop.mp4` upload pending (Drive 503s) — agent follow-up commit.
- Jaideep's original message cut off at item 12 in the first send; items 12–14 arrived in the second message — treated as complete. No item beyond 14 expected.
