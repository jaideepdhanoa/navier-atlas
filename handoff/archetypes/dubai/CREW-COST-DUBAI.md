# CREW-COST-DUBAI — method: UAE-ADAPTED (internal audit file — never renders)

BLS OEWS method not applicable (no UAE coverage). Per INTERNATIONAL-ADDENDUM: sourced UAE maritime wage benchmarks + explicit UAE burden assumptions. FX peg 3.6725 AED/USD (canon). All sources accessed 2026-08-16.

## 1 · Base wage benchmarks (AED/month, sourced)

**Captain / Master (commercial small-passenger class):**
| Source | Figure | Use |
|---|---|---|
| NaukriGulf, "Yacht Captain salary in UAE" — https://www.naukrigulf.com/salaries/yacht-captain-salary-in-uae | avg **AED 7,725**/mo; range **AED 4,000–18,500** | LOW base = 7,725; MID base = 11,250 (DERIVED: midpoint of sourced range — commercial DMA Master's-permit work sits above the small-charter average) |
| GulfTalent — https://www.gulftalent.com/uae/salaries/boat-captain | avg AED 5,000 (500–6,000) | cross-check (skews to small workboats) |
| Indeed UAE, Boat Captain — https://ae.indeed.com/career/boat-captain/salaries | avg AED 3,060 (1,414–6,624) | cross-check only — EXCLUDED from math (captures abra/workboat tier, below commercial passenger-vessel standard) |
| SalaryExpert Dubai — https://www.salaryexpert.com/salary/job/boat-captain/united-arab-emirates/dubai | AED 278,707/yr (~23.2K/mo) | EXCLUDED — modeled estimate, not survey |
| yacrew.com posting, 42 m private yacht Dubai — https://www.yacrew.com/i57452/private-yacht-captain-permanent-dubai/ | AED 38,000/mo | EXCLUDED — superyacht class, wrong vessel class; cited as ceiling context |

**Deckhand / Seaman:**
| Source | Figure | Use |
|---|---|---|
| Indeed UAE, Deckhand — https://ae.indeed.com/career/deckhand/salaries | avg **AED 3,365** (2,224–5,092) | LOW base = 3,365 |
| Indeed Dubai, Deckhand — https://ae.indeed.com/career/deckhand/salaries/Dubai | avg AED 3,655; range **2,399–5,567** | MID base = 3,983 (DERIVED: midpoint of Dubai sourced range) |
| Indeed, Dubai Yachting Company deckhands — https://ae.indeed.com/cmp/Dubai-Yachting-Company/salaries/Deckhand | AED 3,881 | cross-check (consistent with MID) |

## 2 · Burden stack (explicit; UAE marine employment customary items)

Applied to base salary unless noted. All four burden items are **ASSUMPTIONS** — stated so they can be audited; component logic follows standard UAE employment structure (allowance-heavy packages, statutory gratuity, employer-paid visa & medical insurance):

| Item | Rate | Basis |
|---|---|---|
| Housing allowance | +25% of base | customary UAE allowance for marine/hospitality staff — ASSUMPTION |
| Transport allowance | +10% of base | customary — ASSUMPTION |
| End-of-service gratuity accrual | +5.75% of base | statutory 21 days' basic pay/yr (first 5 yrs), UAE Labour Law — formula standard; statute not separately loaded this run |
| Medical insurance (mandatory in Dubai) + visa/work-permit amortized | AED 3,000/yr + AED 1,750/yr per head (= AED 395.8/mo/head) | ASSUMPTION anchored to typical basic-plan and 2-yr-visa costs |

Loaded monthly = base × 1.4075 + 395.83 per head. Hours basis: UAE standard 48-hr week ⇒ **208 paid hrs/mo per crew member**; a 2-person crew (Master + Seaman, both DMA-permitted — Minimum Safe Manning per ECR 9/2020) delivers 208 staffed vessel-hours/mo per shift team. 16-hr service days therefore require two shift teams; cost per *operated* hour is unchanged (each staffed hour is paid once).

## 3 · Loaded cost, 2-person crew

| Case | Captain base | Deckhand base | Loaded AED/mo (crew) | AED/hr | **USD/hr** |
|---|---|---|---|---|---|
| **LOW** (survey averages) | 7,725 | 3,365 | 16,401 | 78.85 | **$21.47** |
| **MID** (range midpoints, commercial premium) | 11,250 | 3,983 | 22,232 | 106.89 | **$29.10** |

Arithmetic (LOW): (7,725+3,365) × 1.4075 + 2 × 395.83 = 15,609.2 + 791.7 = 16,400.9 AED/mo ÷ 208 = 78.85 AED/hr ÷ 3.6725 = $21.47/hr.

**Model value used in REVENUE-STACK-DUBAI: $30/hr** (MID rounded up as buffer for overtime/split-shift premia on the 16-hr day).

Context: this is ~35–45% of the Boston loaded benchmark (LOW $67 / MID $77/hr, boston/CREW-COST-BENCHMARKS.md) — labor is the structurally cheap line in Dubai marine opex; energy and berthing follow the same pattern. No unlabeled numbers above; every base wage is a real loaded page; burden is explicitly assumed.
