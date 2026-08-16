# REVENUE-STACK-ABU-DHABI — one N45, tourism-weighted utilization stack (internal audit file — never renders)

**As of:** 2026-08-16 · Structure per boston/REVENUE-STACK-BOSTON.md + INTERNATIONAL-ADDENDUM (12-month year, summer-heat midday shape). One N45: $2.5M capex, 20 seats (canon). Peg 3.6725 AED/USD. All scenario lines sum EXACTLY to gross (script-verified 2026-08-16).

## 1 · Corridors (GEOMETRY-ABU-DHABI.json `curation.bindable_clean_routes` ONLY — bound by route_id)

| Role | route_id | Corridor | nm |
|---|---|---|---|
| Commute spine | **rn-60483e41e97f** | Emirates Palace Marina ↔ Saadiyat Marina & Ferry Terminal | 8.9 |
| Commute alt | rn-f14ad5f39fcc | Rabdan Marina ↔ Saadiyat Marina & Ferry Terminal | 9.5 |
| Cross-network | rn-b58e6dc0d928 | Yas Marina ↔ Saadiyat Marina & Ferry Terminal | 11.4 |
| Cross-network | rn-94858c712852 | Yas Marina ↔ Rabdan Marina | 7.8 |
| Experience loop A | rn-544c3f7471c1 / rn-7c69dd29a122 | Emirates Palace Marina ↔ Lulu Island / Lulu Island Jetty | 3.3 / 3.1 |
| Experience loop B | rn-b56442e5125a | Saadiyat Marina & Ferry Terminal ↔ Hidd Al Saadiyat Marina | 2.7 |
| Resort transfer | rn-cedce441d25a | Zaya Nurai Island Jetty ↔ Saadiyat Marina & Ferry Terminal | 5.0 |
| Marquee showcase | rn-b89451fb7867 | Emirates Palace Marina ↔ Yas Marina | 18.0 |
| (network completion) | rn-881a8cdb6576 | Emirates Palace Marina ↔ Rabdan Marina | 11.6 |

