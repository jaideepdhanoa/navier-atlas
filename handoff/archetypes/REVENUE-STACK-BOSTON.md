# Revenue-Stack Model — Fleet Investors Archetype (Boston pilot)

**Date:** 2026-08-15 · **Status:** APPROVED (Jaideep 2026-08-15) — D6′ locked: utilization stack replaces anchor-plus-fill; cargo added to upside alongside sponsorship; Boston seat price $950–1,200 adopted
**Companion files:** `REVENUE-LEVER-BENCHMARKS.md` (all sourced market prices), `FLEET-ECONOMICS-BOSTON.md` (v1 model, superseded on economics if this frame is adopted)
**Fleet Investors firewall applies:** vessel-fleet financing only; no Navier equity/round content.

---

## 1 · The problem with the v1 model (stated plainly)

The v1 model sells one product — flat monthly commuter seats — on ~2 round trips/day, 22 days/month. That monetizes roughly **15% of the asset's available hours**: ~14 idle hours on every weekday plus 8 fully idle weekend days. It then patches the resulting hole with an anchor tenant at $100–125K/month — which for a ~20-seat block is **~$5K/seat-month, a price no employer rationally pays**, and which investors will treat as a contingency, not a plan. Verdict (Jaideep, 2026-08-15): the anchor is a one-off wish, not a financeable base case. This document replaces it.

## 2 · The reframe: one asset, one day, four demand layers

A commuter-only vessel is a mispriced asset. The same N45 that runs AM/PM peaks can run midday and weekend **experiences**, evening **charters**, and (eventually) overnight **cargo** — all of which exist as priced, operating markets in Boston today (see benchmarks file). The commute network remains the strategic backbone (it's what authorities and employers care about, and it's the schedule spine); the other layers buy down the payback.

**Convergence check (why this is credible):** Navier's own approved partner-model corridor — Boston↔Hingham at $65/leg, 65–76% all-day occupancy — produces a **2.49-yr payback**. The fully-built utilization stack below independently lands at **~2.1 yr** in its upside case (incl. sponsorship + cargo upside lines). Same physics: a premium vessel utilized across the whole day pays back in ~2.5 years; a vessel used 4 legs/day cannot.

## 3 · Pricing methodology — from flat rate to yield architecture

Flat $/seat-month is replaced by a three-layer yield structure. Every layer is benchmark-anchored (sources in `REVENUE-LEVER-BENCHMARKS.md`):

| Layer | Product | Pricing logic | Benchmark anchors (sourced) |
|---|---|---|---|
| **L1 · Committed bundles** | Monthly commuter seat (AM+PM guaranteed) | Priced as a *discounted pass vs the premium spot fare* — the universal industry structure. Pass discounts run **26–51% off spot** across MBTA monthly (~26%), Seastreak 40-trip (~35%), NYC Ferry 10-trip (~36%), Blade passes (~44–51%). Position at **3–4× MBTA monthly** ($319) = **$950–1,275/mo** — the top of our program band, justified by door-to-door substitutes (Uber Salem→Boston ~$56/trip ≈ $2,460/mo equivalent). | MBTA $9.75/$319; Seastreak $30 flex / $782 40-trip; Blade $95 pass-seat vs $195+ retail; Uber route averages $55–56 |
| **L2 · Spot seats** | Per-leg, dynamic, on residual commute capacity + shoulder sailings | Benchmarked between premium ferry ($30 Seastreak) and door-to-door car ($55 Uber): **$40–65/leg**, yield-managed. Matches canon corridor fares (Boston↔Hingham $65 approved). | Seastreak $30; Uber $55–56; canon $65 |
| **L3 · Block products** | Experiences (per-person) and private charters (per-hour), midday/evening/weekend | Experiences **$49–98/pp** (BHCC sunset $49, dinner $77–98, whale watch $75, Classic Harbor Line $87). Charters **$500–600/hr** for 20–25-pax vessels (Boston Charter Boat $550/hr, 2-hr min). A silent electric foiling harbor experience is a *premium* entrant in this set. | BHCC, Odyssey, NEAQ, CHL, Boston Charter Boat — all live 2025–26 prices |

