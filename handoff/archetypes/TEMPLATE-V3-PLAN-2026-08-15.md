# Archetype microsites v3 — narrative, visuals, and math-bridge plan

**Date:** 2026-08-15 · **Pages:** `/fleet-investors/boston`, `/public-partners/boston` · **Trigger:** Jaideep review of v2 build
**Verdict on v2:** structure fixed (footnotes ✓, stat chips ✓, deck-style P&L ✓, role cards ✓, expander ✓) — but the pages still *assume* instead of *persuade*. Five gaps below, each with a fix and an owner (Tasklet = authored data/assets · Grok = template).

---

## §1 · Diagnosis — five gaps

| # | Gap | Where it shows |
|---|-----|----------------|
| 1 | **Self-owns on the investor page** — the page repeatedly signals dependence on employer deals and inexperience | Hero subline ("Employer-committed seat bundles anchor each corridor before capital deploys"), "60–80 seat launch trigger" hero chip, "Demand-gated launch" callout, "none committed yet" in Operator card, "Navier does not yet operate in Boston" small print, fn1 "Navier has not yet operated these services" |
| 2 | **No visuals** — zero market composites, zero Navier imagery; every section is text + tables | Both pages: only the hero photo (generic, reused from employer page) and the map |
| 3 | **Navier is never introduced** — the vessel, the technology, and why it's different appear nowhere before the ask | FI: "The asset" is 4 spec chips with no image. PP: "The vessels" is two bare text cards buried at the bottom |
| 4 | **P&L math disconnect** — fares are listed, totals are asserted, nothing bridges them; the business models themselves are never explained | FI: "$950–1,275/seat-month" then suddenly "Gross $91,000/mo" — no seats count, no legs count, no sailings count, no "here's how a day works" |
| 5 | **Hierarchy + wayfinding** — no narrative arc, no navigation; PP buries the offer under reference material | PP: Authority landscape (9 cards) and Modal integration sit mid-page at full weight; "Two ways to partner" (the offer) competes with directory content. Both pages: header nav is just Network/Overview |

---

## §2 · The fix — one narrative spine, both pages

Every section answers the reader's next natural question. Sticky anchor nav reflects exactly this order.

**Fleet Investors** (nav: `Vessel · Model · Economics · Network · Plan · Contact`)
1. **Hero** — market composite + sell-first headline + 4 stat chips (no trigger chip, no disclaimers)
2. **Meet the vessel** *(new)* — who Navier is, the N45/N30, why foiling wins (energy, wake, noise, smoothness) — imagery + optional video
3. **The model** — role cards (cleaned: no "none committed yet")
4. **How one vessel earns** *(new)* — service-day timeline: morning commute → midday experiences → evening commute → evening charter → (upside: overnight cargo). This *is* the business-model explainer
5. **The revenue build** *(new)* — the math bridge: per-layer quantity × price = $/mo, summing visibly to gross
6. **The P&L** — existing deck-style table (unchanged numbers), now landing on a reader who has seen the build
7. **The network + demand** — map + demand-pool table (kept as evidence of demand, stripped of trigger mechanics)
8. **The plan** — fleet phasing + protection stack (reframed, see §3)
9. Notes & assumptions → **Contact**

**Public Partners** (nav: `Vessel · Partnership · Value · Network · Reference · Contact`)
1. **Hero** — market composite, chips unchanged (18 stations · 0 terminals · 0 subsidy · 1.5M riders — these are strong)
2. **Meet the vessel** *(new)* — zero-emission, near-zero wake, near-silent: the traits that *are* the public value; imagery + optional video
3. **The gap + plan alignment** *(merged)* — "Massachusetts is already asking" + the three plan quotes in one section; the state's own words do the selling
4. **Two ways to partner** — Enable / Operate (moves UP; this is the offer)
5. **Public value** — ridership, farebox, awards + the three value lines
6. **Speed-rule relief** — keep as-is (short + chips + expander; it works)
7. **The network** — map
8. **Reference** *(new, collapsed by default)* — Authority landscape + Modal integration move here as expanders; content unchanged
9. Notes & assumptions → **Start with one corridor** (contact)

---

## §3 · Self-own kill list (Fleet Investors) — exact replacements

Principle: demand discipline is a *strength* — express it as "capital follows demand" without exposing the employer-LOI machinery or narrating our own inexperience. All removed language survives in `_internal` fields.

