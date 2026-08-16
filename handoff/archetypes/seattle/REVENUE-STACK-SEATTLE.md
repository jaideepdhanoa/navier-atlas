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

## 7 · Scope amendment 2026-08-16 — Lake Washington cluster reopened

Jaideep directive 2026-08-16: LKW-1/LKW-2 re-enter the rendered network (see SPEED-RULES-SEATTLE.md §7 + EASTSIDE-VERIFICATION-2026-08-16.md). **Economics in §1–§6 are unchanged** — every revenue layer there remains anchored on the documented Puget Sound corridors and benchmarks. Lake corridors were initially additive network reach only.

**Superseded in part, same day (Jaideep-approved second pass):** the sourced-benchmarks condition below has now been met — `EASTSIDE-DEMAND-BENCHMARKS.md` (2026-08-16) is that pass — so §8 adds a **separate, dedicated lake-corridor vessel stack**. The Sound-anchored per-vessel N45 model in §4 is untouched; no lake figure is blended into it. Fail-closed doctrine carries forward: the lake stack uses only sourced or labeled-derived inputs.

---

## 8 · Lake-corridor vessel stack (added 2026-08-16 · rebuilt same day on the N45)

**Vessel class — corrected 2026-08-16:** this stack runs on the **N45 in 20-seat commuter configuration**, the program standard for commuter corridors. The launch gate itself — 60–80 committed seats per corridor — is N45-scale demand by definition, so an 8-seat hull was the wrong class for the corridors it gates. The initial same-day N30 draft is **superseded**; the only lines carried over unchanged are the L3 experience/charter quantities (sized off sourced Seattle benchmarks, vessel-class-independent at these fill levels) and the crew activity-hour bands they drive.

**What this is:** the parallel utilization stack for **one N45 (20 seats) dedicated to the Lake Washington cluster** — LKW-1 Cross-Lake (Leschi ↔ Meydenbauer, 3.38 nm) + LKW-2 Eastside (Kirkland ↔ Carillon ↔ Meydenbauer ↔ Renton/Coulon, 6.14 / 10.34 nm legs). Same D6′ architecture as §1: L1 committed bundles + L2 spot + L3 experiences/charters in base; no U1/U2 for the lake vessel (omitted — no lake-specific sponsorship or cargo benchmark exists; fail closed).

**Why a separate stack (structural, not stylistic):** Lake Washington connects to Puget Sound only through the Ballard Locks — a first-come lock queue with a blanket 7-kn Ship Canal transit (see hub.json decision ledger). A lake vessel cannot flex onto Sound corridors intraday or even same-week without an hours-long, unschedulable transit. **A lake vessel is a dedicated asset**, so its economics must stand alone. Nothing here sums with §4.

**Demand gate unchanged:** a lake corridor advances only at **60–80 committed seats on that corridor** (program canon, hub.json locked_numbers). The fills below stay deliberately punitive: conservative 40 sits at the bottom of the combined conservative corridor ranges (LKW-1 20–32 + LKW-2 20–28 = 40–60, EASTSIDE-DEMAND-BENCHMARKS §4); mid 56 sits inside them; **upside 72 exceeds them and assumes at least one corridor at gate scale (60–80)** — say so wherever it renders.

### 8.1 · Assumption register (each row sourced or derived)

