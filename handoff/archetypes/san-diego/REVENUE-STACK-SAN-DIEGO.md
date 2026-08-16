# Revenue-Stack Model — Fleet Investors Archetype (San Diego Bay)

**Date:** 2026-08-16 · **Status:** research draft for Jaideep review — Boston D6′ utilization-stack template applied per cascade (`../boston/REVENUE-STACK-BOSTON.md` §6.6); San Diego seat pricing is **DERIVED, not canon**
**Companion files:** `CREW-COST-SAN-DIEGO.md` (loaded crew rate), `SPEED-RULES-SAN-DIEGO.md` (corridor speed basis), `hub.json` (all corridors/route times)
**Fleet Investors firewall applies:** vessel-fleet financing only; no Navier equity/round content.

---

## 1 · What San Diego changes about the Boston frame (stated plainly)

Same asset, same four-layer day — but **the commute price floor is far lower here and the tourism layer is far stronger.** San Diego's public substitutes are cheap ($2.50 trolley / $72 month pass; $15 public ferry on the exact flagship pair; ~$29 Uber Chula Vista→downtown vs Boston's ~$56 comparators), so L1/L2 price at the **bottom of the program band**, not the top. Offsetting that: a year-round, perfect-weather experiences market (whale season Dec–Apr, daily harbor tours, 200+ convention/resort event days between two on-network convention centers). The honest output: **commute yield alone is thinner than Boston's; the L3 layer carries more of the payback.** Crew also prices ~10% above Boston (see `CREW-COST-SAN-DIEGO.md`).

Demand-pool honesty: no invented demand. Committed-seat fills reference the 60–80 seat launch trigger; corridor demand context comes from `hub.json` employer data (Gaylord Pacific ~1,600 rooms / ~800 hires at opening at the Chula Vista landing; downtown/Convention Center forward run) — **indicative only**.

## 2 · The reframe (unchanged from Boston D6′)

One N45, one 16-hour day, four demand layers: L1 committed commuter bundles + L2 spot seats on residual capacity (base), L3 experiences/charters (base at thin utilization), U1 sponsorship + U2 overnight cargo (upside only, never base). The anchor tenant stays demoted: employer blocks welcome **at market per-seat prices** to accelerate the trigger; no scenario depends on an above-market subsidy.

## 3 · Pricing methodology — San Diego benchmarks (all sourced, retrieved 2026-08-16)

### 3a · Benchmark table

