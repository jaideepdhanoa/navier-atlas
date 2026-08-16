# Revenue-Stack Model — Fleet Investors Archetype (Washington DC)

**Date:** 2026-08-16 · **Status:** research-complete draft for Jaideep review — D6′ utilization-stack template applied per `../FLEET-INVESTORS-BRIEF.md`; DC seat pricing **DERIVED** (no canon)
**Companion files:** `CREW-COST-WASHINGTON-DC.md` (loaded crew rate), `SPEED-RULES-WASHINGTON-DC.md` (all route times at posted limits), `../boston/REVENUE-STACK-BOSTON.md` (template), `../boston/CARGO-LAYER-BENCHMARKS.md` (cargo rate anchors)
**Fleet Investors firewall applies:** vessel-fleet financing only; no Navier equity/round content. Corridors and route times from `hub.json` only, at posted speed limits (Washington Channel/upper Potomac/Anacostia 6 mph regimes — primary-verified in SPEED-RULES).

---

## 1 · DC seat-price derivation — DERIVED, shown in full (no canon for DC)

Local premium-substitute benchmarks (all captured 2026-08-16 unless noted):

| Benchmark | Price | Unit | Source | Year | URL | Confidence |
|---|---|---|---|---|---|---|
| Potomac Water Taxi (City Cruises) one-way, Old Town↔Wharf network | from **$21–27** | per one-way ride (booking calendar) | City Experiences DC water taxi | 2026 (live booking page) | https://www.cityexperiences.com/washington-dc/city-cruises/water-taxi/ | sourced (dynamic pricing; basis band) |
| Potomac Water Taxi one-way (press-reported standard fare) | **$22** | per one-way ride | Washington Post | Oct 2022 | https://www.washingtonpost.com/transportation/2022/10/07/water-taxis-dc-region/ | sourced (dated) |
| Water Taxi Season Pass | **$248** | per season (leisure product; capacity not guaranteed, seasonal schedule) | City Experiences | 2026 (live page) | https://www.cityexperiences.com/washington-dc/city-cruises/water-taxi/ | sourced — see honesty note below |
| VRE Woodbridge (Zone 5) → DC (Zone 1) monthly | **$284.10** (single ride $10.25) | per month | VRE FY2027 fare chart, effective 7/1/2026 | 2026 | https://www.vre.org/assets/1/6/FY_2027_Fare_Chart_7.1.2026.pdf | sourced |
| OmniRide Express (I-95 corridor → DC) | **$285.00** monthly ($11.00 one-way) | per month / per trip | OmniRide fares page | 2026 (live page) | https://omniride.com/service/southern-express-commuter-routes/fares-and-transfers/ | sourced |
| Metrorail max fare | **$6.75** peak max ($2.25–6.75 band) | per trip | WMATA cost-to-ride page | 2026 (live page) | https://www.wmata.com/fares/basic.cfm | sourced |
| Downtown DC monthly parking | ~**$250** average; Ronald Reagan Building garage $319–349/mo unreserved | per stall-month | SpotHero DC monthly index; Colonial Parking RRB listing | 2026 (live pages) | https://spothero.com/monthly-parking/washington-dc · https://www.ecolonial.com/location/ronald-reagan-building-international-trade-center-garage/ | sourced (marketplace index) |
| Uber Alexandria → Washington (published route average) | ~**$23** (≈24 min, ~9 mi) | per ride, trailing-month average | Uber route-estimate page | 2026 (live page) | https://www.uber.com/global/en/r/routes/alexandria-va-to-washington-dc-dc/ | sourced |
| Uber premium tier (Black), Alexandria→DC | **unsourced — fail closed** (Uber's route page publishes no Black-tier average) | — | — | — | — | fail closed |

**Derivation (Boston yield logic, DC inputs):**
- *Pass-vs-spot structure:* industry pass discounts run 26–51% off walk-up (MBTA/Seastreak/NYC Ferry/Blade — sourced in `../boston/REVENUE-LEVER-BENCHMARKS.md`).
- *Walk-up water equivalent:* $21–27/leg × 44 commuting legs/mo = **$924–1,188/mo**. A committed AM+PM seat priced at **$750–1,000/mo is a 19–24% discount off the midpoint walk-up equivalent** — inside the industry pass-discount band.
- *Premium-transit multiple:* DC's premium commuter transit anchor is $284–285/mo (VRE Zone 5, OmniRide). **$750–1,000 = 2.6–3.5×** that anchor — at/just below Boston's 3–4× positioning, appropriate because DC's door-to-door substitute is cheaper than Boston's (Uber ~$23 vs ~$55).
- *Door-to-door ceiling:* Uber-equivalent ≈ $23 × 44 = ~$1,012/mo; parking displacement adds ~$250–349/mo of avoided cost for drivers. $750–1,000 sits at or below the rideshare-monthly ceiling before counting parking.
- **DERIVED DC seat band: $750–1,000/seat-month** (within the global program band $650–1,200; below Boston's $950–1,200). Honesty note: City Cruises' $248 season pass is a seasonal leisure product without guaranteed commuter capacity or AM-peak frequency — it is not a committed-commuter-seat comparator, but it must be acknowledged in any DC pricing conversation.

## 2 · Pricing architecture — three layers + two upside lines (D6′)

| Layer | Product | DC pricing logic | DC benchmark anchors |
|---|---|---|---|
| **L1 · Committed bundles** | Monthly commuter seat (AM+PM guaranteed) | **$750–1,000/mo DERIVED** (§1) — pass-discount vs walk-up water taxi, 2.6–3.5× premium transit, ≤ rideshare-monthly | Water taxi $21–27/leg · VRE $284.10/mo · OmniRide $285/mo · Uber ~$23 |
| **L2 · Spot seats** | Per-leg, yield-managed residual commute capacity + shoulder sailings | **$25–40/leg** — floor at incumbent water-taxi walk-up ($21–27), ceiling at a premium over Uber door-to-door (~$23) for a faster, terminal-to-terminal premium ride | Same |
| **L3 · Block products** | Experiences (per-person) + private charters (per-hour), midday/evening/weekend | Experiences **$59–79/pp** inside the live DC operator band ($44 lunch → $106 premier dinner); charters **$450–600/hr** for a 20-pax premium vessel | Odyssey DC lunch from $44–56, brunch from $69, Signature dinner from $87, Premier dinner from $106 (https://www.cityexperiences.com/washington-dc/city-cruises/odyssey-dining-cruises/ · https://www.cityexperiences.com/washington-dc/city-cruises/); DC charter marketplaces list ~$150–650/hr for 12–25-pax vessels (e.g., https://www.getmyboat.com/boat-rental/washington--dc--united-states/ — secondary, marketplace) |
| **U1 · Sponsorship** | Fleet-level naming/branding | **Upside only**, $150K/yr fleet placeholder ÷ 4 vessels — transit precedents per Boston file (Citi Bike, Santander, HealthLine, Barclays). No DC transit naming deal with a disclosed value found (Capital Bikeshare is publicly owned, no title sponsor) — **fail closed as DC-specific anchor**, national precedents only | `../boston/REVENUE-LEVER-BENCHMARKS.md` §4 |
| **U2 · Overnight cargo** | Scheduled night contracts, clean classes only | **Upside only**, ~$350/run × 16 nights — **courier-linehaul rates, not island air-substitute rates** (Casco Bay 2026 published tariff $0.108–0.162/kg ≈ $216–324 per ~2,000-kg run; Dropoff 2026 medical courier $30–160/job; Breakaway rate card). **DC-appropriate clean classes:** medical/lab specimens (hospital–lab network flows), secure batch documents/parcels (DC's legal-government courier market), catering/event logistics (National Harbor–Wharf venue cluster). Seafood-class rejected per Boston finding | `../boston/CARGO-LAYER-BENCHMARKS.md` |

## 3 · The four levers — defensibility grading (DC)

| Lever | Market-proven? | Navier-proven? | Treatment |
|---|---|---|---|
| L1+L2 commute yield | ✅ structure universal; DC-specific: an active 4-node water-taxi network runs today on our exact DC-1 anchors, and water taxis were the promoted commuter alternative in the 2019 Metro shutdown (hub canon: 5,000/day Old Town↔Wharf — not independently re-verified) | Partially (program structure; no DC operations) | **Base case**, conservative fills |
| L3 experiences & charters | ✅ deep DC market at named prices (Odyssey/City Cruises dinner-cruise fleet; monuments-by-water tourism) | ❌ | **Base case at thin utilization** (conservative = 10 sailings/mo vs incumbents' daily-plus cadence) |
| U1 sponsorship | ✅ transit precedents priced (national); DC-specific deal value: none found | ❌ | **Upside only**, never per-vessel headline |
| U2 cargo | ✅ published waterborne tariffs + courier benchmarks (Casco Bay, Dropoff, Breakaway); DC water-freight precedent: none found (**fail closed**) | ❌ | **Upside only**, $5.6K/mo, contract-gated |

## 4 · Worked per-vessel model (N45, Washington DC)

Fixed inputs: $2.5M capex · 20 seats · energy 4.1 kWh/nm @ $0.30/kWh (canon) · Navier network share 10% of gross (canon) · maintenance $82.5K/yr → $6,875/mo (midpoint of unvalidated $65–100K range, same as Boston) · insurance+berth **$7.7K/mo placeholder — DC berthing costs unverified; NPS-concession and private-pier fee structures unknown** · crew **$100/hr 2-crew fully loaded** (DC metro OEWS means × 1.4294 ECEC × ~3%/yr drift to 2026 ≈ $101 — `CREW-COST-WASHINGTON-DC.md`) · 22 weekdays + up to 8 weekend days · commute = 8 legs/day × ~5.5 nm avg (hub launch segments 1.77–5.7 nm) = 968 nm/mo · capacity 8 legs × 20 seats × 22 days = 3,520 seat-legs/mo; residual = 3,520 − committed×2×22.

| | Conservative | Mid | Upside |
|---|---|---|---|
| L1 committed seats × price | 24 × $750 = $18,000 | 32 × $875 = $28,000 | 36 × $1,000 = $36,000 |
| L2 spot fill of residual commute capacity × fare | 2,464 × 10% × $25 = $6,160 | 2,112 × 20% × $30 = $12,672 | 1,936 × 30% × $40 = $23,232 |
| L3 experiences (sailings/mo × pax × price) | 10 × 10 × $59 = $5,900 | 28 × 13 × $69 = $25,116 | 40 × 15 × $79 = $47,400 |
| L3 charters (per mo × hrs × rate) | 3 × 2.0 × $450 = $2,700 | 6 × 2.25 × $500 = $6,750 | 10 × 2.5 × $600 = $15,000 |
| Sponsorship (fleet-level ÷ 4 vessels) | $0 | $0 | $3,125 |
| Overnight cargo (16 runs/mo × $350 contract) | $0 | $0 | $5,600 |
| **Gross revenue /mo** | **$32,760** | **$72,538** | **$130,357** |
| Opex /mo (energy · crew · maint · ins/berth) | $31,883 ($1,358 · $15,950 · $6,875 · $7,700) | $36,663 ($1,638 · $20,450 · $6,875 · $7,700) | $40,642 ($1,867 · $24,200 · $6,875 · $7,700) |
| **Net to investor /mo** (gross × 0.90 − opex) | **−$2,399** | **+$28,621** | **+$76,679** |
| **Annual** | −$28.8K | **+$343.5K** | +$920.2K |
| **Payback on $2.5M** | never (cash-negative) | **~7.3 yr** | **~2.7 yr** |
| L1-only commuter model (same opex basis, mid seats) | — | −$3,766/mo · never | — |

Opex build: crew hours = 132 commute (6.0 hr/day × 22) + 2.0 hr/experience sailing + (charter hrs + 0.5) per charter → 159.5 / 204.5 / 242 hrs × $100. Energy nm = 968 commute + 10 nm/experience + ~12–15 nm/charter → 1,104 / 1,332 / 1,518 nm × $1.23/nm.

**Honest reads:**
- **DC's conservative case is slightly cash-negative** (−$2.4K/mo) where Boston's was +$10K: the DERIVED seat band sits ~20% below Boston's and loaded crew ~18% above. The stack still rescues it from the L1-only case (−$3.8K/mo at mid fills), but there is no pretending: punitive fills do not pencil in DC.
- **Mid (~7.3 yr) is honest but not yet financeable** (Boston mid: 4.3 yr). The gap is structural — cheaper substitutes (Uber ~$23, VRE $284/mo) cap seat pricing, and DC crew costs more. Paths to a financeable mid, all labeled: (a) L3 execution nearer incumbent cadence (DC's tourism water market is deep — monuments by water); (b) multi-corridor utilization at Phase 2/3; (c) **speed-rule relief upside** — DC is the one market whose regulation (19 DCMR § 1027.3, Mayoral hydrofoil demonstration permits) explicitly anticipates the relief mechanism; faster cycles raise legs/day at constant crew hours. Never blend (c) into base or mid.
- **Upside (~2.7 yr) converges** toward canon partner-corridor economics (2.49 yr) and Boston's upside (2.1 yr) — same physics: the whole day utilized.
- Demand pools: from hub.json employer data only, **indicative** — Navy Yard ~17,000 federal personnel + US DOT HQ (Teague), Gaylord 1,001–5,000 + MGM 3,200+ (National Harbor), Amazon HQ2 8,000+ today/14,000 planned + Boeing HQ (via Daingerfield shuttle), USPTO Carlyle (Old Town), Wharf professional cluster. Launch trigger unchanged: 60–80 committed seats/corridor. No invented demand; fills are scenario knobs, not forecasts.

## 5 · Assumption register

| Assumption | Value | Basis | Confidence |
|---|---|---|---|
| L1 seat price $750–1,000 | DERIVED | §1 derivation: pass-discount vs walk-up water taxi, 2.6–3.5× VRE/OmniRide monthly, ≤ Uber-monthly ceiling | Derived (labeled; needs Jaideep sign-off before any page shows a DC-specific band) |
| Committed-seat fills 24/32/36 of 40 max | scenario | trigger 60–80 seats/corridor ≈ 1.5–2 vessel-loads; same grammar as Boston | Derived |
| Spot fill 10/20/30% × $25/30/40 | scenario | no Navier precedent; incumbent water taxi proves paid walk-up demand on these exact corridors | Placeholder (price floor sourced) |
| Experience sailings 10/28/40 × $59/69/79 | benchmark-bounded | DC operator band $44–106/pp (Odyssey/City Cruises live pages); conservative ≈ ⅓ of one daily sailing | Benchmark-bounded |
| Charters 3/6/10 per mo × $450–600/hr | benchmark-bounded | DC marketplace listings ~$150–650/hr for 12–25 pax (secondary); premium electric-foiling positioning at the top of band | Secondary-sourced |
| Sponsorship $150K/yr fleet | placeholder | national transit precedents only; no DC deal value found | Weak — upside only |
| Cargo $350/run × 16 nights | benchmark-anchored | Casco Bay 2026 tariff $216–324/2,000-kg run + medical-courier premium headroom (Dropoff 2026); clean classes: medical/lab, secure documents, catering/event | Published-tariff-anchored, unproven by Navier |
| Crew $100/hr × activity hours | benchmark-validated | DC metro OEWS means × 1.4294 × drift ≈ $101 (`CREW-COST-WASHINGTON-DC.md`); thin local sample flagged (200/80 employed) | Validated at rate level; shift structure to ops walkthrough |
| Insurance+berth $7.7K/mo | placeholder | carried from Boston; DC berth/landing fees (NPS concession, private piers) unverified | Placeholder — priority gap |
| Commute 8 legs/day × 5.5 nm avg | derived from hub | hub launch segments (Old Town↔Wharf 5.7, Wharf↔Georgetown 2.97, NH↔Old Town 1.77, Old Town↔Teague 5.33), all at posted limits | Derived |
| Weekend operating days 4/8/8 | scenario | experiences market weekend-heavy | Placeholder |

---
*All benchmark prices captured from live pages 2026-08-16 unless dated otherwise; every number is sourced, DERIVED (labeled), or canon (labeled). Cargo and sponsorship fail closed out of base. Route geometry and times from hub.json only, at posted speed limits per SPEED-RULES-WASHINGTON-DC.md. Internal audit language only — never renders.*
