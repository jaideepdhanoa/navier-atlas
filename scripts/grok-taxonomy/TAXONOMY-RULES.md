# Taxonomy rules — Region → Cluster → City → Locale

**Locked product tree**

```
Region  (e.g. Europe, Caribbean)
  └── Cluster  (country / multi-island market — **nav chip**)
        └── City  (member_city_ids on the country cluster)
              └── Locale  (FEATURES locale under parent city)
```

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

- Proper `cluster_label` (`Poland`, `United Kingdom`, …)
- `member_city_ids` = union of its cities (including those also listed on child water-system clusters)

## Never do this

1. Leave a hyphenated water-system id as a **top-level** cluster with `cluster_label == cluster_id`.
2. Mint a new water-system cluster without setting `parent_cluster_id` + `nav_hidden`.
3. Invent cities/locales without exact IDs (null beats wrong).
4. Duplicate country nav chips for the same geography.

## Gate (CI / pre-merge)

```bash
python3 scripts/grok-taxonomy/validate_cluster_taxonomy.py
```

Fails on top-level water-system tokens or raw-slug multi-hyphen chips without a parent.

## Apply nest for current Wave1 leftovers

```bash
python3 scripts/grok-taxonomy/nest_water_system_clusters_2026_07_11.py
python3 scripts/grok-taxonomy/validate_cluster_taxonomy.py
```

## Precedent

- PR #231 — UK water-systems under `uk`; Germany fjord/rhine children under `germany`
- This pass — Poland / Hungary / Austria country nodes + Baltic / Danube / Balaton / Constance / Seine children
