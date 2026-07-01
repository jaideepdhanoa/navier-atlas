# PTA Economics Convention (v1) — public-value + operating model

The economics frame for **public transport authority** proposals. Replaces the
mobility SOM/SAM/TAM/journey-GMV ladder, which is wrong for an authority: a ministry
does not buy marketplace GMV, it buys public value delivered through a credible
operating model. Analogous to the hospitality `$1M/vessel` convention — a category
gets its own economics language.

**Hard rules**
- **No** SOM / SAM / TAM / GMV / "journey wallet" / "super-app" / "platform take" language, partner-facing.
- **No** internal finance taxonomy partner-facing (no `atom.py`, multipliers, derivations, `_mid (…)` strings).
- Lead with **public value**; revenue is the supporting operating layer.
- Quote the **mid** figure; never headline the optimistic ceiling. Band and label every projected figure.
- Fares, frequencies, and cost-recovery are **"set with the authority"** — never fabricate subsidy numbers.

---

## The three layers

### 1. Public value (the headline — what the authority buys)
Quantified outcomes, tied to the authority's own published targets:
- **Emissions avoided** — t CO₂/yr from zero-emission operation vs the road/diesel alternative; tie to the authority's decarbonization target (Bahrain: −30% by 2035, net-zero 2060).
- **Congestion relieved** — peak road / causeway / bridge trips shifted to water.
- **Time saved** — passenger-minutes vs the congested road alternative.
- **Access widened** — islands, airport, and waterfront communities brought onto the public network (equity).
- **Tourism & waterfront uplift** — a signature, low-impact way to move.

Per-vessel anchor (grounded): each foiling vessel = capacity × service pattern, a grounded CO₂-avoided/yr figure, and N road-trips removed. This is the authority analogue of `$1M/vessel`.

### 2. Operating model (how it pays for itself, credibly)
- **Fare integration** — rides on the authority's existing fare system / app (Bahrain: Masar app).
- **Operating cost** per service-hour, **benchmarked against bus and ferry** the authority already runs.
- **Cost-recovery band** — farebox vs operating cost, expressed as a band, "agreed with the authority." No invented subsidy-per-passenger numbers.

### 3. Network revenue (operating, supporting layer)
Plain-English fare-revenue rungs (transport revenue only — no journey wallet):
- **Operating revenue — starter corridors (today's demand)** — grounded floor.
- **Operating revenue — full archipelago/metro network** — width step, same ridership assumption.
- **Operating revenue — mature network** — better boats grow ridership; well-run network carries more of it.
- **Total water-transport market (addressable)** — the full market the network can serve (optional top rung; replaces "TAM").

Horizons stay **maturity-honest** but drop the formulaic verbs: **Starter service → Full network → Mature network** (not Prove/Scale/Mature). Geography-led phasing (today's corridors → full archipelago → cross-region links) lives in the story `phases`, not here — do not duplicate.

---

## Render mapping (current front-end)
Uses the existing `growth_case` block (`_growthCaseHtml`), which is data-driven:
- `revenue_potential.rungs[].label` / `.basis` → plain rung copy (no jargon).
- `phase_economics.horizons[].name` / `.scope` → maturity-honest names.
- `ladder_transitions[]` → keep `headline` + `basis` **plain**; **drop** `derivation` / `multipliers_cited` / `source_fields` (they render as finance jargon).
- `growth_case.public_value` (Tasklet-added) → headline + levers. **Grok front-end TODO:** add a render slot for `public_value` (quantified levers) + a fares/operating-model table; until then it lives in narrative + the levers list.

## Division of labor
- **Tasklet:** plain-English presentation — rung/horizon labels, public-value levers (qualitative), narrative, jargon scrub.
- **Grok:** model regeneration — quantified public-value figures, fares/operating-model numbers, and the `public_value` render slot. Numbers stay in Grok's model lane.

## Status
- **Applied (presentation):** Bahrain MOTC `bahrain-motc.json` — rungs/horizons relabeled, super-app rung dropped, bridges de-jargoned, `public_value` block added.
- **Pending (Grok):** quantified public-value + operating-model numbers after routes seal.
