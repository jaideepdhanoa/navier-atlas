# New York, NY small commercial ferry crew-cost benchmarks

**As of:** 2026-08-16
**Status:** Source-backed benchmark, Boston method followed exactly (see `../boston/CREW-COST-BENCHMARKS.md`). Metro figures are from the latest directly validated local OEWS tables (May 2023) — the current BLS metro landing page did not expose a directly readable data table this pass, so as in Boston the May 2023 metro table is the controlling local source. Metro is **New York-Newark-Jersey City, NY-NJ-PA** (OEWS area 35620 — includes the NJ Gold Coast stops in this network). Modeled crew: one licensed captain/master (SOC 53-5021 proxy) + one deckhand (SOC 53-5011 proxy).

## Sources

All OEWS figures are hourly dollars, all-industry estimates; they do not isolate Subchapter T passenger-ferry employers.

| Source | Geography | Occupation | Wage | Year / date | URL |
|---|---|---|---|---|---|
| BLS OEWS May 2023 metro table | New York-Newark-Jersey City, NY-NJ-PA | Captains, Mates, and Pilots of Water Vessels (53-5021) | Median **$47.59/hr**; mean **$49.28/hr** | May 2023 | https://www.bls.gov/oes/2023/may/oes_35620.htm |
| BLS OEWS May 2023 metro table | New York-Newark-Jersey City, NY-NJ-PA | Sailors and Marine Oilers (53-5011; deckhand proxy) | Median **$29.38/hr**; mean **$31.50/hr** | May 2023 | https://www.bls.gov/oes/2023/may/oes_35620.htm |
| BLS OEWS May 2023 state table (cross-check) | New York State | Captains, Mates, and Pilots (53-5021) | Median **$39.33/hr**; mean **$45.33/hr** | May 2023 | https://www.bls.gov/oes/2023/may/oes_ny.htm |
| BLS OEWS May 2023 state table (cross-check) | New York State | Sailors and Marine Oilers (53-5011) | Median **$27.62/hr**; mean **$29.37/hr** | May 2023 | https://www.bls.gov/oes/2023/may/oes_ny.htm |
| BLS OEWS May 2025 occupation profile (national) | United States | Captains, Mates, and Pilots (53-5021) | Median $44.45; mean $49.87; 90th pct **$82.04/hr** | May 2025 (retrieved Aug 2026, same profile validated in Boston pass) | https://data.bls.gov/oesprofile/?major_group=530000&occupation=535021&measure=01&areas=INDUSTRY,STATE,MSA |
| BLS OEWS May 2025 occupation profile (national) | United States | Sailors and Marine Oilers (53-5011) | Median $24.77; mean $27.32; 90th pct **$40.20/hr** | May 2025 | https://data.bls.gov/oesprofile/?major_group=530000&occupation=535011&measure=01&areas=INDUSTRY,STATE,MSA |
| BLS ECEC, private industry (burden benchmark) | United States | — | Total comp **$46.60/hr** ÷ wages **$32.60/hr** = **1.4294×** | March 2026 (release June 12, 2026) | https://www.bls.gov/news.release/ecec.nr0.htm |
| Hornblower / NYC Ferry job posting (local corroboration) | Brooklyn, NY | Ferry Captain | **$36.04/hr** posted salary | Live posting, retrieved Aug 16, 2026 | https://recruiting.ultipro.com/HOR1007HORNB/JobBoard/dec5c41f-535e-4693-8cc7-e4ae40474a06/OpportunityDetail?opportunityId=df084a53-ef1b-4065-8578-f47372f4c9f1 |
| Indeed employer-salary aggregate (job-board corroboration) | NY Waterway (US) | Deckhand | ~**$15.37/hr** average | Retrieved Aug 16, 2026; aggregate, not a dated posting | https://www.indeed.com/cmp/Ny-Waterway/salaries/Deckhand |
| Glassdoor aggregate (weak corroboration) | NY Waterway | Deckhand | ~$25/hr estimated average | Retrieved Aug 16, 2026 | https://www.glassdoor.com/Hourly-Pay/NY-Waterway-Deckhand-Hourly-Pay-E22635_D_KO12,20.htm |

**Local-posting interpretation.** The Hornblower captain posting ($36.04) and NY Waterway deckhand aggregates ($15–25) sit **well below** the OEWS metro means. The likely reason: OEWS 53-5021 for this metro pools harbor/docking pilots and deep-sea officers (very high earners in the Port of NY/NJ) with small-passenger-vessel captains. The OEWS-based figures below are therefore a conservative (high) cost basis for a 45-ft ferry; the posting-based cross-check is shown after the table.

## Loaded-cost computation (two people, per operating hour)

Burden multiplier (Boston method): ECEC total compensation ÷ wages = $46.60 / $32.60 = **1.4294×** (U.S. private-industry benchmark, not marine-specific).

```text
loaded crew cost per operating hour = (captain base + deckhand base) × 1.4294
```

| Case | Captain base | Deckhand base | Two-person base | × 1.4294 | Loaded $/operating-hr |
|---|---:|---:|---:|---:|---:|
| **LOW — NY metro median (May 2023)** | $47.59 | $29.38 | $76.97 | $76.97 × 1.4294 | **$110.02/hr (~$110)** |
| **MID — NY metro mean (May 2023)** | $49.28 | $31.50 | $80.78 | $80.78 × 1.4294 | **$115.47/hr (~$115)** |
| **HIGH — national OEWS 90th-percentile stress case (May 2025; not NY-specific)** | $82.04 | $40.20 | $122.24 | $122.24 × 1.4294 | **$174.73/hr (~$175)** |

**Drift to 2026** (~3%/yr from May 2023, ×1.0927): LOW → **~$120/hr**; MID → **~$126/hr**. The revenue-stack model uses **$130/hr** (2026-drifted metro mean rounded up, same convention as Boston's $85).

**Posting-based cross-check (LOW-side):** Hornblower NYC Ferry captain $36.04 + NY Waterway deckhand $15.37 = $51.41 base × 1.4294 = **$73.49/hr loaded** — 42% below the drifted OEWS mean. This is direct market evidence that an operator hiring at posted NYC ferry wages could run materially cheaper than the OEWS-based model value; it is not used as the headline because postings are not a standardized wage series and the deckhand figure is an undated aggregate. Shown as a sensitivity in `REVENUE-STACK-NEW-YORK.md`.

## Caveats

- Same structural caveats as Boston: a ~16-hr stacked day needs split shifts/two crews (not schedule-modeled here); overtime, union terms (NYC ferry labor is partially unionized — MM&P/SIU presence at major operators is **unverified this pass**), credential premiums (100-ton masters), and seasonal scarcity can raise costs.
- OEWS metro geography includes NJ and PA counties; that is a feature here (the network has seven NJ stops) but the pool still spans all industries.
- The 53-5021 pilot-pooling issue cuts the other way from Boston: in the nation's largest port, the OEWS mean is likely **biased high** for small-vessel captains. Fail-open on cost (we keep the high basis) rather than fail-open on revenue.
- ECEC multiplier is not marine-specific; replace with operator quotes (workers' comp, MEL/P&I) when available.
