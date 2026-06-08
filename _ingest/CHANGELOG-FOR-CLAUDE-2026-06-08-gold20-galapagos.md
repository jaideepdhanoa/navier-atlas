# Gold #20 — Galápagos inter-island heroes (autonomous lane, market #2)

**Date:** 2026-06-08
**Base:** Gold #19 (Catalina)
**Method:** `_solve_corridor_waypoints` offline solver-splice (LB-34) — no full build.

## What changed
- **+2 hero routes** (5213 → 5215), connecting 3 previously-orphan Galápagos island pins.
- No new city nodes or POIs — all 3 ferry ports already existed as gold POIs.

## Heroes (real open-water arcs, both N30 Pioneer II ≤70nm)
- **Puerto Ayora (Santa Cruz) ↔ Puerto Villamil (Isabela)** — 42.5 nm, land 0.0 km
- **Puerto Ayora (Santa Cruz) ↔ Puerto Baquerizo Moreno (San Cristóbal)** — 44.0 nm, land 0.40 km

## Network-authenticity decision
- Galápagos public inter-island lanchas run **hub-and-spoke through Santa Cruz** (the central island). Isabela ↔ San Cristóbal (81 nm) is **omitted**: it exceeds Pioneer II range AND is not a real direct public route (passengers transit via Santa Cruz). Null beats confidently-wrong.

## Economics
- Sidecar unchanged at **69 records** (geometry-only hero; no partner finance corridor).

## Front-end note
- Routes are `edge_class: inter-city`, rendered bidirectional `↔` on the front end (authoring stays directional). Endpoints reference existing Galápagos port POIs.
