# CREW-COST-RAS-AL-KHAIMAH — method: UAE-ADAPTED (internal audit file — never renders)

BLS OEWS method not applicable (no UAE coverage). Per INTERNATIONAL-ADDENDUM: sourced UAE maritime wage benchmarks + explicit UAE burden assumptions, same structure as dubai/CREW-COST-DUBAI.md. FX peg 3.6725 AED/USD (canon). All sources accessed 2026-08-16.

**RAK-specific note:** searches for RAK / northern-emirates rows (Indeed "deckhand Ras Al Khaimah", NaukriGulf "boat captain Ras Al Khaimah") returned **no usable salary pages this run**. Northern-emirates wages are commonly assumed cheaper than Dubai/AD, but **no discount is claimed here because none was sourced** — UAE-wide benchmarks are used, labeled. Marine labor is a single national market (crew routinely commute between emirates), so UAE-wide rows are a defensible basis.

## 1 · Base wage benchmarks (AED/month, sourced — UAE-wide, labeled)

**Captain / Master (commercial small-passenger class):**
| Source | Figure | Use |
|---|---|---|
| NaukriGulf, "Yacht Captain salary in UAE" — https://www.naukrigulf.com/salaries/yacht-captain-salary-in-uae | avg **AED 7,725**/mo; range **AED 4,000–18,500** | LOW base = 7,725; MID base = 11,250 (DERIVED: midpoint of sourced range — commercial Master's-permit work sits above the small-charter average). UAE-wide, labeled |
| GulfTalent — https://www.gulftalent.com/uae/salaries/boat-captain | avg AED 5,000 (500–6,000) | cross-check only (skews to small utility craft) |
| Indeed UAE, Boat Captain — https://ae.indeed.com/career/boat-captain/salaries | avg AED 3,060 | cross-check only — EXCLUDED (abra/utility tier, below commercial passenger-vessel standard) |

**Deckhand / Seaman:**
| Source | Figure | Use |
|---|---|---|
| Indeed UAE, Deckhand — https://ae.indeed.com/career/deckhand/salaries | avg **AED 3,365** (2,224–5,092) | LOW base = 3,365; MID base = 3,365 (UAE-wide average used for both — no RAK row found; MID premium is carried on the captain side only) |
| NaukriGulf, Deck Hand (AD row, nearest comparator) — https://www.naukrigulf.com/salaries/deck-hand-salary-in-abu-dhabi | AED 2,000–3,000 | cross-check (below Indeed UAE avg; consistent — using 3,365 is conservative-high) |

## 2 · Burden stack (explicit; identical structure to Dubai/AD files)

All four burden items are **ASSUMPTIONS**, stated for audit; standard UAE employment structure (allowance-heavy packages, statutory gratuity, employer-paid visa & medical insurance):

| Item | Rate | Basis |
|---|---|---|
| Housing allowance | +25% of base | customary UAE allowance for marine/hospitality staff — ASSUMPTION |
| Transport allowance | +10% of base | customary — ASSUMPTION |
| End-of-service gratuity accrual | +5.75% of base | statutory 21 days' basic pay/yr (first 5 yrs), UAE Labour Law |
| Medical insurance + visa/work-permit amortized | AED 395.83/mo/head | ASSUMPTION anchored to typical basic-plan and 2-yr-visa costs (AED 3,000/yr + 1,750/yr) |

Loaded monthly = base × 1.4075 + 395.83 per head. Hours basis: UAE standard 48-hr week ⇒ **208 paid hrs/mo per crew member**; 2-person crew (Master + Seaman, licensed per RAKTA's Executive Regulation of Law 13/2023 — manning schedule to be confirmed with RAKTA; federal small-passenger norms assumed). 16-hr service days require two shift teams; cost per *operated* hour is unchanged (each staffed hour is paid once).

## 3 · Loaded cost, 2-person crew

| Case | Captain base | Deckhand base | Loaded AED/mo (crew) | AED/hr | **USD/hr** |
|---|---|---|---|---|---|
| **LOW** (UAE survey averages) | 7,725 | 3,365 | 16,401 | 78.85 | **$21.47** |
| **MID** (range-midpoint commercial premium captain + UAE avg deckhand) | 11,250 | 3,365 | 21,362 | 102.70 | **$27.97** |

Arithmetic (LOW): (7,725 + 3,365) × 1.4075 + 2 × 395.83 = 15,609.2 + 791.7 = 16,400.9 AED/mo ÷ 208 = 78.85 AED/hr ÷ 3.6725 = $21.47/hr. (Script-verified 2026-08-16.)

**Model value used in REVENUE-STACK-RAS-AL-KHAIMAH: $30/hr** (MID rounded up as buffer for overtime/split-shift premia on the 16-hr day — same treatment as Dubai [$30 on MID $29.10] and Abu Dhabi [$30 on MID $27.97]). The three UAE markets land within ~4% of each other on identical national sources, as expected.

Context: ~30–40% of the Boston loaded benchmark (LOW $67 / MID $77/hr, boston/CREW-COST-BENCHMARKS.md) — labor is the structurally cheap line in UAE marine opex. No unlabeled numbers above; every base wage is a live salary page; burden is explicitly assumed; the absence of RAK-local rows is stated rather than papered over.
