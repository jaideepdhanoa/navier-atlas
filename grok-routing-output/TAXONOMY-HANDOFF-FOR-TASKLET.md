# Taxonomy Migration Handoff — Grok → Tasklet
**Date:** 2026-06-19 · **Seal target:** `#79ao` (taxonomy)  
**Machine-readable manifest:** `grok-routing-output/TAXONOMY-MIGRATION-2026-06-19.json`  
**Migration script:** `scripts/grok-taxonomy/apply_taxonomy.mjs` (idempotent re-run safe)

---

## Executive summary

Grok shipped the **global 4-tier geography model**:

```
Region → Cluster (country/archipelago) → City (metro/emirate) → Locale (district/island/development) → Boarding points
```

| Metric | Before | After |
|--------|--------|-------|
| Clusters in `CLUSTERS.json` | 117 | **99** (−18) |
| `FEATURES_BY_TYPE.locale` | 0 | **127** |
| Locale brief stubs (`city_briefs/*__*`) | 1 (Palawan) | **7** (+6 UAE) |
| Nav tiers | 3 (Region/Cluster/City) | **4** (+Locale) |
| `dubai-uae` → cluster | `the-world-dubai` ❌ | `uae` ✅ |

---

## What Grok changed

### 1. `data-clean/CLUSTERS.json` (v2-taxonomy)

**Deleted 18 clusters** (demoted to locale OR duplicate twin):

| cluster_id | Action | Replacement |
|------------|--------|-------------|
| `palm-jumeirah-dubai` | → locale | `dubai-uae__palm-jumeirah-crescent-inner` |
| `the-world-dubai` | → locale | `dubai-uae__world-islands-heart-of-europe` |
| `abu-dhabi-islands` | → locales | Yas, Saadiyat, Corniche, Sir Bani Yas (4 pins) |
| `nassau-bahamas-cluster` | duplicate | keep `bahamas` |
| `cayman-islands-cluster` | duplicate | keep `cayman-islands` |
| `turks-caicos-cluster` | duplicate | keep `turks-caicos` |
| `usvi-bvi-cluster` | duplicate | keep `usvi-bvi` |
| `aeolian-islands-italy` | → city | `sicily-aeolian-italy` |
| `saronic-gulf-greece` | → city | `athens-saronic-greece` |
| `ionian-islands-greece` | → city | `corfu-ionian-greece` |
| `corsica-island-france` | → city | `corsica-france` |
| `malta-archipelago` | → city | `malta-gozo` |
| `lisbon-tagus-estuary` | → city | `lisbon-tagus-portugal` |
| `seychelles-archipelago` | → city | `mahe-seychelles` |
| `mauritius-island` | → city | `port-louis-mauritius` |
| `the-red-sea-archipelago` | → city | `the-red-sea-archipelago-ksa` |
| `amaala-triple-bay` | → city | `red-sea-global-ksa` (crosswalk) |
| `thuwal-private-retreat` | → city | `neom-sindalah-ksa` (stub parent) |

**Set `parent_cluster_id` + `nav_hidden: true`** on 8 multi-city sub-regions (routing anchors retained, hidden from tier-2 nav):

| cluster_id | parent_cluster_id |
|------------|-------------------|
| `dalmatia-croatia` | `croatia` |
| `bay-of-naples-amalfi-coast-italy` | `italy` |
| `balearic-islands-spain` | `spain` |
| `turkish-riviera-aegean` | `turkey` |
| `cote-dazur-france-archipelago` | `france` |
| `ksa-commercial` | `saudi-arabia` |
| `leeward-antilles-northern` | `st-maarten-st-barths` |
| `windward-antilles` | `st-lucia-grenadines` |

**Region split — LatAm-Caribbean → Latin-America + Caribbean:**

| New region | Clusters migrated |
|------------|-------------------|
| `Latin-America` (6) | brazil, colombia, costa-rica, mexico, panama, galapagos-ecuador |
| `Caribbean` (16) | abc-islands, antigua-barbuda, bahamas, barbados, belize, cayman-islands, cuba, dominican-republic, jamaica, puerto-rico, st-lucia-grenadines, st-maarten-st-barths, turks-caicos, usvi-bvi, leeward-antilles-northern*, windward-antilles* |

