# Boston, MA small commercial ferry crew-cost benchmarks

**As of:** 2026-08-15  
**Status:** Source-backed benchmark; Boston metro/state figures below are from the latest directly validated local OEWS tables (May 2023), while the latest directly readable national OEWS profiles are May 2025. The 2025 profile fetch did not expose a readable Boston/MA row, so local calculations use May 2023. Boston metro is Boston-Cambridge-Nashua, MA-NH (the OEWS metro includes parts of New Hampshire). The modeled crew is one licensed captain/master (SOC 53-5021 proxy) plus one deckhand (SOC 53-5011 proxy).

## Sources

All OEWS wage figures below are hourly dollars. BLS's table columns are **median hourly wage** and **mean hourly wage**. The direct BLS pages describe the estimates as covering all industry sectors; they do not isolate Subchapter T passenger-ferry employers.

| Source | Geography | Occupation | Wage | Year / date | URL |
|---|---|---|---|---|---|
| U.S. Bureau of Labor Statistics, OEWS May 2023 metro table | Boston-Cambridge-Nashua, MA-NH | Captains, Mates, and Pilots of Water Vessels (SOC 53-5021) | Median **$29.64/hr**; mean **$33.29/hr** | May 2023 (page last modified Apr. 3, 2024) | https://www.bls.gov/oes/2023/may/oes_71650.htm |
| U.S. Bureau of Labor Statistics, OEWS May 2023 metro table | Boston-Cambridge-Nashua, MA-NH | Sailors and Marine Oilers (SOC 53-5011; deckhand proxy) | Median **$17.42/hr**; mean **$20.69/hr** | May 2023 (page last modified Apr. 3, 2024) | https://www.bls.gov/oes/2023/may/oes_71650.htm |
| U.S. Bureau of Labor Statistics, OEWS May 2023 state table | Massachusetts (nearest state-level coverage; Boston is separately available above) | Captains, Mates, and Pilots of Water Vessels (SOC 53-5021) | Median **$29.73/hr**; mean **$34.20/hr** | May 2023 (page last modified Apr. 3, 2024) | https://www.bls.gov/oes/2023/may/oes_ma.htm |
| U.S. Bureau of Labor Statistics, OEWS May 2023 state table | Massachusetts | Sailors and Marine Oilers (SOC 53-5011; deckhand proxy) | Median **$17.45/hr**; mean **$20.85/hr** | May 2023 (page last modified Apr. 3, 2024) | https://www.bls.gov/oes/2023/may/oes_ma.htm |
| U.S. Bureau of Labor Statistics, OEWS occupation profile | United States | Captains, Mates, and Pilots of Water Vessels (SOC 53-5021) | Median **$42.66/hr**; mean **$47.03/hr**; 90th percentile **$77.65/hr** | May 2023 (page last modified Apr. 3, 2024) | https://www.bls.gov/oes/2023/may/oes535021.htm |
| U.S. Bureau of Labor Statistics, OEWS occupation profile | United States | Sailors and Marine Oilers (SOC 53-5011) | Median **$23.27/hr**; mean **$25.71/hr**; 90th percentile **$38.07/hr** | May 2023 (page last modified Apr. 3, 2024) | https://www.bls.gov/oes/2023/may/oes535011.htm |
| U.S. Bureau of Labor Statistics, OEWS May 2025 occupation profile | United States | Captains, Mates, and Pilots of Water Vessels (SOC 53-5021) | Median **$44.45/hr**; mean **$49.87/hr**; 90th percentile **$82.04/hr** | May 2025; profile retrieved Aug. 15, 2026 | https://data.bls.gov/oesprofile/?major_group=530000&occupation=535021&measure=01&areas=INDUSTRY,STATE,MSA |
| U.S. Bureau of Labor Statistics, OEWS May 2025 occupation profile | United States | Sailors and Marine Oilers (SOC 53-5011) | Median **$24.77/hr**; mean **$27.32/hr**; 90th percentile **$40.20/hr** | May 2025; profile retrieved Aug. 15, 2026 | https://data.bls.gov/oesprofile/?major_group=530000&occupation=535011&measure=01&areas=INDUSTRY,STATE,MSA |
| BLS Employer Costs for Employee Compensation (ECEC), private industry | United States, private industry (sector benchmark; not marine-specific) | Employer burden benchmark | Total compensation **$46.60/hr**; wages and salaries **$32.60/hr**; benefits **$14.01/hr** (benefits were 30.1% of total) | March 2026; release June 12, 2026 | https://www.bls.gov/news.release/ecec.nr0.htm |
| Charles River Boat Company careers page | Boston/Cambridge area operator | Boat Captain | 50-ton license **$25–$30/hr + gratuities**; 100-ton license **$35–$38/hr + gratuities** | Page retrieved Aug. 15, 2026; no posting date shown | https://charlesriverboat.com/jobs/ |
| Boston Harbor City Cruises, Deckhand (Onboard Guest Services) listing | Boston | Deckhand / onboard guest services | Starting pay **$16/hr** | Listing displayed “1 week ago” when retrieved Aug. 15, 2026 | https://talents.vaia.com/jobs/deckhand-onboard-guest-services-boston-harbor-city-cruises/ |
| Indeed Boston deckhand search (job-board corroboration; listing names Odyssey & Spirit of Boston/Hornblower) | Boston | Deckhand | **$16/hr** | Search result retrieved Aug. 15, 2026; posting date not visible | https://www.indeed.com/q-deckhand-l-boston,-ma-jobs.html |
| Indeed Boston boat-captain search (job-board corroboration; listing names Boston Harbor City Cruises/Hornblower) | Boston | Captain | **$22–$28/hr** for Captain – Boston Harbor City Cruises | Search result retrieved Aug. 15, 2026; posting date not visible | https://www.indeed.com/q-boat-captain-l-boston,-ma-jobs.html |
| Indeed Massachusetts ferry-captain search (job-board corroboration; listing names Odyssey & Spirit of Boston/Hornblower) | Boston | Ferry/passenger-vessel captain | **$30–$35/hr** | Search result retrieved Aug. 15, 2026; posting date not visible | https://www.indeed.com/q-ferry-captain-l-massachusetts-jobs.html |

