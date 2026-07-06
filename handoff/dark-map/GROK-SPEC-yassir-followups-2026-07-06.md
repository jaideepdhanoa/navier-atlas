# GROK SPEC — Yassir follow-ups (El Jadida + Senegal/Algeria finance inheritance)
_Tasklet → Grok · 2026-07-06 · owner_next: Grok_

Verified against live tip (75239c1b). Dark-map ✓ 0 null cluster routes. Senegal 12 / Algeria 7 routes render. Two real follow-ups below.

---

## 1 · El Jadida is a distinct city — NOT "likely legitimate" (corrects prior receipt)

Your Morocco re-stamp left **4 legs** whose El Jadida / Mazagan endpoint fell back to `casablanca-morocco` (~102 km nearest anchor). El Jadida is a **genuinely distinct city** ~90–96 km SW of Casablanca (UNESCO Portuguese City of Mazagan, major Atlantic port, Mazagan Beach & Golf Resort). One leg is even self-referential (`rn-4873b929b710` Casablanca→El Jadida, both ends stamped `casablanca-morocco`).

**Affected legs (El Jadida / Mazagan endpoint mis-stamped as `casablanca-morocco`):**
- `rn-7492176da39c` — Rabat → El Jadida (El Jadida end)
- `rn-aacdddb20e68` — Mohammedia → El Jadida (El Jadida end)
- `rn-4873b929b710` — Casablanca → El Jadida (El Jadida end; currently self-referential)
- `rn-ca3c8a1beb62` — Sidi Kaouki → Mazagan Beach & Golf Resort (Mazagan end)

**Action:**
1. Mint an `el-jadida-morocco` anchor + BP(s) from the sourced coords below (verify geometry / land_qa as usual).
2. Re-stamp the 4 El Jadida/Mazagan endpoint sides `casablanca-morocco → el-jadida-morocco`.
3. `el-jadida-morocco` is a member of the `morocco` cluster (keep `cluster_id=morocco`).
4. Brief authored + registered (`data-clean/city_briefs/el-jadida-morocco.json`, `_index.json`).

**Sourced BP coords (verify, don't trust blindly):**
| BP | approx lat, lon | source |
|---|---|---|
| El Jadida fishing/commercial port (below citadel) | 33.256, -8.501 | UNESCO #1058; Wikipedia El Jadida |
| Mazagan Beach & Golf Resort marina (El Haouzia) | 33.363, -8.415 | visitmorocco.com; resort |

Nobody invents a pier — these are real, but confirm exact berth geometry.

---

## 2 · Senegal + Algeria finance inheritance (unblocks economics cascade)

Finance registry (`finance/model/corridors.json`) state today:
- **`yassir-senegal` = MISSING.** But `yango-senegal` exists with **7 richly-sourced L3 corridors** (Dakar⇄Gorée re-anchored to ~800k visitor pool; COSAMA Dakar–Casamance RoPax; pirogue hops; per-seat fares all sourced T2). Per the **finance-corridor inheritance contract**, Yassir must inherit the identical Senegal corridor spine (`route_id` set) with a Yassir-specific overlay only.
- **`yassir-algeria` = 3 corridors**, but the `algeria` atlas cluster now has **7 routes** (post-Annaba mint). Spine is understated → reconcile to the full shared Algeria spine.

**Action (Grok deterministic derivation):**
1. Create `yassir-senegal` mirroring the shared Senegal corridor spine (route_id set = `global_canonical ∩ senegal`), inheriting `yango-senegal`'s L3 demand/fare records 1:1 (shared spine — do not re-source).
2. Reconcile `yassir-algeria` spine 3 → full Algeria set (include the newly minted Annaba corridor(s) that carry route_ids).
3. Yassir overlay across both: `archetype = super_app` (Yassir is a super_app), `capture_rate` per Yassir convention, `fleet_basis` per model. These MAY differ from Yango; the spine MAY NOT.
4. Run `validate_finance_inheritance.py` — spine identity per shared market (Senegal shared with Yango; Algeria shared with Yango/Yassir).
5. Cascade → boats/TAM/growth_case for Yassir Senegal + Algeria (currently null in yassir.json, left for your model lane).

**Do not invent L3.** Senegal + Algeria demand records already exist and are sourced; this is inherit + reconcile + cascade, not re-source.

---

## 3 · Minor data-quality notes (non-blocking)
- `yango-senegal` + `yassir-tunisia` carry some corridors with `route_id=None` (unsealed: COSAMA overnight RoPax, Sfax⇄Kerkennah) — headline L3 present, route_id pending seal.
- `yassir-tunisia` has `rn-74a61d330456` appearing **twice** (Jorf⇄Ajim + a TGM placeholder both bound to it) — dedupe/rebind at next pass.

---

## Acceptance
- `el-jadida-morocco` anchor minted; 4 legs re-stamped; 0 self-referential Morocco routes.
- `yassir-senegal` exists; Senegal + Algeria finance spines pass `validate_finance_inheritance.py`.
- Yassir Senegal + Algeria economics cascade non-null (or honest-pending if any spine leg lacks L3).
