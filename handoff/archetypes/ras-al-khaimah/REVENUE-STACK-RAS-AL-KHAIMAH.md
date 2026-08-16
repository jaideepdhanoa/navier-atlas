# REVENUE-STACK-RAS-AL-KHAIMAH — one N45, tourism-weighted utilization stack (internal audit file — never renders)

**As of:** 2026-08-16 · Structure per boston/REVENUE-STACK-BOSTON.md + INTERNATIONAL-ADDENDUM (12-month year, summer-heat midday shape) · grammar per abu-dhabi/REVENUE-STACK-ABU-DHABI.md. One N45: $2.5M capex, 20 seats (canon), 16-hr day. Peg 3.6725 AED/USD. All scenario lines sum EXACTLY to gross (script-verified 2026-08-16, /tmp/rak_verify.py — sealed RAK geometry unusable, so all corridor math is coordinate-derived; script rerun required on any input change). **Re-tiered 2026-08-16: §9 (Wynn-open planning basis) is the current basis for all renderables; §6–§7 preserved as derivation history.**

## 1 · Corridors (journey spine — **NO route_ids**; sealed RAK set contaminated, fail-closed)

Distances are **DERIVED-approximate**: haversine between OSM-geocoded real coordinates × explicit over-water routing factor, **rounded up** for time/energy math. Anchor points: Al Marjan resort cluster = DoubleTree Marjan (25.6693, 55.7442); Al Hamra Marina/RYC (25.6950, 55.7804); Mina Al Arab/Hayat (25.7222, 55.8390); Corniche = Manar Mall abra station (25.7850, 55.9657); Jazirat Al Hamra centroid (25.6841, 55.8231).

| Role | Corridor | Straight | Factor | **Used (nm)** |
|---|---|---|---|---|
| Resort shuttle | Al Marjan Island ↔ Al Hamra Marina (RYC) | 2.5 | ×1.5 (breakwaters/lagoon) | **4.0** |
| Commute/city line | Mina Al Arab ↔ Al Qawasim Corniche | 7.8 | ×1.25 | **10.0** |
| Full spine / showcase | Al Marjan Island ↔ Al Qawasim Corniche | 13.9 | ×1.2 | **17.0** |
| Heritage line | RAK Creek/Old Town ↔ Jazirat Al Hamra | 9.8 | ×1.3 (creek exit) | **13.0** |
| (network context) | Al Hamra Marina ↔ Mina Al Arab | 3.6 | ×1.25 | 4.5 |

**Landing verification (every rendered stop must be a real landing):**
- **Al Hamra Marina / Royal Yacht Club of RAK — VERIFIED operating** (220+ wet berths, vessels to 200 ft, published rates): https://alhamrawaterfront.alhamra.ae/royal-yacht-club-of-ras-al-khaimah/berthing/
- **Al Qawasim Corniche marine stations (Corniche 1, Corniche 2, Hilton Garden Inn) — VERIFIED operating** RAKTA abra stations: https://www.rakta.gov.ae/marine-transport-services/
- **Mina Al Arab / Hayat Island marina — developer-published**, community partially delivered (Anantara operating): https://hayatislandrak.com/ — **status-flag: developer-published, not independently verified as operating marina**
- **Al Marjan Island — NO public marine facility verified today.** RYC operates anchorage buoys at Al Marjan (operator-published, Instagram); resort beach jetties unverified; **Wynn marina published, opening 2027** (RAKTDA primary) — render Al Marjan stop only with **status flag (planned/interim landing via RYC-coordinated buoy/jetty)**
- **Jazirat Al Hamra waterfront — NO verified facility**; heritage-anchor only, status-flag.

## 2 · Spine timing at conservative planning basis (SPEED-RULES-RAS-AL-KHAIMAH.md — **no numeric RAK limits published; every time conservative-basis flagged**)

