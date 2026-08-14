# GROK SPEC — Employer hub map corrections (2026-08-14)

Post-launch verification audit (`inputs/GROK-STOP-VERIFICATION.md`) failed 4 stops added in the
v2 build against Navier's landing gate (a stop may only render if a presently usable
commercial-passenger landing exists). Corrections, nothing else moves:

## Bay Area (`employer-hub/hubs/bay-area/hub.json`)
1. **CULL — Alviso Marina** (stop 5): silted; kayak/small-craft launch only. Remove stop + segments; Peninsula Trunk full-network terminus becomes Port of Redwood City.
2. **CULL — Hayward Landing** (stop 11): no dock exists (shoreline trail).
3. **CULL — San Leandro Marina** (stop 12): harbor basin closed to boats; docks removed.
4. **CULL — Hercules Waterfront** (stop 17): ferry dock never built. North Bay Express skips Hercules (Pittsburg → Benicia → Vallejo → Richmond → Berkeley → Emeryville → TI → FB).
5. **RE-SPINE — Southeast Bay Line**: with Hayward + San Leandro culled, respine as
   Jack London Square → Main St Alameda → Harbor Bay → Oyster Point (phase 2, OP transfer).
   Keep geography-first name.
6. Keep (verified PASS): Coyote Point Marina, Pittsburg Marina, Benicia Marina, Emery Cove Marina, Berkeley Marina guest docks, Port of Redwood City.

## New York (`employer-hub/hubs/new-york/hub.json`)
7. **RENAME — "Throgs Neck" (stop 21) → "Ferry Point Park"**: the actual landing is at Ferry Point Park; adjust pin to the real landing coordinates.
8. **BIND — Norwalk (stop 25)**: exact landing = Sheffield Island ferry dock at Hope Dock. Update stop label/landing field.
9. Port Washington Town Dock: keep, phase 3 unchanged. (Commercial-use permission note is internal-only — do NOT render.)

## Gates (unchanged)
- Zero invented landings; dock/permission status never in rendered DOM; locked numbers, calculator, LOI untouched; trip planner must not route through culled stops.

## QA acceptance
- Culled stops absent at every phase toggle state and in trip-planner stop lists.
- Southeast Bay Line continuous, water-only, ends at OP.
- North Bay Express continuous post-Hercules.
- Ferry Point Park pin at true landing; no land chords introduced.
- Build passes `build-employer-hubs.mjs` asserts; redeploy `_dist`.
