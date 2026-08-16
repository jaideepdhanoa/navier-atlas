# Miami / Fort Lauderdale small commercial ferry crew-cost benchmarks

**As of:** 2026-08-16
**Status:** Source-backed benchmark following the Boston method exactly (`boston/CREW-COST-BENCHMARKS.md`): BLS OEWS metro medians/means for one licensed captain (SOC 53-5021 proxy) + one deckhand (SOC 53-5011 proxy), × 1.4294 ECEC burden, × ~3%/yr wage drift to 2026. The latest directly validated local OEWS rows are **May 2023** for the **Miami-Fort Lauderdale-West Palm Beach, FL** MSA (BLS area 33100); the May 2025 releases did not expose a directly readable Miami metro row in this pass (the current-tables URL resolves to an index page), so local calculations use May 2023 — same vintage as the Boston file.

## Sources

All OEWS figures are hourly dollars from tables covering all industry sectors; they do not isolate Subchapter T passenger-ferry employers.

| Source | Geography | Occupation | Wage | Year / date | URL |
|---|---|---|---|---|---|
| BLS OEWS May 2023 metro table | Miami-Fort Lauderdale-West Palm Beach, FL | Captains, Mates, and Pilots of Water Vessels (53-5021) | Median **$36.56/hr**; mean **$38.60/hr** (annual mean $80,280; mean wage RSE 19.3%; employment estimate not released — footnote (8)) | May 2023 | https://www.bls.gov/oes/2023/may/oes_33100.htm |
| BLS OEWS May 2023 metro table | Miami-Fort Lauderdale-West Palm Beach, FL | Sailors and Marine Oilers (53-5011; deckhand proxy) | Median **$19.98/hr**; mean **$25.21/hr** (employment 670) | May 2023 | https://www.bls.gov/oes/2023/may/oes_33100.htm |
| BLS OEWS occupation profile | United States | 53-5021 | Median $42.66/hr; mean $47.03/hr; 90th pct $77.65/hr | May 2023 | https://www.bls.gov/oes/2023/may/oes535021.htm |
| BLS OEWS occupation profile | United States | 53-5011 | Median $23.27/hr; mean $25.71/hr; 90th pct $38.07/hr | May 2023 | https://www.bls.gov/oes/2023/may/oes535011.htm |
| BLS OEWS May 2025 occupation profile | United States | 53-5021 | Median $44.45/hr; mean $49.87/hr; 90th pct **$82.04/hr** | May 2025 (retrieved for the Boston pass, 2026-08-15) | https://data.bls.gov/oesprofile/?major_group=530000&occupation=535021&measure=01&areas=INDUSTRY,STATE,MSA |
| BLS OEWS May 2025 occupation profile | United States | 53-5011 | Median $24.77/hr; mean $27.32/hr; 90th pct **$40.20/hr** | May 2025 | https://data.bls.gov/oesprofile/?major_group=530000&occupation=535011&measure=01&areas=INDUSTRY,STATE,MSA |
| BLS ECEC, private industry | United States | Employer burden benchmark | Total comp **$46.60/hr** ÷ wages **$32.60/hr** → **1.4294×** | March 2026 (released June 12, 2026) | https://www.bls.gov/news.release/ecec.nr0.htm |
| Indeed employer salary page (job-board corroboration) | Miami | Boat Captain — "Water Taxi" (company page) | ~**$24.58/hr** average (5 reported salaries; described as 15% below national average) | Retrieved 2026-08-16 | https://www.indeed.com/cmp/Water-Taxi-2/salaries/Boat-Captain/Miami-FL |
| ZipRecruiter aggregate (job-board corroboration) | Miami | Ferry captain | Average **$35.69/hr**; most between $16.54 and $39.57/hr | As of Aug 2026 | https://www.ziprecruiter.com/Jobs/Ferry-Captain/-in-Miami,FL |
| Glassdoor search (job-board corroboration) | Miami | Boat captain (WaterTaxi Miami listing) | **$22–$35/hr** (employer-provided) | Retrieved 2026-08-16 | https://www.glassdoor.com/Job/miami-boat-captain-jobs-SRCH_IL.0,5_IC1154170_KO6,18.htm |

**Local-posting interpretation.** Job-board aggregates are corroboration only, can be stale, and skew toward tour/water-taxi operators rather than USCG-licensed fast-ferry masters. They bracket the OEWS metro figures (posted captain rates $22–$39.57/hr vs OEWS median $36.56/mean $38.60) and do not contradict them. Note the direction of surprise vs Boston: **Miami captain wages are materially higher than Boston's** (median $36.56 vs $29.64; mean $38.60 vs $33.29) — consistent with South Florida's large yachting/cruise labor market — while deckhand wages are moderately higher ($19.98/$25.21 vs $17.42/$20.69). The 19.3% mean-wage RSE on the captain row means the mean is noisier than Boston's; medians are the tighter anchor here.

## Loaded-cost computation (two people, per operating hour)

### Burden multiplier

Same as Boston: ECEC private-industry total-compensation multiplier = $46.60 / $32.60 = **1.4294** (≈1.43×). U.S.-wide, not marine-specific; replace with operator-specific data when available.

### Scenarios

```text
loaded crew cost per operating hour = (captain base + deckhand base) × 1.4294
```

LOW and MID use the directly published Miami metro May 2023 medians and means. HIGH is the national May 2025 90th-percentile stress case (identical construction to Boston's HIGH; not a Miami point estimate).

| Case | Captain base | Deckhand base | Two-person base | × 1.4294 | Loaded $/operating hr (May 2023 basis) | + ~3%/yr drift to 2026 (×1.0927) |
|---|---:|---:|---:|---:|---:|---:|
| **LOW — Miami metro median (2023)** | $36.56 | $19.98 | $56.54 | $56.54 × 1.4294 | **$80.82/hr** | **≈ $88.31/hr** |
| **MID — Miami metro mean (2023)** | $38.60 | $25.21 | $63.81 | $63.81 × 1.4294 | **$91.21/hr** | **≈ $99.67/hr** |
| **HIGH — national 90th-percentile stress (May 2025, not Miami-specific)** | $82.04 | $40.20 | $122.24 | $122.24 × 1.4294 | **$174.73/hr** | (already 2025; no drift applied) |

**Model value adopted for `REVENUE-STACK-MIAMI.md`: $100/hr loaded, 2-person crew** — the 2026 wage-drifted metro mean ($99.67) rounded up, i.e., sourced mean with a built-in buffer, mirroring Boston's $85 construction. Miami's model crew rate is ~18% above Boston's for the same method — a real cost headwind, carried honestly into the revenue stack.

## Caveats

- Same structural caveats as Boston: a ~16-hour stacked operating day requires split shifts or two crews; overtime, seasonal scarcity (South Florida charter season), credential premiums (100-ton masters), and union/contract terms are not modeled — this is a per-operating-hour rate only.
- SOC 53-5011 includes sailors and marine oilers broadly; 53-5021 includes mates and pilots — neither isolates a 45-ft/20-pax foiling ferry crew.
- The Miami metro OEWS geography spans Miami-Dade, Broward, and Palm Beach counties — appropriate here since the network itself spans Miami-Dade and Broward.
- Captain-row employment was not released (footnote (8)) and the mean wage RSE is 19.3%; the median-based LOW case is the statistically firmer floor.
- ECEC multiplier is not marine-specific (no P&I/Jones Act workers-comp adjustment).
- The May 2023 local vintage + drift assumption should be refreshed when BLS exposes a readable May 2025 Miami metro row (national May 2025 data exist and are cited above).