| Current (v2) | Replace with |
|---|---|
| Hero subline: "Employer-committed seat bundles anchor each corridor before capital deploys…" | "One vessel, four revenue layers. A premium water network that earns across the whole day — commuters, experiences, charters, and spot seats." |
| Hero chip "60–80 / seat launch trigger" | "18 / stations" (or "20 / seats per vessel") |
| Hero small print "…Navier does not yet operate in Boston." | Delete. Keep only "Indicative economics — conservative defaults, ranges not points.³" |
| Callout "Demand-gated launch / 60–80 committed seats / Corridors launch only at…" | Delete component. Its honest core moves into Protection stack card 1 (below) |
| Protection card "Demand-gated launch … 60–80 committed seats — capital deploys behind committed demand, not ahead of it." | "**Capital follows demand.** Fleet scales corridor by corridor as ridership fills — launch small, grow with proof." |
| Operator card "…none committed yet." | "…existing Boston operators are natural candidates." |
| Employers role card "Contract committed seat bundles … the schedule spine and largest revenue layer." | "Ride the network — commuter bundles at market per-seat prices form the schedule spine." |
| "Each corridor activates only when 60–80 seats are committed. Earliest launch: end of 2027." (network footer + phasing) | "Service phases corridor by corridor from launch lines outward. Target first sailings: 2027." |
| fn1 "…Navier has not yet operated these services in Boston." | "Pricing and experience rates are benchmarked to Boston operators' published 2025–26 fares." (full stop) |
| fn2 "…Seat estimates assume 3.0% capture of on-site headcount, a planning estimate." | Keep — this is a modeling note, not a self-own |
| Demand table column "SEATS" + "City total: 1,350 seats" | Keep table (it's demand evidence) but retitle section "Who works on these corridors" and drop the trigger link |

**Public Partners page:** no employer-trigger language present — only cleanup is moving "The vessels" up into Meet the vessel and demoting reference content.

---

## §4 · Visuals — image manifest (Tasklet generates, Grok places)

Standards: market-specific composites per N30/N45 compositing canon (vessel fidelity mandatory, bright daylight/golden hour, minimal gold, stable repo-linked URLs, no Atlas-generated imagery).

| Slot | Page(s) | Composite spec |
|---|---|---|
| `hero-fleet-boston` | FI hero | N45 foiling across Boston Inner Harbor, downtown skyline + Zakim or Seaport backdrop, golden hour, flat wake visible |
| `hero-public-boston` | PP hero | N45 at speed passing Long Wharf / Custom House tower, clean flat wake in frame (the public-value shot), bright daylight |
| `vessel-n45-plate` | Both, Meet the vessel | N45 Explorer beauty plate, foilborne, side profile, open water |
| `vessel-n30-plate` | Both, Meet the vessel | N30 Quanta at dock or foilborne, complements N45 plate |
| `service-day-experience` | FI, service-day timeline | Evening harbor experience: guests aboard, city lights or sunset skyline |
| `service-day-commute` | FI, service-day timeline | Morning commute: professionals boarding at a pier, vessel waiting |

Video: one embed slot per page in Meet the vessel (official Navier footage only). **Open item for Jaideep:** confirm approved video URL(s) — until then the slot renders the vessel plate instead. No unapproved or third-party footage.

---

## §5 · Revenue build — the math bridge (Tasklet authors, Grok renders)

New `revenue_build` module (per scenario, mid shown by default), rendered as a build-up table directly above the P&L:

```
Committed commuter bundles   [n] seats sold × $[price]/seat-month          = $X/mo
Spot seats                   [n] legs/day × [n] seats/leg avg × $[fare]    = $X/mo
Experiences                  [n] sailings/wk × [n] seats × $[price]        = $X/mo
Private charters             [n] charter-hrs/mo × $[rate]/hr               = $X/mo
────────────────────────────────────────────────────────────────
Gross revenue / month                                            = $91,000
```

Every quantity comes from the approved stack model (`REVENUE-STACK-BOSTON.md`) — no new assumptions, just *exposing* the ones already inside the totals. Each line's quantity gets a footnote ref. The three scenarios differ only in the quantities, making the conservative→upside logic legible at a glance.

Paired with the **service-day timeline** (§2 FI-4): a horizontal day strip (0600–2300) showing which layer earns in which window — commute AM / experiences midday / commute PM / charter evening / (upside) cargo overnight. Timeline = when; revenue build = how much; P&L = what's left.

---

## §6 · Division of labor

**Tasklet (authored data + assets) — before Grok starts:**
- T1. Both JSONs → v3: §3 kill-list replacements, `navier_intro` module (vessel + technology copy, plain English), `service_day` module, `revenue_build` module with exposed quantities, `nav_anchors` list, image-slot references, PP section reorder + `reference_collapsed` flags
- T2. Generate 6 composites per §4 manifest, commit to repo at stable paths
- T3. Update spec ADDENDUM v3 + this plan into the PR for Grok

**Grok (template) — binding list:**
- G1. Sticky anchor nav component (renders `nav_anchors`; both archetype pages)
- G2. Image slots: hero composite per page, vessel plates in Meet the vessel, timeline imagery; video embed component (renders only if `video_url` present)
- G3. `navier_intro` section component — image left / copy right, spec chips, 3 technology proof chips (energy · wake · noise)
- G4. `service_day` timeline component — horizontal day strip, layer-colored windows, upside windows visually separated (dashed/muted)
- G5. `revenue_build` table component — quantity × price = subtotal rows summing to gross; renders above P&L; scenario toggle shared with P&L
- G6. Delete the trigger callout component from FI; apply §3 copy (comes from JSON, but remove any hardcoded trigger strings)
- G7. PP reorder per §2; `reference_collapsed` sections render as expanders (Authority landscape, Modal integration)
- G8. Retain all v2 wins: footnote system, deck P&L, status chips, role cards, speed-rule expander
- G9. QA: side-by-side vs `/employers/boston` + §7 kill-scan; screenshot hand-back before any city replication

## §7 · QA gate (updated)
Adds to the existing kill-scan: `trigger`, `committed seats` (outside demand-table context), `not yet operate`, `has not yet operated`, `anchor` (FI renderables), `none committed`. Gate unchanged: **no city replication until Boston passes the employer-page bar side-by-side.**