**The anchor tenant is demoted, not deleted:** an employer buying a block of L1 bundles *at market per-seat prices* is welcome and accelerates the trigger — but no scenario depends on an above-market flat subsidy.

## 4 · The four levers — defensibility grading

| Lever | Market-proven? | Navier-proven? | Treatment in model |
|---|---|---|---|
| L1+L2 commute yield (bundles + spot) | ✅ universal (MBTA/Seastreak/Blade/NYC Ferry structures) | Partially — canon corridor fares approved, no Boston operations | **Base case**, conservative fills |
| L3 experiences & charters | ✅ deep Boston market at named prices | ❌ never operated | **Base case at deliberately thin utilization** (conservative counts ~⅓ of Boston operators' evident sailing frequency); fuller in mid |
| Sponsorship | ✅ transit precedents priced: Citi Bike ~$7–8M/yr system; Santander Cycles £6.25M/yr; Emirates cable car £3.6M/yr; Cleveland HealthLine $250K/yr line-naming; Barclays station $200K/yr | ❌ | **Upside only**, fleet-level $150K/yr placeholder (~1 line-naming precedent), never per-vessel headline |
| Cargo / overnight | ✅ **published waterborne tariffs found** (Casco Bay Lines 2026: $0.108–0.162/kg generic freight = $216–324 per ~2,000 kg run; Steamship Authority commercial tariffs) + medical-courier pricing (Dropoff 2026: $30–100/job, refrigerated $3.50–5.25/mi; Breakaway $21/delivery batch) | ❌ | **Upside only (Jaideep 2026-08-15), ~$350/run × 16 nights/mo = $5.6K/mo.** Key honesty finding: harbor cargo earns **courier-linehaul rates, not island air-substitute rates** — the $0.75–1.50/kg canon applies only where roads don't exist. First cargo classes: **medical/lab specimens** (Boston strength — clean, urgent, night-moving), batch parcels, catering/event. **Seafood rejected as first class**: premium-cabin odor/leakage/sanitation conflict, and it's commodity-priced ($2.50–3.75/box at Casco Bay) — low value AND wrong fit. Sources: `CARGO-LAYER-BENCHMARKS.md`. |

## 5 · Worked per-vessel model (N45, Boston)

Fixed inputs: $2.5M capex · 20 seats · energy 4.1 kWh/nm @ $0.30 (canon) · Navier network share 10% of gross (canon) · maintenance $82.5K/yr (midpoint of the unvalidated $65–100K range) · insurance+berth $7.7K/mo (placeholder) · crew $85/hr 2-crew fully loaded (placeholder) · 22 weekdays + up to 8 weekend days · commute = 8 legs/day × ~10 nm.

| | Conservative | Mid | Upside |
|---|---|---|---|
| L1 committed seats × price | 24 × $950 | 32 × $1,100 | 36 × $1,200 |
| L2 spot fill of residual commute capacity × fare | 10% × $45 | 20% × $55 | 30% × $60 |
| L3 experiences (sailings/mo × pax × price) | 10 × 10 × $59 | 28 × 13 × $69 | 40 × 15 × $79 |
| L3 charters (per mo × hrs × rate) | 3 × 2.0 × $550 | 6 × 2.25 × $550 | 10 × 2.5 × $600 |
| Sponsorship (fleet-level ÷ 4 vessels) | $0 | $0 | $3.1K/mo |
| Overnight cargo (16 runs/mo × $350 contract) | $0 | $0 | $5.6K/mo |
| **Gross revenue /mo** | **$43.1K** | **$91.0K** | **$149.2K** |
| Opex /mo (energy · crew · maint · ins/berth) | $28.8K | $33.0K | $36.4K |
| **Net to investor /mo** (gross × 0.90 − opex) | **+$10.0K** | **+$48.8K** | **+$97.9K** |
| **Annual** | +$120K | +$586K | +$1.17M |
| **Payback on $2.5M** | ~21 yr | **~4.3 yr** | **~2.1 yr** |
| v1 flat-rate model (same opex basis) | — | –$11.5K/mo · never | — |

**Honest reads:**
- The stack turns the conservative case **cash-positive with zero anchor** (v1 was –$138K/yr) — but ~21 yr is not financeable. Conservative here is deliberately punitive: 10% spot fill, 10 experience sailings/month in a market where incumbents run multiples of that.
- **Mid (~4.3 yr) is the honest financeable case** — it requires executing L3 at roughly half the cadence of Boston's incumbent experience operators, at prices below their dinner-cruise tier.
- Upside (~2.1 yr, incl. sponsorship + cargo upside lines) matches canon partner-corridor economics (2.49 yr) — the model's credibility anchor, not a coincidence.
- Crew is the swing cost ($142–225K/yr at full stacking) and has **no canon** — the walkthrough with engineering/ops should prioritize it.

## 6 · What changes where — APPROVED (Jaideep 2026-08-15, with cargo moved to upside alongside sponsorship)

1. **D6 revised → D6′:** Fleet Investors lead frame = **utilization-stack economics** (mid case headline, conservative shown, upside labeled). Anchor-plus-fill language removed as lead; anchor appears only as "employer block commitments accelerate the trigger — at market seat prices."
2. **FLEET-INVESTORS-BRIEF.md** — economics section rewritten around the yield architecture (§3) and the four-layer day.
3. **PR #361 pilot data (`boston/fleet-investors.json`)** — economics module re-authored to the stack model; benchmarks file referenced as source layer; cargo stays qualitative-only.
4. **Microsite honesty labels:** L3 revenue lines carry "market-priced (Boston operators cited); not yet operated by Navier." Sponsorship confined to upside with precedent citations. Cargo has no number anywhere.
5. **Boston seat price:** recommend adopting **$950–1,200/seat-month for Boston** (top of program band, 3–4× MBTA, ~50–60% off door-to-door substitute) — needs Jaideep sign-off to remove the "city pricing TBD" flag.
6. **Cascade:** the stack becomes the standard Fleet Investors economics template for the other six cities (each with city-specific benchmark research).

## 7 · Assumption register (deltas vs v1)

| Assumption | Value | Basis | Confidence |
|---|---|---|---|
| Committed-seat fills (24/32/36 of 40 max) | scenario | launch trigger is 60–80 seats/corridor ≈ 1.5–2 vessel-loads — 24 committed/vessel is consistent with trigger being met | Derived |
| Spot fill 10/20/30% of residual | scenario | no Navier precedent; MBTA ferry carried 1.4M trips 2024, +10% 2025 (demand exists); labeled unproven | Placeholder |
| Experience sailings 10/28/40 per month | scenario | incumbents (BHCC, CHL, Odyssey) run daily-to-multiple-daily schedules in season; conservative ≈ ⅓ of one daily sailing | Benchmark-bounded |
| Experience price $59–79 | benchmark | BHCC $49 sunset → Odyssey $98 dinner band | Sourced |
| Charter $550–600/hr, 2–2.5 hr | benchmark | Boston Charter Boat $550/hr (25 pax, 2-hr min); marketplace $500–600/hr | Sourced |
| Sponsorship $150K/yr fleet | placeholder | Cleveland HealthLine $250K/yr; Barclays $200K/yr; scaled down for novelty/no-precedent | Weak — upside only |
| Cargo $350/run × 16 nights/mo (upside only) | benchmark-anchored | Casco Bay 2026 published tariff $216–324 per ~2,000 kg run + medical/urgent per-job premium headroom (Dropoff 2026); contract-gated, not yet operated | Published-tariff-anchored, unproven by Navier |
| Crew $85/hr × activity hours | placeholder | v1 basis, extended to stacked hours | Not validated — top priority |
| Weekend operating days 4/8/8 | scenario | experiences market is weekend-heavy | Placeholder |

---
*All benchmark prices sourced in `REVENUE-LEVER-BENCHMARKS.md` with operator, year, URL, confidence. No invented economics; cargo and sponsorship fail closed out of the base case.*
