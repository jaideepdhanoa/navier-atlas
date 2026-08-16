# New York Harbor Authority Map — Public Partners Research

> **Speed-rule note (doctrine: ARCHETYPE-STRATEGY.md §4b):** unlike Boston, New York's corridors face no located standing numeric open-water speed cap; the binding rules are near-dock bands (NY 5 mph/100 ft; NJ no-wake/200 ft) and CT per-harbor zones. Relief upside is small and CT-channel-specific. See `SPEED-RULES-NEW-YORK.md`. Base map times keep posted/assumed harbor limits.

**Date:** 2026-08-16 · **Status:** research-complete, source-verified desk pass (web) · **Scope:** the 38-station / 9-line employer network in `hub.json` (NY-M East River trunk, NY-H Hudson spine, NY-B Brooklyn, NY-Q East River Feeder, NY-C Connecticut Express, NY-G Long Island Sound, NY-X Bronx, NY-SI Staten Island, NY-S East End Seasonal).

Fail-closed rules followed: every claim carries a URL or is marked **unverified**; nothing invented. Access date for all sources: 2026-08-16. No Gulf counterparties named. Hub gates honored: `forbid_dock_unlock`, `forbid_employer_names`, banned term list, and `ny_c_honesty` ("no raw-speed claims vs Metro-North").

---

## 1 · Authority inventory

**City of New York (multi-stop jurisdiction):**
1. NYC Economic Development Corporation (NYCEDC) — owns NYC Ferry; Brooklyn Marine Terminal/Atlantic Basin operator; Blue Highways program
2. NYC Department of Transportation (NYC DOT) — operates the Staten Island Ferry; owns public ferry landings (Pier 11, E 34th St, Pier 79)
3. NYC Department of City Planning (DCP) — Comprehensive Waterfront Plan
4. Hudson River Park Trust (HRPT) — state/city partnership controlling Hudson piers, Battery–W 59th
5. Brooklyn Bridge Park Corporation — Pier 6 / Fulton Ferry landings
6. Brooklyn Navy Yard Development Corporation (BNYDC) — Dock 72
7. Roosevelt Island Operating Corporation (RIOC, NYS public benefit corp) — Roosevelt Island landing

**Bi-state / regional:**
8. Port Authority of New York & New Jersey (PANYNJ) — port district; Atlantic Basin underlying owner (transfer to City announced 2024); historic ferry-terminal broker
9. MTA / Metro-North (modal integration only — no landing control; NY-C/NY-G corridors touch its catchments)

**New Jersey:**
10. NJ Transit — owns Hoboken Terminal incl. ferry slips ($125M restoration with PANYNJ)
11. Borough of Edgewater — owns Edgewater Marina & Ferry Landing
12. Weehawken / West New York municipalities — general waterfront jurisdiction (posture **unverified**); Port Imperial & Lincoln Harbor landings are private (NY Waterway/Port Imperial Ferry Corp)

**Westchester / Long Island:**
13. City of Yonkers — Recreation Pier (currently under construction)
14. City of New Rochelle — Municipal Marina, Echo Bay
15. City of Glen Cove — Ferry Terminal & Boat Basin, Garvies Point (federally funded)
16. Town of North Hempstead — Port Washington Town Dock

**Connecticut:**
17. CT DOT (statewide transit; posture toward water transit **unverified this pass**)
18. Town of Greenwich — Arch Street dock (town-owned; seasonal island ferries today)
19. City of Stamford + state-appointed harbormaster — Harbor Point marina itself is private (Harbor Point/BLT)
20. City of Norwalk + harbormaster — 90 Water St dock used by Norwalk Seaport Association (nonprofit operator, **not an authority**)
21. City of Milford — Lisman Landing Marina (city-owned)
22. City of Bridgeport / Bridgeport Port Authority (est. 1993) — Steelpointe Harbor; marina is private (Bridgeport Harbor Marina/RCI)

**East End (seasonal NY-S line):**
23. Village of Sag Harbor (Long Wharf), Village of Greenport (Mitchell Park Marina), Town of Shelter Island (ferry landings context), Montauk/East Hampton Town — landing control **unverified this pass** (line is seasonal, Phase 1–2 mixed)

**Federal:**
24. USCG Sector New York (VTS NY, COTP zones) · USACE (federal channels incl. Buttermilk) — permitting/navigation context, not landing grantors

**Private operators (precedent evidence, never authorities):** NYC Ferry operator Hornblower Group; NY Waterway (Port Imperial Ferry Corp); SeaStreak.

---