| Assumption | Value | Basis / source | Confidence |
|---|---|---|---|
| Vessel | **N45, 20 seats** | program-standard commuter class — same vessel and configuration as §4 (N30 draft superseded; commuter corridors run 20-seat vessels) | Canon |
| Capex | **$2.5M** | N45 program canon, same as §4 | Canon |
| L1 seat price $750/900/1,050 | DERIVED band | §3 derivation (3.6–5.0× Kitsap $210 pass; 55–70% below door-to-door). Lake check: Uber Bellevue→Seattle ~$48 × 44 legs ≈ $2,100/mo, Kirkland ~$57 ≈ $2,500/mo (EASTSIDE-DEMAND-BENCHMARKS §3 [27][33]) — $900 mid ≈ 57–64% below | Derived — same sign-off flag as §3 |
| L1 committed seats 40/56/72 | scenario | EASTSIDE-DEMAND-BENCHMARKS §4 combined conservative corridor ranges 40–60: cons 40 = bottom (2.0 vessel loads), mid 56 inside (2.8), upside 72 above — assumes ≥1 corridor at the 60–80 gate (3.6 loads); one N45's rider ceiling ≈ 120 distinct riders (6 peak-direction sailings × 20 seats) | Derived |
| L2 spot fare $25/30/35 per leg | DERIVED | Undercuts/matches solo substitutes: Uber Bellevue→Seattle avg $48 (Electric $35), Kirkland→Seattle $57 (EASTSIDE §3 [33][27]); floor context: no public lake service exists at all (last ferry 1950, EASTSIDE §3 [31][32]) | Derived |
| L2 spot fill 10/20/30% of residual | scenario | residual = 5,280 − committed × 44; no precedent; same fill doctrine as §4 | Placeholder |
| L3 experiences 6/12/20 sailings × 6/7/8 pax × $55/65/75 | benchmark-bounded | §2 band (Argosy from $45.70 → Waterways $89); Waterways and Argosy both operate lake cruises; unchanged from first pass — small-group sailings well under the 20-seat cabin | Benchmark-bounded |
| L3 charters 2/4/6 × 2.0/2.0/2.5 hr × $400/450/500/hr | DERIVED | unchanged from first pass: premium foiler priced well under SWT $725–838/hr (42-pax displacement, §2), above Boatsetter floor $107+/hr | Derived |
| Commute schedule 12 legs/day × ~4.5 nm avg, 22 days | stated assumption | hub.json geometry: LKW-1 legs 3.38 nm (12–15 min) mixed with LKW-2 spine runs 6.14/10.34 nm; capacity 20 × 12 × 22 = **5,280 seat-legs/mo**; committed riders ≈ 2 legs/day (44/mo) | Derived from hub.json |
| Crew $120/hr 2-person loaded, 146/160/180 hr/mo | benchmark-validated | CREW-COST-SEATTLE.md (BLS OEWS Seattle metro; LOW≈MID); same activity-hour rules as §4 (132 commute + 1.5 hr/experience + charter hrs + 0.5 hr wrap per charter); bands unchanged from the N30 draft because the L3 day is unchanged. A 20-passenger COI is a two-crew operation like §4 — the N30-era single-captain case is dropped | Validated at rate level |
| Energy 4.1 kWh/nm × $0.30/kWh | canon (N45 rate) | program canon; experience sailings ~8 nm, charters ~5 nm/hr (stated) | Canon |
| Maintenance $82.5K/yr = $6,875/mo | benchmark-anchored | same Seattle N45 figure as §4 — midpoint of the unvalidated $65–100K range | Derived |
| Insurance + berth $7,900/mo | Sound convention reused | berth ~$3.4K = Bell Harbor published $2.50/ft/day × 45 ft (no lake-marina commercial rate sourced — Kirkland/Carillon/Bellevue terms TBD); insurance $4.5K placeholder, same as §4 — estimated | Weak — placeholder |
| Navier network share 10% of gross | canon | program canon | Canon |
| Launch gate 60–80 committed seats/corridor | canon | hub.json locked_numbers | Canon |

### 8.2 · Worked per-vessel model (N45, lake corridors)

Total commute seat-legs/mo = 20 seats × 12 legs × 22 days = 5,280. Residual = 5,280 − committed × 44 legs/mo.

