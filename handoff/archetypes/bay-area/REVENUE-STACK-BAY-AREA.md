# Revenue-Stack Model — Fleet Investors Archetype (Bay Area)

**Date:** 2026-08-15 · **Status:** DRAFT for Jaideep review — Boston D6′ utilization-stack template applied to the Bay Area (`../boston/REVENUE-STACK-BOSTON.md` is the structural exemplar)
**Companion files:** `CREW-COST-BAY-AREA.md` (loaded crew $/hr, sourced) · `AUTHORITY-MAP-BAY-AREA.md` · `SPEED-RULES-BAY-AREA.md` · corridors/geometry from `hub.json` only
**Fleet Investors firewall applies:** vessel-fleet financing only; no Navier equity/round content.

---

## 1 · Frame

Same physics as Boston: one N45, one 16-hr service day, four demand layers — L1 committed seat bundles + L2 spot seats on residual commute capacity (base), L3 experiences/charters (base at thin utilization), U1 sponsorship + U2 overnight cargo (upside-only). The commute spine is hub.json's BA-1 Peninsula Trunk Phase-1 core: **Ferry Building ↔ Oyster Point via Mission Bay and Brisbane, 9.40 nm one-way** (hub.json segments 1.53 + 7.39 + 0.48 nm; 23 min water time at posted limits + 2 intermediate stops). Demand context is indicative only: hub.json catchment anchors are Oyster Point/SSF biotech, Mission Bay/UCSF, and the Financial District; hub.json carries **no employer-headcount rows** for this city, so no seat-demand pool is quantified here (fail closed).

## 2 · Local benchmark anchors (all sourced, retrieved 2026-08-15)

| Layer | Bay Area benchmark | Price | Source |
|---|---|---|---|
| L1 seat bundle | **Canon (confirmed): $800–1,200/seat-month** | canon | program canon; hub.json `locked_numbers.seat_price_band_usd_month` [800, 1200] |
| L1/L2 public-ferry floor | SF Bay Ferry regular fares effective July 1, 2026: Oakland/Alameda $5.10 · Richmond $5.20 · South San Francisco $7.60 · Vallejo $10.00 | sourced | https://sanfranciscobayferry.com/fare-change/ |
| L1/L2 public-ferry floor | Golden Gate Ferry fares effective July 1, 2026: adult paper $14.00 (Larkspur/Sausalito/Tiburon); Clipper $8.50–9.50 | sourced | https://www.goldengate.org/ggt--ggf-regional-fares-increase-july-1-2026/ |
| L2 door-to-door substitute | Uber South San Francisco → Oakland estimated **$60** (~37 min) | sourced | https://www.uber.com/global/en/r/routes/south-san-francisco-ca-to-oakland-ca/ |
| L1 substitute | Downtown SF monthly parking ≈ **$340/mo** average (ranges $65–650) | sourced | https://spothero.com/city/monthly/san-francisco-parking · https://www.spotangels.com/san-francisco/downtown-san-francisco-monthly-parking |
| Private commuter precedent | Tideline Berkeley–SF private commuter ferry: $8/leg, $290/mo pass (2017 — dated, floor only) | sourced (dated) | https://www.berkeleyside.org/2017/05/25/new-berkeley-ferry-offers-alternative-crowded-commutes |
| Water taxi | SF Water Taxi (Port-sanctioned): $10/ride north of Bay Bridge, $15 all-day | sourced | https://www.sfwatertaxi.net/book-now/ |
| L3 experiences | Red & White Golden Gate Bay Cruise adult **$39**; sunset tier **$75** | sourced | https://www.redandwhite.com/golden-gate-bay-cruise · https://www.redandwhite.com/ |
| L3 experiences | Blue & Gold Fleet tours from **$31** | sourced | https://www.blueandgoldfleet.com/ |
| L3 experiences | City Cruises SF Premier Dinner Cruise **$134**; Signature Dinner (Viator) **$58**; brunch $122 | sourced | https://www.cityexperiences.com/san-francisco/city-cruises/ · https://www.viator.com/tours/San-Francisco/San-Francisco-Supper-Club-Cruise/d651-2540SFOSUPPER |
| L3 charters | SF Bay charters: sailing/mid-size motor $150–450/hr; larger motor yachts "start at $500/hr and can exceed $2,500/hr"; party boats commonly $500+/hr | sourced | https://www.sailo.com/boat-rentals/CA/San_Francisco · https://www.getmyboat.com/boat-rental/San-Francisco--CA--United-States/ · https://www.boatsetter.com/yacht-rentals/san-francisco--ca--united-states |

