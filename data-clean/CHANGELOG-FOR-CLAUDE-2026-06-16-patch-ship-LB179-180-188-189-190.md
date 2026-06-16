# CHANGELOG-FOR-CLAUDE — Gold #79v — patch-ship LB-179/180/188/189/190

**Date:** 2026-06-16
**Type:** Tools-only patch-ship (classifier + scrubber consolidation + pattern codification)
**Prior gold:** #79u (LB-190 / Wave 5 Indian Ocean close).
**Promotion-critical:** ships 12 consecutive bites of inline scrubber/classifier patches.

## What changed

### Tools (overlay)
1. **`partner-pitch/_tools/classify_marine_bp.py` (LB-179)**
   - Consolidated ~80 NOISE_STRONG tokens across Caribbean / Med / Adriatic / Iberia / Riviera / Eastern-Med / Hawaii / Indian-Ocean.
   - New `NOISE_STRONG_HARD` subset (~50 tokens) — the only ones permitted to veto a confirmed marine `bp_type`.
   - 6 `NOISE_REGEX_PATTERNS`: multi-pipe SEO (`\|.+\|`), condo macro, French villa, Turkish marina-tail, Russian-Cyrillic, marina-outdoor-rec.
   - `CAPTIVE_MARQUEE` chain rescue list (~35 brands: ACI / D-Marin / IGY / Safe Harbor / Aman / Six Senses / Rixos / Mandarin Oriental / Hilton Labriz / Frégate …).
   - `BRAND_RESCUE` operator allow-list (~124 cumulative: Pelni / Jadrolinija / Krilo / Hellenic Seaways / Baleària / Bodrum Express / Cat Cocos / Coraline / Expeditions / Hawaii Superferry …).
   - `MARINE_BP_TYPES` synced with live data — added `public_pier`, `ferry-terminal`, `marina_or_jetty`, `dock`, `quay`, `beach_jetty`, `slipway`, `abra_station`, `floating_helipad`, etc.
   - `NOISE_TERMS_WB` word-boundary list (bar / press / spa / ras / lua).
   - Classifier regression suite green (19 codified cases).

2. **`partner-pitch/_tools/gate_osm_noise_bp.py` (LB-179 / LB-180)**
   - Imports unified term lists from `classify_marine_bp.py` (single source of truth).
   - `METRO_BBOX` extended with permanent blocks: Caribbean 9 / Med 5 / Adriatic 5 / Iberia 7 / Côte d'Azur 7 / Corsica 7 / Eastern-Med 39 / Hawaii 4 / Indian-Ocean 4 (incl. Rodrigues).
   - New `--global` flag (LB-180): sweep entire POI set ignoring bbox.
   - New `--check-only` flag (seal-gate mode): fails on remaining **safe** kills only; route-referenced are advisory.
   - `is_noise()` now delegates to canonical `classify()`.

### Data-clean (sweep deltas)
- Ran `gate_osm_noise_bp.py --global --apply` over full POI set:
  - **139 safe BPs killed** (unreferenced OSM noise: residential / SEO / cultural).
  - **33 route-referenced BPs flagged ADVISORY** (require curator review before kill — preserved this seal).
- POIs: 10,968 → **10,829** (Δ −139).
- Routes: **5,350 unchanged** (no route delta — sweep kills only unreferenced BPs).
- Cities / clusters: unchanged (171 / 99).

### Skills (codification — LB-188 / 189 / 190)
- `navier-scrub-enrich-wave.md` — new section "Cluster-mint patterns" with payload examples for:
  - Greenfield triple-mint (city + country cluster + anchor BP atomic — LB-188).
  - Existing meta-cluster reuse via LB-174 re-anchor (LB-189).
  - Payload-driven dual-cluster (country re-anchor + archipelago mint alongside — LB-190).
  - Payload-named anchor BP mint-first (LB-190 corollary).
- `_SHARED_PRINCIPLES.md` §43 — META-CLUSTER GROUPING + GREENFIELD MINT PATTERNS named-precedent registry: saronic / bay-of-naples-amalfi / aeolians / san-juan-gulf / dalmatia / balearic / turkish-riviera / hawaii / seychelles-archipelago / mauritius-island.

## Gates (HARD)
| Gate | Result |
|---|---|
| `gate_endpoint_labels.py` | 4 HARD pre-existing carries (PH+UAE); 3 WEAK single-token binds — unchanged vs #79u |
| `gate_city_ids.py` | PASS — 206 valid nodes / 5,350 routes / 99 clusters |
| `gate_partner_rationale_leak.py` | clean |
| `gate_osm_noise_bp.py --global --check-only` | **PASS — 0 safe kills remaining; 33 advisory route-referenced** |
| `gate_premint_pair.py` | **0 / 5,350 routes flagged** — 11th consecutive 0-flag at scale |

## Counts (Gold #79u → #79v)
- Routes: 5,350 → **5,350** (Δ 0 — tools-only ship)
- POIs: 10,968 → **10,829** (Δ −139 global sweep kills)
- Cities: **171 unchanged**
- Clusters: **99 unchanged**
- Sidecar `economics_by_route_id.json`: 78 records / 48 pending — unchanged vs #79u

## Provenance
- LB-179: classifier-patch ship (12 consecutive inline bites consolidated).
- LB-180: global sweep mode (`--global` flag).
- LB-188: greenfield triple-mint codified in scrub-enrich skill.
- LB-189: existing-meta-cluster reuse codified in scrub-enrich skill + named-precedent registry.
- LB-190: payload-driven dual-cluster mint codified in scrub-enrich skill.

Seal recompute: nested-blob shape per LB-188; sha256 over actual blob bytes per LB-171.
DUAL-SEAL-WRITE (LB-182): live `atlas-external/data-clean/` mirrored from stage.
