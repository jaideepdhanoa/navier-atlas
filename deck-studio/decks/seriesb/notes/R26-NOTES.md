# R26 — 2026-08-06 (Jaideep live review, round 3)

## Trigger
Jaideep on slide 20: why 11× (N30 vs Targa 32) but only 8× (N45 vs Princess 55) when the Princess is the bigger diesel? Root cause: panel A was bottom-up (battery spec × tariff), panel B was top-down (Princess burn ÷ 4 hydrofoil ÷ 2 hybrid) — and hybrid never got the cheap-electron multiplier. Jaideep decision: make the N45 electric and bottom-up for consistency.

## Change 1 — Slide 20 panel B: N45 hybrid → N45 ELECTRIC, bottom-up
- Basis: 285 kWh battery / 70 nm = 4.07 kWh/nm (same intensity method as N30's 114/70 = 1.6), × 16 nm leg × $0.20/kWh × 2,400 legs/yr = **$31.3K/yr**.
- Ratio vs Princess 55 measured $630.0K = **20×** (630/31.3). Saved = **$599K/yr** (598.7 rounded).
- All-three-lines total: $31.3K + $50.0K + $120.0K = **$201.3K** (was $248.7K). All-in vs Princess $697.1K → 3.46×.
- Header "N45 — HYBRID" → "N45 — ELECTRIC".
- Explainer band: "Where the multiples come from — foiling cuts drag ~6×, cheap electricity does the rest — and the thirstier the diesel it replaces, the bigger the multiple. Physics, not pricing."
- Footnote extended: "N30 at 1.6 kWh/nm (114 kWh / 70 nm); N45 modelled at 4.1 kWh/nm — the same energy intensity scaled to the 20-seat hull."

## Change 2 — Master stat 8–11× → 11–20×
- Tech pillars slide (PDF p7): "11–20× less energy per mile vs diesel".
- Moat slide (PDF p15): same string, same fix (one replaceAllText pass, 2 occurrences).

## Change 3 — Memo (edit-in-place, doc 10ba33SA…) + local mirror
- §3: "…11× less energy per mile — and 20× on the N45, whose diesel counterpart is thirstier still. Run hybrid, the same foil efficiency still cuts fuel burn deeply on routes where charging does not yet exist." (8× hybrid figure removed — it was the ÷4÷2 construction, no longer cited anywhere.)
- Unit-econ ¶: "the electric N45 20× less than the Princess 55 it replaces… roughly 2–3.5× cheaper to run" (was hybrid/8×/2–2.8×).
- One-pager checked: no 8×/11× strings — clean.

## Change 4 — Cargo hierarchy residuals (Jaideep: slide 5 step 4 "Fill the night shift" not core strategy)
- Slide 5 card 4: headline → **"Move the freight"**; body → "Dedicated cargo vessels loading at any ramp — seeded by night freight on the passenger fleet." Chip NEXT — 2027 unchanged.
- Slide 22 (cargo chapter lede) still led with "Cargo is the night shift" → "Dedicated foiling freighters are the play; night freight on the passenger network is how it starts."
- Left untouched (poetic network lines, not strategy claims): slide 2 "moving people by day and cargo by night"; "People by day. Cargo by night." rhythm band (~p33). Flagged to Jaideep as optional.

## Q&A bank
- Q24 added (local + Drive doc): why the bigger boat shows the bigger multiple.

## Divergence flag
- JIH sheet (1cRueboa…) still models the N40/N45 as hybrid (÷4 ÷2 editable calls). Series B deck/memo now use electric bottom-up. JIH deck is a different commercial context (hybrid offer stands there) — do NOT auto-cascade without Jaideep's word.

## Verification
- All replaceAllText occurrence counts exact (7×1 + 1×2; then 1,1,1).
- PDF exported via browser (API export >10MB limit): `Navier-Series-B-R26-42slides.pdf`, 42 pages. Visual check pages 5, 7, 15, 20, 22 — all clean, no overflow.

## Scripts
`/tasklet/agent/home/scripts/seriesb-rebuild/r26/r26-build.ts`, `r26b-cargo-card.ts`.

## R26c addendum (Jaideep round 4, 2026-08-06)
**Ask:** (1) efficiency row above the energy line so the derivation is visible; (2) reprice electricity at STELCO mid-band $0.30/kWh (was floor $0.20 — "too aggressively optimistic").

**Slide 20 (sb_unitecon40) — new state:**
- New first row in all four columns: "Energy use per mile" — N30 1.6 kWh/nm · Targa 32 2.4 L/nm · N45 4.1 kWh/nm · Princess 55 10.9 L/nm.
- Repriced at $0.30/kWh: N30 energy $18.8K/yr (was $12.3K) · N45 $46.9K/yr (was $31.3K).
- Totals: N30 $103.8K vs Targa $183.5K · N45 $216.9K vs Princess $697.1K.
- Delta strips: "7× less energy — $80K/yr saved" · "13× less energy — $480K/yr saved".
  Consistency fix: "saved" now = all-three-lines delta on BOTH panels (R26 had panel B as energy-only $599K while panel A was total $86K).
- Footnote: mid-band tariff language + both diesel burn bases (Targa dealer sea trial · Princess measured burn).
- Multiples: 140.5/18.8 = 7.5 → 7× (floor) · 630.0/46.9 = 13.4 → 13×.

**Master stat (S7 pillars + S15 moat):** "11–20× less energy per mile" → "7–13× lower energy cost per mile vs diesel" (×2 via scoped replaceAllText). Wording also corrected: it is a cost multiple, not a physical-energy multiple (physical ratio is 14–26× at 9.7 kWh/L diesel — larger; cost framing is the conservative one).

**Memo (live doc + local MD, 4 subs):** $5 → $8 electricity leg · 7×/13× lower energy cost · "roughly 2–3× cheaper to run" (was 2–3.5×; new ratios 1.8×/3.2×).

**Q&A bank:** Q24 rewritten at $0.30 with net-of-three-lines savings ($480K / $80K).

**Left alone (flagged):** S34 premium payback P&L footnote cites "energy from the live Maldives operating model" — locked R21/R24 cascade ($752K owner profit); repricing there not authorized. JIH sheet/deck still hybrid ÷4÷2 at $0.20 — separate commercial context, awaiting Jaideep's word.

**Script:** r26c-efficiency-row.ts (48 requests, verified render pages 7/15/20).
**PDF:** /tasklet/agent/home/seriesb-rebuild/r26/Navier-Series-B-R26c-42slides.pdf

## R26d addendum (Jaideep round 5, 2026-08-06)
**Ask:** (1) rebase S34 premium payback P&L to $0.30/kWh; (2) refresh memo + one-pager to new deck story; (3) recommend teaser selection.

### S34 reprice (deck slide 34, `sb_premium`)
- Energy $15K → **$23K** (index-based edit — column has two "$15K": energy line 3, marina line 7)
- Owner-operator profit $752K → **$744K** (sum-checked) · payback still **~16 months**
- 10-yr cumulative ≈$7.5M → **≈$7.4M** · leased operator $502K → **$494K** · running costs $220K → $228K
- Footnote: "$0.30/kWh mid-band tariff" noted; stale battery-reserve line fixed ($810–830K → $694–714K — was still on pre-R24 basis)
- Q&A bank: R26d supersede note appended.

### Memo (live doc + local MD, 7 edits each, all verified 1-occurrence)
- $70M+ → **$100–150M** (§1, §12×2 — third instance reworded to "full Series B program")
- §1 "roughly 10×" → **7–13× per mile vs diesel** (matches deck master stat)
- §8 cargo inverted to deck hierarchy: dedicated freighters = play (two modes + any-shore ramp), night freight = the way in; SIDS 2× import-cost line added (UNCTAD); sequencing line matched.

### One-pager (docx edited in place, Drive fileIdToReplace @ v111)
- "roughly 10×" → 7–13× per mile vs diesel
- $1.1T+ → **$600B+ waterborne economy** (R20b sourced sizing)
- $70M+ → $100–150M
- Cargo sentence added to Business Model (dedicated freighters + night-freight seed)
- Live version downloaded first (v111 = local was in sync); backup at `onepager/live-download-2026-08-06.docx`

### Flagged, not touched
- Memo §11 "Gulf 180-ft program kickoff, on contract" — possible LC-180 firewall breach (spec + region + contract status). Awaiting Jaideep ruling.
- JIH sheet still hybrid @ $0.20 — separate commercial context, awaiting call.

## Teaser rebuild (Jaideep round 6, 2026-08-06)
**Ask:** Rebuild teaser from current R26d master content. Include Gulf + Quanta slides; no round slide.
**Method:** Drive-duplicated master (perfect fidelity incl. R26d figures) → pruned 46→18 slides → cover retag "Investor Deck"→"Investor Teaser" → closer chapter tag 05·FINANCIALS→04·GTM (both element-scoped, API-verified).
**New teaser:** `1JJ-QWO5-W1K_GQaUu7NCARrY7_C3COAl0s-4HnUz8GY` — "Navier — Series B Teaser" (18 slides).
**Old teaser:** `1wyc6ereNDU3VZc8aTXw0Wy6oJJ6tzuHmXA3CuwMtM0M` renamed "[SUPERSEDED 2026-08-06 — do not share]". Jaideep browser-delete when ready.
**Order (master idx):** 1,2,4,6,7,8,9,10,11,13,14,16,17,18,19,21,25,33.
**Note:** master has 46 slides (42 export-visible + 4 skipped appendix: sb_prod_cost, g3f556ac5e67_1_714, g3f556ac5e67_1_798, g3f6623c186e_4_145) — none selected.
**Browser session:** Google re-auth wall hit (password challenge) — PDF export blocked until Jaideep logs back in. Structural + text verification done via API.

## R27 addendum (Jaideep round 7, 2026-08-06) — Sampriti's new slides rebuilt natively
**Ask:** Sampriti pasted two mockup screenshots into slides 4 & 5 (from an external 23-slide draft) and reinserted slide 7 (native, with Why-now box — no work needed). Rebuild 4 & 5 natively + transcript-driven enhancements (Joe Batcha / GKB call) + Q&A update.
**Slide 4 — THE NETWORK SHIFT (native):** "From a few giant ships to thousands of fast ones." Two panels: SHIPPING TODAY (sparse gray 5-node mega-port diagram, "20 knots · infrequent departures · fixed terminals") vs THE NAVIER NETWORK (dense 16-node gold mesh, "30 knots · departures all day · direct routes"). Kept protocol line (marinas=nodes…NavierOS=protocol) bottom-left; "The internet did this to information. We are doing it to payloads." bottom-right gold.
**Slide 5 — THE MASTER PLAN (native):** "Prove the system. Then compound the network." 6-phase timeline: 01 Prove flight/PIONEER (gold=done) → 02 Prove endurance/QUANTA (done) → 03 Prove network/MALDIVES (white+NOW) → 04 Add throughput/REGIONAL → 05 Scale corridors/GLOBAL → 06 Own the nodes/NETWORK. Bottom bar: "The vessel creates the route. The route creates the node."
**⚠️ Firewall decision:** Sampriti's mock said "80–180 ft" on phase 05 → rendered as **"80–220 ft"** (public N80/N120/N220 ladder) to keep LC-180 firewall. Flag to Jaideep.
**Slide 23 enhancement:** "We live this gap." strip — own Türkiye→U.S. shipments ~$40K/~40 days sea vs ~$400K/2–3 days air (Sampriti firsthand, call 2026-08-06).
**Q&A bank:** Q25–Q33 added (recurring rev per vessel, production ramp 20→40/yr, fabless/NVIDIA model, payload/foil-assist, how-big-can-foils-get + Plainview, exit paths, offshore energy crew transfer, defense commercial-first, hardware margins 20%→40–45%). Appended to live doc + local MD. Production-ramp answer partially closes the open production Q&A item.
**Transcript discrepancies flagged (deck unchanged):** (1) Sampriti quoted Quanta 2,400 NMi unmanned / 800 NMi manned vs deck canon ~2,000 NMi — needs Jaideep reconciliation; (2) she sized Series B "70–100M" on call vs locked $100–150M ask slide; (3) Saronic $3-per-$1 comparison spoken — stays off-deck (no primary source); (4) Maldives payback "5–6 months" spoken vs modeled figures.
**QA scratch decks created (Jaideep browser-delete):** `1f4fo-wup0Zs9ZlOYxwLDSy-XXkSnQUxiVEFVO5_qPf8`, `1zq1NJiRoVE40-GZzkLjSKe-WOHPtRP1Zim9BB_zCYaw` (both "[QA SCRATCH — safe to delete]").
**Render-verified:** via Drive PDF export of pruned scratch (browser auth-walled; Google session needs Jaideep re-login). Slides 4/5/23 verified clean after r27b fixes + source-append revert.
**Scripts:** /tasklet/agent/home/scripts/seriesb-rebuild/r27/{r27-build.ts,r27b-fixes.ts}

## R28 addendum (Jaideep round 8, 2026-08-06) — N180 ladder + Sampriti memo revision
**Ladder rule change (permanent):** N220 retired → top rung is now **N180** (unnamed). Public ladder: N30 Quanta · N45 Explorer · N80 Valkyrie · N120 Morpheus · N180. This makes "180 ft" a public Navier class, resolving the memo §11 firewall flag.
**Deck edits (all render-verified):**
- s5 phase 05: "80–220 ft" → **"80–180 ft"** (Sampriti's original restored)
- s13 GMVP ladder (+ teaser s10): "N120 —" → "N120 · N180 — ocean ferry and cargo / contested logistics"
- s23 cargo lede: "…night freight on the passenger network is how it starts." → "…night freight on the passenger fleet is the pilot-phase test." (Sampriti: night cargo = pilot trial, cost-gated — not the starting model)
- s31 H1-2027 milestone: "N120 Morpheus program — kickoff on contract" → **"N180 program — kickoff on contract"** (now matches memo §11; the on-contract Gulf program is the 180-ft one — deck previously mislabeled it N120)
**Memo edits (live doc + local MD, 5 edits):**
- §1 opens with Sampriti's "future we see" arc (ships got bigger not faster → others tried, hull-first control-last → disciplined sequence), definition sentence kept verbatim
- §3: "Four larger platforms (45/80/120/180 ft)"
- §8: night freight → pilot-phase trial, corridor-by-corridor, cost-gated; "(N80, N120)" → "(N80–N180)"
- §11: "Gulf 180-ft program kickoff, on contract" → "N180 program kickoff (Gulf) — on contract"
**Q&A:** Q34 (cargo pricing — 10× ocean ≈ $2.50–3/kg lands at/below air band floor; anchored framing) + Q35 (FY2028 revenue — 🔴 needs representative model; no improvised numbers) appended to live doc + local.
**Standing design preference (Sampriti 2026-08-06):** more white space, cleaner, not text-heavy; text on clean fields not busy graphics. Apply to all future Series B slide work.
**Valuation/round-terms from her debrief:** verbal-only per standing rule — nothing written.
**Left unchanged + flagged:** s31 2028 column "N120 Morpheus — drawing board → first hull" and s44 N120 TRL slide (N120 remains a real rung; only N220 was renamed). Teaser still carries old "Navier Network" slide as its #3 (Sampriti's new S4/S5 postdate teaser build).
**QA scratch:** `134wiE-a8kpfCwMRku4wT44PBr3P-PdLKI2jHkgqECiU` (browser-delete).
**Script:** /tasklet/agent/home/scripts/seriesb-rebuild/r28/r28-n180-memo.ts

## R28b addendum (Jaideep, 2026-08-06) — Q34 cargo-pricing correction
**Jaideep rejected the R28 Q34 framing** ("~10× sea freight, at or below air"). Authoritative pricing = deck slide 39 `sb_cargo_econ` ("Night Cargo — Example Economics", ILLUSTRATIVE), which was **never changed and needed no restore**: **$0.75–1.50/kg** (LOW $0.75 · MID $1.00 · HIGH $1.50), midway between sourced bands (ocean $0.03–0.50/kg, air $2.50–4.50/kg). "10× ocean" ≈ $2.50–3.00/kg prices ABOVE the deck's own band — retired everywhere.
**Edits:** memo §8 cargo paragraph (live + local MD) now carries "$0.75–1.50 per kilogram, a fraction of air rates and a healthy multiple of ocean"; Q34 rewritten (live + local) to anchor on the deck band and explicitly warn off "10×". Sampriti's Claude-derived "10× of $0.30/kg" figure is what Q34 now corrects.
**QA scratch copies created this round (browser-delete):** 2× "[QA SCRATCH — safe to delete] r28 cargo check" (one orphaned by a failed script run, one used: `16IxvvZJ7F5F6DnlwCovtZt7lu3nOkEdFpZw10tvJabo`). Plus the r28 verify scratch from earlier.