| Benchmark | Price | Unit | Operator/Source | URL | Confidence |
|---|---|---|---|---|---|
| Coronado Ferry (Broadway Pier↔Coronado; Convention Center↔Coronado) | $9.00 one-way / $18 RT, taxes included; 15 min; every 30–60 min | per trip | Flagship Cruises & Events | https://www.flagshipsd.com/cruises/flagship-ferry · https://coronadoferrylanding.com/ferry-info/ | sourced |
| Chula Vista Ferry (Chula Vista Marina↔Fifth Avenue Landing; launched June 1, 2026) | $15.00 one-way; ~45 min (vessel *Balboa*, 32 pax, 10 kn) | per trip | Flagship; KPBS/NBC launch coverage | https://www.flagshipsd.com/cruises/flagship-ferry · https://www.kpbs.org/news/living/2026/06/01/new-chula-vista-to-san-diego-ferry-service-officially-launches | sourced |
| Coronado commuter runs | Fare-free weekday mornings (City of Coronado-supported, since 1993) | per trip | Flagship | https://www.flagshipsd.com/commuter-ferry | sourced |
| MTS transit (Blue Line Trolley serves Chula Vista↔downtown, ~45 min) | $2.50 one-way; **$72 adult month pass** (PRONTO fare-capping) | per trip / month | MTS | https://www.sdmts.com/fares/pronto | sourced |
| Uber Chula Vista→San Diego (route average) | ~$29 average (11 mi, ~19 min) | per ride, trailing average | Uber official route page | https://www.uber.com/global/en/r/routes/chula-vista-ca-to-san-diego-ca/ | sourced (premium tiers not published for this route — fail closed) |
| Downtown SD monthly parking | Bookable deals $120–175/mo (SpotAngels listings); avg ~$280/mo, range $91–813 (Spacer, secondary) | per stall-month | SpotAngels / Spacer | https://www.spotangels.com/san-diego/downtown-monthly-parking · https://www.spacer.com/parking-downtown-san-diego-san-diego-ca-usa | sourced / secondary |
| Flagship 1-hr harbor tour (North or South Bay) | $39.22 adult all-in ($37.00 + taxes/fees) | per person | Flagship | https://www.flagshipsd.com/cruises/san-diego-harbor-tour | sourced |
| Flagship 2-hr Full Bay tour | $44.52 adult all-in | per person | Flagship | https://www.flagshipsd.com/cruises/san-diego-harbor-tour | sourced |
| City Cruises SD whale & dolphin watch (Dec–Apr season) | from $63–79 | per person | City Experiences | https://www.cityexperiences.com/san-diego/city-cruises/san-diego-whale-dolphin-watch-adventure/ | sourced |
| Flagship champagne brunch cruise | $101.17 adult | per person | Flagship | https://www.flagshipsd.com/cruises/brunch-cruise | sourced |
| Flagship harbor dinner cruise | $100.16 weekday / $110.79 Saturday, adult | per person | Flagship | https://www.flagshipsd.com/cruises/nightly-dinner-cruise | sourced |
| City Cruises SD premier dinner cruise | from $135 (fees/taxes incl.) | per person | City Experiences | https://www.cityexperiences.com/san-diego/city-cruises/dinner-cruises/ | sourced |
| SD yacht charter market floor | from $225/hr (Boatsetter index); mid-size from ~$350/hr (Sailo); "luxury" listings ~$400/hr (GetMyBoat) | per hour | marketplaces | https://www.boatsetter.com/yacht-rentals/san-diego--ca--united-states · https://www.sailo.com/boat-rentals/CA/San_Diego · https://www.getmyboat.com/boat-rental/San-Diego--CA--United-States/ | secondary (marketplace) |
| Triton Charters (crewed, 40–100 pax) | $975/hr (≤40 guests) up to $2,400/hr (≤100) | per hour | Triton Charters | https://triton-charters.com/ | sourced |
| Medical courier benchmark (national; no SD-published tariff found) | Standard same-day $30–45 (0–10 mi); STAT $90–160+; refrigerated $3.50–5.25/mi | per job / mile | Dropoff 2026 rate guide | https://www.dropoff.com/blog/medical-courier-service-rates/ | industry survey |
| Waterborne freight base-rate comparator | $0.108–0.162/kg published tariff (≈$216–324 per ~2,000 kg run) | per kg | Casco Bay Lines 2026 tariff (per `../boston/CARGO-LAYER-BENCHMARKS.md`) | https://www.cascobaylines.com/uploads/Att_5_Tariff_effective_2_28_26-1-1.pdf | published tariff (non-SD) |
| Sponsorship precedents | Citi Bike ~$7–8M/yr system; Santander Cycles £6.25M/yr; Cleveland HealthLine $250K/yr line; Barclays station $200K/yr | per year | per `../boston/REVENUE-LEVER-BENCHMARKS.md` §4 | (see Boston file for URLs) | sourced (non-SD precedents) |

### 3b · Yield architecture

