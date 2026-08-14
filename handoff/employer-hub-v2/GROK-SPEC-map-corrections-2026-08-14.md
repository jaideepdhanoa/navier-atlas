# GROK SPEC — Employer hub map corrections + marina-standard refinement (2026-08-14, v2)

**v2 note:** Supersedes the morning version. The landing gate is corrected: Navier needs a usable
**pier / marina berth** (30–45 ft vessel, adequate low-tide depth, open dock, navigable access) —
NOT a ferry terminal. Both hub networks were re-audited under this standard (audits in `inputs/`).
The 4 culls hold even under the relaxed standard, and the sweep adds verified marina-grade stations.

## A · Bay Area (`employer-hub/hubs/bay-area/hub.json`)

### Culls (all re-verified — fail even at marina standard)
1. **CULL — Alviso Marina** (stop 5): silted, kayak-grade slough. No usable landing exists south of Redwood City. Peninsula Trunk full-network terminus = Port of Redwood City.
2. **CULL — Hayward Landing** (stop 11): no dock or marina anywhere on Hayward shoreline.
3. **CULL — San Leandro Marina** (stop 12): permanently closed Jan 2023, docks removed.
4. **CULL — Hercules Waterfront** (stop 17): ferry dock never built; Rodeo and Crockett marinas also closed/derelict.

### Replacements & additions (all source-verified OPEN, see `inputs/BAY-REFINEMENT-AUDIT.md`)
5. **ADD — Martinez Marina** (phase 3): replaces Hercules on North Bay Express. 332 slips 20–45 ft, guest dock. Spine: Antioch → Pittsburg → Martinez → Benicia → Vallejo → Richmond → Berkeley → Emeryville → TI → FB.
6. **ADD — Antioch Marina** (phase 3): North Bay Express eastern terminus. Guest + 100-ft public dock, deep San Joaquin channel.
7. **ADD — Brisbane Marina / Sierra Point** (phase 2, Peninsula Trunk between Oyster Point and Coyote Point): 250-ft guest dock; serves Sierra Point biotech campus + Brisbane.
8. **ADD — South Beach Harbor / Pier 40** (phase 2, Peninsula Trunk between Ferry Building and Mission Bay): 640-ft guest dock; SoMa/South Beach residential + Oracle Park district.
9. **RE-SPINE — Southeast Bay Line**: Jack London Square → Main St Alameda → Harbor Bay → Oyster Point (phase 2).

### Watchlist (do NOT render; keep in comments/data notes only)
Petaluma Turning Basin (dredged Nov 2025 — seasonal/leisure lane candidate), Napa Main Street Dock (tide-limited), Pier 39 Marina (dredging closure to Sep 2026), SF Marina West Harbor (sandbar; re-check after Fall 2026 dredge), Ballena Isle & Suisun City (MAYBE).

## B · New York (`employer-hub/hubs/new-york/hub.json`)

### Corrections (unchanged from v1)
10. **RENAME — "Throgs Neck" (stop 21) → "Ferry Point Park"**; pin at the true landing.
11. **BIND — Norwalk (stop 25)**: landing = Sheffield Island ferry dock at Hope Dock.

### Additions (all source-verified OPEN, see `inputs/NY-REFINEMENT-AUDIT.md`)
12. **ADD — Yonkers Recreation Pier** (phase 2): new Hudson line stop → Midtown West/BPC. 211k-person city, Metro-North adjacent, prior ferry history. If no Hudson line exists, spine a 2-stop Hudson Express: Yonkers → W 39th St → Battery Park City.
13. **ADD — New Rochelle Municipal Marina, Echo Bay** (phase 2): join LI Sound / Ferry Point line toward E 34th. 10 ft depth, daily dockage.
14. **ADD — Liberty Landing Marina, Jersey City** (phase 2): Gold Coast line, Morris Canal catchment. 520 deep-water slips.
15. **ADD — Newport Marina, Jersey City** (phase 3): 400-ft floating dock between Paulus Hook and Hoboken.
16. **ADD — Bridgeport Harbor Marina / Steelpointe** (phase 3): Connecticut Express eastern extension. New deep-water marina, CT's largest city.
17. **ADD — Milford Lisman Landing** (phase 3): CT Express extension beyond Bridgeport. 7 ft MLW city marina, walkable downtown.
18. **ADD — Moonbeam Great Kills Marina, Staten Island** (phase 3): new South Shore Express → Wall St (Pier 11). 15-ft floating docks.

### Held / watchlist (do NOT render)
- **Atlantic Highlands Municipal Harbor**: verified usable, but Monmouth = Seastreak incumbency → stays partner-lane, off-map (existing gate).
- **Marine Basin Marina (Bensonhurst)**: selling commercial berths but depth unpublished — site-visit gate before mapping.
- Reopening watch: W 79th Boat Basin + Dyckman (~2028), North Cove Marina (2026 redevelopment), World's Fair Marina (closed), Sheepshead Bay (NYC Parks PUDO ban — regulatory), New Haven Long Wharf (rebuild 2026–27).
- **Internal flag (not rendered): Lincoln Harbor (stop 8) under construction** — confirm berth assignment before service start.

## Gates (unchanged)
Zero invented landings; dock/permission status never in rendered DOM; locked numbers, calculator, LOI untouched; trip planner must not route through culled stops; water-only geometry for all new segments.

## QA acceptance
- 4 culled stops absent at every phase state and in trip-planner lists.
- All 11 additions render at their assigned phase with exact landing names above; pins on the true dock.
- North Bay Express continuous Antioch→FB; Hudson Express / South Shore Express / CT extension water-only, no land chords.
- Catchment panel counts update per phase; build passes `build-employer-hubs.mjs`; redeploy `_dist`.
