# DiDi Brazil / Colombia T3 Proof Status — 2026-07-09

**Snapshot:** `jaideepdhanoa/navier-atlas@ba48bc5d`  
**Inputs read:** the sealed handoff, exact route spine, existing deepening artifact, and G2 receipt named in the handoff.  
**Ledger:** `DIDI-BR-CO-T3-PROOF-2026-07-09.json` (JSON validated).

## Finance gate

**Wave gate: `blocked_pending_primary_evidence`.** The four sealed Rio routes now have defensible non-null 2023 passenger-trip totals and current official published-fare benchmarks. The sealed Colombia route `rn-aa790551baa7` remains null-only because exact-OD current scheduled service, annual demand, fare, and operator permission were not publicly proved. Realized yield, country-specific opex values, and a transferable DiDi/Navier permission remain null everywhere.

| Sealed route | Exact OD | 2023 annual one-way passenger-trips | Official published fare | Proof disposition | Finance gate |
|---|---|---:|---:|---|---|
| `rn-1886629dbf0c` | Praça XV ↔ Arariboia (Niterói) | **10,848,719** | **R$5.00**, effective 2026-02-08 | demand `usable_for_base_case`; fare `benchmark_only`; DiDi/Navier entry `permission_required` | `t3_buildable_non_null` |
| `rn-80f0d0ebe0bd` | Praça XV ↔ Charitas (Niterói) | **825,637** | **R$7.70**, effective 2025-03-06 | demand `usable_for_base_case`; fare `benchmark_only`; DiDi/Navier entry `permission_required` | `t3_buildable_non_null` |
| `rn-00bb6ded4be5` | Praça XV ↔ Paquetá | **1,170,652** | **R$5.00**, effective 2026-02-08 | demand `usable_for_base_case`; fare `benchmark_only`; DiDi/Navier entry `permission_required` | `t3_buildable_non_null` |
| `rn-369ef0eb69d9` | Praça XV ↔ Cocotá | **278,607** | **R$5.00**, effective 2026-02-08 | demand `usable_for_base_case`; fare `benchmark_only`; DiDi/Navier entry `permission_required` | `t3_buildable_non_null` |
| `rn-aa790551baa7` | Club de Pesca Marina ↔ Bocachica (Tierrabomba) | **null** | **null** | service/demand/fare `not_publicly_supported`; entry `permission_required` | `t3_buildable_null_only` |

## Rio proof notes

- The annual figures are arithmetic sums of all 12 line-level monthly passenger totals in AGETRANSP’s January 2024 report, covering January–December 2023. They are **not** annualizations of a peak day, average day, or sample.
- The source describes passengers transported and reports bidirectional totals by line. Each count is treated as one one-way passenger-trip/boarding. No directional split was available, and no count was doubled or halved.
- Reconciliation flag: AGETRANSP’s separate 2023 all-system annual table reports 13,428,425, while the twelve monthly all-system totals sum to 13,331,608, a difference of 96,817. No route-level correction is public, so the difference was **not allocated** across lines. This is recorded as `conflicting`, separate from the four line sums.
- The R$5.00 and R$7.70 values are passenger-facing official tariff benchmarks, not realized operator yield. Payment mix, concessions/gratuities, integration, subsidy/availability payment, and audited route revenue are absent. Do not multiply every passenger by the tariff as audited revenue.
- AGETRANSP/state contract evidence proves incumbent regulation/operation, not permission for DiDi/Navier to enter or run the routes.

## Cartagena / La Bodeguita

- **Exact BP found — `usable_for_base_case` as a terminal point only.** CARDIQUE Resolution 0020 (2024-01-12), following a 2024-01-11 site visit, identifies **Muelle Turístico La Bodeguita**, Centro, Avenida Blas de Lezo, at **10°25′11.04″N, 75°33′4.56″W**. Arithmetic decimal conversion: **10.4197333333, -75.5512666667**.
- The record says the terminal has four sectors (Delta, Alfa, Bravo, Charly), but does not map Rosario or Isla Grande to a particular berth.
- The official tourism bulletin reports **619,282 passenger entries at La Bodeguita in 2023**. Classification: `benchmark_only` aggregate terminal context. It cannot be mapped 1:1 to Rosario, Isla Grande, Bocachica, or `rn-aa790551baa7`.
- **Rosario vs Isla Grande destination split: `not_publicly_supported`.** The older district mobility study gives only an aggregate La Bodeguita–Islas del Rosario observation of 818 passengers/day. It is an old base-2012 planning observation, not an annual exact-destination count; it was not annualized or split.
- For `rn-aa790551baa7`, La Bodeguita–Bocachica evidence has the wrong origin. No substitution for Club de Pesca was made.

## Barranquilla Río-Bus

- **Current operation: `current_ops_proof_only`.** A Transmetro official post dated 2025-11-14 says Riobús Karakalí operates Wednesday–Sunday, departures 15:00–20:00, last admission 19:00, with same-day ticketing at Muelle Puerta de Oro. An Alcaldía page dated 2026-03-31 independently tells visitors they can board Riobús Karakalí at Puerta de Oro for river excursions.
- The 2026 page does not restate an endpoint or fare. A 2023 start-up announcement gave Puerta de Oro → Intendencia Fluvial and an initial COP6,000 tariff; these remain **historic benchmarks**, not proof of the current exact OD or current realized yield.
- Annual route-level passenger demand remains `not_publicly_supported`. No service schedule was converted into demand.

## Country-reference opex fields

Official reference systems were identified, but **no values were fabricated or selected without the required local scope**:

- **Brazil fuel:** ANP series — municipality, exact product, retail/distribution level, BRL/litre, week/month.
- **Brazil electricity:** ANEEL — actual terminal distributor, group/subgroup, voltage, modality/time band, taxes/flags, BRL/kWh, effective dates.
- **Brazil labor:** RAIS/CAGED — CBO occupation, CNAE, city/state, remuneration, hours/contract, period; PGFN/employment rules for employer pension, RAT, FGTS, third-party levies, benefits, 13th salary and vacation accrual.
- **Colombia fuel:** MinEnergía/SICOM — municipality, exact fuel product, retail/wholesale level, COP/unit, surcharge/tax, month.
- **Colombia electricity:** SUI — provider, municipality/market, user class, voltage/tariff option, CU/components, COP/kWh, month.
- **Colombia labor:** DANE GEIH — occupation/industry, city, status, income, hours, period; UGPP for IBC, health, pension, ARL class, compensation fund and parafiscales.
- **Colombia maritime fees:** DIMAR 2026 price list — exact vessel/service category, inspection/certificate/permit item, UVB/tariff unit and frequency.
- Still requiring primary quotes/contracts: maintenance/spares, insurance, dock/berth charges, route/operator permits, financing/depreciation, communications/ticketing, taxes, and FX/indexation.

## Failed searches retained

1. No public source reconciled the 96,817-passenger difference between AGETRANSP’s annual and monthly system totals; it was not allocated.
2. No primary Rosario-versus-Isla-Grande passenger allocation was found.
3. No exact `rn-aa790551baa7` current schedule, annual demand, official fare, or operator authorization was found.
4. Río-Bus current operation is supported, but current endpoint, current fare, annual demand, and a sealed Atlas route are not.
5. No route-level realized operator yield was found for any route.

No repository production files, finance models, partner JSON, Sheets, PRs, Slack, or external services were edited.