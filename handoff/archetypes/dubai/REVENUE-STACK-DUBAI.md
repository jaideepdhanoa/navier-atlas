# REVENUE-STACK-DUBAI — one N45, tourism-weighted utilization stack (internal audit file — never renders)

Grammar per boston/REVENUE-STACK-BOSTON.md; international adaptations per INTERNATIONAL-ADDENDUM. One **N45 (20 seats, $2.5M capex — canon)**, 16-hr service day, **12-month operating year with summer midday shape**: Jun–Sep midday leisure demand dips and experience sailings shift to morning/evening slots; commuter peaks unaffected (climate-controlled cabin). Scenario quantities are annual monthly averages with that shape absorbed. FX peg 3.6725. Sums verified by script before writing (run 2026-08-16; all layer lines sum exactly to gross).

## Corridors (GEOMETRY-DUBAI.json clean routes ONLY)

| Role | route_id | Corridor | nm |
|---|---|---|---|
| Commute spine | **rn-02b2927692e0** | Bluewaters Ferry Station ↔ Dubai Canal Marine Transport Station 1 | 9.6 |
| Commute alt/extension | rn-9d23e412de22 | Business Bay MTS ↔ Bluewaters Ferry Station | 10.0 |
| Experience loop A | **rn-200157a4d545** | Bluewaters Ferry Station ↔ The World Islands | 9.9 |
| Experience loop B | rn-d3a88461a5ed / rn-f314996e94b7 | Atlantis The Palm Jetty ↔ Bluewaters | 3.5 / 3.6 |
| Marquee/charter showcase | rn-b7ac6238165d | Atlantis The Palm Jetty ↔ Mina Rashid Cruise Terminal | 12.9 |
| Charter feeder | rn-c6db0ce8b6a6 | Dubai Harbour Cruise Terminal ↔ Atlantis The Palm Jetty | 2.8 |

## Spine timing at controlling limits (SPEED-RULES-DUBAI.md basis)

rn-02b2927692e0, 9.6 nm (segment split estimated from chart geography):

| Segment | nm | Limit basis | Time |
|---|---|---|---|
| Bluewaters/Marina basin exit | 0.4 | 5 kn (port/marina — secondary-verified) | 4.8 min |
| Open coast | 7.7 | 25 kn N45 service speed (canon — flag) | 18.5 min |
| Dubai Water Canal to Canal MTS 1 | 1.5 | 6 kn (conservative assumption — no numeric limit verified) | 15.0 min |
| Dock dwell (2 calls × 2 min) | — | assumption | 4.0 min |
| **Total** | 9.6 | | **≈42 min** |

**Zone time cost:** the 1.9 restricted nm cost 19.8 min vs 4.6 min at open speed — **+15.2 min/leg** is the price of the 5-kn/canal zones. ("What relief unlocks," never base math: a foil-borne 12-kn canal allowance — low-wake case — would save ~7.5 min/leg.) Land substitute: ~25 km via SZR, ~35–60+ min at peak (TOURISM-DEMAND §4). Base schedule: 8 commuter legs/day (4 AM-peak, 4 PM-peak), 22 weekdays/mo → 176 legs, 3,520 leg-seats/mo, 1,690 commute nm/mo.

## Seat pricing — DERIVED (no canon for this market; flag for Jaideep confirmation)

Substitute anchors (TOURISM-DEMAND §3–4): RTA marine fare ceiling AED 75 ≈ $20 (ferry Gold class); RTA water-taxi route band AED 55–205 ≈ $15–56; street taxi Marina↔Downtown ~$16–19 + Salik AED 6+VAT/gate peak; ride-hail ~$30 (low-confidence band edge); 42-min productive water leg vs 35–60+ min drive.
- **Spot seat (L2): $25 / $30 / $35** (Con/Mid/Up) — inside the water-taxi band, above ferry Gold, at/below premium ride-hail door-to-door.
- **L1 committed monthly seat = 44 legs × spot × ≈0.59 (bundle discount ≈41%) → $650 / $775 / $900.** DERIVED band **$650–900/mo** (coincidentally equal to NY canon; derived independently from Dubai substitutes).

## Experience & charter pricing — DERIVED from sourced benchmarks

- Shared foiling experience (60–75 min, Palm/Bluewaters/World Islands loops A/B): **$35 / $45 / $55 pp** — positioned mid-band vs sourced AED 85–425 pp shared-tour market; premium over conventional shared tours justified by speed/smoothness, below Atlantis-frontage top band.
- Private charter (marquee route + Harbour feeder): **$500 / $575 / $650 per hr** — between RTA water-taxi charter (~$109/hr, 20 pax) and Dubai Ferry private hire (~$762/hr); within small-yacht AED 1,700–9,000/trip band.

## Opex basis

