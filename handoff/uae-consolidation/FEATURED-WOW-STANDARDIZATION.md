# Featured / wow corridor standardization — canonical marquee set per cluster

**Owner:** Tasklet (curation + canonical set) → Grok (enforce subset + schema at seal).
**Date:** 2026-07-05 · **Applies to:** every partner's `featured_routes` + `wow_corridors`, every market.
**Trigger:** Jaideep — "are we using only the highest-quality featured/wow routes for each market and archiving/retiring the rest… so all the UAE partners in Dubai see the same wow/featured routes as there were some strange routes being featured."

## The finding (measured — `FEATURED-WOW-AUDIT.json`)
- **1,293 hand-curated marquee entries** across the roster (**945** `featured_routes` + **348** `wow_corridors`).
- **Three competing schemas**, no standard: `{from_label,to_label}` dict (822), plain string (348), `{name}` dict (123).
- **No canonical per-cluster set** — each partner spotlights a different subset of the same city. In Dubai: Careem/Noon feature *Dubai Harbour→Nikki Beach* / *Al Khan Lagoon*; Bolt/Yango feature *One&Only Palm→Jumeirah* / *Dubai Creek→Al Seef*. Same city, different marquees.
- **Genuinely strange / out-of-range featured routes confirmed:**
  - Careem (and Noon mirror): **`Abu Dhabi → Muscat`** and **`Fujairah → Muscat`** — UAE→Oman cross-border, ~200 nm, far outside N30 range.
  - Bolt: **`Barcelona → Palma de Mallorca`** — ~130 nm open-sea crossing.
  - (Not all 49 token-flagged are wrong — Athens↔Saronic, Split↔Trogir, Capri↔Positano are legitimate *for their own markets*; the point is nothing curates or range-checks the set.)
- Bolt alone carries **142** entries sprawling across Croatia, Greece, Italy, Spain, Lagos, Qatar, Egypt with mixed formats.

## The principle
`featured_routes` and `wow_corridors` are **presentation highlights, not a source of geometry.** They must be:
1. **Canonical per cluster** — one curated "marquee set" per cluster, chosen for quality, that **every partner operating in that cluster inherits identically.** All UAE-Dubai partners feature the same Dubai marquees.
2. **A strict subset of the inherited geometry** — `featured(P) ⊆ (global_canonical ∩ P.clusters)`. A highlight can never introduce a corridor/route_id not already in the shared map set (ties into the `corridor-inheritance` contract).
3. **Schema-uniform** — one shape: `{route_id, from_label, to_label, cluster_id}`. Retire string and `{name}` variants.
4. **Clean** — no land-crossers, no out-of-range/cross-border legs (kills Abu Dhabi→Muscat, Barcelona→Palma).

## Curation method (per cluster)
For each cluster, from its canonical corridor set, select the **top marquee corridors** by quality — real named endpoints (marina/resort/landmark, not a bare city centroid), on-water, in-range, iconic, non-duplicative. Target a tight **3–6 wow + up to ~8 featured** per cluster (not a hard cap — quality-gated, but small and marquee). This becomes `cluster.marquee_corridors[]` in the registry.

## Inheritance + archival
- **Promote** the curated set to the **cluster** (`CLUSTERS.json` → `marquee_corridors`), keyed by `route_id`.
- Each partner's `featured_routes`/`wow_corridors` become a **derived view**: `cluster.marquee_corridors ∩ partner.clusters` — so all partners in Dubai render the same marquees.
- **Archive the rest** to `handoff/archive/featured-wow-retired-2026-07-05.json` (retire, don't delete — provenance). Anything strange/out-of-range/land-crossing is retired, not promoted.
- A partner MAY still choose to spotlight a subset of the cluster marquees for narrative emphasis, but only from the canonical set — never a bespoke or out-of-set entry.

## Gate
Extend `validate_partner_inheritance.py`:
1. every `featured_routes`/`wow_corridors` entry ∈ `cluster.marquee_corridors` for a cluster the partner is in — FAIL otherwise;
2. schema == `{route_id, from_label, to_label, cluster_id}` — FAIL on legacy string/named shapes;
3. no entry flagged land-crossing / out-of-range / cross-border — FAIL (catches Muscat, Barcelona→Palma).

## Rollout order (by contention / visibility)
UAE (Dubai + Abu Dhabi marquees first — the reported eyesore) → Thailand → Indonesia → India → Colombia → Singapore → rest. Curate cluster marquee sets as each market's geometry is consolidated in the same pass.

## Ownership
Tasklet curates the canonical per-cluster marquee sets and archives the retired entries; Grok wires the derived view + gate at seal. This is the presentation-layer companion to the `corridor-inheritance` (geometry) and finance-corridor contracts.
