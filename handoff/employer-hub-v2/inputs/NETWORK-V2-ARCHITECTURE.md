# Employer Water Networks v2 — Metro-Style Network Architecture
**Bay Area · New York / CT / Long Island / Hamptons**
Drafted 2026-08-13 · INTERNAL PLANNING — dock/landing status notes must never appear in employer-facing material (standing 2026-08-11 ruling). Employer materials show stations and lines only.

Node basis: `BAY-NODE-INVENTORY.md` and `NY-NODE-INVENTORY.md` (same folder) — every node is a real, source-verified landing. No invented piers.

---

## 1 · Design principles

1. **Sell nodes, not routes.** A route sells one origin; a station on a connected network sells every origin on the system. The employer metric changes from "is there a boat from X" to **"% of workforce living within reach of a station."**
2. **Three-layer structure** (metro logic):
   - **Trunk lines** — high-frequency, all-day spines on the deepest demand. 2–3 vessels for credible headways.
   - **Feeder lines** — residential nodes joining a trunk at an interchange. One vessel can serve 3–4 feeder nodes per peak.
   - **Seasonal overlays** — Hamptons/East End; shares eastern nodes with year-round lines.
3. **Interchanges make the network.** A transfer at a hub is how a node reaches every employer dock without a dedicated boat. Timed transfers at ≤10 min.
4. **Phasing stays honest.** Phase 1 = corridors with committed-seat triggers (~60–72 seats) and existing usable landings. Phase 2/3 = network build-out contingent on landings/demand. Maps must show phases distinctly — never imply day-one full coverage.
5. **Node status is coded internally** (never externally):
   - ● ACTIVE — existing terminal with scheduled service today
   - ◐ DOCK — real landing exists (marina/town dock/private terminal); commercial access = internal dock track
   - ○ BUILD — planned/under construction/built-but-unused; timing from source
6. **Fail closed on times/economics.** Distances/times below are indicative planning bands @ 20 kn service speed; seal in Atlas geometry before any external use. New corridors get economics only after the four-input rule.

---

## 2 · BAY AREA

### 2.1 Node roster (21 verified; status-coded)

**Hubs/interchanges:** SF Ferry Building ● (primary) · Oakland Jack London Sq ● (East Bay hub) · Oyster Point ● (Peninsula hub) · **Mission Bay ● (full interchange — Jaideep 2026-08-13: service launches end-2027 at earliest; Port construction completes 2026/27, so Mission Bay is a day-one hub, not a future node.** ~11,000 housing units within ½ mi + UCSF/Chase Center)

**Residential nodes:** Larkspur ● · Sausalito ● · Tiburon ● · Vallejo ● · Mare Island ● (select) · Richmond ● · Alameda Main St ● · Alameda Seaplane Lagoon ● · Alameda Harbor Bay ● · Treasure Island ● (private operator today) · Berkeley Marina ◐ (WETA terminal in design — separate site) · Emeryville/Emery Cove ◐ · Coyote Point (San Mateo) ◐

**Employer-side nodes:** Oyster Point ● (Genentech/SSF biotech) · Redwood City Port marina ◐ (Peninsula tech corridor) · Mission Bay ○ (UCSF/biotech) · Pier 41 ● (Wharf hospitality) · Oracle Park ● (event)

**No landing exists (do not map):** Palo Alto/EPA, Foster City, Burlingame, Fremont/Newark, San Rafael, Martinez, Benicia, Antioch, Pier 70/Crane Cove.

*Marina gap-check (2026-08-13, sourced — `MARINA-GAP-CHECK.md`):* Palo Alto's harbor closed 1986 (silted; only a low-tide-limited sailing station remains). Foster City's lagoon has no navigable Bay connection. Fremont's only ramp (Newark Slough) is high-tide refuge access. None can berth a 30–45 ft commercial passenger vessel — the "no landing" verdicts hold; these markets need new dock infrastructure before they can ever be stations.

### 2.2 Line design