## 2 · Per-authority profiles (key relationships)

### NYCEDC
- **Mandate/controls:** owns the NYC Ferry system (38 vessels, 25 landings per its naming-rights materials) and manages the operator contract; day-to-day ops by Hornblower Group under a five-year contract. Also operates Brooklyn Marine Terminal (Piers 7–12) and Atlantic Basin (Red Hook stop). Sources: https://edc.nyc/project/nycferry · https://en.wikipedia.org/wiki/NYC_Ferry · https://edc.nyc/project/brooklyn-marine-terminal
- **Published plans:** record ridership announced summer 2025 (system carries 7M+/yr); first-ever system naming-rights sale in process (agency selected; no value yet). **Blue Highways** waterborne-freight action plan + live Dec 2025 microfreight pilot (Atlantic Basin → Pier 79). Sources: https://edc.nyc/press-release/mayor-nycedc-announce-record-breaking-nyc-ferry-ridership-numbers-summer-2025 · https://edc.nyc/press-release/nycedc-advances-search-first-ever-naming-rights-partner-nyc-ferry-system · https://www.nyc.gov/html/dot/html/pr2025/nyc-blue-highways-freight-pilot.shtml
- **Posture: OPERATE (via contracted private operator) — the largest public-ferry OPERATE precedent in the US.** The NYCEDC model (public system, private operator) is structurally the exact frame Navier's Operate track proposes.

