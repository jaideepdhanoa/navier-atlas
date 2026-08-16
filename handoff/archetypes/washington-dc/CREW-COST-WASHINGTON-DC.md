# Washington DC small commercial ferry crew-cost benchmarks

**As of:** 2026-08-16
**Status:** Source-backed benchmark following the Boston method exactly (`../boston/CREW-COST-BENCHMARKS.md`): BLS OEWS metro medians/means for captains (SOC 53-5021) + deckhands (SOC 53-5011 proxy), × 1.4294 ECEC burden, × ~3%/yr wage drift to 2026. Metro used: **Washington-Arlington-Alexandria, DC-VA-MD-WV (OEWS area 47900)** — metro rows were directly available, so no state substitution was needed. Local table vintage: **May 2023** (latest directly validated local OEWS rows, same vintage situation as Boston). The modeled crew is one licensed captain/master (53-5021 proxy) plus one deckhand (53-5011 proxy).

## Sources

All OEWS wage figures are hourly dollars from the May 2023 metro table for Washington-Arlington-Alexandria, DC-VA-MD-WV, retrieved 2026-08-16.

| Source | Geography | Occupation | Wage | Year | URL |
|---|---|---|---|---|---|
| BLS OEWS May 2023 metro table | Washington-Arlington-Alexandria, DC-VA-MD-WV | Captains, Mates, and Pilots of Water Vessels (53-5021) | Median **$28.31/hr**; mean **$36.68/hr** (annual mean $76,300); employment 200; wage RSE 10.8% | May 2023 | https://www.bls.gov/oes/2023/may/oes_47900.htm |
| BLS OEWS May 2023 metro table | Washington-Arlington-Alexandria, DC-VA-MD-WV | Sailors and Marine Oilers (53-5011; deckhand proxy) | Median **$28.16/hr**; mean **$28.02/hr** (annual mean $58,280); employment 80; wage RSE 11.9% | May 2023 | https://www.bls.gov/oes/2023/may/oes_47900.htm |
| BLS OEWS occupation profile (national cross-check) | United States | 53-5021 | Median $42.66/hr; mean $47.03/hr; 90th pct $77.65/hr | May 2023 | https://www.bls.gov/oes/2023/may/oes535021.htm |
| BLS OEWS occupation profile (national cross-check) | United States | 53-5011 | Median $23.27/hr; mean $25.71/hr; 90th pct $38.07/hr | May 2023 | https://www.bls.gov/oes/2023/may/oes535011.htm |
| BLS OEWS May 2025 occupation profile (national, latest) | United States | 53-5021 | Median $44.45/hr; mean $49.87/hr; 90th pct **$82.04/hr** | May 2025 | https://data.bls.gov/oesprofile/?major_group=530000&occupation=535021&measure=01&areas=INDUSTRY,STATE,MSA |
| BLS OEWS May 2025 occupation profile (national, latest) | United States | 53-5011 | Median $24.77/hr; mean $27.32/hr; 90th pct **$40.20/hr** | May 2025 | https://data.bls.gov/oesprofile/?major_group=530000&occupation=535011&measure=01&areas=INDUSTRY,STATE,MSA |
| BLS Employer Costs for Employee Compensation (ECEC), private industry | United States | Employer burden benchmark | Total compensation **$46.60/hr**; wages **$32.60/hr** → multiplier **1.4294** | March 2026 (released June 12, 2026) | https://www.bls.gov/news.release/ecec.nr0.htm |

No DC-area operator job postings were pulled this pass (Boston's file added Indeed/operator corroboration rows); **local-posting corroboration: not collected — flag for a follow-up pass**, not a blocker for the OEWS-based benchmark.

## Loaded-cost computation (two people, per operating hour)

Burden multiplier (same basis as Boston): `$46.60 / $32.60 = 1.4294`. Formula: `(captain base + deckhand base) × 1.4294`.

| Case | Captain base | Deckhand base | Two-person base | × 1.4294 | Loaded $/operating hr (May 2023) |
|---|---:|---:|---:|---:|---:|
| **LOW — DC metro medians (2023)** | $28.31 | $28.16 | $56.47 | 56.47 × 1.4294 | **$80.72/hr (~$81/hr)** |
| **MID — DC metro means (2023)** | $36.68 | $28.02 | $64.70 | 64.70 × 1.4294 | **$92.48/hr (~$92/hr)** |
| **HIGH — national OEWS 90th-percentile stress (May 2025; not DC-specific)** | $82.04 | $40.20 | $122.24 | 122.24 × 1.4294 | **$174.73/hr (~$175/hr)** |

### Drift to 2026 and model value

Applying the Boston convention of ~3%/yr wage drift from May 2023 to 2026 (×1.0927):

- LOW drifted: $80.72 × 1.0927 ≈ **$88.20/hr**
- MID drifted: $92.48 × 1.0927 ≈ **$101.06/hr**

**Model value for the DC revenue stack: $100/hr loaded, 2-person crew** — the 2026-drifted metro mean, rounded down slightly (drifted mean ≈ $101). Same construction as Boston's $85 (2023 mean $77.16 + drift). Note the DC premium: DC's modeled crew cost is ~18% above Boston's, driven mostly by the deckhand-proxy mean ($28.02 DC vs $20.69 Boston).

## Caveats

- **Thin local samples:** OEWS shows only 200 captains and 80 sailors/oilers employed in the DC metro, with wage RSEs of 10.8%/11.9% — wider uncertainty than Boston's rows. Treat MID as a benchmark, not a quote.
- **Median ≈ mean quirk for 53-5011** (median $28.16 > mean $28.02): consistent with a small, compressed local sample; it makes LOW and MID unusually close on the deckhand side.
- The ECEC 1.4294 multiplier is US private-industry average burden, not marine-specific; replace with operator-specific workers' comp/P&I data when available.
- OEWS covers all industries; it does not isolate Subchapter T passenger-vessel employers. A 100-ton master requirement, security-clearance-adjacent routes, or federal-contract crewing in this market could price above the SOC proxy.
- A ~16-hour stacked operating day requires split shifts or two crews; this file prices the operating hour only. Overtime, seasonal premiums, and union/contractor terms are structure items for the ops walkthrough.
- Local vintage is May 2023 because that is the latest directly validated metro table (matching the Boston file's situation); the national May 2025 profile is used only for the HIGH stress case.