| Line | Working name | Stations (west→east / north→south) | Layer | Phase |
|---|---|---|---|---|
| **BA-1** | Peninsula Trunk | Ferry Building ● → Mission Bay ● → Oyster Point ● → Redwood City ◐ | Trunk | P1 (FB↔Mission Bay↔OP — Mission Bay is day-one: Port construction completes 2026/27, service launches end-2027) · P2 (Redwood City on dock) |
| **BA-2** | Marin Line | Larkspur ● / Sausalito ● / Tiburon ● → Ferry Building ● → through-run to Oyster Point ● | Trunk (peak through-running) | P1 — the Stripe-relaunch line (old Line A) |
| **BA-3** | East Bay Trunk | Oakland JLS ● / Alameda Seaplane ● / Alameda Main ● → Ferry Building ● | Trunk | P1 |
| **BA-4** | Biotech Crosstown | Alameda Harbor Bay ● / Alameda Seaplane ● / Oakland JLS ● → Oyster Point ● (direct, bypassing SF) | Crosstown trunk | **P2 flagship** — East Bay→Peninsula biotech commute has zero water option today; no backtrack through FB |
| **BA-5** | North Bay Express | Vallejo ● / Mare Island ● / Richmond ● → Ferry Building ● (premium express overlay on WETA-served pairs) | Feeder/express | P2–P3 |
| **BA-6** | Inner East Bay Feeder | Berkeley ◐ / Emeryville ◐ / Treasure Island ● → Ferry Building ● or Oakland JLS ● | Feeder | P2–P3 (dock track: Berkeley, Emeryville) |

**Interchange logic:** Ferry Building = primary (all trunks meet). Oakland JLS = East Bay collector (BA-5/6 feeders meet BA-3/BA-4). Oyster Point = Peninsula anchor (BA-1, BA-2 through-runs, BA-4 all terminate/call).

**Indicative times @ 20 kn (seal in Atlas before external use):** Larkspur→FB ~30 min · FB→Oyster Point ~25 min · Oyster Point→Redwood City ~40 min · Harbor Bay→Oyster Point ~30 min · Oakland→FB ~20 min · Vallejo→FB ~55 min (25 kn N30 express ~45 min).

### 2.3 Employer catchment (the new pitch table)

| Employer anchor | Direct-line nodes (no transfer) | +1 transfer nodes | Phase-1 reachable stations | Full-network stations |
|---|---|---|---|---|
| **Oyster Point / SSF biotech** (Genentech et al.) | FB, Mission Bay●, Redwood City◐, Larkspur, Sausalito, Tiburon (BA-2 through), Harbor Bay/Seaplane/Oakland (BA-4) | Richmond, Vallejo, Berkeley◐, Emeryville◐, Treasure Island, Alameda Main (via FB/JLS) | **7** | **15** |
| **Mission Bay / UCSF cluster** ● (day-one hub — opens before end-2027 launch) | FB, Oyster Point, Redwood City◐ + BA-3 East Bay through-calls | Marin trio, Richmond, Vallejo, TI, Berkeley◐, Emeryville◐ | **5** | 14 |
| **Financial District (FB)** | Everything on BA-1/2/3/5/6 | BA-4 nodes | 9 | 16 |
| **Redwood City / Peninsula tech** ◐ | FB, Mission Bay○, Oyster Point | East Bay + Marin via interchanges | — (P2, dock) | 14 |

**The headline for employer decks:** an Oyster Point employer goes from *"one shuttle from Larkspur"* to *"6 stations at launch, 15 at full network"* — coverage across Marin, SF, East Bay, and Peninsula residential clusters.

### 2.4 What's genuinely new vs. current plan
- BA-4 Biotech Crosstown (East Bay→SSF direct) — largest unserved flow, no current water option, strong N45 case.
- Treasure Island promoted to feeder node (active landing, private operator today — partner/replace conversation).
- Mission Bay timed to Port construction (2026/27) — **promoted to full day-one interchange (Jaideep 2026-08-13):** service launches end-2027 at earliest, after construction completes. Map it as a solid hub with an "opens 2027" tag, not dashed/aspirational.
- Berkeley/Emeryville/Coyote Point/Redwood City = the Bay dock track's priority list, in that order of demand value.

---

## 3 · NEW YORK / CT / LONG ISLAND / HAMPTONS — one connected system

### 3.1 Node roster (58 verified; keys only)

**Hubs/interchanges:** Pier 11 ● (primary) · E 34th St ● (Midtown/medical) · Brookfield Place/BPC ● + W 39th/Pier 79 ● (west side pair) · Paulus Hook ● (NJ collector)

