# CREW-COST-BENCHMARKS-BAHRAIN (internal audit file — does not render)

Researched 2026-08-16. Method: **BAHRAIN-ADAPTED** (BLS method not applicable, per international addendum). Peg: 1 BHD = USD 2.6596 (BHD 0.376/USD fixed).

## 1 · Wage evidence (captain / skipper)
| Evidence | BHD/month | Source | Tag |
|---|---|---|---|
| Naukrigulf "Boat Captain salary in Bahrain" survey range | 400–700 (avg ≈ 500) | https://www.naukrigulf.com/boat-captain-jobs-in-bahrain (salary insight) | SECONDARY (salary survey) |
| Job posting, tourism skipper/boat captain (BH social job boards, 2024–25) | 130–200 | Instagram/Facebook job-post listings (e.g., skipper BD130–150; fishing/leisure BD160–200) | SECONDARY (job postings, low-end informal segment) |
| Context: average private-sector salary of Bahrainis | 892 | Ministry of Labour via newsofbahrain.com/bahrain/131119.html | SECONDARY (news report of official figure) |
| LMRA/SIO occupational wage dataset (data.gov.bh) | 2016 vintage — too dated to anchor | https://www.data.gov.bh (Workers by Monthly Wage Groups & Occupation) | PRIMARY but stale — not used |

**Selected captain benchmark (licensed passenger-vessel master, Decree 32/2020 master licence):** LOW **BHD 450**/mo, MID **BHD 650**/mo. Rationale (DERIVED): a licensed master for a 20-pax scheduled foiling service sits above the informal leisure-skipper market (BD130–200) and at/above the Naukrigulf survey mid-to-top (BD400–700); MID set near survey top because scheduled passenger ops + foil systems demand the top of the local market.

## 2 · Wage evidence (deckhand / able seaman)
| Evidence | BHD/month | Source | Tag |
|---|---|---|---|
| Gulf manpower agency rate cards, able seaman Bahrain | ≈ 310–430 | Gulf crewing agency listings (Mahad group etc.) | SECONDARY |
| Job postings, deckhand/marina hand | 180–250 | BH job boards/social postings | SECONDARY |

**Selected deckhand benchmark:** LOW **BHD 200**/mo, MID **BHD 325**/mo (DERIVED from the two SECONDARY bands above).

## 3 · Burden (explicit, Bahrain-customary)
Applied multiplier: **×1.35** on base wage (DERIVED, assumptions stated):
- GOSI social insurance, employer share (expat ~3% + injury; Bahraini higher — mixed-crew assumption) — official schedule not re-pulled this pass (flag).
- LMRA work-permit fees ~BHD 5–10/mo equivalent + visa/renewal amortized.
- Medical insurance (mandatory for expats), uniform/training.
- Housing/food allowances customary in Gulf marine employment for junior crew (partial — assume captain package all-in, deckhand +BHD 50–75 allowance).
All components bundled into the single 1.35 factor; not separately sourced — **DERIVED, flag for finance review**.

## 4 · Loaded crew cost — 2-person crew (1 captain + 1 deckhand)
Hours basis: 48-hr week ≈ **208 paid hrs/month** per person (DERIVED, Bahrain norm is 48h/wk private sector).

| Scenario | Base BHD/mo (2 crew) | ×1.35 loaded BHD/mo | USD/mo | **USD/hr (crew pair)** |
|---|---|---|---|---|
| LOW (450+200) | 650 | 878 | $2,334 | **$11.2/hr** |
| MID (650+325) | 975 | 1,316 | $3,501 | **$16.8/hr** |

**Per 16-hr service day (two 8-hr crew shifts, i.e., 2 crew-pairs staffed):** LOW ≈ **$180/service-day**, MID ≈ **$269/service-day** (16 crew-pair-hours × rate). DERIVED.

Comparison note (do not render): this is ~5–8× cheaper than US benchmarks (Boston loaded ~$85–110/hr pair) — Bahrain's crew line will be a minor opex item; energy and maintenance dominate.

## 5 · EWA commercial electricity tariff (PRIMARY-verified)
Source: https://www.ewa.bh/en/tariff (Electricity & Water Authority official tariff page) — **PRIMARY**.
- **Non-domestic (commercial) electricity:** **22 fils/kWh** for first 5,000 kWh/mo; **32 fils/kWh** above 5,000 kWh/mo.
- USD at peg: 22 fils = **$0.0585/kWh**; 32 fils = **$0.0851/kWh**.
- A single N45 in service (~4.1 kWh/nm × >100 nm/day) exceeds 5,000 kWh/mo in week one → **marginal tariff 32 fils = $0.0851/kWh** is the correct planning number. Per addendum rule ("use sourced local tariff if cheaper than $0.30/kWh"): **use $0.0851/kWh, cited EWA**. Note: EWA tariffs are politically administered; re-verify at proposal time.
- Not yet verified: any dedicated marina/shore-power resale markup at berth (marina operators may resell above EWA tariff) — **UNSOURCED, flag**; use EWA commercial + 20% contingency in sensitivity only.

## 6 · Fail-closed list (this file)
1. GOSI employer-contribution schedule — not re-pulled; bundled in 1.35 burden (DERIVED).
2. Marina shore-power resale rate — UNSOURCED.
3. No Bahrain-specific licensed "foiling vessel master" wage market exists — premium over local top-of-market may be needed for first crews (train-up assumption, not priced).
