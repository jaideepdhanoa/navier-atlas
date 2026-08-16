# New York speed & wake rules — corridor-by-corridor (v3 pipeline)

**Date:** 2026-08-16 · **Status:** research-complete, source-verified desk pass (web) · **Scope:** the 9-line / 38-station network in `hub.json` (East River trunk, Hudson spine, Brooklyn, East River Feeder, Connecticut Express, Long Island Sound, Bronx, Staten Island, East End Seasonal).
**Fail closed:** every claim carries a URL or is marked **unverified**. Base schedule math in `hub.json` and the revenue stack ALWAYS respects the rules below as posted; the "what relief unlocks" section is labeled upside only, per ARCHETYPE-STRATEGY.md §4b.

## 1 · The headline finding (different from Boston)

**New York Harbor has no standing harbor-wide numeric speed limit for the open water of the East River, Hudson River, Upper Bay, or Long Island Sound that this pass could locate in current law.** The binding constraints on Navier corridors are (a) near-shore/near-dock distance bands (NY 5 mph within 100 ft; NJ slow-no-wake within 200 ft), (b) the federal safe-speed duty, (c) VTS New York participation rules that the N45 falls *below*, and (d) episodic federal safety/security zones. Consequence: **the speed-relief upside that matters in Boston is largely moot in New York** — line-haul segments are already governed by safe-speed judgment, not numeric caps. The rules bind at dock approaches, which every schedule must respect anyway.

## 2 · Controlling rules, by layer

### Federal — Coast Guard / COLREGS

| Rule | What it says | Applies to Navier? | Stated purpose | Source |
|---|---|---|---|---|
| Inland Navigation Rule 6 (safe speed) | Every vessel shall proceed at a safe speed for conditions, traffic, visibility | Yes, always — judgment standard, not a number | Collision avoidance | https://www.navcen.uscg.gov/navigation-rules-amalgamated |
| VTS New York, 33 CFR Part 161 | Vessel Traffic Service covering the Port of NY/NJ; VTS/VMRS Users must monitor/report | **N45 is below every applicability threshold** of 33 CFR § 161.16: (a) power-driven ≥40 m, (b) towing ≥8 m, (c) certificated for **50+ passengers** for hire. A 20-pax N45 / 8-pax N30 is not a required participant (voluntary monitoring is good practice; confirm at COI certification) | Traffic organization in the harbor | https://www.law.cornell.edu/cfr/text/33/161.16 · https://www.ecfr.gov/current/title-33/chapter-I/subchapter-P/part-161 |
| 33 CFR § 165.165 — RNA, Hudson River south of Troy Locks | Restrictions apply **to tugs <3,000 hp when towing** | No — passenger vessels out of scope | Towing safety | https://www.law.cornell.edu/cfr/text/33/165.165 |
| 33 CFR § 165.166 — **now** "Safety Zones; COTP New York Zone Drone Displays" (Aug 2024) | Episodic 500-yd drone-show safety zones on Hudson/East River, enforced only when noticed | Only during enforcement windows | Event safety | https://www.law.cornell.edu/cfr/text/33/165.166 (Doc. USCG-2024-0225, 89 FR 68104) |
| Historical East River RNA (former § 165.166, 2002 CFR edition) | "Vessels transiting Area A must do so at no wake speed, or speeds not to exceed 10 knots, whichever is less" | **Superseded** — the section number now holds the drone-display rule above; no standing numeric East River speed RNA was located in the current Part 165 this pass. **Verify with USCG Sector New York before any in-page claim about East River speed law.** | Wake/safety in the constricted East River | https://www.govinfo.gov/content/pkg/CFR-2002-title33-vol2/pdf/CFR-2002-title33-vol2-sec165-166.pdf |
| Temporary/episodic zones (precedents) | 2017 East River RNA (bare steerage/no-wake, Manhattan side, Brooklyn–Williamsburg bridges) during the Con Ed dielectric-oil spill; 2021 Roosevelt Island safety zone; UN General Assembly security zones (E 35th–Queensboro); drone/fireworks zones | Episodic only — schedule-resilience issue (UNGA week affects E 34th/E 90th), not a standing limit | Incident/event control | https://content.govdelivery.com/accounts/USDHSCG/bulletins/19b413c · https://www.federalregister.gov/documents/2021/05/26/2021-11103/safety-zone-east-river-new-york-ny · https://oceancruisingclub.org/home/News/113 |

### New York State

- **Navigation Law § 45:** no vessel may exceed **5 mph within 100 feet of the shore, a dock, pier, raft, float, or an anchored/moored vessel**. This is the operative near-dock rule at every NY stop (Pier 11, E 34th, E 90th, BPC, Pier 79, Brooklyn stops, Roosevelt Island, Bronx stops, St. George, Yonkers, New Rochelle, Glen Cove, Port Washington, East End). Statewide; enforced by local harbor units/police. Source: https://www.nysenate.gov/legislation/laws/NAV/45
- No NYC-specific numeric harbor speed ordinance beyond § 45 was located this pass (**unverified whether NYC Parks/NYPD Harbor impose additional posted zones at specific landings** — verify per-landing during ops planning).

### New Jersey (Hudson spine, seven stops)

