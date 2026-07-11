# Taxonomy rules — Region → Cluster → City → Locale

**Locked product tree**

```
Region  (e.g. Europe, Caribbean)
  └── Cluster  (country / multi-island market — **nav chip**)
        └── City  (member_city_ids on the country cluster)
              └── Locale  (FEATURES locale under parent city)
```

## Display capitalization (permanent)

**IDs stay kebab-case / lowercase. User-visible names never do.**

| Tier | Stable ID field | Display field(s) | Example |
|------|-----------------|------------------|---------|
| Region | region slug / key | region brief title / chip | `Europe` not `europe` |
| Cluster | `cluster_id` | **`cluster_label`** (required; primary UI) | `Belgium` not `belgium` |
| City | `properties.id` | `name` / `shortName` / `fullName` | `Antwerp` not `antwerp-belgium` |
| Locale | `properties.id` | `name` / `shortName` / `fullName` | `Saadiyat Island` not slug |

Rules:

1. **Every cluster must set `cluster_label`** to a human proper-noun form (`Belgium`, `Hong Kong`, `United Kingdom`, `Gdańsk / Tricity`). Do not rely on `label`/`display` alone — map UI uses `cluster_label || cluster_id`, so a missing `cluster_label` renders the raw id.
2. Keep `label` and `display` **aligned** with `cluster_label` when those fields are present (no leftover raw slugs in `display`).
3. City and locale `name` / `shortName` must be Title Case or correct local orthography (`Düsseldorf`, `Siófok`, `Liège`) — never the city id, never all-lowercase.
4. When minting via `ensure_cluster()` / Wave1 seals, always set `cluster_label` at create time (not only `label`/`display`).
5. Null beats wrong: if you do not know the proper local spelling, leave the entity unminted rather than shipping a lowercase slug as the chip text.

## Water-system routing anchors (not nav chips)

Wave1 and similar mints often create **water-system** clusters (`gulf-of-gdansk-tricity`, `lake-balaton-hungary`, …). These are **routing anchors**, not top-level browse labels.

**Required fields on every water-system cluster:**

| Field | Value |
|-------|--------|
| `parent_cluster_id` | Country cluster id (`poland`, `hungary`, `germany`, `uk`, …) |
| `nav_hidden` | `true` |
| `cluster_label` / `label` | Human display (e.g. `Gdańsk / Tricity`, **never** the raw slug) |
| `region` | Same as parent country |

**Country cluster** stays the top-level chip:

- Proper `cluster_label` (`Poland`, `United Kingdom`, `Belgium`, …)
- `member_city_ids` = union of its cities (including those also listed on child water-system clusters)

## Never do this

1. Leave a hyphenated water-system id as a **top-level** cluster with `cluster_label == cluster_id`.
2. Mint a new water-system cluster without setting `parent_cluster_id` + `nav_hidden`.
3. Invent cities/locales without exact IDs (null beats wrong).
4. Duplicate country nav chips for the same geography.
5. Ship a cluster without `cluster_label`, or with `cluster_label` equal to the raw `cluster_id` / all-lowercase (shows as `belgium` in nav).
6. Use a city id as `name`/`shortName` (e.g. `tampere-finland`, `bregenz`).

## Gate (CI / pre-merge)

```bash
python3 scripts/grok-taxonomy/validate_cluster_taxonomy.py
```

Fails on:

- top-level water-system tokens or raw-slug multi-hyphen chips without a parent
- missing / all-lowercase / raw-slug `cluster_label` on any cluster
- missing / all-lowercase / raw-slug city or locale `name` / `shortName`

## Apply nest for current Wave1 leftovers

```bash
python3 scripts/grok-taxonomy/nest_water_system_clusters_2026_07_11.py
python3 scripts/grok-taxonomy/validate_cluster_taxonomy.py
```

## Precedent

- PR #231 — UK water-systems under `uk`; Germany fjord/rhine children under `germany`
- This pass — Poland / Hungary / Austria country nodes + Baltic / Danube / Balaton / Constance / Seine children