**Derived bands (labeled DERIVED):** L2 spot **$35–55/leg** — positioned between the premium public-ferry ceiling (~$10–14) and the door-to-door car substitute (~$60 Uber + parking displacement); a silent foiling 25–30-min Peninsula hop at roughly the Uber price minus friction. L3 experiences **$49–79/pp** — above the $31–39 mass-market bay-cruise floor, below the $122–134 dinner tier, matching Boston's positioning logic. L3 charters **$600–700/hr** — inside the sourced "$500+/hr larger vessel" band; a 20-pax electric foiling vessel is a premium entrant.

## 3 · The four levers — defensibility grading

| Lever | Market-proven? | Navier-proven? | Treatment |
|---|---|---|---|
| L1+L2 commute yield | ✅ WETA/GGF fare structures + Tideline private-commuter precedent + canon seat band confirmed | ❌ no Bay Area operations | **Base case**, conservative fills |
| L3 experiences & charters | ✅ deep SF market at named prices (largest experience market of the seven cities) | ❌ | **Base case at thin utilization** (conservative ≈ ⅓ of one daily incumbent sailing) |
| U1 Sponsorship | ✅ transit precedents per Boston benchmarks file (Citi Bike ~$7–8M/yr; HealthLine $250K/yr line-naming) | ❌ | **Upside only**, $150K/yr fleet placeholder ÷ 4 vessels |
| U2 Overnight cargo | ✅ courier-linehaul rates per Boston cargo research (`../boston/CARGO-LAYER-BENCHMARKS.md` — Casco Bay published tariff anchor, Dropoff medical-courier rates); Bay Area first classes: **medical/lab specimens (UCSF Mission Bay ↔ Oyster Point/SSF biotech corridor is purpose-built for this), batch parcels, catering/event** | ❌ | **Upside only**, ~$350/run × 16 nights/mo — Boston-anchored, **not separately re-benchmarked for SF this pass (labeled)** |

## 4 · Worked per-vessel model (N45, Bay Area)

Fixed inputs: $2.5M capex · 20 seats · energy 4.1 kWh/nm @ $0.30/kWh (canon) · Navier network share 10% of gross (canon) · maintenance $82.5K/yr → $6,875/mo (midpoint of the unvalidated $65–100K range, same as Boston) · insurance+berth $7,700/mo (placeholder carried from Boston; Bay Area berth rates not separately validated — flagged) · **crew $155/hr 2-person fully loaded** (sourced/derived: BLS SF metro mean loaded $140.88 (May 2023) + ~3%/yr drift to 2026 ≈ $154 — see `CREW-COST-BAY-AREA.md`) · 22 weekdays + up to 8 weekend days · commute = 8 legs/day × 9.40 nm (hub.json BA-1 Phase-1 spine) · commute capacity 3,520 seat-legs/mo; residual = capacity − L1 usage (seats × 2 legs × 22 days).

| | Conservative | Mid | Upside |
|---|---|---|---|
| L1 committed seats × price | 24 × $800 = $19,200 | 32 × $1,000 = $32,000 | 36 × $1,200 = $43,200 |
| L2 spot fill of residual commute capacity × fare | 10% × 2,464 × $35 = $8,624 | 20% × 2,112 × $45 = $19,008 | 30% × 1,936 × $55 = $31,944 |
| L3 experiences (sailings/mo × pax × price) | 10 × 10 × $49 = $4,900 | 28 × 13 × $65 = $23,660 | 40 × 15 × $79 = $47,400 |
| L3 charters (per mo × hrs × rate) | 3 × 2.0 × $600 = $3,600 | 6 × 2.25 × $650 = $8,775 | 10 × 2.5 × $700 = $17,500 |
| U1 Sponsorship (fleet-level $150K/yr ÷ 4 vessels) | $0 | $0 | $3,125 |
| U2 Overnight cargo (16 runs/mo × $350) | $0 | $0 | $5,600 |
| **Gross revenue /mo** | **$36,324** | **$83,443** | **$148,769** |
| Opex /mo (energy · crew · maint · ins/berth) | $41,468 | $48,724 | $54,861 |
| **Net to investor /mo** (gross × 0.90 − opex) | **−$8,776** | **+$26,375** | **+$79,031** |
| **Annual** | −$105K | +$316K | +$948K |
| **Payback on $2.5M** | never (cash-negative) | **~7.9 yr** | **~2.6 yr** |

Opex detail (sums exactly; assumptions stated):
- **Energy** = $1.23/nm (4.1 kWh/nm × $0.30) × [commute 1,654 nm + experiences 8 nm/sailing + charters 5 nm/booked-hr] = $2,170 / $2,394 / $2,582.
- **Crew** = $155/hr × activity hours [commute ops 6 hr/day × 22 = 132 h; experiences 2 h/sailing; charters booked hrs × 1.25 positioning factor] = 159.5 h / 204.9 h / 243.3 h = $24,723 / $31,756 / $37,704.
- **Maintenance** $6,875 + **insurance/berth** $7,700 in all scenarios.

