# /invest — Design Audit v8 (binding) — 2026-08-17, round 4 (post-Grok rebuild)

Evidence: full live-site scan (40,836px page, section-by-section screenshots + DOM/CSS inspection) + Jaideep's 24 annotated screenshots (uploads image 451–474) + deck reference slides transcribed. Scan detail: `work/v8/V8-SCAN-FINDINGS.md` (thread a_q1ppv3ypwhe56ve51bpk).

## A. Verdict on the build

Real progress worth keeping: Thesis/Traction renames live · 4-tab ladder working well (honest RENDER chips) · Atlas camera correctly FIXED (no pan/zoom on row interaction — compliant with the disclosure rule) · TAM section now matches the deck reference row-for-row, value-for-value · annual "Delivered in year" series present · competitor table and Maldives unit-econ table strong.

Still broken: 11 of Jaideep's 15 round-4 items confirmed on the live build, plus systemic bugs below.

## B. Jaideep round-4 directives (all v1-blocking; contracts updated this commit)

| # | Directive | Contract |
|---|---|---|
| 1 | NOW pill pinned ON phase-3 node, never floating in the 3–4 gap | claim.json arc |
| 2 | Three-costs→levers REBUILD: 1:1 in-place card morph (01→01, 02→02, 03→03), no whole-stage crossfade, no ghosting; Navier vessel triptych removed from the PAST stage (may live on levers stage); both ~250–270px dead gaps closed | claim.json costs-levers |
| 3 | Stability-contrast context line renders ABOVE the video as a lede, not caption below | proof.json demo-grid |
| 4 | Control: schematic + CTO video SIDE BY SIDE; repeated 7-fact text list DELETED; image never mirrored (bow faces LEFT per deck); anchors re-authored to deck geometry; every leader line terminates on its part | product.json control-tech |
| 5 | GMVP layers render as a connected 3-layer diagram tied to the wireframe (MISSION/SOFTWARE/HARDWARE with connectors), not three disconnected boxes | product.json gmvp |
| 6 | Hangar/Foundry hero REMOVED from GMVP (Traction only — standing rule); "Single Platform. Multiple Use Cases." becomes the ladder's lead-in line | product.json gmvp + vessel-ladder |
| 7 | Quanta: ONE title moment; headline in standard Title Case serif (no all-caps); founder video FIRST at ≥70% width with caption unclipped; camo photo moves down to pair with "Introducing the N30 Quanta" + stat chips | product.json quanta-* |
| 8 | Maldives matches Gulf structure: hero → kicker → title → subtitle → chips; italic caption retired; aerial photo full-exposure with press cards or dropped | gtm.json maldives |
| 9 | Cargo: one shared `04 · GTM — CARGO` kicker; ISLANDS/PLAY/SHIP SCALE/WEDGE demoted to sub-labels; each image composed WITH its own heading/body/cards — no image blocks divorced from copy | gtm.json cargo-* |
| 10 | Unified GTM kicker taxonomy `04 · GTM — {SEGMENT}` authored for all 13 GTM sections; Offshore and Defense get kickers (currently none) | gtm.json all |
| 11 | Defense: camo Quanta + Navy X-99 images side by side 50/50, not stacked full-width | gtm.json dual-use |
| 12 | TAM: values already match deck — ADD explicit column labels (DEMAND POOL · FLEET TODAY · VESSELS · 10-YR FLOOR · HULL $ · 10-YR FLOOR) so no figure's meaning is inferred | gtm.json market-floor |
| 13 | Money: KPI strip FIRST, charts below (sections reordered in contract); single OPERATING PLAN sub-kicker; per-year labels on Delivered-in-year | money.json |
| 14 | "The next 12–18 months" → "THE NEXT 24 MONTHS" (applied in contract; deliberate departure from deck slide per Jaideep) | money.json roadmap |
| 15 | Five-markets rows: hover/focus = row expands + thumbnail scales (~94×60→~180×115) + gold border, 200ms; touch renders expanded | money.json five-markets |

## C. Additional findings this round (also blocking unless marked)

C1 **[HIGH] Systemic left-edge clipping bug** — control callout labels AND Quanta founder caption ("…ampriti Bhattacharyya / …EO NAVIER") clip mid-word. Component-level fix + scripted horizontal-clip scan added to gate (site.json render_rules.clipping).
C2 **[HIGH] Duplicate kickers** — "03 · THE PRODUCT" prints twice back-to-back; "OPERATING PLAN — CONSERVATIVE CASE" twice in chapter 05. One kicker per section (site.json render_rules.kickers).
C3 **[MED] Kicker-less sections** — GMVP intro, ladder, Business Model, cargo body blocks, Offshore, Defense, closing. Resolved by authored kickers in gtm.json/product.json; renderer must render the authored kicker field everywhere.
C4 **[MED] RENDER — IN DEVELOPMENT chip** must appear on every render-image tab (N45, N180 too), not only N80.
C5 **[LOW] Competitor table**: give the row-label column a proper header cell.
C6 **[LOW] Nav Title Case vs in-page caps** — intentional, keep (confirmed).
C7 **[verified OK]** "9% recurring by FY30E" is consistent with authored data (45.5/512.1 ≈ 8.9%) — scan flag dismissed; chart and KPI agree.

## D. Verification gate before review request
1. v7 §D protocol (scans: no-ellipsis, banned terms, clip scan) + NEW horizontal-clip scan at 1280/1440/2560 — paste outputs in PR.
2. Screenshots: arc with NOW on node 3 · costs→levers mid-morph (no ghosting) · control side-by-side with all 7 callouts terminating on parts · GMVP layer diagram · Quanta restructured · Maldives header vs Gulf header · one cargo stage (image+copy composed) · defense side-by-side · TAM with column labels · money KPIs-above-charts · five-markets row hovered · full-page kicker inventory (every section, one taxonomy).

---
Round-4 source observations: `work/v8/jaideep-observations.md`. Deck reference transcriptions (TAM slide, control schematic orientation/callout map): `work/v8/V8-SCAN-FINDINGS.md` §4–5.
