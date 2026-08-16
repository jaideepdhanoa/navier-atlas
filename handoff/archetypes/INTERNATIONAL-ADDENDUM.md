# International city addendum (UAE run: Dubai → Abu Dhabi → Ras Al Khaimah)

Deltas vs CITY-RESEARCH-TEMPLATE.md. Everything not amended here follows the domestic template + archetype contract v3.

## Page pair (NO employer page)
1. **Public Transport page** (`public-partners.json`, same contract): authority-audience per PTA skill. The authority's OWN mandate leads (published plans, existing marine transit ops). Enable/Operate posture → **"extend your marine network"** (these authorities already operate water transport; posture is augmentation). Domestic-first routing: emirate-internal corridors lead; inter-emirate/cross-border appear as later-phase roadmap only.
2. **Fleet Investor page** (`fleet-investors.json`, same contract): utilization stack rebuilt on local inputs; **tourism-weighted** — L3 experiences moves from garnish to headline layer where sourced yields support it. Demand pools = sourced visitor/resident flows (not employer trackers), labeled indicative.

## Tourism layer (both pages)
Sourced visitor volumes, hotel stock, marquee attractions on the water. On PT page: "visitor economy" section. On FI page: L3 sized from sourced local experience/charter benchmarks. No invented yields.

## Economics
- Currency: render USD; every local benchmark cited in AED with source; peg 3.6725 AED/USD.
- Crew cost: BLS method not applicable. Use sourced UAE maritime wage benchmarks (captain + deckhand), state explicit burden (visa/insurance/accommodation allowances customary in UAE marine employment), explicit assumptions, LOW/MID $/hr loaded for 2-person crew. Label method UAE-ADAPTED.
- Season: 12-month operating year; summer-heat midday shape (Jun–Sep demand dip midday, evening peak) replaces winter discount. State the shape assumption.
- Seat pricing: no canon for these markets. Derive from local premium substitutes (RTA/authority marine fares, premium ride-hail, chauffeur, charter rates), label DERIVED, flag for Jaideep confirmation.
- Vessels: N45 20-seat commuter stack (canon); N30 for premium/experience variants where the stack says so. $2.5M N45 / $1.5M Quanta LR / N30 canon capex. Energy $0.30/kWh unless a sourced local tariff is cheaper — use sourced DEWA/EWEC/EtihadWE commercial tariff if found, cited.

## Geometry (fail closed — sealed sets are contaminated outside Dubai)
- Base inventory: `GEOMETRY-{CITY}.json` in the city folder (extracted from sealed corridors + canonical marquees).
- **Dubai:** sealed set clean (35 routes). Bind lines to sealed route_ids.
- **Abu Dhabi:** only ~7 BPs in the sealed set are genuinely AD. Corridor spine = partner-file journeys (Yas Bay↔Al Raha · Corniche↔Saadiyat · Reem↔Corniche · Eastern Mangroves↔Yas) + research-verified landings. Note: several AD BPs (Al Bandar, Al Qana, Hudayriat, ADNEC marinas) are mis-tagged into the RAK sealed file — cite labels, not RAK route_ids.
- **RAK:** sealed set unusable (mis-geocoded Dubai/AD POIs). Corridor spine = RAKTA partner journeys (Al Marjan↔Al Hamra · Mina Al Arab↔RAK corniche · Al Marjan↔corniche · RAK Creek↔Jazirat Al Hamra) + research-verified landings only.
- Every rendered stop must be a research-verified real landing (existing marina/ferry terminal/marine station; "planned" facilities rendered only with status flag and source).
- Mis-geocode findings go in the research record for Grok locale cleanup (#119) — never re-tag Atlas data in the microsite pass.

## Disclosure rails (kill-scan additions for UAE)
Firewalled everywhere: royal office / any Gulf counterparty identity · LOI existence · LC-180 / AD Ports · program fleet counts, costs, timelines · "committed fleet" numbers from partner JSONs (internal). Public authority facts (RTA Marine Transport Master Plan 2030, Abu Dhabi Mobility operations, RAKTA Marine Transport Project, Wynn Al Marjan as published development) are fine WITH primary sources. Pipeline timing canon (RTA/ITC 2028, RAKTA 2029) must not be contradicted; microsites carry no launch dates.

## Consistency with authority decks
Same corridors, same phase logic, same fleet ceilings as the partner-pitch authority JSONs — the microsite is the pre-read/leave-behind layer; the deck is the meeting artifact. Never contradict; never copy unverified deck numbers — re-verify every rendered claim.

## Repo layout (same as domestic)
`employer-hub/hubs/{dubai|abu-dhabi|ras-al-khaimah}/` — two JSONs + `assets/hero-fleet-*.jpg` + `assets/hero-public-*.jpg`
`handoff/archetypes/{city}/` — research MDs. One PR per city, sequential.
