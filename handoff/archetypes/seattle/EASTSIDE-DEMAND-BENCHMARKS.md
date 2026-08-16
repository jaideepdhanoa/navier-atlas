# Eastside (Lake Washington) Demand Benchmarks — LKW-1 / LKW-2

**Date:** 2026-08-16 · **Status:** sourced benchmarks pass for the reopened lake corridors (LKW-1 Cross-Lake Leschi ↔ Meydenbauer; LKW-2 Eastside Kirkland · Carillon · Meydenbauer · Renton/Coulon)
**Companion files:** `hub.json` (stop geometry, corridor defs), `REVENUE-STACK-SEATTLE.md` (economics — lake corridors remain fail-closed there), `EASTSIDE-VERIFICATION-2026-08-16.md` (speed rules), `SPEED-RULES-SEATTLE.md`
**Rules applied:** every figure carries source + URL + year (register in §5). UNSOURCED items are labeled and excluded from recommended use. Landing-walk classifications marked *(est.)* are map-geometry estimates against hub.json stop coordinates, not sourced figures — ops-verify before external use. Employer names are **indicative of demand potential, not commitments or commercial relationships** wherever rendered.

---

## 1 · Employer pool — Eastside waterfront-reachable

| Employer | Headcount (figure · year) | Source [#] | Nearest lake landing | Landing classification (honest) |
|---|---|---|---|---|
| **Amazon — Bellevue** | **17,500** expected by end-2024; publicized plan **25,000** in Bellevue [1]; company states ">15,000, city's largest employer" [2] | PSBJ 2024 [1]; Amazon [2]; Seattle Times 2026 confirms 25K plan intact [3] | Meydenbauer Bay (Bellevue Marina) | **Shuttle-tier / longer walk** — downtown towers ~0.8–1.0 mi uphill from the dock, 15–20 min *(est., consistent with hub.json)* |
| **Microsoft — Redmond HQ** | **>52,000** in Redmond, 2025 [4]; Redmond.gov cites >47,000 on campus [5] | PSBJ 2026 [4]; City of Redmond [5] | Carillon Point (Kirkland S) | **Shuttle-tier only** — campus is ~4 mi inland from Carillon Point *(est.)*; no Microsoft water dock. No sourced Kirkland/Bellevue-waterfront Microsoft office found. |
| **Boeing — Renton 737 plant** | **~12,000** Renton workforce (2019, latest sourced site figure) [6]; 2026: hiring 100–140 factory workers/week region-wide [7] | Seattle Times 2019 [6]; Reuters 2026 [7] | Gene Coulon / Southport | **Walk-tier** — plant abuts the south lake shore next to Renton Municipal Airport; Coulon dock is adjacent *(est., consistent with hub.json)*. Figure is pre-2020; treat as order-of-magnitude. |
| **Google — Kirkland** | **5,076** Kirkland employees (2025 city data); grew 47% from 3,449 in 2024; majority of ~8,000 regional workforce [8][9] | PSBJ 2026 [8][9] | Kirkland Marina Park | **Split:** Kirkland Urban is ~0.5 mi / ~10 min from Marina Park — **walk-tier borderline** *(est.)*; the original 6th St S campus is ~1 mi — **shuttle-tier** *(est.)*. hub.json currently classifies Google Kirkland as shuttle-tier (~0.9 mi); keep shuttle-tier as the rendered default, walk-tier upside for Kirkland Urban only. |
| **T-Mobile — HQ (Factoria/Eastgate/BelRed)** | **>6,200** at Bellevue sites | City of Bellevue / T-Mobile press [10][11] (2023–24) | Meydenbauer Bay (nearest) | **Shuttle-tier at best** — Factoria campus ~3 mi from the Meydenbauer dock *(est.)*; no walk service. |
| **Meta — Bellevue (Spring District)** | Region headcount shrunk to **~5,600** after layoffs [12]; Spring District-specific headcount **UNSOURCED** (developer cites 10,000+ *capacity*, not staff [13]); Meta ended Bellevue expansion, subleasing space [12] | Seattle Times [12]; Seneca Group [13] | Meydenbauer Bay (nearest) | **Shuttle-tier / too-far** — Spring District ~2 mi east of the dock *(est.)*, and the 2 Line now serves Spring District/120th directly [16]. **Do not render as an anchor** (downsizing + rail-served). |
| **Downtown Bellevue — total office workforce** | **>60,000 employees**; jobs base +25% since 2015 | Bellevue Downtown Association [14] (page current 2026) | Meydenbauer Bay | Shuttle-tier/longer-walk as above; this is the aggregate pool behind the Amazon line. |
| Valve (Bellevue) | **UNSOURCED** — no reliable public headcount found this pass | — | — | Excluded from use |
| The Pokémon Company Intl (Bellevue) | **UNSOURCED headcount** — confirmed Bellevue HQ, taking 16 floors at a new Bellevue tower (2024) [15], but no employee figure | The Real Deal 2024 [15] | Meydenbauer (shuttle-tier, downtown core) | Name renderable as a downtown-Bellevue tenant only; no number |
| Snowflake (Bellevue) | **UNSOURCED headcount** — Bellevue office confirmed via careers site only | snowflake careers [22] | — | Excluded from numeric use |
| Smartsheet (Bellevue HQ) | Company total "over 3,000 employees," HQ Bellevue [21]; **Bellevue-site headcount UNSOURCED** | Smartsheet [21] | Meydenbauer (shuttle-tier, downtown core) | Name renderable; no site number |

**Sourced walk-tier demand on the lake is thin and concentrated at Renton (Boeing).** Everything in downtown Bellevue is real but sits behind a 15–20 min uphill walk or a shuttle from Meydenbauer. This matches hub.json's honest tiering and must not be softened in partner copy.

## 2 · Commute pain (the demand driver)

| Metric | Figure | Source [#] |
|---|---|---|
| SR-520 floating bridge volume | **66,260 vehicles per average weekday (2025)**; AADT 57,913 (2023); pre-COVID weekday avg 74,912 (2018) | Wikipedia/Evergreen Point, citing WSDOT [17] — secondary; primary home is WSDOT SR 520 T&R Study 2025 [18] |
| I-90 floating bridge volume | **~133,000 vehicles per average weekday** (WSDOT IRT background — page undated, treat as dated) [19]; City of Mercer Island posts EB 69,900 + WB 72,800 + reversible 15,200 ≈ **157,900/day** (year not stated) [20] | WSDOT [19]; Mercer Island [20] — both flagged for vintage; do not quote without the caveat |
| SR-520 peak drive time, Seattle↔Eastside | WSDOT corridor dashboard: peak-period commute averaged **31 min** with a **reliable (planning) time of 51 min** — the 51-min planning figure already anchors hub.json copy | WSDOT Multimodal Mobility Dashboard [23] |
| SR-520 toll, 2-axle weekday peak (7–10a, 3–7p) | **$4.90 Good To Go! / $6.90 Pay By Mail / $5.15 Pay By Plate** (schedule effective 2024-08-15; matches hub.json's "$4.90–$6.90") | WSTC [24] (2024, current) |
| Sound Transit 2 Line (East Link) | Full cross-lake line **opened March 28, 2026**: 10 stations Seattle (Judkins Park) → Mercer Island → S Bellevue → East Main → **Bellevue Downtown** → Wilburton → **Spring District** → BelRed → Overlake → Redmond Tech (+ downtown Redmond, opened May 2025). **No Kirkland station. No Renton station.** S Kirkland–Issaquah is an unbuilt ST3 project. | Sound Transit [16]; Seattle Transit Blog 2026 [25]; City of Bellevue [26] |
| Kirkland ↔ Seattle transit | Route 255 terminates at UW Link (transfer required); ~**45 min** Kirkland TC → downtown per Uber's transit note [27]; route running 57–60 min end-to-end vs 47 min historically [28] | Uber route page 2025 [27]; Seattle Transit Blog 2025 [28] |
| Renton ↔ Seattle transit | Metro 101/102, ~**30–46 min** Renton TC → downtown (46 min per Transit app; ~45 min per Uber's note) | Transit app [29]; Uber route page [30] |

**Read:** the 2 Line now directly serves downtown Bellevue and the Spring District from Seattle — it is a real competitor on the Seattle↔downtown-Bellevue pair. **Kirkland and Renton got no rail** and keep transfer-laden 45–60 min transit; those are the corridors where the water's time claim does structural work.

## 3 · Substitutes / pricing

- **There is no scheduled passenger water service on Lake Washington today — none.** The lake's last ferry, *Leschi* (Madison Park ↔ Kirkland), made its final run **August 31, 1950** [31][32]. Confirmed plainly; 75 years without service.
- **Uber (published route-page averages, past-month, page updated April 2025):**
  - Bellevue → Seattle: avg **$48 / 24 min / 11 mi**; UberX $50, Comfort $59, **Black $90**, Electric $35 [33]
  - Kirkland → Seattle: avg **$57 / 27 min / 14 mi** [27]
  - These bound a door-to-door ceiling of roughly **$2,100–2,500/mo** at 44 legs/mo (UberX) — same logic as the Sound-side derivation in REVENUE-STACK-SEATTLE §3.
- **SR-520 toll as a daily-driver floor:** $9.80/day round-trip peak (2× $4.90 GTG) ≈ **~$215/mo** in tolls alone before parking [24].
- Downtown Seattle monthly parking ~$220/mo already benchmarked in REVENUE-STACK-SEATTLE §2 (SpotHero). Downtown **Bellevue** parking: **UNSOURCED this pass** — excluded.
- No premium bus/shuttle substitute on Kirkland/Renton↔Seattle was sourced beyond Uber's generic "private bus ~$10" note (too vague to use — excluded).

## 4 · Recommendation

**Strongest sourced demand case: LKW-2's endpoints, then LKW-1.**
1. **Renton/Coulon (LKW-2 south)** has the lake's only sourced *walk-tier* employer mass: Boeing's ~12,000-person plant on the shore, no rail, 30–46 min transit. Cleanest single-employer anchor story on the lake.
2. **Kirkland (LKW-2 north)** pairs Google's 5,076 (growing 47%/yr, second-largest city employer) with a dock-adjacent downtown and no rail; Kirkland Urban is arguably walk-tier from Marina Park.
3. **Meydenbauer (LKW-1 / LKW-2 hub)** has the largest gross pool (Amazon 17,500→25,000; downtown Bellevue >60,000) but it is shuttle-tier from the dock, and the 2 Line (open 2026) now competes directly on Seattle↔downtown Bellevue. LKW-1's honest framing is lakefront-residential Leschi ↔ Bellevue jobs, 12–15 min indicative vs 51-min SR-520 planning time + $9.80/day tolls — not "faster than the train for everyone."

**Conservative committed-seat ranges (planning, not demand claims — launch gate stays 60–80 committed seats/corridor):**
- **LKW-1 Cross-Lake:** model **20–32 committed seats** conservative (1.0–1.6 N45 loads), consistent with the 24/32/36 L1 fill scenarios in REVENUE-STACK-SEATTLE. Reaching the 60–80 gate plausibly requires 2–3 employer LOIs at Meydenbauer plus Leschi-side residential/employer sign-ups; label all of it derived.
- **LKW-2 Eastside:** model **20–28 committed seats** conservative across the Kirkland–Meydenbauer–Renton spine (Boeing + Google are the anchors; Microsoft only via Carillon shuttle). The 60–80 gate likely needs Boeing or Google at anchor scale — say so plainly in any partner material.
- No lake-corridor revenue enters the P&L until these convert to LOIs (scope amendment in REVENUE-STACK-SEATTLE stands — fail closed).

**Safe to render as indicative demand pools** (always with the label "indicative of demand potential, not commitments or commercial relationships"): **Amazon (Bellevue), Boeing (Renton), Google (Kirkland), Microsoft (Redmond — shuttle-tier via Carillon Point, never walk), T-Mobile (Factoria — shuttle-tier)**. Renderable as names only, no numbers: Pokémon Company Intl, Smartsheet. **Do not render:** Meta (region downsizing, rail-served Spring District), Valve/Snowflake (unsourced).

## 5 · Source register

1. Puget Sound Business Journal — "Amazon expects to reach 17,500 employees in Bellevue" (2024) — https://www.bizjournals.com/seattle/news/2024/11/06/amazon-bellevue-employees-headcount.html
2. Amazon — "Amazon's impact in Seattle, Bellevue, and the Puget Sound" (accessed 2026) — https://www.aboutamazon.com/news/community/amazon-seattle-bellevue-puget-sound-news
3. Seattle Times — "Amazon added thousands to its Bellevue offices last year" (2026) — https://www.seattletimes.com/business/amazon-added-thousands-to-its-bellevue-offices-last-year/
4. Puget Sound Business Journal — "Microsoft, Amazon employee counts surge in Redmond" (2026; >52,000 in Redmond in 2025) — https://www.bizjournals.com/seattle/news/2026/01/22/microsoft-amazon-headcounts-in-redmond-grow.html
5. City of Redmond — "Microsoft Redmond Campus Refresh" (>47,000 on campus; 2018–2025 project page) — https://www.redmond.gov/386/Microsoft-Redmond-Campus-Refresh
6. Seattle Times — "Boeing will halt Renton assembly lines… no layoffs for the 12,000-strong Renton workforce" (2019) — https://www.seattletimes.com/business/boeing-aerospace/boeing-will-halt-renton-assembly-lines-but-no-layoffs-for-employees/
7. Reuters — "Boeing hiring more than 100 factory workers a week" (2026) — https://www.reuters.com/world/boeing-hiring-more-than-100-factory-workers-week-grow-output-replace-retirees-2026-04-16/
8. Puget Sound Business Journal — "Google's employee count in Kirkland takes big jump" (2026; 5,076 in 2025, city data) — https://www.bizjournals.com/seattle/news/2026/06/30/googles-alphabet-headcount-kirkland-increase.html
9. Puget Sound Business Journal — "Google grows Seattle-area workforce as Kirkland Urban plans remain on hold" (2026) — https://www.bizjournals.com/seattle/news/2026/07/30/google-workforce-kirkland-urban.html
10. City of Bellevue — "City congratulates T-Mobile on major campus renovation" (>6,200 at Bellevue sites) — https://bellevuewa.gov/city-news/city-congratulates-t-mobile-major-campus-renovation
11. T-Mobile — "5 Cool Things Coming to All-New T-Mobile HQ in Bellevue" (HQ campus >6,200) — https://www.t-mobile.com/news/press/new-hq-remodel
12. Seattle Times — "Meta plans to offer more Bellevue office space for sublease" (region headcount ~5,600) — https://www.seattletimes.com/business/technology/meta-plans-to-offer-more-bellevue-office-space-for-sublease/
13. Seneca Group — "Meta Spring District Campus" (capacity claim only, developer source) — https://senecagroup.com/project/meta-spring-district-campus/
14. Bellevue Downtown Association — "About Downtown" (>60,000 employees; +25% since 2015; accessed 2026) — https://www.bellevuedowntown.com/discover/downtown
15. The Real Deal — "Pokémon to exit Lincoln Square with move to Bellevue" (2024) — https://therealdeal.com/national/seattle/2024/04/09/pokemon-to-exit-lincoln-square-with-move-to-bellevue/
16. Sound Transit — "East Link Extension: project map and summary" (10 stations, station list) — https://www.soundtransit.org/system-expansion/east-link-extension
17. Wikipedia — "Evergreen Point Floating Bridge" (66,260 weekday avg 2025; AADT 57,913 in 2023; 74,912 in 2018 — cites WSDOT; secondary) — https://en.wikipedia.org/wiki/Evergreen_Point_Floating_Bridge
18. WSDOT — SR 520 Bridge Traffic and Revenue Study Update (2025, Stantec; primary volume source) — https://wsdot.wa.gov/sites/default/files/2025-11/Toll-SR520Bridge-TrafficRevenue-Study2025.pdf
19. WSDOT — I-90 Independent Review Team background (~133,000 vpd; page undated) — https://www.wsdot.wa.gov/partners/irt/background.htm
20. City of Mercer Island — "Interstate-90 Issues" (EB 69,900 / WB 72,800 / reversible 15,200; year not stated) — https://www.mercerisland.gov/community/page/interstate-90-issues
21. Smartsheet — "About Smartsheet" (HQ Bellevue; >3,000 employees; accessed 2026) — https://www.smartsheet.com/about
22. Snowflake — Bellevue careers page (office existence only) — https://careers.snowflake.com/us/en/bellevue
23. WSDOT — Multimodal Mobility Dashboard, Central Puget Sound SR 520 commute times (peak avg 31 min; reliable 51 min) — https://wsdot.wa.gov/about/data/multimodal-mobility-dashboard/dashboard/central-puget-sound/stateroute520-cps/commute-time.htm
24. Washington State Transportation Commission — SR 520 Bridge toll rates (effective 2024-08-15; peak 2-axle $4.90 GTG / $6.90 PBM) — https://wstc.wa.gov/programs/tolling/sr-520-bridge/
25. Seattle Transit Blog — "Full East Link Extension will open March 28" (2026) — https://seattletransitblog.com/2026/01/23/full-east-link-extension-will-open-march-28/
26. City of Bellevue — "East Link Light Rail" (station list) — https://bellevuewa.gov/city-government/departments/transportation/projects/east-link-light-rail
27. Uber — Kirkland, WA → Seattle, WA route page (avg $57 / 27 min / 14 mi; transit note ~45 min; updated April 2025) — https://www.uber.com/global/en/r/routes/kirkland-wa-to-seattle-wa/
28. Seattle Transit Blog — "Route 255 to Downtown Seattle" (2025; 57–60 min vs 47 min) — https://seattletransitblog.com/2025/06/28/route-255-to-downtown-seattle/
29. Transit app — Metro 101 Renton TC–Seattle (~46 min) — https://transitapp.com/en/region/seattle/metro-transit/bus-101
30. Uber — Renton, WA → Seattle, WA route page (transit note: 101/102 ~45 min) — https://www.uber.com/global/en/r/routes/renton-wa-to-seattle-wa/
31. Wikipedia — "Lake Washington steamboats and ferries" (Leschi last run 1950) — https://en.wikipedia.org/wiki/Lake_Washington_steamboats_and_ferries
32. Kirkland Heritage Society — "Kirkland Ferries" (Leschi final run Aug 31, 1950) — https://kirklandheritage.org/ferries/
33. Uber — Bellevue, WA → Seattle, WA route page (avg $48 / 24 min / 11 mi; UberX $50, Black $90; updated April 2025) — https://www.uber.com/global/en/r/routes/bellevue-wa-to-seattle-wa/

---
*UNSOURCED and excluded from recommended use: Valve headcount; Pokémon Bellevue headcount; Snowflake Bellevue headcount; Smartsheet Bellevue-site headcount; Meta Spring District-specific headcount; downtown Bellevue parking rates. Dock-walk distances marked (est.) are map-geometry estimates pending ops verification. No lake-corridor figure here enters the fleet P&L until LOI-backed (fail closed).*
