# Grok backlog — pending work (living queue)

**Baseline:** `main` @ post-phase-2 drain · Production: https://navier-atlas.vercel.app  
**Updated:** 2026-06-27  
**Intake:** `GROK-HANDBACK-2026-06-27-phase2.md`  
**Story geometry:** 1019 pass / 0 fail · **Bite 2:** 33/36 `growth_case` (hawaii forward-SAM bound) · **Open Grok issues:** 4 (#119, #118-partial, #112-partial, Bite-2 tail)

---

## 0. Current status vs issue requirements

| Issue | Verdict | Gap |
|-------|---------|-----|
| **#127** | ✅ CLOSED | Gojek 3-phase drain on `44060e8a` |
| **#121** | ✅ CLOSED | Maldives jetty repoint on `44060e8a` |
| **#104** | ✅ CLOSED | Bolt greenfield off on `44060e8a` |
| **#115** | ✅ CLOSED | 32/36 + hawaii forward-SAM on phase 2 |
| **#124** | ✅ CLOSED | FE-2 core done; ~193 dedup groups remain |
| **#119** | 🔴 OPEN | Gate run: **FAIL 1297 true mis-geocodes** (allowlist integrated); Tasklet gold sign-off pending |
| **#118** | 🟡 PARTIAL | KPI JSON refreshed; generator fix done; **Slides API apply blocked** (stale OIDs) |
| **#112** | 🟡 PARTIAL | Hospitality `gen_deck_economics` branch (7/7 Centara); applier + Minor re-pull held |

**Open backlog:**

1. **#119** — Triage 1297 true bp mis-geocodes (coord snap / allowlist expansion)
2. **#118** — Tasklet OID refresh → live Grab Slides KPI apply
3. **#112** — Hospitality page-fill applier + Minor binding re-pull + QA gate
4. **cote-dazur / d-marin / discovery-land** — bind `route_id`s, cascade
5. **Mesh geometry** — 3,036 fail (non-story)
6. **FE-2 dedup tail** — ~193 referenced-copy groups

---

## 1. GitHub issue queue

| Issue | Title | Status | Action |
|-------|-------|--------|--------|
| **#127** | Gojek corridor + census | ✅ **CLOSED** | `44060e8a` |
| **#121** | Maldives Velana jetties | ✅ **CLOSED** | `44060e8a` |
| **#104** | Bolt Bug C census | ✅ **CLOSED** | `44060e8a` |
| **#119** | `bp_on_water` gate + gold re-seal | 🔴 OPEN | §2.3 |
| **#118** | Grab deck KPI + growth labels | 🟡 PARTIAL | §2.5 |
| **#112** | Unified deck builder hospitality | 🟡 PARTIAL | §2.6 |
| **#115** | Bite 2 ladder cascade | ✅ **CLOSED** | 33/36; 3 hospitality route binds remain |

---

## 2. Grok-owned work (priority order)

### 2.1 Bite 2 completion — 3 partners remaining (#115 tail)

**Done (33/36):** hawaii bound with `_forward_sam_only` Quanta-LR roadmap block.

**Blocked (3):**

| Partner | Blocker | Grok action |
|---------|---------|-------------|
| **cote-dazur** | 0 `route_id`s in partner JSON | Bind corridors from `corridors.json` + cascade |
| **d-marin** | 0 `route_id`s | Same |
| **discovery-land** | 0 `route_id`s | Same |

---

### 2.2 Story geometry — ✅ COMPLETE (monitor only)

1019 / 0 fail. Regression watch only.

---

### 2.3 SEAL + gates (#119)

| Gate | Current | Grok action |
|------|---------|-------------|
| `geometry_story` | **PASS** (1019/0) | Monitor |
| `bp_on_water` | **FAIL 1297 true** | Coord snap wave or allowlist expansion; re-run gate |
| Gold reseal tag | Interim hashes | Tasklet formal sign-off after gate PASS |

---

### 2.4–2.5 (closed / partial)

- **#121 Maldives** — ✅ done
- **#118 Grab** — KPI JSON refreshed; live Slides apply needs OID re-pull (Tasklet)

---

### 2.6 Unified deck builder (#112) — PARTIAL

- ✅ `gen_deck_economics.py` hospitality branch (Centara 7/7)
- 🔴 Page-fill applier, Minor binding re-pull, `deck_studio` QA gate

Spec: `handoff/centara-thailand/GROK-SPEC-unified-deck-builder-hospitality-profile.md`

---

### 2.7–2.9 (unchanged lower priority)

Mesh 3,036 fails · FE-2 dedup ~193 groups · research/coverage waves as capacity allows.

---

## 3. Tasklet-owned (Grok does NOT block)

| Item | Notes |
|------|-------|
| **Gojek copy + Indonesia deck** | After #127 — unblocked |
| **Grab live Slides apply** | After OID manifest refresh |
| **Formal gold SEAL sign-off** | After #119 triage |
| **Centara / Minor / LINE MAN decks** | Hospitality gen branch ready for Centara values |

---

## 4. Suggested Grok execution order

1. **#119** — bp mis-geocode triage wave (snap / allowlist)
2. **Bite 2 tail** — cote-dazur / d-marin / discovery-land route binds
3. **#112** — hospitality applier + QA gate
4. **#118** — unblock with Tasklet OID refresh → apply
5. **FE-2 dedup** + **mesh** as capacity allows

---

*Grok seat · update when issues close or priorities shift*