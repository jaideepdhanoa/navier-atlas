# San Diego, CA small commercial ferry crew-cost benchmarks

**As of:** 2026-08-16
**Status:** Source-backed benchmark following the Boston method exactly (see `../boston/CREW-COST-BENCHMARKS.md`): BLS OEWS metro medians/means for a captain (SOC 53-5021 proxy) + deckhand (SOC 53-5011 proxy), × 1.4294 ECEC burden, × ~3%/yr wage drift to 2026. The latest directly validated local OEWS tables are **May 2023**; the metro is **San Diego-Chula Vista-Carlsbad, CA** (BLS area 41740) — the exact metro containing every network stop. California state rows are supplied as a cross-check, not silently substituted. The modeled crew is one licensed captain/master plus one deckhand.

## Sources

All OEWS wage figures are hourly dollars; table columns are **median hourly wage** and **mean hourly wage**. The estimates cover all industry sectors; they do not isolate Subchapter T passenger-ferry employers.

| Source | Geography | Occupation | Wage | Year / date | URL |
|---|---|---|---|---|---|
| U.S. Bureau of Labor Statistics, OEWS May 2023 metro table | San Diego-Chula Vista-Carlsbad, CA | Captains, Mates, and Pilots of Water Vessels (SOC 53-5021) | Median **$33.66/hr**; mean **$36.89/hr** (employment 270) | May 2023 | https://www.bls.gov/oes/2023/may/oes_41740.htm |
| U.S. Bureau of Labor Statistics, OEWS May 2023 metro table | San Diego-Chula Vista-Carlsbad, CA | Sailors and Marine Oilers (SOC 53-5011; deckhand proxy) | Median **$21.03/hr**; mean **$22.63/hr** (employment 240) | May 2023 | https://www.bls.gov/oes/2023/may/oes_41740.htm |
| U.S. Bureau of Labor Statistics, OEWS May 2023 state table | California (cross-check) | Captains, Mates, and Pilots of Water Vessels (SOC 53-5021) | Median **$34.03/hr**; mean **$43.90/hr** | May 2023 | https://www.bls.gov/oes/2023/may/oes_ca.htm |
| U.S. Bureau of Labor Statistics, OEWS May 2023 state table | California (cross-check) | Sailors and Marine Oilers (SOC 53-5011) | Median **$24.46/hr**; mean **$29.61/hr** | May 2023 | https://www.bls.gov/oes/2023/may/oes_ca.htm |
| U.S. Bureau of Labor Statistics, OEWS May 2025 occupation profile (national; as recorded in `../boston/CREW-COST-BENCHMARKS.md`, retrieved 2026-08-15; not re-pulled this pass) | United States | Captains, Mates, and Pilots of Water Vessels (SOC 53-5021) | Median $44.45/hr; mean $49.87/hr; **90th percentile $82.04/hr** | May 2025 | https://data.bls.gov/oesprofile/?major_group=530000&occupation=535021&measure=01&areas=INDUSTRY,STATE,MSA |
| U.S. Bureau of Labor Statistics, OEWS May 2025 occupation profile (national; same provenance) | United States | Sailors and Marine Oilers (SOC 53-5011) | Median $24.77/hr; mean $27.32/hr; **90th percentile $40.20/hr** | May 2025 | https://data.bls.gov/oesprofile/?major_group=530000&occupation=535011&measure=01&areas=INDUSTRY,STATE,MSA |
| BLS Employer Costs for Employee Compensation (ECEC), private industry (same provenance as Boston file) | United States, private industry | Employer burden benchmark | Total compensation **$46.60/hr**; wages and salaries **$32.60/hr** → multiplier **1.4294** | March 2026 (release June 12, 2026) | https://www.bls.gov/news.release/ecec.nr0.htm |
| Indeed employer salary aggregate (job-board corroboration) | San Diego / Flagship Cruises & Events | Captain | ~**$27.39/hr** (Indeed aggregate; "17% below" a comparison average per page); Deckhand San Diego **$20/hr** | Retrieved 2026-08-16; aggregate, posting dates not visible | https://www.indeed.com/cmp/Flagship-Cruises-&-Events/salaries/Captain |
| LinkedIn job listing (corroboration) | San Diego / Flagship Cruises & Events | Boat Captain (part-time) | Starting **$25.00/hr+** depending on experience | Retrieved 2026-08-16 | https://www.linkedin.com/jobs/view/boat-captain-at-flagship-cruises-events-4437421985 |
| ZipRecruiter search aggregate (corroboration) | San Diego, CA | Crew boat captain | Median ~**$25.29–$27.32/hr** (aggregate) | Retrieved 2026-08-16 | https://www.ziprecruiter.com/Jobs/Crew-Boat-Captain/-in-San-Diego,CA |