| Layer | Product | San Diego pricing logic | Anchors |
|---|---|---|---|
| **L1 · Committed bundles** | Monthly commuter seat (AM+PM guaranteed) | **DERIVED — no canon.** Premium-spot equivalent: 32 legs/mo × $30 Navier spot (see L2) = $960/mo; apply the universal pass-discount structure (26–51% off spot: MBTA/Seastreak/NYC Ferry/Blade, per Boston benchmarks) → **$650–850/seat-month**. Floor = program band floor ($650). Cross-checks: ~70–90% of the $928/mo Uber-equivalent (32 × $29) — a thinner substitute headroom than Boston's 50–60%; ~2.3–5× downtown parking ($120–280/mo + drive time); ~9–12× the $72 MTS pass (the honest weak point — San Diego's public floor is very low; the product sells time, a guaranteed seat, and a bayfront-to-bayfront pair the trolley doesn't serve). | Uber $29; CV ferry $15; parking $120–280; MTS $72 |
| **L2 · Spot seats** | Per-leg, yield-managed residual | **$25–35/leg**, positioned above the $15 public ferry (guaranteed seat, ~25–40% faster than the 45-min *Balboa*, schedule breadth) and around/above the $29 Uber average. DERIVED. | CV ferry $15; Uber ~$29 |
| **L3 · Block products** | Experiences (per-person) & charters (per-hour) | Experiences **$39–79/pp**: entry at the $39–45 harbor-tour tier, mid at whale-watch tier ($63–79), premium below the $100–135 dinner tier. Charters **$550–600/hr** for a 20-pax premium electric foiler — inside the SD market band ($225–400/hr marketplace floor → $975/hr crewed 40-pax). A silent foiling bay experience is a premium entrant with year-round weather; whale season (Dec–Apr) is a proven seasonal spike. | Flagship/City Cruises/Triton rows above |
| **U1 · Sponsorship** | Fleet-level naming/branding | Upside only; $150K/yr fleet placeholder ÷ 4 vessels (transit precedents per Boston §4; no SD-specific deal found — fail closed to placeholder) | HealthLine $250K/yr etc. |
| **U2 · Overnight cargo** | Scheduled contract runs, courier-linehaul rates | Upside only; **$350/run × 16 nights/mo**, anchored to Casco Bay's published waterborne tariff (~$216–324/2,000-kg run) + urgent-courier premium headroom (Dropoff). **San Diego first clean classes: convention/event materials & catering** — the network uniquely links two convention centers (SD Convention Center at Fifth Avenue Landing; Gaylord Pacific at Chula Vista) one water hop apart — plus batch parcels. Medical/lab is secondary here (no bay-adjacent hospital cluster verified). No SD courier publishes a tariff (fail closed to national survey). | Casco Bay tariff; Dropoff 2026 |

## 4 · The four levers — defensibility grading

