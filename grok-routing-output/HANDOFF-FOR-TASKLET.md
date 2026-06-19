# Grok → Tasklet Mega Handoff — Phase 3 apply (#79al)

**Date:** 2026-06-18 (LB-221 + LB-224 + LB-242)  
**From:** Grok (Jaideep lane)  
**To:** Tasklet  
**BRIEF:** `_review/grok-routing-v2/grok-routing-v2/BRIEF.md`  
**Zip:** `grok-tasklet-mega-handoff-2026-06-18.zip`  
**Target reseal:** #79al (geometry + gate policy; Grok did not touch live `data-clean/` except allowlist artifacts in zip)

---

## Headline

**Strict QA: 27/42 pass** in `route-solutions.jsonl` (`qa_pass: true`, `interior_land_km ≤ 0.05`).

| Tier | Pass / inputs |
|------|---------------|
| `hudayriyat-khalifa-saadiyat` (LB-221) | **7/7** |
| `palm-9-cross-trunk` (LB-208a) | 6/9 |
| `densify-residual-LB-211` | 12/20 |
| `ics-cleanup-LB-225` | 2/6 |

**Live (#79ak) unchanged** until Tasklet apply + reseal.

---

## What changed since morning handoff

1. **LB-221** — Abu Dhabi dredged-channel cutouts in `ad_channel_cutouts.py`; rebuilt `uae_gulf_land_v2.wkb` (132 polys).
2. **LB-224** — `qa_land_crossing.py`: UAE overlay precedence inside bbox; marina apron **0.08 → 0.12 km**; four long coastal Hud hops solved with offshore waypoints.
3. **LB-242** — `route_water_allowlist.json` (4791 allowlisted / 25 denied); `restored-routes-LB-242.json` (3 legit scrubbed routes).

**Superseded:** `route-solutions-candidates.jsonl` (18 pre-strict drafts) — use **`route-solutions.jsonl` rows with `qa_pass: true`** only.

---

## Artifacts in this zip

| Path | Use |
|------|-----|
| `grok-routing-output/route-solutions.jsonl` | **Primary apply input** — 27 geometries + `waypoints_authored` |
| `grok-routing-output/uae_gulf_land_v2.wkb` | Promote to geom-gates bundle |
| `grok-routing-output/seaward-candidates.json` | 35/35 densify-residual seaward coords |
| `grok-routing-output/ad_channel_cutouts.py` | AD channel centerlines + widths |
| `grok-routing-output/build_landmask_v2.py` | Reproducible mask builder |
| `grok-routing-output/solve_routes_phase2.py` | Phase 2 solver (reference) |
| `grok-routing-output/verify_solutions.py` | Official QA runner |
| `grok-routing-output/build_route_water_allowlist.py` | LB-242 allowlist builder |
| `grok-routing-output/restored-routes-LB-242.json` | Merge 3 scrubbed routes back |
| `data-clean/route_water_allowlist.json` | Gate hook — subtract from Tier A/B |
| `data-clean/qa_baseline.json` | Frozen Tier-B baseline |
| `data-clean/SEAL.prior.json` | Frozen Tier-A geom-hash reference |
| `_review/.../code/qa_land_crossing.py` | **LB-224** — promote to canonical pipeline |
| `_ingest/.../pipeline/_tools/qa_land_crossing.py` | CI copy (same patch) |
| `grok-routing-output/LB-221-NOTES.md` | Channel mask notes |
| `grok-routing-output/LB-224-NOTES.md` | Overlay + apron policy |
| `grok-routing-output/LB-242-NOTES.md` | Allowlist math |
| `grok-routing-output/PHASE1-NOTES.md` | Landmask build |
| `grok-routing-output/PHASE2-NOTES.md` | UNSOLVED list (15 rows) |
| `grok-routing-output/synthesize-bp-id-map.json` | **Slug → `bp-*` crosswalk** for 13 passing synthesize rows |
| `grok-routing-output/route-solutions-synthesize-remapped.jsonl` | Same 13 rows with `from_bp_id` / `to_bp_id` |

---

## Synthesize slug → `bp-*` mapping (13 routes)

`route-solutions.jsonl` uses Grok display slugs (`dxb-*`, `ad-*`). Live gold (#79ak) keys boarding points as **`bp-*` only**. Use `synthesize-bp-id-map.json` at apply time.

| Policy | Count | Slugs |
|--------|-------|-------|
| **Exact remap** (0 m) | 14 | All Palm endpoints + Hudayriyat, EP, Yas, Saadiyat Beach/Marina |
| **Remap + snap endpoint** | 2 | `ad-lulu-island` → `bp-31b06c534d` (825 m); `ad-reem-island` → `bp-f47f75836a` (1.4 km) |
| **Mint new `bp-*` first** | 1 | `ad-khalifa-port` — no live node within 3 km |

**Apply order for synthesize rows:**
1. Mint `ad-khalifa-port` using `mint_payload` in map (then 2 Khalifa routes can bind).
2. For Lulu / Reem rows, snap geometry first/last vertex to `live_coords` in map (Grok used channel/planned anchors, not live jetty coords).
3. Ingest from `route-solutions-synthesize-remapped.jsonl` (or remap inline from `route-solutions.jsonl` using the map).

**Quick reference (passing synthesize only):**

| Grok slug | Live `bp-*` |
|-----------|-------------|
| `dxb-dmyc` | `bp-06edb1cb16` |
| `dxb-jbr-the-walk` | `bp-d1a16f292d` |
| `dxb-zabeel-saray` | `bp-f4ac4e0a50` |
| `dxb-one-only-palm` | `bp-69b8c08204` |
| `dxb-waldorf-palm` | `bp-eabf9538e3` |
| `dxb-anantara-palm` | `bp-409ae0c3e7` |
| `dxb-bluewaters-marina` | `bp-cef3fdf035` |
| `dxb-rixos-palm` | `bp-5ff7762dc1` |
| `dxb-atlantis-royal` | `bp-8625aeb0ac` |
| `ad-hudayriyat-bab-al-nojoum` | `bp-1dd1c580ce` |
| `ad-emirates-palace-marina` | `bp-14c19a643c` |
| `ad-yas-marina` | `bp-3b66a8ce1d` |
| `ad-saadiyat-beach-club` | `bp-5e6f444b82` |
| `ad-saadiyat-marina` | `bp-10899a1b48` |
| `ad-lulu-island` | `bp-31b06c534d` *(snap)* |
| `ad-reem-island` | `bp-f47f75836a` *(snap)* |
| `ad-khalifa-port` | **mint** `[54.651205, 24.808029]` |

---

## Phase 3 checklist

1. **Landmask** — Replace `uae_gulf_land.wkb` with v2 in geom-gates (includes Palm fronds + AD channels).
2. **QA policy** — Promote LB-224 `qa_land_crossing.py` (overlay precedence + 120 m apron).
3. **Allowlist** — Install `route_water_allowlist.json`; merge `restored-routes-LB-242.json`.
4. **Apply** — Ingest **27** `qa_pass: true` rows from `route-solutions.jsonl` via `_apply_corridor_waypoints.py`; mint `route_id` for `synthesize` rows. For the **13 synthesize** rows, remap slugs via `synthesize-bp-id-map.json` (mint Khalifa Port BP first; snap Lulu/Reem endpoints).
5. **Seaward** — Wire `seaward-candidates.json` for densify residuals still UNSOLVED.
6. **QA cascade** — `qa_land_crossing` → `qa_sinuosity` → `qa_distance_vs_geom`.
7. **Reseal #79al** when cascade clean (or document remaining 15 UNSOLVED with reasons).

---

## 27 strict-pass routes (apply these)

**Palm (6):** `dxb-dmyc→dxb-waldorf-palm`, `dxb-jbr-the-walk→dxb-one-only-palm`, `dxb-zabeel-saray→dxb-anantara-palm`, `dxb-bluewaters-marina→dxb-rixos-palm`, `dxb-jbr-the-walk→dxb-zabeel-saray`, `dxb-dmyc→dxb-atlantis-royal`

**Hud / Lulu (7):** all synthesize rows — `ad-hudayriyat-bab-al-nojoum→ad-emirates-palace-marina`, `→ad-yas-marina`, `ad-khalifa-port→ad-yas-marina`, `→ad-saadiyat-beach-club`, `ad-lulu-island→ad-emirates-palace-marina`, `ad-saadiyat-marina→ad-reem-island`, `ad-saadiyat-beach-club→ad-lulu-island`

**Densify `rn-*` (12):** `rn-ceadb9c7fa90`, `rn-5e85f0705584`, `rn-77b4a0f16177`, `rn-e18102cbc6de`, `rn-1347ee2ca13f`, `rn-0c9936fbf037`, `rn-c4e06fd812db`, `rn-7d0b8f0bc5f3`, `rn-395ecff03a2e`, `rn-15fcd5208c1d`, `rn-1ad18654169b`, `rn-fecba89ce1bb`

**ICS (2):** `ics-0038607154`, `ics-00745324c2`

---

## 15 UNSOLVED (see PHASE2-NOTES.md)

**Palm (3):** `dxb-dubai-harbour-marina→dxb-atlantis-palm`, `dxb-zabeel-saray→dxb-rixos-palm`, `dxb-palm-west-beach→dxb-five-palm`

**Densify (8):** `edge-0684`, `rn-d4b70c269a15`, `rn-b1553fad7fc5`, `rn-eed908cac473`, `rn-3f0bb036c8a6`, `rn-cef5f57bcd80`, `rn-766596b9e733`, `rn-08f29522c5f2`

**ICS (4):** `ics-003ff4d4d6`, `ics-0076cdc28b`, `ics-01732febf5`, `ics-017490951d`

---

## Division of labor (locked)

- **Grok:** mask, allowlist, QA policy, solver artifacts (this zip).
- **Tasklet:** apply geometries, reseal #79al, live deploy.