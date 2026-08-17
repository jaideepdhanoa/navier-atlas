# REVENUE-INPUTS-ISTANBUL
Internal research record — INPUTS ONLY, no P&L assembled here. Vessel: N45, 20 seats, $2.5M capex (canon), 20 kn cruise / ~25 kn service. Date: 2026-08-16. **FX: 47.76 TRY/USD (TCMB, 2026-08-16)** — TRY volatile, re-pull at model time. Economics render USD-primary.

## 1 · Service envelope
- **Season: 12-month operating year** (mild-winter market; no seasonal shutdown). [Structure per international addendum, adapted]
- **Weather cancellation allowance: 5% of departures annually** — Marmara lodos (SW gale) days cluster Nov–Mar; Şehir Hatları/İDO routinely cancel in lodos. [DERIVED assumption — no primary cancellation-rate statistic captured; INDICATIVE, flag]
- **Demand shape:** standard AM/PM commute peaks on IST-1; weekend/summer surge on IST-2 (counter-seasonal pairing). **Ramadan note:** during Ramazan (≈Feb–Mar in 2027) midday leisure and commute demand softens and shifts to post-iftar evenings; Şeker Bayramı weekend produces an Islands surge — schedule shape, not annual-volume, adjustment. [DERIVED assumption, flag]
- Service day: 16 hr on IST-1/IST-2; IST-3 off-peak weighted; IST-4 roadmap only.

## 2 · Utilization stack — three revenue tiers (+ upside per template; U-layers not sized here)
### L1 — Committed seat bundles (premium commuter, IST-1 trunk)
- **Anchors (FARE file):** public ferry $1.1–1.4/trip · Deniz Taksi per-seat $4–11 · taxi $15–29 + 60–110 min · net minimum wage $588/mo (income-reality check).
- Per-trip premium express anchor (DERIVED): trunk **150–220 TL ($3.1–4.6)/seat-trip**.
- **Committed monthly seat (2 trips/day × 22 days = 44 trips, ~15% commitment discount):**
  - LOW: 44 × 150 TL × 0.85 ≈ 5,610 TL ≈ **$117/seat-month**
  - MID: 44 × 185 TL × 0.85 ≈ 6,920 TL ≈ **$145/seat-month**
  - HIGH: 44 × 220 TL × 0.85 ≈ 8,230 TL ≈ **$172/seat-month**
- **Recommended DERIVED committed band: $120–170/seat-month, mid $145** — ≈7–9× the İstanbulkart cost of the same trips (time+comfort premium), ~20–25% of the taxi-commute alternative, and ~5–8% of a professional-tier (100–150K TRY/mo gross) income. Realistic for Istanbul, nothing Gulf-priced. **Flag for Jaideep confirmation.** [DERIVED]
### L2 — Spot seats
- IST-1 trunk spot: **175–220 TL ($3.7–4.6)/seat-leg** (full anchor, no discount). [DERIVED from FARE anchors]
- IST-2 Islands spot: **250–400 TL ($5.2–8.4)/seat-leg** — vs 114–206 TL existing fares for 2–4× the speed; summer peak at the top of band. [DERIVED]
- IST-3 comfort shuttle spot: **100–150 TL ($2.1–3.1)** — priced on comfort only, honest about no time win. [DERIVED]
### L3 — Experiences / charter (headline-adjacent in this market — tourism-weighted)
- Whole-vessel hourly anchor: private Bosphorus charter market clears **6,000–8,000+ TL/hr ($131–168/hr)** for conventional yachts [PRIMARY vendor listings — SU Yatçılık from 6,250 TL/hr; market band SECONDARY].
- N45 (20 seats, zero-emission, silent, low-wake — Bosphorus-appropriate at 10 kn displacement/low-foil) charter rate: **$300–450/hr DERIVED** (2–3× conventional-yacht hourly, justified by capacity+novelty; upper Bosphorus IST-4 water). Sunset/tour per-seat variant: **$25–45/seat** (vs mass tours far below, private charters far above). [DERIVED — flag]
- Demand context: 17.5M visitors 2025, 625K+ cruise pax at İstanbul ports (DEMAND file, SECONDARY) — labeled indicative.
### U1/U2 (upside-only, not sized): sponsorship (Galataport/marina brands); cargo — courier linehaul Islands class (car-free islands = genuine clean-logistics niche) — city-appropriate, note only.

## 3 · Cost-side inputs (from CREW + canon)
| Input | Value | Source/label |
|---|---|---|
| Crew, 2-person, loaded | LOW $16.8/hr · MID $23.4/hr; ≈2.5 rostered crews per 16-hr vessel → $8.2–11.4K/vessel-mo | CREW file — TURKEY-ADAPTED (statutory burden PRIMARY, wages SECONDARY, band DERIVED) |
| Energy tariff | 5.93 TL/kWh ex-tax (EPDK ticarethane >30 kWh/day, 4 Apr 2026) → **$0.149/kWh incl. tax uplift** — sourced local tariff used (< $0.30 canon). Overnight TOU 2.94 TL/kWh upside noted | CREW file §4 — SECONDARY transcription of EPDK, re-verify at epdk.gov.tr |
| **Energy per nm (N45)** | 4.1 kWh/nm × $0.149 = **$0.61/nm** | DERIVED (canon consumption × sourced tariff) |
| Maintenance | **$82.5K/yr N45-class** | CANON (per template scaling) |
| Network share | **10% of revenue** | CANON |
| Berthing | İBB/Şehir Hatları pier access or marina berth — **UNSOURCED this pass → placeholder only, must be sourced before any P&L** (Ataköy/Kalamış marina tariffs exist publicly — pull at model time) | UNSOURCED — fail closed |
| Insurance | Turkish hull/P&I market rate — **UNSOURCED → placeholder, fail closed** | UNSOURCED |
| Capex | $2.5M N45 | CANON |

## 4 · Line-level distance/energy quick table (NODES file, DERIVED)
| Line | Round trip nm | Energy $/RT (N45) |
|---|---|---|
| IST-1 full (Bakırköy↔Bostancı) | 25.2 | $15.4 |
| IST-1 short (Yenikapı↔Kadıköy) | 7.2 | $4.4 |
| IST-2 (Kadıköy↔Büyükada) | 19.0 | $11.6 |
| IST-3 (Karaköy↔Kadıköy) | 5.8 | $3.5 |
- Note energy is a rounding error next to crew — the binding constraints are the 10-kn strait cap (route design) and seat pricing vs local incomes.

## 5 · Fail-closed register (whole Istanbul pass)
1. Berthing & insurance costs — UNSOURCED → no P&L until sourced.
2. Weather-cancellation rate — assumption (5%), no primary statistic.
3. Existing-service journey times (ferry/road comparisons) — INDICATIVE, verify schedules before render.
4. Şehir Hatları official fare page & Deniz Taksi official tariff — verify at source before rendering TRY figures.
5. Adalar annual visitation, bridge crossing totals, marina capacities, İBB electric-ferry program status — UNSOURCED → excluded.
6. Licensing end-to-end sequence — DERIVED, confirm with İBB.
7. All TRY→USD at 47.76 (2026-08-16) — stale within weeks; re-pull.
