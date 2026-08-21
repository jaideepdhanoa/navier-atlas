# Archetype PR stack review — 2026-08-21

**Stack tip reviewed:** `origin/feat/archetype-istanbul-v3` (PR #386, accumulates #367–#385)  
**Base:** `origin/main`  
**Constraint (Jaideep):** Main’s RAK rewrite (4 stops / 1 Coastal Spine line) is intentional. **Do not revert to the stack’s older 7-stop / 4-line RAK geometry.**

---

## Summary

**Do not merge the Graphite stack onto main.** Main has already absorbed (and moved past) the live city rollout. A merge would clobber newer FI demand-pool v3 work, softened standing labels, About/Vessels media wiring, demand-table collapse, and template/build scripts — and would incorrectly restore the discarded RAK multi-line hub.

What remains useful on the stack is mostly **research handoff** under `handoff/archetypes/{city}/` (authority maps, crew/fare/demand notes, geometry receipts) that never landed on main. Treat data/build PRs as **close-as-superseded**; cherry-pick handoff docs only if we want them archived on main.

---

## Stack vs main (merge risk)

| Area | Main | Stack tip | Merge risk |
|---|---|---|---|
| FI `demand_pool` rows | Bay 16, NY 14, Seattle 16, … + soft standing label | Often **0 rows** (Bay/NY) or fewer; standing empty/older | **High — regresses live FI pages** |
| FI template (`archetype.js/css`) | About/Vessels demos, demand expand, service-day cards (Aug 20) | Aug 16 multi-city baseline — **missing** those features | **High — clobbers template** |
| `build-employer-hubs.mjs` | Shared about/vessels inject + soft-split blurbs | Older inject | **High** |
| PP JSON (most cities) | Same blob as stack | Same | Low |
| Istanbul hub lines | IST-1…4 same IDs/names as stack | Same topology | Low for geometry |
| **RAK `hub.json`** | **4 stops / SPN-1 Coastal Spine only** (purposeful rewrite) | 7 stops / MRJ-1, MNA-1, SPN-1, HER-1 | **Do not take stack RAK** |

### RAK (explicit)

Main (keep):

- Stops: `al-marjan`, `royal-yacht-club`, `mina-al-arab`, `qawasim-1`
- Line: `SPN-1` Coastal Spine only

Stack (discard for hub geometry):

- Extra stops: `qawasim-2`, `hilton-corniche`, `jazirat-al-hamra`
- Lines: Resort Shuttle / City Line / Coastal Spine / Heritage Line

Any cherry-pick from #378/#379 must **exclude** `employer-hub/hubs/ras-al-khaimah/hub.json` (and any PP/FI that assume the old four-line graph).

---

## Unique value still on stack

1. **Research packages** only on stack (examples):  
   `handoff/archetypes/{abu-dhabi,bahrain,dubai,istanbul,jeddah,…}/*`, plus  
   `GULF-WAVE2-GEOMETRY-RECEIPT.json`, `ISTANBUL-HUB-GEOMETRY-RECEIPT.json`, `INTERNATIONAL-ADDENDUM.md`, Bay Area authority/crew/revenue notes.
2. **Geometry receipts / mint scripts** — `scripts/mint_istanbul_hub.py`, `scripts/mint_gulf_wave2_hubs.py` + receipts. Archive-only; hubs already live on main.
3. Employer microsite handoff PRs **#349, #353–#358** — handoff specs + node inventories only (no live hub JSON conflict). Safe to merge as docs if still wanted; many cities already have live hubs on main.

### Explicitly NOT unique / do not take

- **RAK multi-line hub** — discarded; main Coastal Spine rewrite wins.
- **Registry entries for bahrain / jeddah / red-sea-global / saudi-eastern-province / istanbul** — stack adds them as `/employers/{city}`, but main correctly treats these as **archetype-only** (PP/FI, no employer microsite). Importing those registry rows would mint broken employer routes.

Main-only (must keep): `handoff/archetypes/demand-pool-v3-2026-08-20/**`.

---

## Template / code delta

Stack tip templates last touched **2026-08-16**; main **2026-08-20+**.  
Feature markers (`renderAboutNavier`, `demand-expand`, vessel soft-split) exist on main only. Merging stack code files would wipe them.

---

## Per-PR recommendation

| PR | Kind | Recommendation |
|---|---|---|
| **#367** template Boston | code | **Close** — superseded by main template evolution |
| **#368–#372, #374** US city data | FI/PP JSON + handoff | **Close as superseded** for JSON; optional cherry-pick city `handoff/archetypes/*` research only |
| **#373, #375** multi-city / SD builds | cumulative code+data | **Close — do not merge** |
| **#376–#378** UAE data | JSON + handoff | **Close** JSON; **exclude RAK hub** if anything is cherry-picked; handoff research OK |
| **#379** Gulf UAE build | cumulative | **Close — do not merge** |
| **#380–#383** Gulf wave-2 data | JSON + handoff | **Close** JSON (already on main); cherry-pick research handoffs if desired |
| **#384** Gulf wave-2 build | cumulative | **Close — do not merge** |
| **#385–#386** Istanbul data/build | JSON + geometry + cumulative | **Close build (#386)**; Istanbul hub already on main with same line IDs; keep geometry receipt/research via cherry-pick if missing |
| **#349, #353–#358** employer hub handoffs | docs/inputs only | **Optional merge** as archival handoff; not blocking; verify no expectation that v1 stop graphs replace live hubs |

---

## Issues

### Issue 1 -- Severity: bug
- File: employer-hub/hubs/bay-area/fleet-investors.json (stack tip)
- Description: Stack Bay FI has **0 demand rows** vs main’s **16** (demand-pool v3). Same class of regression for NY (0 vs 14) and thinner Seattle (9 vs 16). Merging stack FI JSON would blank live demand tables.
- Suggestion: Close data/build PRs without merging FI JSON; never reset main demand pools from this stack.
- Status: open

### Issue 2 -- Severity: bug
- File: employer-hub/template/archetype.js (stack tip vs main)
- Description: Stack template predates About/Vessels media, demand collapse, service-day card revert, soft-split vessels. Merge would remove those behaviors from all archetype pages.
- Suggestion: Close cumulative build PRs (#373/#375/#379/#384/#386); keep main template.
- Status: open

### Issue 3 -- Severity: bug
- File: employer-hub/hubs/ras-al-khaimah/hub.json (stack tip)
- Description: Stack restores discarded 4-line / 7-stop RAK graph. Product direction is main’s single Coastal Spine rewrite.
- Suggestion: **Never cherry-pick or merge stack RAK hub.json.** If importing UAE handoff research, path-exclude this file.
- Status: open

### Issue 4 -- Severity: suggestion
- File: handoff/archetypes/ (stack-only research trees)
- Description: Large set of authority/crew/fare/demand research + geometry receipts never copied to main. Valuable provenance; not required for render.
- Suggestion: Optional follow-up PR: copy `handoff/archetypes/**` research + receipts onto main **without** hub JSON overwrites (and without RAK hub).
- Status: open

### Issue 5 -- Severity: nit
- File: PRs #349, #353–#358
- Description: Employer handoff-only PRs still open after live hubs shipped.
- Suggestion: Merge as docs or close with “superseded by live `/employers/{city}` on main.”
- Status: open
