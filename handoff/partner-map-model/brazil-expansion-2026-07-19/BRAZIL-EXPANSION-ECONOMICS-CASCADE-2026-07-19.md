# Brazil expansion — economics cascade record (2026-07-19)

Cascade run after Grok seal (`BRAZIL-EXPANSION-SEAL-RECEIPT-2026-07-19.json`) and fare-anchor
approval (`FARE-ANCHORS-2026-07-19.md`, Santos revised $12 in PR #297). FX locked 5.0727 BRL/USD.
All figures MID scenario. Country-reference gate: PASS (errors: []) for both partners.

## Corridors added to shared `brazil` market (finance/model/corridors.json) — 9 new, 16 total

**In grounded floor (5):**
| route_id | corridor | nm | pax/yr | basis | fare |
|---|---|---|---|---|---|
| rn-4aa1660ff921 | São Joaquim ↔ Bom Despacho (Salvador) | 6.31 | 7,490,000 | T1/T2 MTur 2025, COMBINED system (incl. Mar Grande lancha) | $15 |
| rn-1d1a798e7d82 | São Sebastião ↔ Ilhabela | 1.18 | 1,493,447 | T3 modeled from Semil T1 inputs (ped+cyc only, conservative) | $15 |
| rn-07cdabeba7a9 | Santos Ponta da Praia ↔ Guarujá | 0.25 | 5,584,500 | T2/T3, 15,300 ped+cyc/day × 365 | $12 |
| rn-1ff034e787c5 | Vila Velha (Prainha) ↔ Vitória (Praça do Papa) | 3.49 | 500,000 | T1 SEMOBI year-one official | $20 |
| rn-d0bee9173524 | Pontal do Sul ↔ Ilha do Mel (Nova Brasília) | 3.82 | 383,162 | T1/T2 Abaline 2025, direction split unavailable → conservative | $12 |

**Held at null demand (4, fail-closed):** rn-c6d5aa38e4dc (Mar Grande — embedded in combined
series), rn-8dbc3663c115 (Morro de São Paulo — no citable annual series; Observatório PDFs
unreachable 2026-07-19, retried; fare $30 banked), rn-3a67668a48a5 (Vicente de Carvalho — no
per-line series), rn-f405c4df3ed2 (Encantadas — embedded in Abaline series). Held corridors
contribute zero pax/fleet/revenue in both engines (verified: vessels_supported = null).

## Brazil floor (was → is)
- Grounded floor market revenue: **$56.63M → $77.93M** (+$21.3M)
- Fleet: **199 → 333** vessels (+134)
- Transport spend pool: **$573.5M → $789.9M**
- Corridors: 7 → 16 (12 in floor) · Cities with floor economics: 3 → **8**
- Effective capture 0.0987 (contested). Parity: didi `brazil` ≡ indrive `indrive-brazil` (shared canonical basis).

## Brazil TAM ladder (MID, template greenfield 4.9×, same basis as shipped ladder)
| Rung | was | is |
|---|---|---|
| SOM grounded floor | $56.6M | **$77.9M** |
| SAM Navier transport | $1,264.6M | **$1,741.7M** |
| Marine-mobility TAM | $5,063M | **$6,966.9M** |
| TAM journey GMV | $15,175.6M | **$20,900.6M** |
| Network journey GMV | $3,793M | **$5,225.2M** |
| DiDi platform (18%) | $682.9M | **$940.5M** |

inDrive Brazil: same anchor, stops at Journey GMV **$20.9B** (no platform rung — DiDi-only).

## New-corridor unit economics (MID, per boat, Pioneer II, CAPEX $600K non-US/EU)
| corridor | rev/boat-yr | opex/yr | margin | payback | vessels | corridor rev/yr |
|---|---|---|---|---|---|---|
| Salvador São Joaquim↔Bom Despacho | $164,538 | $80,506 | 51.1% | 7.14 yr | 68 | $11.19M |
| São Sebastião↔Ilhabela | $176,352 | $78,662 | 55.4% | 6.14 yr | 12 | $2.12M |
| Santos↔Guarujá | $141,082 | $78,298 | 44.5% | 9.56 yr | 47 | $6.63M |
| Vitória↔Vila Velha | $235,136 | $79,567 | 66.2% | 3.86 yr | 4 | $0.94M |
| Pontal do Sul↔Ilha do Mel | $141,082 | $79,696 | 43.5% | 9.77 yr | 3 | $0.42M |

Existing corridors unchanged: Rio (Arariboia) $329,190 / 75.9% / 2.40yr / 92 boats; Angra $235,092 /
65.3% / 3.91yr / 2; Floripa R3+R4 $235,136 / 65.9% / 3.87yr / 33+51.

## Artifacts refreshed
- `finance/model/corridors.json` (canonical, +9 corridors)
- `finance/recal/corridors-didi.json`, `corridors-indrive.json` (scoped views, +9 each)
- `finance/recal/agg-didi.json`, `agg-indrive.json` (aggregates)
- `finance/recal/growth-didi.json`, `growth-indrive.json`, `growth-frontend-didi.json`, `growth-frontend-indrive.json`
- `partner-pitch/partners/didi.json`, `indrive.json` (growth_case spliced, 6 rungs / 5 transitions)
- Transparent sheets uploaded in place: didi `1LY0Vp7FskgDDnEixkrEUCH0m-A_pYd2YCNuq3LF8ESM` (v76), indrive `1xo2a-XalddB6kRiLKzB7RIrV-u29LJmt3N2zc7ik3_k` (v24), master tracker (v185)
- Engine outputs banked: `/tasklet/agent/home/brazil-expansion/{agg-didi-exp,aggB-exp,GB-exp,new-corridor-unit-econ-MID}.json`

## For Grok (next seal lane)
Economics sidecar (`economics_by_route_id.json`) is stale for the 9 new route IDs — rebuild into the
next gold zip from the refreshed `agg-*.json`. No geometry change.
