# Revenue-Stack Model — Fleet Investors Archetype (Seattle / Puget Sound)

**Date:** 2026-08-16 · **Status:** DRAFT for Jaideep review — Boston D6′ stack structure applied to Seattle with city-specific benchmarks; **Seattle seat pricing is DERIVED, no canon**
**Companion files:** `CREW-COST-SEATTLE.md` (loaded crew rate), `AUTHORITY-MAP-SEATTLE.md` (operators, landings, Bell Harbor berthing rates), `SPEED-RULES-SEATTLE.md` (posted limits honored in all times)
**Scope (locked):** Puget Sound corridors only, from hub.json — SND-1 Elliott Bay Line (Phase 1), SND-2 Sound Line (Phase 2/3), SND-3 Narrows (Phase 3). Lake Washington excluded. Fleet Investors firewall applies: vessel-fleet financing only; no Navier equity/round content.

---

## 1 · Structure (per Boston D6′ — one asset, one day, four demand layers)

Same architecture as `../boston/REVENUE-STACK-BOSTON.md`: L1 committed seat bundles + L2 spot seats + L3 experiences/charters in base; U1 sponsorship + U2 cargo as upside-only lines. One N45, 16-hr service day, 22 weekdays + up to 8 weekend days.

## 2 · Seattle pricing benchmarks (all sourced; captured 2026-08-16)

| Layer input | Benchmark | Price | Source | Confidence |
|---|---|---|---|---|
| Public premium-ferry pass | Kitsap Fast Ferries monthly pass (eff. Oct 1, 2025) | **$210/mo** ($2 EB / $13 WB one-way) | https://www.kitsaptransit.com/fares | sourced |
| Public ferry walk-on | WSF Seattle–Bainbridge adult | $11.35; 10-ride $92.80; monthly pass $148.50 | https://www.wsdot.wa.gov/ferries/fares/faresdetail.aspx?departingterm=7&arrivingterm=3 | sourced |
| Public water taxi | KCWT West Seattle / Vashon (ORCA) | $5.25 / $6.00 per ride | https://kingcounty.gov/en/dept/metro/travel-options/water-taxi/west-seattle · .../vashon | sourced |
| Door-to-door car substitute | Uber Edmonds→Seattle route average | **~$59** (15 mi, ~32 min) | https://www.uber.com/global/en/r/routes/edmonds-wa-to-seattle-wa/ | sourced |
| Door-to-door car substitute | Uber Tacoma→Seattle route average | **~$125** (34 mi, ~44 min) | https://www.uber.com/global/en/r/routes/tacoma-wa-to-seattle-wa/ | sourced |
| Parking | Downtown Seattle monthly parking | avg **~$220/mo**; downtown core garages $200–365 | https://spothero.com/city/monthly/seattle-parking | sourced (marketplace average) |
| Experience — harbor tour | Argosy Cruises 1-hr Harbor Cruise | from **$45.70** | https://www.tripadvisor.com/AttractionProductReview-g60878-d11448174 (operator page hides price in booking widget) | secondary |
| Experience — dinner cruise | Waterways Cruises Seattle dinner cruise | from **$89** | https://www.tripadvisor.com/AttractionProductReview-g60878-d13474998 | secondary |
| Experience — whale watch | Puget Sound Express half-day (Edmonds) | adult **$155** (2026) | https://www.pugetsoundexpress.com/seattle-half-day-whale-watching-tour/ | sourced |
| Charter — mid-size vessel | Seattle Water Tours (up to 42 pax) | **$1,675 / 2 hr + $825/addl hr** (≈$725–838/hr) | https://www.seattlewatertours.com/private-charter-faq/ | sourced |
| Charter — marketplace floor | Boatsetter Seattle party-vessel listings | ~$107–675+/hr | https://www.boatsetter.com/party-boat-rentals/seattle--wa--united-states | secondary |
| Berthing | Bell Harbor Marina guest moorage, under-50′ | $2.15–2.64/ft/day (+power $7–29/day) | https://www.portseattle.org/page/bell-harbor-marina-moorage-rates-and-info | sourced |
| Demand context | Kitsap 1.22M riders 2024 (record) · KCWT Vashon +55% H2-2024 on midday adds · WSF walk-ons +5.7% 2024 | — | see AUTHORITY-MAP §2 | sourced |

