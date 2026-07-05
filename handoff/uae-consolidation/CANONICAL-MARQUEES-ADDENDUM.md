# Addendum — canonical marquee sets for ALL markets (one pass, no per-market cycles)

**Date:** 2026-07-05 · **From:** Tasklet · Companion to `GROK-MASTER-HANDOFF-2026-07-05.md`.

## Why this is done now (not one market at a time)
Curation is done at the **OD-pair level (BP node pair + cluster_id)**, ID-based — *not* at the volatile `route_id` level. Grok's reseal changes route IDs/geometry, **not** which named waterfront OD pairs are the marquees. So Tasklet completed the canonical curation for the **entire roster in a single pass**; Grok only needs to **bind `route_id` after reseal** (deterministic). No dependency, no cycles.

## What was produced
- **`CANONICAL-MARQUEES.json`** — one canonical set per cluster: `marquee_wow` (≤6) + `marquee_featured` (≤8), each entry `{route_id (hint), from_node_id, to_node_id, from_label, to_label, cluster_id, distance_nm, partner_feature_count, partners_currently_featuring, _score}`.
  - **91 clusters** have canonical sets · **40** carry real crowd-signal (≥1 partner currently features) · 51 are greenfield (top clean-by-traffic, honest).
- **`MARQUEE-RETIRE-LIST.json`** — **926 current entries retired** (348 free-text strings with no ID, 104 unresolved BP pairs not in ROUTES, rest = not in cluster canonical top set). Retire = archive to `handoff/archive/`, not delete.
- **`CANONICAL-MARQUEES-REVIEW.md`** — human-readable table for the contested markets (UAE, Thailand, Indonesia, India, Colombia, Singapore, Qatar, Egypt, Morocco, Tunisia).
- **`gen_canonical_marquees.py`** — deterministic generator (re-runnable post-reseal).

## Quality gate (what can NOT enter a marquee set)
`_qa_land_flag` / `_quarantine` · land_km > 0.2 · distance ∉ [0.4, 30] nm · missing endpoint labels · **self-referential** (same place both ends) · `(planned)` down-weighted. Result: `Abu Dhabi→Muscat`, `Fujairah→Muscat`, `Barcelona→Palma`, and the self-referential Cartagena dup are **provably excluded**. A `_label_needs_cleanup` flag marks any pick whose label carries geocoding-provenance noise (currently 0 in the selected set).

## What Grok does with this
1. After UAE (then each market's) reseal, **bind `route_id`** to each canonical marquee by its BP node pair (`from_node_id`,`to_node_id`) → resealed corridor. If a marquee's BP pair didn't survive reseal, drop it and pull the next-ranked clean candidate from `CANONICAL-MARQUEES.json` (already ordered by score).
2. **Derive every partner's featured/wow** as `cluster.marquee_corridors ∩ partner.clusters` — identical set for all partners in a market (UAE-Dubai partners all see the same marquees).
3. **Collapse schema** to the single `{route_id, from_label, to_label, cluster_id}` shape; archive retired entries.
4. Gate: `validate_partner_inheritance.py` rejects any featured/wow entry not in the cluster canonical set, wrong-schema, or land/range-dirty.

## Worked example — UAE (all four partners inherit this identical set)
1. Kempinski Palm Jumeirah ↔ Atlantis The Palm (2.0 nm)
2. One&Only The Palm ↔ Jumeirah Zabeel Saray (1.9 nm)
3. La Mer / J1 Beach ↔ Nikki Beach Pearl Jumeirah (1.2 nm)
4. Côte d'Azur Resort Marina ↔ Anantara World Islands (2.4 nm)
5. Vida Beach Umm Al Quwain ↔ Sharjah Waterfront City (7.3 nm)
6. Ras Al Khaimah Harbour ↔ RAK Corniche (0.4 nm)

_Note: canonical granularity follows CLUSTERS.json (UAE is one country-cluster). All UAE partners inherit the same set, so Dubai marquee consistency is achieved by construction._
