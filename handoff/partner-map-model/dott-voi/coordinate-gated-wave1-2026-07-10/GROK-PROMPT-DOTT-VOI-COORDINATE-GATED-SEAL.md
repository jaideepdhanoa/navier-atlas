# Grok seal request — Dott/Voi coordinate-gated Wave 1 follow-on

Use `DOTT-VOI-COORDINATE-GATED-CANONICAL-HANDOFF.json` as research input only. ID-match against current `main`; reuse exact IDs; mint no placeholder IDs verbatim. Seal coordinate-ready T1/T2 boarding points only when the named physical feature, city, cluster, water adjacency, public-pickup/access context, and duplicate checks pass. Generate deterministic water-aware route geometry only for endpoint pairs with both coordinates ready and no remaining source/access/operational hold.

Corridors are global geography: author each accepted corridor once in canonical `ROUTES.json`, bind it to the canonical cluster, and derive partner views as `global_canonical ∩ partner.clusters`. Never hand-author Dott- or Voi-specific route subsets. Preserve all unresolved records with null coordinates. Do not change economics.

Return a seal receipt with every BP and route candidate classified as reused / sealed / held or dropped with reason; before/after counts; 0 silent drops; 0 land crossings; 0 orphan routes; 0 duplicate IDs; strict inheritance; Dott UAE retained; Voi Europe-only.
