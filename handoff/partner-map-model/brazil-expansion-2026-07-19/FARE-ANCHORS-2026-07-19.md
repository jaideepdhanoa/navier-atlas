# Brazil expansion — premium fare anchors (approved batch, 2026-07-19)

Approved by Jaideep 2026-07-19 (batch approval alongside PR #296, same pattern as DiDi Mexico $30).
Basis: premium-substitute benchmarking (per standing economics policy). FX locked: **5.0727 BRL/USD** (BCB PTAX sell 2026-07-15). All anchors are **one-way per-passenger legs, USD, MID scenario**.

Existing sealed anchors (unchanged): Rio corridors; Angra–Abraão **$30**; Florianópolis R3/R4 **$20**.

| # | Market / corridor family | Anchor (USD/leg) | Primary evidence (live, sourced in demand record) |
|---|---|---|---|
| 1 | **Salvador — Morro de São Paulo corridor** | **$30** | Live direct catamaran R$138.75–152 one-way (agency all-in to R$172.51) = US$27.35–34.01 on the exact water corridor, 3+ departures/day. Strongest premium anchor in Brazil. |
| 2 | **Salvador — bay crossings** (Náutico↔Mar Grande, São Joaquim↔Bom Despacho, Itaparica/Ilha dos Frades hops) | **$15** | Schooner island day tours US$17.74–35.49 pp on the same waters; AGERBA's own Hora Marcada +30% queue-skip tariff proves regulated premium willingness; sits well above the $1.42–2.60 commodity ferry/lancha floor and below live tour pricing. |
| 3 | **São Sebastião–Ilhabela** (channel crossing + island pier hops) | **$15** | Official Hora Marcada queue-skip R$65.30–98/car = US$12.87–19.32 (3.4× standard — state-published willingness-to-pay); Aquabus single ticket US$3.94 (Jan-2025 tourist decree tariff ~US$9.86); Castelhanos speedboats US$57–61 pp ceiling; new R$48 vehicle-entry TPA fee favors passenger-first water mobility. |
| 4 | **Santos–Guarujá** (incl. Vicente de Carvalho and marina/cruise spurs) | **$12** | Uber's published tier ladder for the Guarujá→Santos road detour (Uber route page, Jul 2026): UberX R$44 = US$8.67 → Comfort R$52 = US$10.25 → Bag R$63 = US$12.42 (top listed passenger tier; Uber Black is not offered on this corridor). $12 = top-of-ladder equivalent per premium-substitute policy. Free 2026 pedestrian balsa noted: positioning is speed/comfort/marina, not fare-versus-balsa. Context ceiling: São Paulo→Santos ride-hail US$42.98 (cruise transfers). *Revised $10 → $12 on 2026-07-19 (Jaideep approved): $10 was Comfort-tier equivalent; $12 matches the highest listed tier on the corridor.* |
| 5 | **Vitória–Vila Velha** (bay corridors) | **$20** | Live shared premium lancha on the exact bay: R$139–169 pp = US$27.40–33.32 (Capitão Grilo, Jul 2026 departures); matches Floripa $20 urban-corridor precedent; regulated aquaviário US$1.01 is the public-transit baseline, not the substitute. |
| 6 | **Ilha do Mel** (Pontal do Sul↔island piers) — **PROMOTED to full economics** | **$12** | Market one-way already US$9.66 (2025/26 season average); AGEPAR-homologated nautical-taxi premium tier R$69.07 RT = US$13.62; $12/leg is a modest premium over the current market one-way for a faster, cleaner, bookable service. Demand basis: **383,162 boat boardings 2025** (Abaline) + 247,020 park visitors 2025 (IAT). |

## Economics lanes after this approval
- **FULL T1 (5 markets):** Salvador, Santos–Guarujá, São Sebastião–Ilhabela, Vitória–Vila Velha, **Ilha do Mel** (promoted from hold).
- **HOLD:** São Luís–Alcântara (no recent annual series), Porto Alegre–Guaíba (CatSul series unpinned).
- **Display-only (null economics):** Búzios/Cabo Frio/Arraial, Paraty, Recife (parked basis).
- **Out of scope (Amazon lane):** Belém, Manaus — geometry/brief presence only.

## Cascade order (per partner-model-cascade skill)
1. Jaideep merges PR #296 → Grok seal returns route IDs + sealed nm distances.
2. Corridors built for the 5 T1 markets with these anchors, locked FX, MID scenario.
3. `finance/model/corridors.json` → single-market rollups → `growth.py --agg` → TAM ladders.
4. Cascade into **both DiDi Brazil and inDrive Brazil** (shared canonical basis), sheets, and master tracker.
