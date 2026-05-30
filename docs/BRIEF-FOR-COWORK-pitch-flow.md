# Claude Cowork — Test Brief: Pitch-Document Flow (round 3)

_2026-05-30 · supersedes the round-2 brief (`COWORK-TEST-BRIEF.md`) · partner-facing reviewer; observe-and-report_

**URL:** https://navier-atlas.vercel.app — **the pitch render is LIVE.**
**What's new since round 2:** clean City→City route labels, rich city pitch panels (19 cities), partner
pitch mode with a phase carousel (`?partner=<slug>`, 6 partners), and **route colour = platform**
(Pioneer II mint solid · Quanta-LR amber dashed) — trip purpose now shows only on hover / in the route panel.
**Lanes:** tag every finding `[RENDER]` (Claude Code) or `[DATA]` (Tasklet) — see "How to route findings".

## Gate 0 — Confirm you're on the new build (30 seconds)
Deploys can be cached; make sure you're not looking at an old version before reporting failures.
1. Click **Singapore** → you should see a **rich pitch panel** (tagline, "Why marine mobility here",
   use-cases). If you only get a plain name/details panel → hard-refresh (Cmd/Ctrl-Shift-R). If still
   plain after a refresh, report **"new UI not served"** and stop.
2. Open `…/?partner=grab` → the panel should be a **pitch carousel** (hero + "Phased rollout" with ‹ ›
   and dots).
3. Routes draw (mint Pioneer II + amber dashed Quanta-LR); `…/#camera=103.85,1.29,12` lands on Singapore.
   **Cite all findings by camera (`#camera=lng,lat,zoom`) or partner (`?partner=<slug>`) deep-link.**

## A. Route-label correctness
1. Hover/click ~15 routes across MENA + SEA. **PASS** = clean origin→destination, no underscores, no
   raw slugs, no "Bp 643f1f62a7". Spot-check old offenders: Salalah→Hasik, Jeddah→Shura,
   Doha→Lusail/Pearl, Dubai→Sir Bani Yas.
2. Every Quanta-LR (amber) route reads **City → City** (or City → Destination (Region)).
3. The literal **"boarding point"** as an endpoint is an **acceptable fallback** (that BP has no name in
   the data yet) — log as `[DATA]` "name this BP", not a render bug. Underscores / "Bp <hash>" leaks = `[RENDER]`.

## B. Rich city pitch panel (19 cities have briefs)
3. Click a spread of brief cities — **MENA:** Dubai, Abu Dhabi, Doha, Jeddah, Muscat, Manama ·
   **SEA/S.Asia:** Singapore, Bali, Phuket, Bangkok, Jakarta/Batam, Hong Kong, Malé, Colombo ·
   **Red Sea:** NEOM/Sindalah, Sharm El-Sheikh, Red Sea Global. **PASS** = panel shows hook/tagline,
   demand signals, use-cases badged by archetype, Navier-fit (Pioneer II + Quanta-LR), signature routes
   (+ live routes), transit-planning angle. Reads like a fast "why Navier here" for a partner.
4. A city **without** a brief shows the lightweight panel — that's expected; log `[DATA]` "missing brief
   for <city>", not a bug.
5. Partner overlay: `?partner=grab` → Singapore/Bali/Phuket lead with the super-app / cross-border angle;
   `?partner=dubai-rta` → Dubai leads with the public-transit angle.

## C. Partner pitch mode + phase carousel — FUNCTION (all 6 partners)
For **grab, careem, dubai-rta, abu-dhabi-itc, red-sea-global, singapore-mpa**, step phases 1→2→3.
**PASS** per step = (a) camera flies to the phase, (b) only that phase's cities/routes are lit and the
rest dim, (c) narrative + KPIs + featured-routes swap, (d) dots / ‹ › track the active phase.
6. Deep-link + reload: append `#/partner/grab/phase/3`, reload → restores phase 3.
7. Navigation coherence: click a city while in a carousel → its city panel opens; click empty water →
   returns to the carousel (not a blank/admin panel).
