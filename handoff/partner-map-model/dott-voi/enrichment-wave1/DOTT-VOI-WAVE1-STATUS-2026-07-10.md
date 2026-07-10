# Dott / Voi canonical-geography enrichment — Wave 1

**Date:** 2026-07-10  
**Status:** research-complete / seal-needed

## What this wave establishes

The renderer/inheritance repair made the partner pages broad, but the underlying canonical geography is still uneven. Wave 1 converts the official footprint audit into source-backed, geography-owned seal inputs across five lanes:

1. Belgium and Switzerland
2. United Kingdom and Germany
3. Nordics
4. Voi Le Havre and Dott Poland
5. Dott Austria, Hungary and Balearics

Each lane includes a normalized exact-bind ledger, source-led candidate boarding points and routes, explicit nulls/holds, and deterministic next actions. No route IDs, coordinates, economics or partner-specific corridors were invented.

## Three P0 exact-ID repairs precede new geography

### 1. UK cluster precision

The existing generic `uk` cluster contains 64 visible routes: 33 London-only, 18 Liverpool/Mersey and 13 Firth of Clyde. That is too coarse for exact partner operation:

- Dott currently supports Glasgow, but current evidence explicitly excludes London and does not establish Liverpool.
- Voi currently supports London and Glasgow, but not Liverpool.

The UK graph must be decomposed into water-system-owned clusters while preserving route IDs. Dott should inherit Clyde only from the existing set; Voi should inherit London and Clyde. Solent and Severn/Avon are new-geography candidates after source and water QA.

### 2. Lake Geneva cluster ownership

Fourteen existing routes whose city is `lake-geneva-switzerland` are incorrectly stamped `cluster_id: indonesia`. Retag those exact route IDs to Switzerland; do not mint replacements. This repairs both the global graph and Dott/Voi's current zero-route Switzerland state.

### 3. Ibiza reuse

Dott's official Ibiza row already exact-binds to `ibiza-spain`. The city has an existing brief and ten visible canonical routes, including Ibiza Harbour–La Savina/Formentera geometry. The initial fallback assessment was corrected: reuse the existing route IDs and normalize terminal aliases only.

## Enrichment order after the repairs

1. Shared Belgium: Brussels canal first, then Antwerp/Ghent/Liège as evidence permits
2. Switzerland: Basel Rhine and Lake Zürich; reuse repaired Lake Geneva
3. UK: Solent, Clyde and Severn/Avon exact depth
4. Germany: Baltic, Elbe and Rhine/Ruhr systems
5. Nordics: exact coastal systems and city bindings
6. Voi Le Havre / Seine estuary
7. Dott Baltic Poland
8. Dott Austria/Hungary waterways

## Seal acceptance

- New routes are created once in the global canonical graph.
- Partner pages inherit `ROUTES ∩ partner.clusters`; no per-partner route lists.
- Every boarding point is either sealed with provenance or retained in a reasoned drop/hold ledger.
- Zero land crossings, zero orphan routes, zero silent drops.
- Dott remains UAE-inclusive; Voi remains Europe-only with no MENA.
- Before/after route counts are reported by partner and cluster.
- Partner inheritance, finance inheritance and partner-copy gates pass; economics remain unchanged.
