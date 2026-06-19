# CHANGELOG — Gold #79ao — Global taxonomy migration (2026-06-19)

**Base:** #79an (5876 routes)

## Summary
- 4-tier geography: Region → Cluster → City → Locale → Boarding points
- CLUSTERS: 117 → 99 (−18 demoted/duplicate twins)
- FEATURES_BY_TYPE.locale: 0 → 127
- LatAm-Caribbean split → Latin-America + Caribbean
- Sub-clusters: parent_cluster_id (8 nav-hidden) or demoted to locales
- CITY_TO_CLUSTER fix: dubai-uae / abu-dhabi-uae → uae
- 6 UAE locale brief stubs + tier-4 nav in index.html

**Handoff:** grok-routing-output/TAXONOMY-HANDOFF-FOR-TASKLET.md
