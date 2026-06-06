# CHANGELOG 2026-06-06 — featured_routes string→object + Grab citation
- All 113 legacy bare-string top-phase `featured_routes` converted to `{label, route_id}` objects (0 bare strings remain).
- 29 high-confidence top-phase featured_routes linked to real built route_ids (bilateral endpoint match + generic-token guard); 84 remain `{label, route_id:null}` (intentional: unbuilt pairs or network/theme statements) — enrichment pass to follow.
- Grab proof_points[0] citation source set to official press release URL (foodpanda Taiwan acquisition), per Jaideep.
- Content-only change; geometry frozen; staged seal (FUSE-safe local stage) → batch copy.