\*These two retain `parent_cluster_id` and are nav-hidden.

**Orphan cities wired:**

| city_id | cluster_id |
|---------|------------|
| `al-wakrah-qatar` | `qatar` |
| `dammam-khobar-ksa` | `saudi-arabia` |
| `moorea-french-polynesia` | `french-polynesia` |
| `huahine-french-polynesia` | `french-polynesia` |
| `maupiti-french-polynesia` | `french-polynesia` |

**Removed from `member_city_ids`:** locale ids (e.g. `palawan-philippines__el-nido-bacuit-bay` was incorrectly listed as a cluster member).

### 2. `data-clean/FEATURES_BY_TYPE.json`

- Added **`locale`** array: **127 features** emitted from `app/data-spine/output/nodes.json` (`type: locale` + promoted POI subnodes for Dubai/Abu Dhabi marquee areas).
- Locale id canonicalization: slash variants (`/-`) → hyphen form for filesystem-safe ids.

### 3. Locale brief stubs (`data-clean/city_briefs/`)

New stubs (Tasklet: **enrich** — demand signals, signature routes, use cases):

| File | Migrated from cluster |
|------|----------------------|
| `dubai-uae__palm-jumeirah-crescent-inner.json` | `palm-jumeirah-dubai` |
| `dubai-uae__world-islands-heart-of-europe.json` | `the-world-dubai` |
| `abu-dhabi-uae__yas-island.json` | `abu-dhabi-islands` |
| `abu-dhabi-uae__saadiyat-island.json` | `abu-dhabi-islands` |
| `abu-dhabi-uae__abu-dhabi-island-corniche-al-maryah-cbd.json` | `abu-dhabi-islands` |
| `abu-dhabi-uae__sir-bani-yas-desert-islands.json` | `abu-dhabi-islands` |

Each stub has `_taxonomy.migrated_from_cluster`, `_taxonomy.status: "stub"`, `_taxonomy.tasklet_action: "enrich"`.

**No cluster briefs were deleted** — the 32 country-level `cluster_briefs/` are unchanged. Sub-cluster *narrative* that lived only in routing changelogs should be folded into the locale stubs above + parent city briefs (`dubai-uae.json`, `abu-dhabi-uae.json`).

### 4. `index.html` (render lane)

- **`NAV_CLUSTERS`**: excludes `parent_cluster_id` / `nav_hidden` clusters from tier-2 chips and cluster pins.
- **`CITY_TO_CLUSTER`**: built from nav-visible clusters only; skips `__` locale ids in member lists.
- **`LOCALES_BY_PARENT`**: tier-4 index for city → locale drill.
- **Locale map layer** re-enabled (coral pins, z8+, labels z10+).
- **Top nav tier 4**: city chip → locale chips when city has 2+ locales.
- **Breadcrumb**: `Global › Region › Cluster › City › Locale`.
- **City brief panel**: "Areas in {city}" locale chip row.
- **Search**: locales indexed again.
- **Region aliases**: `Latin-America` / `Caribbean` split; Europe sub-regions normalize to `Europe`.

---

## Tasklet action items (prioritized)

### P0 — Adopt on next seal

1. **Re-emit `FEATURES_BY_TYPE.locale`** in Tasklet `build.py` — do **not** strip locales inside BP-covered cities (Grok currently owns locale emission via `apply_taxonomy.mjs` until Tasklet adopts).
2. **Enrich the 6 UAE locale brief stubs** — pull narrative from #79ab/#79ac Dubai showcase + #79ac Abu Dhabi Islands changelogs.
3. **Guardrail on new mints:** never add a cluster sharing a `member_city_id` without `parent_cluster_id`; sub-geographies → `parent__locale` + `city_briefs` entry.

### P1 — Global locale depth

4. **Mint locale subnodes** in city `.md` files for markets that lost sub-clusters but have no locale pins yet (see table below).
5. **Enrich locale briefs** following `palawan-philippines__el-nido-bacuit-bay.json` as the gold template.
6. **Resolve `dammam-khobar-ksa` vs `eastern-province-ksa`** — duplicate Eastern Province representation; pick canonical city or split locales.

### P2 — Remaining orphans (Grok deferred)

