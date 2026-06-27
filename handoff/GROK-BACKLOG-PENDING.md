# Grok backlog — pending work (living queue)

**Baseline:** `main` @ `4750ac95` · Production: https://navier-atlas.vercel.app  
**Updated:** 2026-06-27  
**Story geometry:** 1019 pass / 0 fail · **Bite 2:** 32/36 `growth_case` · **Open Grok issues:** 6 (#127, #121, #119, #118, #104, #112)

---

## 0. Current status vs issue requirements

| Issue | Verdict | Gap |
|-------|---------|-----|
| **#115** | ✅ CLOSED | 32/36 bound on `65df120f`; 4 deferred (§2.1); crown-champa/villa-hotels/sun-siyam bound with **wrong** jetties → #121 |
| **#124** | ✅ CLOSED | Core FE-2 done; ~193 referenced dedup groups + 4 Hua Hin land-QA routes remain (§2.8) |
| **#119** | 🔴 OPEN | Geometry 1019/0 ✅; `bp_on_water` still **NOT_RUN**; gold tag pending Tasklet sign-off |
| **#121** | 🔴 OPEN | crown-champa→kurumba, villa-hotels→baros, sun-siyam→westin-miriandhoo still wrong operator |
| **#118** | 🔴 OPEN | `growth_frontend_block.py` label fix + Grab BKK marquee KPI refresh not started |
| **#127** | 🔴 OPEN | Gojek top-level Korea contamination + census re-base — HIGH, not started |

**Open backlog (unchanged priority):**

1. **hawaii** — `growth_frontend_block` null-key failure (>70 nm inter-island)
2. **cote-dazur / d-marin / discovery-land** — no `route_id`s to bind
3. **Mesh geometry** — 3,036 fail (non-story)
4. **Tasklet-owned** — Centara deck (#111), LINE MAN Slides (#108), Minor gold deck (#106)

---

## 1. GitHub issue queue

| Issue | Title | Status | Action |
|-------|-------|--------|--------|
| **#124** | FE-2 POI follow-through | ✅ **CLOSED** | Done on `65df120f` — see handback comment |
| **#115** | Bite 2 ladder cascade (36 partners) | ✅ **CLOSED** | 32/36 bound; 4 deferred → §2.1 |
| **#119** | `bp_on_water` gate + gold re-seal | 🔴 OPEN | §2.3 |
| **#121** | Maldives Velana jetty repoint (3 partners) | 🔴 OPEN | §2.4 |
| **#118** | Grab deck KPI + growth label de-jargon | 🔴 OPEN | §2.5 |
| **#127** | Gojek Korea contamination + census re-base | 🔴 OPEN | §2.6 |
| **#104** | Bolt Bug C greenfield census rebase | 🔴 OPEN | §2.7 |
| **#112** | Unified deck builder hospitality profile | 🟡 OPEN | Shared Grok/Tasklet — deck-studio lane |

---

## 2. Grok-owned work (priority order)

### 2.1 Bite 2 completion — 4 partners remaining (#115 tail)

**Done (32/36):** all mobility + hospitality partners in `bite2-cascade-report.json` with `growth_case: true`.

**Blocked (4):**

| Partner | Blocker | Grok action |
|---------|---------|-------------|
| **hawaii** | Inter-island routes >70 nm → `growth_frontend_block.py` `KeyError: SOM_full_network_navier_transport_rev_yr` | Patch generator for Quanta-LR / forward-SAM-only path OR mark partner `forward_sam_only` in JSON |
| **cote-dazur** | 0 `route_id`s in partner JSON | Mint hospitality corridors + bind (or Tasklet supplies route_ids) |
| **d-marin** | 0 `route_id`s | Same |
| **discovery-land** | 0 `route_id`s | Same |

**Quality debt (32 bound):** 196 economics rows are **distance-tier stubs** (`bite2/distance_tier_stub`), not deck-grounded. Replace when Tasklet sheets exist. `build_economics_sidecar.py` full refresh overwrites stubs — use `SKIP_ECON_SIDECAR_REFRESH=1` until grounded.

**Note:** #115 originally held crown-champa / sun-siyam / universal-enterprises / villa-hotels for Bite 8 — Grok bound them with stubs anyway; **#121** still requires correct Velana jetty geometry.

**Artifacts:** `scripts/grok-bite2/`, `handoff/partner-map-model/bite2-cascade-report.json`, `bite2-econ-stubs-report.json`

---

### 2.2 Story geometry — ✅ COMPLETE (monitor only)

| Metric | Value |
|--------|-------|
| Story pass | **1019 / 0 fail** |
| Allowlisted | 0 |

No active story geometry backlog. Regression watch only.

---

### 2.3 SEAL + gates (#119)

| Gate | Current | Grok action |
|------|---------|-------------|
| `geometry_story` | **PASS** (1019/0) | Update SEAL gate string; ping Tasklet for formal sign-off |
| `bp_on_water` | **NOT_RUN** | Run `gate_bp_water_adjacency.py`; record PASS/FAIL in `SEAL.json` |
| Gold reseal tag | Interim hashes only | Issue new gold tag after gate; handback diff to Tasklet |

**Tasklet:** formal SEAL sign-off (per house rules Grok runs gate, Tasklet signs).

---

### 2.4 Maldives Velana jetty repoint (#121)

Wrong operator jetties still bound on `main`:

| Partner | Current `route_id` | Wrong owner | Target |
|---------|------------------|-------------|--------|
| `crown-champa` | `e__velana__kurumba-jetty` | Universal | Kuredu / Meeru flagship |
| `villa-hotels` | `e__velana__baros-jetty` | Universal | Sun Island / Paradise |
| `sun-siyam` | `e__velana__westin-miriandhoo-jetty` | Marriott | Iru Fushi |

**Leave alone:** `universal-enterprises`→kurumba, `constance`→halaveli.

**Scope:** `journeys_unlocked`, matching `featured_routes`, `_velana_hospitality_bind`; mint/repoint routes if needed; reseal.

---

### 2.5 Grab deck KPI + economics labels (#118)

1. **`growth_frontend_block.py` generator fix** — SOM/SAM/TAM rung labels need plain-English descriptors per house rule (recurrence prevention).
2. **One-time pass** over existing partner `growth_case` objects (bolt.json et al.).
3. **Grab deck KPI refresh** — reconcile BKK marquee: Atlas BKK↔Hua Hin vs deck ICONSIAM→Wat Arun.
4. **Slides API live-edit only** — no full PPTX round-trip.

Partial overlap: #126 merged de-jargon on 8 partners + sub-$10M format; does **not** cover generator fix or Grab deck.

---

### 2.6 Gojek Korea contamination + census (#127) — HIGH

**Bug A — top-level Korea residue (live contamination):**
- `gojek.json` `journeys_unlocked` + `phases` are 100% Korea (Kakao template); markets[] are clean Indonesia.
- Rebind from in-file Indonesian `route_id`s; re-derive phase `boats` from Gojek model (not Kakao 8/173/432/864).
- Normalize descriptive `to_node_id` strings in eastern-indonesia to real node IDs.

**Bug B — census re-base (Bolt Bug-C twin):**
- `greenfield_corridors: 341` (shared census), `sourced 35`, `som_network` ~5× floor.
- Per-market economics `authored_for: grab` throughout.
- Re-base to Gojek-specific corridor set; re-cascade ladder before Indonesia deck.

**Tasklet holds:** copy/jargon fixes + Indonesia deck until Grok lands geometry + census.

---

### 2.7 Bolt Bug C greenfield census (#104)

- Bolt `growth_case` rests on borrowed peer census (341 corridors, Grab width).
- `som_network` ~4.9× grounded floor — confidently-wrong for Bolt.
- Re-cascade with Bolt-specific corridor census; reseal economics.
- **No new geography / BPs.**

Spec: `handoff/GROK-HANDOFF-bolt-bugC-census-rebase.md`

---

### 2.8 FE-2 POI dedup tail (#124 closed, residual)

**Done on `65df120f`:**
- 16 route-bound junk rebinds (28 routes)
- Hua Hin pier coord fix
- 876 safe duplicate drops (11,490 POIs)
- SEAL hash refresh

**Remaining (~193 dedup groups):** copies still referenced in ROUTES / CLUSTERS / partners — need per-group rebind before drop. Worklist: `data-clean/_handoff/fe2-grok-dedup-worklist.json` (1,069 groups; 876 orphans already removed).

**Hua Hin routes:** 4 routes still fail land QA after coord fix — coastal geometry rebuild pending (non-story mesh).

---

### 2.9 Mesh geometry (non-story)

| Metric | Value |
|--------|-------|
| Mesh pass | 3,353 |
| Mesh fail | **3,036** |

Out of story north-star scope. See `handoff/MESH-BACKLOG.md`, `handoff/partner-map-model/PARKED-ROUTING-GEOMETRY-QUEUE.md`.

Priority mesh markets (from handback): Bolt South Africa, Croatia depth, Bolt Phase 0 footprint.

---

### 2.10 Narrative / proposal completeness (no open issue)

| Item | Scale | Notes |
|------|-------|-------|
| Null `journeys_unlocked` | ~190 across 23 partners | Bite 5 hygiene merged (#117); content still sparse |
| Bolt East Africa parity | #116 merged | Verify live `/bolt` sub-pages |
| India `economics_url` wiring | Adani/Reliance tracker | Sheets on Drive; cards unwired |
| Bolt data bugs | `handoff/GROK-SPEC-bolt-data-bugs.md` | Floor rounding, stale `source_rollup`, ladder on minted corridors |

---

### 2.11 Research / coverage / locale (lower priority)

- P0 promotion: Bolt (`crete`, `malta-gozo`), Lyft (4 Hawaii)
- Yango interim regional seed reconciliation
- P1 mobility depth: Grab, DiDi, Gojek, Ola, inDrive, Cabify, FREENOW, Kakao
- Locale ledgers: UAE, Bolt, Thailand, Wave2 — residual gates
- India normalization + Adani/Reliance missing-market scan

---

## 3. Tasklet-owned (Grok does NOT block on these)

| Item | Source | Notes |
|------|--------|-------|
| **Centara Thailand deck appendix** | PR #111 | Bind 7 sealed corridors; refresh economics from sidecar; dock rights null |
| **LINE MAN Wongnai live Slides** | PR #108 | Package on `main`; Slides build |
| **Minor Hotels gold deck** | PR #106 | LB-261 rebase refresh |
| **Formal gold SEAL sign-off** | #119 | After Grok runs `bp_on_water` |
| **Gojek copy cascade** | #127 | After Grok rebind |
| **Gojek Indonesia deck** | #127 | After census re-base |

---

## 4. Suggested Grok execution order

1. **#127 Gojek** — HIGH live contamination
2. **#121 Maldives jetties** — confidently-wrong geometry on 3 partners
3. **#119 `bp_on_water` gate** — unblock Tasklet SEAL sign-off
4. **#118 Grab labels + deck KPI**
5. **#104 Bolt Bug C census**
6. **Bite 2 tail** — Hawaii generator + mint routes for cote-dazur / d-marin / discovery-land
7. **FE-2 dedup tail** — referenced-copy groups
8. **Mesh waves** — as capacity allows

---

## 5. Completed since last Tasklet handback (do not re-queue)

- Story geometry 1019/0 (waves 10–11)
- FE-2 routebound + Hua Hin + 876 dedup (#124)
- Bite 2 cascade 32/36 (#115 core)
- All Tasklet PRs through #126 merged
- Production deploy `65df120f` / handback `4750ac95`

---

*Grok seat · update this file when issues close or priorities shift*