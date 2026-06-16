# CHANGELOG — UAE/Careem economics-sidecar reseal (Gold #79af) — 2026-06-16

**Bite:** navier-uae-econ-cascade 4c-reseal · **Base:** #79ae (5198 routes) · **Type:** SIDECAR-ONLY reseal (no geometry change).

## What changed
- `economics_by_route_id.json` refreshed to reflect the recalibrated UAE/Careem economics authored in bites 4a/4b
  (corridors.json rebuilt: `uae-careem` 17 + `uae-luxury` 18; aggregate + growth re-run; new careem-aggregate.json current).
- **Careem partner records regenerated** from the recal `model/corridors.json` + new `careem-aggregate.json`
  against #79ae gold ROUTES (ID-based resolution only): **35 UAE corridors → 32 route-pinned records**
  (11 grounded / 21 estimated; 3 Quanta-LR/cross-border held out, not binding failures).
- **Non-careem partners carried byte-identical** from #79ae (grab 25 / jih-global 33 / qatar 3 /
  red-sea-global 2 / saudi-redsea-pif 4) — avoids stale-aggregate regression per LB-199/LB-201
  (qatar/grab/saudi aggregates are not on disk under the in-tree naming, so a full rebuild would
  drop them; splice preserves them exactly).

## Record-set delta vs #79ae
- records: **78 → 99** (+21 net; careem 11 → 32; all other partners unchanged)
- pending_route_pin: **48 → 45** (careem 3 → 0 binding failures; grab 45 carried)
- $600K/vessel capex confirmed on every careem record (depreciation $30,000/yr × 20yr).
- New UAE route IDs now carry economics, incl. rn-42aa1791bb60, rn-dd4500aa99f5, rn-a5ac4f587aee,
  rn-01b4a3efaf0f + the Abu Dhabi island set (Lulu rn-4d0113ef1fd5, Reem rn-4a56839963b5,
  Sir Bani Yas rn-08f29522c5f2, etc.).

## Geometry
- ROUTES unchanged: **5198** (LB-175a verified pre-seal). FEATURES/CLUSTERS content byte-stable.
- SEAL recomputed on actual blob bytes (LB-171); meta.gold 79ae → **79af**.

## Market-rollup (careem-aggregate, for reference — not a sidecar field)
- Grounded floor: **4 boats · $3,759,500/yr · 303.7 t CO₂/yr** (uae-careem 3/$2.41M · uae-luxury 1/$1.35M).
- Per-corridor sidecar vessels_10pct=0 by design: UAE fleet is network_sum (each <1-boat leg rounds once
  at the market rollup, not per-corridor — L-UAE-ECON-1).