| city_id | Suggested cluster | Notes |
|---------|-------------------|-------|
| `bp-4e324134ef` (Sir Bani Yas jetty) | `uae` / locale under `abu-dhabi-uae` | Promoted-hub anomaly |
| `bp-095a41dfcb` (Daymaniyat) | `oman` / locale under `muscat-oman` | |
| `bp-893a394e6a`, `bp-7a5f687851`, `bp-23245c74f6`, `bp-6af248fd3b`, `bp-d4738f6ad2` | `philippines` cities | BP-as-city Bucket B artifacts — crosswalk to city nodes |

### P3 — Europe display regions

Normalize `Europe-Mediterranean`, `Europe-Atlantic`, `Europe-Baltic`, `Europe-Med` cluster.region values to `Europe` (render already aliases; data cleanup optional).

---

## Sub-clusters demoted to city (Tasklet: add locales when ready)

These clusters were **removed**; the **city node** is now the nav target. Tasklet should add locale subnodes in city `.md` when sub-area drill is warranted:

| Removed cluster | Parent city | Suggested locale work |
|-----------------|-------------|----------------------|
| `aeolian-islands-italy` | `sicily-aeolian-italy` | Lipari, Vulcano, Stromboli… |
| `saronic-gulf-greece` | `athens-saronic-greece` | Piraeus, Hydra, Spetses… |
| `ionian-islands-greece` | `corfu-ionian-greece` | Already city-level |
| `corsica-island-france` | `corsica-france` | Ajaccio, Bonifacio… |
| `malta-archipelago` | `malta-gozo` | Valletta, Gozo, Comino |
| `lisbon-tagus-estuary` | `lisbon-tagus-portugal` | Tagus south bank, Setúbal… |
| `seychelles-archipelago` | `mahe-seychelles` | Praslin, La Digue |
| `mauritius-island` | `port-louis-mauritius` | Grand Baie, Le Morne |
| `the-red-sea-archipelago` | `the-red-sea-archipelago-ksa` | RSI islands |
| `amaala-triple-bay` | `red-sea-global-ksa` | Triple Bay jetties |
| `thuwal-private-retreat` | `neom-sindalah-ksa` | KAUST harbour |

---

## Locale coverage by parent city (top 15)

| parent_city_id | locale count |
|----------------|-------------|
| `muscat-oman` | 11 |
| `dubai-uae` | 10 |
| `phuket-phang-nga-thailand` | 7 |
| `abu-dhabi-uae` | 6 |
| `sharjah-uae` | 6 |
| `bali-indonesia` | 6 |
| `komodo-flores-indonesia` | 6 |
| `doha-qatar` | 5 |
| `banda-maluku-indonesia` | 5 |
| `lombok-indonesia` | 5 |
| `malaysia` | 5 |
| `japan` | 4 |
| `fujairah-uae` | 4 |
| `bangkok-thailand` | 4 |
| `singapore` | 4 |

**Total:** 127 locale features across all parent cities with spine definitions.

---

## RACI (unchanged)

| Work | Owner |
|------|-------|
| Locale `.md` definitions, brief *content*, demand/signature routes | **Tasklet** |
| `CLUSTERS.json` mechanical edits, locale feature emission, nav/render | **Grok** |
| Re-seal after Tasklet enriches briefs | **Grok** |

---

## Verification

```bash
node scripts/grok-taxonomy/apply_taxonomy.mjs   # idempotent
node scripts/build.mjs                          # expect locale in feature types
# Nav QA: MENA → UAE → Dubai → Palm Jumeirah / World Islands (not peer clusters)
# Breadcrumb: dubai-uae resolves to cluster uae (not the-world-dubai)
```

---

## Files touched

- `data-clean/CLUSTERS.json`
- `data-clean/FEATURES_BY_TYPE.json`
- `data-clean/city_briefs/dubai-uae__*.json` (2)
- `data-clean/city_briefs/abu-dhabi-uae__*.json` (4)
- `index.html`
- `scripts/grok-taxonomy/apply_taxonomy.mjs`
- `grok-routing-output/TAXONOMY-MIGRATION-2026-06-19.json`
- `docs/NOTES-FOR-TASKLET.md`