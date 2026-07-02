# Grok → Tasklet handback — PTA Phase C landed on `main`

**From:** Grok · **Date:** 2026-07-02 · **Status:** Grok lane **CLOSED** — zero Grok dependencies for Tasklet  
**`main` commit:** (see git log after push) · **Supersedes:** all prior PTA handbacks for open work

---

## 0. Executive summary

Everything Tasklet shipped in **#162–#169** plus all Grok seal/economics/mint work is now on **`main`**. Tasklet can proceed to **Phase D** and housekeeping with **no Grok wait**.

| Layer | Status |
|-------|--------|
| Batch-5 taxonomy scrub (#162) | ✅ **Landed** — qatar + singapore-mpa |
| Mint-heavy six (#163–#168) | ✅ **Landed** — partner JSON + dossiers + GROK-SPECs |
| WSF finish (#169) | ✅ **Landed** — close scrub + dossier + seal spec |
| Grok geometry mint (6 cities) | ✅ **Landed** (`0df92d29`) — cities + 24 BPs |
| Grok partial seals + economics | ✅ **Landed** — see §3 |
| Open GitHub PRs #162–#169 | **Content is on `main`** — close PRs as superseded if GitHub still shows them open |

---

## 1. What landed (file inventory)

### 1a. New PTA partners (12 files each tree)

| Slug | Display | Dossier | GROK-SPEC | Seal receipt |
|------|---------|---------|-----------|--------------|
| `oslo-ruter` | Oslo — Ruter Fjord Ferry | `PTA-DOSSIER-oslo-ruter.json` | `GROK-SPEC-oslo-ruter-mint-authority-2026-07-02.md` | `PTA-SEAL-RECEIPT-oslo-ruter.json` |
| `amsterdam-gvb` | Amsterdam — GVB IJ | `PTA-DOSSIER-amsterdam-gvb.json` | `GROK-SPEC-amsterdam-gvb-mint-authority-2026-07-02.md` | `PTA-SEAL-RECEIPT-amsterdam-gvb.json` |
| `copenhagen-movia` | Copenhagen — Movia harbour bus | `PTA-DOSSIER-copenhagen-movia.json` | `GROK-SPEC-copenhagen-movia-mint-authority-2026-07-02.md` | `PTA-SEAL-RECEIPT-copenhagen-movia.json` |
| `wellington-metlink` | Wellington — Metlink | `PTA-DOSSIER-wellington-metlink.json` | `GROK-SPEC-wellington-metlink-mint-authority-2026-07-02.md` | `PTA-SEAL-RECEIPT-wellington-metlink.json` |
| `rotterdam-mrdh` | Rotterdam — MRDH Waterbus | `PTA-DOSSIER-rotterdam-mrdh.json` | `GROK-SPEC-rotterdam-mrdh-mint-authority-2026-07-02.md` | `PTA-SEAL-RECEIPT-rotterdam-mrdh.json` |
| `gothenburg-vasttrafik` | Gothenburg — Västtrafik | `PTA-DOSSIER-gothenburg-vasttrafik.json` | `GROK-SPEC-gothenburg-vasttrafik-mint-authority-2026-07-02.md` | `PTA-SEAL-RECEIPT-gothenburg-vasttrafik.json` |

Also updated: `qatar`, `singapore-mpa` (batch-5 scrub), `wsf` (close scrub + dossier).

### 1b. Geometry mint receipts (Grok, pre-Tasklet PRs)

All under `handoff/partner-map-model/GEOMETRY-MINT-RECEIPT-*.json`:

| City ID | BPs minted | Starter routes at mint |
|---------|------------|------------------------|
| `oslo-norway` | 4 | 0 (fjord land-QA) |
| `amsterdam-netherlands` | 4 | 0 (IJ land-QA) |
| `copenhagen-denmark` | 4 | 1 |
| `wellington-new-zealand` | 4 | 1 |
| `rotterdam-netherlands` | 4 | 0 (river land-QA) |
| `gothenburg-sweden` | 4 | 1 |

Atlas: `FEATURES_BY_TYPE.json`, `CLUSTERS.json`, `ROUTES.json` updated.

### 1c. Grok tooling (persisted)

| Script | Role |
|--------|------|
| `scripts/pta/mint_authority_city.py` | Mint city + BPs + starter routes |
| `scripts/pta/seal_authority.py` | Seal from dossier (supports compact + `domestic_network` formats) |
| `scripts/pta/regen_pta_economics.py` | Authority economics; mint-heavy slugs in `PHASE_BC_SLUGS` |

---

## 2. Seal + economics state (authoritative)

Post-Grok second lane. Fidelity **PASS** on all.

| Partner | Sealed routes (total) | Economics panel | `archetype` |
|---------|----------------------|-----------------|-------------|
| `oslo-ruter` | **1** / 4 (Hovedøya↔Bygdøy) | ✅ Live (1 corridor) | `public_transit` |
| `amsterdam-gvb` | **2** / 4 | ✅ Live (2 corridors) | `public_transit` |
| `copenhagen-movia` | **2** / 4 | ✅ Live (2 corridors) | `public_transit` |
| `wellington-metlink` | **3** / 4 | ✅ Live (3 corridors) | `public_transit` |
| `rotterdam-mrdh` | **0** / 4 | ✅ Floor-only (0 sealed) | `public_transit` |
| `gothenburg-vasttrafik` | **2** / 4 | ✅ Live (2 corridors) | `public_transit` |
| `wsf` | **4** sealed + **4** pending | ✅ Live (unchanged) | `public_transit` |
| `kolkata-wbtc` | 5 / 5 | ✅ Live | `public_transit` |
| `helsinki-hsl` | 7 / 7 | ✅ Live | `public_transit` |

**Unsealed corridors** keep `route_id: null` + `_link_status: pending-seal` (or `aspirational-no-built-route` on WSF). Fidelity accepts this.

### Honest-null inventory (optional future seal — NOT Tasklet blockers)

| Partner | Corridor | Why unsealed |
|---------|----------|--------------|
| `oslo-ruter` | Aker Brygge ↔ Nesoddtangen, Hovedøya, Bygdøy (3) | Inner-fjord land-QA |
| `amsterdam-gvb` | 2 IJ pairs | Land-QA |
| `copenhagen-movia` | 2 harbour pairs | Land-QA |
| `wellington-metlink` | 1 harbour pair | Land-QA |
| `rotterdam-mrdh` | All 4 | Nieuwe Maas river land-QA |
| `gothenburg-vasttrafik` | 2 archipelago pairs | Land-QA |
| `wsf` | Bainbridge, Kingston, Fauntleroy–Vashon, Vashon–Southworth | Puget Sound seal pass pending |
| `bc-ferries` | Horseshoe Bay ↔ Departure Bay (bcf-d04) | Georgia Strait land-QA |
| `mumbai-mmb` | Belapur↔Nerul, Gateway↔Rewas | Mis-bound DROP (#151) |

---

## 3. Tasklet next steps (complete checklist — no gaps)

### P0 — Housekeeping (1 PR recommended)

| # | Task | Files | Acceptance |
|---|------|-------|------------|
| 1 | **Close superseded GitHub PRs** #162–#169 if still open | GitHub UI | PRs show closed; `main` has their content |
| 2 | **Append mint-heavy six to `PTA-PAIR-GAP-TABLE.json`** | gap table + `.md` | Six new rows with pair counts from dossiers |
| 3 | **Update `PTA-MASTER-PLAN.md`** progress log | master plan | Phase C = merged on main; Grok lane closed |
| 4 | Verify **batch-5 forbidden-key sweep** still 0 | 24 batch-5 JSONs | `rg 'Forward-SAM\|Prove \+ Scale\|_marine_tam_split' data-clean/partners/{batch-5}.json` → 0 |

### P1 — Phase D (Batch-8) — **greenlit, no Grok dependency**

Author when ready; each needs full Batch-6 deliverable set (dossier → rewrite → GROK-SPEC → partner JSON):

| Authority | Water body | Notes |
|-----------|------------|-------|
| Scotland — CalMac / Transport Scotland | Hebrides | Diesel-legacy; strong lifeline story |
| Liverpool — Mersey Ferries (Merseytravel) | Mersey | |
| HCMC — Saigon Waterbus | Saigon River | |
| Manila — Pasig River Ferry | Pasig | |
| Rio — CCR Barcas | Guanabara Bay | |
| Toronto — Island Ferry | Lake Ontario | |
| Seoul — Hangang Bus | Han River | **⚠️ ID hygiene** — reconcile vs `kakao-mobility` / existing Seoul nodes before mint |

**Sequencing:** Jaideep greenlit Batch-8 in master plan §6. No dependency on mint-heavy seal gaps.

### P2 — Deferred (Jaideep scope — not Tasklet)

| Item | Status | Tasklet action |
|------|--------|----------------|
| **`shun-tak`** | Deferred | Hold — GBA commercial cross-boundary lane; memo on file |
| Residual honest-null seals (§2) | Optional Grok | **Do not block Phase D** — prose already honest |

### P3 — Deck / non-PTA lanes (unchanged)

Centara deck appendix · LINE MAN live Slides · Minor gold deck · bite-2 economics stubs.

---

## 4. Guardrails (do not break)

| Rule | Why |
|------|-----|
| **Never** `regen_pta_economics.py --all` on batch-5 | Reverts #150 presentation scrub |
| **Never** rewrite WSF `growth_case` numbers | #169 surgical rule — economics already Grok-regenerated |
| **Never** invent `route_id`s for honest-null corridors | Null beats wrong; bind only to receipt `rn-` ids |
| Mirror **both trees** on every partner edit | `data-clean/partners/` + `partner-pitch/partners/` |

---

## 5. Acceptance commands (all green on landed `main`)

```bash
# Mint-heavy + anchor-ready + WSF + batch-5 scrub targets
for p in qatar singapore-mpa oslo-ruter amsterdam-gvb copenhagen-movia \
  wellington-metlink rotterdam-mrdh gothenburg-vasttrafik wsf \
  kolkata-wbtc helsinki-hsl bc-ferries; do
  python3 scripts/audit_proposal_fidelity.py --partner "$p"
done

BUILD_PROFILE=public node scripts/build.mjs --profile=public
BUILD_PROFILE=public node scripts/build-site.mjs --profile=public
```

---

## 6. Program state diagram

```
Phase A (batch-5 scrub)     ✅ #150–#154
Phase B (outside-lane 5)    ✅ #155–#159 + Grok seals
Phase C anchor (2)          ✅ #160–#161 + Grok economics
Phase C mint-heavy (6)      ✅ #163–#168 + Grok partial seals
Batch-5 P0 scrub            ✅ #162
WSF finish                  ✅ #169
Grok lane                   ✅ CLOSED
─────────────────────────────────────────
Phase D (batch-8)           → Tasklet next
shun-tak                    → Jaideep scope call
```

---

## 7. Who owns what (final)

| Layer | Owner | Status |
|-------|-------|--------|
| Partner narrative / dossier / GROK-SPEC | **Tasklet** | Phase C complete |
| City/BP/route geometry mint | **Grok** | ✅ Done |
| Route seal + economics regen | **Grok** | ✅ Done (partial seals documented) |
| Renderer (`index.html`) | **Grok** | ✅ Live (`_ptaEconomicsHtml`) |
| Phase D research + PRs | **Tasklet** | **Next** |
| Merge / deploy | **Jaideep** | At your pace |

---

*Grok seat · navier-atlas · PTA Phase C on main · Tasklet cleared for Phase D*