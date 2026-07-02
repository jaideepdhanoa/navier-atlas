# Grok → Tasklet handback — PTA Phase D complete

**From:** Grok · **Date:** 2026-07-02 · **Status:** Grok lane **CLOSED** — zero Grok dependencies for Tasklet  
**Supersedes:** `grok-handback-TASKLET-PTA-MAIN-LANDED-2026-07-02.md` for Phase D work

---

## 0. Executive summary

Phase D (Batch-8) Grok lane is **complete**. All Wave 1 seals + Wave 2 greenfield mints are on `main` (pending push). Tasklet can bind Wave 2 partner JSONs and close superseded GitHub PRs **#170–#173** with no Grok wait.

| Layer | Status |
|-------|--------|
| Wave 1 — Manila re-seal (#170) | ✅ 5 Pasig corridors re-sealed, `interior_land_km == 0`, fidelity **PASS** |
| Wave 1 — HCMC seal (#171) | ✅ 4 Line-1 corridors minted + bound, fidelity **PASS** |
| Wave 1 — Rio seal (#172) | ✅ 4 Praça XV spokes minted + bound, fidelity **PASS** |
| Wave 2 — Mersey / Toronto / CalMac / Seoul (#173) | ✅ Greenfield mint complete — BPs + routes sealed |
| Economics regen (all 7) | ✅ `growth_case` regenerated (Wave 2 floor-only until partner JSON exists) |
| Open GitHub PRs #170–#173 | **Content is on `main`** — close as superseded |

---

## 1. Seal + mint state (authoritative)

### Wave 1 — anchor-ready authorities (partner JSON exists)

| Partner | Sealed routes | Land QA | Fidelity | Economics |
|---------|--------------|---------|----------|-----------|
| `manila-pasig-ferry` | **5** / 5 (+ 1 pending Intramuros) | ✅ 0 km all | **PASS** | ✅ Live (5 corridors) |
| `hcmc-saigon-waterbus` | **4** / 4 | ✅ 0 km all | **PASS** | ✅ Live (4 corridors) |
| `rio-ccr-barcas` | **4** / 4 | ✅ 0 km all | **PASS** | ✅ Live (4 corridors) |

**Manila re-seal note:** Tasklet had bound 5 `rn-` corridors but Grok audit found `PASS_WITH_FLAGS` (0.67–3.75 km land crossings). Grok re-sealed all 5 with Pasig River regional water override → **PASS** at 0 km.

**Receipts:** `PTA-SEAL-RECEIPT-{manila-pasig-ferry,hcmc-saigon-waterbus,rio-ccr-barcas}.json`

### Wave 2 — greenfield seed-and-seal (no partner JSON yet)

| Partner | City node | BPs minted | Routes sealed | Honest-null |
|---------|-----------|------------|---------------|-------------|
| `mersey-ferries` | `liverpool-mersey-uk` (new seed) | 3 | **3** / 3 | — |
| `toronto-island-ferry` | `toronto-island-canada` (new seed) | 4 | **3** / 3 (hub-and-spoke) | — |
| `calmac` | `firth-of-clyde-scotland` (new seed) | 6 | **3** / 4 scoped | Oban↔Craignure held |
| `seoul-hangang-bus` | `seoul-incheon-korea` (reused) | 7 (3 shared kakao) | **4** / 4 | — |

**Receipts:** `GEOMETRY-MINT-RECEIPT-{mersey-ferries,toronto-island-ferry,calmac,seoul-hangang-bus}.json`

### Seoul reconciliation (verified)

Shared physical pier nodes canonicalized to kakao BPs — no double-plot:

| Pier | Canonical `bp_id` | Market |
|------|-------------------|--------|
| Yeouido | `bp-kakao-yeouido` | SMG Hangang + kakao |
| Ttukseom | `bp-kakao-ttukseom` | SMG Hangang + kakao |
| Jamsil | `bp-kakao-jamsil` | SMG Hangang + kakao |

Hangang-exclusive mints: Magok (`bp-7ee5f26a66`), Mangwon (`bp-d6ac07d9fd`), Oksu (`bp-ee5a48e3f1`), Apgujeong (`bp-95c15c88ec`).

---

## 2. Route inventory (bind these `rn-` ids only)

### Manila — Pasig River (re-sealed, same route_ids)

| route_id | corridor |
|----------|----------|
| `rn-b16e98d4316a` | Kalawaan ↔ Guadalupe |
| `rn-1e7d4d541a7b` | Kalawaan ↔ Maybunga |
| `rn-3752e977b617` | Sta. Ana ↔ Lambingan |
| `rn-e52b4a43ab2a` | Lambingan ↔ Pureza |
| `rn-d445408ef0c9` | Pureza ↔ Sta. Ana |

### HCMC — Saigon Waterbus Line 1

| route_id | corridor |
|----------|----------|
| `rn-9eb0307b3eb1` | Bach Dang ↔ Binh An |
| `rn-da00b3e2e930` | Binh An ↔ Thanh Da |
| `rn-0f49fc10d206` | Thanh Da ↔ Linh Dong |
| `rn-e32f782a58ac` | Bach Dang ↔ Linh Dong (through-run) |

### Rio — CCR Barcas (Praça XV hub)

| route_id | corridor |
|----------|----------|
| `rn-1886629dbf0c` | Praça XV ↔ Arariboia (Niterói) |
| `rn-80f0d0ebe0bd` | Praça XV ↔ Charitas |
| `rn-00bb6ded4be5` | Praça XV ↔ Paquetá |
| `rn-369ef0eb69d9` | Praça XV ↔ Cocotá |

### Mersey Ferries

| route_id | corridor |
|----------|----------|
| `rn-6a494ddccc93` | Pier Head ↔ Seacombe |
| `rn-e5030c0a20e1` | Pier Head ↔ Woodside |
| `rn-520412ca1ebe` | Seacombe ↔ Woodside |

### Toronto Island Ferry

| route_id | corridor |
|----------|----------|
| `rn-57b3537e1e7b` | Jack Layton ↔ Centre Island |
| `rn-b26389d844d8` | Jack Layton ↔ Hanlan's Point |
| `rn-ab4e6272d722` | Jack Layton ↔ Ward's Island |

### CalMac (Clyde gateways — 3 sealed, 1 held)

| route_id | corridor | status |
|----------|----------|--------|
| `rn-42bf8c54fd60` | Ardrossan ↔ Brodick | ✅ sealed |
| `rn-8cf92f7f5bc2` | Wemyss Bay ↔ Rothesay | ✅ sealed |
| `rn-45d97634b4a1` | Gourock ↔ Dunoon | ✅ sealed |
| — | Oban ↔ Craignure | ⏸ honest-null (Sound of Mull land-QA; later horizon) |

### Seoul Hangang Bus

| route_id | corridor |
|----------|----------|
| `rn-047fe5d8e686` | Jamsil ↔ Yeouido (Eastern) |
| `rn-6d96e229ce7e` | Magok ↔ Yeouido (Western) |
| `rn-ce55c292989a` | Yeouido ↔ Ttukseom |
| `rn-451fa6544ccd` | Magok ↔ Jamsil (through-run) |

---

## 3. Grok tooling (persisted)

| Script | Role |
|--------|------|
| `scripts/pta/mint_phase_d.py` | Wave 2 greenfield seed cities + BPs + routes |
| `scripts/pta/seal_authority.py` | Seal from dossier; `--force-reseal` for geometry updates; bp_id binding |
| `scripts/pta/regen_pta_economics.py` | Phase D slugs in `PHASE_BC_SLUGS`; reads `GEOMETRY-MINT-RECEIPT` |
| `scripts/grok-geometry/regional_land_masks.py` | +7 Phase D water bboxes (Pasig, Saigon, Guanabara, Mersey, Toronto, Clyde) |

---

## 4. Tasklet next steps (complete checklist)

### P0 — Housekeeping

| # | Task | Acceptance |
|---|------|------------|
| 1 | **Close superseded GitHub PRs** #170–#173 | Content on `main`; PRs closed |
| 2 | **Append Phase D seven to `PTA-PAIR-GAP-TABLE.json`** | 7 new rows with seal state from receipts |
| 3 | **Update `PTA-MASTER-PLAN.md`** | Phase D Grok lane = closed |

### P1 — Wave 2 partner JSON binding (4 authorities)

Per Kolkata/Manila anchor-ready pattern — bind `bp-` + `rn-` from §2 receipts into both trees:

| Slug | Bind from receipt | Notes |
|------|-------------------|-------|
| `mersey-ferries` | `GEOMETRY-MINT-RECEIPT-mersey-ferries.json` | City `liverpool-mersey-uk`, cluster `uk` |
| `toronto-island-ferry` | `GEOMETRY-MINT-RECEIPT-toronto-island-ferry.json` | City `toronto-island-canada`, cluster `great-lakes-usa` |
| `calmac` | `GEOMETRY-MINT-RECEIPT-calmac.json` | City `firth-of-clyde-scotland`; Oban↔Craignure = pending-seal |
| `seoul-hangang-bus` | `GEOMETRY-MINT-RECEIPT-seoul-hangang-bus.json` | City `seoul-incheon-korea`; use shared kakao `bp-` for 3 piers |

### P2 — Optional (not blocking)

| Item | Notes |
|------|-------|
| Manila Intramuros downstream | `manila-intramuros-plaza-mexico` BP not meshed — pending-seal |
| CalMac Oban↔Craignure | Sound of Mull crossing — null beats wrong |
| Residual Phase C honest-nulls | Still optional; do not block |

---

## 5. Guardrails (unchanged)

| Rule | Why |
|------|-----|
| Never `regen_pta_economics.py --all` on batch-5 | Reverts #150 presentation scrub |
| Never rewrite WSF `growth_case` numbers | #169 surgical rule |
| Never bind junk atlas hits | Birkenhead→Sydney, Woodside→NS, Tacloban→PH, Otrobanda→Curaçao |
| Seoul: one canonical pier per location vs kakao | No double-plot |
| Null beats wrong | Bind only receipt `rn-` ids |

---

## 6. Acceptance commands

```bash
# Wave 1 fidelity (all PASS)
for p in manila-pasig-ferry hcmc-saigon-waterbus rio-ccr-barcas; do
  python3 scripts/audit_proposal_fidelity.py --partner "$p"
done

# Manila land QA (all 0 km)
python3 -c "
import json, sys
from pathlib import Path
sys.path.insert(0,'scripts/grok-geometry')
from route_land_qa import evaluate_route
routes = json.loads(Path('data-clean/ROUTES.json').read_text())
ids = {'rn-b16e98d4316a','rn-1e7d4d541a7b','rn-3752e977b617','rn-e52b4a43ab2a','rn-d445408ef0c9'}
for r in routes:
    rid = r.get('properties',{}).get('id')
    if rid in ids:
        ev = evaluate_route(r['geometry']['coordinates'])
        assert ev['qa_pass'] and ev['interior_land_km'] == 0, rid
print('Manila PASS')
"

BUILD_PROFILE=public node scripts/build.mjs
```

---

## 7. Program state

```
Phase C (mint-heavy + WSF)    ✅ landed
Phase D Wave 1 (#170–#172)    ✅ Grok sealed + economics
Phase D Wave 2 (#173)         ✅ Grok minted — Tasklet binds partner JSON
─────────────────────────────────────────
Phase E / batch-9             → Tasklet next (when greenlit)
shun-tak                      → Jaideep scope
```

---

## 8. Who owns what

| Layer | Owner | Status |
|-------|-------|--------|
| Wave 1 partner JSON + dossiers | **Tasklet** | ✅ Done (#170–#172) |
| Wave 1 seal + economics | **Grok** | ✅ Done |
| Wave 2 dossiers + GROK-SPEC | **Tasklet** | ✅ Done (#173) |
| Wave 2 mint + routes | **Grok** | ✅ Done |
| Wave 2 partner JSON binding | **Tasklet** | **Next** |
| Gap table / master plan | **Tasklet** | P0 housekeeping |
| Merge / deploy | **Jaideep** | At your pace |

---

*Grok seat · navier-atlas · PTA Phase D Grok lane closed · Tasklet cleared for Wave 2 binding*