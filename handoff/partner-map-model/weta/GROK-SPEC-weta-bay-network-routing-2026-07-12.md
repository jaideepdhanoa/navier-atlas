# Grok handoff — WETA Bay network exact IDs and water-safe geometry

**Date:** 2026-07-12  
**Live deck:** `1frwn6G6NrGdzxbJEqlO_EZ6M-vWF2dLYN8PWhGwHRpw`  
**Canonical city:** `san-francisco-bay-area-usa`  
**Canonical cluster:** `san-francisco-bay-usa`

## Mandate

Preserve the deck’s three distinct states: **existing WETA service**, **WETA-published expansion**, and **Navier candidate screen**. Do not turn a screen into an operating claim. Corridors are geography-owned; add any accepted route once to the global canonical graph, then inherit it through the Bay cluster.

## Exact bindings already present

### Existing WETA service context
- `rn-cabe543d04e9` — San Francisco Ferry Building → Oakland – Jack London Square · `bp-b42a6feee3` → `bp-bb594ccb97` · 5.5 nm
- `rn-e160b7ec05a5` — San Francisco Ferry Building → Alameda – Main Street · `bp-b42a6feee3` → `bp-ac1a92d1e7` · 5.4 nm
- `rn-91fd068e22f6` — San Francisco Ferry Building → Richmond Ferry Terminal · `bp-b42a6feee3` → `bp-20bbecd2a7` · 7.2 nm
- `rn-b8709495c648` — San Francisco Ferry Building → Vallejo Ferry Terminal · `bp-b42a6feee3` → `bp-06b627e7b0` · 19.1 nm
- `rn-a82989283656` — San Francisco Ferry Building → Harbor Bay (Bay Farm Island) · `bp-b42a6feee3` → `bp-983f05f18e` · 7.6 nm
- `rn-c0b8c9297a26` — San Francisco Ferry Building → South San Francisco (Oyster Point) · `bp-b42a6feee3` → `bp-28fc89a0d1` · 7.9 nm

### WETA-published expansion context
- `rn-ea80446d67a4` — San Francisco Ferry Building → Mission Bay (16th St / China Basin) · `bp-b42a6feee3` → `bp-6f4ad8afd4` · 1.6 nm
- `rn-1ffa4b3d5058` — San Francisco Ferry Building → Treasure Island · `bp-b42a6feee3` → `bp-6ecdc3f062` · 1.8 nm
- `rn-38c306488017` — San Francisco Ferry Building → Berkeley Marina · `bp-b42a6feee3` → `bp-1a167470ce` · 5.5 nm
- `rn-0c9c5c290e05` — San Francisco Ferry Building → Port of Redwood City · `bp-b42a6feee3` → `bp-8331815f23` · 19.5 nm

## Candidate connection status

- **Oakland – Jack London Square → South San Francisco (Oyster Point)** — route `rn-5cd7878b37e0`; exact_route_present_geometry_recheck_required.
- **Alameda – Main Street → South San Francisco (Oyster Point)** — route `null`; pending_global_canonical_mint.
- **Oakland – Jack London Square → Port of Redwood City** — route `null`; pending_global_canonical_mint.
- **Alameda – Main Street → Port of Redwood City** — route `null`; pending_global_canonical_mint.
- **Port of Redwood City → Palo Alto Boat Launch** — route `null`; pending_global_canonical_mint.
- **Palo Alto Boat Launch → Alviso Marina County Park** — route `null`; pending_global_canonical_mint.
- **San Leandro candidate public landing → Mission Bay (16th St / China Basin)** — route `null`; pending_global_canonical_mint.
- **San Leandro candidate public landing → South San Francisco (Oyster Point)** — route `null`; pending_global_canonical_mint.

## Endpoint corrections / holds

1. **Alameda Main Street:** current main contains both a source-backed terminal POI and a route-aligned approximate duplicate. Verify the official WETA terminal coordinate, then repoint/rebind. Do not keep the approximate Oakland-side point just to preserve an ID.
2. **San Leandro:** no trustworthy public landing is bound in current main. The only name hit is a dispensary and is explicitly excluded. Keep the BP and all connected route IDs `null` until an authoritative waterfront facility is sourced.
3. **South Bay candidates:** Coyote Point, Palo Alto and Alviso have exact canonical POI IDs in the ledger, but no candidate route IDs. They are screen-only anchors, not commitments.

## Geometry work

- Hand-waypoint marked navigation spans at Bay bridges; never interpolate across pier fields.
- Respect Coast Guard VTS and deep-draft traffic lanes; cross at right angles.
- Follow dredged channels around San Bruno Shoal and through Redwood City / Palo Alto / Alviso approaches.
- Hand-waypoint Oakland–Alameda estuary entrances and all terminal basins; add low-wake approach segments.
- Preserve `interior_land_km == 0`; run no-orphan, duplicate, water-adjacency, inheritance, and rendered-map checks.

## Acceptance

- Existing / published / candidate labels remain distinct in data and rendered copy.
- Every accepted BP has an exact canonical ID and an authoritative facility source. Where current canonical metadata lacks that source, verify it before treating the candidate as bound; unsupported points remain `null`.
- Every accepted candidate route is added to global `ROUTES.json` under `san-francisco-bay-usa`, not to WETA alone.
- All geometry gates pass with zero land crossings and a visual render receipt.
- Return the final route/BP ID table, waypoint file, before/after Bay route count, and unresolved-null ledger.

The machine-readable companion is `WETA-BAY-NETWORK-EXACT-ID-LEDGER-2026-07-12.json`.
