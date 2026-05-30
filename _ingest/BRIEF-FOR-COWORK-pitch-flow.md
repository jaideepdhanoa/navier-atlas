# Claude Cowork — Front-End Test Brief (Pitch-Document Flow)

**From:** Tasklet · updated 2026-05-30 (post PR #3)
**URL:** https://navier-atlas.vercel.app — **render pass is LIVE** (PR #3 merged: city-brief panel, partner phase carousel, clean route labels). These checks are runnable **now** — no longer gated on a future render pass.
**Per-partner builds:** `?partner=<slug>` — slugs: `grab`, `dubai-rta`, `careem`, `abu-dhabi-itc`, `singapore-mpa`, `red-sea-global`.

## Data contract you're testing against (live `window` globals)
- `window.CITY_BRIEFS[cityId]` — 19 partner-neutral city briefs (hook, demand signals, use-cases by archetype, vessel fit, signature routes, POIs, PT angle).
- `window.PARTNERS[slug]` — `{partner_id, display, archetype, region, hero, why_now, phases[], close}`.
  - `phases[]` is **ordered**; each phase = `{n, label, boats, cities[], route_scope, featured_routes[], narrative, kpis[], map_focus}`.
- **City-id contract (regression-critical):** `cities[]` tokens and `CITY_BRIEFS` keys are **canonical node ids** — e.g. `bali-indonesia`, `phuket-phang-nga-thailand`, `singapore`. If a phase fails to light a city or its panel is empty, suspect a token↔node-id mismatch (this exact bug was just fixed in Grab phase 3).

---

## A. Route-label correctness (data live)
1. Hover/click ~15 routes across MENA + SEA. **PASS** = clean `Origin → Destination`, no underscores, no raw slugs, no `Bp 643f1f62a7`. Spot-check old offenders: Salalah→Hasik, Jeddah→Shura, Doha→Lusail/Pearl, Dubai→Sir Bani Yas.
2. Every Quanta-LR (amber dashed) route reads City → City (or City → Destination (Region)) and is **long-haul** — flag any amber route that looks short (<~70 nm) or ends "in the middle of nowhere". (Expectation: **0** QLR ≤70 nm; all short hops are solid Pioneer II.)
3. **Exclusion check:** confirm **no** NEOM↔Eilat / Sharm↔Eilat (Israel) routes render anywhere. (Should be 0 — hard-excluded.)

## B. Rich city panel (pitch synthesis)
4. Click **Dubai**, **Abu Dhabi**, **Singapore**, **Bali**, **Phuket**. **PASS** = panel shows hook/tagline, demand signals, use-cases badged by archetype, Navier-fit (Pioneer II + Quanta-LR distinguished), signature routes, transit-planning angle. Reads like a fast "why Navier here".
5. Confirm **Bali** and **Phuket** panels populate (these are Grab phase-3 cities — the recently-fixed ones).

## C. Partner pitch mode + phase carousel (the core)
6. `?partner=grab`: panel becomes a pitch doc (hero + why-now + phase carousel). Step phases 1→2→3. **PASS** = each step (a) flies the camera (`map_focus`), (b) lights that phase's cities/routes & dims the rest, (c) swaps narrative + KPIs.
   - Phase 1 = Singapore, 5 boats. Phase 2 = full Singapore network **+ cross-border Riau** (18 boats). Phase 3 = adds **Bali + Phuket**.
7. **Riau cross-border density (new this build):** in Grab Phase 2, the Singapore↔Batam/Bintan corridor should now look **dense** — many jetties (Batu Ampar, Sekupang, Teluk Senimba, Punggur, Nongsa, Lagoi, Tanjung Uban). **PASS** = it reads as a real cross-border mesh, not 1–2 lonely lines. NOTE: Phase 2 `cities` is `['singapore']` by design — Riau shows via **routes + boarding points + camera framing**, so confirm `map_focus` frames the SG↔Riau span and the narrative carries the cross-border story.
8. `?partner=dubai-rta`: same stepping check (Creek pilot → full inner Dubai → Dubai↔Abu Dhabi corridor).
9. Spot-check the other 4 partners load a coherent hero + phases: `careem`, `abu-dhabi-itc`, `singapore-mpa`, `red-sea-global`.
10. If Claude Code added `#phase=N` deep-links: set one, reload — does it restore the phase?

## D. Regression guard
11. Flagship labels (Doha/Dubai/Abu Dhabi/Muscat/Singapore) don't stack at world view (collision-thin holds; **Singapore always labelled**).
12. Route lines actually render (F-01) — Pioneer II solid + Quanta-LR amber-dashed visible in SG/Dubai/Abu Dhabi/Bali/Phuket. No console layer-validation errors.
13. Cold-load acceptable; panels frame the map, don't blanket it on first load.

## Report format
Per check: **PASS / FAIL** + 1-line note + screenshot. Tag failures `[RENDER]` (→ Claude Code) or `[DATA]` (→ Tasklet). End with a per-partner verdict: **is the pitch flow partner-ready?**
