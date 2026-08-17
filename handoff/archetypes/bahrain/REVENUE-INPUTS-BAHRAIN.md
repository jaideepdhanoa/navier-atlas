# REVENUE-INPUTS-BAHRAIN (internal audit file — does not render)

Researched 2026-08-16. Inputs only — **no P&L computed here** (later stage). Basis: **N45, 20 seats, $2.5M capex (canon), 16-hr service day** structure per CITY-RESEARCH-TEMPLATE + INTERNATIONAL-ADDENDUM. Peg 1 BHD = USD 2.6596. Every line: value + source + tag.

## 1 · Vessel & structural canon
| Input | Value | Tag |
|---|---|---|
| Hull for stack | N45, 20 seats, $2.5M capex | CANON |
| Service speed | 25 kn (20 kn cruise) | CANON |
| Energy intensity | N45 4.1 kWh/nm · N30 1.6 kWh/nm | CANON |
| Service day | 16 hr, four-layer stack (L1 committed / L2 spot / L3 experiences / U1 sponsorship / U2 cargo) | CANON (Boston grammar) |
| Maintenance | $65K/yr (N30-class canon, scaled at model stage) | CANON |
| Navier network share | 10% of revenue | CANON |
| Network geometry | 4 lines, 14 nodes, legs ≤15 nm (NODES-BAHRAIN.md) | DERIVED (this research) |

## 2 · L1 — Committed seat bundles ($/seat-month) — **DERIVED band, flag for Jaideep**
Derivation chain (all anchors in FARE-BENCHMARKS / DEMAND-POOLS):
- Ride-hail/taxi commute substitute (Amwaj↔CBD): BHD 2.5–4.4/trip (Careem SECONDARY; MTT meter PRIMARY-derived) → 44 trips/mo = **BHD 110–194/mo = $293–515/mo** door-to-door road cost.
- Current public water taxi: BHD 0.8–1.5/leg (PRIMARY) → BHD 35–66/mo equivalent = $94–176 — the subsidized-style floor.
- Income context: avg private wage BHD 892/mo ($2,372, SECONDARY); target pools (BFH finance, Amwaj/Reef/Diyar residents, 1BR rents BHD 350–500) are 2–4× that.
- Canon cross-check: NY $650–900, Bay Area $800–1,200 — Bahrain's substitute costs are ~⅓ of US metros, so the band must sit well below US canon.

**Recommended committed-seat band: $220–330/seat-month (LOW $220 · MID $275 · HIGH $330 ≈ BHD 83–124/mo).** Position: ~2.5–3× the public water-taxi monthly equivalent, at/below the ride-hail commute cost it replaces, ~4–5% of a target-segment household income. Tag: **DERIVED — requires Jaideep confirmation before any rendered use.**

## 3 · L2 — Spot seats per leg (DERIVED from fare anchors)
| Segment | One-way seat | USD | Anchor logic |
|---|---|---|---|
| BH-1 urban legs (0.2–1.3 nm) | BHD 2 std / BHD 3–4 premium | $5.3 / $8.0–10.6 | 2.5× Masar std fare (PRIMARY anchor BHD 0.8); below ride-hail door-to-door |
| BH-2 Amwaj→BFH through-ride (9.8 nm) | BHD 3–5 | $8.0–13.3 | vs BHD 2.5–4 Careem flat + parking/time |
| BH-3 southern legs (BFH→Al Dar/Durrat) | BHD 6–10 | $16–27 | vs Al Dar entry BHD 5–8 (incl. their shuttle), taxi south BHD 8–12 |
| BH-4 Hawar express (14.6 nm) | BHD 12–18 | $32–48 | vs BHD 20 day-trip bundle (SECONDARY-operator), ferry benchmark $1.37/pax-nm (DERIVED) → 14.6 nm ≈ $20 at ferry parity; premium foiling 1.5–2.5× parity |
All DERIVED; label every rendered price "indicative."

## 4 · L3 — Experiences / charter (tourism-weighted headline layer, per addendum)
| Input | Value | Tag |
|---|---|---|
| N45 charter-hour rate | **BHD 80–130/hr ($213–346), MID BHD 100 ($266)** | DERIVED (from BHD 20–72/hr conventional charters SECONDARY; BHD 77/hr yacht-hour SECONDARY; FS $180/hr PRIMARY-operator) |
| Marquee products | Jarada sandbank anchorage runs (no fixed landing — charter only); Hawar nature/resort experiences; Bahrain Bay sunset circuits; F1-week shuttles+charters (105K weekend attendance PRIMARY) | Sourced in FARE/DEMAND files |
| Sourced yield justification for headline treatment | 14.88M visitors 2024 (PRIMARY data.gov.bh); sea-mode arrivals 205K and 3× YoY growth (PRIMARY); Hawar Resort open with boat-only access (PRIMARY) | PRIMARY |

