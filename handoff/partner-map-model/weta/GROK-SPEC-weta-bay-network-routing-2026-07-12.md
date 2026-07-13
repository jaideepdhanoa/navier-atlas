# Grok handoff — WETA Bay route repair, hand-waypoints, and shuttle expansion screen

**Date:** 2026-07-12  
**Live deck:** `1frwn6G6NrGdzxbJEqlO_EZ6M-vWF2dLYN8PWhGwHRpw`  
**Canonical city:** `san-francisco-bay-area-usa`  
**Canonical cluster:** `san-francisco-bay-usa`

## Answer to the routing question

The earlier handoff had the right exact-ID/null discipline, but it was not explicit enough about geometry work. The canonical file `data-clean/pta_hand_waypoints_sf_bay_ferry.json` currently lists 17 route pairs with **empty waypoint arrays**. Current route metadata reports zero interior land distance, but that does not prove a route passes through the correct bridge span, avoids marsh/shoreline, follows a dredged channel, or enters a terminal basin safely.

Treat this as three separate lanes:

1. **Repair existing canonical service geometry and endpoints.**
2. **Mint selected WETA-published and Navier-screened routes globally.**
3. **Research/screen additional North, East and South Bay boarding points; do not mint routes to unsuitable or unapproved facilities.**

The machine-readable queue is `WETA-BAY-SHUTTLE-CANDIDATES-AND-WAYPOINT-GATE-2026-07-12.json`.

## Lane A — repair/mint first

### A1. Alameda Main Street endpoint correction

Current routes use approximate `bp-ac1a92d1e7` at `[-122.2792, 37.7906]`. Canonical source-backed `bp-98bb5bad66` is Main Street Alameda Ferry Terminal at `[-122.293984, 37.790723]`. Verify against WETA’s official terminal record, repoint/rebind all affected routes, and retire/dedupe the approximate endpoint. Do not preserve the wrong point merely to retain an ID.

### A2. Alameda Seaplane Lagoon current-service route

WETA officially operates Downtown San Francisco ↔ Alameda Seaplane Lagoon, and exact canonical POI `bp-3f1c5e31c4` exists. There is no correct `rn-*` route in the exact-ID ledger. Mint/bind San Francisco Ferry Building `bp-b42a6feee3` ↔ Seaplane Lagoon `bp-3f1c5e31c4` as **existing WETA service**, through the Bay Bridge navigation span and Alameda terminal-basin approach.

### A3. Oakland ↔ Redwood City

WETA identifies Redwood City among near-term/Tier 1 expansion opportunities, and its project material reports passenger demand to Oakland and San Francisco. Mint Oakland `bp-bb594ccb97` ↔ Port of Redwood City `bp-8331815f23` as **WETA-published expansion**, not current service. Hard-waypoint the Oakland–Alameda estuary exit, traffic-lane crossing, San Mateo–Hayward bridge span, and Redwood City dredged channel.

## Lane B — mandatory hand-waypoint cases

Populate the currently empty Bay waypoint file. At minimum, explicitly review:

- **Bay Bridge:** Ferry Building ↔ Oakland, Alameda Main, Seaplane Lagoon, Harbor Bay, Oyster Point and Redwood City; Alameda/Oakland ↔ Mission Bay candidates. Pass through a marked navigation span, not a pier field.
- **Richmond–San Rafael Bridge:** northbound Vallejo/Mare Island/Delta routes and Richmond/Berkeley ↔ Larkspur candidates.
- **San Mateo–Hayward Bridge:** every route continuing to Redwood City, Palo Alto or Alviso. Use a marked navigation span.
- **Oakland–Alameda estuary / Bay Farm:** hand-waypoint basin exits and avoid straight segments across Alameda or Bay Farm. This is especially important for Oakland/Alameda/San Leandro ↔ Oyster Point/Redwood City/Mission Bay.
- **San Bruno Shoal / South Bay:** follow the usable approaches to Oyster Point, Coyote Point and Redwood City. No straight-line shoal cuts.
- **Redwood City / Alviso:** follow dredged/slough channels; do not cross marsh, salt ponds or shoreline polygons.
- **Larkspur:** use the Richmond–San Rafael marked span where applicable, then the Corte Madera Creek/Larkspur approach.

For every pair, either provide reviewed waypoint coordinates or an explicit reason why no intermediate waypoint is necessary. `[]` without an explanation is not acceptance evidence.

## Lane C — additional shuttle screen

### Strongest additions

- **Alameda Seaplane Lagoon ↔ Mission Bay** — exact existing/future WETA facilities; candidate pair only.
- **Harbor Bay ↔ Oyster Point** — exact existing WETA terminals; useful East Bay–Peninsula shuttle screen.
- **Oakland ↔ Mission Bay** — candidate only; WETA’s adopted Mission Bay pair is Downtown SF–Mission Bay.
- **Oyster Point ↔ Coyote Point ↔ Redwood City** — Peninsula chain screen. Coyote Point is an existing county marina, not a proven passenger terminal; facility/use/ADA/charging rights must be established first.
- **San Leandro Wes McClure Boat Launch ↔ Mission Bay / Oyster Point** — the City confirms a public launch ramp and canonical ID `bp-f6212541ea` exists. This replaces the prior “no facility found” state, but it remains a **site-conversion candidate**, not a passenger terminal.
- **Richmond ↔ Larkspur**, **Berkeley ↔ Larkspur**, and **Vallejo ↔ Larkspur** — North Bay regional-interchange screens. Larkspur belongs to Golden Gate Ferry/GGBHTD, so these require inter-agency coordination and cannot be presented as current WETA service.

### Holds

- **Palo Alto:** hold. Official city material describes the Baylands facility as hand launch for non-motorized/small craft. It is not an N30 passenger stop as-is.
- **Alviso:** retain only as a research screen. The county confirms a boat launch/floating docks, but tide, bathymetry, environmental constraints, passenger use and commercial operations remain unresolved.
- **Sausalito and Tiburon:** retain as Golden Gate Ferry context. Do not duplicate existing SF services as “new WETA routes”; only screen genuinely new cross-network links if both agencies support them.
- **Private marinas / false positives:** do not bind Emeryville/private yacht harbors or the San Leandro dispensary name match.

## Inheritance and labeling

Any accepted route is added once to global `ROUTES.json` under `san-francisco-bay-usa`, then inherited. Maintain four labels without drift:

1. existing WETA service;
2. WETA-published future/expansion;
3. existing Golden Gate Ferry context;
4. Navier candidate screen.

A candidate line is not a WETA route, terminal commitment, operating plan or approval.

## Acceptance return

Return:

- corrected/minted BP and route ID table;
- non-empty reviewed Bay waypoint file;
- before/after rendered Bay maps showing bridge spans and South Bay channels;
- `interior_land_km == 0` results plus bridge-pier/channel visual QA;
- duplicate/orphan/water-adjacency/inheritance checks;
- before/after Bay route count;
- facility-source ledger and unresolved-null ledger.

Do not write route IDs back to the deck/source until this return is green.
