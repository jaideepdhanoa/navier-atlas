# CREW-COST-BENCHMARKS-ISTANBUL
Internal research record — audit language, never renders. Method: TURKEY-ADAPTED (BLS OEWS not applicable). Date: 2026-08-16.
**FX: 47.76 TRY/USD** (TCMB indicative mid — buying 47.7206 / selling 47.8066, retrieved 2026-08-16 from tcmb.gov.tr today.xml). TRY is volatile: every TRY figure below is dated; re-pull FX before any regeneration.

## 1 · Statutory floor & burden (2026)
- **Minimum wage 01/01–31/12/2026:** gross **33,030.00 TRY/mo**; net 28,075.50 TRY/mo. [PRIMARY — T.C. Çalışma ve Sosyal Güvenlik Bakanlığı: https://www.csgb.gov.tr/poco-pages/asgari-ucret/]
- **Employer burden (same source, PRIMARY):**
  - SGK employer share **20.75%** standard (shown as 21.75% incl. variants in the ministry table; 5510 s.81(ı) gives a 5-point treasury discount → 15.75% for qualifying employers; table shows 16.75%/19.75% variants with discounts)
  - Employer unemployment insurance **2%**
  - Ministry's own all-in example without discount: gross 33,030 → total employer cost **40,874.63 TRY** → **burden multiplier ≈ 1.2375** on gross. With 5-point discount: 39,223.13 → ≈1.1875.
- **Modeling choice:** use **1.2375** (no-discount, conservative). [PRIMARY-derived]
- Severance accrual (kıdem tazminatı, ~1 month gross/yr ≈ +8.3%) and meal/transport allowances customary in Turkish employment are NOT in the multiplier; add explicit **+10% allowance line** → **effective loaded multiplier 1.36** (DERIVED, assumption stated).

## 2 · Wage benchmarks — captain & deckhand (coastal, Turkish-flag)
No TUİK occupation-level maritime wage table was captured this pass (TUİK publishes sectoral labour cost indices, not captain/deckhand rows) — postings/aggregator method used instead, labeled SECONDARY.
- Turkish-flag **coastal vessel postings band (2026): 61,000–215,000 TRY/mo** across ratings→masters. [SECONDARY — denizcilikakademisi.com/gemiadami-maaslari]
- **Captain:** private-sector estimate 56,151–84,227 TRY/mo [SECONDARY — ikuz.com.tr/kaptan-maasi]; "kaptan yardımcısı" (chief mate) average 123,630 TRY/mo [SECONDARY — kariyer.net pozisyonlar/kaptan+yardimcisi/maas — skewed by oceangoing; treat as upper bound for a harbor master ticket]. Deep-sea USD scales (3,600–15,000 USD/mo) explicitly EXCLUDED — wrong segment.
- **Deckhand (gemici):** floor = minimum wage 33,030 TRY; coastal postings start ~61,000 TRY denizcilikakademisi band incl. ratings. [SECONDARY]

### Selected gross bands (harbor/commuter craft, 2-person crew) — DERIVED from above
| Role | LOW (TRY/mo gross) | MID (TRY/mo gross) |
|---|---|---|
| Captain (yakın kıyı ticket) | 75,000 | 105,000 |
| Deckhand (gemici) | 40,000 | 55,000 |
| **Crew of 2, gross** | **115,000** | **160,000** |

## 3 · Loaded cost (2-person crew)
Loaded = gross × 1.2375 (statutory, PRIMARY-derived) × 1.10 (severance+allowances, DERIVED) = ×1.36.
| | LOW | MID |
|---|---|---|
| Loaded TRY/mo | 156,400 | 217,600 |
| Loaded USD/mo @47.76 | **$3,275** | **$4,556** |
| Loaded USD/hr (÷195 h/mo per rostered crew: 45 h statutory week × 4.33) | **$16.8/hr** | **$23.4/hr** |

- A 16-hr service day, 7 days (≈480 vessel-hours/mo) needs ≈ **2.5 rostered 2-person crews per vessel** (480/195, DERIVED) → crew cost per vessel-month: LOW ≈ $8.2K, MID ≈ $11.4K.
- Cross-check: MID all-in ≈ 6.6× minimum-wage employer cost per head for the captain — plausible for a licensed master in Istanbul's market. [DERIVED sanity check]
- Method label: **TURKEY-ADAPTED** — statutory burden PRIMARY, wage points SECONDARY (postings), bands DERIVED. Flag for Jaideep confirmation before any economics render.

## 4 · Energy — commercial electricity tariff
- **EPDK tariff (effective 4 Apr 2026), Ticarethane (commercial):** 5.35 TL/kWh (≤30 kWh/day) / **5.93 TL/kWh (>30 kWh/day)** excl. taxes; industrial LV single-time 4.81 TL/kWh; time-of-use night (23:00–08:00) 2.94 TL/kWh. [SECONDARY transcription of EPDK tariff — piagrid.com/indirimli-elektrik/elektrik-fiyati, "Kaynak: EPDK, 4 Nisan 2026"; PRIMARY table lives at epdk.gov.tr "Elektrik Faturalarına Esas Tarife Tabloları" — re-verify numbers there before render]
- A charging operation draws ≫30 kWh/day → **5.93 TL/kWh ex-tax**; +20% VAT & funds ≈ **7.12 TL/kWh ≈ $0.149/kWh** (DERIVED, @47.76, tax uplift assumption stated).
- **$0.149/kWh < $0.30 canon → use the sourced local tariff** (addendum rule). Overnight TOU charging at 2.94 TL/kWh (≈$0.074/kWh incl. tax uplift ≈ $0.089) is a real upside lever — note only, base case uses 5.93.
- **Energy per nm:** N45 4.1 kWh/nm × $0.149 = **$0.61/nm** (base) · N30 1.6 kWh/nm × $0.149 = $0.24/nm. [DERIVED — canon consumption × sourced tariff]

## 5 · Fail-closed list (crew file)
- TUİK captain/deckhand wage rows: not found → not used.
- Collective agreements (e.g., Şehir Hatları union scale): not captured → not used; would be a better MID anchor if published.
- Distribution-company-specific İstanbul tariff (BEDAŞ/AYEDAŞ) vs national EPDK table: assumed identical (national tariff) — verify at EPDK table before render.
