# REVENUE-INPUTS — Red Sea Global (Fleet Investor economics inputs; NO final P&L here)

Internal audit file. Research date: 2026-08-16. Peg SAR 3.75/USD. Revenue shape: **destination-resort network, NOT commuter city market — no commuter seat bundles.** Tiers are **status-keyed to hotel-opening state, never year-keyed.** All demand chains from DEMAND-POOLS (indicative); all prices from FARE-BENCHMARKS (DERIVED bands, flagged for Jaideep confirmation).

## 1 · Revenue layers
| Layer | Definition | Pricing input | Sizing input | Tags |
|---|---|---|---|---|
| **L1 — Resort transfer contracts** | Contracted guest transfers (arrival/departure + inter-resort), priced per guest one-way, sold to RSG/resorts as the transfer product (guest pays resort; operator paid per seat or per movement) | **$140–200 per guest one-way (mid $170)**; private-vessel variant $1,200–2,000/movement | Outer-island arrival chain: 226 keys × occ × 1.9 pax ÷ 3.5 nights × 2 legs × (1 − seaplane share 30–40%) | Price DERIVED (FARE §5); demand DERIVED chain (DEMAND §5) |
| **L2 — Scheduled inter-island / experience seats** | Public scheduled hops on RSG-1/RSG-2 (Shura↔Ummahat↔Sheybarah loop), Triple Bay loop; discretionary trips | $80–150/seat/hop | 0.3–0.8 trips/guest-day across open water-served keys + 10–20% elective share of Shura keys | DERIVED |
| **L3 — Private charters** | Sunset/dive/island-hop charters (with Galaxea/WAMA tie-ins), premium buy-outs | $450–700/hr; half-day $1,800–2,800 | 1–3 charters/vessel-day in season; anchored to houseofsaud day-charter market + resort wallet | DERIVED; comparable SECONDARY |
| **U1 — Sponsorship (upside-only)** | Brand partnership on the destination fleet (luxury/sustainability halo) | unpriced | — | UNSOURCED — upside only |
| **U2 — Cargo: overnight resort resupply (upside-only)** | **Genuinely relevant here**: island resorts are resupplied by water from the mainland; silent overnight foiling linehaul on RSG-1/RSG-2 alignments | No sourceable rate found for RSG marine resupply [UNSOURCED → unpriced]; note existence of daily marine logistics under Coastal Transportation Services Co. (PRIMARY) | — | UNSOURCED — upside only |
| Staff shuttle (optional L1b) | Turtle Bay Village (6,000→14,000 residents, PRIMARY) ↔ island resorts staff runs — contract with RSG ops | Price per staff-seat well below guest fare; unpriced pending counterparty data | Sized from workforce pool | PRIMARY basis, UNSOURCED pricing |

## 2 · Occupancy driver (DERIVED chain, all links labeled)
`water transfer demand = keys_open(status tier) × occupancy × 1.9 guests/room ÷ 3.5-night stay × 2 legs + discretionary trips/guest-day`
- Occupancy bands [DERIVED planning assumptions; signals: 82% Eid peak Q1 2026, >50K tourists 2025 across nine resorts]: conservative 45% · mid 60% · upside 70%.
- Seaplane share of island arrivals 30–40% [DERIVED from dual-mode product at rsiairport.sa; no published split].
- Season: 12-month year, summer midday dip / evening peak (addendum canon); no winter discount.

## 3 · Status-keyed tiers (NO year commitments)
| Tier | Hotel state (from DEMAND §2) | Water-served demand base |
|---|---|---|
| **Conservative — "open today"** | 11 properties open at The Red Sea; water-served: St. Regis 90 + Nujuma 63 + Shebara 73 = **226 outer-island keys** + elective Shura share (~600–800 keys × 10–20%); AMAALA first vessels at Triple Bay loop only | ~75–85 contracted transfer legs/day + L2/L3 discretionary |
| **Mid — Phase 1 complete** | RSG current build-out complete: **18 hotels / ~3,000 keys** (The Red Sea) + AMAALA first wave **~650 keys**; Laheq marina open adds a stop | scale conservative chain by keys; add Triple Bay scheduled loop |
| **Upside — fuller build-out** | Toward 2030 vision: **50 hotels / 8,000 rooms** (The Red Sea), Triple Bay toward ~3,900–4,000 rooms; Thuwal gateway line active | full network; inter-destination roadmap legs still excluded from vessel economics (range) |

## 4 · Cost inputs (for the downstream stack — not assembled here)
| Input | Value | Source/Tag |
|---|---|---|
| Crew (2-person, remote-adjusted) | **LOW $23.9/hr · MID $41.9/hr**; per 16-h day $382 / $670 | CREW-COST file (SAUDI-ADAPTED + remote uplift, DERIVED) |
| Energy | 4.1 kWh/nm (N45 canon) × **$0.0853/kWh** proxy ≈ **$0.35/nm**; RSG off-grid microgrid may change actuals [flagged assumption] | CREW-COST §3, PRIMARY-derived tariff |
| Maintenance | **$82.5K/yr per vessel** | instruction canon for this market |
| Network share | **10% of revenue** | canon |
| Berthing | Shura 115–118 berths / AMAALA 10-ha marina exist [PRIMARY]; tariffs unpublished → placeholder from Jeddah-class marina benchmarks until counterparty data [UNSOURCED here] |
| Capex | N45 $2.5M (20 seats, 20 kn cruise / ~25 kn service); N30 8-pax for premium/low-volume legs | canon |
| Vessel-day | 16-hr service day; ~120–180 nm/vessel-day on RSG-1/RSG-2 duty cycles [DERIVED from NODES leg times] | DERIVED |

## 5 · Fit notes (audit only)
- L1 contract form matches RSG's existing product: transfers are pre-booked, resort-bundled fees (St. Regis fee schedule = SAR 1,370 RT). Navier seat pricing at $140–200/way holds guest price roughly at today's boat fee while delivering seaplane-class speed silently — the price does the brand's sustainability work.
- Thuwal: transfer is bundled in a SAR 120K/night buy-out — price-insensitive; one N30-class vessel service contract, priced per movement not per seat [DERIVED note].
- Fail-closed: no invented demand; Shura bridge means Shura keys are elective water demand only; B2 resort jetties and A7/A8 gateway landings excluded until verified; inter-destination (79 nm) excluded from vessel economics — roadmap only.
