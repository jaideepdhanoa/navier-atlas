# Washington DC Authority Map — Public Partners Research

> **Speed-rule relief map (doctrine: ARCHETYPE-STRATEGY.md §4b):** DC is the strongest relief jurisdiction researched so far. 19 DCMR § 1027 caps hydrofoils at 6 mph in the Washington Channel / above Memorial Bridge and 10 mph along the Old Town strip — but § 1027.2 states the rule's purpose in wash/wake terms, § 1027.3 **explicitly exempts hydrofoils operated for demonstration/experimentation under a Mayoral permit**, and § 1027.1/§ 1027.10 give the Mayor standing authority to set vessel speed limits. Pitch posture: invite the Mayor's office/DDOT/MPD Harbor Patrol to measure wake+noise and use their own regulation's mechanisms; cite Stockholm Route 89 (Candela P-12, Länsstyrelsen exemption). Base map times keep posted limits; relief minutes only as labeled upside. Full corridor-by-corridor detail: `SPEED-RULES-WASHINGTON-DC.md`.

**Date:** 2026-08-16 · **Status:** research-complete, source-verified desk pass (web) · **Scope:** the 11-stop / 3-line employer network (DC-1 Potomac, DC-2 Anacostia, DC-3 Pentagon Link) per `hub.json` (v2026-08-15-dc-mece-f3).

Fail-closed rules followed throughout: every claim carries a source (URL) or is marked **unverified**; nothing invented. Access date for all sources: 2026-08-16. No Gulf counterparties named anywhere. Security-zone content is internal-only (hub `gates.banned_terms` bans that vocabulary from rendering) — see the flagged subsection at the end.

---

## 1 · Authority inventory

**Federal (unusually central in DC — the defining feature of this market):**
1. National Park Service — George Washington Memorial Parkway (GWMP)
2. National Park Service — National Capital Parks-East (NACE) + Piscataway Park
3. US Coast Guard — Sector/Captain of the Port Maryland-National Capital Region
4. US DOT Maritime Administration (MARAD) — M-495 Marine Highway
5. US Army Corps of Engineers (permits; not deep-profiled)

**District of Columbia:**
6. DDOT (District Department of Transportation)
7. MPD Harbor Patrol / DC Harbor Master (Metropolitan Police Department)
8. Office of the Mayor (vessel speed-limit authority under 19 DCMR § 1027.1)
9. DMPED (Deputy Mayor for Planning & Economic Development) — waterfront asset builder (Diamond Teague)
10. DOEE (Dept. of Energy & Environment) — environmental permitting (**not deep-profiled this pass**)

**Regional / transit context:**
11. WMATA (Metrorail/Metrobus — context, not a water operator)
12. MWCOG (Metropolitan Washington Council of Governments — regional MPO)

**Virginia:**
13. City of Alexandria (owns the City Marina landing)
14. PRTC / OmniRide (Potomac & Rappahannock Transportation Commission)
15. Prince William County (Occoquan/Woodbridge origin market)
16. Arlington County / National Landing context (no dock at HQ2; Daingerfield is NPS)
17. Virginia DWR (statewide boating rules)
18. NVRC (Northern Virginia Regional Commission — commuter-ferry convener)

**Maryland:**
19. Prince George's County (National Harbor host jurisdiction)
20. Maryland DNR / Natural Resources Police (MD-water speed zones)

**Private / non-governmental landing controllers (flagged clearly — not authorities):**
21. Hoffman Madison Waterfront (The Wharf district manager — Transit Pier)
22. Washington Harbour ownership (investor group; managed by MRP Realty) — Georgetown dock
23. Peterson Companies (National Harbor developer/owner)
24. Living Classrooms of the National Capital Region (nonprofit; operates The Yards Marina)
25. Occoquan Harbour Marina (private, family-owned)
26. City Cruises / Hornblower (Potomac Riverboat Co.) — incumbent water-taxi operator (precedent, not an authority)

