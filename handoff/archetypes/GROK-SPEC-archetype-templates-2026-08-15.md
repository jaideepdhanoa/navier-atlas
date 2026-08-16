# GROK SPEC — Archetype Template System + Boston Pilot
**Date:** 2026-08-15 · **Author:** Tasklet · **Audience:** Grok (navier-atlas front end)
**Repo destination:** `handoff/archetypes/GROK-SPEC-archetype-templates-2026-08-15.md` (PR body basis)
**Canon:** ARCHETYPE-STRATEGY.md (D1–D6), PUBLIC-PARTNERS-BRIEF.md, FLEET-INVESTORS-BRIEF.md, boston/AUTHORITY-MAP-BOSTON.md, boston/FLEET-ECONOMICS-BOSTON.md, boston/TRACKER-SNAPSHOT-2026-08-15.md, SPEED-RULE-RELIEF-PRECEDENTS.md

---

## 1 · Purpose & scope

Expand the employer microsite system into a **three-archetype system** over one shared data spine:

| Archetype | Status | Route pattern | Access |
|---|---|---|---|
| Employers | live — **unchanged by this PR** | existing employer routes | public |
| Public Partners | new | `/{city}-partners` | public, indexed |
| Fleet Investors | new | `/{city}-invest` | **unlisted** (noindex, no sitemap, no nav/cross-links) |

> Slug note: `-partners` / `-invest` suffixes are the contract; align the exact slug pattern to whatever the live employer route convention is in this repo (e.g. `/boston-partners` if employer pages are `/boston-employers`). Do not introduce a third pattern.

One data spine, three lenses: all three archetypes render **views of the same hub.json** (stops, lines, segments, phases). Same corridors on all three microsites — nothing added, nothing removed (Decision D3).

**This PR:** archetype registry + two new page templates + shared-component extensions + **Boston pilot only** (both new pages, built from two authored data files shipped alongside this spec). Six more cities follow later as **data-only handoffs** — no template changes expected after pilot QA.

## 2 · Architecture

### 2.1 Archetype registry — `employer-hub/archetypes.json` (new)

```json
{
  "archetypes": [
    { "id": "employers",       "label": "Employers",       "route": "existing employer route (unchanged)", "access": "public",   "dataFile": null },
    { "id": "public-partners", "label": "Public Partners", "route": "/{city}-partners", "access": "public",   "dataFile": "public-partners.json", "template": "public-partners" },
    { "id": "fleet-investors", "label": "Fleet Investors", "route": "/{city}-invest",   "access": "unlisted", "dataFile": "fleet-investors.json", "template": "fleet-investors" }
  ]
}
```

A city's archetype page exists **iff** its data file exists under `employer-hub/hubs/{city}/`. No data file → no route, no placeholder page (fail closed).

### 2.2 Data layout per city

```
employer-hub/hubs/{city}/
├── hub.json                 # single source of truth: stops, lines, segments, phases, geometry — UNCHANGED
├── public-partners.json     # authored by Tasklet (archetype copy + data; contract = Boston pilot file)
└── fleet-investors.json     # authored by Tasklet (archetype copy + data; contract = Boston pilot file)
```

Archetype JSON files carry a `copy` / `data` split per module: `copy` fields are authored strings rendered **verbatim**; `data` fields are structured values Grok formats visually. Underscore-prefixed fields (`_contract`, `_guard`, …) are non-renderable guard notes and must never reach the DOM. Grok renders, never invents; `null` or missing = render nothing (no defaults, no placeholder text).

### 2.3 Routing & access