| Line | Value | Basis |
|---|---|---|
| Crew | **$30/hr** × activity hrs | CREW-COST-DUBAI.md MID $29.10 rounded up (LOW $21.47) |
| Energy | 4.1 kWh/nm (N45, canon) × **$0.126/kWh** | DEWA commercial top slab 0.380 + fuel surcharge 0.060 (Aug 2026) = 0.44 AED/kWh + 5% VAT = 0.462 AED/kWh ÷ 3.6725. Primary: https://dewa.gov.ae/en/consumer/billing/slab-tariff (accessed 2026-08-16). Cheaper than $0.30 canon ⇒ sourced tariff used per addendum. Monthly draw 8.8–11.5 MWh sits almost entirely in the >6,000 kWh top slab; charging all kWh at top-slab rate is the conservative treatment. Sensitivity: at $0.30 canon the energy line rises ~2.4× (+$1.5–2.0K/mo) — nets stay positive in all scenarios. |
| Berthing | **$2,723/mo** (AED 10,000) | ASSUMPTION inside sourced Dubai Marina band AED 6,000–30,000/mo (secondary: https://yachtr.com/guides-dubai-marina-buyer-guide/) — commercial berth agreement TBD |
| Insurance | $4,167/mo ($50K/yr ≈ 2% hull + P&I) | placeholder assumption, same treatment as Boston; UAE-licensed insurer mandatory (ECR 9/2020 Art. 9.8) |
| Maintenance | $6,875/mo ($82.5K/yr) | canon $65K/yr N30-class scaled to N45 (Boston precedent midpoint) |
| Network share | 10% of gross revenue | canon |
| Activity hours | 198 / 245 / 300 hrs/mo | derived: commute 132 + experiences/charters + 15% positioning-standby |
| Energy nm | 2,149 / 2,439 / 2,783 nm/mo | commute 1,690 + experience/charter nm + 10% repositioning |

## Scenarios (monthly, USD) — lines sum EXACTLY to gross

### Conservative
| Layer | Quantity × price | $/mo |
|---|---|---|
| L1 committed seat bundles | 24 seats × $650 | 15,600 |
| L2 spot seats | 2,464 residual leg-seats × 10% fill = 246 seats × $25 | 6,150 |
| L3 shared experiences | 20 sailings × 12 pax × $35 | 8,400 |
| L3 private charters | 8 hrs × $500 | 4,000 |
| U1 sponsorship | — (upside only) | 0 |
| U2 cargo | — (upside only) | 0 |
| **Gross** | | **34,150** |
| Network share (10%) | | −3,415 |
| Crew 198 hrs × $30 | | −5,940 |
| Energy 2,149 nm × 4.1 × $0.126 | | −1,108 |
| Berthing + insurance + maintenance | 2,723 + 4,167 + 6,875 | −13,765 |
| **Net** | | **9,922** |
| **Simple payback on $2.5M** | 2,500,000 ÷ (9,922 × 12) | **21.0 yr** |

### Mid
| Layer | Quantity × price | $/mo |
|---|---|---|
| L1 committed seat bundles | 32 seats × $775 | 24,800 |
| L2 spot seats | 2,112 residual leg-seats × 20% fill = 422 seats × $30 | 12,660 |
| L3 shared experiences | 40 sailings × 14 pax × $45 | 25,200 |
| L3 private charters | 16 hrs × $575 | 9,200 |
| U1 / U2 | — (upside only) | 0 |
| **Gross** | | **71,860** |
| Network share (10%) | | −7,186 |
| Crew 245 hrs × $30 | | −7,350 |
| Energy 2,439 nm × 4.1 × $0.126 | | −1,258 |
| Berthing + insurance + maintenance | | −13,765 |
| **Net** | | **42,301** |
| **Simple payback** | 2,500,000 ÷ (42,301 × 12) | **4.9 yr** |

### Upside
| Layer | Quantity × price | $/mo |
|---|---|---|
| L1 committed seat bundles | 36 seats × $900 | 32,400 |
| L2 spot seats | 1,936 residual leg-seats × 30% fill = 580 seats × $35 | 20,300 |
| L3 shared experiences | 60 sailings × 15 pax × $55 | 49,500 |
| L3 private charters | 30 hrs × $650 | 19,500 |
| U1 sponsorship (upside only) | $150K/yr fleet program ÷ 4 vessels ÷ 12 (placeholder canon per Boston) | 3,125 |
| U2 cargo (upside only) | 16 runs × $300 (clean class: medical/lab specimens + premium parcels + island-resort resupply; courier-linehaul rate logic per Boston — Dubai waterborne tariff NOT VERIFIED, hence upside-only) | 4,800 |
| **Gross** | | **129,625** |
| Network share (10%) | | −12,962.50 |
| Crew 300 hrs × $30 | | −9,000 |
| Energy 2,783 nm × 4.1 × $0.126 | | −1,435 |
| Berthing + insurance + maintenance | | −13,765 |
| **Net** | | **92,462.50** |
| **Simple payback** | 2,500,000 ÷ (92,462.50 × 12) | **2.3 yr** |

Note on L2 rounding: seats sold are rounded down to whole seats from the fill%×residual product; the stated seat count × fare is the exact revenue line.

## Fail-closed register
- Demand pools are **indicative**: no employer trackers here; L1/L2 sized on capacity × fill grammar, anchored to 18.4M existing marine riders + 19.59M visitors (sourced), not on invented rider counts.
- DERIVED (need confirmation): seat band $650–900; spot $25–35; experience $35–55 pp; charter $500–650/hr; N45 25-kn service speed flag; canal 6-kn planning speed.
- NOT VERIFIED (excluded from base math or upside-only): water-taxi charter $400/hr (secondary), ferry hire $762/hr (secondary — used only as positioning anchors), premium parking primary source, U2 cargo local tariffs, Ain Dubai operating status, World Islands development claims.
- No "boats," no Gulf counterparties, no fleet-count/program economics, no launch dates.
