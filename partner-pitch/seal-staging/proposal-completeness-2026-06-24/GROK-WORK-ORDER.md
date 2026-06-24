# GROK WORK ORDER — Proposal completeness: mint → handback → complete

**Date:** 2026-06-24 · **From:** Tasklet · **For:** Grok
**Companion:** `PROPOSAL-COMPLETENESS-AUDIT.md` (the diagnosis) · `PROPOSAL-AUDIT.json` (machine-readable)
**Related open PR:** #93 (Curaçao/Ocean Whisperer + Caribbean seal package)

## The loop we are closing
**Grok mints corridor geometry → hands back to Tasklet → Tasklet completes economics (cascade → TAM
ladder) + reconciles narrative → Grok reseals deck/map.** Today both ends are open: corridors are
largely un-minted (census / cluster-dots / null-route journeys), and 36 of 58 proposal files have no
growth ladder. This work order sequences the fix.

## Hard gates (every phase)
- **0 silent drops**, 0 land-crossings, ID-based matching only, **null beats confidently-wrong**.
- Per-partner census/rollup — no shared global census; no two partners share a TAM.
- **Hand back to Tasklet after each phase's mint batch** (this is the missing return leg). Tasklet then
  cascades the ladder on the real `route_id`s and reconciles the narrative.

---

## PRIORITY 1 — Curaçao / Ocean Whisperer  *(active; see PR #93)*
**Grok:** seal the geometry per `GROK-PROMPT.md` in PR #93 — split the lumped
`aruba-curacao-bonaire` node into 3 island nodes, mint/ID-match BPs (Curaçao sealed once, shared by both
the Ocean Whisperer captive view and the Caribbean network view), build routes + water gates, bind
`route_id`s, retire the old `caribbean-mobility` stub.
**Handback → Tasklet:** cascade ladders (Ocean Whisperer $1M captive-rising at 0.55 capture; Caribbean
$900K network) on the minted routes; ship sheets + tracker + economics sidecar.

## PRIORITY 2 — Grab Thailand
**Symptom:** 52 `journeys_unlocked`, only **3 minted** (52/3); Thailand corridors mostly un-minted.
**Grok:** mint the Thai water corridors behind the 49 null-route legs (bind `route_id`s), promote the
Thailand footprint from cluster-dots to geometry.
**Handback → Tasklet:** reconcile `journeys_unlocked` to minted routes (drop/flag any that can't be
built), refresh economics.

## PRIORITY 3 — Bolt markets  *(curated to 12 — see `BOLT-UAE-GRADE-GAPS.md`)*
**Curation applied this PR:** Bolt cut from 18 sub-proposals to **12 shown / 6 hidden**, every kept
market to be brought to **UAE grade**. New per-market fields `display_order` (1–12) and `hidden:true`;
**renderer must sort by `display_order` and drop `hidden`.** Shown order: Croatia, France-Riviera, East
Africa, Estonia, Greece, Italy, Nigeria, Qatar, Saudi Arabia, Spain, Thailand, UAE. Hidden: egypt,
finland, ireland, portugal, south-africa, sweden. KSA label cleaned ("(commercial)" dropped); `id`/
`slug` kept stable (referenced by yango + crosswalk).
**Grok:**
- **Mint the 38 unbuilt legs across the 12 kept markets** (full leg list in `BOLT-UAE-GRADE-GAPS.md`);
  promote kept-market cities from cluster_dots → `map_promote` geometry.
- **Validate the 3 cross-border water gates** — Dubrovnik↔Kotor (ME), Rhodes↔Marmaris (TR),
  Tarifa↔Tangier (MA). Mint only on a clean gate; else seasonal/aspirational — **null beats
  confidently-wrong**. Leave Lebanon **held**.
- **Fix the 3 data bugs:** (a) floor rounding — $1.54M must not display "$2M"; (b) stale
  `source_rollup: careem-aggregate.json` → Bolt's own rollup; (c) regenerate the ladder so
  network/SAM rungs rest on minted (sourced) corridors, not the 341 shared census.
**Handback → Tasklet:** cascade the ladder on minted `route_id`s; **author East Africa to UAE parity**
(only 2 journeys + missing 9/12 narrative fields today); reconcile the rest; refresh economics. Then
**Grok reseals** the Bolt page/map honoring `display_order` + `hidden`.

## PRIORITY 4 — Minor Hotels
**Symptom:** **80 `journeys_unlocked`, 0 minted** — entirely aspirational geometry.
**Grok:** mint the Phase-1 scope first — **UAE + Thailand + Maldives** (coastal/resort-first, include
waterfront NH outliers and under-construction assets per the Minor scope), bind `route_id`s.
**Handback → Tasklet:** author the growth ladder (hospitality **$1M/vessel**, Cost · Convenience ·
Comfort framing), reconcile narrative, ship sidecar.

## PRIORITY 5 — The rest
1. **India ride-hail dedupe** — adani-ports and reliance-industries are **byte-identical**; ola/rapido/
   uber-india within ~1%. Give each a partner-specific census so TAMs differentiate (Kolkata + Chennai
   in scope; high-value consumer markets only; Priority B out of scope).
2. **The 36 no-ladder proposals** — after corridor minting, Tasklet cascades ladders for the real
   partner decks (hospitality: aman, six-senses, four-seasons, soneva, discovery-land, crown-champa,
   sun-siyam, villa-hotels, indian-ocean-luxury; mobility: lyft, didi, gojek, kakao-mobility, line,
   cabify, indrive, freenow, yango[held], dubai-rta, d-marin). Leave genuine territory leads as-is.
3. **Remaining cluster-dots / null journeys** — indrive (12), uber (11), freenow (4), didi (3), and the
   all-unbuilt tail (cote-dazur, d-marin, discovery-land, french-polynesia, red-sea-global).

---
*Counts read directly from partner JSONs; no numbers hand-edited. Ladder regeneration + corridor minting
stay in Grok's deterministic lane — Tasklet supplies guardrails, specs, and completes the cascade after
each handback.*
