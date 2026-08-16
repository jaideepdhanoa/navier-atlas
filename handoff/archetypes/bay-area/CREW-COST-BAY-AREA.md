# San Francisco Bay Area small commercial ferry crew-cost benchmarks

**As of:** 2026-08-15
**Status:** Source-backed benchmark following the Boston method exactly (`../boston/CREW-COST-BENCHMARKS.md`). Local figures are from the latest directly validated metro OEWS table (May 2023); the May 2024/May 2025 metro HTML pages were not directly readable this pass (the `/oes/current/` and `/oes/2024/may/` area URLs redirect to the OEWS tables index), so local calculations use May 2023 — the same vintage as the Boston benchmark. The BLS metro used is **San Francisco-Oakland-Hayward, CA** (this is the OEWS May 2023 name for the SF metro; the delegation referred to "San Francisco-Oakland-Berkeley" — BLS's own page header says Hayward and that name is used here). The modeled crew is one licensed captain/master (SOC 53-5021 proxy) plus one deckhand (SOC 53-5011 proxy).

## Sources

All OEWS wage figures are hourly dollars (median and mean columns from the BLS table). Estimates cover all industry sectors; they do not isolate Subchapter T passenger-ferry employers.

| Source | Geography | Occupation | Wage | Year / date | URL |
|---|---|---|---|---|---|
| BLS OEWS May 2023 metro table | San Francisco-Oakland-Hayward, CA | Captains, Mates, and Pilots of Water Vessels (53-5021) | Median **$47.75/hr**; mean **$57.48/hr** | May 2023 (retrieved Aug. 15, 2026) | https://www.bls.gov/oes/2023/may/oes_41860.htm |
| BLS OEWS May 2023 metro table | San Francisco-Oakland-Hayward, CA | Sailors and Marine Oilers (53-5011; deckhand proxy) | Median **$35.78/hr**; mean **$41.08/hr** | May 2023 (retrieved Aug. 15, 2026) | https://www.bls.gov/oes/2023/may/oes_41860.htm |
| BLS OEWS May 2023 state table | California (cross-check, not substituted) | Captains, Mates, and Pilots of Water Vessels (53-5021) | Median **$34.03/hr**; mean **$43.90/hr** | May 2023 (retrieved Aug. 15, 2026) | https://www.bls.gov/oes/2023/may/oes_ca.htm |
| BLS OEWS May 2023 state table | California | Sailors and Marine Oilers (53-5011) | Median **$24.46/hr**; mean **$29.61/hr** | May 2023 (retrieved Aug. 15, 2026) | https://www.bls.gov/oes/2023/may/oes_ca.htm |
| BLS OEWS May 2025 occupation profile | United States | Captains, Mates, and Pilots of Water Vessels (53-5021) | 90th percentile **$82.04/hr** | May 2025 (as validated in the Boston pass, Aug. 15, 2026) | https://data.bls.gov/oesprofile/?major_group=530000&occupation=535021&measure=01&areas=INDUSTRY,STATE,MSA |
| BLS OEWS May 2025 occupation profile | United States | Sailors and Marine Oilers (53-5011) | 90th percentile **$40.20/hr** | May 2025 (as validated in the Boston pass, Aug. 15, 2026) | https://data.bls.gov/oesprofile/?major_group=530000&occupation=535011&measure=01&areas=INDUSTRY,STATE,MSA |
| BLS Employer Costs for Employee Compensation (ECEC), private industry | United States (sector benchmark; not marine-specific) | Employer burden benchmark | Total compensation **$46.60/hr**; wages **$32.60/hr** | March 2026 (release June 12, 2026) | https://www.bls.gov/news.release/ecec.nr0.htm |

**Notable local context (sourced, not used in the calculation):** the SF metro's captain mean ($57.48) runs ~31% above the California state mean ($43.90) and ~73% above the Boston metro mean ($33.29, May 2023) — the Bay Area is the most expensive crew market yet benchmarked in this program.

## Loaded-cost computation (two people, per operating hour)

### Burden multiplier (identical to Boston)

```text
Multiplier = ECEC total compensation / wages and salaries = $46.60 / $32.60 = 1.4294
```

This is a total-employer-compensation benchmark (paid leave, insurance, retirement, legally required benefits). It is not a marine-insurance premium or an operator-specific workers-comp/P&I quote.

### Scenarios

```text
loaded crew cost per operating hour = (captain base wage + deckhand base wage) × 1.4294
```

| Case | Captain base | Deckhand base | Base two-person wage | Math | Loaded crew cost / operating hour |
|---|---:|---:|---:|---:|---:|
| **LOW — SF metro median (May 2023)** | $47.75/hr | $35.78/hr | $83.53/hr | $83.53 × 1.4294 | **$119.40/hr (about $119/hr)** |
| **MID — SF metro mean (May 2023)** | $57.48/hr | $41.08/hr | $98.56/hr | $98.56 × 1.4294 | **$140.88/hr (about $141/hr)** |
| **HIGH — national OEWS 90th-percentile stress case (May 2025; not Bay-Area-specific)** | $82.04/hr | $40.20/hr | $122.24/hr | $122.24 × 1.4294 | **$174.73/hr (about $175/hr)** |

### 2026 wage-drift model value (for the revenue-stack model)

Applying the same ~3%/yr drift assumption used in Boston, from May 2023 to 2026 (×1.0927):

- LOW drifted: $119.40 × 1.0927 ≈ **$130.5/hr**
- MID drifted: $140.88 × 1.0927 ≈ **$153.9/hr**

**Adopted model value: $155/hr** for a 2-person crew — the 2026-drifted metro mean with a small buffer, structurally identical to Boston's adoption of $85/hr (2023 mean $77.16 + drift). Derived, per the method above.

## Caveats

- Same caveats as Boston apply in full: OEWS is all-industry, SOC 53-5011 is a proxy, the ECEC multiplier is a U.S. private-industry average, a ~16-hour stacked day needs split shifts/two crews (structure not modeled here), and overtime/seasonal/union/credential premiums can raise actual cost.
- The California state rows are supplied as a cross-check only; the SF metro rows are directly published and are used for LOW/MID.
- No Bay Area operator job postings were collected this pass (Boston used postings as corroboration). Flagged as a possible follow-up; the OEWS metro rows are the primary evidence either way.
- The HIGH case is the national 90th percentile (May 2025), not an SF percentile — the directly validated May 2023 metro table does not expose local percentiles, and inventing one would violate fail-closed rules. Note the SF metro *mean* already sits near the national 90th percentile band, so the HIGH stress case is less of a stretch here than in Boston.
