# Gold #26 — Region-label cleanup + Mombasa orphan fill (autonomous lane housekeeping)
Base: Gold #25.

## Region-label cleanup
- 35 POIs had `region = null`. Filled by inheriting from `parent_city_id` (exact ID match):
  34 -> Europe (Ionian/Cyclades/Aeolian/Sporades/Tuscan/Pontine/Ligurian clusters),
  1 -> LatAm-Caribbean (Panama City under san-blas-panama). Zero null regions remain.

## Mombasa orphan fill (5217->5219... -> 5227->5229)
- `mombasa-kenya` was an orphan node (5 POIs, 0 routes). Now connected, +2 heroes, N30 Pioneer II:
  - Mombasa Old Port Jetty (Old Harbour) <-> Mtwapa Creek Jetty (The Moorings) — 11.4nm (coastal, solver, land 0.314km)
  - Likoni Ferry: Mombasa Island <-> Likoni Mainland — 0.3nm (the iconic direct crossing, clean straight line)

## Deferred
- Shanghai (`shanghai-china`, 4 POIs, orphan): the flagship Shiliupu Wharf <-> Wusongkou Cruise
  Terminal run (10.9nm) is on the Huangpu River, which is NOT in the solver's ocean mask
  (gen_anchors=0) — same class as the Great Lakes (LB-40). Needs curated river-channel waypoints
  (the Huangpu bends, so a straight line would cross land). Curated-waypoint follow-up.

## Remaining orphan nodes (need fresh BP sourcing before geometry)
0-POI cluster nodes: Chios/Samos, Halkidiki, Koh Kood (Soneva Kiri), Fukuoka, El Nido/Bacuit Bay,
Mafia Island, Pemba Island; + 7 single-jetty bp-* nodes (Amanpulo, Sir Bani Yas Anantara,
Daymaniyat, Coron Pier, Puerto Princesa, Tagbilaran, El Nido bangka).

Sidecar unchanged at 69.