**Local-posting interpretation.** The operator pages are direct market corroboration, not substitutes for OEWS. Indeed results are aggregates and can be stale or change; gratuities in the Charles River listing are excluded from the base-wage calculations below. The Boston Harbor City Cruises deckhand listing is onboard guest services and may not have the same technical duties as a Subchapter T deckhand.

## Loaded-cost computation (two people, per operating hour)

### Burden multiplier

Use the BLS ECEC private-industry benchmark because a commercial passenger operator is generally a private employer, while noting that ECEC is not marine-specific and is a U.S.-wide sector benchmark:

```text
Multiplier = total compensation / wages and salaries
           = $46.60 / $32.60
           = 1.4294 (use 1.43x when rounded)
```

This is a **total-employer-compensation** multiplier: it captures the ECEC wage-plus-benefit relationship, including benefits such as paid leave, insurance, retirement, and legally required benefits. It is not a marine-insurance premium or a substitute for an operator-specific workers-compensation/P&I quote.

### Scenarios

The required crew formula is:

```text
loaded crew cost per operating hour
  = (captain base wage + deckhand base wage) × 1.4294
```

The LOW and MID cases use the directly published Boston metro OEWS median and mean, respectively (both May 2023, the latest directly validated local rows). HIGH is an explicit upper-tail stress case using the latest official national OEWS 90th-percentile hourly figures (May 2025; not a Boston point estimate); this avoids inventing a Boston percentile that is not visible in the directly validated metro table.

| Case | Captain base wage | Deckhand base wage | Base two-person wage | Math using 1.4294x | Loaded crew cost / operating hour |
|---|---:|---:|---:|---:|---:|
| **LOW — Boston metro median (2023)** | $29.64/hr | $17.42/hr | $47.06/hr | $47.06 × 1.4294 | **$67.27/hr (about $67/hr)** |
| **MID — Boston metro mean (2023)** | $33.29/hr | $20.69/hr | $53.98/hr | $53.98 × 1.4294 | **$77.16/hr (about $77/hr)** |
| **HIGH — national OEWS 90th-percentile stress case (2025; not Boston-specific)** | $82.04/hr | $40.20/hr | $122.24/hr | $122.24 × 1.4294 | **$174.73/hr (about $175/hr)** |

For local reality-checking, the Charles River posting's upper 100-ton base ($38/hr) plus the Boston Harbor City Cruises deckhand listing's $16/hr starting base would be $54/hr before burden, or **$77.19/hr** at the same multiplier. That posting-based check excludes gratuities and is not used as the headline HIGH case because job postings are not a standardized percentile series.

## Caveats

- A ~16-hour operating day can require two crews or split shifts; this report gives only a per-operating-hour crew cost and does **not** schedule-model that requirement.
- Overtime, split-shift rules, seasonal demand/scarcity, union or contractor terms, and route- or credential-specific premiums can raise actual cost. A 100-ton master requirement may price differently from the broad SOC proxy.
- SOC 53-5011 is a defensible BLS proxy for a deckhand, but it includes sailors and marine oilers and is not limited to Subchapter T passenger vessels.
- OEWS covers employee wages across all industries in the geography and does not isolate a 45-ft/20-passenger fast ferry. Boston metro geography includes NH; Massachusetts state figures are supplied as a cross-check, not silently substituted. The local calculation year is May 2023 because the readable May 2025 profile did not expose a local Boston/MA row; the national comparison/high stress case is May 2025.
- The ECEC multiplier is U.S. private-industry average compensation burden, not a marine-specific loaded-cost factor. Employer payroll taxes, benefits, workers' compensation, maritime/P&I insurance, training, and paid non-operating time may differ materially; the burden benchmark should be replaced with operator-specific data when available.
- Job-board listings are time-sensitive. The retrieval date is recorded above; where no posting date was visible, no posting date is asserted. Gratuities are excluded from all calculations.
