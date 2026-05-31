> ⚠️ **SUPERSEDED — do not run this version.** The current QA plan (v5: 10 partners, 78 briefs,
> per-partner `/<slug>` pages, region dropdown, US expansion) is the canonical
> [`docs/BRIEF-FOR-COWORK-pitch-flow.md`](../docs/BRIEF-FOR-COWORK-pitch-flow.md). The text below is the
> earlier (6-partner / 19-city) round, kept for history.

---

# Claude Cowork — Front-End Test Brief (Pitch-Document Flow)

**From:** Tasklet + Claude Code · updated 2026-05-30 (post PR #3, post node-id fix)
**URL:** https://navier-atlas.vercel.app — **render pass is LIVE** (city-brief panel, partner phase carousel, clean route labels). Runnable **now**.
**Partners:** `?partner=<slug>` — `grab`, `dubai-rta`, `careem`, `abu-dhabi-itc`, `singapore-mpa`, `red-sea-global` (each = a 3-phase carousel).
**Cite findings by deep-link:** camera `…/#camera=<lng>,<lat>,<zoom>`; partner+phase `…/?partner=<slug>#/partner/<slug>/phase/<n>`.

## Data contract you're testing against (live `window` globals)
- `window.CITY_BRIEFS[cityId]` — 19 partner-neutral city briefs (hook, demand signals, use-cases by archetype, vessel fit, signature routes, POIs, PT angle).
- `window.PARTNERS[slug]` — `{partner_id, display, archetype, region, hero, why_now, phases[], close}`; `phases[]` is **ordered**, each = `{n, label, boats, cities[], route_scope, featured_routes[], narrative, kpis[], map_focus}`.
- **City-id contract (regression-critical):** `cities[]` tokens and `CITY_BRIEFS` keys are **canonical node ids** (`bali-indonesia`, `phuket-phang-nga-thailand`, `singapore`). A phase that fails to light a city, or an empty city panel, usually means a token↔node-id mismatch (the bug just fixed in Grab phase 3).
- **Route colour = PLATFORM** (Pioneer II mint solid · Quanta-LR amber dashed). Trip purpose shows only in the hover tooltip / route panel — **never** as line colour.

## Gate 0 — confirm you're on the new build (30s)
Click **Singapore** → rich pitch panel (demand signals/use-cases) = live. Plain name/details panel = stale cache → hard-refresh (Cmd/Ctrl-Shift-R). Then `?partner=grab` → a "Phased rollout" carousel. Routes draw (mint solid + amber dashed). If still plain after refresh, report "new UI not served" and stop.

---

## A. Route-label correctness
1. Hover/click ~15 routes across MENA + SEA. **PASS** = clean `Origin → Destination`, no underscores, no raw slugs, no `Bp 643f1f62a7`. Spot-check old offenders: Salalah→Hasik, Jeddah→Shura, Doha→Lusail/Pearl, Dubai→Sir Bani Yas.
2. Every Quanta-LR (amber dashed) route reads City → City (or City → Destination (Region)) and is **long-haul** — flag any amber route that looks short (<~70 nm) or ends "in the middle of nowhere". (Expectation: **0** QLR ≤70 nm; short hops are solid Pioneer II.)
3. **Exclusion check:** confirm **no** NEOM↔Eilat / Sharm↔Eilat (Israel) routes render anywhere (should be 0 — hard-excluded).
4. A bare **"boarding point"** as an endpoint is an acceptable fallback (that BP has no name in the data yet) → log `[DATA]` "name this BP", not a render bug. Underscores / `Bp <hash>` = `[RENDER]`.

## B. Rich city panel (pitch synthesis · 19 cities)
5. Click a spread — **MENA:** Dubai, Abu Dhabi, Doha, Jeddah, Muscat, Manama · **SEA/S.Asia:** Singapore, Bali, Phuket, Bangkok, Jakarta/Batam, Hong Kong, Malé, Colombo · **Red Sea:** NEOM/Sindalah, Sharm El-Sheikh, Red Sea Global. **PASS** = panel shows hook/tagline, demand signals, use-cases badged by archetype, Navier-fit (Pioneer II + Quanta-LR distinguished), signature routes, transit-planning angle. Reads like a fast "why Navier here".
6. Confirm **Bali** and **Phuket** panels populate (the recently node-id-fixed Grab phase-3 cities). A city without a brief shows the lightweight panel → log `[DATA]` "missing brief", not a bug.
7. Partner overlay: `?partner=grab` → Singapore/Bali/Phuket lead with the super-app/cross-border angle; `?partner=dubai-rta` → Dubai leads with public-transit.

## C. Partner pitch mode + phase carousel — FUNCTION (all 6 partners)
8. `?partner=grab`: panel becomes a pitch doc (hero + why-now + phase carousel). Step phases 1→2→3. **PASS** per step = (a) camera flies (`map_focus`), (b) that phase's cities/routes light & the rest dim, (c) narrative + KPIs + featured-routes swap, (d) dots/‹ › track the active phase.
   - Phase 1 = Singapore, 5 boats. Phase 2 = full Singapore **+ cross-border Riau** (18 boats). Phase 3 = adds **Bali + Phuket**.
9. `?partner=dubai-rta`: same stepping (Creek pilot → full inner Dubai → Dubai↔Abu Dhabi corridor). Spot-check **careem, abu-dhabi-itc, singapore-mpa, red-sea-global** each load a coherent hero + 3 phases (not a story-list — flag `[RENDER]` if so).
10. **Deep-link + reload:** append `#/partner/grab/phase/3`, reload → restores phase 3.
11. **Navigation coherence:** click a city while in a carousel → its city panel opens; click empty water → returns to the carousel (not a blank/admin panel).

## D. ⭐ Partner-page QUALITY — accuracy & usefulness (the core of this round)
For **each partner × phase**, decide whether the partner could **present it as-is**. Method: read the panel (featured routes, KPIs, narrative), then **inspect the lit map** — zoom into the corridor, hover/click each lit route, zoom to the endpoint POIs. Score the phase 1–5 on:

1. **Route accuracy (geography).** Each lit route is **City → City**, runs **on water**, crosses **no land/islands**, and ends at a **real coastal place** (marina / ferry terminal / jetty), not mid-ocean. Hover for the label; click for platform · distance · ETA — plausible? (Pioneer II ≤70 nm electric; Quanta-LR longer / hybrid.) *Geometry / land-crossings → `[DATA]`.*
2. **POI / boarding-point quality.** Zoom to each lit endpoint: is the BP **on the coast/water** at a plausible marina/terminal — **not inland**? Spot-check known offenders: **Dubai** (marinas on the Creek, not the street grid), **Abu Dhabi** (no jetty at Khalifa City), **Phuket** (no ferry triangle near Thalang, inland). *Placement → `[DATA]`.*
3. **Commercial usefulness / market fit.** Do the lit routes suit the partner's archetype? super-app (grab/careem) = dense commuter + cross-border demand; public-transit (dubai-rta/abu-dhabi-itc) = authority-grade inner-harbour + intercity corridors; tourism/hospitality (red-sea-global) = resort island hops. Is the **phasing a credible rollout** — small proven beachhead → scale → region?
4. **Narrative ↔ map coherence.** Do the panel's claims match the map? e.g. Grab Phase 1 "5 boats / 3 corridors" ≈ a handful of lit routes; Phase 3 "+Bali +Phuket" actually lights those clusters. Do the **featured-routes** text entries correspond to **routes you can find lit** on the map?
5. **City-brief cross-check.** Click each phase city → do its brief's **signature routes** and **use-cases** match what's drawn (same corridors, same platform)? Inconsistencies → `[DATA]`.

**Riau density (Grab Phase 2, new this build):** the Singapore↔Batam/Bintan corridor should read as a **dense cross-border mesh** — many jetties (Batu Ampar, Sekupang, Teluk Senimba, Punggur, Nongsa, Lagoi, Tanjung Uban), not 1–2 lonely lines. NOTE: Phase 2 `cities` is `['singapore']` **by design** — Riau shows via routes + boarding points + camera framing, so confirm `map_focus` frames the SG↔Riau span and the narrative carries the cross-border story.

**Per-partner deliverable:** one line — "present as-is? yes/no" + the top 3 fixes, each tagged `[RENDER]` or `[DATA]`.

## E. Regression guard
12. Flagship labels (Doha/Dubai/Abu Dhabi/Muscat/Singapore) don't stack at world view (collision-thin holds; **Singapore always labelled**).
13. Route lines render (F-01) — mint Pioneer II solid + amber-dashed Quanta-LR visible in SG/Dubai/Abu Dhabi/Bali/Phuket. **No console layer-validation errors.**
14. Colour = **platform**, never trip-purpose; legend ↔ map parity.
15. Cold-load acceptable; panels **frame** the map (don't blanket it on first load); stats not occluded.

## How to route findings
- **`[RENDER]` (Claude Code):** labels, panel/carousel layout, camera/focus/dim, deep-links, collision/declutter, F-01, console errors.
- **`[DATA]` (Tasklet):** route geometry / land-crossings / existence, BP-on-water placement, BP names, partner narrative/KPI/featured-route content, missing city briefs, phase city-id mismatches.

## Known state (don't file as bugs)
- Per-partner isolated `/slug` URLs aren't in this round (build tooling pending).
- Some labels are render-recovered from node names; "boarding point" fallback is fine.
- `trip_purpose` is sparse/"mixed" in data — irrelevant to colour (colour = platform).

## Report format
Per check: **PASS / FAIL** + 1-line note + screenshot + camera/partner deep-link + lane tag. End with a **per-market partner-ready verdict** for all six: Grab, Careem, Dubai RTA, Abu Dhabi ITC, Red Sea Global, Singapore MPA.
