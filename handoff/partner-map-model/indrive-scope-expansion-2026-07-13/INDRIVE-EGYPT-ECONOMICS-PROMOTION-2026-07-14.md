# inDrive Egypt — luxury-belt economics promotion (2026-07-14)

Builds on `INDRIVE-EGYPT-EVIDENCE-LEDGER-2026-07-13.json`, which held all Egypt routes
because demand values were destination pools (not observed boardings) and fares were
day-trip / Dubai / legacy proxies. The July-13 `must_remain_null` list permitted promotion
once **an explicit, approved destination-pool methodology and exact one-way local fares**
were accepted. Jaideep approved conveying Egypt luxury-belt unit economics on 2026-07-14.
This pass records the improved sourcing, the labeled methodology, and the computed per-boat
economics, and promotes the two best-evidenced routes.

## What changed since 2026-07-13

| Route | July-13 status | New evidence (2026-07-14) | Decision |
|---|---|---|---|
| `rn-b06f6971ed47` Hurghada → Giftun Island | Held. Demand was Hurghada airport pool × 25% (~1,204,586). | **~187,512 published annual Giftun Island visitors (~12% of Red Sea Governorate visitors)** — a real published island figure, ~6.4× lower than the old proxy. | **Promote** on labeled destination pool + premium day-trip per-seat fare. |
| `rn-c16a1627130f` Sharm → Ras Mohammed | Held. 50,000 visitor pool, single-source. | **~50,000 annual Ras Mohammed National Park visitors, corroborated across independent operators.** | **Promote** on labeled destination pool + premium/VIP per-seat fare. |
| `rn-3d161664de08` Hurghada → Sahl Hasheesh | Held. | No route-level count/fare sourced this pass. | **Hold.** |
| `rn-173d32792c07` Hurghada → Soma Bay | Held. | Fare was Dubai placeholder; demand room-pool only. | **Hold.** |
| `rn-285fc16b29dc` Sharm → Sharks Bay | Held. | No route-level count/fare sourced this pass. | **Hold.** |

## Methodology (labeled, approved)

- **Demand** = published annual destination-pool visitors, treated conservatively as **one
  outbound one-way trip per visitor** (no return-leg doubling). This is an addressable pool,
  **not** observed route boardings — labeled as such everywhere.
- **Fare** = a premium per-seat price **within the observed live day-trip market range** for
  each corridor. It is a premium-product fare, not a scheduled ferry tariff.
- **Per-boat unit economics** (the deck headline) are **fare-driven and grounded**: they use
  the canonical Egypt country-reference cost row + validated global constants and do **not**
  depend on the demand pool. Only the market-scale (vessels / market revenue) figures use the
  labeled pool × a conservative 10% capture.

## Computed per-boat unit economics (N30 Pioneer II, 45% load, 12-hour schedule)

Engine replicated from the live model and **validated against the Rio representative route**
(`rn-1886629dbf0c`: reproduced opex $79,094 exact; payback 8.92 vs 8.91 published).

| Route | nm | Fare | Pax/boat/yr | Rev/boat | OPEX/boat | EBITDA/boat | Margin | Payback |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Hurghada → Giftun | 6.6 | $32 | 7,588 | $242,827 | $73,959 | $168,868 | 70% | **3.55 yr** |
| Sharm → Ras Mohammed | 11.7 | $50 | 5,962 | $298,114 | $74,494 | $223,620 | 75% | **2.68 yr** |

OPEX lines (per boat/yr): energy ~$1,359–1,894 · crew $21,600 · marina/overhead $8,000 ·
maintenance $10,000 · insurance $15,000 · charging berth $18,000. At a fuller (realistic)
55% load, paybacks fall to ~2.7 yr (Giftun) and ~2.1 yr (Ras Mohammed).

Full numbers, provenance, and the Rio validation are in
`INDRIVE-EGYPT-UNIT-ECONOMICS-RECEIPT-2026-07-14.json`.

## Cairo and Alexandria

- **Cairo** — distribution context only. Egypt's Nile waterway is a different thesis from the
  Red Sea excursion corridors; no marine boarding points, route IDs, or route-level
  demand/fare exist. Remains null; not added to the deck.
- **Alexandria** — researched as a candidate. Public evidence shows a cruise-ship port and
  ~$5 Corniche harbour rides, but **no scheduled marine network with published route-level
  volumes**. Held as candidate/null; not minted. Would require boarding-point/route minting
  in canonical geography first, then route-level demand/fare, before any economics.

## Geography-owned reconciliation note

Giftun and Ras Mohammed are shared Red Sea geography also referenced by `bolt-egypt` and
`yango-egypt`. Per the corridor-inheritance discipline, the improved Giftun figure (187,512,
replacing the 1.2M airport-pool proxy) and the corroborated Ras Mohammed count should be
cascaded consistently to the bolt and yango Egypt corridor records as well.

## Sources added this pass

- Giftun Island annual visitors (~187,512; ~12% of Red Sea Governorate): Egypt Tours Portal
  — https://www.egypttoursportal.com/ (accessed 2026-07-14).
- Ras Mohammed National Park ~50,000 annual visitors: Jakada Tours Egypt
  — https://jakadatoursegypt.com/ras-mohammed-national-park/ (accessed 2026-07-14), corroborated.
- Live day-trip fare ranges (Hurghada/Giftun ~$23–52; Sharm/Ras Mohammed ~€12–52): multiple
  operator listings (accessed 2026-07-14).
