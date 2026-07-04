# Grok → Tasklet handback — Yango finance refresh (PR #180)

**From:** Grok · **Date:** 2026-07-04 · **Status:** Grok lane closed — Yango sheet published  
**PR:** [#180](https://github.com/jaideepdhanoa/navier-atlas/pull/180) merged `41913c71`  
**Spec:** `handoff/partner-map-model/yango-roster-correction/GROK-SPEC-yango-finance-refresh-2026-07-03.md`

---

## 1. Executive summary

Merged Tasklet's finance-registry reconciliation + Peru/Colombia L3 + four roll-up markets. Ran full Yango cascade and republished the transparent sheet + master tracker. Rebound `growth_case` and `economics_by_route_id` from `finance/recal/agg-yango.json`.

| Gate | Before (#179 seal) | After (#180 cascade) |
|------|-------------------|----------------------|
| Finance markets (Yango) | stale (incl. Turkey/Tunisia/…) | **11** reconciled |
| Registry corridors | 167 (stale rollup) | **117** (near-term Pioneer) |
| Grounded corridors | 73 | **23** |
| Grounded floor rev | ~$101M/yr | **~$24.6M/yr** (honest re-rollup) |
| Peru + Colombia in sheet | absent | **present** |
| Roll-ups in sheet | absent | Namibia · Venezuela · Cameroon · Congo |
| Stale markets in registry | 6 | **dropped** |

---

## 2. Published artifacts

| Artifact | URL / path |
|----------|------------|
| Yango transparent sheet | https://docs.google.com/spreadsheets/d/1fvB_tc8IWUTlKMWjPcoJde_uPnGKVqoCxxsgd5IL1rM/edit |
| Master tracker | https://docs.google.com/spreadsheets/d/1q80EzTowmY8tUuGg1z5TsTatjMru5xWW1XcIhV-E0Ko/edit |
| Agg rollup | `finance/recal/agg-yango.json` |
| Scoped corridors view | `finance/recal/corridors-yango.json` |

---

## 3. Lane executed

```bash
git merge origin/tasklet/yango-finance-refresh   # 41913c71
RUN_CASCADE=1 PARTNERS=yango ./scripts/grok-econ-reseal/run_finance_sheet_lane.sh
python3 scripts/grok-bolt-yango/bind_yango_growth_case.py --dc data-clean --aggdir finance/recal
python3 scripts/grok-bolt-yango/build_economics_sidecar.py --dc data-clean --corridors finance/model/corridors.json
python3 scripts/grok-econ-reseal/update_seal_hashes.py
```

`route_id` bind on the 22 new finance corridors (11 Peru/Colombia + 11 roll-ups) deferred — all carry `route_id: null` in registry; geometry binds from #178/#179 seals are on partner surface, not yet wired into finance rows. Next bite if desired.

---

## 4. DiDi Colombia — not executed (scope hold)

Per `CROSS-PARTNER-COVERAGE-MATRIX-2026-07-04.md`: Cartagena L3 is reusable, but **`didi-colombia` finance block not instantiated** — Tasklet staged sourcing only; DiDi has no `PARTNER-SHEET-IDS` entry and no transparent-sheet universe today. Recommend Jaideep greenlight before Grok copies `yango-colombia` L3 → `didi-colombia` + cascade.

**Held (null beats wrong):** Uber, inDrive — aspirational nodes only.

---

*Grok lane closed for Yango finance. Sheet live; partner JSON rebound from fresh agg.*