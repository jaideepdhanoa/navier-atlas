# CREW-COST-ABU-DHABI — method: UAE-ADAPTED (internal audit file — never renders)

BLS OEWS method not applicable (no UAE coverage). Per INTERNATIONAL-ADDENDUM: sourced UAE maritime wage benchmarks + explicit UAE burden assumptions, same structure as dubai/CREW-COST-DUBAI.md. FX peg 3.6725 AED/USD (canon). All sources accessed 2026-08-16.

## 1 · Base wage benchmarks (AED/month, sourced)

**Captain / Master (commercial small-passenger class):**
| Source | Figure | Use |
|---|---|---|
| NaukriGulf, "Yacht Captain salary in UAE" — https://www.naukrigulf.com/salaries/yacht-captain-salary-in-uae | avg **AED 7,725**/mo; range **AED 4,000–18,500** | LOW base = 7,725; MID base = 11,250 (DERIVED: midpoint of sourced range — commercial Master's-permit work sits above the small-charter average). **UAE-wide source, labeled** — no Abu Dhabi row at commercial passenger tier found |
| NaukriGulf, Boat Captain in Abu Dhabi — https://www.naukrigulf.com/salaries/boat-captain-salary-in-abu-dhabi | avg AED 4,304 (2,500–5,500) | cross-check only — EXCLUDED from math (small-craft/utility tier, below commercial passenger-vessel standard) |
| Indeed UAE, Boat Captain in Abu Dhabi — https://ae.indeed.com/career/boat-captain/salaries/Abu-Dhabi | range AED 1,308–8,321; UAE table shows AD avg ~AED 3,299 | cross-check only — EXCLUDED (abra/small-craft tier) |
| Glassdoor AD boat captain — https://www.glassdoor.com/Salaries/abu-dhabi-abu-dhabi-boat-captain-salary-SRCH_IL.0,19_IC2203308_KO20,32.htm | implausible low outliers | EXCLUDED — sample too thin |

**Deckhand / Seaman:**
| Source | Figure | Use |
|---|---|---|
| Indeed, Deckhand in Abu Dhabi — https://ae.indeed.com/career/deckhand/salaries/Abu-Dhabi | range **AED 2,269–3,808**/mo (AD avg shown elsewhere as ~2,939) | LOW base = **3,039** (DERIVED: midpoint of the Abu Dhabi sourced range) |
| Indeed UAE, Deckhand — https://ae.indeed.com/career/deckhand/salaries | avg **AED 3,365** (2,224–5,092) | MID base = 3,365 (UAE-wide average, labeled — sits above the AD midpoint, consistent with commercial-passenger premium) |
| NaukriGulf, Deck Hand in Abu Dhabi — https://www.naukrigulf.com/salaries/deck-hand-salary-in-abu-dhabi | AED 2,000–3,000 (avg 2,250–2,750) | cross-check (slightly below Indeed AD; consistent) |

## 2 · Burden stack (explicit; identical structure to Dubai file)

All four burden items are **ASSUMPTIONS**, stated for audit; standard UAE employment structure (allowance-heavy packages, statutory gratuity, employer-paid visa & medical insurance):

| Item | Rate | Basis |
|---|---|---|
| Housing allowance | +25% of base | customary UAE allowance for marine/hospitality staff — ASSUMPTION |
| Transport allowance | +10% of base | customary — ASSUMPTION |
| End-of-service gratuity accrual | +5.75% of base | statutory 21 days' basic pay/yr (first 5 yrs), UAE Labour Law |
| Medical insurance + visa/work-permit amortized | AED 395.83/mo/head | ASSUMPTION anchored to typical basic-plan and 2-yr-visa costs (AED 3,000/yr + 1,750/yr) |

Loaded monthly = base × 1.4075 + 395.83 per head. Hours basis: UAE standard 48-hr week ⇒ **208 paid hrs/mo per crew member**; 2-person crew (Master + Seaman, DMA/Abu Dhabi Maritime-permitted per applicable manning rules). 16-hr service days require two shift teams; cost per *operated* hour is unchanged (each staffed hour is paid once).

## 3 · Loaded cost, 2-person crew

| Case | Captain base | Deckhand base | Loaded AED/mo (crew) | AED/hr | **USD/hr** |
|---|---|---|---|---|---|
| **LOW** (UAE survey avg captain + AD-range midpoint deckhand) | 7,725 | 3,039 | 15,942 | 76.64 | **$20.87** |
| **MID** (range-midpoint commercial premium captain + UAE avg deckhand) | 11,250 | 3,365 | 21,362 | 102.70 | **$27.97** |

Arithmetic (LOW): (7,725 × 1.4075 + 395.83) + (3,039 × 1.4075 + 395.83) = 15,941.9 AED/mo ÷ 208 = 76.64 AED/hr ÷ 3.6725 = $20.87/hr.

**Model value used in REVENUE-STACK-ABU-DHABI: $30/hr** (MID rounded up as buffer for overtime/split-shift premia on the 16-hr day — same treatment as Dubai's $30/hr on MID $29.10; the two markets land within ~4% of each other, as expected for a single national labor market).

Context: ~30–40% of the Boston loaded benchmark (LOW $67 / MID $77/hr, boston/CREW-COST-BENCHMARKS.md) — labor is the structurally cheap line in UAE marine opex. No unlabeled numbers above; every base wage is a live salary page; burden is explicitly assumed.
