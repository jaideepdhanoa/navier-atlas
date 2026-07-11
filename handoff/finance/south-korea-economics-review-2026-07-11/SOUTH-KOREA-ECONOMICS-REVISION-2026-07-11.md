# South Korea unit-economics revision — evidence and route schedule review

**Date:** 11 July 2026  
**Scope:** Swing, Kakao Mobility, and NAVER’s shared 39-route South Korea model  
**Status:** Audit scenario only; no production model, workbook, Sheet, or live deck has been changed.

## Decision summary

- All **39 routes** matched an existing canonical route ID; there are no name-only joins.
- Removing the arbitrary 15-leg ceiling and applying a 12-hour operating window produces **3–21 gross legs/day**, with a median of **9**.
- The schedule denominator includes 20-knot run time, 20-minute turnaround, 10-minute boarding dwell, and energy-proportional charging.
- At **65% seat occupancy** and a separately visible **65% revenue-leg utilization**, **34** routes have positive EBITDA under the premium-local-analog scenario; **21** fall below three-year payback and **18** do not.
- The under-three-year set is **not cleared for production pricing**. The fare sources are local premium whole-vessel analogs translated through exact route duration; they are not exact fares for the canonical origin–destination pairs.
- Korean crew cost and the existing **$51,000/year port and administration cost** are retained. No unsupported headcount or port-cost reduction is used.

## Model mechanics

| Input | Treatment |
|---|---|
| Service window | 12 hours/day |
| Cruise speed | 20 kt |
| Turnaround | 20 minutes/leg |
| Boarding dwell | 10 minutes/leg |
| Charging | `distance / 70 nm × 45 minutes` per leg, using Navier’s published 70-nm range and 45-minute DC fast-charge figures |
| Gross legs/day | `floor(720 / (run + turnaround + dwell + charge recovery))`; no 15-leg ceiling |
| Revenue-leg utilization | 65%, shown separately |
| Seat occupancy | 65% = 5.2 riders on an eight-seat N30 |
| Operating days | 274/year |
| CAPEX | $600,000 for South Korea under the non-US/EU commercial rule |
| Crew | Live workbook value retained: $134,951/year |
| Port/admin | Live workbook value retained: $51,000/year |

The charging term is a planning proxy, not an engineering certificate. Before production it still needs usable battery reserve, charge-curve, thermal-derating, charger-power, and berth-availability validation. It is preferable to charging a full fixed interval after every short leg because it scales with energy consumed.

## Korean wage evidence