Spine Al Marjan ↔ Corniche, 17.0 nm: | 0.5 nm collars @5 kn = 6.0 min | 2.5 nm lagoon/creek-mouth @12 kn = 12.5 min | 14.0 nm open coast @25 kn (N45 canon) = 33.6 min | dwell 2×2 min | **≈57 min** (≈65 min after sunset @20 kn basis).
Mina Al Arab ↔ Corniche 10.0 nm ≈ **37 min** · Al Marjan ↔ Al Hamra 4.0 nm ≈ **24 min** · Creek ↔ Jazirat Al Hamra 13.0 nm ≈ **48 min** (11.25 min in-creek @8 kn).
**Honest read:** RAK roads are uncongested (no TomTom row; Al Marjan↔city drive ~25–35 min). The water line is **slower than the road on every corridor** — this stack is a resort-experience/premium-transfer play, not a time play. L1 is priced and sized accordingly (small).

## 3 · Seat pricing — DERIVED (no canon; below Abu Dhabi per instruction logic; flag for Jaideep confirmation)

Substitute anchors (TOURISM-DEMAND §4): Al Marjan↔city metered taxi ≈ AED 57 (~$15.5, primary tariff math); Mina Al Arab↔city ≈ AED 34; abra AED 10/station public floor; road commute anchor ≈ AED 2,508/mo (~$683) Al Marjan↔city; no congestion premium available.
- **Spot seat (L2): $15 / $20 / $25** (Con/Mid/Up) — at/slightly above the door-to-door taxi meter on the long corridors; premium positioned on experience + resort segment, honestly below AD's $20/25/30 (cheaper substitutes, no time win).
- **L1 committed monthly seat = 44 legs × spot × ≈0.59 (bundle discount, program-standard pass structure) → $389 / $519 / $649, rounded $400 / $500 / $650.** DERIVED band **$400–650/mo** — below AD's $500–775 and Dubai's $650–900, consistent with RAK's cheaper road substitutes; 59–95% of the metered road anchor. **Flag for Jaideep.**

## 4 · Experience & charter pricing — DERIVED from sourced benchmarks (headline layer)

- Shared foiling experience (60–75 min: Al Marjan/Al Hamra coast loop, creek-mouth heritage run, Jazirat Al Hamra sunset): **$35 / $45 / $55 pp** — inside the sourced RAK band (kayak/abra floor $27–48 · Suwaidi Pearls $50–71 · zipline anchor $88).
- Private charter: **$400 / $475 / $550 per hr** — DERIVED; RAK's only published on-water hourly is the RAKTA abra at AED 300/hr (~$82, displacement heritage craft — floor, not comparator). Band anchored to AD's derived $450–600 with a further haircut for RAK price level. **Weakest-anchored price in this file — labeled.**

## 5 · Opex basis