## 3 · L1 seat price — DERIVED (no Seattle canon)

**DERIVED band: $750–1,050/seat-month (cons $750 · mid $900 · upside $1,050).** Logic, Boston-style (pass discounted vs premium spot; positioned against substitutes):
- **3.6–5.0× the Kitsap fast-ferry monthly pass ($210)** — same multiple family as Boston's 3–4× MBTA $319 (Seattle's public anchors are more heavily subsidized, which caps the defensible multiple; going 4×+ requires the door-to-door argument below).
- **~55–70% below the door-to-door substitute** on regional runs: Uber Edmonds→Seattle ~$59 × 44 legs/mo ≈ $2,600/mo (Tacoma ≈ $5,500/mo) — deeper discount than Boston's ~50–60% because the public-transit reference points are cheaper here.
- Parking alone (~$220/mo avg, $300+ core) plus 2026 downtown drive times make the employer-subsidized comparison favorable; per-seat monthly ≈ parking + ~2 Uber round-trips.
- Within the program band ($650–1,200) and below Boston ($950–1,200) — honest, since Boston's premium public comparator ($319 MBTA ferry pass) is 50% above Seattle's ($210).
**Label wherever used: DERIVED — not a Seattle quote; program band applies.**

L2 spot: **$30/38/45 per leg** — bounded by WSF walk-on $11.35 / Kitsap $13 westbound (subsidized public floor) and Uber $59–125 (door-to-door ceiling); premium positioning nearer the ceiling on regional legs, yield-managed. L3 experiences **$55–75/pp** (Argosy $45.70 → Waterways $89 band; whale-watch $155 shows headroom for premium foiling products). L3 charters **$600–700/hr** (SWT $725–838/hr for a 42-pax displacement vessel; marketplace floor lower; a 20-seat premium foiler priced just under SWT is conservative).

## 4 · Worked per-vessel model (N45, Seattle)

Fixed inputs: $2.5M capex · 20 seats · energy 4.1 kWh/nm @ $0.30/kWh (canon) · Navier network share 10% of gross (canon) · maintenance $82.5K/yr = $6,875/mo (midpoint of unvalidated $65–100K range, Boston-consistent) · insurance+berth **$7.9K/mo** (berth ~$3.4K/mo anchored to Bell Harbor $2.50/ft/day × 45 ft; insurance $4.5K/mo placeholder) · **crew $120/hr 2-person loaded (BLS-validated — see CREW-COST-SEATTLE.md; LOW/MID drift to $121–122, HIGH stress $175)** · 22 weekdays + up to 8 weekend days · commute = 8 legs/day, avg ~5 nm/leg (Elliott Bay locals 2.2–2.3 nm + Bainbridge-overlay legs 6.6 nm; stated assumption) = 880 nm/mo · crew activity hours = commute 132 hr/mo + 1.5 hr per experience sailing + charter hrs + 0.5 hr wrap + 1.5 hr per cargo run (stated assumptions).

