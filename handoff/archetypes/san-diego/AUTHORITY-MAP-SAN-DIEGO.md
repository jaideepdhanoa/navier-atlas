# San Diego Bay Authority Map — Public Partners Research

> **Speed-rule relief map (doctrine: ARCHETYPE-STRATEGY.md §4b):** San Diego Bay's controlling speed rules are **numeric Port ordinances** (SDUPD Port Code §4.30/§4.35: 5 mph zones) layered on a **reasonable-and-prudent baseline** (§4.04) — there is no general numeric limit in the main ship channel. The Port Code contains its own relief geometry: the South Bay 5 mph rule **exempts vessels transiting the marked Chula Vista Harbor Channel seaward of daymarks 11 and 12** (§4.30(c)3), where only the §4.04 prudent-speed standard applies. Rulemaker for any numeric relief: the **Board of Port Commissioners** (ordinance), enforced by San Diego Harbor Police. Federal security zones (33 CFR 165.1101/.1102, 165.2030, 334.870/.880) are routing/authorization constraints, not speed-relief candidates. Base schedule math always respects posted limits; relief minutes labeled upside only. Precedent: Stockholm Candela P-12 (see ../SPEED-RULE-RELIEF-PRECEDENTS.md). Full detail: `SPEED-RULES-SAN-DIEGO.md`.

**Date:** 2026-08-16 · **Status:** research-complete, source-verified desk pass (web) · **Scope:** the 7-stop / 3-line employer network (SD-1 South Bay, SD-2 Point Loma, SD-3 Bridge) per `hub.json` (version 2026-08-15-san-diego-v1).

Fail-closed rules followed throughout: every claim carries a source (URL) or is marked **unverified**; nothing invented. Access date for all sources: 2026-08-16 (web capability). No Gulf counterparties named anywhere in this document. Held/not-routed corridors (National City, Barrio Logan shipyard shuttle, Coronado Ferry Landing) appear only in the flagged internal-only subsection at the end and must never appear as corridors on any microsite.

---

## 1 · Authority inventory

**The structural headline: San Diego is a single-landlord market.** Unlike Boston's 24-authority patchwork, one authority — the San Diego Unified Port District — holds the tidelands trust for the working waterfronts of all five bay cities. Every one of the 7 network stops sits on Port-managed tidelands (directly or via a Port tenant/lessee).

**State/regional:**
1. San Diego Unified Port District ("Port of San Diego") — **the dominant landlord and gatekeeper**
2. California Coastal Commission (CCC)
3. California State Lands Commission (SLC) — trust oversight
4. SANDAG (San Diego Association of Governments) — MPO / regional transportation plan
5. San Diego Metropolitan Transit System (MTS) — land transit operator
6. California Air Resources Board (CARB) — funder (zero-emission vessel grants), not a transport authority

**City/municipal (Port member cities; the network touches the first three):**
7. City of San Diego
8. City of Chula Vista
9. City of Coronado
10. City of National City (member city; no network stop — held-corridor context only)
11. City of Imperial Beach (member city; no network stop)

**Federal:**
12. U.S. Coast Guard Sector San Diego / Captain of the Port (COTP)
13. U.S. Navy — Navy Region Southwest and bayfront installations (security-zone context only; naval installations are never referenced in rendered copy per `hub.json` gates)
14. U.S. Fish & Wildlife Service (USFWS) — San Diego Bay National Wildlife Refuge
15. U.S. Army Corps of Engineers (USACE) — dock/float construction permits (specifics unverified this pass)

**Non-governmental operators / private landing gates (not authorities — flagged clearly):**
16. Flagship Cruises & Events — the incumbent bay ferry operator (Coronado ferry; new Chula Vista route)
17. Fifth Avenue Landing (Convention Center dock lessee) and private marina operators (Safe Harbor, Harbor Island West, Glorietta Bay Marina) — berth gates within Port tidelands

---

## 2 · Per-authority profiles

