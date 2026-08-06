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
