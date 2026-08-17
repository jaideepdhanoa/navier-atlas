# CREW-COST-BENCHMARKS — Red Sea Global destinations

Internal audit file. Method: **SAUDI-ADAPTED + REMOTE-SITE UPLIFT** (BLS method not applicable). Peg SAR 3.75/USD. Research date: 2026-08-16.

## Method statement
Reuses the Eastern Province / Jeddah methodology verbatim (see saudi-eastern-province/CREW-COST-BENCHMARKS-EASTERN-PROVINCE.md and jeddah/CREW-COST-BENCHMARKS-JEDDAH.md): Saudi marine labor is a national market (GOSI/GASTAT frames and job-posting bands are Kingdom-wide). The Red Sea/AMAALA sites are **remote** (Umluj–Al Wajh coast, ~500 km north of Jeddah), so a remote-site uplift is applied on top of the national loaded bands.

## 1 · Base national bands (carried from EP/Jeddah, cited anew)
| Evidence | Figure (SAR/mo) | Source | Tag |
|---|---|---|---|
| Boat captain postings, KSA marine leisure ops | 7,000–10,000 | KSA job boards (naukrigulf/gulftalent) | SECONDARY |
| Yacht captain, KSA average | 6,933–8,474 (range 5,925–9,600) | naukrigulf.com/salaries/yacht-captain-salary-in-saudi-arabia | SECONDARY |
| Deckhand postings, KSA | 3,900–5,795; Jeddah FB-group hiring 2,000–3,000 (weak, below LOW band — LOW retained conservatively); "basic from SAR 4,000" marine-ops Instagram hiring post | KSA job boards + social hiring posts | SECONDARY |
| GASTAT avg monthly wage (4 sectors incl. transport) | 10,238 | stats.gov.sa | PRIMARY (economy-wide context) |
| Burden | GOSI ~11.75% Saudi / ~2% expat; iqama levies; medical; EOS accrual ~8.33%/yr; uniforms/training; housing & transport allowances → multipliers **1.35 LOW / 1.45 MID** | GOSI published rates + stated assumption | SECONDARY + DERIVED |

Base loaded (2-person crew: captain + deckhand; 208 paid h/mo each; loaded $/hr = (cap+deck)×burden÷3.75÷208):
| Case | Captain | Deckhand | Burden | **USD/hr (pair)** |
|---|---|---|---|---|
| LOW | 7,000 | 4,500 | 1.35 | **$19.9/hr** |
| MID | 12,000 | 6,000 | 1.45 | **$33.5/hr** |

## 2 · Remote-site uplift (DERIVED — stated assumptions)
Umluj/Al Wajh/Triple Bay are remote postings. RSG houses staff on site — Turtle Bay Village "now houses 6,000 of an eventual 14,000 workers, staff, and management at The Red Sea" (redseaglobal.com Turtle Bay Village page, PRIMARY) — so the employer bears accommodation, messing, and rotation travel that a Jeddah operator does not.
- Uplift components [all DERIVED]: on-site housing/messing (or housing allowance at remote premium), rotation travel to Jeddah/home country, remote-hardship allowance customary for KSA remote sites, higher recruiting/retention cost.
- Multipliers applied on loaded base: **×1.20 (LOW) / ×1.25 (MID)**.

| Case | Base $/hr | Uplift | **Remote-adjusted USD/hr (2-person crew)** | Per 16-hr service day |
|---|---|---|---|---|
| LOW | 19.9 | 1.20 | **$23.9/hr** | ≈ $382/day |
| MID | 33.5 | 1.25 | **$41.9/hr** | ≈ $670/day |
Tags: wages SECONDARY, burden DERIVED, remote uplift DERIVED, arithmetic DERIVED. Method label: **SAUDI-ADAPTED (REMOTE)**.
- Alternative structure: RSG-employed crew seconded to the network (RSG already staffs 13 vessels + marinas) could price below these bands; treat as negotiation upside, not base [DERIVED note].

## 3 · Energy
| Item | Value | Source | Confidence |
|---|---|---|---|
| National grid commercial tariff (>6,000 kWh/mo) | SAR 0.32/kWh = **$0.0853/kWh** — the modeling proxy | SERA https://www.sera.gov.sa/en/consumer/electric-tariff/... + SEC (geo-blocked; search-index captures of primary pages; verified for the Jeddah file 2026-08-16) | PRIMARY-derived |
| RSG reality | Destinations are **off-grid**: 100% solar + 1,300 MWh BESS microgrid (world's largest off-grid BESS). There is no SEC meter at Shura/Triple Bay; charging energy is RSG's own generation. Marginal daytime solar cost is plausibly *below* the SEC proxy; night charging draws on BESS capacity that is sized for resorts. | redseaglobal.com (PRIMARY) + Huawei/energy-storage.news (SECONDARY) | PRIMARY + SECONDARY |
| Modeling treatment | Use **$0.0853/kWh proxy** in all economics [per template rule: cheaper sourced local tariff beats $0.30 canon]. Flag: actual charging economics at RSG are a counterparty conversation (internal microgrid transfer price, day-vs-night charging windows, dedicated PV+storage at marinas). Charge scheduling should prefer daytime solar surplus [ASSUMPTION, flagged]. | — | DERIVED |
| Consumption | 4.1 kWh/nm (N45 canon) → energy ≈ **$0.35/nm** at proxy tariff | canon + arithmetic | DERIVED |

## Fail-closed
- No RSG-published crew wage scale (UNSOURCED); no GOSI occupation-level marine tables (absent).
- Saudization ratio for marine passenger crew: unpublished; Saudi-national crewing pushes toward MID [assumption carried from EP].
- RSG internal energy transfer price: UNSOURCED — proxy tariff stands until counterparty data.