## 5 · U1 / U2 (upside-only)
- U1 sponsorship: waterfront brand economy exists (Avenues, Marassi Galleria, F1 sponsors) — no sourced rate; carry as upside-only, UNSOURCED rate.
- U2 cargo: courier-linehaul class inappropriate for Bahrain's short road network except Hawar resupply (boat-only island, resort open — PRIMARY). Carry "Hawar clean resupply" as the city-appropriate U2, rate UNSOURCED, upside-only.

## 6 · Season & demand shape (12-month year, addendum shape)
| Input | Value | Tag |
|---|---|---|
| Operating year | 12 months (no winter discount) | ADDENDUM CANON |
| Summer shape (Jun–Sep) | Midday leisure dip, evening peak; commuter peaks intact (a/c cabin mitigates but does not remove the shape) | DERIVED (Gulf norm; Masar's own hours are afternoon–evening weighted: Sun–Thu 14:30–21:45 — PRIMARY signal) |
| Ramadan (~1 month, moves annually) | Daytime demand suppressed; post-iftar surge into late evening | DERIVED — **collides with MOI night-ban risk; see next line** |
| Night-ops constraint | MOI Coast Guard night maritime bans (18:00/18:30–04:00) announced 2025 "until further notice" — status unresolved. Until cleared, model service day as 06:00–18:00 effective (12 hr) in a sensitivity, 16-hr day as base | PRIMARY/SECONDARY (SPEED-RULES §1.2) — **top modeling risk** |
| Weekend shape | Fri–Sat leisure peak; Saudi causeway influx (≈32.9M pax/yr over causeway, SECONDARY-of-official) | SECONDARY |

## 7 · Opex inputs
| Input | Value | Source / Tag |
|---|---|---|
| Crew, 2-person, loaded | LOW $11.2/hr · MID $16.8/hr per crew pair → **$180–269 per 16-hr service day** (two shifts) | CREW-COST file — SECONDARY wages + DERIVED burden 1.35 |
| Energy tariff | **$0.0851/kWh** (EWA non-domestic >5,000 kWh/mo, 32 fils) — cheaper than $0.30 canon → use sourced tariff per addendum rule | PRIMARY (ewa.bh/en/tariff) |
| → N45 energy per nm | 4.1 kWh/nm × $0.0851 = **$0.35/nm** | DERIVED from PRIMARY tariff + canon intensity |
| → N30 energy per nm | 1.6 × $0.0851 = $0.14/nm | DERIVED |
| Sensitivity: marina shore-power resale markup | +20% ($0.102/kWh) | UNSOURCED — sensitivity only |
| Berthing (BFH/Amwaj/Durrat commercial berth for 45-ft class) | **UNSOURCED — no published rate cards found; fail closed, obtain quotes** (do not borrow US canon) | UNSOURCED |
| Insurance (hull+P&I, Bahrain flag, passenger ops) | **UNSOURCED — fail closed, obtain quotes** | UNSOURCED |
| Maintenance | $65K/yr canon (N30-class, scale for N45 at model stage) | CANON |
| Network share | 10% of revenue | CANON |
| Registration/licensing | Small-ship registration + master/navigation licences (Decree 32/2020) — fee schedule not pulled; minor | PRIMARY process / UNSOURCED fees |

## 8 · Demand-pool linkage (indicative only — no invented demand)
Demand pools feeding L1/L2 sizing at model stage (all labeled indicative, sources in DEMAND-POOLS-BAHRAIN.md): BFH/CBD professionals (SECONDARY headcount), Amwaj ~10K+ residents (SECONDARY-dated), Diyar/Marassi residents+resort guests (developer PRIMARY), Durrat planned 60K (SECONDARY-planned), 14.88M visitors/yr with 205K by sea (PRIMARY), Hawar Resort 136 keys boat-only (PRIMARY/SECONDARY), F1 105K weekend (PRIMARY), causeway ≈32.9M pax/yr (SECONDARY-of-official). **No corridor-level ridership figures exist — the model must derive demand from these pools with explicit capture assumptions, labeled.**

## 9 · Fail-closed list (this file)
1. Berthing rates — UNSOURCED (quotes needed).
2. Insurance — UNSOURCED (quotes needed).
3. MOI night-ban status — unresolved; run 12-hr-day sensitivity.
4. Seat-band, spot fares, charter rate — all DERIVED; Jaideep confirmation required before rendering.
5. Marina shore-power resale rate — UNSOURCED.
6. Registration/licence fee schedule — UNSOURCED (minor).
