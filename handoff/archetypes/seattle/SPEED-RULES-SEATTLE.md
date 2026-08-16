# Seattle / Puget Sound speed & wake rules — primary-source verification pass

**Date:** 2026-08-16 · **Status:** research-complete, primary sources cited by section number · **Scope:** the hub.json network (Sound cluster in-scope: SND-1 Elliott Bay Line, SND-2 Sound Line, SND-3 Narrows Line; Lake Washington cluster documented for the record — excluded from the network per locked scope rule).
**Fail-closed rules:** every rule claim carries a statute/regulation citation or is marked **unverified**. Base schedule math ALWAYS respects posted limits. Relief framing appears only under "what relief unlocks."

---

## 1 · PRIORITY VERIFICATION ITEM — the "8-knot Lake Washington limit" claim

**Result: the claimed blanket "8-knot Lake Washington speed limit" DOES NOT EXIST in any primary source located.** What actually governs Lake Washington is a set of *shore-buffer* rules plus one *seasonal federal* rule:

| Instrument | What it actually says | Where it applies | Source (primary) |
|---|---|---|---|
| **SMC 16.20.130.A** (Seattle Harbor Code) | **7 knots within 100 yards** of any shoreline, pier, restricted area or shore installation **in Lake Washington** (Seattle's jurisdictional waters) | Seattle shoreline of Lake Washington (e.g., Leschi) | Seattle Municipal Code Title 16, § 16.20.130.A — text verified from the City Clerk's archived SMC Title 16 file (Ord. 87983 § 7A, 1959; last amended Ord. 120451 § 1, 2001): http://clerk.seattle.gov/~F_archives/historicsmc/2006/2006SMC_T016%20-%20Title%2016%20%20HARBOR%20CODE1.pdf |
| **KCC 12.44.090** (King County Code) | **8 miles per hour within 100 yards** of any shoreline, pier, restricted area or shore installation on Lake Washington or Lake Sammamish (Ord. 1235 § 4, 1972) | King County jurisdictional waters of Lake Washington | https://aqua.kingcounty.gov/council/clerk/code/15_Title_12.htm |
| **KCC 12.44.070** | 8 mph general limit **on lakes** in King County "except on lakes otherwise specifically provided for" (Ord. 1235 § 2, 1972) — Lake Washington *is* otherwise provided for by 12.44.090's buffer rule | Small King County lakes | Same Title 12 source |
| **33 CFR § 165.1341** (USCG RNA) | Minimum-wake speed, **7 mph or less**, unless more is needed for bare steerageway | Lake Washington **south of the I-90 west-bound bridge** to a Bailey Peninsula–Mercer Island line; **enforced only around Seafair** (annual notice of enforcement; 2026 notice published July 2, 2026) | https://www.law.cornell.edu/cfr/text/33/165.1341 · https://www.federalregister.gov/documents/2026/07/02/2026-13414/regulated-navigation-area-lake-washington-seattle-wa |
| **RCW 79A.60.030** | No numeric limit — negligent-operation standard requiring "careful and prudent rates of speed … taking into account … effects of vessel wake" | All Washington waters, including mid-lake | https://app.leg.wa.gov/rcw/default.aspx?cite=79A.60.030 |
| **WAC 352-60** (State Parks boating rules) | Safe-speed/steering-and-sailing rules mirroring COLREGS/Inland Rules (WAC 352-60-070(3): "every vessel shall at all times proceed at a safe speed"); **no numeric Lake Washington cap** | Statewide | https://app.leg.wa.gov/wac/default.aspx?cite=352-60-070 |

**Read-through (internal):** mid-lake Lake Washington between the 100-yard buffers carries **no numeric speed cap outside Seafair enforcement windows** — the controlling rules there are the state negligent-operation/safe-speed standards. The prior internal "8-knot Lake Washington limit" claim appears to be a conflation of KCC 12.44.090's 8-mph **shore buffer** with a lake-wide cap. Note carefully: this verification result means the lake-exclusion scope rule rests on **network/scope grounds as locked by decision, not on a blanket lake-wide speed prohibition** — hub.json's own LKW-1 routing note ("Mid-lake is unrestricted") is consistent with the primary sources. Eastside shoreline cities (Bellevue, Kirkland, Mercer Island, Renton — e.g., the RMC 9-3-7 and Mercer Island buoy rules named in hub.json) were **not primary-verified this pass** because the lake cluster is out of network scope; flag for a future pass only if scope changes.

---

## 2 · What governs the in-scope Sound corridors

### (a) Elliott Bay (SND-1: Seacrest ↔ Bell Harbor ↔ Elliott Bay Marina)

- **SMC 16.20.130.A:** 7 knots **within 200 yards** of any shoreline, pier, restricted area or shore installation "in all other waters of the City" — i.e., Elliott Bay and the Duwamish carry a 200-yard 7-knot shore/pier buffer (vs 100 yards on the lake). Source: archived SMC Title 16 file above.
- **SMC 16.20.130.F:** **3 knots** inside the breakwater at Shilshole Bay Marina, **Elliott Bay Marina**, "or within the confines of any established marina or boat moorage area" — this is the marina-approach constraint at both Bell Harbor and Elliott Bay Marina. Where two subsections overlap, **the lowest maximum speed controls** (§ 16.20.130 closing text).
- **SMC 16.20.132:** compliance with the speed limits does **not** exempt an operator from liability for wake damage — Seattle's code separates the numeric cap from an outcome-based wake-liability rule.
- **Open-bay water between the buffers has no numeric municipal cap**; RCW 79A.60.030 safe-speed/wake-effects and COLREGS (adopted by SMC 16.20.020) govern, plus USCG Captain of the Port Puget Sound authority. Ferry-traffic separation from WSF Colman Dock, Kitsap Pier 50, and KCWT operations is an ops-planning duty, not a codified speed zone.
- **Enforcement:** Seattle Police Harbor Patrol enforces the Harbor Code (https://www.seattle.gov/police/about-us/about-policing/harbor-patrol); USCG Sector Puget Sound is COTP.

### (b) Duwamish Waterway

- Same SMC 16.20.130.A 200-yard/7-knot buffer regime (city waters). Federal overlay: 33 CFR 165.1340 establishes a safety zone for Vigor Industrial drydock movements in the West Duwamish Waterway (adjacent section to the RNA cited above at law.cornell.edu). **No hub.json corridor touches the Duwamish** — documented for completeness only.

### (c) Lake Union / Ship Canal (no hub.json stops — for the record)

- **SMC 16.20.130.B:** 7 knots throughout Lake Union (daylight speed-test area excepted, tightly constrained).
- **SMC 16.20.130.A:** blanket 7 knots "upon the Lake Washington Ship Canal and adjacent waters east of the entrance buoy at Shilshole Bay to one hundred (100) yards east of Webster Point light."
- **SMC 16.20.130.C:** **4 knots** between the guide piers of the Hiram M. Chittenden (Ballard) Locks.
- This is the primary-source confirmation of hub.json's SLU decision-ledger entry: the Ship Canal system is speed-capped end-to-end with no exemption mechanism visible in the code — relief would require a code amendment, and the Locks themselves (USACE-operated) are a queue, not a schedule. Matches the locked "no Lake↔Sound connector" rule.

### (d) Encounter-conditional rule the whole Sound network must plan for

- **RCW 77.15.740** (as amended 2023, effective Jan. 1, 2025): it is unlawful to exceed **7 knots within 1/2 nautical mile of a southern resident killer whale**, and vessels must stay ≥1,000 yards away. This is *encounter-conditional* (triggered by whale presence anywhere on the Sound), not a zone on a chart. Primary: https://app.leg.wa.gov/rcw/default.aspx?cite=77.15.740 — **NOTE: this citation and the species reference are on hub.json's `banned_terms` list for rendered copy; internal ops/audit use only.** Schedule math cannot "reserve" for this; treat as an ops-reliability factor akin to weather. (Statute text not re-scraped this pass; section number and 1,000-yd/7-kn parameters from the 2023 session-law coverage — **verify verbatim text before any external legal claim.**)

### (e) Tacoma / Thea Foss Waterway and Gig Harbor (SND-3)

- Local harbor-speed instruments for the Thea Foss Waterway and Gig Harbor entrance were **not primary-verified this pass** (Gig Harbor municipal ordinance archive returned no machine-readable text; hub.json already flags this as "local rule text unverified — internal ops item"). **Fail closed:** keep SND-3 times labeled indicative; verify Tacoma Municipal Code Title 5/City of Gig Harbor ordinances before publishing any Narrows schedule claim.

---

## 3 · Who sets and enforces, and each rule's stated purpose

| Rule | Setter | Enforcer | Stated/structural purpose |
|---|---|---|---|
| SMC 16.20.130 | Seattle City Council (Harbor Code) | SPD Harbor Patrol | Shore/pier protection: buffers scale with proximity to shoreline, piers, moorages; § 16.20.132 separately preserves wake-damage liability |
| KCC 12.44.070/.090 | King County Council | King County Sheriff Marine Unit | Shoreline protection on the lakes (1972 ordinances) |
| 33 CFR 165.1341 | USCG (COTP Puget Sound) | USCG + designated reps | Event-safety minimum-wake condition around Seafair |
| RCW 79A.60.030 / WAC 352-60 | State Legislature / State Parks | WDFW police, county sheriffs, local marine units | Outcome-based: speed reasonable for conditions "taking into account … effects of vessel wake" |
| RCW 77.15.740 | State Legislature | WDFW police | Wildlife disturbance/noise — explicitly purpose-based |

## 4 · What relief unlocks (labeled upside only — never base)

- **The structure favors a foiling vessel more than the numbers do.** Seattle's buffers are proximity-based numeric caps, but the state layer (RCW 79A.60.030) and Seattle's own § 16.20.132 are **wake-outcome** rules. A foilborne N45 producing near-zero wake serves the buffer rules' purpose at speeds above 7 knots; the caps' numbers were calibrated for displacement hulls.
- **The strongest relief precedent in the country is local:** Kitsap Transit's *Rich Passage 1* — a foil-assisted low-wake catamaran purpose-built (2009–2012 research program, FTA-funded) to run **38 knots through wake-sensitive Rich Passage** after beach-monitoring studies demonstrated no shoreline damage. That is a Washington transit agency solving a wake constraint with hydrofoil technology and operating it daily. Source: https://en.wikipedia.org/wiki/Kitsap_Fast_Ferries (secondary; underlying studies are Kitsap Transit/FTA documents — pull before citing in-page). Add Stockholm Candela P-12 (~22 kn in a ~12 kn zone, Länsstyrelsen exemption) per `../SPEED-RULE-RELIEF-PRECEDENTS.md`.
- **Relief pathway per rule:** SMC buffer relief requires City action (no exemption mechanism visible in § 16.20.130 — code amendment or harbor-master-level marked-channel instrument; **unverified** whether Seattle has a marked-channel permission mechanism analogous to Massachusetts 323 CMR 2.07(3)(d)); the Seafair RNA runs through the COTP under the federal instrument; the county buffers via King County Council. Ask posture: "measure our wake at speed, then align the number with the rule's purpose."
- **What it would unlock (indicative, internal):** on SND-1 the buffers dominate short legs (2.2-nm legs with 200-yd buffers at both ends); buffer relief at, e.g., 15 kn low-wake approach would cut several minutes per leg and materially lift cycle counts. Do not quantify in any rendered artifact until wake measurements exist.

## 5 · Sea-state and season honesty (operational, not regulatory)

- Puget Sound commuting is proven **year-round** (WSF 19.1M riders in 2024; Kitsap Fast Ferries and KCWT run all winter — Kitsap suspended only off-season *Saturday* sailings in 2025). Sources: https://wsdot.wa.gov/about/news/2025/back-board-2024-brought-half-million-more-state-ferry-riders · https://en.wikipedia.org/wiki/Kitsap_Fast_Ferries
- Winter southerlies produce chop and small-craft-advisory days on the open Sound (NWS Seattle marine zones; forecast feed: https://www.ndbc.noaa.gov/data/Forecasts/FZUS56.KSEW.html). The N45 is foilborne through chop that stops displacement small craft, but **no Navier vessel has operated a Puget Sound winter** — treat winter reliability as an operational consideration with published cancellation-policy design, not a marketing claim. Longer SND-2 legs (Des Moines, Edmonds, Kingston) carry more exposure than the Elliott Bay locals.

## 6 · Verification ledger

| Claim | Status |
|---|---|
| "8-knot Lake Washington limit" (prior internal claim) | **CLOSED — no such blanket rule found in SMC, KCC, WAC, RCW, or CFR.** Nearest real rules: KCC 12.44.090 (8 mph/100 yd) and SMC 16.20.130.A (7 kn/100 yd) shore buffers + seasonal Seafair RNA |
| SMC 16.20.130 subsection text | Verified against City Clerk archived Title 16 file (2006 archive; latest amendment shown Ord. 120451, 2001). **Current Municode consolidation not machine-readable this pass** — re-verify section text on Municode before quoting in any external document |
| KCC 12.44.070/.080/.090 | Verified from King County Council clerk's Title 12 code file |
| 33 CFR 165.1341 + 2026 enforcement notice | Verified (Cornell LII + Federal Register) |
| RCW 79A.60.030, WAC 352-60-070 | Verified (leg.wa.gov) |
| RCW 77.15.740 parameters | Section identified; verbatim current text **not re-pulled** — verify before external use |
| Bellevue/Kirkland/Mercer Island/Renton municipal rules | Not verified this pass (out of network scope) |
| Tacoma/Gig Harbor harbor-speed ordinances | **Unverified — fail closed**, SND-3 stays indicative |

---

## 7 · SCOPE CHANGE — Lake Washington cluster REOPENED (Jaideep directive 2026-08-16)

The lake-exclusion scope rule is lifted. Basis: §1's finding (no blanket lake-wide speed limit exists) plus the Eastside primary-verification pass in `EASTSIDE-VERIFICATION-2026-08-16.md`. LKW-1 Cross-Lake and LKW-2 Eastside re-enter the rendered network.

**Eastside verification results (supersedes §1's "not verified this pass" flags and the ledger rows below):**

| Jurisdiction | Rule | Status |
|---|---|---|
| Kirkland | **KMC 14.24.030** — 7 kn within 100 yd of shore/pier/shore installation | **VERIFIED** (primary) |
| Renton | **RMC 9-3-7.A/.B** — **8 kn** within 100 yd (not 7 as previously assumed); no-wake extends to bridges within 100 yd (relevant near south-end I-405 crossing) | **VERIFIED** (primary) |
| Bellevue | Posted 7 kn within 300 ft of shore/docks/swim areas (Meydenbauer Bay) | **PARTIALLY VERIFIED** — rule confirmed via official city source, but rests on uncodified 1962 Ord. 540; **no BCC section number may be cited externally** until legal follow-up |
| Mercer Island | **No independent MICC vessel-speed ordinance found** (negative finding). Waters policed to KCC 12.44.090 (8 mph/100 yd) via shared Marine Patrol | UNVERIFIED as codified MICC cite; "Mercer Island buoy rules" = physical buoys marking the standard county buffer, not a distinct city regulation |

**Corrections to prior internal notes:** "RMC 9-3-7" applies to Renton only — the prior conflation with Kirkland is wrong (Kirkland = KMC 14.24.030). Renton's buffer is 8 kn, not 7.

**Mid-lake sanity check (re-confirmed):** no numeric cap on the open SR-520↔I-90 crossing outside 100-yd/300-ft shore buffers and outside the Seafair RNA window — state safe-speed conduct standard only. hub.json's LKW-1 "12–15 min" cross-lake claim is consistent with the verified rules.

**Rendering rules for the lake cluster:** LKW-2 shore-adjacent legs stay `speed_constrained` with "indicative — subject to local shore buffers" labels (buffers dominate short Eastside hops). No Bellevue code section number in any rendered artifact. Seafair RNA is a seasonal operations note, not a corridor blocker.