| Line | Value | Basis |
|---|---|---|
| Crew | **$30/hr** × activity hrs | CREW-COST-RAS-AL-KHAIMAH.md MID $27.97 rounded up (LOW $21.47) |
| Energy | 4.1 kWh/nm (N45, canon) × **$0.1229/kWh** | **EtihadWE commercial tariff, primary:** top slab (>6,000 kWh/mo) **38 fils + 5 fils surcharge = 43 fils/kWh** (https://etihadwe.ae/en/About/Pages/Tariff.aspx) + 5% VAT = 45.15 fils ÷ 3.6725. Marginal top-slab rate applied to ALL kWh (conservative; blended would be ~10% cheaper). Cheaper than $0.30 canon ⇒ sourced tariff used per addendum. Sensitivity: at $0.30 canon, energy ×2.4; Mid net falls ~$2.1K/mo (payback ~13.3 yr) |
| Berthing | **$527/mo** | PRIMARY: Royal Yacht Club of RAK published rates — 39–48 ft wet berth, 12-month rate **AED 43/ft/mo incl. VAT** × 45 ft = AED 1,935/mo (https://alhamrawaterfront.alhamra.ae/media/0mcf1mjd/ryc-rates-public-25.pdf). Cheapest berth in the UAE run (AD $911 primary, cross-check) |
| Insurance | $4,167/mo ($50K/yr ≈ 2% hull + P&I) | placeholder assumption, same treatment as Boston/Dubai/AD; UAE-licensed insurer |
| Maintenance | $6,875/mo ($82.5K/yr) | canon $65K/yr N30-class scaled to N45 (Boston precedent midpoint) |
| Network share | 10% of gross | canon |
| Activity hours | 185 / 209 / 246 hrs/mo | derived: commute 132 (22 days × 6 hr) + experiences ×1.25 hr + charter hrs, ×1.15 positioning-standby (AD structure) |
| Energy nm | 2,818 / 2,977 / 3,384 nm/mo | commute 8 legs/day × 13.5 nm avg (4× spine 17 + 4× Mina 10) × 22 = 2,376 + experiences (≈7 nm/sailing) + charter (≈10 nm/hr) + cargo runs (upside, 12 nm) + 10% repositioning |

Fixed (berth + insurance + maintenance) = **$11,569/mo**.

**Season shape (stated assumption per addendum):** 12-month year; Jun–Sep midday dip, volume shifted to early-morning/evening blocks (evening legs at the 20 kn night planning basis, ≈65-min spine); winter Oct–Apr (events season) runs above the monthly averages shown. No winter discount applied.

## 6 · Scenarios (monthly, USD) — lines sum EXACTLY to gross (script-verified, /tmp/rak_verify.py) — **SUPERSEDED for renderables by §9 (2026-08-16 re-tier); preserved as derivation history**

Commute capacity: 8 legs/day × 20 seats × 22 weekdays = 3,520 leg-seats/mo; each committed seat consumes 44.

### Conservative (deliberately punitive: pre-Wynn base, zero anchor)
| Layer | Quantity × price | $/mo |
|---|---|---|
| L1 committed seat bundles | 16 seats × $400 | 6,400 |
| L2 spot seats | 2,816 residual leg-seats × 8% fill = 225 × $15 | 3,375 |
| L3 shared experiences | 18 sailings × 10 pax × $35 | 6,300 |
| L3 private charters | 6 hrs × $400 | 2,400 |
| U1 sponsorship / U2 cargo | — (upside only) | 0 |
| **Gross** | | **18,475** |
| Network share (10%) | | −1,847.50 |
| Crew 185 hrs × $30 | | −5,550 |
| Energy 2,818 nm × 4.1 × $0.1229 | | −1,420 |
| Berthing + insurance + maintenance | 527 + 4,167 + 6,875 | −11,569 |
| **Net** | | **−1,912** |
| **Simple payback on $2.5M** | | **n/a — cash-negative** |

### Mid
| Layer | Quantity × price | $/mo |
|---|---|---|
| L1 committed seat bundles | 24 seats × $500 | 12,000 |
| L2 spot seats | 2,464 residual leg-seats × 15% fill = 370 × $20 | 7,400 |
| L3 shared experiences | 30 sailings × 12 pax × $45 | 16,200 |
| L3 private charters | 12 hrs × $475 | 5,700 |
| U1 / U2 | — (upside only) | 0 |
| **Gross** | | **41,300** |
| Network share (10%) | | −4,130 |
| Crew 209 hrs × $30 | | −6,270 |
| Energy 2,977 nm × 4.1 × $0.1229 | | −1,501 |
| Berthing + insurance + maintenance | | −11,569 |
| **Net** | | **17,830** |
| **Simple payback** | 2,500,000 ÷ (17,830 × 12) | **11.7 yr** |

### Upside (Wynn-open demand environment)
| Layer | Quantity × price | $/mo |
|---|---|---|
| L1 committed seat bundles | 32 seats × $650 | 20,800 |
| L2 spot seats | 2,112 residual leg-seats × 25% fill = 528 × $25 | 13,200 |
| L3 shared experiences | 48 sailings × 14 pax × $55 | 36,960 |
| L3 private charters | 22 hrs × $550 | 12,100 |
| U1 sponsorship (upside only) | $150K/yr fleet program ÷ 4 vessels ÷ 12 (placeholder canon per Boston) | 3,125 |
| U2 cargo (upside only) | 12 runs × $250 — clean classes: resort resupply (Al Marjan/Al Hamra/Mina Al Arab), premium parcels, medical/lab; courier-linehaul logic per Boston; **no RAK waterborne freight tariff found ⇒ upside-only** | 3,000 |
| **Gross** | | **89,185** |
| Network share (10%) | | −8,918.50 |
| Crew 246 hrs × $30 | | −7,380 |
| Energy 3,384 nm × 4.1 × $0.1229 | | −1,706 |
| Berthing + insurance + maintenance | | −11,569 |
| **Net** | | **59,612** |
| **Simple payback** | 2,500,000 ÷ (59,612 × 12) | **3.5 yr** |

## 7 · Honest reads (NOT massaged — reported per instruction) — **pre-re-tier reads; §9 carries the current reads**

- **Mid-case payback is 11.7 yr — above the 10-yr financeable line.** Inputs were not adjusted to fix this. RAK today (1.35M visitors, ~50% domestic, ~8–9K keys, uncongested roads, water slower than road on every corridor) is the weakest single-N45 market of the three UAE cities on current demand. The stack only clears financeable territory in the Wynn-open environment (Upside 3.5 yr — same physics as the 2.49-yr canon benchmark, reached on a 1,530-key integrated resort + 12,000-key Marjan Beach pipeline).
- **Conservative is cash-negative (−$1.9K/mo)**: fixed costs ($11.6K/mo) exceed what a punitive pre-Wynn month earns. Stated plainly; single-vessel RAK deployment before 2027 is a strategic (authority-partnership) decision, not a standalone yield case.
- **Timing framing must stay honest in anything rendered:** the product sells arrival experience, lagoon-to-lagoon direct hops and event-day capacity — never "faster than the road."
- Structural cost picture: cheapest berth ($527/mo primary) and crew ($30/hr) in the program, but EtihadWE energy ($0.1229/kWh primary) is ~2.1× Abu Dhabi's ADDC rate — energy is a real line here (~8% of Mid gross vs ~1% in AD).
- Revenue mix is tourism-weighted per addendum: L3 = 47–55% of gross in Mid/Upside; the L1 layer is deliberately the smallest of the three UAE cities.
- Weakest links, in order: charter $/hr (DERIVED, thinnest local anchor) · L1 band (DERIVED, flag for Jaideep) · Al Marjan landing (no verified facility until Wynn marina 2027 — interim buoy/jetty coordination required) · Mid experience volume (30 sailings/mo needs ~1/day sold at 12 pax against a 1.35M-visitor base — plausible vs Suwaidi/kayak incumbents but unproven) · insurance placeholder.

## 8 · Assumption register (deltas vs Boston/AD template)

| Assumption | Value | Basis | Confidence |
|---|---|---|---|
| Corridor distances | 4/10/17/13 nm | DERIVED-approximate (OSM coords × routing factor, rounded up); **no route_ids — sealed set contaminated** | Derived — flagged |
| Speed basis | 5/8/12/25/20-night kn | conservative planning basis; **no numeric RAK rules published** | Assumption — flagged everywhere |
| Committed seats 16/24/32 | scenario | below AD (24/32/36) — thin commuter base, stated | Derived |
| Spot fill 8/15/25% | scenario | below AD (10/20/30) — no congestion driver; labeled unproven | Placeholder |
| Experience sailings 18/30/48, 10–14 pax | scenario | ≤1 daily even in Upside; 1.35M visitors, Suwaidi/kayak/abra incumbents daily | Benchmark-bounded |
| Experience price $35–55 pp | benchmark | sourced RAK band $27–88 | Sourced-band |
| Charter $400–550/hr | DERIVED | AD band minus haircut; abra AED 300/hr floor only local anchor | Weak — labeled |
| Seat band $400–650/mo | DERIVED | 44 × spot × 0.59; road anchor AED 2,508/mo | Derived — flag for Jaideep |
| Energy $0.1229/kWh | sourced | EtihadWE commercial top slab 43 fils + VAT, primary; marginal rate on all kWh (conservative) | Sourced (primary) |
| Berth $527/mo | sourced | RYC published 12-mo rate, 39–48 ft, incl VAT | Sourced (primary) |
| Crew $30/hr | benchmark-anchored | UAE-ADAPTED MID $27.97 + buffer; UAE-wide sources (no RAK rows found) | Sourced-with-assumed-burden |
| Cargo $250/run × 12 (upside) | placeholder | courier-linehaul logic; no RAK waterborne tariff | Weak — upside only |
| Summer midday dip | qualitative | addendum-mandated | Stated assumption |
| Dubai↔RAK express (~45 nm) | **excluded from economics** | inter-emirate = later-phase roadmap only per addendum; requires Dubai-side landing rights | Excluded |

## 9 · Re-tier 2026-08-16 — Wynn-open planning basis (CURRENT — supersedes §6 tiers for all renderables)

**Directive (Jaideep, 2026-08-16):** the Wynn-open demand environment is the planning basis for **all three scenarios**. The renderable statement of the assumption appears ONCE, in the microsite's notes block (fn14): *"Economics assume Wynn Al Marjan Island (opening 2027) is open."* No other timing language renders anywhere — no dates for Navier operations in renderables or `_internal`. The former base-destination tiering (§6) no longer renders; it is preserved above and in fleet-investors.json `_internal.superseded_2026_08_16`.

**Wynn-open pool anchors (all previously sourced — TOURISM-DEMAND §1–2; nothing new introduced):** 1,530 rooms × 71.2% FY2024 occupancy ≈ 1,089 occupied rooms ≈ ~2,180 on-island overnight guests/day at the published opening scale · 9,000+ jobs · 22 F&B venues · atop the 1.35M-visitor base and seven operating Al Marjan hotels. Every quantity below traces to the §3–§4 price bands, the §6 builds, the §8 tier comparisons (AD ceilings), or a conservative fraction of the sourced figures above. Prices unchanged — all inside the derived/sourced bands (the $400 seat floor is now unused).

### Conservative — floor: capture held at the former working case
Deliberately thin: the open resort cluster is assumed to add **nothing** to captured demand — quantities and prices are the former §6 Mid build, unchanged.
| Layer | Quantity × price | $/mo |
|---|---|---|
| L1 committed seat bundles | 24 seats × $500 | 12,000 |
| L2 spot seats | 2,464 residual leg-seats × 15% fill = 370 × $20 | 7,400 |
| L3 shared experiences | 30 sailings × 12 pax × $45 | 16,200 |
| L3 private charters | 12 hrs × $475 | 5,700 |
| **Gross** | | **41,300** |
Hours 209 · 2,977 nm · crew 6,270 · energy 1,501 · fixed 11,569 → opex **19,340** · network share 4,130 → **Net 17,830** · **Payback 2.5M ÷ 213,960 = 11.684 → ~11.7 yr.** Above the 10-yr financeable line — rendered plainly as the floor; inputs NOT adjusted to fix it.

### Mid — working case: former §6 Upside base layers (upside lines excluded)
| Layer | Quantity × price | $/mo |
|---|---|---|
| L1 committed seat bundles | 32 seats × $650 | 20,800 |
| L2 spot seats | 2,112 residual leg-seats × 25% fill = 528 × $25 | 13,200 |
| L3 shared experiences | 48 sailings × 14 pax × $55 | 36,960 |
| L3 private charters | 22 hrs × $550 | 12,100 |
| **Gross** | | **83,060** |
Hours (132 + 48×1.25 + 22) × 1.15 = 246.1 → **246** · crew 7,380. Energy nm (2,376 + 336 + 220) × 1.1 = 3,225.2 → **3,225** · 3,225 × 4.1 × $0.12294 = **1,626**. Opex 7,380 + 1,626 + 11,569 = **20,575** · network share 8,306 → **Net 74,754 − 20,575 = 54,179** · **Payback 2.5M ÷ 650,148 = 3.845 → ~3.8 yr.**

### Upside — higher capture at documented ceilings (+ the two upside-only lines)
| Layer | Quantity × price | $/mo | Anchor |
|---|---|---|---|
| L1 committed seat bundles | 36 seats × $650 | 23,400 | 36 = AD upside tier (§8 comparison row); the former reason for sitting below AD (thin commuter base) is directly addressed by the published 9,000 jobs + 1,530 keys. Flag: unproven |
| L2 spot seats | residual 3,520 − 1,584 = 1,936 × 30% = 580.8 → 580 × $25 | 14,500 | 30% = AD upside fill (§8 comparison row). Flag: unproven |
| L3 shared experiences | 60 sailings × 14 pax × $55 | 46,200 | 2/day = 840 pax/mo ≈ 1.3% of Wynn occupied-room guests alone (~2,180/day × 30), excluding the rest of the 1.35M base and the seven existing hotels — conservative fraction |
| L3 private charters | 22 hrs × $550 | 12,100 | held at the Mid quantity — weakest-anchored price in the file, deliberately not pushed |
| U1 sponsorship (upside only) | $150K/yr ÷ 4 vessels ÷ 12 | 3,125 | placeholder canon per Boston |
| U2 cargo (upside only) | 12 runs × $250 | 3,000 | courier-linehaul logic; no RAK waterborne tariff — upside-only |
| **Gross** | | **102,325** | |
Hours (132 + 60×1.25 + 22) × 1.15 = 263.35 → **263** · crew 7,890. Energy nm (2,376 + 420 + 220 + 144) × 1.1 = **3,476** · × 4.1 × $0.12294 = **1,752**. Opex **21,211** · network share 10,232.50 → **Net 92,092.50 − 21,211 = 70,881.50 (renders 70,882)** · **Payback 2.5M ÷ 850,578 = 2.939 → ~2.9 yr.** Annual rounding from unrounded nets: 213,960 → 214,000 · 650,148 → 650,000 · 850,578 → 851,000.

### Register deltas vs §8 (re-tier)
Committed seats **24/32/36** (was 16/24/32) · spot fill **15/25/30%** (was 8/15/25) · experience sailings **30/48/60** at **12/14/14** pax (was 18/30/48 at 10/12/14) · charter hrs **12/22/22** (was 6/12/22) · prices unchanged within the §3–§4 bands. Cost structure unchanged: crew hours and energy nm scale with activity exactly per §5 formulas; fixed lines flat; network share 10% of gross scales with revenue.

### Honest reads (current)
- Conservative ~11.7 yr is above the 10-yr financeable line — rendered plainly as the floor, not adjusted.
- Upside L1/L2 sit exactly at the AD tier ceilings and L3 runs 2/day — all flagged unproven for Jaideep; charter $/hr remains the weakest anchor (quantity held).
- fn10 sensitivity recomputed on the new Mid: at $0.30/kWh, energy 13,222.5 kWh × 0.30 = 3,966.75 → net 51,838 → payback 4.019 → ~4.0 yr (formerly ~13.3 yr on the old tiering).
- No time-play claims anywhere; the only timing language in renderables is the single fn14 assumption sentence.
- L3 share of gross: 53% / 59% / 57% (Con/Mid/Up) — the experience layer remains the headline layer.

**Script-verified 2026-08-16 (re-tier, /tmp/rak_qa.py):** every layer line sums exactly to gross; nets, paybacks and annuals recomputed to $0 diff; kill-scan clean on both JSONs; all footnote refs resolve.
