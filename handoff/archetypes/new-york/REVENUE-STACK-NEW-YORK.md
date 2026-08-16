# Revenue-Stack Model — Fleet Investors Archetype (New York)

**Date:** 2026-08-16 · **Status:** DRAFT for Jaideep review — Boston D6′ utilization-stack template applied to New York; all city benchmarks sourced inline (this city has no separate benchmarks file; URLs are in the tables below)
**Companion files:** `CREW-COST-NEW-YORK.md` (loaded crew rate), `hub.json` (all corridors/distances), `../boston/REVENUE-STACK-BOSTON.md` (approved template)
**Fleet Investors firewall applies:** vessel-fleet financing only; no Navier equity/round content. Hub gates honored (no employer names, no dock-unlock vocabulary, `ny_c_honesty`: no raw-speed claims vs Metro-North).

---

## 1 · What is different about New York (stated plainly)

New York is the only market in the program where a **subsidized $4.50 flat-fare public ferry** (NYC Ferry) and a **free public ferry** (Staten Island) already run on or near several of our corridors. That backdrop is why the locked NY seat canon is the lowest in the program: **$650–750/seat-month where a ferry alternative exists, $750–900 where none does** (hub.json `locked_numbers`, Jaideep 2026-08-15). Combined with the highest marine labor costs in the program (`CREW-COST-NEW-YORK.md`: $130/hr loaded model value vs Boston's $85), the per-vessel stack pays back **slower than Boston at identical fills** — that is a finding, not a flaw, and it is shown honestly below. The NY case leans harder on (a) **gap corridors** (CT Express, LI Sound, Bronx, New Rochelle — no ferry alternative), (b) the **deepest experience/charter market in the US** for L3, and (c) network scale (9 lines, 38 stations).

## 2 · The frame (unchanged from D6′)

One asset, one day, four demand layers: L1 committed commuter bundles + L2 spot seats + L3 experiences/charters in base; U1 sponsorship + U2 overnight cargo as upside-only lines. The launch trigger (60–80 committed seats/corridor) is unchanged. No anchor-tenant subsidy anywhere.

## 3 · Pricing methodology — NYC benchmark anchors (all sourced 2026-08-16)

| Layer | Product | NY pricing logic | Benchmark anchors (sourced) |
|---|---|---|---|
| **L1 · Committed bundles** | Monthly seat (AM+PM) | **Canon bands, blended by corridor type** (see blend math below): $650–750 transit-parity · $750–900 gap. Sanity vs substitutes: parity band ≈ 2.3–2.7× NY Waterway's published 30-day pass ($279.50 Port Imperial↔Midtown, page effective Nov 2014 — dated, flagged); gap band vs Metro-North New Haven monthlies $314.25 (Greenwich) – $465.25 (Milford zone) **plus** last-mile, positioned as comfort/direct-to-waterfront, never raw speed; and vs door-to-door car: Uber New Rochelle→Manhattan ~$71 avg (≈$2,272/mo at 32 trips), Port Washington→Manhattan ~$96 avg, plus $9/day congestion toll and ~$570/mo Manhattan parking | NYC Ferry $4.50 / 10-trip $29: https://www.ferry.nyc/ticketing-info/ · NY Waterway passes: https://www.nywaterway.com/tickets.aspx (effective Nov 2014 — **dated, flagged**) · Metro-North: https://www.mta.info/document/194941 · Uber route averages: https://www.uber.com/global/en/r/routes/new-rochelle-ny-to-manhattan-ny/ · https://www.uber.com/global/en/r/routes/port-washington-ny-to-manhattan-ny/ · congestion toll: https://www.mta.info/fares-tolls/tolls/congestion-relief-zone/about · parking ~$570/mo avg: https://spothero.com/city/monthly/nyc-parking (matches hub.json calculator default — canon) |
| **L2 · Spot seats** | Per-leg, residual capacity | **$30–45 yield-managed**, bounded below by SeaStreak's premium walk-up ($30 One Way Flex — the proof a premium spot fare clears in this harbor) and above by Uber route averages ($71–96 on gap corridors). On parity corridors spot skews to the $30 floor; on gap corridors toward $45+ | SeaStreak: https://seastreak.com/ferry-routes-and-schedules/between-new-jersey-and-new-york-city/ ($30 flex; 40-trip $782 = $19.55/trip, ~35% pass discount — same structure as our L1-vs-L2 spread) · Blade pass-vs-spot (NYC): $95 w/ pass vs ~$195 walk-up: https://www.blade.com/airport-pass |
| **L3 · Block products** | Experiences (per-person), charters (per-hour) | Experiences **$59–79/pp** — inside the observed NYC band: Classic Harbor Line sightseeing from $52, jazz $98, sunset ~$114 (secondary); Circle Line listed departures $29–54. Charters **$600–800/hr** for a 20-pax premium vessel — Sailo Manhattan: luxury motor yachts start ~$600/hr (to $2,500); Boatsetter NYC yachts from $800 | CHL NYC: https://sail-nyc.com/public-cruises/sightseeing-nyc-boat-tour-with-statues-and-skylines/ · https://sail-nyc.com/public-cruises/evening-jazz-cruise-in-nyc-on-yacht-manhattan/ · Tripadvisor (secondary): https://www.tripadvisor.com/Attraction_Review-g60763-d1488018-Reviews-Classic_Harbor_Line-New_York_City_New_York.html · Circle Line: https://www.circleline.com/ · Sailo: https://www.sailo.com/boat-rentals/NY/New_York/Manhattan · Boatsetter: https://www.boatsetter.com/boat-rentals/new-york--ny--united-states |

**L1 blend math (the modeled vessel).** The modeled N45 runs 8 commute legs/day: **5 legs on transit-parity corridors** (East River trunk / Hudson spine, ~6 nm avg leg) and **3 legs on a gap corridor** (LI Sound west end, e.g., New Rochelle→E 34th, 13.6 nm — corridor and distance from hub.json). Committed seats are blended in the same 62.5/37.5 proportion:

| Scenario | Parity seats × price | Gap seats × price | L1 total | Blended $/seat |
|---|---|---|---|---|
| Conservative | 16 × $650 = $10,400 | 8 × $750 = $6,000 | **$16,400** | $683 |
| Mid | 20 × $700 = $14,000 | 12 × $825 = $9,900 | **$23,900** | $747 |
| Upside | 22 × $750 = $16,500 | 14 × $900 = $12,600 | **$29,100** | $808 |

Prices never leave the locked canon bands; the blend only shifts weight between them.

## 4 · The four levers — defensibility grading (NY)

| Lever | Market-proven in NY? | Navier-proven? | Treatment |
|---|---|---|---|
| L1+L2 commute yield | ✅ strongest in program: NYC Ferry 7M+ riders/yr (https://edc.nyc/press-release/mayor-nycedc-announce-record-breaking-nyc-ferry-ridership-numbers-summer-2025); SeaStreak proves premium fares; NY Waterway proves private pass commuting | Partially — canon bands locked, no NY operations | **Base case**, conservative fills |
| L3 experiences & charters | ✅ deepest US market (CHL, Circle Line, City Cruises, charter marketplaces — priced above) | ❌ | **Base at thin utilization** (conservative = 10 sailings/mo vs incumbents' multiple-daily schedules) |
| U1 Sponsorship | ✅ NYC precedents are the program's best: Citi Bike ~$7–8M/yr system title (https://www.nyc.gov/html/dot/html/pr2014/pr14-087.shtml); Barclays station $200K/yr (https://www.nytimes.com/2009/06/24/nyregion/24naming.html); NYC Ferry system naming rights **in market now**, value undisclosed (https://edc.nyc/press-release/nycedc-advances-search-first-ever-naming-rights-partner-nyc-ferry-system) | ❌ | **Upside only**: $200K/yr fleet placeholder (÷4 vessels), above Boston's $150K on precedent depth, still ~1 station-naming deal |
| U2 Overnight cargo | ✅ existence proven **in this exact harbor**: NYC Blue Highways pilot moves 300–400 parcels/day by ferry from Atlantic Basin (a network stop) to Pier 79 (a network stop) — no public rate (https://www.nyc.gov/html/dot/html/pr2025/nyc-blue-highways-freight-pilot.shtml). Priced at **courier-linehaul rates only**: Breakaway Manhattan rate card $26.50/job base, $21.15 4-hr economy (https://www.breakawaycourier.com/courier-delivery-rates); Dropoff 2026 medical benchmarks $30–160/job (https://www.dropoff.com/blog/medical-courier-service-rates/) | ❌ | **Upside only, $350/run × 16 nights/mo** (canon contract placeholder from Boston, benchmark-anchored). Natural NY clean class: **medical/lab specimens** — the NY-M trunk directly links E 90th/E 34th (hub.json tags both as medical-corridor stops) with downtown; batch parcels second (Blue Highways precedent). Seafood remains rejected (cabin-fit ruling, `../boston/CARGO-LAYER-BENCHMARKS.md`) |

## 5 · Worked per-vessel model (N45, New York)

Fixed inputs: $2.5M capex · 20 seats · energy 4.1 kWh/nm × $0.30 = $1.23/nm (canon) · Navier network share 10% of gross (canon) · maintenance $82.5K/yr → $6,875/mo (canon midpoint, unvalidated range) · insurance+berth $7.7K/mo (placeholder carried from Boston — **not NY-sourced**; NY berthing likely higher, flagged) · crew **$130/hr** 2-person loaded (2026-drifted BLS metro mean, `CREW-COST-NEW-YORK.md`) · 22 weekdays + up to 8 weekend days · commute 8 legs/day = 5 parity legs × 6 nm + 3 gap legs × 14 nm = 72 nm/day (hub.json geometry).

Quantity × price lines sum exactly to gross:

| | Conservative | Mid | Upside |
|---|---|---|---|
| L1 committed seats (blend, §3) | 24 seats → **$16,400** | 32 seats → **$23,900** | 36 seats → **$29,100** |
| L2 spot: residual seat-legs × fill × fare | 2,464 × 10% = 246 × $30 = **$7,380** | 2,112 × 20% = 422 × $38 = **$16,036** | 1,936 × 30% = 581 × $45 = **$26,145** |
| L3 experiences (sailings × pax × price) | 10 × 10 × $59 = **$5,900** | 28 × 13 × $69 = **$25,116** | 40 × 15 × $79 = **$47,400** |
| L3 charters (charters × hrs × rate) | 3 × 2.0 × $600 = **$3,600** | 6 × 2.25 × $700 = **$9,450** | 10 × 2.5 × $800 = **$20,000** |
| U1 sponsorship ($200K/yr fleet ÷ 4 ÷ 12) | $0 | $0 | **$4,167** |
| U2 overnight cargo (16 runs × $350) | $0 | $0 | **$5,600** |
| **Gross revenue /mo** | **$33,280** | **$74,502** | **$132,412** |
| Opex: crew (hrs × $130) | 160 h → $20,800 | 206 h → $26,780 | 277 h → $36,010 |
| Opex: energy (nm × $1.23) | 1,764 nm → $2,170 | 2,055 nm → $2,528 | 2,506 nm → $3,082 |
| Opex: maintenance · insurance+berth | $6,875 · $7,700 | $6,875 · $7,700 | $6,875 · $7,700 |
| **Opex /mo total** | **$37,545** | **$43,883** | **$53,667** |
| **Net to investor /mo** (gross × 0.90 − opex) | **−$7,593** | **+$23,169** | **+$65,504** |
| **Annual** | −$91.1K | **+$278.0K** | +$786.0K |
| **Payback on $2.5M** | never (negative) | **~9.0 yr** | **~3.2 yr** |

*Quantity notes:* residual seat-legs = 3,520 capacity (8 legs × 20 seats × 22 days) − committed usage (seats × 2 legs × 22 days); trips rounded to whole numbers. Crew hours = 6.0 h/day commute block × 22 + 2.0 h/experience sailing + charter hrs × 1.3 positioning + 2.0 h/cargo run, rounded. Energy nm = commute 1,584 + experiences at 12 nm/sailing + charters at 10 nm/hr + cargo at 12 nm/run.

**Honest reads:**
- **NY mid (~9.0 yr) does not match Boston mid (~4.3 yr), and the model says why:** blended L1 at $747 is 68% of Boston's $1,100, and crew at $130/hr is 153% of Boston's $85. Same physics, different city inputs — presenting anything better would require breaking the locked seat canon or the sourced crew basis.
- **The two honest levers, shown as sensitivities (not blended into the headline):**
  1. **Crew at posted NYC ferry wages.** The Hornblower captain posting + NY Waterway deckhand aggregate imply ~$73.49/hr loaded (`CREW-COST-NEW-YORK.md` posting check). At $75/hr, mid opex falls to $32,553 and mid net rises to **+$34,499/mo → ~6.0-yr payback**. Labeled: posting-anchored, not a standardized series.
  2. **Gap-weighted deployment.** A vessel assigned fully to gap corridors (L1 all at $825 mid) lifts mid gross to $77,002 and net to **+$25,419/mo → ~8.2 yr**; both levers together → **~5.7 yr**. Gap corridors are where NY demand has no water alternative — fleet sequencing should start there.
- **Upside (~3.2 yr) is credible on NY market depth** — 40 experience sailings/mo is ~1.3/day in the US's largest experience market, and both upside lines (sponsorship, cargo) have live NYC precedents (naming-rights sale in market; Blue Highways pilot on our own stops).
- Conservative is deliberately punitive and lands negative: it prices a premium product against a subsidized $4.50 incumbent at 10% spot fill and ⅓-of-one-daily-sailing L3 cadence. The stack cannot rescue canon-priced NY seats at punitive fills — the launch trigger (60–80 committed seats before capital deploys) is what protects the investor from this case.
- The seasonal NY-S East End line (approved Quanta LR corridor, $625/$645 legs per hub.json) is **not modeled here** — different vessel class and season; upside for a later pass.

## 6 · Cascade notes (for the NY fleet-investors JSON / microsite)

1. Headline = mid case with both sensitivities shown as labeled rows; conservative shown; upside labeled. No point-estimate promises.
2. All L3 lines carry "market-priced (NYC operators cited); not yet operated by Navier."
3. Sponsorship confined to upside with NYC precedent citations; cargo carries no number on the microsite (qualitative only, per D6′ rule 4) — the $350/run line is internal.
4. CT-corridor copy must pass `ny_c_honesty` (comfort/direct-to-waterfront vs Metro-North; no raw-speed claims) and the banned-term scan.
5. NY Waterway pass prices used only with their Nov 2014 effective-date flag until a current fare pull is verified.

## 7 · Assumption register

| Assumption | Value | Basis | Confidence |
|---|---|---|---|
| L1 fills 24/32/36 of 40 max | scenario | trigger = 60–80 seats/corridor ≈ 1.5–2 vessel-loads (canon) | Derived |
| L1 prices $650–900 by corridor type | canon | hub.json `locked_numbers` (Jaideep 2026-08-15) | Canon |
| Parity/gap blend 62.5/37.5 | scenario | 5-of-8 legs on parity trunk per modeled day; hub.json geometry | Derived |
| Spot fares $30/$38/$45; fill 10/20/30% | scenario | bounded SeaStreak $30 ↔ Uber $71–96; fills unproven, labeled | Placeholder (bounds sourced) |
| Experience sailings 10/28/40 × 10–15 pax × $59–79 | scenario × benchmark | CHL $52–114, Circle Line $29–54; conservative ≈ ⅓ of one daily sailing | Benchmark-bounded |
| Charters 3/6/10 per mo, $600–800/hr | benchmark | Sailo ~$600+/hr motor yachts; Boatsetter from $800 | Sourced (marketplace) |
| Sponsorship $200K/yr fleet | placeholder | Barclays $200K/yr station (NYC); Citi Bike scale above; NYC Ferry sale value undisclosed | Weak — upside only |
| Cargo $350/run × 16 nights | canon placeholder | Boston ruling + Breakaway/Dropoff rates + Blue Highways existence (no public rate) | Benchmark-anchored, unproven |
| Crew $130/hr | benchmark-validated | BLS OEWS NY metro means × 1.4294 ECEC, +3%/yr to 2026, rounded up | Validated at rate level; posting check suggests high bias |
| Insurance+berth $7.7K/mo | placeholder | carried from Boston, not NY-sourced | Weak — replace with NY quotes |
| Maintenance $6,875/mo | canon midpoint | $65–100K/yr N45 range, unvalidated | Placeholder |
| Energy/positioning distances | derived | hub.json segment nm; 12 nm/experience, 10 nm/charter-hr, 12 nm/cargo run assumed | Derived (stated) |

---
*All prices captured from live pages 2026-08-16 unless a different effective date is stated (NY Waterway: Nov 2014, flagged). No invented economics; sponsorship and cargo fail closed out of the base case.*