| | Conservative | Mid | Upside |
|---|---|---|---|
| L1 committed seats × price (DERIVED band) | 24 × $750 = $18,000 | 32 × $900 = $28,800 | 36 × $1,050 = $37,800 |
| L2 spot fill of residual commute capacity × fare | 10% × 2,464 seat-legs × $30 = $7,392 | 20% × 2,112 × $38 = $16,051 | 30% × 1,936 × $45 = $26,136 |
| L3 experiences (sailings/mo × pax × price) | 10 × 10 × $55 = $5,500 | 28 × 13 × $65 = $23,660 | 40 × 15 × $75 = $45,000 |
| L3 charters (per mo × hrs × rate) | 3 × 2.0 × $600 = $3,600 | 6 × 2.25 × $650 = $8,775 | 10 × 2.5 × $700 = $17,500 |
| U1 Sponsorship (fleet $150K/yr ÷ 4 vessels) | $0 | $0 | $3,125 |
| U2 Overnight cargo (16 runs/mo × $350) | $0 | $0 | $5,600 |
| **Gross revenue /mo** | **$34,492** | **$77,286** | **$135,161** |
| Opex /mo — crew | 154.5 hr × $120 = $18,540 | 190.5 hr × $120 = $22,860 | 246 hr × $120 = $29,520 |
| Opex /mo — energy (nm × 4.1 kWh × $0.30) | 1,045 nm = $1,285 | 1,306 nm = $1,606 | 1,830 nm = $2,251 |
| Opex /mo — maintenance | $6,875 | $6,875 | $6,875 |
| Opex /mo — insurance + berth | $7,900 | $7,900 | $7,900 |
| **Opex total /mo** | **$34,600** | **$39,241** | **$46,546** |
| **Net to investor /mo** (gross × 0.90 − opex) | **−$3,557** | **+$30,316** | **+$75,099** |
| **Annual** | −$43K | **+$364K** | **+$901K** |
| **Payback on $2.5M** | never (cash-negative) | **~6.9 yr** | **~2.8 yr** |

(Line items sum exactly to gross: 18,000+7,392+5,500+3,600 = 34,492 · 28,800+16,051+23,660+8,775 = 77,286 · 37,800+26,136+45,000+17,500+3,125+5,600 = 135,161.)