### San Diego Unified Port District (Port of San Diego) — THE gatekeeper
- **Mandate:** created by the San Diego Unified Port District Act (Chapter 67, Statutes of 1962) to manage in trust the tide and submerged lands of San Diego Bay; lands previously granted to San Diego, Chula Vista, Coronado, and National City were transferred to the District (plus Imperial Beach's ocean frontage). Trust purposes: commerce, navigation, fisheries, recreation — for the statewide public. Sources: https://www.slc.ca.gov/granted-public-trust-lands/grantees/san-diego-unified-port-district/ · https://www.portofsandiego.org/about-port-san-diego
- **Controls:** San Diego Bay and **34 miles of waterfront** across the five member cities; self-funded; $13.8B stated regional impact. Governed by a seven-member Board of Port Commissioners appointed by the five cities. It is simultaneously: (a) **landlord** for every network stop (all seven landings are Port tidelands or Port-tenant marinas/piers), (b) **regulator of vessel operations** on the bay via the Port Code (Article 4: speed, anchoring, berthing, charter-vessel rules §4.37) enforced by its own **Harbor Police**, and (c) **planner** via the Port Master Plan. Sources: https://www.portofsandiego.org/about-port-san-diego · https://www.portofsandiego.org/maritime/mariner-resources/tariffs-regulations-vessels · https://www.portofsandiego.org/coming-and-going/boating-san-diego-bay/charter-vessel-regulations · https://en.wikipedia.org/wiki/Port_of_San_Diego
- **Permit path evidence:** commercial charter operations require Port-issued vessel decals via tenant marinas/landings, USCG-licensed captains, insurance minimums, and are **prohibited from using Port public facilities (boat launches, public docks)** — i.e., commercial water transportation runs through Port tenant agreements and Port permission, full stop. Tidelands Use and Occupancy Permits (TUOP) are the Port's instrument for tidelands activities. Sources: https://www.portofsandiego.org/coming-and-going/boating-san-diego-bay/charter-vessel-regulations · https://ceqanet.lci.ca.gov/2023010348
- **Published plans:** Port Master Plan Update (PMPU) — Board unanimously certified the Final PEIR and approved the PMPU on February 28, 2024; **California Coastal Commission certification listed as pending** on the Port's PMPU page as retrieved this pass (verify current status before citing in-page). Maritime Clean Air Strategy (2021) — electrification / zero-emission agenda for bay operations. Chula Vista Bayfront Master Plan — a future ferry terminal "was included … from the very beginning" (Port Board Chair Ann Moore at the June 1, 2026 Chula Vista ferry launch). Sources: https://www.portofsandiego.org/waterfront-development/port-master-plan-update · https://www.portofsandiego.org/mcas · https://www.kpbs.org/news/living/2026/06/01/new-chula-vista-to-san-diego-ferry-service-officially-launches
- **Posture: ENABLE — and the single Enable gatekeeper for the whole market.** Evidence: the Port grants leases/permits and regulates vessels but does not operate ferries; the bay's scheduled water services are run by a private operator (Flagship). A future Operate posture would most plausibly appear as Port- or city-funded service contracts (see Coronado precedent below), not Port-crewed vessels.

### California Coastal Commission
- **Mandate/controls:** certifies the Port Master Plan and amendments (e.g., unanimously certified the National City Balanced Plan PMPA); coastal development within the coastal zone outside Port jurisdiction. Any new landing structure or master-plan-level change at network stops routes through PMPU/PMPA machinery. Sources: https://www.portofsandiego.org/press-releases/general-press-releases/california-coastal-commission-unanimously-approves-national · https://www.portofsandiego.org/waterfront-development/port-master-plan-update
- **Posture: ENABLE only** (permitting/plan certification; no operations or funding).

### California State Lands Commission
- **Mandate/controls:** statutory oversight of granted public trust lands; the SDUPD is a listed grantee. No day-to-day landing control, but the trust framing ("commerce, navigation, fisheries, recreation") is the legal spine any water-transit pitch should align to. Source: https://www.slc.ca.gov/granted-public-trust-lands/grantees/san-diego-unified-port-district/
- **Posture: ENABLE** (oversight only).

### SANDAG
- **Mandate:** the region's MPO; adopted the 2025 Regional Plan (~$125B through the planning horizon) focused on transit expansion, equity, and climate. Sources: https://www.sandag.org/regional-plan/2025-regional-plan · https://www.kpbs.org/news/quality-of-life/2026/02/09/breaking-down-sandags-125-billion-spending-plan
- **Water-transit content: none found this pass** — no ferry/water-transit program was identified in the 2025 Regional Plan materials reviewed (**unverified at document level**; a targeted read of the full plan chapters is recommended before claiming SANDAG alignment in-page).
- **Posture: ENABLE (planning/funding), water-transit posture unverified.**

### MTS (San Diego Metropolitan Transit System)
- **Mandate/controls:** operates bus, Rapid, and Trolley (the UC San Diego Blue Line runs Chula Vista↔downtown, ~45 min, $2.50 one-way / $72 month pass via PRONTO). **No water-transit role identified.** Relevance is modal integration (Broadway Pier is steps from downtown trolley/bus) and the public-fare floor context. Sources: https://www.sdmts.com/fares/pronto · https://www.uber.com/global/en/r/routes/chula-vista-ca-to-san-diego-ca/ (trolley time/fare context)
- **Posture: not applicable to water (land-transit operator); water posture unverified.**

### CARB (funder)
- **Controls:** no transport authority role, but the live zero-emission-vessel money: awarded Flagship **$15.27M** (Advanced Technology Demonstration and Pilot Projects, California Climate Investments / Cap-and-Trade) toward two fully electric 275-passenger ferries for the San Diego–Coronado run; total project >$21M; first vessel expected fall 2026. Direct precedent that state money electrifies this bay's passenger fleet. Source: https://fox5sandiego.com/sustainable-san-diego/san-diego-coronado-ferries-to-go-electric-thanks-to-15-2m-state-grant/ · https://www.flagshipsd.com/eferry
- **Posture: ENABLE (grant funding).**

### City of San Diego
- **Controls:** general city jurisdiction landside of the Embarcadero; the bayfront itself (Broadway Pier, Fifth Avenue Landing area) is Port tidelands. The City's lifeguard boating rules govern the **oceanfront** (5 mph within 1,000 ft of the ocean coastline), not the bay corridors. Source: https://www.sandiego.gov/lifeguards/safety/boatreg
- **Published plans:** Climate Action Plan — mode-share targets for all residents' trips: by 2030, 19% walking / 7% cycling / 10% transit; by 2035, 25% walking / 10% cycling / 15% transit. A zero-emission water commute that removes car trips on the I-5 South / bridge corridors is directly additive to these targets. Sources: https://www.sandiego.gov/planning/work/working-on/cap · https://climatedashboard.sandiego.gov/indicators/3226
- **Posture: ENABLE** (plans and street-side integration; the Port controls the water and landings).

### City of Chula Vista
- **Controls/plans:** partner with the Port on the Chula Vista Bayfront Master Plan (Gaylord Pacific Resort & Convention Center opened May 2025; Sweetwater Park opened April 2025 — the Port's largest park at 39 acres; Harbor Park doubling to ~25 acres, South Phase construction authorized February 2026). Mayor John McCann on the June 2026 ferry launch: "Economically, this is a game changer … It will also make it easier for residents to access jobs." Sources: https://www.portofsandiego.org/projects/chula-vista-bayfront · https://www.kpbs.org/news/living/2026/06/01/new-chula-vista-to-san-diego-ferry-service-officially-launches
- **Posture: ENABLE, actively pro-water-transit** — the loudest political champion of the exact SD-1 corridor.

### City of Coronado
- **Controls/plans:** the market's clearest **public-money-for-water-commute precedent**: since 1993 the City has supported fare-free weekday commuter ferry runs (Flagship operates six morning departures each way, Broadway Pier↔Coronado Ferry Landing, free between roughly 4:50–8:30 AM, with an honored return ticket). Sources: https://www.flagshipsd.com/commuter-ferry · https://coronadoferrylanding.com/ferry-info/
- **Posture: ENABLE-plus-FUND** — Coronado doesn't operate vessels; it buys down fares on a private operator. This "city-funded seats on a private operator" structure is the closest local analog to an employer seat-block and the natural template for any public partnership on SD-3 (which is deliberately anchored at Glorietta Bay, not the incumbent's landing — see `hub.json` decision_ledger).

### City of National City / City of Imperial Beach
- Member cities of the Port with no network stop. National City context (Pier 32, Balanced Plan PMPA certified by CCC) belongs to a **held, not-routed corridor** — internal section only. Sources: https://www.portofsandiego.org/about-port-san-diego · https://www.portofsandiego.org/press-releases/general-press-releases/california-coastal-commission-unanimously-approves-national

### USCG Sector San Diego / Captain of the Port
- **Controls:** security zones at naval installations (33 CFR 165.1101 — entry prohibited unless authorized by COTP or Navy commanders, COTP tel. 619-683-6495 / VHF 16; 33 CFR 165.1102 — Point Loma), the Naval Vessel Protection Zone rule (33 CFR 165.2030 — minimum speed within 500 yd, no approach within 100 yd of large naval vessels), and the San Diego Bay/Mission Bay RNA (33 CFR 165.1122 — applies to vessels ≥100 GT; an N45 is under the threshold). Sources: https://www.law.cornell.edu/cfr/text/33/165.1101 · https://www.law.cornell.edu/cfr/text/33/165.1102 · https://www.law.cornell.edu/cfr/text/33/165.2030 · https://www.law.cornell.edu/cfr/text/33/165.1122
- **Posture: ENABLE (authorization/enforcement).** A scheduled service on SD-1 (which passes the 32nd St naval shore) should brief COTP early; hub routing already stands clear of all zones.

### U.S. Navy (Navy Region Southwest)
- **Controls:** the installations behind the 165.11xx security zones and the Part 334 restricted areas (334.870 Bravo Pier / degaussing-station most-direct-transit rule; 334.880 Point Loma naval anchorage — transit permitted, mooring >24h prohibited). Not a landing counterparty for this network; a routing-compliance stakeholder only. **Per `hub.json` gates (navy_honesty, banned terms), naval installations are never named in rendered copy.** Sources: https://www.law.cornell.edu/cfr/text/33/334.870 · https://www.law.cornell.edu/cfr/text/33/334.880
- **Posture: not applicable (security stakeholder).**

### USFWS — San Diego Bay National Wildlife Refuge
- **Controls:** the refuge (~2,620 acres; Sweetwater Marsh Unit + the 2,300-acre South San Diego Bay Unit, dedicated 1999) protects eelgrass beds, the largest contiguous mudflat in southern California, migrating **Pacific green sea turtles**, and nesting California least terns / western snowy plovers — the ecological purpose behind the South Bay's posted 5 mph area. Any SD-1 schedule case that touches South Bay speed rules should treat USFWS as a consultation stakeholder, not an adversary. Source: https://www.fws.gov/refuge/san-diego-bay/about-us
- **Posture: ENABLE (consultation), with a genuine wildlife-purpose limit on speed-relief asks** (see SPEED-RULES §4).

### USACE
- Dredge/fill and new-structure permitting where a new float/gangway is proposed; specifics **unverified this pass** — flag for legal review before any new-structure commitment (existing landings used as-is likely avoid this).

### Flagship Cruises & Events — incumbent operator (NOT an authority)
- Operates the Coronado ferry (Broadway Pier↔Coronado $9 one-way / 15 min / hourly; Convention Center↔Coronado every 30 min), the City-of-Coronado-supported fare-free commuter runs (since 1993), and — since **June 1, 2026** — the Chula Vista ferry (vessel *Balboa*, 30 ft, 32 passengers, diesel, 10 kn, ~45 min crossing, $15 one-way, Chula Vista Marina↔Fifth Avenue Landing, roughly hourly alternating). Building California's first fully electric 275-pax ferries (CARB-funded, first expected fall 2026). Sources: https://www.flagshipsd.com/cruises/flagship-ferry · https://www.flagshipsd.com/commuter-ferry · https://www.kpbs.org/news/living/2026/06/01/new-chula-vista-to-san-diego-ferry-service-officially-launches · https://www.nbcsandiego.com/news/local/new-ferry-route-connects-south-bay-to-san-diego-for-first-time/4030959/ · https://www.flagshipsd.com/eferry
- **Treatment:** incumbent-respect gate governs all copy (complement, never displace; no Broadway↔Coronado pair ever). Flagship is simultaneously the strongest **demand proof** (both flagship corridors' precedent services exist), a potential **operating partner**, and the party any Coronado/SD-3 conversation must include. Whether the Chula Vista route is subsidized (Port/city) or purely commercial is **unverified** — flagged in §6.

### Private berth gates (NOT authorities)
- Fifth Avenue Landing (Convention Center dock + 12-slip marina; lessee/operator terms **unverified this pass**), Safe Harbor South Bay / Bayfront (Chula Vista), Harbor Island West Marina / Safe Harbor Sunroad, Shelter Island Guest Docks and America's Cup Harbor sportfishing landings, Glorietta Bay Marina. All sit on Port tidelands; commercial operations from them run through their Port leases (the charter-decal structure shows the mechanism). Source: https://www.portofsandiego.org/coming-and-going/boating-san-diego-bay/charter-vessel-regulations · landing details per `hub.json` stop inventory.

---

## 3 · Per-stop landing control table (7 stops)

| # | Stop (network key) | Landing owner/operator | Permit path | Authority relationship that unlocks it | Coverage |
|---|---|---|---|---|---|
| 1 | Chula Vista (`chula-vista`) | Port tidelands; Safe Harbor South Bay marina (private tenant) — the active Chula Vista ferry landing since June 2026 | Port tenant/berth agreement (+ charter/commercial decal mechanism); TUOP if new use; CCC only if master-plan-level change | Port of San Diego + Safe Harbor (tenant) + City of Chula Vista (champion) | Verified (active ferry landing; KPBS/NBC + hub inventory) |
| 2 | Convention Center (`fifth-avenue-landing`) | Port tidelands; Fifth Avenue Landing dock (private lessee) — active ferry stop (Coronado + Chula Vista routes land here) | Private lessee agreement + Port lease compliance | Port of San Diego + Fifth Avenue Landing lessee | Verified as active ferry stop; lessee/lease terms unverified |
| 3 | Broadway Pier (`broadway-pier`) | Port of San Diego (Port Pavilion / public pier; incumbent ferry + cruise operations) | Direct Port agreement (note: charters are barred from Port *public* facilities — a scheduled-service berth agreement is a Port real-estate conversation, not a charter decal) | Port of San Diego (sole counterparty) | Verified (Port facility) |
| 4 | Shelter Island (`shelter-island`) | Port tidelands; Shelter Island Guest Docks (26 public slips) | Port agreement; note public-dock commercial-use prohibition — needs an explicit Port carve-out or alternate tenant berth | Port of San Diego | Verified location; commercial-use path needs Port ruling (flagged) |
| 5 | Point Loma (`americas-cup-harbor`) | Port tidelands; private sportfishing landings (Fisherman's Landing, H&M, Point Loma Sportfishing) | Private landing agreement + Port lease compliance (the sportfishing landings are the bay's existing high-throughput passenger gates) | Port of San Diego + landing operators | Verified (hub inventory); operator terms unverified |
| 6 | Harbor Island (`harbor-island`) | Port tidelands; Harbor Island West Marina (620 slips) / alternate Safe Harbor Sunroad | Private marina agreement + Port lease compliance | Port of San Diego + marina operators | Verified (hub inventory); operator terms unverified |
| 7 | Glorietta Bay (`glorietta-bay`) | Glorietta Bay Marina & Public Dock, Strand Way; **ownership split (Port vs City of Coronado) unverified this pass** | Marina agreement + Port and/or City of Coronado; 5 mph zone inside the bay (§4.35(c)3) | Port of San Diego + City of Coronado | Location verified (hub inventory); controlling owner unverified |

**Coverage tally: every stop is inside the Port's tidelands trust — one landlord.** 3 of 7 stops (Fifth Avenue Landing lessee terms, Glorietta Bay ownership split, Shelter Island public-dock commercial path) have open document-level questions — flagged, not guessed.

---

## 4 · Funding hooks

| Program | Level | What it funds | Source |
|---|---|---|---|
| FTA ferry programs, FY2026: $657M total announced April 6, 2026; includes Passenger Ferry Grant Program and **$98M Electric or Low-Emitting Ferry Pilot Program** (federal share up to 80–85% for electric-ferry capital) | Federal | Purchase of electric/low-emitting ferry vessels, charging infrastructure, terminals | https://www.transit.dot.gov/funding/grants/grant-programs/electric-or-low-emitting-ferry-pilot-program-iija-ss-71102 |
| CARB Advanced Technology Demonstration and Pilot Projects (California Climate Investments / Cap-and-Trade) | State | **$15.27M already awarded on this bay** to Flagship for two 275-pax electric ferries (total project >$21M) — proof the state funds zero-emission vessels in San Diego specifically | https://fox5sandiego.com/sustainable-san-diego/san-diego-coronado-ferries-to-go-electric-thanks-to-15-2m-state-grant/ |
| City of Coronado fare-free commuter ferry support (since 1993) | Municipal | Ongoing fare buy-down on a private operator's commuter runs — the local template for publicly funded seats | https://www.flagshipsd.com/commuter-ferry |
| Port of San Diego Maritime Clean Air Strategy (2021) | Port | Not a grant program per se; the Port's own electrification agenda that a zero-emission foiling fleet advances (project/initiative pipeline) | https://www.portofsandiego.org/mcas |
| SANDAG 2025 Regional Plan (~$125B) | Regional | Transit expansion funding framework; **no water-transit line item verified this pass** — engage, don't cite | https://www.sandag.org/regional-plan/2025-regional-plan · https://www.kpbs.org/news/quality-of-life/2026/02/09/breaking-down-sandags-125-billion-spending-plan |

---

## 5 · Quality-of-life hooks (each tied to a named, sourced plan)

- **City of San Diego Climate Action Plan** — 2035 targets: 25% walking, 10% cycling, 15% transit mode share of residents' trips. Zero-emission water commutes on corridors paralleling I-5 South and the bridge are directly additive. Sources: https://www.sandiego.gov/planning/work/working-on/cap · https://climatedashboard.sandiego.gov/indicators/3226
- **Port Maritime Clean Air Strategy (2021)** — the Port's own decarbonization/electrification agenda for bay operations; an all-electric foiling network is on-thesis. Source: https://www.portofsandiego.org/mcas
- **Chula Vista Bayfront Master Plan build-out** — Gaylord Pacific (May 2025), Sweetwater Park (April 2025), Harbor Park expansion (2026–27), and a ferry terminal envisioned "from the very beginning" (Port Chair Moore, June 2026). The bayfront's own plan assumes water transportation. Sources: https://www.portofsandiego.org/projects/chula-vista-bayfront · https://www.kpbs.org/news/living/2026/06/01/new-chula-vista-to-san-diego-ferry-service-officially-launches
- **Coronado's 30+-year fare-free commuter ferry program** — a member city has paid for water commuting on this bay since 1993; water commuting is an established public good here, not a novelty. Source: https://www.flagshipsd.com/commuter-ferry
- **Live demand proof (June 2026)** — a public ferry now operates the exact SD-1 pair (Chula Vista↔Fifth Avenue Landing, $15, ~45 min at 10 kn). The employer network adds guaranteed seats, speed, and new station pairs as a complement — never a displacement. Sources: https://www.kpbs.org/news/living/2026/06/01/new-chula-vista-to-san-diego-ferry-service-officially-launches · https://www.nbcsandiego.com/news/local/new-ferry-route-connects-south-bay-to-san-diego-for-first-time/4030959/

---

## 6 · Enable vs Operate — market classification

**San Diego is primarily ENABLE, with a single dominant gatekeeper.** Reasoning:
1. The Port holds every landing, regulates every vessel movement, and runs its own police force — but operates no ferries. There is **no WETA/MBTA-analog public water-transit operator** in this market.
2. Where public money touches water transit, it flows **to a private operator**: Coronado's fare-free commuter runs (municipal), CARB's $15.27M e-ferry grant (state). The local "Operate" energy is really **Fund/Contract**.
3. Therefore the Public Partners page should lead Enable (Port: landings, permits, pilot blessing; cities: plan alignment and fare programs) and present Operate as procurement *or* Coronado-style service contracting — with the honest note that the natural operating partner conversation on this bay includes the incumbent operator.
4. **One relationship unlocks the whole map.** In Boston, seven landlords; here, one Board of Port Commissioners vote covers speed relief, berth agreements, and master-plan alignment simultaneously. That concentration is the market's biggest opportunity and its biggest single-point risk.

---

## 7 · Open flags for Jaideep

1. **Chula Vista ferry funding structure unverified** — launch coverage (KPBS/NBC, June 1, 2026) names Flagship as owner-operator with Port and City celebration presence, but no source states whether the route is subsidized, Port-supported, or purely commercial. Matters for incumbent-respect framing and for any future SD-1 partnership ask. Recommend a direct Port/Flagship conversation before any public claim.
2. **PMPU Coastal Commission status** — the Port's PMPU page (as retrieved) lists CCC certification *pending* while the National City Balanced Plan PMPA is separately CCC-certified. Verify current PMPU status before referencing it in-page.
3. **Fifth Avenue Landing lessee terms unverified** — it's the proven Convention Center gate (both incumbent routes land there) but the lease/operator structure needs a document-level pass before berth-terms assumptions.
4. **Glorietta Bay Marina ownership split (Port vs City of Coronado) unverified** — gates the SD-3 feeder conversation.
5. **Shelter Island Guest Docks are a Port *public* facility** — Port rules bar charters from public docks; a scheduled employer service would need an explicit Port berth agreement or an alternate tenant berth in the basin. Do not assume the guest docks are usable.
6. **SANDAG/MTS water posture is a blank** — no published water-transit program found; treat as engagement targets (the MPO's plan cycle is where a future corridor could be written in), not as citable alignment.
7. **COTP/Navy briefing** — SD-1 passes near the 32nd St security zone and naval anchorages (routing already stands clear per hub). A pre-launch COTP briefing is cheap insurance; never rendered in copy (navy_honesty gate).
8. **USACE specifics not researched** — only relevant if any stop needs a new float/gangway.

---

## 8 · HELD / internal only — never renders

Per `hub.json` decision_ledger; listed here for authority-map completeness only. **None of the following may appear on any microsite, map, or public copy.**

- **Coronado Ferry Landing (1201 First St):** real active incumbent stop — NOT authored as a station. Incumbent's commute runs are City-subsidized and free at commute hours; landing lease in flux (40-yr lease expired June 30, 2026; one-year renewal voted June 23, 2026 per ledger). Any conversation is an operating-partner conversation with Flagship / the Port / the City. Broadway↔Coronado head-to-head is **excluded permanently**.
- **National City Line (Pier 32↔Fifth Avenue Landing/Broadway):** corridor held, not routed — weak walk-tier employment; Balanced Plan context above is background only.
- **Shipyard Shuttle (Barrio Logan):** dead until a permitted civilian float exists near Cesar Chavez Park; watchlist on the Port park-improvement process.
- Authority-map implication of the ledger: all three held items still run through the same single landlord — the Port — which strengthens the one-relationship thesis in §6.
