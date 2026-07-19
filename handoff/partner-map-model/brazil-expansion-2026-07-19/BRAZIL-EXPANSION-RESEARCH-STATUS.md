# Brazil coastal expansion — research status (2026-07-19)

Source-led research pass for the Brazil priority-market expansion: **3 → 14 Atlas cities**. All artifacts in this folder; city briefs in `partner-pitch/city_briefs/`. Status label: **research-complete / seal-needed** for geometry; economics promotion pending fare-anchor approvals and Grok route IDs.

## Totals
- **13 market packages** (12 new + Angra densification)
- **162 boarding points** — 149 with verified coordinates (OSM/Nominatim cross-checked against official operator/regulator pages), 13 honest nulls (real facilities, coords unverifiable — flagged for survey; never guessed)
- **185 candidate routes** — 91 grounded / 94 aspirational / **41 signature**
- **9 new city briefs** written + Angra brief corrected — all pass `scripts/audit_partner_copy.py` (0 leaks)

## Per-market summary

| Market | Tier | BPs (verified) | Routes (grounded/sig) | Economics lane | Headline demand basis |
|---|---|---|---|---|---|
| salvador-brazil | marquee | 13 (13) | 27 (7/5) | **FULL T1** | 7.49M pax 2025, 3.42M Jan–May 2026 (MTur/AGERBA); Morro catamaran R$138.75–172.51 live premium fare |
| santos-guaruja-brazil | marquee | 15 (15) | 21 (7/5) | **FULL T1** | 9.65M users H1-2024 litoral crossings (Semil/G1); ~21k veh + 7.6k ped/day; Acqua Vias PPP R$2.5bn, 40+ mostly-electric vessels |
| sao-sebastiao-ilhabela-brazil | marquee | 12 (10) | 18 (13/5) | **FULL T1** | 12,584 users/day (Semil VDM 2024); 1.15M+ pax 86-day summer op; 15% of state trips; Hora Marcada queue-skip premium R$65.30–98 (3.4×) |
| vitoria-vila-velha-brazil | full | 15 (12) | 13 (7/3) | **FULL T1** | ~500k pax yr-1, >1.2M cumulative Dec 2025 (SEMOBI/SEP); 4th station opened May 2026, 3 more funded |
| sao-luis-alcantara-brazil | full | 9 (8) | 12 (2/3) | HOLD (`_economics_hold_reason`) | 1.8M pax 2017 record (EMAP); Carnival 71,737/11 days 2026; no recent annual series. **Correction:** 190–220k festival figure was Bahia's, not MA |
| ilha-do-mel-brazil | display→full candidate | 9 (9) | 10 (9/2) | HOLD — promotion candidate | **383,162 boat boardings 2025** (Abaline); 247,020 park visitors 2025 (IAT); AGEPAR-homologated tariffs incl. R$69.07 nautical-taxi premium |
| porto-alegre-guaiba-brazil | full | 11 (9) | 14 (6/3) | HOLD | CatSul live R$16.90; 314k pax 2020; ~1.7k/day 2022; no continuous series (AIIB EIAS PDF = best lead) |
| buzios-cabo-frio-arraial-brazil | full | 11 (10) | 12 (8/4) | display-only | Búzios 992,139 tourists 2023 + 76,276 cruise-tender pax Jan 2026 (official); Arraial Navy 300-person Farol cap; no regulated pax series |
| paraty-brazil | display | 9 (9) | 10 (5/2) | display-only | ~3.5M visitors/yr (municipal estimate); ~50-schooner fleet; no official boarding series |
| recife-brazil | display | 11 (9) | 9 (3/2) | display-only (parked) | Rios da Gente shelved <2% built (TCE-PE); Catamaran Tours R$90 live; honest urban-waterway-potential framing |
| belem-brazil | display (riverine) | 14 (12) | 10 (8/2) | out of scope (Amazon lane) | **553,823 pax 2024 (ARTRAN intermunicipal)**; COP30 legacy terminals; >300k/Jul-2026 projected |
| manaus-brazil | display (riverine) | 12 (12) | 10 (4/2) | out of scope (Amazon lane) | **808,462 pax 2023 (+8.6%) — ARSEPAM annual report**; R$875.9M Novo PAC terminal, 3.5M pax/yr capacity by 2029 |
| angra-dos-reis-ilha-grande-brazil | densify | 21 (21) | 19 (12/3) | existing sealed — untouched | >1.2M Ilha Grande visitors/yr; 1,356,295 municipal tourists 2023; Barcas Rio R$20.50 state ferry; Conceição flexboats R$60–100 |

## Angra brief corrections applied (this PR)
1. `navier_fit.quanta_lr` 2,000 nm → **700 nm** (release-gate token)
2. `navier_fit.pioneer_ii` Angra↔Ilha Grande ~9 nm → **~13 nm** (matches sealed corridor)
3. `competitive_landscape`: Conceição de Jacareí crossing = private **flexboats**; state ferry operator = **Barcas Rio consortium since Feb 2025** (ex-CCR Barcas)
4. `regulatory_note`: added **AGETRANSP** (source of the sealed T1 economics)
5. `demand_signals`: added sourced 1.2M island / 1,356,295 municipal visitor numbers

## Known residuals (tracked, non-blocking)
- Atlas node label "CCR Barcas - Mangaratiba" (`bp-f032d26f15`, Rio market) is stale → **Barcas Rio** (folded into the Grok seal spec).
- Observatório do Turismo da Bahia PDFs unreachable (per-mode Salvador series) — system totals closed via MTur/AGERBA/press; retry queued for the economics pass.
- Per-market `gaps[]` lists inside each demand record.

## Next steps
1. Jaideep review/merge this PR (**PR A**).
2. Fare-anchor approval batch (separate message) for the T1 markets.
3. Grok seal per `GROK-SPEC-brazil-expansion-seal-2026-07-19.md`.
4. Economics cascade (corridors.json → aggregate → growth → sheets → both Brazil partner decks) after sealed route IDs return.