## 5 · Honest reads

- **The Bay Area's crew premium is the story.** SF metro loaded crew ($155/hr modeled) runs ~1.8× Boston ($85/hr). That single line flips the conservative case **cash-negative** (−$8.8K/mo) where Boston's was +$10K, and pushes the mid payback to **~7.9 yr** vs Boston's ~4.3 — with the *same* fill assumptions and a *richer* experience market. Crew-rate sensitivity: at the LOW (2026-drifted median) $130/hr, mid net rises to ~$31.5K/mo → **~6.6-yr payback**. Nothing here is inflated to fix this; it is the honest output of sourced local wages.
- **What actually closes the gap (levers, not wishes):** (1) the confirmed canon L1 band tops at $1,200 — mid holds it at $1,000; every $100/seat-month × 32 seats is +$3.2K/mo (≈ −1 yr of payback at mid); (2) the Bay Area experience market's price ceiling ($122–134 dinner tier) leaves the modeled $65 mid price deliberately low; (3) N30 (8-pax, lower crew intensity if single-crew-certifiable — **unverified, ops question**) may fit shoulder/experience duty better than N45 in this market. All three are Phase-2 walkthrough items, not model overrides.
- **Upside (~2.6 yr) again converges with canon partner-corridor economics** (Boston stack upside ~2.1 yr; Boston↔Hingham canon 2.49 yr) — a premium vessel utilized across the whole day pays back in ~2.5–3 yr; the Bay Area simply demands more of the day be sold to get there.
- Conservative remains deliberately punitive: 10% spot fill, 10 experience sailings/mo in the market where Red & White and Blue & Gold run multiple daily sailings year-round.
- **No demand invented:** L1 fills (24/32/36) are scenario positions consistent with the 60–80 committed-seat corridor trigger (hub.json `locked_numbers`), not employer commitments. hub.json has no employer headcount data for this city; the Fleet Investors demand-pool table must wait for the city tracker (fail closed).

## 6 · Assumption register

| Assumption | Value | Basis | Confidence |
|---|---|---|---|
| L1 seat band $800–1,200; scenario prices 800/1,000/1,200 | canon | confirmed city canon + hub.json locked_numbers | Canon |
| Committed-seat fills 24/32/36 of 40 max | scenario | consistent with 60–80 seat corridor trigger ≈ 1.5–2 vessel-loads | Derived |
| Spot fare $35/45/55 | DERIVED | bounded by public-ferry premium fares ($7.60–14, July 2026) and Uber door-to-door (~$60) | Derived, sourced bounds |
| Spot fill 10/20/30% of residual | scenario | no Navier precedent; labeled unproven | Placeholder |
| Commute spine 8 legs/day × 9.40 nm | hub.json | BA-1 Phase-1 segments (FB–Mission Bay–Brisbane–Oyster Point), posted limits | Canon geometry |
| Experience sailings 10/28/40 per month; price $49/65/79 | scenario / DERIVED | incumbents run daily-to-multiple-daily; price between $31–39 mass floor and $122–134 dinner tier | Benchmark-bounded |
| Charter $600–700/hr, 2–2.5 hr, 3/6/10 per month | benchmark | Sailo/Getmyboat/Boatsetter SF bands ($500+/hr larger vessels) | Sourced band |
| Sponsorship $150K/yr fleet, upside only | placeholder | Boston benchmarks file precedents | Weak — upside only |
| Cargo $350/run × 16 nights/mo, upside only | Boston-anchored | courier-linehaul logic + Casco Bay published-tariff anchor; **not re-benchmarked for SF** | Anchored, unproven; label carried |
| Crew $155/hr × activity hours | sourced/derived | BLS SF metro means × 1.4294 ECEC + 3%/yr drift (`CREW-COST-BAY-AREA.md`) | Validated at rate level; shift structure to ops walkthrough |
| Energy $0.30/kWh | canon | program canon; **note PG&E commercial rates likely higher — flag for Phase-2 validation, canon held per template** | Canon (flagged) |
| Maintenance $82.5K/yr; insurance+berth $7.7K/mo | placeholder | Boston values carried; Bay Area berth market not validated | Placeholder (flagged) |
| Weekend operating days 4/8/8 | scenario | experiences market weekend-heavy | Placeholder |

---
*Every number above is sourced, derived (labeled), or canon (labeled). Cargo and sponsorship fail closed out of the base case. No employer-anchoring/launch-trigger framing renders publicly; internal audit language only.*