8. If a partner shows a story-list instead of a carousel, flag it (`[RENDER]`).

## D. ⭐ Partner-page QUALITY — accuracy & usefulness (the core of this round)
For each partner × phase, judge whether the partner could **present it as-is**. Method: read the panel
(featured routes, KPIs, narrative), then **inspect the lit map** — zoom into the corridor, hover/click
the lit routes, zoom to the endpoint POIs. Score each phase 1–5 on:

1. **Route accuracy (geography).** Each lit route is **City → City**, runs **on water**, crosses **no
   land/islands**, and ends at a **real coastal place** (marina / ferry terminal / jetty), not mid-ocean.
   Hover for the label; click for platform · distance · ETA — plausible? (Pioneer II ≤70 nm electric;
   Quanta-LR longer / hybrid.) *Geometry / land-crossings → `[DATA]`.*
2. **POI / boarding-point quality.** Zoom to each lit endpoint: is the BP **on the coast / water** at a
   plausible marina/terminal — **not inland**? Spot-check known offenders: **Dubai** (marinas on the
   Creek, not the street grid), **Abu Dhabi** (no jetty at Khalifa City), **Phuket** (no ferry triangle
   near Thalang, inland). *Placement → `[DATA]`.*
3. **Commercial usefulness / market fit.** Do the lit routes suit the partner's archetype? super-app
   (grab/careem) = dense commuter + cross-border demand; public-transit (dubai-rta/abu-dhabi-itc) =
   authority-grade inner-harbour + intercity corridors; tourism/hospitality (red-sea-global) = resort
   island hops. Is the **phasing a credible rollout** — small proven beachhead → scale → region?
4. **Narrative ↔ map coherence.** Do the panel's claims match the map? e.g. "5 boats / 3 corridors" ≈ a
   handful of lit routes in phase 1; "+Bali +Phuket" in phase 3 actually lights those clusters. Do the
   **featured-routes** in the text correspond to **routes you can find lit** on the map?
5. **City-brief cross-check.** Click each phase city → do its brief's **signature routes** and
   **use-cases** match what's drawn (same corridors, same platform)? Inconsistencies → `[DATA]`.

**Per-partner deliverable:** a 1-line "present as-is? yes/no" verdict + the top 3 fixes, each tagged
`[RENDER]` or `[DATA]`. Special attention to **grab phase 3** (its `bali`/`phuket` ids are resolved at
render) — confirm Bali & Phuket actually light up; if not, `[RENDER]`.

## E. Regression guard
9. Flagship labels (Doha/Dubai/Abu Dhabi/Muscat/Singapore) don't stack at world view (collision-thin
   holds; Singapore always labelled).
10. Routes still render (F-01); **no console layer-validation errors**.
11. Route **colour = platform** (mint Pioneer II / amber Quanta-LR); trip purpose appears only in the
    hover tooltip + route panel, never as line colour. Legend ↔ map parity.
12. Cold-load acceptable; panels don't blanket the map on first load; stats not occluded.

## How to route findings
- **`[RENDER]` (Claude Code):** labels, panel / carousel layout, camera / focus / dim, deep-links,
  collision/declutter, F-01, console errors.
- **`[DATA]` (Tasklet):** route geometry / land-crossings / existence, BP-on-water placement, BP names,
  partner narrative / KPI / featured-route content, missing city briefs, phase city-id alignment.

## Known state (don't file these as bugs)
- Per-partner isolated `/slug` URLs are **not** in this round (build tooling pending).
- Some labels are render-recovered from node names; "boarding point" fallback is fine.
- `trip_purpose` is sparse / "mixed" in the data — irrelevant to colour now (colour = platform).

## Report format
Per check: **PASS / FAIL** + 1-line note + screenshot + camera/partner deep-link + lane tag. Then a
**per-market partner-ready verdict** for all six: Grab, Careem, Dubai RTA, Abu Dhabi ITC, Red Sea Global,
Singapore MPA.