| | Conservative | Mid | Upside |
|---|---|---|---|
| L1 committed seats × price (DERIVED band) | 40 × $750 = $30,000 | 56 × $900 = $50,400 | 72 × $1,050 = $75,600 |
| L2 spot fill × residual seat-legs × fare (DERIVED fare) | 10% × 3,520 × $25 = $8,800 | 20% × 2,816 × $30 = $16,896 | 30% × 2,112 × $35 = $22,176 |
| L3 experiences (sailings × pax × price) | 6 × 6 × $55 = $1,980 | 12 × 7 × $65 = $5,460 | 20 × 8 × $75 = $12,000 |
| L3 charters (per mo × hrs × rate) | 2 × 2.0 × $400 = $1,600 | 4 × 2.0 × $450 = $3,600 | 6 × 2.5 × $500 = $7,500 |
| **Gross revenue /mo** | **$42,380** | **$76,356** | **$117,276** |
| Opex — crew (hrs × $120) | 146 hr = $17,520 | 160 hr = $19,200 | 180 hr = $21,600 |
| Opex — energy (nm × 4.1 kWh × $0.30) | 1,256 nm = $1,545 | 1,324 nm = $1,629 | 1,423 nm = $1,750 |
| Opex — maintenance | $6,875 | $6,875 | $6,875 |
| Opex — insurance + berth | $7,900 | $7,900 | $7,900 |
| **Opex total /mo** | **$33,840** | **$35,604** | **$38,125** |
| **Net to investor /mo** (gross × 0.90 − opex) | **+$4,302** | **+$33,116** | **+$67,423** |
| **Annual** | **+$51.6K** | **+$397.4K** | **+$809.1K** |
| **Payback on $2.5M** | **~48 yr** | **~6.3 yr** | **~3.1 yr** |

(Line items sum exactly to gross: 30,000+8,800+1,980+1,600 = 42,380 · 50,400+16,896+5,460+3,600 = 76,356 · 75,600+22,176+12,000+7,500 = 117,276. Energy nm: commute 1,188 + experiences 48/96/160 + charters 20/40/75. Nets rounded to the dollar from unrounded gross×0.90: 38,142.00−33,840 = 4,302 · 68,720.40−35,604 = 33,116.40 → 33,116 · 105,548.40−38,125 = 67,423.40 → 67,423. Annual from unrounded nets: 51,624 / 397,396.8 / 809,080.8. Payback: 2.5M ÷ annual = 48.4 / 6.29 / 3.09 yr.)

**Honest reads:**
- **Twenty seats absorb the Seattle crew day.** The lake vessel pays the same 2-person $120/hr crew over the same 146/160/180 activity hours as the N30 draft did — but 20 seats of L1/L2 capacity now sit on top of it. That flips every scenario cash-positive, including the deliberately punitive conservative case (+$4.3K/mo vs the N30 draft's −$11.3K/mo). Class choice, not optimism: the fills stay bottom-of-range.
- **Conservative (~48-yr payback) is a floor statement, not a financing case.** It renders with its payback because it is cash-positive, but 40 committed seats at the bottom of the derived band is the punitive doctrine case, same as §4's cash-negative conservative.
- **Mid (~6.3 yr) lands beside the Sound vessel's ~6.9 yr** — the lake case is no longer structurally worse than the Sound case. Same levers as §4 apply, led by proving the upper seat band ($1,000+) with Eastside LOIs; the door-to-door math ($2,100–2,500/mo Uber-equivalent) supports it.
- **Upside (~3.1 yr) is honest only with its demand condition attached:** 72 committed seats exceeds the combined conservative corridor ranges (40–60) and assumes **at least one corridor at the 60–80 gate**. It sits near the canon convergence zone (Sound upside ~2.8, Boston ~2.1, partner-corridor 2.49).
- **The single-captain sensitivity is dropped.** It was an N30 lever; a 20-passenger service runs captain + deckhand like the Sound vessel, so no captain-only case is modeled or rendered.
- Demand inputs are corridor-level potential from EASTSIDE-DEMAND-BENCHMARKS (Boeing Renton walk-tier ~12,000 [2019 figure]; Google Kirkland 5,076; Amazon Bellevue 17,500→25K and downtown Bellevue >60K shuttle-tier; Microsoft >52K shuttle-only via Carillon) — **indicative, never fill rates**. The 2 Line (open 2026-03-28) directly serves Seattle↔downtown Bellevue; the water case does its structural work on **Kirkland and Renton, which have no rail**.
- No lake revenue, cost, or payback figure here blends into §4, the Sound fleet case, or any cross-vessel total. Renders only as a separately labeled dedicated-vessel case.