- **N.J.A.C. 13:82-1.7:** vessels must reduce to **slow speed / no wake when passing within 200 feet of any marina, pier, dock, wharf, or abutment**. This is the operative rule at Paulus Hook, Newport, Liberty Landing, Hoboken (both), Lincoln Harbor, Port Imperial, Edgewater — and note the NJ Gold Coast is nearly continuous marina/pier frontage, so the practical no-wake band along the NJ bank is wide. Enforced by NJ State Police Marine Services. Source: https://www.law.cornell.edu/regulations/new-jersey/N-J-A-C-13-82-1-7
- The rule is **explicitly wake-framed** ("slow speed/no wake"), the cleanest fit in this market for the foiling low-wake argument (§4).

### Connecticut (NY-C Express: Greenwich, Stamford, Norwalk, Milford, Bridgeport)

- CT harbors are governed by **CGS Chapter 263 (Harbors and Rivers)** — state-appointed harbormasters for Stamford, Norwalk, Bridgeport, etc., with statutory authority over vessel speed in harbor limits; specific slow-no-wake zones are set per harbor. Source: https://www.cga.ct.gov/2023/pub/chap_263.htm
- Per-harbor posted zones (e.g., Norwalk Harbor's posted no-wake) are locally set and were **not primary-verified this pass** — the schedule assumption used in `hub.json`-derived math is harbor-speed inside breakwaters/channel entrances at all five CT stops, full foiling speed only in open Long Island Sound. **Verify each harbor's ordinance before publishing CT segment times.** (Secondary indication of ~5 mph/no-wake norms: town boating pages, e.g., https://www.branford-ct.gov/253/Boating-Regulations.)

### Specific water bodies flagged in the corridor set

- **Hell Gate (NY-M north of E 90th, NY-X, NY-G, NY-C all transit it):** no numeric speed limit located; the controlling realities are 4–6 kn tidal currents and commercial traffic (secondary: https://www.amnautical.com/blogs/the-mariners-blog/cruising-new-yorks-east-river). VTS NY manages large-vessel traffic; the N45 is below participation thresholds. Schedule buffers, not speed caps, are the design constraint.
- **Buttermilk Channel (NY-B Red Hook segment):** a federal navigation channel (USACE-maintained, https://www.nan.usace.army.mil/Media/Fact-Sheets/Fact-Sheet-Article-View/Article/487499/fact-sheet-buttermilk-channel-new-york/); no standing speed rule located — episodic safety zones only (e.g., 2017: https://www.federalregister.gov/documents/2017/06/02/2017-11463/safety-zone-east-river-and-buttermilk-channel-brooklyn-ny). NYC Ferry runs it daily at service speed — operating precedent.
- **East River generally:** NYC Ferry and SeaStreak run the full trunk at service speeds today; that operating precedent, plus the absence of a located standing numeric rule, is the basis for the hub.json trunk times. Flag: the historical 10-kn RNA text means Sector NY institutional memory may still treat parts of the East River as speed-sensitive — **engage Sector NY early**.

## 3 · Who sets and enforces what (summary table)

| Zone | Rule | Number | Setter | Enforcer | Purpose as stated |
|---|---|---|---|---|---|
| Within 100 ft of any NY shore/dock/moored vessel | NAV § 45 | 5 mph | NY Legislature | NYPD Harbor, county/municipal marine units | Safety near shore |
| Within 200 ft of any NJ marina/pier/dock | N.J.A.C. 13:82-1.7 | slow/no wake | NJ Motor Vehicle Commission regs | NJ State Police Marine Services | Wake protection of structures/vessels |
| CT harbor limits | CGS ch. 263 + local | per harbor | Harbormasters/towns | Harbormasters, local marine police | Harbor safety |
| Open East River / Hudson / Upper Bay / LI Sound | Rule 6 safe speed | none | USCG | USCG Sector NY | Collision avoidance |
| Episodic zones (UNGA, events, incidents) | 33 CFR Part 165 actions | varies | USCG COTP NY | USCG | Event/incident safety |

## 4 · What relief unlocks (labeled upside only — mostly small in New York)

- **Base position:** all hub.json times respect the rules above; no relief is assumed anywhere.
- The NY/NJ near-dock bands are short (100–200 ft ≈ 15–30 seconds per call at 5 mph vs foiling speed) — **relief would unlock almost no schedule time on most corridors.** The honest NY pitch to authorities is therefore not "raise the number" but: (1) the NJ rule is already wake-based, and a foiling N45 at speed produces less wake than a displacement ferry at the same distance — invite NJSP/harbormasters to measure; (2) in CT harbors with long no-wake channels (Norwalk's channel, Stamford Harbor), measured-wake relief on the channel run could recover **2–5 min per CT call** — worth pursuing only after harbor-specific rules are primary-verified.
- Precedent to cite (per canon): Stockholm Route 89 Candela P-12 exemption (~22 kn in a ~12 kn zone, Länsstyrelsen; formal instrument unverified) — see `../SPEED-RULE-RELIEF-PRECEDENTS.md`.
- **Never** claim the East River is speed-capped (the located cap is historical) and never claim it is affirmatively uncapped (Sector NY verification pending) — until verified, corridor pages should stay silent on East River speed law and simply show schedule times.

## 5 · Open verification items

1. Current standing status of any East River speed/wake RNA — direct query to USCG Sector New York / review of full current 33 CFR Part 165 Subpart F NY sections.
2. Per-landing posted zones at NYC DOT/NYC Ferry landings (Pier 11, E 34th, E 90th) — NYC Parks/NYPD Harbor postings unverified.
3. CT per-harbor ordinances for all five NY-C stops; Glen Cove/Manhasset Bay/Echo Bay local zones for NY-G; Village/Town codes for the four East End seasonal stops.
4. Whether the N45's eventual COI keeps it under the 50-passenger VTS threshold configuration (it should at 20 pax; confirm at certification).
