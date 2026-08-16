# TOURISM-DEMAND-DUBAI (internal audit file — never renders)

Tourism is the headline demand layer for the Dubai Fleet Investor page (per INTERNATIONAL-ADDENDUM). All figures sourced; accessed 2026-08-16. FX peg 3.6725.

## 1 · Visitor economy (PRIMARY)

- **19.59M international overnight visitors in 2025** (+5% YoY vs 18.72M in 2024; third consecutive record year) — DET press release: https://www.dubaidet.gov.ae/en/newsroom/press-releases/dubais-tourism-industry-achieves-third-successive-record-breaking-year
- **Hotel stock: 154,264 rooms across 827 establishments** (end-Dec 2025); DET states this leads Bangkok/New York/Paris/Singapore and is near-par with London — same release.
- H1-2025: 9.88M visitors; **80.6% occupancy**, 22.24M room nights, ADR +5% — Dubai Media Office/DET: https://dmo.dof.gov.ae/en/news-and-publications/latest-press-releases/dubai-welcomes-988-million-international-visitors-in-the-first-half-of-2025/
- Marine transit demand already proven: **18.4M marine riders 2025 (+3%)** on abras/water taxis/Dubai Ferry — https://www.mediaoffice.ae/en/news/2026/february/15-02/rta-records-802-riders-in-dubai-2025

## 2 · Marquee waterfront anchors on clean corridors (GEOMETRY-DUBAI.json)