**Manhattan spine:** E 90th ● · E 34th ● · Skyport Marina (E 23rd) ◐ · Pier 11 ● · BPC ● · W 39th ● · St. George ●

**Brooklyn/Queens:** DUMBO ● · BBP Pier 6 ● · Navy Yard ● (controlled campus access) · Red Hook ● · Greenpoint ● · N/S Williamsburg ● (**held** per standing rule — not in employer materials) · LIC Gantry ● · Hunters Point South ● · Astoria ● · Roosevelt Island ● · Soundview ● · Throgs Neck ●

**NJ Gold Coast:** Paulus Hook ● · Liberty Harbor ● · Port Liberté ● (private) · Hoboken NJT ● · Hoboken 14th ● · Lincoln Harbor ● · Port Imperial ● · Edgewater ● · (Monmouth: Atlantic Highlands/Highlands/Belford ● — Seastreak incumbent market, treat as partner/adjacent lane, not day-one target)

**Connecticut:** Greenwich Arch St ◐ (real town-owned ferry dock; seasonal island service today) · Stamford Harbor Point ◐ · Norwalk (Cove + SoNo) ◐ · Bridgeport ● (cross-Sound) · New Haven ◐

**Long Island North Shore:** Glen Cove ○ (**built terminal, no service — highest-value dormant asset in the region**) · Port Washington ◐ · Oyster Bay ◐ · Huntington ◐ · Northport ◐ · Port Jefferson ● (cross-Sound)

**East End:** Sag Harbor ◐ · Greenport ● · Shelter Island N ● / S ● · Montauk ● (seasonal ops) · Bay Shore/Fire Island ● · Hampton Bays ◐ · Three Mile Harbor ◐

