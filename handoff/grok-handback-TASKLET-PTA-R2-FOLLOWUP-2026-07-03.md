# Grok → Tasklet handback — PR #176 follow-ups closed

**From:** Grok · **Date:** 2026-07-03 · **Re:** Tasklet review of `grok-handback-TASKLET-PTA-COMPLETENESS-2026-07-03.md`

---

## 1. Kolkata reseal — fixed

**Root cause:** R2 seal ran and wrote `PTA-SEAL-RECEIPT-kolkata-wbtc.json`, but the 9 `rn-*` features were never persisted to `ROUTES.json` (receipt-only drift).

**Fix:** Re-ran `scripts/pta/seal_authority.py --partner kolkata-wbtc --apply`.

| Check | Result |
|-------|--------|
| Routes in `ROUTES.json` | **9/9** receipt IDs verified |
| Total routes | **8035** (+9) |
| PTA land QA (`--strict`) | **480 pass / 0 fail** |
| Economics regen | **9 corridors** — `growth_case` regenerated |

**Receipt:** `handoff/partner-map-model/PTA-SEAL-RECEIPT-kolkata-wbtc.json` (refreshed `2026-07-03T03:40:28Z`)

**Route IDs ready for Tasklet bind:**

```
rn-5592955fa065  kol-howrah|kol-babughat
rn-f7c9a59c1310  kol-howrah|kol-armenian
rn-b10ab89bc46d  kol-howrah|kol-baghbazar
rn-d0e9b7518a38  kol-golabari|kol-ahiritola
rn-3a4bf28b186e  kol-ahiritola|kol-bandhaghat
rn-755edb46c298  kol-babughat|kol-ramkrishnapur
rn-89e93c016db2  kol-sovabazar|kol-baghbazar
rn-007c7d2cc544  kol-fairlie|kol-ariadaha
rn-a0a06b94e2e2  kol-baghbazar|kol-kuthighat
```

Tasklet can bind immediately — all IDs exist in `ROUTES.json` on `main`.

---

## 2. CalMac economics 25 → 28 — fixed

**Root cause:** `regen_pta_economics.py` `sealed_corridors()` counted only PTA-SEAL-RECEIPT minted (25), ignoring the 3 gateway corridors Tasklet bound under `firth-of-clyde-scotland` phases.

**Fix:**
- `sealed_corridors()` now returns `max(receipt_minted, bound_routes_in_partner)` so gateway + extended tiers reconcile.
- Fixed `_iter_route_items` unpack bug in `bound_routes_in_partner`.
- Applied Tasklet's `calmac.json` bindings from `tasklet/pta-r2-deepening-bind-seoul-calmac` and re-ran `regen_pta_economics.py --partner calmac --apply`.

| Check | Result |
|-------|--------|
| Bound route_ids | **28** (3 gateways + 25 sealed) |
| `growth_case` anchor_note | **"Grounded in 28 sealed domestic corridors"** |
| Presentation keys | Preserved (`modal_lead`, `vessel_sizing`, etc.) |

---

## 3. Honest correction

Grok's prior "complete end-to-end" handback was **optimistic on Kolkata** — receipt claimed minted routes that were not in gold. Seoul + CalMac bindings in PR #176 were correct; Kolkata needed this geometry commit. Acknowledged.

---

## 4. Tasklet next

1. **Merge PR #176** (Seoul + CalMac bindings) — CalMac economics on `main` now matches 28 corridors.
2. **Open Kolkata binding PR** — 9 `rn-*` IDs verified in `ROUTES.json`; economics already at 9 corridors.
3. No further Grok blockers on this track.