| Anchor | Corridor binding (route_id) | Status |
|---|---|---|
| Palm Jumeirah / Atlantis (Atlantis The Palm Jetty, bp-55aa98c7fb) | rn-d3a88461a5ed (↔Bluewaters 3.5 nm), rn-c6db0ce8b6a6 (↔Dubai Harbour 2.8 nm), rn-b7ac6238165d (↔Mina Rashid 12.9 nm, marquee rank 1) | operating resort/jetty |
| Bluewaters / Ain Dubai (bp-711cf44b60, bp-cef3fdf035) | rn-200157a4d545 (↔World Islands 9.9 nm, marquee rank 2) | operating district; Ain Dubai operational status intermittent — NOT VERIFIED this run, do not claim wheel operations |
| Dubai Harbour Cruise Terminal (bp-1982dfd974) | rn-f4c2f161324c (↔World Islands 8.9 nm, marquee rank 4) | operating cruise terminal |
| Creek / Al Seef (bp-a27aa3915d, bp-6556b79930) | rn-bfa9c0d8ba7b (Festival City↔Al Seef 3.4 nm) | operating RTA marine stations |
| **The World Islands (bp-8c7fcc1977) — status, honestly:** | rn-200157a4d545 / rn-fb4ca86ddc17 / rn-842804312dbf | **largely undeveloped.** The first operating resort (Anantara World Islands, opened 2021) is reported permanently closed as of April 2025 (secondary: https://www.resortx.com/the-world-islands-dubai/). Heart of Europe cluster in phased opening with completion claims around 2026 (secondary: https://elitetraveler.com/travel/news/story-behind-the-world-islands-dubai (search-result capture; page not fully loaded — LOW CONFIDENCE) ; https://www.memphistours.co.uk/trips-to-dubai/discover-dubai-islands). Render only with "planned/partial" status flag; do NOT size demand on it. Its honest role: proof that island access is the unsolved dependency. |

## 3 · L3 experience-fare benchmarks (what the market already pays on the water)

| Benchmark | Price | Source / status |
|---|---|---|
| Shared yacht tour, Dubai Marina, 1 hr | AED 65–85 pp (~$18–23) | https://yachtridedubai.com/yacht-tour-ticket-price/ (operator price page) |
| Shared sunset tour, 2 hr | AED 99–149 pp (~$27–41) | same |
| Shared tours incl. Atlantis/Palm frontage | AED 135–425 pp (~$37–116) | https://www.skywalker.ae/news/atlantis-yacht-tour-dubai-prices-booking-best-experience/ (secondary aggregator) |
| 90-min speed-vessel tour Marina–Atlantis–Palm–Burj Al Arab | AED 102 pp (~$28) | https://anchorsbook.com/destinations/public-yacht-parties/ |
| RTA heritage abra, Water Canal sightseeing | AED 25 pp/hr; AED 300/hr full-vessel | RTA (primary): https://www.rta.ae/wps/portal/rta/ae/public-transport/marine/about-marine |
| RTA marine fares band (all modes) | AED 1–75 pp | RTA (primary): https://www.rta.ae/wps/portal/rta/ae/home/rta-services/service-details?serviceId=358 |
| RTA water taxi private charter | ~AED 400/hr, up to 20 pax | secondary: https://dubaivisitsvisa.com/article/water-taxis-dubai — NOT primary-verified |
| Dubai Ferry full-vessel private hire | ~AED 2,800/hr (~$762) | secondary: https://dubai-ferry.com/routes/ — NOT primary-verified |
| Private yacht trips (small) | AED 1,700–9,000/trip | skywalker.ae above (secondary) |

Read: a shared premium water experience clears AED 100–425 pp today on conventional hulls; full-vessel hires clear AED 300–2,800/hr depending on class. Foiling pricing derived from this band in REVENUE-STACK-DUBAI.md.

## 4 · Commuter substitutes (L1/L2 derivation inputs)

- **Street taxi (RTA-regulated):** flagfall AED 5 (road) / booking AED 9–13 (e-hail) — RTA (primary): https://www.rta.ae/wps/portal/rta/ae/home/promotion/taxi-fare . Per-km AED 2.09–2.19 (secondary: https://www.propertyfinder.ae/blog/rta-dubai-taxi-fares/). Marina↔Downtown ≈ 25 km ⇒ ~AED 60–68 (~$16–19) per leg, DERIVED.
- **Ride-hail (app-based):** Marina/Deira-class cross-city trips reported ~AED 110 (~$30) vs ~AED 60 taxi (forum-level secondary: https://www.tripadvisor.com/ShowTopic-g295424-i872-k13822205-Dubai_taxi_fares-Dubai_Emirate_of_Dubai.html) — LOW CONFIDENCE, used only as a band edge.
- **Salik road toll (primary, salik.ae):** variable pricing since 31 Jan 2025 — **AED 6 + VAT per gate at peak** (6–10 AM, 4–8 PM), AED 4 off-peak: https://www.salik.ae/en/news/salik-announces-implementation-of-variable-toll-pricing-effective-january-31-2025 and https://www.salik.ae/en/Toll-Gates/variable-toll-rates . Marina↔Downtown typically crosses 1–2 gates each way.
- **Parking:** premium zones AED 6/hr peak (secondary press captures of the 2025 variable-parking policy; e.g., https://www.arnnewscentre.ae/en/news/uae/dubai-announces-new-salik-and-parking-tariff-system/) — NOT primary-verified this run.
- **Congestion:** Dubai average ~12–13.7 min per 10 km (Dubai Media Office on TomTom index, 2023: https://mediaoffice.ae/en/news/2023/august/20-08/dubai-scores-advanced-position-in-tomtom-traffic-index ; TomTom 2024 reporting 13.7 min/10 km and ~35 hrs/yr lost — secondary captures). Peak SZR runs Marina↔Downtown are commonly 35–60+ min door-to-door; the `_ref-brief` journeys table carries 35–60 min for Marina↔Palm road trips (internal canon, indicative).
- **Monthly car-commute cost floor (DERIVED):** 44 peak legs × (2 Salik gates × AED 6.3 incl VAT) + 22 days × 9 hrs parking… parking at workplace varies too widely; the conservative derivation used for seat pricing is ride-based, not ownership-based (see REVENUE-STACK §L1).

## 5 · Seasonality statement (canon for both pages)

12-month operating year. Sheltered inner waters operable year-round; Jun–Sep summer heat suppresses midday leisure demand — experience sailings shift to morning/evening slots; commuter peaks unaffected (climate-controlled cabins). Peak visitor season Oct–Apr (`_ref-brief-dubai-uae.json`, internal canon). Scenario counts in REVENUE-STACK are annual monthly averages with this shape absorbed.
