# Gold #40 — Mexico: Playa del Carmen ↔ Cozumel (+1 route)

**Base:** Gold #39 (5,211 routes) → **5,212 routes** (+1).

## What changed
Added the **iconic Caribbean ferry corridor — Playa del Carmen ↔ Cozumel** (9.5nm, Pioneer II).
First-class desired corridor that previously had no network leg.

| Route id | nm | Vessel |
|---|---|---|
| `e__playa-del-carmen-mexico__playa-del-carmen-ferry__cozumel-mexico__cozumel-ferry-san-miguel` | 9.5 | Pioneer II |

- Endpoints = **Nominatim named ferry terminals**: Terminal Marítima de Playa del Carmen (-87.0750, 20.6209) and Ferry Cozumel, San Miguel (-86.9514, 20.5125). Satellite-verified deep-water crossing.
- Two new `mexico` cluster members: `playa-del-carmen-mexico`, `cozumel-mexico` (added to CLUSTERS.json + source city-cluster-map; CLUSTERS blob re-hashed). Both lack city_briefs (content-lane follow-up).

## Why it was a false-null in Lane G (resolver improvement)
The multi-channel resolver tiered on **Wikidata↔Mapbox agreement**. For Playa & Cozumel, Mapbox
returned wrong inland homonyms (El Carmen, Nuevo León / Cozumel St., Morelos), so the pair nulled —
even though Nominatim had nailed both ferry terminals. Added a **WD+Nominatim-agreement and
Nominatim-in-bbox promotion path** to the recipe (LB-58). This also recovered Khasab, Bastia,
Sveti Stefan, Diani, etc. (most of those are deferred — held Quanta-LR or need the water solver).

## Also confirmed (no action — dup-guard catch)
The Galápagos inter-island corridors (Puerto Ayora↔Villamil, Ayora↔Baquerizo) **already exist** in
the gold (built Gold #20 with correct boarding points). The Lane-G need-list "tag-only" label was
stale. Not re-added.

## Deferred (honest holds)
- **Mombasa ↔ Diani** — straight line runs overland down the coast (satellite-confirmed); needs the water-following solver.
- Dibba↔Zighy, Khasab fjord hop, Montenegro bay hops (Sveti Stefan) — coastal/headland, need the water solver.
- Palma↔Mahon (78nm), Fukuoka↔Busan (119nm), Zanzibar↔Pemba/Wete (87nm+), Côte d'Azur↔Corsica (~95nm) — held Quanta-LR (>70nm).

Geometry is great-circle; re-solve through the high-memory land-gate when available. Endpoints + topology authoritative now.
