# Gold #23 — San Juan Islands + Cape Cod & the Islands (autonomous lane, US batch)
Base: Gold #22. Method: `_solve_corridor_waypoints` solver-splice (LB-34/36 pattern).
+6 inter-island heroes (5218->5224), all N30 Pioneer II, all gate-pass <=1.0km land.

**San Juan Islands (Puget Sound cluster):**
- Anacortes Ferry Terminal <-> Friday Harbor — 21.2nm (land 0.916km)
- Friday Harbor <-> Orcas Island Ferry Terminal — 5.2nm (land 0.898km)
- Anacortes Ferry Terminal <-> Lopez Island — 19.9nm (land 0.453km)

**Cape Cod & the Islands (Boston & New England cluster):**
- Hyannis Terminal <-> Nantucket (Steamship Wharf) — 24.1nm (land 0.0km)
- Hyannis Terminal <-> Oak Bluffs (Martha's Vineyard) — 17.7nm (land 0.0km)
- Nantucket (Steamship Wharf) <-> Vineyard Haven (Martha's Vineyard) — 27.1nm (land 0.0km)

All ports pre-existed as gold POIs (sourced under seattle-puget-sound-usa / boston-new-england-usa)
but were orphan-unconnected. Both clusters now live. Renders bidirectional on front end.

**Deferred:** Anacortes<->Orcas direct (a real WSF run) — A* exceeded solver budget in the dense
San Juan archipelago. Orcas is already network-connected via Friday Harbor<->Orcas, so no orphan.
Follow-up: curated channel-waypoint construction (same as deferred UAE lagoon edges).

Sidecar unchanged at 69 (geometry-only heroes carry no finance corridor).
