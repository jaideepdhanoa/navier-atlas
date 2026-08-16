# Bay Area speed & wake rules — corridor controls (v3 pipeline)

**Date:** 2026-08-15 · **Status:** source-verified desk pass (web) · **Scope:** the 5-line / 22-station network in `hub.json` (BA-1 Peninsula Trunk, BA-2 Marin, BA-3 East Bay Trunk, BA-4 Southeast Bay, BA-5 North Bay Express). Fail closed: every rule below carries a primary source or is flagged **unverified**. Base schedule math ALWAYS respects posted limits; relief framing appears only in §4, labeled "what relief unlocks."

## 1 · The controlling structure (who sets what)

| Layer | Instrument | What it controls | Source |
|---|---|---|---|
| State statute | **California Harbors & Navigation Code § 655.2** | 5 mph limit within 100 ft of a bather and within 200 ft of (A) a beach frequented by bathers, (B) a swimming float/diving platform/lifeline, or (C) **"a way or landing float to which boats are made fast or that is being used for the embarkation or discharge of passengers"** — in areas "not otherwise regulated by local rules and regulations" | https://law.justia.com/codes/california/code-hnc/division-3/chapter-5/article-1/section-655-2/ |
| Local rules | Locally imposed speed regulations adopted pursuant to **HNC § 660** (referenced in § 655.2(c)); harbor/city ordinances and posted no-wake zones | Marina basins, channels, special districts — e.g., Richardson Bay (below) | § 655.2(c), same URL; RBRA Ordinance 91-1 below |
| Federal RNA | **33 CFR 165.1181** — San Francisco Bay Region Regulated Navigation Area | 15-knot cap applies only to power-driven vessels **of 1,600 or more gross tons** (or tugs with tows ≥1,600 GT); all vessels must "navigate with particular caution" in precautionary areas and at traffic-lane/channel terminations | https://www.ecfr.gov/current/title-33/chapter-I/subchapter-P/part-165/subpart-F/subject-group-ECFR74589bc369d0095/section-165.1181 |
| Federal safe-speed duty | USCG Navigation Rules (Rule 6) | Safe speed at all times; no nationwide numeric no-wake standard | https://www.navcen.uscg.gov/navigation-rules-amalgamated (per `../SPEED-RULE-RELIEF-PRECEDENTS.md`) |

**Key structural finding (contrast with Boston):** open San Francisco Bay carries **no general numeric speed cap for a vessel of the N30/N45 class** — the RNA's 15-knot cap is tonnage-gated at 1,600 GT, far above an N45. Existing public ferries routinely run high-speed service on these same waters (WETA's REEF program is building "the nation's first high-speed, high-capacity zero-emission vessels" — https://sanfranciscobayferry.com/our-ferry-future/). The controlling constraints on the hub.json corridors are therefore **terminal-approach and marina-basin rules**, not open-water caps.

## 2 · Rules by corridor (hub.json lines only)