**No landing (do not map):** LGA waterside (Marine Air Terminal closed; World's Fair Marina closed) — flag: E 34th↔LGA corridor's LGA end needs its own dock solution, keep internal. Long Beach. Stapleton (use St. George).

### 3.2 Line design

| Line | Working name | Stations | Layer | Phase |
|---|---|---|---|---|
| **NY-M** | Manhattan Medical Spine | E 90th ● → E 34th ● → Pier 11 ● | Trunk | P1 (carries NY-1 UES Medical) |
| **NY-H** | Hudson Line | Edgewater ● → Port Imperial ● → Lincoln Harbor ● → Hoboken 14th ● → Hoboken NJT ● → Paulus Hook ● → BPC ● / W 39th ● / Pier 11 ● | Trunk | P1 (carries NY-2 Gold Coast + NY-3 Goldman; premium overlay on NY Waterway pairs) |
| **NY-B** | Brooklyn Line | Navy Yard ● → DUMBO ● → BBP Pier 6 ● → Red Hook ● → Pier 11 ● | Trunk | P1 (carries NY-4) |
| **NY-Q** | Queens Feeder | Astoria ● → Roosevelt Island ● → LIC Gantry ● → Hunters Point S ● → Greenpoint ● → E 34th ● | Feeder | P2 (Williamsburg stops stay held) |
| **NY-C** | Connecticut Express | Greenwich ◐ → Stamford ◐ → (opt. Norwalk ◐) → E 34th ● → Pier 11 ● | Premium express | **P2 flagship** — richest untapped commute; honest positioning: time-competitive vs. door-to-door drive+Metro-North for waterfront-origin riders; sell guaranteed seat + workspace, not raw speed |
| **NY-G** | Gold Coast (LI) Line | Glen Cove ○ → Port Washington ◐ → E 34th ● → Pier 11 ● | Premium express | **P2 flagship** — Glen Cove terminal already built; ~22 nm ≈ 60 min ≈ LIRR-competitive with zero infrastructure build |
| **NY-X** | Bronx/North Feeder | Throgs Neck ● → Soundview ● → E 90th ● → E 34th ● | Feeder | P3 |
| **NY-S** | Hamptons Seasonal Overlay | Pier 11 ● → Sag Harbor ◐ → Shelter Island ● / Greenport ● / Montauk ● (+ East End local shuttle loop) | Seasonal | P1 seasonal (Quanta LR corridors already approved: Pier 11↔Sag Harbor $625 · ↔Montauk $645) |

**Interchange logic:** Pier 11 = primary (M, H, B, C, G, S all call). E 34th = Midtown/medical hub (M, Q, C, G, X). Timed transfers make e.g. Glen Cove→FiDi or Greenwich→Hudson Yards one-transfer trips.

**Indicative times @ 20 kn (seal in Atlas):** E 90th→E 34th ~10 min · E 34th→Pier 11 ~10 min · Glen Cove→E 34th ~60 min · Greenwich→E 34th ~80 min (25 kn ~65 min) · Stamford→E 34th ~95 min (25 kn ~75 min) · Port Imperial→W 39th ~8 min · Navy Yard→Pier 11 ~12 min.
**Honesty flag:** NY-C raw times exceed Metro-North station-to-station; the case is door-to-door for waterfront-origin riders + productivity (seat, wifi, no transfer at GCT). Never claim raw speed advantage on NY-C.

### 3.3 Employer catchment

| Employer anchor | Direct-line nodes | +1 transfer | Phase-1 stations | Full-network stations |
|---|---|---|---|---|
| **UES Medical (E 90th/E 34th)** — NYP, MSK, Rockefeller, NYU Langone | Pier 11, E 90th↔E 34th + NY-Q five nodes + NY-C (Greenwich, Stamford) + NY-G (Glen Cove, Port Washington) | Hudson + Brooklyn lines via Pier 11 | **3** | **20+** |
| **FiDi / Goldman (Pier 11/BPC)** | Every trunk terminates here: NJ 8 nodes, Brooklyn 4, E-river spine, CT, LI | Queens feeder via E 34th | **13** | **25+** |
| **Hudson Yards / Manhattan West (W 39th)** | NJ Gold Coast 8 nodes | E-river/Brooklyn via Pier 11–BPC link | **8** | **20+** |
| **Brooklyn Navy Yard / DUMBO tech** | Pier 11 + Brooklyn line | Everything via Pier 11 | **5** | **20+** |

### 3.4 What's genuinely new vs. current plan
- The four NY-1…NY-4 corridors become **stations on three connected trunks** instead of four disconnected segments — same launch economics, network story.
- **NY-G Glen Cove:** built-but-dormant terminal = fastest new-geography win in the region; single-municipality counterparty (Glen Cove CDA).
- **NY-C Connecticut Express:** Greenwich Arch St dock is town-owned and real — the CT conversation starts with one town government, not a private marina patchwork. Stamford = Harbor Point developer conversation (BLT), aligned incentives (amenity for their towers).
- **Monmouth (Seastreak) treated as adjacent incumbent lane** — partner conversation, not competitive entry, consistent with Hornblower fold-in logic.
- LGA has **no usable public landing** — E 34th↔LGA corridor needs a dock solution on the LGA end; keep the corridor in exec-shuttle materials only with this internal flag.

---

## 4 · Pitch implications (both markets)

1. **New core slide per deck:** "The network" map (phased: solid = launch lines, dashed = build-out) + the catchment table for that employer's dock. Replaces single-corridor framing.
2. **LOI language shifts** from "join the [X] line" to "commit seats at your station" — seats are line-agnostic at the network level; corridors still light in trigger order (~60–72 seats).
3. **Anchor-tenant offer gains a network clause:** anchor underwrites a line, gets branding + priority across the network as it grows.
4. **All node/dock status coding stays internal.** Employer maps show stations only. Landings negotiation remains the separate Jaideep-led track.
5. Every new corridor still passes the four-input rule before economics appear anywhere.

## 5 · Next steps
1. Jaideep review of this architecture (line set, phasing, flagships BA-4 / NY-C / NY-G).
2. Seal geometry in Atlas for new corridors (BA-4, NY-C, NY-G, feeders) — then real times replace indicative bands.
3. Render phased network maps (Atlas gold system, text-free plates) for both microsites + decks — Grok spec after review.
4. Rebuild employer decks' corridor slides → network slide + catchment tables.
5. Dock-track priority list update (internal): Bay = Berkeley, Emeryville, Redwood City, Coyote Point; NY = Glen Cove CDA, Greenwich (town), Stamford Harbor Point/BLT, Skyport Marina.
