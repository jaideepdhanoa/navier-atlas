# Finance-corridor inheritance contract — TAM-ladder corridors (all partners, all markets)

**Owner:** Tasklet (contract + corridor-set discipline) → Grok (cascade + gate at model build).
**Date:** 2026-07-05 · **Applies to:** `finance/model/corridors.json` and every partner's growth_case / TAM ladder.
**Trigger:** Jaideep — "ensure we have the correct inheritance contracts for financial economics corridors as well… which corridors in which markets are being used by which partners for their TAM ladders."

## The finding (measured — `FINANCE-CORRIDOR-AUDIT.json`)
`finance/model/corridors.json` holds **84 market keys**, one per `{partner}-{geography}`, each with its own `corridors[]` (route_id + `L3_locals` demand + vessel + archetype) that feed that partner's TAM ladder. Across **66 distinct geographies, 13 are covered by 2+ partners** — and the corridor sets **diverge**, exactly like the map layer:

| Geography | Partners | route_id union | common to all | identical? |
|---|---|---|---|---|
| **UAE** | careem(39) · bolt(37) · yango(37) · noon(12) | 122 | **0** | ✗ |
| Qatar | qatar · bolt · yango | 21 | 3 | ✗ |
| Egypt | bolt · yango | 2 | 0 | ✗ |
| Morocco | yango · yassir | 5 | 0 | ✗ |
| Tunisia | yango · yassir | 1 | 0 | ✗ |
| gulf-authority | rakta · bahrain-motc | 51 | 3 | ✗ |
| **India (Kolkata/Chennai/Mumbai/Goa/Kerala/Andaman)** | rapido · ola · uber-india | — | **all** | **✓** |

**UAE's four partners share ZERO of 122 route_ids** — four different corridor sets → four different TAM ladders for the same water. India (Ola/Rapido/uber-india) is already **identical** — proof standardization works and is the target state.

## The principle (finance-specific nuance)
Split every finance corridor into two parts:

1. **Corridor spine (WHICH corridors exist in a market)** — the `route_id` set, endpoints, distance, `cluster_id`. **This is geography and MUST be inherited**, identical to the map layer: `finance_corridor_set(partner, market) == global_canonical ∩ partner.clusters`. A partner's TAM ladder may not be built on a corridor that isn't in the shared geometry, and may not omit one that is.
2. **Economics overlay (the NUMBERS on each corridor)** — `L3_locals` demand, `capture_rate`, `archetype`, `vessel`, `fleet_basis`, pool. **These MAY legitimately differ per partner** — a super_app (Careem 10% gross capture) captures differently than a ride-hail or a captive operator. Divergence here is correct and expected.

So the rule is: **shared corridor spine, partner-specific economics overlay.** Same OD pairs for everyone in a market; different demand/capture per partner is fine.

## Rules (do / don't)
- **DO** derive each partner-market's corridor spine from the same canonical geometry that the map inherits (one `cluster_id`-tagged global set).
- **DO** keep per-partner `L3_locals` / capture / archetype / fleet_basis as an economics overlay keyed by `route_id`.
- **DON'T** let two partners in the same geography carry different `route_id` sets. (Today: UAE 0/122 common — must go to 122/122.)
- **DON'T** invent an L3 demand number (existing rule) — null beats wrong; Grok cascades.
- **DON'T** create partner/region catch-all `rollup` market keys (already banned by the registry `_doc`).

## Registry hygiene (fix in the same pass)
- **Key naming:** enforce one canonical `{geography}` token. Audit found duplicate geos **`mumbai` vs `india-mumbai`** — collapse to one.
- **UAE:** the five keys (`uae-careem`, `bolt-uae`, `yango-uae`, `uae-noon`, `uae-luxury`) must all draw the **same** UAE corridor spine (from the consolidated canonical UAE set in the geometry pass), differing only in the economics overlay. `uae-luxury` is a distinct archetype overlay, not a distinct geography.

## Gate
`validate_finance_inheritance.py` (Grok, runs at model build): for every geography covered by 2+ partners, assert the `route_id` **spine** sets are identical (allowing the economics overlay to differ). FAIL the model build on spine divergence. Order by contention: UAE → Qatar → gulf-authority → Egypt/Morocco/Tunisia (India already passes).

## Ownership
Tasklet owns the shared corridor spine (sourced in `finance/model/corridors.json` L3 lane) and this contract. Grok runs the cascade, applies the overlay, and enforces the gate. This is the finance twin of the geometry `corridor-inheritance` contract — same principle (corridor belongs to geography), one added degree of freedom (economics overlay per partner).