The official [2026 Korea Seafarer’s Statistical Year Book](https://www.koswec.or.kr/koswec/information/sailorshipstatistics/detailSailorShipStaticsPage.do?prg=statistic&seqIdx=SSS_0000000250), reference date 2025-12-31, reports monthly average total wages for coastal leisure and ferry boats of **KRW 3,890k for a master** and **KRW 3,506k for an ordinary seaman**. One master plus one deck rating, multiplied by 1.8 relief teams and a 1.2 payroll burden, implies **$134,766/year** at KRW 1,422.5/USD—within **0.137%** of the workbook. The workbook figure is therefore retained. The publication supports wages, not safe-manning; Korean safe-manning validation remains open.

## Premium fare evidence

| Benchmark market | Published product | Whole-vessel price | Minimum duration | Evidence use |
|---|---|---:|---:|---|
| Seoul | [Golden Blue Marina Sea Ray private charter](http://www.gbboat.com/mobile/reservation/price.html) | KRW 250,000 | 30 min | Local premium analog; route duration scales longer trips |
| Incheon | [Hyundai Yacht Holiday private charter](https://itour.incheon.go.kr/thmtour/rcmdtour/detail.do?cotId=ITA23052417015841280) | KRW 320,000 | 40 min | Local premium analog; route duration scales longer trips |
| Jeju | [Gimnyeong Yacht private tour](http://gnytour.com/PrivateTour) | KRW 780,000 | 70 min | Local premium analog; route duration scales longer trips |
| Busan | [Busan private-yacht premium bracket](https://experiences.myrealtrip.com/products/4224744) | KRW 350,000 | 50 min | Local premium analog; route duration scales longer trips |
| Geoje | [Geoje private yacht charter](http://www.haemayachting.com/privatetour) | KRW 350,000 | 50 min | Local premium analog; route duration scales longer trips |
| Yeosu | [Stella Yacht Club private-tour published range; premium endpoint](http://yeosukorea.com/?page_id=10) | KRW 400,000 | 60 min | Local premium analog; route duration scales longer trips |
| Tongyeong | [Pangpang 10,000-won Yacht Tour weekend/holiday whole-vessel rental](https://www.tripinfo.co.kr/info.html?content_type_id=12&content_id=3075913) | KRW 150,000 | 60 min | Local premium analog; route duration scales longer trips |

All conversions use **KRW 1,422.4/USD** and 5.2 riders. The equivalent fare is deliberately labeled a comparable premium benchmark, not an observed fare on the canonical route.

## Route-level result

### Sub-three-year benchmark cases — pricing validation still required

| Route ID | Corridor | Gross legs/day | Premium-equivalent fare/rider | Payback |
|---|---|---:|---:|---:|
| `rn-7c451ce2752d` | Oksu Pier → Apgujeong Pier | 21 | $33.80 | 1.40 yr |
| `rn-529e3834c165` | Ttukseom → Jamsil | 20 | $33.80 | 1.51 yr |
| `rn-64f4b4293a52` | Seongsan Port (Udo ferry gateway + Seongsan Ilchulbong tender) → Udo (Cow Island) — Cheonjin Port + Haunchi Port | 20 | $105.45 | 0.35 yr |
| `rn-b4b6294b39e2` | Apgujeong Pier → Seoul Forest Wharf | 19 | $33.80 | 1.65 yr |
| `rn-d128d9b4c5c8` | Jongdal Port (Udo Ferry) → Udo (Cow Island) — Cheonjin Port + Haunchi Port | 19 | $105.45 | 0.37 yr |
| `rn-0a711c22926a` | Mangwon Pier → Yeouido | 18 | $33.80 | 1.80 yr |
| `rn-bc4b1bfe4b23` | Seoul Forest Wharf → Ttukseom | 17 | $33.80 | 1.99 yr |
| `rn-38d097ab8503` | Busan → Busan/Geoje Cluster | 16 | $47.32 | 1.28 yr |
| `rn-dd841301f944` | Seongsan Eup → Seopjikoji | 16 | $105.45 | 0.45 yr |
| `rn-6e4ab1de83d4` | Yeouido → Oksu Pier | 15 | $33.80 | 2.52 yr |
| `rn-2be3c3285c7a` | Seopjikoji → Jeju | 14 | $105.45 | 0.53 yr |
| `rn-6d96e229ce7e` | Magok Pier → Yeouido Pier | 14 | $33.80 | 2.90 yr |
| `rn-7e7e6da7abba` | Incheon Coastal Passenger Terminal → Yeongjong Island Marina | 13 | $43.26 | 2.08 yr |
| `rn-ed5d6c0609fe` | Jeju → Seogwipo Jungmun | 12 | $105.45 | 0.64 yr |
| `rn-5689dc99e479` | Muuido Island Ferry Berth → Yeongjong Island Marina | 11 | $43.26 | 2.88 yr |
| `rn-8a05c6dc9a81` | Jeju Yacht Club / Aewol Marina pipeline → Jeju Ferry Passenger Terminal | 10 | $105.45 | 0.81 yr |
| `rn-451fa6544ccd` | Magok Pier → Jamsil Pier | 9 | $60.84 | 2.19 yr |
| `rn-c35e6140fd66` | Jeju Ferry Passenger Terminal → Hallim Port (Biyangdo ferry gateway) | 8 | $105.45 | 1.09 yr |
| `rn-2c32d38bb153` | Jeju → Seongsan Eup | 8 | $105.45 | 1.10 yr |
| `rn-50bd5ea42fec` | Jongdal Port (Udo Ferry) → Jeju Ferry Passenger Terminal | 6 | $105.45 | 1.70 yr |
| `rn-7288c917e055` | Jeju Ferry Passenger Terminal → Seongsan Port (Udo ferry gateway + Seongsan Ilchulbong tender) | 6 | $105.45 | 1.70 yr |

### Held — cannot reach three-year payback under the same supported scenario

| Route ID | Corridor | Gross legs/day | Current benchmark payback | Fare needed for 3-year payback |
|---|---|---:|---:|---:|
| `rn-dd8e26889f29` | Magok → Mangwon Pier | 16 | 8.61 yr | $29.07 |
| `rn-047fe5d8e686` | Jamsil Pier → Yeouido Pier | 12 | 4.18 yr | $38.89 |
| `rn-ce55c292989a` | Yeouido Pier → Ttukseom Pier | 11 | 5.35 yr | $42.42 |
| `rn-66dce8d7e72d` | Incheon Coastal Passenger Terminal → Muuido Island Ferry Berth | 9 | 4.69 yr | $51.91 |
| `rn-c33493f0f593` | Saryangdo Island ferry pier → Yokjido Island ferry pier | 9 | No positive EBITDA | $51.94 |
| `rn-ff2684a4219c` | Gimpo Ara Marina → Incheon Coastal Passenger Terminal | 9 | 4.70 yr | $51.95 |
| `rn-2a7a816ff5a9` | Geumodo Yeocheon Ferry Terminal → Yeosu Passenger Ferry Terminal | 8 | 3.58 yr | $58.42 |
| `rn-f4f4e680146e` | Tongyeong Passenger Ferry Terminal → Yokjido Ferry Terminal | 8 | No positive EBITDA | $58.45 |
| `rn-eab1a8d9b140` | Yokjido Island ferry pier → Tongyeong Ferry Terminal | 8 | No positive EBITDA | $58.45 |
| `rn-972f52f72589` | Yeosu Passenger Ferry Terminal → Samcheonpo Ferry Terminal | 7 | 5.13 yr | $66.88 |
| `rn-4f591a53d3b3` | Geumodo Yeocheon Ferry Terminal → Yokjido Ferry Terminal | 5 | No positive EBITDA | $93.67 |
| `rn-716172aedee7` | Yeosu Passenger Ferry Terminal → Yokjido Ferry Terminal | 5 | 6.20 yr | $93.69 |
| `rn-79388bf546a1` | Samdeok Yokji Ferry Terminal → Yeosu Passenger Ferry Terminal | 4 | 7.15 yr | $117.06 |
| `rn-b93989547df9` | Tongyeong Passenger Ferry Terminal → Yeosu Passenger Ferry Terminal | 4 | 5.84 yr | $117.14 |
| `rn-649a78c56f95` | Yeosu Passenger Ferry Terminal → Gaochi Passenger Ferry Terminal | 4 | 5.24 yr | $117.18 |
| `rn-ba28d38bee02` | Tongyeong Passenger Ferry Terminal → Geumodo Yeocheon Ferry Terminal | 4 | No positive EBITDA | $117.28 |
| `rn-0bf2689ed1c9` | Busan Coastal Ferry Terminal (Yeonan Yeogaek — Jeju line) → Yokjido Island ferry pier | 3 | 3.94 yr | $156.34 |
| `rn-fd62bdd18267` | Busan Coastal Ferry Terminal (Yeonan Yeogaek — Jeju line) → Saryangdo Island ferry pier | 3 | 3.04 yr | $156.56 |

## Production gate

1. Apply the 65% South Korea midpoint occupancy and schedule-derived capacity in **both** independent economics engines.
2. Keep 65% revenue-leg utilization as a separate named input; do not multiply it into an opaque effective occupancy.
3. Preserve the workbook-led crew and port costs.
4. Do not promote the premium-analog fares as exact route fares. Bind exact route/operator pricing where available; otherwise retain explicit low-confidence comparable-fare provenance.
5. Re-run model → workbook/Sheet → Swing, Kakao, and NAVER partner JSON → sidecar/manifest only after the two engines agree.
6. Keep all 18 non-compliant routes visibly held. Do not tune unsupported assumptions solely to cross the three-year threshold.
7. Before any live-deck clearance, validate charging engineering and Korean safe manning, then replay copy, linkage, inheritance, finance-parity, and live-Slides readback gates.

## Artifacts

- `KOREA-ROUTE-SCHEDULE-SCENARIO-2026-07-11.csv` — route-level audit table
- `KOREA-ROUTE-SCHEDULE-SCENARIO-2026-07-11.json` — assumptions, limits, and route rows
- `KOREA-PREMIUM-FARE-EVIDENCE-2026-07-11.json` — source ledger
- `KOREA-SEAFARER-WAGE-EVIDENCE-2026-07-11.json` — official wage extraction and workbook cross-check
- `build_korea_schedule_scenario.py` — reproducible audit builder