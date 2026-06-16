# CHANGELOG — Gold #79ad — UAE Phase 2/3 Marjan / Sharjah / AD-trunk enrich (2026-06-16)

**Bite:** `P2P3-marjan-sharjah-trunk` · **Base:** #79ac (`navier-export-20260616T150428Z-uae-p2p3-abu-dhabi-islands.zip`, 5198 routes)
**Method:** LB-67/81 zip-patch overlay (ROUTES.json whole-file only) onto extracted #79ac base. Live `data-clean/` chronic-stale/skeletal per LB-192a (holds only economics + partners — no SEAL/ROUTES) → gold extract is canonical splice base; base-gold drift logged, proceeded on extract. LB-171/LB-174: SEAL recomputed on actual blob bytes.

## Counts vs #79ac
- ROUTES:   5198 → **5201** (Δ +3 new, 0 removed, 0 edits)
- POIs:     10646 → 10646 (Δ 0 — 0 new BPs; all 4 endpoints pre-existing)
- CLUSTERS: 107 → 107 (Δ 0 — 0 new clusters)
- CITIES 176 → 176 · PRIORITY_CITY 37 → 37 (unchanged)

## Enrich — 3 new Pioneer II inter-emirate corridors (0 new BPs — all endpoints reused, LB-55 multi-channel)
- `rn-dd4500aa99f5` **Dubai Harbour Marina (Dubai) → Wynn Al Marjan Island arrival lagoon (Ras Al Khaimah)** — 56.0 nm, regional, marquee tourism corridor (Wynn Al Marjan opening anchor). Endpoints bp-56d5f5bd8d ↔ bp-29c2c81221.
- `rn-a5ac4f587aee` **Dubai Harbour Marina (Dubai) → Marina Mall / Breakwater Marina (Abu Dhabi)** — 59.8 nm, trunk, Dubai↔Abu Dhabi business spine. Endpoints bp-56d5f5bd8d ↔ bp-b3458dd3c6.
- `rn-01b4a3efaf0f` **Dubai Harbour Marina (Dubai) → Al Khan Lagoon mouth (Sharjah)** — 25.1 nm, trunk, Sharjah adjacency commuter. Endpoints bp-56d5f5bd8d ↔ bp-f0fde14967.
- Fujairah east-coast retention: no-op (no corridor change this bite).

## Seal gates — ALL PASS
- `gate_city_ids`: PASS (211 nodes / 5201 routes / 107 clusters / 0 unresolved).
- `gate_premint_pair`: 0 / 5201 flagged @0.5.
- `gate_cluster_anchor_realbp --check-only`: PASS=105 WARN=2 FAIL=0 (great-lakes-usa / shanghai-china synthetic-no-BP WARN by design — baseline preserved).
- `gate_osm_noise_bp --check-only --global`: PASS (0 safe kills; 29 advisory route-referenced carry — 0 new).
- `gate_partner_rationale_leak`: clean.
- **UAE land gate** `qa_land_crossing` over the 3 new corridors: **0 / 3 FAIL** (fine-OSM uae_gulf_land.wkb interior land 0.000 km on all 3 per manifest; coarse 0/3). Full-file coarse FAIL 219/5201 = unchanged from #79ac (219/5198) — pre-existing island-hop carries, 0 new from this bite.
- `gate_endpoint_labels`: 4 HARD carry-forward (Philippines + uae-careem + uae-luxury×2; FLAG_MISSING_IN_GOLD dangling corridor binds — unchanged since #79w) / 3 WEAK advisory — **0 NEW**. Note: the uae-luxury "Dubai Harbour Marina → Wynn Al Marjan" corridor in corridors.json still pins stale `rn-f94dae947809`; the new geometry id is `rn-dd4500aa99f5` — re-pin owed in the standing label-fix bite.
- LB-175a pre-build: ROUTES 5201 ≥ floor 5072 (margin 129) ✓ / pier-coord verification on the 4 reused endpoint BPs ✓ (DH 0.15nm, Wynn 0.0, Breakwater 0.0, Al Khan 0.75nm water-snap).

## Economics sidecar (LB-28)
**Carried forward unchanged** from #79ac (78 route-pinned / 48 `_pending_route_pin`). Deterministic resolution check: the 3 new corridor endpoint-pairs match **0** pending corridors-of-record (the 3 inter-emirate trunks are not partner economics corridors; ID/endpoint-based resolution yields 0 newly-pinned) → record set byte-identical; sidecar sha256 unchanged. Carrying the #79ac sidecar (built from fresh full-recipe aggregates) avoids regressing the record set vs a stale-aggregate rebuild.

## SEAL
LB-171 recompute on actual blob bytes. meta.gold 79ac → **79ad**. Pre-existing carries logged: 5 duplicate `ics-*` route ids (ics-3c55ce6e65/5d9f47b3c4/b7b04ed77d/be4a12ba5c/e33d21f71e — identical to #79ac, NOT introduced here); Oman-Musandam points filed under `fujairah-uae` (upstream geo carry).