**Honest reads:**
- **Crew is the Seattle story.** At $120/hr loaded (vs Boston $85), the same stack that turns Boston's conservative case cash-positive leaves Seattle's conservative case **cash-negative (−$3.6K/mo)**. There is no cheap-crew scenario: metro medians ≈ means (union-shaped market). Seattle's fleet case *requires* executing the L3 day, not just running commutes.
- **Mid (~6.9 yr) is real but not yet financeable headline material** — it trails Boston's ~4.3 yr on two structural facts: ~41% higher crew cost and a DERIVED seat band ~$200/mo below Boston's (because Seattle's public-ferry comparators are cheaper). Levers that close the gap, in order of defensibility: (1) prove the upper half of the derived seat band ($1,000+) against door-to-door math with early LOIs; (2) speed-rule relief on buffer-dominated Elliott Bay legs → more cycles per crew-hour (labeled upside only — precedent: Stockholm P-12; local design precedent: *Rich Passage 1*, see SPEED-RULES §4); (3) second-vessel crew utilization sharing across the SND-1/SND-2 schedule spine.
- **Upside (~2.8 yr incl. both upside lines)** is in the canon convergence zone (Boston upside ~2.1, partner-corridor 2.49) — same physics, dragged by crew cost.
- **No Seattle canon partner corridor exists** to run the Boston-style convergence check against; the check here is against Boston/canon only. Flag, not a failure.
- Demand pools are **indicative** and come from hub.json employer data only (Expedia/Interbay at Elliott Bay Marina; downtown CBD at Bell Harbor; Bainbridge/Kingston/Edmonds/Des Moines residential origins). The region's public numbers (Kitsap 1.22M record, Vashon midday +55%, WSF walk-ons +5.7%) evidence growing passenger-water demand but are **not** transferable fill rates. Fail closed.

## 5 · U2 cargo — Seattle-appropriate clean class (upside only, courier-linehaul rates)

Same doctrine as Boston (`../boston/CARGO-LAYER-BENCHMARKS.md`): harbor cargo earns **courier-linehaul rates, not island air-substitute rates**; $350/run contract placeholder anchored to Casco Bay Lines' published 2026 tariff ($0.108–0.162/kg ≈ $216–324 per ~2,000-kg run) plus medical-courier premium headroom (Dropoff 2026 national guide: STAT $65–160/job; refrigerated $3.50–5.25/mi — https://www.dropoff.com/blog/medical-courier-service-rates/).
- **First clean classes for Seattle:** (1) **batch parcels / business documents** between downtown (Bell Harbor) and Bainbridge/Kingston/Edmonds town centers — the WSF walk-on corridors already carry informal versions of this flow; (2) **catering/event logistics** for waterfront venues; (3) **medical/lab specimens only on corridor-fit pairs** — hub corridors connect island/peninsula clinics (Winslow, Kingston, Edmonds) to downtown Seattle, and island-origin specimen flows to Seattle labs are plausible **but no Seattle waterborne specimen contract or published local courier tariff was found — fail closed; class remains a candidate pending a named counterparty** (Seattle courier firms surveyed publish no rates: e.g., https://statexperts.com/ — quote-only).
- No seafood in the premium cabin (Boston finding stands, doubly so in a fishing port). No number renders anywhere.

## 6 · Assumption register (deltas vs Boston)

| Assumption | Value | Basis | Confidence |
|---|---|---|---|
| L1 seat price $750–1,050 | DERIVED | §3 derivation vs Kitsap $210 pass, Uber $59–125, parking ~$220 | Derived — needs Jaideep sign-off before any page use |
| Committed fills 24/32/36 | scenario | launch trigger 60–80 seats/corridor ≈ 1.5–2 vessel-loads (program canon) | Derived |
| Spot fills 10/20/30% × $30/38/45 | scenario | no Navier precedent; regional demand growth cited §4; labeled unproven | Placeholder |
| Experience sailings 10/28/40 × $55–75 | scenario | Argosy runs multiple daily harbor tours in season; conservative ≈ ⅓ of one daily sailing; prices below incumbent dinner tier | Benchmark-bounded |
| Charters 3/6/10 × $600–700/hr | benchmark | SWT $725–838/hr (42-pax); Boatsetter floor $107+ | Sourced |
| Crew $120/hr × activity hours | benchmark-validated | BLS OEWS Seattle metro × 1.4294 × drift (CREW-COST-SEATTLE.md); LOW≈MID quirk documented | Validated at rate level |
| Commute 8 legs × ~5 nm avg | stated assumption | SND-1 legs 2.2–2.3 nm + Bainbridge 6.6 nm mix; hub.json geometry only | Derived from hub.json |
| Berth $3.4K/mo | benchmark-anchored | Bell Harbor published $2.50/ft/day × 45 ft; commercial long-term terms TBD | Sourced anchor, terms placeholder |
| Insurance $4.5K/mo | placeholder | no Seattle quote | Weak |
| Sponsorship $150K/yr fleet | placeholder | Boston precedent set (Citi Bike/HealthLine etc.); no Seattle-specific precedent priced | Weak — upside only |
| Cargo $350/run × 16 | benchmark-anchored | Casco Bay 2026 tariff + Dropoff 2026; no Seattle contract | Upside only |
| Weekend days 4/8/8 | scenario | experiences market weekend-heavy | Placeholder |
| Winter reliability | unmodeled | year-round precedent real (WSF/KCWT/Kitsap); N45 foilborne-through-chop is an operational consideration, not a modeled uptime bonus; longer SND-2 legs carry more weather exposure | Flagged |

---
*Every number above is sourced, derived (labeled), or canon (labeled). Base times respect posted limits per SPEED-RULES-SEATTLE.md. No invented demand; cargo and sponsorship fail closed out of the base case. Plain-English audience-safe copy is authored FROM this file; internal audit language never renders.*

---

## Scope amendment 2026-08-16 — Lake Washington cluster reopened

Jaideep directive 2026-08-16: LKW-1/LKW-2 re-enter the rendered network (see SPEED-RULES-SEATTLE.md §7 + EASTSIDE-VERIFICATION-2026-08-16.md). **Economics in this file are unchanged** — every revenue layer remains anchored on the documented Puget Sound corridors and benchmarks. Lake corridors are additive network reach; no lake-corridor demand, fare, or utilization figure exists yet, so none enters the P&L. Fail closed: any future lake-corridor economics require their own sourced benchmarks pass.
