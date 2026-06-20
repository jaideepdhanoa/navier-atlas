# India Partner Normalization Batch — Rapido / Ola / Uber India / Noon next

Date: 2026-06-20  
Repo PR target: `tasklet/india-gcc-partner-spines-2026-06-20` / PR #58

## Executive posture

This batch continues the India + GCC proposal plan from the safe first spine. It does **not** treat the 97 accepted India routes as final sufficiency. It turns the next step into a deterministic handoff:

1. Normalize **Rapido India** and **Ola India** onto the shared India corridor spine.
2. Draft **Uber India** from the same four accepted India baseline markets, without shrinking the existing global Uber proposal.
3. Promote **Goa** from safe baseline to marquee/full tourism-market expansion.
4. Move Gujarat, Tamil Nadu/Chennai, Andhra/Vizag, and West Bengal/Kolkata-Haldia from passive candidates to active exact-bind lanes.
5. Keep **Lakshadweep** gated until grounded or explicitly green-lit.
6. Keep **Noon** queued as the next UAE/Gulf build using Careem-style platform economics.

## Baseline normalization result

Current Rapido/Ola India market anchors already resolve against the repo city-brief IDs:

| Partner | Market anchors checked | Result |
|---|---:|---|
| Rapido | Mumbai, Goa, Kerala, Andaman | OK — all anchors resolve |
| Ola | Mumbai, Goa, Kerala, Andaman | OK — all anchors resolve |
| Uber global file | India currently has Mumbai + Goa only | OK anchors, but India footprint is incomplete for the new India-focused pass |

Immediate consequence: Rapido/Ola can cascade on the accepted India spine first. Uber India needs a derivative/draft spec that adds Kerala + Andaman as accepted-baseline India markets, while leaving the global Uber page intact unless the user chooses to merge the derivative back into the global page.

## Source-led partner posture

| Partner | Source signal | Evidence tier | Proposal action |
|---|---|---|---|
| Rapido | Official Rapido site says India’s ride-hailing app, present across 400+ cities; services include bike taxi, auto, cab, parcel, travel, metro. | `country_supported` | Use 80:20 inheritance into existing Atlas India waterfront markets; no city over-precision required for safe baseline. |
| Ola | 2024 public reports confirm exit from UK, Australia, and New Zealand to focus on India. | `country_supported` / India-only for this pass | Keep India-only. Use same accepted India waterfront baseline as Rapido. |
| Uber India | Official Uber India cities page lists India service areas, including coastal/near-coastal states and entries overlapping the India lanes. | `city_supported` where listed, otherwise `country_supported` | Draft India-focused derivative with Mumbai, Goa, Kerala, Andaman first; then apply exact-bind expansion lanes. |
| Noon | UAE/Gulf platform build, not India. | `country_supported` UAE/GCC platform hypothesis pending local mechanics | Build after India normalization from Careem-style UAE/Gulf spine. |

Sources used:

- Rapido official site: `https://www.rapido.bike/`
- Uber India cities page: `https://www.uber.com/global/en/r/india/cities/`
- Ola exit / India focus public report: `https://www.reuters.com/world/india/indias-ola-stop-ride-hailing-operations-international-markets-2024-04-09/`
- Goa River Navigation Department ferry routes: `https://rnd.goa.gov.in/ferry-routes/`
- Adani Ports official ports and terminals page: `https://www.adaniports.com/ports-and-terminals`

## Partner-by-partner build spec

### 1. Rapido India

**Status:** already has four India markets in `partner-pitch/partners/rapido.json`:

- Mumbai / Maharashtra waterfront corridors
- Goa corridors
- Kerala / Kochi + backwaters
- Andaman Islands

**Do next:**

- Reconcile every featured route against `india-shared-corridor-spine.json`.
- Bind `route_id` where the route already exists in the spine.
- Leave `route_id: null` only where the route is narrative, intra-city-unbound, or needs new exact geometry.
- Run economics after the route reconciliation, not before.
- Promote Goa to marquee/full: see Goa section below.

**Do not:** broaden into Gujarat/Tamil Nadu/Andhra/West Bengal until those lanes have exact Atlas support.

### 2. Ola India

**Status:** already has four India markets in `partner-pitch/partners/ola.json`:

- Mumbai / Maharashtra waterfront corridors
- Goa corridors
- Kerala / Kochi + backwaters
- Andaman Islands

**Do next:**

- Keep India-only for this pass, reflecting the international exit/focus correction.
- Normalize to the same shared route spine as Rapido.
- Preserve Ola Electric / clean-mobility framing in narrative, but do not let brand narrative drive geography.
- Run the same economics cascade after exact route reconciliation.

### 3. Uber India

**Status:** the existing global `partner-pitch/partners/uber.json` has an India market, but it currently covers only Mumbai + Goa. That is not enough for the India-focused pass.

**Draft options:**

