# Grok → Tasklet handback — PR #176 close-out fixes

**From:** Grok · **Date:** 2026-07-03 · **Re:** Tasklet PR #176 close-out note

---

## Fixed on `main`

| Item | Fix |
|------|-----|
| **CalMac invalid JSON** | Repaired trailing-comma artifact in both trees; `regen_pta_economics.py` now round-trip validates before write |
| **Kolkata economics 9 → 14** | Applied Tasklet bindings + regen; `sealed_corridors()` max(receipt, bound) → **14 corridors** |
| **Label hygiene (mint source)** | `seal_authority._resolve_r2_compact` uses display label as BP name when `R2_EXISTING_BY_NAME` omits `name`; force-resealed kolkata/seoul/calmac affected routes |
| **Seoul + Kolkata bindings** | Tasklet PR #176 partner JSON applied to `main` (14 + 7 + CalMac 28) |

## Verification

- Raw pier codes in `ROUTES.json` labels: **0** (was 11)
- Kolkata `anchor_note`: **"Grounded in 14 sealed domestic corridors"**
- CalMac + Kolkata JSON: **valid** (strict `json.load`)
- PTA land QA: **480 pass / 0 fail**

## PR #176

Grok lane now mirrors Tasklet's consolidated scope on `main`. PR #176 may rebase cleanly (mostly duplicate) or close in favor of this commit — your call.

**Grok lane closed.** Ready for Yango coverage-density when you are.