**Local-posting interpretation.** The Flagship-linked postings are direct market corroboration from the bay's incumbent operator, not substitutes for OEWS. They sit **below** the OEWS metro mean (tourism-operator wage tier; part-time structures), which suggests the OEWS-based model value below carries buffer rather than optimism. Job-board aggregates can be stale; retrieval date recorded.

## Loaded-cost computation (two people, per operating hour)

### Burden multiplier

Same as Boston: ECEC private-industry total-compensation multiplier

```text
Multiplier = $46.60 / $32.60 = 1.4294 (≈1.43×)
```

Not marine-specific; replace with operator-specific workers-comp/P&I-inclusive data when available.

### Scenarios

```text
loaded crew cost per operating hour = (captain base + deckhand base) × 1.4294
2026 drift = ×1.03³ ≈ ×1.0927 (≈3%/yr from May 2023)
```

| Case | Captain base | Deckhand base | Two-person base | × 1.4294 (May 2023 loaded) | × 1.0927 drift → **2026 loaded** |
|---|---:|---:|---:|---:|---:|
| **LOW — San Diego metro medians (May 2023)** | $33.66/hr | $21.03/hr | $54.69/hr | **$78.17/hr** | **$85.42/hr (≈$85/hr)** |
| **MID — San Diego metro means (May 2023)** | $36.89/hr | $22.63/hr | $59.52/hr | **$85.08/hr** | **$92.97/hr (≈$93/hr)** |
| **HIGH — national OEWS 90th-percentile stress case (May 2025; not San Diego-specific)** | $82.04/hr | $40.20/hr | $122.24/hr | **$174.73/hr (≈$175/hr)** | (already 2025-vintage; no drift applied) |

**Model value for `REVENUE-STACK-SAN-DIEGO.md`: $93/hr** (2026-drifted metro mean, MID). Posting-based cross-check: Flagship captain $27.39 + deckhand $20.00 = $47.39 base → $67.74/hr loaded at the same multiplier — ~27% below the model value, i.e., the model rate is conservative against the incumbent's visible pay scale.

**San Diego vs Boston:** San Diego's loaded metro mean ($85.08, May 2023) runs ~10% **above** Boston's ($77.16, May 2023) — captains and deckhands both price higher in this metro despite the lower-cost tourism-operator postings. Do not import Boston's $85/hr into San Diego; use $93/hr.

## Caveats

- A ~16-hour stacked operating day requires split shifts or two crews; this file prices per operating hour only and does not schedule-model crewing structure (same residual as Boston: overtime, seasonal premiums, credential tiers — structure, not rate).
- SOC 53-5011 includes sailors and marine oilers generally; SOC 53-5021 includes mates and pilots — proxies, not Subchapter T-specific rates. A 100-ton master requirement may price differently.
- OEWS metro rows are directly published for this metro (no state substitution needed); the May 2023 vintage is used because it is the latest directly validated local table (matching the Boston method); the ~3%/yr drift to 2026 is an assumption, labeled.
- ECEC is a U.S. private-industry average burden, not marine-specific; maritime/P&I insurance, training, and paid non-operating time may differ materially.
- The HIGH case is a national upper-tail stress figure, not a San Diego percentile (the metro table does not expose percentiles in the validated pull).