### NYC DOT
- **Mandate/controls:** operates the **Staten Island Ferry** directly (free, 24/7, ~25-min crossing — the St. George stop's anchor precedent: https://www.nyc.gov/html/dot/html/ferrybus/siferryschedule.shtml). Owns the public ferry landings at **Pier 11/Wall St and E 34th St** (https://en.wikipedia.org/wiki/East_34th_Street_Ferry_Landing) and the **West Midtown/Pier 79 terminal**, city-owned, leased to NY Waterway and explicitly "open to any ferry company" as a public terminal (https://en.wikipedia.org/wiki/West_Midtown_Ferry_Terminal). General ferry landing/operator info: https://www.nyc.gov/html/dot/html/ferrybus/ferintro.shtml
- **Posture: DUAL — OPERATE (SI Ferry) + ENABLE (public landings open to private operators).** NYC DOT landing access at Pier 11/E 34th/Pier 79 is the single highest-leverage Enable relationship in the market: those three stops carry all nine lines' Manhattan ends.

### NYC DCP — Comprehensive Waterfront Plan (2021)
- 10-year citywide waterfront vision ("equitable, resilient and healthy waterfront"); the plan and its waterborne-transportation strategies are the plan-alignment hook for the Public Partners page. Sources: https://www.waterfrontplan.nyc/ · https://www.nyc.gov/content/planning/pages/about-us/newsroom/pr-20211219
- **Posture: ENABLE (planning overlay only).**

### Hudson River Park Trust
- State-city partnership (Hudson River Park Act, 1998) operating the park Battery–W 59th on the Manhattan Hudson bank; its rules prohibit docking/landing on park piers except as designated. BPC Terminal and Pier 79 sit at/adjacent to its boundary seams — exact jurisdiction at each proposed touch **must be confirmed parcel-by-parcel**. Sources: https://hudsonriverpark.org/about-us/hudson-river-park-trust/ · https://hudsonriverpark.org/park-rules-regulations/
- **Posture: ENABLE (permitting/landing grantor), narrow.**

### PANYNJ
- Bi-state port district authority (air/sea/rail/PATH; https://www.panynj.gov/port-authority/en/about.html). Owns Atlantic Basin (Red Hook), historically leased to NYCEDC; City takeover announced May 2024 (transition status **unverified**). Sources: https://dos.ny.gov/system/files/documents/2021/05/f-2021-0309_homeport_ii.pdf · https://redhookwaterstories.org/tours/show/7. Brokered the post-9/11 ferry expansion and the Hoboken slip restoration with NJ Transit. Source: https://www.njtransit.com/press-releases/port-authority-nj-transit-sign-agreement-restore-historic-hoboken-terminal-ferry
- **Posture: ENABLE.**

### NJ Transit
- Owns Hoboken Terminal; with PANYNJ funded the ~$125M restoration of the historic ferry slips, explicitly "to allow for expansion of ferry service." Sources: https://www.njtransit.com/press-releases/port-authority-nj-transit-sign-agreement-restore-historic-hoboken-terminal-ferry · https://www.njtransit.com/press-releases/nj-transit-advances-hoboken-ferry-terminal-restoration
- **Posture: ENABLE (rail-integrated landing grantor).** Hoboken is the network's premier modal-integration story on the NJ side.

### Municipal / suburban landing owners (Enable ring)
- **Edgewater:** Borough owns Edgewater Marina & Ferry Landing (https://www.edgewaternj.org/221/Edgewater-Marina-Ferry-Landing).
- **Yonkers:** City owns Recreation Pier — **currently under construction** (https://www.yonkersny.gov/511/The-Pier); prior Yonkers↔Manhattan ferry precedent (PANYNJ-contracted NY Water Taxi, 2006: https://www.panynj.gov/port-authority/en/press-room/press-release-archives/2006_press_releases/port_authority_hiresnewyorkwatertaxitoprovideferryservicebetween.html).
- **New Rochelle:** City Municipal Marina, Echo Bay — 350 slips (https://www.newrochelleny.gov/336/Municipal-Marina).
- **Glen Cove:** City Ferry Terminal & Boat Basin at Garvies Point, federally funded, built 2015, long unserved — a ready asset seeking service (https://glencoveny.gov/glen-cove-ferry · https://abc7ny.com/post/glen-cove-ferry-commuters-nyc/11020683/).
- **North Hempstead:** Town Dock, Port Washington (**town control assumed from name; not document-verified this pass**).
- **Greenwich:** Town-owned Arch Street dock; town runs seasonal island ferries — an existing municipal water-transport operation (https://www.greenwichct.gov/641/Ferry-Service).
- **Milford:** Lisman Landing Marina, city-owned, 35 slips (https://www.milfordct.us/317/Milford-Lisman-Landing-Marina).
- **Bridgeport:** Port Authority created 1993 to develop the harbor (https://www.cga.ct.gov/2005/rpt/2005-R-0875.htm); state legislative action reported to free harbor space for a new ferry terminal (secondary/social source — **unverified**); Steelpointe marina is private (https://bridgeportharbormarina.com/).
- **Stamford:** Harbor Point marina is private (Harbor Point Marinas/BLT, https://harborpointmarinas.com/) — private-landing stop with municipal/harbormaster oversight.
- **Norwalk:** 90 Water St "Hope Dock" used by Norwalk Seaport Association (nonprofit, https://www.seaport.org/) — **not an authority**; underlying ownership **unverified**.

### Campus/park landing corporations (NYC)
- **Brooklyn Bridge Park Corp:** Pier 6 ferry dock inside the park (https://brooklynbridgepark.org/places-to-see/pier-6/). **ENABLE.**
- **BNYDC:** Dock 72 ferry landing inside the Navy Yard campus (https://www.brooklynnavyyard.org/directions-map/ · https://www.dock72.com/). **ENABLE** (controlled-access campus).
- **RIOC:** Roosevelt Island ferry landing, 40 River Rd (https://www.rioc.ny.gov/community/transportation/ferry). **ENABLE.**

### Existing operators (precedent, factual only)
- **NYC Ferry / Hornblower:** public system, private operator, $4.50 flat fare, free 120-min transfers (https://www.ferry.nyc/ticketing-info/).
- **NY Waterway (Port Imperial Ferry Corp):** private operator owning/serving the NJ Gold Coast terminals incl. Port Imperial and Lincoln Harbor; city-owned Pier 79 lessee (https://www.nywaterway.com/ · https://en.wikipedia.org/wiki/West_Midtown_Ferry_Terminal).
- **SeaStreak:** private premium operator, NJ↔Manhattan (Pier 11/E 35th; https://seastreak.com/) — proof that a **premium-priced** private tier coexists with the subsidized public system.

---

## 3 · Per-stop landing control table (38 stops)

Coverage key: V = source-verified · P = partially verified · U = unverified this pass.

| # | Stop | Landing owner/controller | Key relationship | Cov. |
|---|---|---|---|---|
| 1 | Pier 11/Wall St | NYC DOT (public landing) | NYC DOT landing access | V |
| 2 | E 34th St | NYC DOT | NYC DOT | V |
| 3 | E 90th St | NYC Ferry landing; underlying owner (Parks vs DOT) **unverified** | NYC DOT/NYCEDC | P |
| 4 | BPC/Brookfield Place | Terminal ownership (Brookfield vs BPCA) **unverified** | Private/authority mix | U |
| 5 | Pier 79/W 39th | City of New York (leased to NY Waterway; public terminal) | NYC DOT + incumbent lessee | V |
| 6 | Paulus Hook | NY Waterway-served terminal; ownership **unverified** | Private operator precedent | P |
| 7 | Liberty Landing Marina | Private marina (Liberty Landing) | Private agreement | P |
| 8 | Newport Marina | Private (Newport/LeFrak) — **unverified** | Private agreement | U |
| 9 | Hoboken Terminal | NJ Transit (restored slips) | NJ Transit | V |
| 10 | Hoboken 14th St | NY Waterway-served; ownership **unverified** | Private/municipal | U |
| 11 | Lincoln Harbor | NY Waterway private terminal | Private agreement | P |
| 12 | Port Imperial | NY Waterway (Port Imperial Ferry Corp) private terminal | Private agreement | P |
| 13 | Edgewater | Borough of Edgewater (Marina & Ferry Landing) | Borough | V |
| 14 | Yonkers Recreation Pier | City of Yonkers (under construction) | City | V |
| 15 | Brooklyn Navy Yard (Dock 72) | BNYDC campus | BNYDC | V |
| 16 | DUMBO/Fulton Ferry | Brooklyn Bridge Park / NYC Ferry landing (parcel owner **unverified**) | BBP Corp/NYCEDC | P |
| 17 | BBP Pier 6 | Brooklyn Bridge Park Corp | BBP Corp | V |
| 18 | Red Hook/Atlantic Basin | PANYNJ owner / NYCEDC operator (City takeover announced 2024) | NYCEDC + PANYNJ | V |
| 19 | Greenpoint Landing | NYC Ferry landing; private developer dock (**unverified**) | NYCEDC + private | U |
| 20 | Hunters Point South | NYC Ferry landing (city park); owner detail **unverified** | NYCEDC/Parks | P |
| 21 | LIC Gantry Plaza | State park landing (**unverified**) | NY State Parks (assumed) | U |
| 22 | Roosevelt Island | RIOC | RIOC | V |
| 23 | Astoria (Hallets Point) | NYC Ferry landing; owner **unverified** | NYCEDC + private | U |
| 24 | Soundview (Clason Point) | NYC Ferry landing; owner **unverified** | NYCEDC/Parks | U |
| 25 | Ferry Point Park (Throgs Neck) | NYC Ferry landing, Ferry Point Park (NYC Parks assumed) | NYC Parks/NYCEDC | P |
| 26 | St. George | NYC DOT (SI Ferry terminal complex) | NYC DOT | V |
| 27 | Greenwich (Arch St) | Town of Greenwich | Town | V |
| 28 | Stamford (Harbor Point) | Private marina (Harbor Point/BLT) | Private agreement | V |
| 29 | Norwalk (90 Water St) | Norwalk Seaport Assoc. dock use; ownership **unverified** | City/harbormaster + nonprofit | P |
| 30 | Milford (Lisman Landing) | City of Milford | City | V |
| 31 | Bridgeport (Steelpointe) | Private marina (Bridgeport Harbor Marina/RCI); Port Authority context | Private + BPA | V |
| 32 | Glen Cove (Garvies Pt) | City of Glen Cove | City | V |
| 33 | Port Washington Town Dock | Town of North Hempstead (assumed from designation) | Town | P |
| 34 | New Rochelle (Echo Bay) | City of New Rochelle Municipal Marina | City | V |
| 35 | Sag Harbor (Long Wharf) | Village of Sag Harbor (assumed) | Village | U |
| 36 | Shelter Island | Town/private ferry landings — **unverified** | Town | U |
| 37 | Greenport (Mitchell Park) | Village of Greenport (assumed) | Village | U |
| 38 | Montauk | Existing seasonal ferry docks — owner **unverified** | Town/private | U |

**Coverage tally: 17 V · 9 P · 12 U.** The unverified cluster is concentrated in NYC Ferry outer-borough landings (where NYCEDC relationship likely suffices regardless of parcel owner) and the seasonal East End — flagged, not guessed.

---

## 4 · Funding hooks

| Program | Level | Relevance | Source |
|---|---|---|---|
| FTA Passenger Ferry Grant Program (49 U.S.C. § 5307(h)) | Federal | Capital for vessels/terminals in urbanized areas ($657M available FY2026) | https://www.transit.dot.gov/passenger-ferry-grants |
| FTA Electric or Low-Emitting Ferry Pilot Program | Federal | Electric-vessel purchase funding — direct Navier fit | https://sam.gov/fal/282135e5554e4674b21182aaa0780671/view |
| NJT/PANYNJ Hoboken ferry-slip restoration (~$125M) | Bi-state | Proof of public capital already committed to ferry infrastructure at a network stop | https://www.njtransit.com/press-releases/port-authority-nj-transit-sign-agreement-restore-historic-hoboken-terminal-ferry |
| NYC Ferry naming-rights sale (in process) | City | Revenue-side precedent for sponsorship layer (no value disclosed yet — fail closed) | https://edc.nyc/press-release/nycedc-advances-search-first-ever-naming-rights-partner-nyc-ferry-system |
| NYCEDC Blue Highways | City | Waterborne freight program with a live pilot touching two network stops (Atlantic Basin, Pier 79) | https://edc.nyc/blue-highways · https://www.nyc.gov/html/dot/html/pr2025/nyc-blue-highways-freight-pilot.shtml |
| ESD Garvies Point investment (Glen Cove) | State | $18.7M waterfront connector — state capital already sunk at a network stop awaiting service | https://esd.ny.gov/esd-media-center/press-releases/esd-announces-completion-18-million-garvies-point-road-waterfront-connector-glen-cove |

## 5 · Quality-of-life hooks (named, sourced plans)

- **NYC Comprehensive Waterfront Plan (2021)** — the city's own 10-year vision for "an equitable, resilient and healthy waterfront for all New Yorkers"; quote plan language directly on the partners page. https://www.waterfrontplan.nyc/
- **Congestion Relief Zone tolling (2025– )** — $9/day passenger-vehicle toll south of 60th St; every water commute that replaces a car trip is toll-relief the city's own policy created. https://www.mta.info/fares-tolls/tolls/congestion-relief-zone/about · https://portal.311.nyc.gov/article/?kanumber=KA-03612
- **NYC Ferry record ridership (summer 2025; 7M+/yr system)** — demand for water transit is proven and growing, per the city's own releases. https://edc.nyc/press-release/mayor-nycedc-announce-record-breaking-nyc-ferry-ridership-numbers-summer-2025
- **Blue Highways** — the city is actively moving freight to the water; Navier's clean overnight-cargo upside rides the city's own program direction. https://edc.nyc/blue-highways

## 6 · City classification: **DUAL — Operate-weighted in NYC proper, Enable across the ring**

- **Operate evidence:** NYCEDC owns a 38-vessel public ferry system run by a contracted private operator; NYC DOT directly operates the Staten Island Ferry. New York is the strongest public-OPERATE water-transit market in the country — procurement conversations (vessels bought/chartered into the public system, or a premium tier layered onto it) have native precedent.
- **Enable evidence:** the same city owns public landings explicitly open to any ferry company (Pier 79 precedent); NJ Transit, Edgewater, Yonkers, New Rochelle, Glen Cove, North Hempstead, Greenwich, Milford own landings and none operate vessels — the entire suburban ring is Enable.
- **Page weighting:** NYC-proper panels lead Operate-friendly ("augment the public network"); NJ/Westchester/LI/CT panels lead Enable ("your dock is ready; private capital and committed demand do the rest"). CT panels must respect `ny_c_honesty`: comfort/direct-to-waterfront framing only, never raw-speed claims vs Metro-North.

## 7 · Open flags for Jaideep

1. **NYCEDC is both the biggest partner and the incumbent** — NYC Ferry's owner has an operator contract (Hornblower) and a naming-rights sale in flight. Navier's premium tier must be framed as complementary (different price point, different corridors — CT/LI Sound gaps NYC Ferry doesn't serve), not competitive, or the Enable relationship at 10+ NYC Ferry landings gets harder.
2. **12 stops are unverified at parcel level** (see §3) — mostly outer-borough NYC Ferry landings and the East End. Recommend targeted verification before any binding landing claim.
3. **BPC/Brookfield Place terminal ownership** (Brookfield vs Battery Park City Authority) unresolved — a Phase-1 stop; verify early.
4. **Atlantic Basin control is in transition** (PANYNJ→City announced May 2024) — confirm counterparty before Red Hook outreach.
5. **Yonkers pier is under construction** — Phase-2 stop; construction scope/completion date unverified; opportunity to shape the rebuild.
6. **Glen Cove is the ripest Enable story in the network:** a federally-funded, state-connected, city-owned ferry terminal with no service — but the failed-ferry history there cuts both ways; launch-trigger honesty (60–80 committed seats) is the answer to their subsidy-trap fear.
7. **No CT DOT research this pass** — the NY-C line spans five CT municipalities; whether CT DOT or municipalities lead water-transit policy is unresolved.
8. **Never present NY Waterway/SeaStreak/Hornblower as authorities or partners** — operators appear as market precedent only.
