# Grok G4 — DiDi Brazil T3 + Mexico Punta Sam residual

**UTC:** 2026-07-10T06:00:39Z  
**Git commit:** `dd51975caa69`  
**Status:** `g4-complete`  
**Upstream:** PR #213 merge `f43420eb`

## Sidecar

- Records total: 232 (added 4, updated 8)
- DiDi agg rows joined: 12

### Joined IDs

- `rn-1886629dbf0c` — grounded — rev 19469224.0 — fare 18.0
- `rn-80f0d0ebe0bd` — grounded — rev 1481354.0 — fare 18.0
- `rn-369ef0eb69d9` — grounded — rev 423244.0 — fare 18.0
- `rn-00bb6ded4be5` — grounded — rev 2031000.0 — fare 18.0
- `ics-413f51cd44` — grounded — rev 8150050.0 — fare 15.07
- `ics-dd1d814699` — grounded — rev 6254760.0 — fare 16.63
- `ics-03e3853317` — estimated — rev None — fare None
- `ics-aa6ff40d2d` — grounded — rev 354350.0 — fare 15.07
- `ics-89a8844858` — estimated — rev None — fare 18.19
- `ics-de6758216f` — estimated — rev None — fare None
- `ics-db0930d9d1` — estimated — rev None — fare None
- `ics-b5861451fb` — estimated — rev None — fare None

## Combined floor (from agg)

- Fleet: **201**
- Floor: **$38,163,982.0**/yr
- Pool: **$386,158,495.0**/yr

- economics_url: https://docs.google.com/spreadsheets/d/1LY0Vp7FskgDDnEixkrEUCH0m-A_pYd2YCNuq3LF8ESM/edit

## Colombia

- Status: **unmaterialized_hold**
- Decision: C — keep DiDi Colombia unmaterialized in finance until route-level demand/fare proof + spine decision
- Only in DiDi featured: ['rn-aa790551baa7']
- Only in yango finance: ['rn-20762e2b40f5', 'rn-3ebf0c9aece2', 'rn-59374c41f8ab', 'rn-74aa778f6655', 'rn-84ffd58e7f82']

## Gates

- **gate_g:** PASS (exit 0)
- **inheritance_strict:** PASS (exit 0)
- **finance_inheritance:** PASS (exit 0)
- **fidelity:** PASS (exit 0)
- **route_linkage:** PASS (exit 0)

Machine: `handoff/didi-ex-china/waves/tasklet-proof/GROK-G4-BRAZIL-MEXICO-T3-RECEIPT-2026-07-10.json`