Landing verification: Saadiyat Marina & Ferry Terminal and Rabdan Marina **opened 2024 (primary — admaritime Dalma release)**; Yas Marina and Emirates Palace Marina are operating marinas (Abu Dhabi Maritime facilities/tariff schedule); Zaya Nurai Island Jetty exists but resort is **temporarily closed for renovation (2026) — status-flag**; Lulu Island has **no verified public facility — status-flag, experience-anchor only**. Candidate labels from `ad_bps_misfiled_in_rak_set_labels_only` verified as real landings by label — **Al Qana Marina** and **Al Bandar** (both scheduled water-taxi stops, u.ae primary), **ADNEC Marina**, **Hudayriat Marina**, **Irshad Ferry Terminal** (listed Abu Dhabi Maritime facilities) — cite by LABEL only, never bind their route_ids (contaminated RAK file; Grok locale cleanup #119 pending).

## 2 · Spine timing at controlling limits (SPEED-RULES-ABU-DHABI.md basis — PRIMARY zoned limits)

Spine rn-60483e41e97f, 8.9 nm, Emirates Palace ↔ Saadiyat:

| Segment | nm | Limit basis | Time |
|---|---|---|---|
| Marina basins/no-wake (both ends) | 0.4 | 5 kn (primary, Rule 1) | 4.8 min |
| Marked channel (Zayed Port approach) | 2.0 | 20 kn (primary, Rule 3) | 6.0 min |
| Open water | 6.5 | 25 kn N45 service speed (canon) — inside 50 kn limit | 15.6 min |
| Dock dwell (2 calls × 2 min) | — | assumption | 4.0 min |
| **Total** | 8.9 | | **≈30 min** (≈34 min after sunset — 20 kn night cap, primary Rule 5) |

Drive substitute: 10 km averages 21 min 40 s citywide, ~27 min in rush (TomTom 2025); Yas/Al Raha↔CBD 30–45+ min peak with AED 4 Darb toll. The water leg is competitive-to-faster **and productive time**.

## 3 · Seat pricing — DERIVED (no canon for this market; flag for Jaideep confirmation)

Substitute anchors (TOURISM-DEMAND §4): metered taxi Yas/Al Raha↔CBD ≈ AED 60 (~$16.2, primary tariff math) with observed AED 60–85; Saadiyat↔CBD ≈ AED 32; Darb AED 4/peak crossing; subsidized public water-taxi floor AED 10 (leisure schedule, not a commute product); TomTom congestion 29.6%, 57 hrs/yr lost.
- **Spot seat (L2): $20 / $25 / $30** (Con/Mid/Up) — at/above door-to-door taxi on the long corridors, far above the subsidized leisure floor; premium positioned on time + reliability + segment (visitor/corporate), honestly noted as a premium to AD's cheap street-taxi meter.
- **L1 committed monthly seat = 44 legs × spot × ≈0.59 (bundle discount ≈41%, program-standard pass structure) → $519 / $649 / $779, rounded $500 / $650 / $775.** DERIVED band **$500–775/mo** — below Dubai's derived $650–900, consistent with cheaper road substitutes; ~70–108% of the AED 2,640/mo road-commute anchor. **Flag for Jaideep.**

## 4 · Experience & charter pricing — DERIVED from sourced benchmarks (tourism-weighted headline layer)

- Shared foiling experience (60–75 min: Lulu loop, Saadiyat/Hidd, mangrove-fringe, Yas showcase): **$40 / $50 / $60 pp** — inside the sourced $40–79 sightseeing band (Klook $40.59 / GetYourGuide ~$51 / Captain Tony's $55.55 / premium $78.70); Nurai bundles water transfer at $131–150 pp (ceiling context).
- Private charter (marquee Emirates Palace↔Yas + event-day F1/Etihad Arena positioning): **$450 / $525 / $600 per hr** — DERIVED; local published hourly market above small-craft tier is thin (small-craft floor ~AED 600–700/hr ≈ $163–190), so band is anchored to the Dubai adjacent-market charter band ($500–650, dubai/REVENUE-STACK-DUBAI.md) with a conservative haircut. Weakest-anchored price in this file — labeled.

## 5 · Opex basis

| Line | Value | Basis |
|---|---|---|
| Crew | **$30/hr** × activity hrs | CREW-COST-ABU-DHABI.md MID $27.97 rounded up (LOW $20.87) |
| Energy | 4.1 kWh/nm (N45, canon) × **$0.0572/kWh** | ADDC business tariff, Commercial: **20 fils/kWh** (primary: https://www.addc.ae/en-US/business/Pages/RatesAndTariffs2025.aspx, accessed 2026-08-16) + 5% VAT = 21 fils ÷ 3.6725. Flat tariff, no slab. Far cheaper than $0.30 canon ⇒ sourced tariff used per addendum. Sensitivity: at $0.30 canon energy rises ~5.2×; nets stay positive in all scenarios |
| Berthing | **$911/mo** | PRIMARY: Abu Dhabi Maritime Public Marine Facilities tariff — Rabdan Marina commercial wet berth **AED 850/ft/yr** × 45 ft × 1.05 VAT = AED 40,163/yr (https://www.admaritime.ae/wp-content/uploads/2025/07/Tariff__Services_Rates_for_Public_Marine_Facilities.pdf). Cross-check: Al Saadiyat AED 750/ft/yr → $804/mo. Utilities metered separately (not included) |
| Insurance | $4,167/mo ($50K/yr ≈ 2% hull + P&I) | placeholder assumption, same treatment as Boston/Dubai; UAE-licensed insurer |
| Maintenance | $6,875/mo ($82.5K/yr) | canon $65K/yr N30-class scaled to N45 (Boston precedent midpoint) |
| Network share | 10% of gross | canon |
| Activity hours | 198 / 245 / 300 hrs/mo | derived: commute 132 (22 days × 6 hr) + experiences/charters + 15% positioning-standby (same structure as Dubai) |
| Energy nm | 1,965 / 2,154 / 2,757 nm/mo | commute 8 legs × 8.9 nm × 22 = 1,566 + experience (≈7 nm/sailing) + charter (≈10 nm/hr) + cargo runs (upside) + 10% repositioning |

Fixed (berth + insurance + maintenance) = **$11,953/mo**.

**Season shape (stated assumption per addendum):** 12-month year; Jun–Sep summer heat suppresses midday demand and shifts L2/L3 volume to early-morning and evening blocks (evening legs timed at the 20 kn night cap). Scenario quantities are annual monthly averages across this shape; winter (Oct–Apr, F1/event season) runs above average, summer below. No winter discount applied.

## 6 · Scenarios (monthly, USD) — lines sum EXACTLY to gross (script-verified)

Commute capacity: 8 legs/day × 20 seats × 22 weekdays = 3,520 leg-seats/mo; each committed seat consumes 44.

### Conservative
| Layer | Quantity × price | $/mo |
|---|---|---|
| L1 committed seat bundles | 24 seats × $500 | 12,000 |
| L2 spot seats | 2,464 residual leg-seats × 10% fill = 246 × $20 | 4,920 |
| L3 shared experiences | 20 sailings × 12 pax × $40 | 9,600 |
| L3 private charters | 8 hrs × $450 | 3,600 |
| U1 sponsorship / U2 cargo | — (upside only) | 0 |
| **Gross** | | **30,120** |
| Network share (10%) | | −3,012 |
| Crew 198 hrs × $30 | | −5,940 |
| Energy 1,965 nm × 4.1 × $0.0572 | | −461 |
| Berthing + insurance + maintenance | 911 + 4,167 + 6,875 | −11,953 |
| **Net** | | **8,754** |
| **Simple payback on $2.5M** | 2,500,000 ÷ (8,754 × 12) | **23.8 yr** |

*(L1 line: 24 × $500 = $12,000 — the struck figure above corrects a transposition; 12,000 is the value summed.)*

### Mid
| Layer | Quantity × price | $/mo |
|---|---|---|
| L1 committed seat bundles | 32 seats × $650 | 20,800 |
| L2 spot seats | 2,112 residual leg-seats × 20% fill = 422 × $25 | 10,550 |
| L3 shared experiences | 36 sailings × 14 pax × $50 | 25,200 |
| L3 private charters | 14 hrs × $525 | 7,350 |
| U1 / U2 | — (upside only) | 0 |
| **Gross** | | **63,900** |
| Network share (10%) | | −6,390 |
| Crew 245 hrs × $30 | | −7,350 |
| Energy 2,154 nm × 4.1 × $0.0572 | | −505 |
| Berthing + insurance + maintenance | | −11,953 |
| **Net** | | **37,702** |
| **Simple payback** | 2,500,000 ÷ (37,702 × 12) | **5.5 yr** |

### Upside
| Layer | Quantity × price | $/mo |
|---|---|---|
| L1 committed seat bundles | 36 seats × $775 | 27,900 |
| L2 spot seats | 1,936 residual leg-seats × 30% fill = 581 × $30 | 17,430 |
| L3 shared experiences | 56 sailings × 15 pax × $60 | 50,400 |
| L3 private charters | 26 hrs × $600 | 15,600 |
| U1 sponsorship (upside only) | $150K/yr fleet program ÷ 4 vessels ÷ 12 (placeholder canon per Boston) | 3,125 |
| U2 cargo (upside only) | 16 runs × $300 — clean classes: medical/lab specimens, premium parcels, island-resort resupply (Saadiyat/Yas/Nurai); courier-linehaul rate logic per Boston; **no AD waterborne freight tariff found ⇒ upside-only** | 4,800 |
| **Gross** | | **119,255** |
| Network share (10%) | | −11,925.50 |
| Crew 300 hrs × $30 | | −9,000 |
| Energy 2,757 nm × 4.1 × $0.0572 | | −646 |
| Berthing + insurance + maintenance | | −11,953 |
| **Net** | | **85,730** |
| **Simple payback** | 2,500,000 ÷ (85,730 × 12) | **2.4 yr** |

## 7 · Honest reads

- **Mid (5.5 yr) is the financeable case**; it asks for 36 experience sailings/mo in a market where sourced operators run daily-to-multiple-daily schedules at Yas alone, against a 5.9M-hotel-guest, 81%-occupancy demand base. Conservative (23.8 yr) is deliberately punitive and cash-positive with zero anchor.
- **Upside 2.4 yr matches the canon partner-corridor benchmark (2.49 yr)** — the credibility anchor, not a coincidence; same physics as Boston/Dubai.
- Structural cost advantage vs Boston: crew $30 vs $85/hr, energy $0.0572 vs $0.30/kWh, berth $911/mo primary-sourced — fixed lines (insurance placeholder, canon maintenance) now dominate opex; both are flagged for operator quotes.
- Revenue mix is tourism-weighted per addendum: L3 is the largest layer in Mid and Upside (39–55% of gross). The commute spine remains the schedule backbone and the authority-relevant product.
- Weakest links, in order: charter $/hr (DERIVED, thin local anchor) · L1 band (DERIVED, flag for Jaideep) · Nurai transfer demand while resort renovation persists (status-flagged) · insurance placeholder.

## 8 · Assumption register (deltas vs Boston template)

| Assumption | Value | Basis | Confidence |
|---|---|---|---|
| Committed seats 24/32/36 | scenario | trigger logic per Boston (60–80 seats/corridor ≈ 1.5–2 vessel-loads) | Derived |
| Spot fill 10/20/30% | scenario | no Navier precedent; labeled unproven | Placeholder |
| Experience sailings 20/36/56, 12–15 pax | scenario | tourism-weighted; ≤ one daily sailing even in Upside vs incumbents' multiple-daily; 26.6M visitors 2025 | Benchmark-bounded |
| Experience price $40–60 pp | benchmark | sourced $40–79 AD sightseeing band | Sourced |
| Charter $450–600/hr | DERIVED | Dubai adjacent-market band, conservative haircut; thin local publication | Weak — labeled |
| Seat band $500–775/mo | DERIVED | 44 legs × spot × 0.59 pass structure; road-substitute anchored | Derived — flag for Jaideep |
| Energy $0.0572/kWh | sourced | ADDC commercial 20 fils + VAT, primary | Sourced |
| Berth $911/mo | sourced | Abu Dhabi Maritime published tariff, Rabdan 45-ft commercial wet berth | Sourced (primary) |
| Crew $30/hr | benchmark-anchored | UAE-ADAPTED MID $27.97 + buffer | Sourced-with-assumed-burden |
| Cargo $300/run × 16 (upside) | placeholder | courier-linehaul logic; no AD waterborne tariff found | Weak — upside only |
| Summer midday dip shape | qualitative | addendum-mandated; DCT seasonality | Stated assumption |
