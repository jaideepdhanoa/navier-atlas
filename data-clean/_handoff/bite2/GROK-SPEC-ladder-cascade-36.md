# Grok spec — economics cascade for 36 no-ladder partner proposals

**Owner:** Grok (deterministic model→ladder generation is Grok's lane).
**Tasklet half (done):** grounded readiness worklist + this spec + post-generation sheet/tracker cascade + QA.
**Worklist data:** `data-clean/_handoff/bite2/LADDER-CASCADE-WORKLIST.json` (36 partners, readiness flags, ladder_type, priority order).

## Problem
36 partner proposals render full narrative but carry **no `growth_case`** — qualitative pitch, no quantified scale. All 36 already have **minted route_ids**, so nothing is blocked on geometry. 6 already carry a partial `_economics_cascade` to assemble (do not re-derive from scratch).

## Two ladder types — DO NOT mix
1. **`mobility_ladder` (23 partners)** — full economics object on minted route_ids:
   `revenue_potential`, `marine_mobility_tam` (+ split provenance), `journey_gmv`, `ladder_transitions`, `vessel_sizing`, `phase_economics`. Same shape as the gold `grab.json` / `uber-india.json` `growth_case`.
2. **`hospitality_unit_econ` (13 partners)** — hospitality doctrine: **$1M/vessel** frame + **one marquee-corridor unit-economics example**. **NO SOM/SAM/TAM ladder.** Cost · Convenience · Comfort framing. Mirror the Centara/Minor sealed-sidecar pattern (per-corridor unit econ + CO₂), not a mobility TAM ladder.

## Priority (high-value consumer first)
`lyft, yango, didi, gojek, six-senses, aman, four-seasons, indrive, kakao-mobility, line, cabify, freenow` → then remaining mobility → then remaining hospitality.
**Hold:** `crown-champa, sun-siyam, universal-enterprises, villa-hotels` are deferred to Bite 8 (Maldives consolidation) — **do not ladder** until their structure is decided.

## Rules
- Ladders bind to **minted route_ids only** (ID-based; null beats confidently-wrong). If a rung has no real corridor, leave null — do not invent.
- Plain-English partner-facing copy; recognized labels SOM/SAM/TAM/GMV may appear only as labels with plain-English descriptors. No internal model/finance taxonomy in titles/subtitles/captions.
- Cascade each result through the transparent economics sheet + master tracker (wire `economics_url`).
- Money formatting: sub-$10M one decimal (see Bolt money-rounding bug).

## Handback required (no self-certification)
Branch name · PR link · commit SHA · exact files changed · validation receipt (per-partner: growth_case present, route_ids bound, sheet+tracker rows written) · explicit nulls/held items (which rungs/partners left null and why). No line-range audits.

## Tasklet will then
QA the handback, confirm sheet/tracker wiring, and fold the 12 high-value results into proposal pages first.
