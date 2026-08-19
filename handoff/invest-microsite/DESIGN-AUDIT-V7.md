# /invest — Design Audit v7 (binding) — 2026-08-17 (post-update live scan)

Live scan of the deployed site, 42 screenshots at `v7-scan/shots/`, full section log at `v7-scan/FINDINGS.md`.
Scored against DESIGN-AUDIT-V6 §C (16 items): **14 FIXED · 2 PARTIAL**. The page has turned the corner — the Atlas pipeline embed is now the strongest moment on the page. What remains is two bugs, one copy revert to wire, and a polish tier to take it from "matches the deck" to "sings."

## A. Blocking bugs (fix before v1 review)

**A1 — N80 ladder tab shows the N30 photo.** Tab label and "RENDER — IN DEVELOPMENT" caption are correct, but the image bound to the N80 tab is N30's photo — not the approved `assets/deck/n80-render-v1.png` (manifest status: approved). Wrong-hull substitution is a canon violation, worse than the wireframe it replaced. Bind the approved render.

**A2 — Three-Costs stage 1 photo tiles are empty.** Right-column tiles render as dark placeholder boxes — reads as broken to a cold viewer. Bind the three cost-pillar images per the v6 §C-2 spec; stage-2 morph still to be evidenced (screenshots of both states required per the v1 gate).

**A3 — About stage: wire the prose revert (commit `87989f2`).** `claim.json` about is now `prose-stage`: kicker "An American maritime company" + four deck paragraphs VERBATIM. Current render is a narrow text block — must become a full-viewport stage per `render_notes` (para 1 lead weight, wide measure ~70–80ch, clean dark field, no cards).

## B. Confirmed fixed on live (no action)
Grand-plan rail (§C-1) · Traction/foundry (§C-3) · Control diagram (§C-4) · GMVP (§C-5) · Maldives dedupe (§C-7) · Gulf hero (§C-8) · Coastal-model player logos (§C-9) · Cargo hero (§C-10) · Islands formatting (§C-11) · Play/Ship-scale/Wedge image bindings (§C-12) · Dual-use (§C-13) · Nation bars (§C-14) · **Signed-and-In-Motion live Atlas with clickable pipeline rows (§C-15) — best moment on the page** · FY26–FY30 native ramp charts, chips secondary (§C-16). Investor logo strip present and crisp. No internal-jargon strings found. N30/N45/N180/Quanta ladder tabs correct.

## C. Make-it-sing plan (priority order)

The bar: an investor should feel the company's precision in the page itself. Tight, coherent, one visual system — and a handful of moments the deck physically cannot do.

**S1 — About Navier as a statement, not a block.** Full-viewport dark stage. Kicker small-caps gold → title → para 1 at lead size (~28–32px, wide measure) → paras 2–4 at body, generous leading. Paragraphs reveal on scroll (fail-visible). This is the company's thesis in prose; give it the gravity of a manifesto page.

**S2 — Finish Three-Costs morph (v1 gate).** With images bound, the problem→answer turn becomes the page's second signature interaction after the Atlas.

**S3 — Why Now: recompose.** Boxed card floating in dead space → full-width weighted stage; align to the same grid and chapter rhythm as adjacent sections.

**S4 — Network Shift: color + purpose.** Interactive works but reads monochrome. Gold trunk corridors vs subdued feeders, soft node glow on hubs, and a one-line state caption that changes with the mix (point-to-point → networked). The open-network line (already in contract) closes it.

**S5 — Chapter interstitials.** The deck's numbered section dividers (01 · The Claim … 05 · The Money) should exist as short full-viewport breathers — number, title, one line. Gives the scroll a narrative pulse and makes the five-act structure legible, mirroring the deck's spine.

**S6 — One stat-chip system.** Single chip component (size, gold rule, label case) reused everywhere chips appear — hero, traction, pipeline band, money. Consistency of small furniture is what reads as "this company is precise."

**S7 — Coastal-model logos: quiet hover.** Subtle lift/brighten per player logo; no motion otherwise.

**S8 — Proof chapter: let the vessels move.** The four proof videos are the page's unfair advantage over any deck. Autoplay muted on enter (motion-reduced: poster + play), full-bleed, one line of copy each. No layout change, just confidence.

**S9 — Pipeline rows ↔ Atlas polish.** Already good; add focused-row gold highlight and a calm default state. Verify anonymized Gulf labels exactly match the pipeline contract.

## D. Verification protocol for v1 review request
1. Screenshots: About stage, Three-Costs both states, N80 tab, at laptop and wide widths.
2. Scripted scans re-run (clip 0 / manifest strings 0) and pasted in PR.
3. Wide-width (≥2560) composition sample for hero, cargo hero, money charts — audit tooling maxes at 1280, so Grok must supply these.