| Line | Corridor segments (hub.json) | Controlling rules found | Enforcement |
|---|---|---|---|
| BA-1 Peninsula Trunk | Ferry Building–South Beach–Mission Bay–Brisbane–Oyster Point–Coyote Point–Redwood City | HNC § 655.2 (5 mph within 200 ft of landing floats/marina docks) at every marina-based stop (South Beach Harbor, Brisbane Marina, Oyster Point Marina, Coyote Point Marina, Redwood City Municipal Marina); open-bay legs uncapped for this vessel class (§1) | City/county harbormasters & police marine units; USCG. Stop-specific posted basin limits **unverified this pass** — verify each marina's posted rules before schedule lock |
| BA-2 Marin | Larkspur–Tiburon–Sausalito–Ferry Building | **Richardson Bay Regional Agency Ordinance 91-1: 5 mph limit in the Sausalito Channel**; within the harbor "due caution must be observed at all times" (https://www.rbra.ca.gov/files/d2f17031d/ord91-1.pdf). HNC § 655.2 at landings. Larkspur approach (Corte Madera Channel) — ferry-channel-specific limits **unverified this pass** | RBRA harbormaster, Marin County sheriff, city PDs, USCG |
| BA-3 / BA-4 East & Southeast Bay | Oakland JLS–Alameda Main–Ferry Building; +Harbor Bay–Oyster Point | Oakland Estuary transit: City of Alameda marine enforcement states **"NO vessel shall travel more than 5 mph when within 200 feet of any floating dock or marina"** (citing HNC § 655.2(a)(2)) and that within posted NO WAKE zones vessels must be off-plane and fully settled (https://www.alamedaca.gov/Departments/Police-Department/Bureau-of-Field-Services/Boating-Laws-and-Safety). The estuary is dense with marinas on both banks — effective transit speed through the JLS–Alameda Main segment is materially constrained | Alameda PD marine patrol, Oakland PD, USCG |
| BA-5 North Bay Express | Antioch–Pittsburg–Martinez–Benicia–Vallejo–Richmond–Berkeley–Emeryville–Treasure Island–Ferry Building | HNC § 655.2 at each marina landing; Carquinez Strait/San Pablo Bay open-water legs uncapped for this class (§1); RNA precautionary-area caution duty near Central Bay (33 CFR 165.1181(e)) on the Treasure Island–Ferry Building approach. Delta-side local rules (Antioch/Pittsburg) **unverified this pass** | County sheriffs' marine units, city PDs, USCG Sector San Francisco |

**Stated purpose of each rule class:** HNC § 655.2 is a **proximity/safety** rule (bathers, swim floats, passenger landings); posted marina no-wake zones are **wake-damage** rules (Alameda PD: skippers are "financially and legally liable for any damage or injury caused by their vessel's wake"); the RNA is a **traffic-safety** instrument for large-vessel interaction; Rule 6 is a general safety duty.

## 3 · What this means for base schedule math

- hub.json `water_min` values stand as the base: open-bay legs are legally available at foiling speed for this vessel class, and the 5-mph zones bind only within ~200 ft of landing floats and inside marina basins — functionally the docking/undocking minute(s) already inside hub.json's per-stop dwell allowance.
- The slow-transit exception is the **Oakland Estuary (BA-3/BA-4)** and the **Sausalito Channel (BA-2)**, where 5-mph zones extend beyond the immediate berth. Schedule modeling for those segments should assume displacement-speed transit inside the constrained reaches. hub.json's 4-min JLS–Alameda Main time (0.9 nm ≈ 13.5 kn average) **may be optimistic against a 5-mph reading of the estuary's marina-adjacency rule — flagged for schedule validation, not silently changed here.**

## 4 · What relief unlocks (labeled upside only — never base)

- **The relief case is narrower than Boston's.** Massachusetts caps headway speed in broad regulated zones; the Bay Area's §655.2 is proximity-triggered and safety-purposed, so most of the network already runs at full speed legally. Relief matters only in the estuary/channel reaches (BA-2, BA-3/BA-4).
- Where the binding rule is a **posted no-wake zone** (wake-damage purpose), a foiling Navier serves the rule's purpose at speed — the Stockholm Candela P-12 precedent applies (~22 kn in a ~12 kn zone under a Länsstyrelsen low-wake exemption; formal instrument unverified — see `../SPEED-RULE-RELIEF-PRECEDENTS.md`). The ask to Alameda/Oakland/RBRA marine-enforcement authorities: measure wake and noise, then permit marked-channel transit speeds where the wake-purpose is met.
- Where the binding rule is **§ 655.2 proximity** (bather/passenger safety), low wake is *not* an automatic compliance argument; relief runs through local rulemaking under § 660 or does not exist. Do not present § 655.2 relief as available.
- Indicative upside if estuary/channel relief were granted: ~2–4 minutes per affected leg (derived from hub.json distances at 5 mph vs foiling speed) — label "what relief unlocks" only.

## 5 · Unverified / follow-up flags

1. Per-marina posted basin speed rules for all 22 stops (only Alameda and Richardson Bay were primary-verified this pass).
2. Larkspur ferry channel (Corte Madera Channel) — whether GGBHTD ferry operations carry channel-specific speed guidance.
3. VTS San Francisco (33 CFR Part 161) participation requirements for a Subchapter T N45 — **not researched this pass; legal review before any pilot.**
4. USCG security zones (e.g., around anchored vessels, Alcatraz events) that intermittently affect Central Bay transits — operational awareness item, not a standing speed rule; unverified this pass.
5. HNC § 660's exact local-adoption mechanism text was not directly pulled; § 655.2(c)'s reference to it is the cited basis.
