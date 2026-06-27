# Grok handback — AirAsia MOVE Malaysia seal

**Partner:** `airasia-move`  
**Script:** `scripts/grok-airasia/seal_airasia_malaysia.py`  
**Receipt:** `AIRASIA-MALAYSIA-SEAL-RECEIPT.json`

---

## Minted routes (4 new)

| Key | route_id | Distance |
|-----|----------|----------|
| jesselton_gaya | `rn-2a148be8da55` | 3 nm |
| jesselton_mamutik | `rn-4a35d08732bc` | 4 nm |
| semporna_sipadan | `rn-a0a21bf62427` | 20 nm |
| langkawi_intra | `rn-76bf7675c6e3` | 12 nm |

**ROUTES.json:** 7418 (+4 from 7414)

## Reused sealed routes (9)

| Key | route_id |
|-----|----------|
| jesselton_manukan | `rn-9cf6a4039290` |
| langkawi_koh_lipe | `gcn-b3d5523f36-shared` |
| langkawi_penang | `gcn-5596b8c9ee-shared` |
| langkawi_phuket | `rn-853cbe7dd006` (107 nm; spec 140 — held note) |
| penang_butterworth | `gcn-c46f3bf4b8-shared` |
| penang_ferringhi | `gcn-0965643d33-shared` |
| penang_langkawi | `gcn-5596b8c9ee-shared` |
| desaru_singapore | `rn-5d1a30fbb0a9` |
| desaru_intra | `rn-59e1b8a8a6ca` |

## Bindings

- **27 total** (16 featured + 11 journeys) — 0 `unlinked-needs-mint` remaining in Malaysia markets
- Thailand + Indonesia geometry **untouched**

## Build fix

- `layout` → `hub` (was `super_app_multi_market` — caused `no cities resolved`)
- `network_footprint` added for 15 markets
- Exclusion grep: removed `Jaideep` from deploy-facing provenance strings

## Held

| Item | Reason |
|------|--------|
| Tioman sub-page | `tioman-island` city node missing from FEATURES_BY_TYPE |
| Indonesia 13 inherited nulls | Per spec — bind when Gojek binds, not AirAsia mint |
| Langkawi↔Phuket distance | Reused 107 nm route vs 140 nm card — Quanta-LR still valid |

## Validation

- `build-site.mjs` — all 14 AirAsia pages pass (tioman skipped advisory)
- Preflight — pending post-commit