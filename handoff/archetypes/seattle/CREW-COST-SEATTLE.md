# Seattle, WA small commercial ferry crew-cost benchmarks

**As of:** 2026-08-16
**Status:** Source-backed benchmark following the Boston method exactly (`../boston/CREW-COST-BENCHMARKS.md`): BLS OEWS metro wages for one licensed captain/master (SOC 53-5021 proxy) + one deckhand (SOC 53-5011 proxy), × 1.4294 ECEC burden, × ~3%/yr drift to 2026. **Vintage:** the latest directly machine-readable local rows are the **May 2023** OEWS metro table for **Seattle-Tacoma-Bellevue, WA** (OEWS area 42660). A fetch of the May 2024 metro table did not return readable occupation rows this pass, so local calculations use May 2023 — same vintage and same limitation as the Boston benchmark.

## Sources

| Source | Geography | Occupation | Wage | Year / date | URL |
|---|---|---|---|---|---|
| BLS OEWS May 2023 metro table | Seattle-Tacoma-Bellevue, WA | Captains, Mates, and Pilots of Water Vessels (SOC 53-5021) | Median **$49.41/hr**; mean **$48.93/hr** (annual mean $101,770; employment 1,120) | May 2023 | https://www.bls.gov/oes/2023/may/oes_42660.htm |
| BLS OEWS May 2023 metro table | Seattle-Tacoma-Bellevue, WA | Sailors and Marine Oilers (SOC 53-5011; deckhand proxy) | Median **$28.49/hr**; mean **$28.63/hr** (annual mean $59,550; employment 1,340) | May 2023 | https://www.bls.gov/oes/2023/may/oes_42660.htm |
| BLS OEWS May 2025 occupation profile (national) | United States | SOC 53-5021 | Median $44.45/hr; mean $49.87/hr; **90th percentile $82.04/hr** | May 2025 | https://data.bls.gov/oesprofile/?major_group=530000&occupation=535021&measure=01&areas=INDUSTRY,STATE,MSA (as captured in the Boston pass, 2026-08-15) |
| BLS OEWS May 2025 occupation profile (national) | United States | SOC 53-5011 | Median $24.77/hr; mean $27.32/hr; **90th percentile $40.20/hr** | May 2025 | https://data.bls.gov/oesprofile/?major_group=530000&occupation=535011&measure=01&areas=INDUSTRY,STATE,MSA (as captured in the Boston pass, 2026-08-15) |
| BLS ECEC, private industry | United States | Employer burden benchmark | Total comp $46.60/hr; wages $32.60/hr → **multiplier 1.4294** | March 2026 (released June 12, 2026) | https://www.bls.gov/news.release/ecec.nr0.htm |
| Seattle Office of Labor Standards | City of Seattle | Minimum-wage floor context | **2026 Seattle minimum wage $21.30/hr** (all employers) | 2026 | https://www.seattle.gov/laborstandards/ordinances/minimum-wage |
| WA L&I local minimum-wage rates page | Washington State | Context | State + local rates listed (state 2026 rate not captured this pass — **unverified**, do not quote a number) | 2026 | https://www.lni.wa.gov/workers-rights/wages/minimum-wage/local-minimum-wage-rates |

**Notable structural read:** the Seattle metro captain wage distribution is unusually *flat at a high level* — the median ($49.41) slightly **exceeds** the mean ($48.93), unlike Boston (median $29.64 < mean $33.29). This is consistent with a large, unionized public-fleet employer base (WSF is the largest US ferry operator; KCWT and Kitsap Transit crews are public-agency/contracted union workforces) compressing the distribution from below. Two consequences: (1) the LOW (median-based) case is **not materially lower** than MID here; (2) Seattle crew cost runs ~40–45% above Boston's at the same vintage. Washington's aggressive wage floors (Seattle $21.30 minimum in 2026 — the deckhand *market* wage is still ~$28+ at the mean) support treating drift as real, not optional. Union pay-scale documents (MM&P/IBU agreements with WSF) were not pulled this pass — **unverified**, noted as an upgrade path for operator-specific rates.

## Loaded-cost computation (two people, per operating hour)

Burden multiplier (Boston method): `$46.60 / $32.60 = 1.4294`. Drift: ~3%/yr May 2023 → 2026 = ×1.0927.

| Case | Captain base | Deckhand base | Base 2-person | × 1.4294 (2023 loaded) | × 1.0927 drift → 2026 |
|---|---:|---:|---:|---:|---:|
| **LOW — Seattle metro medians (May 2023)** | $49.41 | $28.49 | $77.90 | **$111.35/hr** | **$121.68/hr (≈$122)** |
| **MID — Seattle metro means (May 2023)** | $48.93 | $28.63 | $77.56 | **$110.86/hr** | **$121.14/hr (≈$121)** |
| **HIGH — national OEWS 90th-percentile stress (May 2025; not Seattle-specific)** | $82.04 | $40.20 | $122.24 | **$174.73/hr (≈$175)** | (already 2025 vintage; no drift applied) |

**Model value adopted for the Seattle revenue stack: $120/hr loaded, 2-person crew** — the drifted LOW/MID cases bracket $121–122 and are effectively identical (see structural read above); $120 is the sourced mean, rounded, with the same construction as Boston's $85 (2023 mean + drift). Because LOW ≈ MID in this metro, there is **no meaningful cheap-crew scenario**: Seattle crew cost is a structural fact of the market, and it is the single biggest economics gap vs Boston.

## Caveats (Boston-method caveats apply; Seattle-specific first)

- Metro geography is the full Seattle-Tacoma-Bellevue MSA; OEWS covers all industries and does not isolate Subchapter T passenger-vessel employers. The large deep-sea/tug/fishing fleet in this metro (Fishermen's Terminal, Harbor Island) may pull SOC 53-5021 above small-harbor-ferry reality — but the public-ferry union scales argue against assuming a discount.
- A 16-hour stacked service day requires split shifts or two crews; this is a per-operating-hour rate only. Overtime, seasonal premiums, and 100-ton-master credential premiums not modeled.
- ECEC 1.4294 is a US private-industry average burden, not marine-specific; WA payroll taxes (PFML, WA Cares) and maritime P&I may differ materially. Replace with operator quotes when available.
- May 2024/2025 Seattle metro OEWS rows: not machine-readable this pass; re-attempt before next model refresh and re-base drift if newer local rows land.
- No Seattle operator job-posting corroboration pass was run this time (Boston had one); flagged as a gap, not a blocker — OEWS local rows were directly readable.
