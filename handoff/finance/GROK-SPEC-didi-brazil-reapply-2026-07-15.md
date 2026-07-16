# GROK re-apply spec — DiDi Brazil live deck (post-PR #279)

**Deck:** `1OixKrHjQbWu0Plkvj-57SQyTFxPL5Ii8l3K6Q9umJOk` — "DiDi × Navier — Brazil mobility review" (12 slides, live).
**Why:** The live deck was applied 2026-07-15 04:53 UTC, ~15h **before** PR #279 merged (20:03 UTC). It therefore carries pre-mid ($18 floor) economics and pre-#279 orphan economics objects on the held city slides. The deterministic source of truth is now correct on `main`; this is a re-apply, not a rebuild.

## Canonical sources (main)
- `deck-studio/decks/didi-brazil/generated-deck-economics.json` (mid basis — authoritative)
- `deck-studio/decks/didi-brazil/deck.editplan.json` (corrected in this PR: slide-3 `$23.4M` → `$36.4M`)
- Structure locked by `content-source.json`: 1 cover · 2 why · 3 market overview · 4 Rio · 5 Angra (HELD) · 6 Florianópolis (HELD) · 7 one-route economics (Arariboia) · 8 floor-not-ceiling · 9 integration · 10 rollout · 11 ask · 12 close.

## Defect map (object IDs read live 2026-07-15)

### Slide 3 — market overview (repaint to mid)
- KPI/body currently read `$23.4M` → **`$36.4M`** (supported annual route revenue). 113 vessels / 4 routes unchanged. Source: `country_total.annual_revenue_usd = 36,407,526`.

### Slide 4 — Rio de Janeiro (city deep-dive; marquee routes gap)
- Route box `g3eec5122801_0_114` lists ONLY "Praça XV → Arariboia … Economics on the next slide". Per the locked pattern the Rio city slide must show the **four marquee corridors with distances/descriptions** (canonical route-list format, amber ▸, no vessel names):
  - Praça XV → Arariboia — ~2.7 nm · cross-bay commuter connection to Niterói
  - Praça XV → Charitas — ~4.4 nm · fast crossing to the Charitas waterfront
  - Praça XV → Cocotá — ~6.0 nm · city-to-island link to Ilha do Governador
  - Praça XV → Paquetá — ~9.2 nm · longer bay crossing to car-free Paquetá Island
  (distances/descs from `economics_routes[]` in generated-deck-economics.json)

### Slide 5 — Angra dos Reis (HELD-NULL — remove economics debris)
- DELETE orphan economics objects (pre-#279 leftovers that contradict held status):
  - `didibrazil_etx1` (full ROUTE ECONOMICS P&L panel, stale $18 / $19.4M / $23.4M)
  - `g3eec5122801_0_395` ("Praça XV → Arariboia" label — wrong city)
  - `g3eec5122801_0_397` ("$19,469,224 annual route revenue · 92 vessels supported")
- Keep title `_392`, held body `_394`, map image `_443`. Slide must show NO economics (hold text: "Route-level passenger demand and fares are under local review; economics remain blank until confirmed.").

### Slide 6 — Florianópolis (HELD-NULL — fix Rio route debris)
- Route box `g3eec5122801_0_209` currently shows "Praça XV → Charitas" (a Rio route). Florianópolis has no sourced routes → remove the Rio route box (or replace with a neutral "crossings mapped; demand under review" hold consistent with slide 5). No Rio corridor may appear on the Florianópolis slide.

### Slide 7 — one-route economics: Praça XV → Arariboia (repaint to mid)
- Body `g3eec5122801_0_300` currently: "$18 · ~8,136 pax · Revenue $146,448 · run cost $79,094 · EBITDA $67,354 · margin 46% · payback 8.91 years" → repaint to MID:
  - one-way fare **$28** · **~11,757** passengers/boat/yr
  - Revenue/boat **$329,190** · run cost **$79,257** · EBITDA **$249,933** · margin **76%** · payback **2.4 years**
- Remove stray leftover objects `g3eec5122801_0_301` ("serving Ilha do Governador" — Cocotá text) and reconcile route box `g3eec5122801_0_304` ("→ Cocotá … On the next slide") to the Arariboia route shown on this slide.
- Six flush OPEX lines per canonical rule (Energy $1,057 · Crew $25,200 · Marina+overhead $10,000 · Maintenance $10,000 · Insurance $15,000 · Charging berth $18,000 → total run cost $79,257).

### Slide 8 — floor not ceiling (repaint to mid)
- `$23.4M` → **`$36.4M`** (`tam.rungs[0] = 36,407,526`). Addressable rung `$367.5M` (`tam.rungs[1] = 367,461,220`). 113 vessels / 4 routes.

### Speaker notes — scrub reference-deck leftovers (all internal + wrong-market)
Remove/replace on slides 3–8:
- S3 notes: "…the whole SEA water network Grab could run … Grab growth-case (35 corridors; M_today $398M)."
- S4 notes: "Singapore shown as a whole market … Corridors + distances from the Grab aggregate (master)."
- S5 notes: "…Grab aggregate MID band … Phuket revenue carries … integer-seat rounding vs sheet."
- S6 notes: "Bali shown as a whole market…"
- S7 notes: "Phuket shown as a whole market."
- S8 notes: "…grab-growth-case.json … SOM_full_network $194.9M; SAM_navier $877.2M; TAM_marine $3.51B…"
No Grab / Singapore / Phuket / Bali / SEA references may remain anywhere in the deck (notes included).

## Gates before seal
- `python3 deck-studio/qa/partner_copy_lint.py didi-brazil` green (blocking).
- `python3 scripts/audit_partner_copy.py` PASS on any touched partner copy.
- Atlas screenshot slots: **human insertion only** — do not populate.
- Read object IDs live per slide before edit (IDs above verified 2026-07-15 but re-read before mutate).
- Return QA receipt: deck id, slide count (12), per-slide econ/KPI values, held-slide blank confirmation, notes-scrub confirmation, no-op replay.

## After DiDi Brazil proof confirmed
Cascade identical pattern to DiDi Mexico (13-slide), inDrive Brazil (inherits Brazil corridors), inDrive Egypt (two-anchor). Then delete legacy decks and repoint configs/manifests.