1. **Preferred:** create an India-focused derivative/draft, e.g. `uber-india`, using the four accepted baseline India markets. Keep the global Uber page unchanged until review.
2. **Alternative:** expand the existing global Uber `india` market/subpage to include Kerala + Andaman. This is simpler but risks making the global Uber proposal do too much.

**India derivative baseline:**

- Mumbai / Maharashtra waterfront corridors — proposal-ready after economics cascade.
- Goa — proposal-ready only after the Goa marquee expansion pass below.
- Kerala / Kochi + backwaters — display-ready baseline; needs sufficiency review before marquee.
- Andaman — display-ready baseline; needs use-case sorting before marquee.

**Do next:**

- Draft from the same spine as Rapido/Ola.
- Use official Uber India city coverage as the broad source; promote exact city support only where it changes a market decision.
- Do not borrow non-India Uber global markets into the India derivative.

### 4. Noon

**Status:** queued after India normalization.

**Do next:**

- Use `uae-gulf-shared-corridor-spine.json`.
- Mirror Careem-style mechanics: domestic UAE first, then UAE/Gulf cross-border roadmap.
- Treat Noon as platform GMV / commerce + mobility enablement, not a ride-hail clone.
- Keep Manama ↔ KSA Eastern Province as the only commercial-now Gulf cross-border candidate; other Gulf cross-border lanes stay Quanta-LR roadmap.

## Goa promotion: from safe baseline to marquee/full

The current Goa spine has 16 geometry-present routes, but they skew toward short ferry/marina hops. That is safe for baseline display, not enough for a tourism destination.

### Local use-case gate

Goa clears the Phase 3 gate for promotion because it has multiple local use cases:

1. **Mandovi / river ferry commuter + tourist mobility:** official Goa River Navigation Department ferry routes include Panaji-Betim, Ribandar-Chorao, St. Pedro-Diwar, and related island crossings.
2. **Tourism resort/beach transfers:** North Goa ↔ South Goa, Panaji/Mandovi ↔ beach belts, and island/day-trip flows are the core premium water-mobility story.
3. **Arrival/port transfer logic:** Mopa/Dabolim airport and Mormugao/Panaji arrival flows should be treated as exact-bind candidates, not assumed routes, until jetties/geometry are sealed.
4. **Konkan line-haul roadmap:** Goa ↔ Mumbai remains Quanta-LR roadmap, not N30 commercial-now.

### Required exact-bind expansion families

- Panaji / Mandovi / Old Goa ferry spine.
- North Goa beach-resort corridor.
- South Goa resort corridor.
- Grande Island / day-trip corridor, if exact geometry is clean.
- Mormugao / port-arrival corridor, if exact geometry is clean.
- Goa ↔ Mumbai Quanta-LR roadmap corridor.

### Current route-quality note

Several existing Goa labels look like raw POI labels rather than proposal-grade corridor names (`Yacht Life Goa`, `Marina Russian B2B Thai Spa Service near me`, etc.). Keep those routes as geometry candidates, but Grok should canonicalize labels before partner-facing render/export.

## Active exact-bind expansion lanes

These are no longer passive candidate notes. They are active lanes, but each stays out of `network_footprint[]` until exact Atlas support exists.

| Lane | Why active | Primary partner fit | Gate before display |
|---|---|---|---|
| Gujarat coast / ports | Adani Ports official page lists Mundra, Tuna, Dahej, Hazira; strong port/coastal spine. | Adani first; Reliance/Jio overlay second; mobility partners only if supported. | Exact port/city/BP bind; no broad Gujarat footprint card. |
| Tamil Nadu / Chennai coast | Adani official page lists Kattupalli and Ennore; Uber official city page supports Chennai/Tamil Nadu entries. | Uber/Ola/Rapido; Adani port overlay. | Exact Chennai/Kattupalli/Ennore bind. |
| Andhra / Visakhapatnam | Adani official page lists Gangavaram; Uber city page includes AP entries including Vizag-area names. | Uber/Ola/Rapido; Adani port overlay. | Exact Vizag/Gangavaram bind. |
| West Bengal / Kolkata-Haldia | Uber official city page includes Haldia and Kolkata-area entries; Adani official page lists Haldia. | Uber/Ola/Rapido; Adani port overlay. | Exact Kolkata/Haldia/Sundarbans-edge validation; avoid fuzzy river/coast geography. |
| Lakshadweep | Strong future tourism/atoll logic, but not grounded enough for this pass. | Kerala extension / Quanta-LR future. | Hold unless already grounded or explicitly green-lit. |

## Grok deterministic handoff

Hand this batch to Grok for deterministic work only:

1. Route reconciliation for Rapido/Ola against `india-shared-corridor-spine.json`.
2. Uber India derivative generation from the same four-market accepted baseline.
3. Goa label canonicalization + route addition proposal, with nulls for unbound geometry.
4. Economics cascade after route binding, including economics sidecar generation.
5. Render QA: anchor city IDs, market subpages, route chips, and TAM ladder.

Tasklet should not invent new boarding points or silently add ungrounded markets. Null beats a sparkly wrong answer.