- `/{city}-partners`: public, indexed, linkable from employer pages if desired (Grok's call within design system).
- `/{city}-invest`: **unlisted** — `<meta name="robots" content="noindex">`, excluded from sitemap.xml, excluded from ALL nav, footers, and cross-links on every page of the site. Reachable only by direct URL. **Employer and Public Partners pages get NO visible link to invest pages.** Unlisted mechanics implemented once at template level.
- Flywheel cross-links: Public Partners may link to the employer page; Fleet Investors pages may link OUT to employer/partners pages but never receive inbound links.

## 3 · Public Partners page template (`public-partners`)

Page spine per PUBLIC-PARTNERS-BRIEF.md §3, in this order (all content from `public-partners.json`; sections with missing data are omitted, never stubbed):

1. **Hero** — city image + public-value headline (authored copy).
2. **The gap** — city's own published pain, sourced (authored copy + sourced stats).
3. **The network** — corridor map **inherited from employer template unchanged** (D3): same stops, lines, phases, phase toggle. Zero geometry divergence.
4. **Infrastructure-light** — landing-gate advantage panel (authored copy + `landings_verified` stat).
5. **Two ways to partner — dual-posture module (new component).** Enable / Operate two-track panel per brief §2. City-level weighting driven by `data.posture` (`enable_dominant` | `operate_dominant` | `balanced`): weighting affects order/visual emphasis only — **both tracks always render**. Operate proof points render only from data (never invented precedents).
6. **Public value + quality-of-life pillar** — stat band; every stat carries its source or assumption string from data. QoL copy points (waterfront activation, time returned, business attraction) are authored.
7. **Speed-rule-relief pillar (new component, standing on every city page).** Pattern: "Your speed rules were written for boats that make wake." Localized from `data.speed_rule_relief`. Hard rules:
   - Base map/trip times ALWAYS reflect posted limits. No exemption ever assumed anywhere in base UI.
   - Relief minutes render ONLY inside a **visually distinct, labeled layer** ("What speed-rule relief unlocks") — off by default, clearly badged as conditional. If `relief_minutes` is null, the layer renders the qualitative invitation copy only, no numbers.
   - Stockholm precedent line rendered verbatim from copy (pre-hedged; do not strengthen).
8. **Plan alignment (new component)** — city plans quoted with sources, from data. Render quotes exactly.
9. **Authority landscape module (new component)** — rendered from `data.authorities`: body, one-line role, posture classification badge (Enable / Operate / Permitting gate). Only bodies present in data render. **Never render contact info.** Non-authority stakeholders are excluded from data upstream — do not add any.
10. **Modal integration** — our stations vs their transit nodes (map layer, data-driven).
11. **The vessels** — N30 Quanta (8 pax) + N45 Explorer (20 pax), electric foiling, spec strings from data. No defense, no Series B content.
12. **Flywheel module (new shared component, also used on Fleet Investors).** Three wheels: *employers commit demand → public partners unlock landings → fleet investors finance vessels*. Each wheel carries its honesty caption from copy (LOIs non-binding; landings sought, not secured; fleet financing being raised). No numbers unless supplied in data.
13. **The ask / CTA + intake** — "Start with one corridor." Form fields from `data.intake`: authority name, agency type, role, corridor(s) of interest, posture interest (enable / operate / both / exploring), message. Same intake infra as employer LOI, archetype tag `public-partners`.

Tone: civic, sober, plan-literate (brief §4). Grok must not paraphrase copy fields.

## 4 · Fleet Investors page template (`fleet-investors`)

Page spine per FLEET-INVESTORS-BRIEF.md §3 with **D6 LOCKED: anchor-plus-fill is the lead economic frame** — anchor-tenant contracted revenue leads; seat-band fill is upside on top; standalone per-seat yield is NEVER the headline.

1. **Hero** — "Own the fleet behind {City}'s water commuter network" + anchor-first subline from copy.
2. **The model** — franchise structure panel (fleet investor / operator / Navier / employers / public partners) + launch trigger as the core protection.
3. **The asset** — N45: $2.5M, 20 passengers, electric foiling, workboat-grade. Redeployability panel (7-city network = residual-value story).
4. **The network** — corridor map inherited unchanged (D3) + launch-trigger explanation.
5. **Demand-pool module (new component).** Named employers + headcounts render ONLY with the standing label, verbatim, visually attached to the table:
   > "Indicative of demand potential along these corridors — not commitments or commercial relationships."
   Columns: employer · node · line(s) · on-site headcount (with its verification label) · demand-pool seats (with capture assumption). Rows render only from data; blank cells stay blank. No logo walls.
6. **Summary P&L module (new component) — anchor-first structure (D6):** anchor contract line → fill upside band → opex lines → Navier network share → indicative payback range. Rules:
   - Ranges only, never point estimates; conservative default posture.
   - **Every line renders its assumption label from data** (e.g. "placeholder, not validated", "program band — not a city quote"). A line without a label in data must not render.
   - Seat-band scenarios appear as the fill/upside band beneath the anchor line, never as the headline economics.
   - **Speed-rule relief appears only as a clearly labeled upside row** ("with authority speed-rule relief — precedent: Stockholm Candela P-12 exemption"), never blended into base or mid cases. If unquantified in data, render the label row without numbers.
7. **Protection stack** — four cards from data: demand-gated launch (60–80 committed-seat trigger) · redeployable network asset · Navier platform continuity · phased fleet growth.
8. **Fleet phasing module (new component)** — vessels at launch vs full build per line + capital, all with assumption labels from data (headway ceilings are illustrative, not timetables).
9. **The ask / CTA + intake** — request city fleet memo. Form fields from `data.intake`: name, entity, capital type (family office / fund / individual / operator+capital), city(ies), indicative fleet interest (1–2 / 3–5 / 5+), message. Tag `fleet-investor`.

Unlisted mechanics per §2.3. Tone: investment-grade sobriety; numbers carry the argument (brief §4).

## 5 · Shared components

**Reused unchanged from employer templates:** hub.json loader, corridor map + stations/lines/interchanges, phase toggle, trip planner, design system (type, color, spacing), responsive frame, intake-form infra (new archetype tags only).

**New components (this PR):** dual-posture panel · public-value stat band · speed-rule-relief pillar (+ labeled relief layer) · plan-alignment panel · authority-landscape module · modal-integration layer · flywheel module (shared by both new templates) · demand-pool table (+ standing-label frame) · summary P&L (anchor-first, range+assumption rendering) · protection-stack cards · fleet-phasing table · vessels panel · unlisted-access mechanics · two intake variants.

**Dependency — `water_min_label` fix (PR #356):** the shared `waterMinLabel()` currently ignores `water_min_label`, so speed-honesty qualifiers don't render. **Both archetype templates depend on this fix**; speed-constrained segment labels must render correctly before the pilot ships. Do not merge this PR ahead of that fix.

**Fields that must NEVER reach the DOM (any archetype, any city):**
- Internal dock-status fields: `note_internal`, `decision_ledger`, `watchlist`, `no_landing`, `legacy_ids`, gate flags (e.g. `logan_held`), any negotiation-status vocabulary.
- Held corridors: **Boston↔Logan, Boston↔Provincetown** — never as stops, lines, labels, or copy.
- Gulf counterparties: **Dubai RTA, Abu Dhabi ITC, RAKTA** — never, in any form.
- Series B / Navier equity / valuation / fundraise content, defense content.
- Authority contact names/emails; employer tracker priority codes (P0/P1/P2) — internal only.

## 6 · Boston pilot

Build **both** Boston pages from the two authored data files shipped with this spec:

- `employer-hub/hubs/boston/public-partners.json` ← `phase3/boston-public-partners.json`
- `employer-hub/hubs/boston/fleet-investors.json` ← `phase3/boston-fleet-investors.json`

Requirements:
- Geometry from `hubs/boston/hub.json` (post-MECE, PR #356: 18 stops, 5 lines — BOS-1 North Shore, BOS-2 South Shore, BOS-3 Quincy, BOS-4 Inner Harbor, BOS-5 Riverside). **Identical to the employer page — pixel-parity design language, same map, same phase toggle.**
- Known open flag (PR #356): BOS-2 segment-phase tags imply a phase-1 discontinuity (Hull–Rowes at phase 3) contradicting the single phase-1 South Shore route; stop-level phases are correct. Resolve on #356 before pilot QA; archetype views inherit whatever hub.json says — do not patch around it in templates.
- Grok proposes visual design for all new components within the existing design system; Tasklet QAs the pilot hard (checklist §7) before any scale-out to the other six cities.

## 7 · Honesty gates & acceptance checklist (Tasklet pre-merge QA)

- [ ] **Geometry parity:** stops/lines/segments on both new pages identical to employer page; MECE topology untouched; segment-phase invariant holds (`segment.phase === max(stop phases), omit when 1`).
- [ ] **Base-time compliance:** every rendered time uses posted-limit base values; no relief-adjusted number outside the labeled relief layer; `water_min_label` qualifiers render (dependency fixed).
- [ ] **Standing indicative label** present verbatim wherever employer names appear on `/boston-invest`: "Indicative of demand potential along these corridors — not commitments or commercial relationships."
- [ ] **Every P&L line** shows a range + its assumption label; no point estimates; anchor line leads; seat-band scenarios positioned as fill/upside.
- [ ] **Unlisted verified:** noindex meta present on `/boston-invest`; absent from sitemap.xml; zero inbound links site-wide (crawl check); employer + partners pages contain no invest link.
- [ ] **No held corridors:** grep rendered output for `Logan`, `Provincetown` → zero hits on all archetype pages.
- [ ] **Banned-terms scan (rendered DOM + all renderable copy/data values; underscore-prefixed guard fields exempt), zero hits:** `Dubai RTA` · `Abu Dhabi ITC` · `RAKTA` · `Series B` · `valuation` · `fundraise` · `secured` (dock/landing context) · `dock unlock` · `logan_held` · `note_internal` · `decision_ledger` · `revolutionary` · `disruptive`/`disruption` as startup rhetoric (verbatim quotes of an authority's own published plan language, e.g. MassDOT's "disruptions to subway or Commuter Rail service", are exempt) · P0/P1/P2 priority codes.
- [ ] **Approval language:** no claim/implication any authority approved, endorsed, or committed; "we seek" / "in discussion" only; no authority contacts rendered.
- [ ] **WETA** (if it ever appears): existing public-partner relationship framing only — no procurement/approval claims. Not applicable to Boston pages.
- [ ] **Fail-closed check:** no rendered element sources from a field absent in the data files; no placeholder/default copy anywhere.
- [ ] Launch-timing honesty: phase labels match employer site; trigger (60–80 committed seats) and end-2027-earliest language intact where authored.
- [ ] Intake forms live, correctly tagged (`public-partners` / `fleet-investor`), routed to existing infra.

## 8 · Division of labor

| | Tasklet | Grok |
|---|---|---|
| Data & copy | Authors ALL data files and copy blocks (this handoff + future cities) | Renders verbatim; **never invents, paraphrases, or fills content** |
| Templates | Specs (this doc) | Builds templates, components, routing, registry, unlisted mechanics; wires data |
| Design | — | Proposes visuals within existing design system |
| Gaps | — | **Any content gap = fail closed and flag in PR notes; never fill** |
| QA | Pre-merge QA per §7 checklist | Fix rounds |
| Merge | Jaideep merges (neither Tasklet nor Grok) | |

Scale-out (Bay → NY → DC → Miami → Seattle → San Diego) happens only after Boston pilot passes §7 in full; those handoffs are data-only.
