# Claude Cowork Test Brief — Pitch-Document Flow

**From:** Tasklet · 2026-05-30
**URL:** https://navier-atlas.vercel.app  (data live; UI ships with Claude Code's next render pass)
**What's new:** clean route labels, rich city pitch panels, partner pitch mode (`?partner=`).

Run these once Claude Code lands the render pass (items 1–4 of `BRIEF-FOR-CLAUDE-pitch-panels.md`).

## A. Route-label correctness (data already live)
1. Hover/click 15 routes across MENA + SEA. **PASS** = origin→destination reads as clean names,
   no underscores, no raw slugs, no "Bp 643f1f62a7". Spot-check the old offenders:
   Salalah→Hasik, Jeddah→Shura, Doha→Lusail/Pearl, Dubai→Sir Bani Yas.
2. Every Quanta-LR (amber) route reads City → City (or City → Destination (Region)). Flag any that
   still end "in the middle of nowhere".

## B. Rich city panel (pitch synthesis)
3. Click **Dubai**, **Abu Dhabi**, **Singapore**. **PASS** = panel shows: hook/tagline, demand
   signals, use-cases badged by archetype, Navier-fit (Pioneer II + Quanta-LR), signature routes,
   transit-planning angle. Reads like a fast "why Navier here" for a partner.
4. As a *Grab user* persona: open `?partner=grab`, click Singapore/Bali/Phuket — does the panel
   lead with the super-app/cross-border angle (partner overlay)? As a *Dubai RTA* persona:
   `?partner=dubai-rta`, click Dubai — does it lead with the public-transit angle?

## C. Partner pitch mode + phase carousel (the core)
5. `?partner=grab`: panel becomes a pitch doc (hero + why-now + phase carousel). Step phases 1→2→3.
   **PASS** = each step (a) flies the camera, (b) lights only that phase's cities/routes & dims the
   rest, (c) swaps narrative + KPIs. Phase 1 = Singapore/5 boats/3 routes; Phase 2 = full SG + Riau;
   Phase 3 = adds Bali + Phuket. Confirm it reads as a phased rollout a partner could present.
6. `?partner=dubai-rta`: same check (Creek pilot → full inner Dubai → Dubai↔Abu Dhabi corridor).
7. Deep-link a specific phase (if Claude adds `#phase=N`) and reload — does it restore?

## D. Regression guard
8. Flagship labels (Doha/Dubai/Abu Dhabi/Muscat/Singapore) don't stack at world view (collision-thin
   must hold; Singapore always labelled).
9. Routes still render (F-01 stays fixed). No console layer-validation errors.
10. Cold-load time acceptable; panels don't blanket the map on first load.

## Report format
Per check: PASS / FAIL + 1-line note + screenshot. File anything broken as `[RENDER]` (Claude Code)
or `[DATA]` (Tasklet). Verdict per market: is the pitch flow partner-ready?
