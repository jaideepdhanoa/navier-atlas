# Grok prompt — BP-seal + route-seal for enriched Bolt/Yango markets (2026-06-20)

## Mandate
Tasklet enriched the geometry behind the Bolt/Yango sub-proposals. Two deterministic jobs:

1. **Seal 51 new boarding points** (`inputs/BP-COVERAGE-NEW-2026-06-20.json`) by ID-match/gazetteer
   promotion into POIs. They carry `precision: web_research_canonical` + a validation_log asking you to
   **validate/snap** coords through your chain (OSM Overpass → Mapbox → Google Places → name-token
   agreement). `confidence: medium` items (island/reef/grotto landings) especially need snapping.
2. **Assign `route_id`s (BP↔BP route graph)** for the kept Bolt/Yango corridors so they render. This
   includes **Spain (111 sealed BPs) and Sweden (153)** where the boarding points already exist but every
   corridor's `route_id` is currently null — they don't render today purely for lack of sealed routes.

## Scope (kept markets only — pruned pages are NOT to be sealed)
- **Route-seal, BPs already exist:** Spain (Balearics+Costa del Sol), Sweden (Stockholm archipelago).
- **Seal new BPs + route-seal:** Portugal (Lisbon/Porto/Algarve), Finland (Helsinki islands),
  Estonia (Tallinn islands), Côte d'Ivoire (Abidjan lagoon), Egypt (Red Sea + Cairo Nile),
  Morocco (Tanger Med/Ceuta, Casablanca–Rabat, Al Hoceima).
- **Do NOT seal (pruned):** Lebanon, Israel, Tunisia, Pakistan, Cyprus, Romania, Senegal, Mozambique,
  Caspian-AZ, Caspian-KZ. Their cities/briefs stay in geometry; the *proposal pages* are retired.

## Gates / acceptance
- **0 silent drops:** every new BP is sealed as a POI or in a drop-ledger with a reason
  (failed snap / water-adjacency / unresolved coords).
- 0 land-crossings post-allowlist; 0 orphan routes; every surviving BP carries a source id.
- Cross-border endpoints tagged to the correct country (Helsinki↔Tallinn; VRSA↔Ayamonte;
  Tanger Med↔Algeciras/Ceuta — Algeciras/Ceuta tag as Spain).
- Corridors that can't be snapped to real geometry render **visibly aspirational**, not silently broken.
- Shared corridor network: correct country tags + cross-partner overlap preserved.
- QA report: BPs sealed/dropped (+reason), routes built/culled, before→after POI total, land-crossing=0 proof.

## Notes
- Source of truth is GitHub `main`; this zip is an **input** package.
- Pairs with today's earlier **econ-reseal** handoff (corrected unit economics + TAM-ladder deep-links +
  `economics_url`). This package adds the geometry those corridors were missing.
