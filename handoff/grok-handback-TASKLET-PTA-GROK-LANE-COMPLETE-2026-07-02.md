# Grok → Tasklet handback — PTA Grok lane COMPLETE

**From:** Grok · **Date:** 2026-07-02  
**Branch:** `main` · **HEAD:** `1b0857b5`  
**Scope:** Zero Grok dependencies remaining for geometry seals, economics regen, mint-heavy city receipts

---

## Grok lane — DONE

| Workstream | Status |
|------------|--------|
| Quick fixes (bahrain inner-harbour `1.8 nm`, mumbai deferred corridors) | ✅ |
| `regen_pta_economics.py` — `sealed_corridors`, batch-5 guard, Phase B/C full apply | ✅ |
| Phase B seals + economics (5 partners) | ✅ partial seals — see receipts |
| Kolkata + Helsinki economics + `public_transit` archetype | ✅ |
| Mint-heavy six cities + `mint_authority_city.py` | ✅ cities + BPs; starter routes partial |
| Public build (`build.mjs`) | ✅ |

---

## Sealed partners (Phase B)

| Partner | Routes sealed | Receipt | Fidelity |
|---------|---------------|---------|----------|
| `bc-ferries` | 7/8 (`bcf-d04` Horseshoe Bay↔Departure Bay pending) | `PTA-SEAL-RECEIPT-bc-ferries.json` | TRIM (1 drop) |
| `hawaii` | 2/7 (anchor Maui↔Lānaʻi + long channels pending land QA) | `PTA-SEAL-RECEIPT-hawaii.json` | PASS_WITH_FLAGS |
| `fullers360` | 4/8 (Waiheke + outer Gulf pending) | `PTA-SEAL-RECEIPT-fullers360.json` | PASS_WITH_FLAGS |
| `maldives-government` | **7/7** | `PTA-SEAL-RECEIPT-maldives-government.json` | PASS_WITH_FLAGS |
| `norway-fjords` | 5/6 (`nor-d02` Geiranger↔Hellesylt pending) | `PTA-SEAL-RECEIPT-norway-fjords.json` | PASS_WITH_FLAGS |

All five have `growth_case` + `_economics_status: pta_regenerated` + `_public_transit_authority` in both trees.

---

## Phase C economics

| Partner | Corridors | Archetype | Fidelity |
|---------|-----------|-----------|----------|
| `kolkata-wbtc` | 5 (`sealed_pairs`) | `public_transit` | PASS |
| `helsinki-hsl` | 7 (`sealed_pairs`) | `public_transit` | PASS |

---

## Geometry mint receipts (mint-heavy five + Oslo)

| City ID | Receipt | BPs | Starter routes |
|---------|---------|-----|----------------|
| `oslo-norway` | `GEOMETRY-MINT-RECEIPT-oslo-norway.json` | 4 | 0 (Oslofjord land-mask QA) |
| `amsterdam-netherlands` | `GEOMETRY-MINT-RECEIPT-amsterdam-netherlands.json` | 4 | 0 (IJ narrow-water QA) |
| `wellington-new-zealand` | `GEOMETRY-MINT-RECEIPT-wellington-new-zealand.json` | 4 | 1 |
| `copenhagen-denmark` | `GEOMETRY-MINT-RECEIPT-copenhagen-denmark.json` | 4 | 1 |
| `gothenburg-sweden` | `GEOMETRY-MINT-RECEIPT-gothenburg-sweden.json` | 4 | 1 |
| `rotterdam-netherlands` | `GEOMETRY-MINT-RECEIPT-rotterdam-netherlands.json` | 4 | 0 (river QA) |

Junk POIs quarantined: `bp-bcfc48aae1` (Oslo Road Boat Ramp FL), `bp-b718f46797` (Fort Amsterdam Caribbean), `bp-71155e0dbe` (Wellington Point AU), `bp-6825d03a00` (Mystic Wellington Yacht Club US).

Cities registered in `CLUSTERS.json`: `oslo-norway` → `norway`; `wellington-new-zealand` → `new-zealand`; `gothenburg-sweden` → `sweden`; new `netherlands` + `denmark` clusters.

**Tasklet unblocked:** dossier + partner rewrite PRs per city (Batch-6 pattern like #160/#161).

---

## What Tasklet still owns (ONLY)

### P0 — Copy / hygiene (no Grok)

1. **`_recal_provenance` SAM/TAM scrub** — all 24 batch-5 partners, both trees (`rg 'Forward-SAM|SAM mid|journey_gmv'` → 0).
2. **`PTA-MASTER-PLAN.md`** — update checkboxes: Grok lane complete; mint receipts landed.
3. **`wsf` dossier + partner scope** — Washington State Ferries rewrite (deferred from batch-5 table).
4. **`shun-tak` scope memo** — commercial cross-boundary franchise; explicitly out of PTA lane.

### P1 — Partner PRs now unblocked (Tasklet research + rewrite)

| Suggested slug | City receipt | Grok follow-up (optional) |
|----------------|--------------|---------------------------|
| `oslo-ruter` | `oslo-norway` | More Oslofjord hand-waypoints for starter routes |
| `amsterdam-gvb` | `amsterdam-netherlands` | IJ pontoon route QA |
| `wellington-metlink` | `wellington-new-zealand` | Harbour crossing waypoints |
| `copenhagen-movia` | `copenhagen-denmark` | Extend harbour-bus mesh |
| `gothenburg-vasttrafik` | `gothenburg-sweden` | Älvsnabben mesh |
| `rotterdam-ret` | `rotterdam-netherlands` | Waterbus river waypoints |

### P2 — Residual seal gaps (Grok optional; fidelity PASS_WITH_FLAGS today)

- `hawaii` — re-waypoint `haw-d01` Maui↔Lānaʻi anchor + open-channel legs.
- `fullers360` — Waiheke (`ful-d02`) + outer Gulf (`ful-d06`–`d08`).
- `norway-fjords` — Geiranger↔Hellesylt WH fjord (`nor-d02`).
- `bc-ferries` — Horseshoe Bay↔Departure Bay (`bcf-d04`).

### P3 — Phase D research

Long-tail PTA authorities not in pair table; Tasklet research into `handoff/partner-map-model/drafts/` only.

---

## Scripts added / extended

- `scripts/pta/regen_pta_economics.py` — batch-5 presentation guard; `sealed_pairs` corridor count; Phase B/C full growth_case.
- `scripts/pta/mint_authority_city.py` — city + BP mint, junk quarantine, starter routes, cluster registration.

---

## Deploy

- `BUILD_PROFILE=public node scripts/build.mjs` — **PASS** (7940 routes, 12001 features).
- `node scripts/build-site.mjs` — **5 page build failures** (pre-existing partner pages; atlas-data OK).