---

## 2 · Per-authority profiles

### NPS — George Washington Memorial Parkway (GWMP)
- **Mandate:** administers federal parkland in DC/MD/VA including Columbia Island Marina, Daingerfield Island (Washington Sailing Marina), Lady Bird Johnson Park, Gravelly Point, Roaches Run, Theodore Roosevelt Island — i.e., much of the Virginia-side Potomac shoreline on our corridors. Source: https://www.nps.gov/gwmp/learn/management/superintendent-s-compendium.htm
- **Controls:** two of our stops outright. Columbia Island Marina (Pentagon stop) and Washington Sailing Marina (Daingerfield/HQ2-shuttle stop) are NPS facilities run by concessioners; NPS offered a 10-year concession opportunity for both in 2019 (https://www.nps.gov/gwmp/learn/news/don-t-miss-the-boat-exciting-business-opportunity-at-columbia-island-marina-and-washington-sailing-marina.htm), and the 2020 solicitation (CC-GWMP005-20) was later cancelled per sam.gov (https://sam.gov/workspace/contract/opp/355ac96ccc0a4a8f907655b5796c8ebe/view) — **current concessioner identity unverified this pass**. The 2025 Superintendent's Compendium permits vessels to dock/moor "at the marinas in the George Washington Memorial Parkway managed under a concessions contract or similar instrument, **or as approved by the Superintendent**" — that last clause is the access pathway.
- **Posture: ENABLE.** NPS is a permitting/concession gatekeeper, not an operator. Boat docks/structures require Superintendent permits (36 CFR §1.6 list in the compendium).

### NPS — National Capital Parks-East + Piscataway Park
- **Controls:** James Creek Marina (Buzzard Point stop) — 297 wet slips, "operated by an NPS-authorized concessioner" (https://www.nps.gov/places/000/james-creek-marina.htm); NPS selected NCR Marine Services as operator in Jan 2020 after Guest Services Inc. ran it from 1986 (https://www.nps.gov/nace/learn/news/national-park-service-selects-operator-for-james-creek-marina.htm). Fort Washington Marina (Piscataway Creek stop) is an NPS facility in Piscataway Park; NPS announced it would resume operational responsibility and issue temporary concession contracts (https://www.nps.gov/pisc/learn/news/national-park-service-to-resume-operational-responsibility-at-fort-washington-marina.htm · https://www.nps.gov/pisc/planyourvisit/fort-washington-marina.htm).
- **Posture: ENABLE.** Same concession/permit structure as GWMP.
- **Net NPS position across the network: 4 of 11 stops (columbia-island, daingerfield, james-creek, fort-washington) sit on NPS land under concession management — NPS is the single most important Enable gatekeeper in this market.** Precedent in our favor: these are already commercial marina concessions, and NPS has repeatedly re-competed them seeking viable operators.

### USCG — Captain of the Port Maryland-National Capital Region
- **Mandate/controls:** navigation safety and the layered federal zones on the Potomac/Anacostia (33 CFR 165.508 — internal-only detail in §7). Operationally: episodic enforcement windows, transit-permission regime when activated. Source: https://www.law.cornell.edu/cfr/text/33/165.508
- **Posture: regulator** — neither Enable nor Operate; a standing stakeholder for any scheduled service, and the COTP is the named authority for zone transit authorization.

### MARAD — M-495 Marine Highway
- **Mandate:** US DOT designated the **M-495 Marine Highway Route — "the navigable portions of the Anacostia, Occoquan, and Potomac Rivers"** — including support for "operation of passenger ferry services." Sources: https://www.maritime.dot.gov/grants-finances/marine-highways/marine-highway-route-m-495-anacostia-occoquan-and-potomac-rivers · route fact sheet (Aug 2023): https://www.maritime.dot.gov/sites/marad.dot.gov/files/2024-02/Marine%20Highway%20M-495_Aug2023.pdf · WTOP explainer (2019): https://wtop.com/dc-transit/2019/11/whats-the-m-495-the-marine-highway-path-would-serve-the-d-c-areas-future-commuter-ferry/
- **Posture: ENABLE (federal endorsement + grant channel).** Our three corridors sit entirely on a federally designated marine highway — a plan-alignment gift for the Public Partners page (audience-safe wording, no security vocabulary).

### DDOT
- **Mandate:** District transportation department; leads the **Anacostia Waterfront Initiative (AWI) Transportation Master Plan** — a 30-year, ~$10B program to reshape waterfront transportation "into one that provides easy access for residents, commuters, and visitors and improves the area's environmental quality" (https://ddot.dc.gov/page/anacostia-waterfront-transportation-master-plan · https://www.anacostiawaterfront.org/about-awi). Also owns **moveDC**, the District's long-range transportation plan (https://movedc.dc.gov/).
- **Published water-transit commitment:** none located in moveDC this pass (**unverified — do not claim moveDC endorses water transit**). The AWI framework is the citable hook.
- **Posture: ENABLE.** DDOT plans/funds infrastructure and permits; it operates no vessels.

### MPD Harbor Patrol / DC Harbor Master + Office of the Mayor
- **Mandate/controls:** MPD Harbor Patrol patrols all DC waterways, "oversees the numerous marinas located in the District," runs vessel registration/titling through the Harbor Master (550 Water St SW), and issues marine event permits (https://mpdc.dc.gov/page/harbor-patrol · https://mpdc.dc.gov/node/203982). The speed-limit regime it enforces (19 DCMR Ch. 10 § 1027) vests limit-setting **in the Mayor**, with an explicit hydrofoil demonstration-permit exemption (§ 1027.3). Primary text: https://mpdc.dc.gov/sites/default/files/dc/sites/mpdc/publication/attachments/harbor_regulations_0.pdf
- **Posture: ENABLE (regulatory gate + relief grantor).** The Mayor's office is the named relief authority for DC speed rules — the single highest-leverage relationship for schedule quality.

### DMPED (Deputy Mayor for Planning & Economic Development)
- **Controls/precedent:** built and funded Diamond Teague Park and its piers ($8M District-funded; 250-ft commercial pier; water-taxi service from Aug 2009; park operations "in partnership with Coastal Properties, a commercial dock operator") — https://dmped.dc.gov/release/new-riverfront-park-opens-anacostia. The Navy Yard stop's landing is thus **District-built public water-transit infrastructure** — the strongest municipal precedent in the network.
- **Posture: ENABLE** (builds/permits waterfront assets; doesn't operate service). **Current Teague pier operator unverified this pass** (2010 source names Coastal Properties; today's operating arrangement needs confirmation).

### WMATA + MWCOG (regional context)
- WMATA operates no water transit; its relevance is modal integration (Metro at the Wharf/L'Enfant, King St-Old Town) and the proven substitution event: during the 2019 Metro platform shutdown, water taxis became the marketed alternative for Old Town↔Wharf commuting (Washingtonian, May 2019: $10 round-trip commuter promotion — https://washingtonian.com/2019/05/30/metro-shutdown-alternative-take-the-water-taxi-from-alexandria-to-dc/; the hub's "5,000 daily riders" figure is **hub canon — not independently re-verified this pass**).
- MWCOG produced the **Potomac River Commuter Ferry Feasibility Study & RPE** ("determine likely ferry service travel times between potential docking locations, assess potential environmental impacts") — https://www.mwcog.org/file.aspx?&A=b8DQqmv%2BKTpPtidwP8VwFzLzjr4EqxmA2xWzmqW4MBM%3D. NVRC maintains a Commuter Ferry Service program page (https://www.novaregion.org/1141/Commuter-Ferry-Service).
- **Posture: WMATA n/a (integration partner); MWCOG/NVRC ENABLE (studies/convening).**

### City of Alexandria
- **Controls:** owns and operates the **Alexandria City Marina, 0 Cameron St** — our interchange-primary landing; city-run docks with published hours, active tour/charter-boat program alongside (https://www.alexandriava.gov/Marina). City Cruises water taxi already serves it (https://www.cityexperiences.com/washington-dc/city-cruises/water-taxi/).
- **Published plans:** the Alexandria Waterfront Small Area Plan builds the waterfront around all travel modes "ranging from personal vehicles to water taxis" (plan PDF: https://media.alexandriava.gov/docs-archives/planning/info/masterplan/city=master=plan=map/waterfrontplancurrent.pdf); contemporary coverage framed it as making Alexandria "a water transportation hub for areas all along the Potomac" (https://www.washingtonexaminer.com/news/1421968/new-waterfront-plan-a-welcome-change-for-alexandria/ — secondary).
- **Posture: ENABLE, actively pro-water-transport.** The single friendliest municipal landing in the network: city-owned dock, ferry-habituated market, plan language on our side.

### PRTC / OmniRide + Prince William County + NVRC
- **Mandate:** PRTC (operating as OmniRide) provides commuter mobility for the I-95 corridor; it has repeatedly studied Potomac commuter ferries from Occoquan/Woodbridge ("The proposed commuter ferry would sail along the Potomac River from Occoquan or Belmont Bay to Washington and back" — InsideNova, Jan 2022: https://www.insidenova.com/headlines/ferry-to-d-c-new-analysis-underway/article_466b9f50-7ce4-11ec-b7ca-4b975d23a37b.html; WTOP 2019 M-495 coverage; https://www.omniride.com/about/). The hub's "~6,000 security-clearance holders within 15 min of the marina" claim traces to a PRTC M-495 RFI per hub canon — **RFI document not located this pass; treat as canon, cite-internally only**.
- **Posture: potential OPERATE-track partner (procures transit service today, has studied ferries), currently study-stage only.** This is the closest thing DC has to a WETA-curious authority; nothing procured — never imply otherwise.

### Prince George's County + Peterson Companies (National Harbor)
- National Harbor is a private, master-planned waterfront development "built and opened by The Peterson Companies in 2008" (https://info.security.kastle.com/resources/case-studies/national-harbor-peterson-companies); the National Harbor Marina/pier is part of the development (https://www.nationalharbor.com/directory/national-harbor-marina/), and water taxi service to Old Town/The Wharf operates from it today (Wharf↔National Harbor service launched 2018 — https://wtop.com/business-finance/2018/03/wharf-water-taxi-service-national-harbor-starts-march-1/). **The National Harbor landing is privately controlled by Peterson — a commercial landing agreement, not a public-authority relationship.**
- Prince George's County governmental posture toward water transit: **unverified this pass.**

### Maryland DNR + Virginia DWR (water-rule authorities on the south segments)
- Maryland waters (National Harbor/Fort Washington reaches): MD DNR maintains river speed zones (https://dnr.maryland.gov/boating/pages/regulations/changes_boating.aspx); specific zones for our reaches **unverified** — see SPEED-RULES file. Virginia: statewide 50-ft no-wake rule around docks (https://dwr.virginia.gov/boating/boaters-guide/safe-boating/) governs the Occoquan marina approach.
- **Posture: regulators (Enable-path permitting/rule relief).**

### Private landing controllers (not authorities — commercial counterparties)
- **The Wharf / Hoffman Madison Waterfront:** Transit Pier (950 Wharf St SW) is the water-taxi pier of the District Wharf development (developer Hoffman & Associates + Madison Marquette; manager Hoffman Madison Waterfront — https://en.wikipedia.org/wiki/The_Wharf_(Washington,_D.C.) · https://www.wharfdc.com/getting-here/water-taxi/). Underlying District land arrangements **unverified this pass** — treat the operating relationship as private.
- **Georgetown / Washington Harbour:** the water-taxi dock sits at Washington Harbour, a privately owned complex (sold 2013 for $370M to an investor group; managed by MRP Realty — https://en.wikipedia.org/wiki/Washington_Harbour · https://mrprealty.com/washington-harbour/ · https://georgetowner.com/articles/2018/06/25/washington-harbour-sell-450-million/). Dock-parcel specifics **unverified**. Adjacent Georgetown Waterfront Park is NPS — relevant to any dock modification.
- **The Yards Marina:** operated/managed by Living Classrooms (marina contact is livingclassroomsdc.org — https://www.yardsmarina.com/marina-information); note the marina's posted "no charters" dockage policy — a commercial-use conversation is required, not a walk-up. Underlying ownership within The Yards development **unverified**.
- **Occoquan Harbour Marina:** private, family-owned full-service marina (built 1981 — https://www.marinaohm.com/).
- **City Cruises (Hornblower) / Potomac Riverboat Co.:** the incumbent operator — daily water taxi connecting The Wharf, Georgetown, Old Town Alexandria, and National Harbor (https://www.cityexperiences.com/washington-dc/city-cruises/water-taxi/), the same four anchors as our DC-1 launch line. This is demand-proof and a regulatory template (Subchapter T ops on these exact corridors), and a potential operator partner per the Fleet Investors model — never a named partner without a contract.

---

## 3 · Per-stop landing control table (11 stops)

| # | Stop (hub key) | Landing owner/operator | Permit path | Relationship that unlocks it | Coverage |
|---|---|---|---|---|---|
| 1 | old-town-alexandria | City of Alexandria (City Marina, 0 Cameron St) | City dock-use agreement; VA/USACE only if structural change | City of Alexandria (marina office; waterfront plan alignment) | Verified (alexandriava.gov/Marina) |
| 2 | the-wharf | Transit Pier — Hoffman Madison Waterfront (private district manager) | Private pier agreement | Hoffman Madison Waterfront; City Cruises co-use precedent at the same pier | Verified at manager level; underlying land arrangement unverified |
| 3 | georgetown | Washington Harbour dock — private complex (investor-owned, MRP-managed) | Private landing agreement; NPS adjacency (Georgetown Waterfront Park) for any structural work | Washington Harbour ownership/MRP Realty | Partially verified (complex ownership verified; dock parcel unverified) |
| 4 | national-harbor | National Harbor Marina — Peterson Companies development | Private landing agreement | Peterson Companies | Verified at development level; marina-entity specifics unverified |
| 5 | navy-yard-teague | Diamond Teague Park Piers — District-built (DMPED), 250-ft commercial pier | District agreement (DMPED/DGS); operator confirmation needed | DMPED + current pier operator (2010: Coastal Properties — needs re-verification) | Verified (District-built); current operator unverified |
| 6 | columbia-island | Columbia Island Marina — NPS (GWMP), concession-run | NPS concession amendment / Superintendent approval (2025 Compendium clause) | NPS GWMP Superintendent + concessioner | Verified (NPS); current concessioner unverified |
| 7 | daingerfield | Washington Sailing Marina — NPS (GWMP), concession-run | NPS concession / Superintendent approval | NPS GWMP + concessioner | Verified (NPS); current concessioner unverified |
| 8 | the-yards | The Yards Marina — operated by Living Classrooms | Marina commercial-use agreement (posted no-charter policy = negotiation required) | Living Classrooms + Yards development ownership | Verified (operator); underlying owner unverified |
| 9 | james-creek | James Creek Marina — NPS (NACE), concessioner NCR Marine Services (2020 selection) | NPS concession / Superintendent approval | NPS NACE + NCR Marine Services | Verified |
| 10 | fort-washington | Fort Washington Marina — NPS (Piscataway Park), temporary concession structure | NPS concession / Superintendent approval | NPS Piscataway Park | Verified |
| 11 | occoquan | Occoquan Harbour Marina — private, family-owned | Private marina agreement | Marina ownership (Lynn/Krauss families per marina site) | Verified (marina site) |

**Coverage tally: 7 of 11 stops fully verified for landing control; 4 partially verified (georgetown dock parcel, national-harbor marina entity, navy-yard-teague current operator, the-yards underlying owner) — flagged, not guessed.** Structural theme: **zero municipal-transit-owned docks**. Landings split NPS-federal (4), municipal/District (2: Alexandria, Teague), and private (5) — this is why DC is an Enable market.

## 4 · Funding hooks

| Program | Level | What it funds | Source |
|---|---|---|---|
| FTA Passenger Ferry Grant Program (49 U.S.C. § 5307(h)) | Federal | Capital funding for ferry vessels/terminals in urbanized areas ($657M available FY2026 per Boston research) | https://www.transit.dot.gov/passenger-ferry-grants |
| FTA Electric or Low-Emitting Ferry Pilot Program | Federal | Purchase/construction of electric or low-emission ferry vessels — directly on-point for electric hydrofoils | https://sam.gov/fal/282135e5554e4674b21182aaa0780671/view |
| MARAD America's Marine Highway Program — M-495 designation | Federal | Project designation/grant eligibility on the Anacostia–Occoquan–Potomac route, explicitly including passenger ferry operations | https://www.maritime.dot.gov/grants-finances/marine-highways/marine-highway-route-m-495-anacostia-occoquan-and-potomac-rivers |
| MWCOG Potomac River Commuter Ferry Feasibility Study & RPE | Regional | Not funding per se — the regional analytic groundwork (travel times, docking locations, environmental screening) that future funding requests will cite | https://www.mwcog.org/file.aspx?&A=b8DQqmv%2BKTpPtidwP8VwFzLzjr4EqxmA2xWzmqW4MBM%3D |
| District AWI capital program (DDOT) | District | Waterfront transportation infrastructure under the AWI umbrella (Teague precedent: $8M District-funded pier/park) | https://ddot.dc.gov/page/anacostia-waterfront-transportation-master-plan · https://dmped.dc.gov/release/new-riverfront-park-opens-anacostia |

## 5 · Quality-of-life hooks (named, sourced plans)

- **Sustainable DC 2.0** — District goal: "By 2032, increase use of public transit to 50% of all commuter trips" (transportation chapter: https://sustainable.dc.gov/sites/default/files/dc/sites/sustainable/page_content/attachments/SDC2%20Transportation.pdf; goal quoted in GGWash coverage: https://ggwash.org/view/96718/bowser-administration-backs-away-from-modeshift-in-sustainable-dc-progress-report). A zero-emission water commute layer advances the mode-shift and climate pillars.
- **Anacostia Waterfront Initiative (DDOT)** — the District's own 30-year waterfront program: easy access for "residents, commuters, and visitors" plus environmental quality (https://ddot.dc.gov/page/anacostia-waterfront-transportation-master-plan).
- **M-495 Marine Highway designation** — the federal government has already designated our exact waters as an underused transportation corridor suited to passenger ferry service (https://www.maritime.dot.gov/grants-finances/marine-highways/marine-highway-route-m-495-anacostia-occoquan-and-potomac-rivers).
- **Alexandria Waterfront Small Area Plan** — city plan embraces water taxis among core waterfront travel modes (https://media.alexandriava.gov/docs-archives/planning/info/masterplan/city=master=plan=map/waterfrontplancurrent.pdf).
- **Proven behavior:** an active four-node commercial water-taxi network (Wharf–Georgetown–Old Town–National Harbor) runs today (https://www.cityexperiences.com/washington-dc/city-cruises/water-taxi/), and during the 2019 Metro shutdown water taxis were the promoted commuter alternative (https://washingtonian.com/2019/05/30/metro-shutdown-alternative-take-the-water-taxi-from-alexandria-to-dc/). The hub's "#1 worst US traffic congestion (2025 metro rank)" chip is **hub canon — verify its underlying scorecard before re-using outside the hub**.

## 6 · City classification: **primarily ENABLE** (with a Virginia Operate-curious edge)

Reasoning: (1) No public agency operates water transit in the DC region — the only scheduled operator is private (City Cruises), unlike Boston (MBTA) or the Bay Area (WETA). (2) The landing map is NPS-federal + municipal + private, so market entry runs through concession/permit/commercial agreements, not procurement. (3) The District's own posture is infrastructure-and-permits (DMPED built Teague; DDOT plans; MPD regulates; the Mayor holds speed authority). (4) The one Operate-adjacent thread is Virginia's PRTC/OmniRide ferry studies (and MWCOG's feasibility work) — a future procurement conversation worth cultivating, but study-stage only. Page weighting per PUBLIC-PARTNERS-BRIEF §2: **DC page leans Enable** — which the brief itself anticipated ("DC page leans Enable given NPS/DDOT permitting structure — research to confirm"): confirmed.

## 7 · Open flags for Jaideep

1. **NPS is the market-defining relationship** — 4 of 11 stops plus shoreline adjacency at Georgetown. The concession clause ("or as approved by the Superintendent," 2025 GWMP Compendium) is the doorway; recommend early, quiet engagement with GWMP and NACE superintendents' offices before any public page names NPS-land stops as launch-ready. Also resolve current concessioner identities (Columbia Island/Washington Sailing solicitation was cancelled in 2020 — operator today unverified).
2. **The § 1027.3 hydrofoil demonstration-permit clause is the single best regulatory finding across all seven cities so far** — DC law already contemplates Mayoral permits for hydrofoil demonstration operation. Route the relief ask through the Mayor's office with DDOT/MPD Harbor Patrol at the table. Keep expectations honest: it covers demonstration/experimentation, not standing revenue service.
3. **Diamond Teague operator verification** — the District built the pier, but the 2010 operating partnership (Coastal Properties) needs a current-state check before any claim about who grants Navy Yard landing access.
4. **Security-zone scheduling reality is internal-only** (see §8): July 4, State of the Union, and three Pentagon-adjacent dates are predictable no-service or restricted windows on core corridors, and ad-hoc enforcement windows can occur. Build these into schedule-reliability assumptions; keep all such vocabulary off every rendered surface per hub gates.
5. **Private-landing concentration risk:** Georgetown (Washington Harbour), The Wharf (Hoffman Madison), and National Harbor (Peterson) are all single-owner private landings — the entire DC-1 flagship line depends on three commercial agreements plus one city dock. No dock-status vocabulary on rendered pages (hub gates ban it), but sequence outreach accordingly.
6. **PRTC/M-495 RFI document** not located this pass — the hub's "6,000 clearance holders within 15 min" stat stays internal until the RFI or an equivalent source is in hand.
7. **Maryland-water speed zones unverified** for National Harbor/Piscataway reaches; a MD DNR zone-map pull is needed before Phase 3 schedule claims.
8. **DOEE and USACE permitting paths not deep-profiled** — recommend legal/regulatory review before any pilot commitment, same flag as Boston.

## 8 · HELD — internal only, never renders

Per hub `gates` (banned terms include the federal-zone citation and related vocabulary; `security_zones_internal_only: true`): the federal overlay analysis lives in `SPEED-RULES-WASHINGTON-DC.md` §3 (zones, enforcement dates, COTP transit-permission process, 410-576-2693 / VHF 16). Additional internal-only geography: Joint Base Anacostia-Bolling and Fort McNair flank the lower Anacostia approach, the Pentagon reservation flanks the DC-3 spur, and Reagan National's riverside boundary sits along the DC-1 spine — all are context for federal-stakeholder engagement, none are corridor claims, and none of it may appear in rendered copy. Hub gate `hq2_shuttle_honesty` (Daingerfield is shuttle-tier to National Landing; no dock at HQ2) is respected throughout this file.