| Lever | Market-proven in SD? | Navier-proven? | Treatment |
|---|---|---|---|
| L1+L2 commute yield | ✅ structure universal; **live local proof**: $15 public ferry on the exact SD-1 pair (June 2026) + 30-yr city-funded commuter runs | ❌ no SD operations; pricing DERIVED | **Base case**, conservative fills, derived prices at program-band bottom |
| L3 experiences & charters | ✅ deep year-round market at named prices (Flagship, City Cruises, Triton) | ❌ | **Base case at thin utilization** (conservative ≈ 40% of one daily sailing vs incumbents' multiple-daily schedules) |
| U1 sponsorship | ✅ transit precedents (non-SD) | ❌ | Upside only, fleet-level placeholder |
| U2 cargo | ⚠ published waterborne tariffs exist (non-SD); SD courier market exists but publishes no rates | ❌ | Upside only, $350/run contract placeholder, convention/event-linked |

## 5 · Worked per-vessel model (N45, San Diego)

Fixed inputs: $2.5M capex · 20 seats · energy 4.1 kWh/nm @ $0.30 (canon) · Navier network share 10% of gross (canon) · maintenance $82.5K/yr = $6,875/mo (midpoint of the unvalidated $65–100K range, per Boston) · insurance+berth $7,700/mo (placeholder, carried from Boston — SD berth rates not validated) · **crew $93/hr 2-crew fully loaded** (VALIDATED against BLS: SD metro mean loaded $85.08/hr May 2023 × ~3%/yr drift → $92.97; see `CREW-COST-SAN-DIEGO.md`) · 22 weekdays + up to 8 weekend days · commute = 8 legs/day × 6.53 nm on SD-1 (hub.json; ~35–40 min/leg **including the posted 5 mph South Bay tail**) → commute crewed block 6.5 hr/day.

| | Conservative | Mid | Upside |
|---|---|---|---|
| L1 committed seats × price (DERIVED) | 24 × $650 = $15,600 | 32 × $750 = $24,000 | 36 × $850 = $30,600 |
| L2 spot fill of residual commute capacity × fare | 10% × $25 = $6,160 | 20% × $28 = $11,827 | 30% × $32 = $18,586 |
| L3 experiences (sailings/mo × pax × price) | 12 × 10 × $39 = $4,680 | 30 × 13 × $59 = $23,010 | 45 × 15 × $79 = $53,325 |
| L3 charters (per mo × hrs × rate) | 3 × 2.0 × $550 = $3,300 | 6 × 2.25 × $550 = $7,425 | 10 × 2.5 × $600 = $15,000 |
| U1 sponsorship (fleet-level ÷ 4 vessels) | $0 | $0 | $3,125 |
| U2 overnight cargo (16 runs/mo × $350 contract) | $0 | $0 | $5,600 |
| **Gross revenue /mo** | **$29,740** | **$66,262** | **$126,236** |
| Opex /mo (crew · energy · maint · ins/berth) | $31,837 (168.5 h crew $15,671 · energy $1,591 · $6,875 · $7,700) | $35,157 (201.5 h crew $18,740 · energy $1,842 · $6,875 · $7,700) | $41,032 (259.5 h crew $24,134 · energy $2,323 · $6,875 · $7,700) |
| **Net to investor /mo** (gross × 0.90 − opex) | **−$5,071** | **+$24,479** | **+$72,580** |
| **Annual** | −$61K | +$294K | +$871K |
| **Payback on $2.5M** | never (cash-negative) | **~8.5 yr** | **~2.9 yr** |
| v1 flat-rate commuter-only comparator (mid L1 only, same opex basis) | — | −$7.7K/mo · never | — |
| *Labeled sensitivity: Mid with L1 at program-band $1,000 (NOT locally derived)* | — | *+$31,679/mo · ~6.6 yr* | — |

L2 mechanics: residual seat-legs = (160 seat-legs/day − 2 × L1 seats) × 22 days = 2,464 / 2,112 / 1,936; filled legs = 246.4 / 422.4 / 580.8. Energy: commute 1,149 nm/mo + experiences ~10 nm/sailing + charters ~8 nm/hr-block + cargo 13.1 nm RT × 16. Crew hours = commute 143 + experiences 1.5 h/sailing + charters 2.5–3 h incl. positioning + cargo 1.5 h/run.

**Honest reads:**
- **San Diego's stack does not rescue the conservative case.** At locally derived seat prices (program-band bottom) and SD crew rates, conservative is cash-negative (−$5.1K/mo) — worse than Boston's +$10K — because L1 sits ~$300/seat below Boston while crew costs ~10% more. The conservative case is deliberately punitive (10% spot fill, 12 experience sailings in a market where the incumbent runs multiple daily tours year-round), but the direction is real.
- **Mid (~8.5 yr) is honest but not yet financeable** (Boston mid: ~4.3 yr). The gap is almost entirely the derived L1/L2 price level. What moves it: (a) proving the premium over the $15 public ferry supports $30+ spot / $850+ bundles (Point Loma's $142,897-income catchment on SD-2 is the test case — no scheduled service exists on that pair); (b) L3 execution above the deliberately thin base counts — San Diego is the strongest L3 market of the seven cities (year-round weather, whale season, two on-network convention centers); (c) speed relief on the South Bay tail (see `SPEED-RULES-SAN-DIEGO.md` §4 — the Port Code's own channel exemption) compressing cycle times. All three are labeled upside, never blended into base.
- **Upside (~2.9 yr) approaches canon partner-corridor territory** (Boston↔Hingham 2.49 yr; Boston stack upside 2.1 yr) — same physics: a premium vessel utilized across the whole day pays back in ~3 years; a commuter-only vessel never does (v1 comparator: −$7.7K/mo).
- **Crew is the swing cost** ($188–290K/yr across scenarios at $93/hr). Rate is benchmark-validated; the incumbent's visible pay scale ($67.74/hr loaded equivalent) suggests buffer. Split-shift structure for the 16-hr day remains an ops-walkthrough item.
- The $7.7K/mo insurance+berth placeholder is **unvalidated in SD** — Port-tenant berth terms are a named open flag (AUTHORITY-MAP §7). Fail-closed carried, flagged.

## 6 · What changes where

1. **Fleet Investors San Diego page** leads with the utilization stack, mid case headline, conservative shown honestly, upside labeled — same D6′ grammar as Boston, with SD-derived prices and the "L3-heavy market" framing.
2. **Seat-price flag:** hub.json's "San Diego-specific pricing TBD" stays until Jaideep signs off a band; this file recommends **$650–850/seat-month DERIVED** (bottom of program band) as the defensible starting band.
3. **No SD-specific benchmarks file yet** — §3a above is the source layer; if the SD page ships, split §3a into `REVENUE-LEVER-BENCHMARKS-SAN-DIEGO.md` for parity with Boston's file structure.
4. **Honesty labels on-page:** L3 lines "market-priced (San Diego operators cited); not yet operated by Navier"; sponsorship upside-only with precedent citations; cargo has no number anywhere public; incumbent-respect language on every commute panel (complement to the existing bay ferry).

## 7 · Assumption register

| Assumption | Value | Basis | Confidence |
|---|---|---|---|
| L1 seat price $650–850/mo | DERIVED | 32-leg spot-equivalent ($960) × pass discount 26–51%; Uber-equivalent $928/mo ceiling; program-band floor | Derived (weakest link — verify in market) |
| Committed-seat fills 24/32/36 of 40 max | scenario | 60–80 seat corridor trigger ≈ 1.5–2 vessel-loads (canon) | Derived |
| L2 spot $25–35, fill 10/20/30% | scenario | bounded by $15 public ferry and $29 Uber; no Navier precedent | Placeholder |
| Experience sailings 12/30/45 per month | scenario | incumbents run daily-to-multiple-daily year-round; conservative ≈ 0.4/day | Benchmark-bounded |
| Experience price $39–79 | benchmark | Flagship $39.22 harbor tour → City Cruises $63–79 whale watch; below $100–135 dinner tier | Sourced |
| Charter $550–600/hr, 2–2.5 hr | benchmark | SD band $225–400/hr marketplace → $975/hr crewed 40-pax (Triton) | Sourced (position within band is judgment) |
| Sponsorship $150K/yr fleet | placeholder | non-SD transit precedents (Boston file §4) | Weak — upside only |
| Cargo $350/run × 16 nights | benchmark-anchored | Casco Bay published tariff + courier premium (Dropoff); convention/event class fits network geometry | Published-tariff-anchored (non-SD), unproven |
| Crew $93/hr | benchmark-validated | BLS OEWS SD metro mean × 1.4294 ECEC × ~3%/yr drift (`CREW-COST-SAN-DIEGO.md`) | Validated at rate level |
| Commute block 6.5 h/day, 8 legs × 6.53 nm | hub.json geometry | SD-1 at posted limits incl. 5 mph tail (35–40 min/leg + dwell/positioning) | Derived from hub + speed rules |
| Energy $0.30/kWh | canon | program canon; SDG&E commercial rates not validated this pass — flag if SD-specific energy pass happens | Canon (labeled) |
| Insurance+berth $7.7K/mo | placeholder | carried from Boston; SD berth terms unvalidated | Placeholder — open flag |
| Weekend operating days 4/8/8 | scenario | experiences market weekend-heavy; SD year-round | Placeholder |

---
*All San Diego prices captured from live pages 2026-08-16 (URLs in §3a). Non-SD anchors (Casco Bay tariff, sponsorship precedents, pass-discount structures) cite the Boston benchmark files. No invented economics; sponsorship and cargo fail closed out of the base case; seat pricing is DERIVED and flagged for sign-off.*
