# CHANGELOG — Gold #79ac — UAE Phase 2/3 Abu Dhabi Islands enrich (2026-06-16)

**Bite:** `P2P3-abu-dhabi-islands` · **Base:** #79ab (`navier-export-20260616T141821Z-uae-p2p3-dubai-showcase.zip`, 5189 routes)
**Method:** LB-67/81 zip-patch overlay onto extracted #79ab base (live `data-clean/` chronic-stale per LB-192a → gold extract is canonical splice base). LB-171/LB-174: SEAL recomputed on actual blob bytes.

## Counts vs #79ab
- ROUTES:   5189 → **5198** (Δ +9, 0 removed, 0 edits)
- POIs:     10644 → **10646** (Δ +2 new BPs)
- CLUSTERS: 106  → **107** (Δ +1: `abu-dhabi-islands`)
- CITIES 176 → 176 · PRIORITY_CITY 37 → 37 (unchanged)

## Enrich — 2 new minted BPs (Abu Dhabi islands had NO BP in base, L-UAE-06 Phase-2 flag)
- `bp-31b06c534d` **Lulu Island Jetty** [54.3475, 24.4945] — Nominatim+Mapbox <1nm agreement on 'Lulu Island'; jetty on south shore facing Corniche channel. conf 0.95.
- `bp-f47f75836a` **Reem Island Marina (Najmat / Marina Square)** [54.394, 24.4949] — Nominatim 'Marina Square, Al Reem Island'; Mapbox cross-check. conf 0.95.

## Enrich — 9 new corridors (8 Pioneer II commercial, 1 Quanta-LR held amber-dashed)
- `rn-c2a5e2033f94` Yas Marina → Saadiyat Beach Club Jetty (13.0nm, Pioneer II)
- `rn-6b584e8b2049` Saadiyat Beach Club Jetty → Marina Mall / Breakwater Marina (8.9nm, Pioneer II; fine-OSM re-solve)
- `rn-aef40f1a50bb` Marina Mall / Breakwater Marina → Al Bateen Marina (2.6nm, Pioneer II)
- `rn-afe7eee97714` Al Bateen Marina → Emirates Palace Marina (2.2nm, Pioneer II)
- `rn-4a56839963b5` Marina Mall / Breakwater Marina → Reem Island Marina (7.1nm, Pioneer II; fine-OSM re-solve)
- `rn-4d0113ef1fd5` Marina Mall / Breakwater Marina → Lulu Island Jetty (1.7nm, Pioneer II)
- `rn-0721cde8d55b` Al Bateen Marina → Hudayriat Marina (3.6nm, Pioneer II)
- `rn-00156f800fd5` Marina Mall / Breakwater Marina → Sir Bani Yas Cruise Port (**93.1nm, Quanta-LR HELD amber-dashed** — 75–150 band, not aspirational)
- `rn-08f29522c5f2` Jebel Dhanna / Ruwais Ferry Terminal → Sir Bani Yas Cruise Port (5.3nm, Pioneer II — real Jebel Dhanna ferry crossing)

## New cluster
- `abu-dhabi-islands` anchored on `bp-b3458dd3c6` (Marina Mall / Breakwater Marina, Corniche — real BP, LB-174). Sir Bani Yas + Al Ruwais kept as outlier nodes, NOT folded into core centroid.

## Seal gates — ALL PASS
- `gate_city_ids`: PASS (211 nodes / 5198 routes / 107 clusters / 0 unresolved).
- `gate_premint_pair`: 0 / 5198 flagged @0.5.
- `gate_cluster_anchor_realbp --check-only`: PASS=105 WARN=2 FAIL=0 (great-lakes-usa / shanghai-china synthetic-no-BP WARN by design — baseline preserved; AD cluster adds a PASS).
- `gate_osm_noise_bp --check-only --global`: PASS (0 safe kills; 29 advisory route-referenced carry — 0 new).
- `gate_partner_rationale_leak`: clean.
- **UAE land gate** `qa_land_crossing` over the 9 new AD corridors: **0 / 9 FAIL — 0.000 km coarse** (HARD gate). Fine-OSM re-verify per manifest: yas→saadiyat 0.755km, corniche→sirbaniyas 0.371km, both <1.0km thr; 2 corridors re-solved fine-OSM A* (saadiyat→corniche, corniche→reem) now 0.000km.
- `gate_endpoint_labels`: 4 HARD carry-forward (Philippines + uae-careem + uae-luxury×2, unchanged since #79w; FLAG_MISSING_IN_GOLD dangling corridor binds — owed a label-fix bite) / 3 WEAK advisory — **0 NEW** (bite adds no corridors.json binds).
- LB-175a pre-build: ROUTES 5198 ≥ floor 5072 (margin 126) ✓ / pier-coord verification on the 2 new endpoint BPs ✓.

## Economics sidecar (LB-28)
Rebuilt against new geometry via fresh full-recipe aggregates (grab/careem/jih-global/red-sea-global/saudi-redsea-pif/qatar). 78 route-pinned / 48 `_pending_route_pin` — records byte-identical to #79ab (0 prior-pinned lost AND 0 gained; the 9 new AD routes are intra-cluster/Western-Region, not partner economics corridors).

## SEAL
LB-171 recompute on actual blob bytes. meta.gold 79ab → **79ac**.
