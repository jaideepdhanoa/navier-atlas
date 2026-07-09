# DiDi Ex-China — Execution Handoff

**Authorized:** Jaideep, 9 July 2026  
**Current status:** `research-needed / scope-repair-needed`  
**Mainland China:** excluded

## What this package contains

- Verified ex-China operating-footprint inventory and scope ledger.
- Current Atlas coverage audits.
- P0 no-shrink baseline and exact anchor-city crosswalk.
- Route-stamp defect ledger for all 14 involved existing clusters.
- Full execution and handback specification.
- Mexico Pacific and Caribbean BP/brief research.
- Mexico demand/fare source research.
- Chile/Argentina registry-gap research.

## Phase-1 findings

- 17 target full sub-proposals across 16 jurisdictions.
- 40 existing city IDs approved for immediate scope treatment.
- Taiwan's two city IDs remain behind a current-operation verification gate.
- Macau is held because its shared cluster must not create an unsupported DiDi claim.
- Chile and Argentina require new registry hierarchy and real BP geometry.
- 77 definite foreign route stamps exist in target clusters:
  - Mexico: 21.
  - Galápagos: 46.
  - New Zealand: 10.
- Three one-endpoint routes need legitimate trunk/cross-border review, not automatic deletion.
- Mexico research now includes two strong 2025 ferry-demand anchors:
  - Puerto Juárez–Isla Mujeres: about 5.46M passenger movements.
  - Playa del Carmen–Cozumel: about 3.85M passenger movements and 27,920 departures.
- These counts are not yet model-ready: directional splits, realized fare mix, accepted BP coordinates and current route seal remain required.

## Immediate execution order

1. Execute G0 scope repair from the no-shrink baseline and crosswalk.
2. Execute G1 global route-stamp hygiene; return changed route IDs and all inheritance gates.
3. Resolve the Mexico Caribbean terminal/BP conflicts and seal Mexico routes globally.
4. Return the current Mexico route-ID spine so Tasklet can bind sourced demand and fares.
5. Do not run a DiDi economics cascade from stale route IDs, the catch-all `didi` key, or Grab's census.

## Hard gates

- Null beats wrong.
- Corridors belong to geography and inherit 1:1.
- Finance route-ID spine must be identical across partners in each shared market.
- No silent BP drops.
- No invented demand, fares, piers or route IDs.
- No mainland-China, Macau or Taiwan overclaim.
- Partner-facing copy must pass Gate G.

Read `GROK-SPEC-didi-ex-china-grand-slam-2026-07-09.md` for the complete baton-pass sequence and acceptance receipts.
