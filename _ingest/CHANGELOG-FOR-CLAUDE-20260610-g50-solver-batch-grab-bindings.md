# CHANGELOG FOR CLAUDE — 2026-06-10 — Gold #50: water-solver batch + Grab featured-route bindings

Base = Gold #49 (`navier-export-20260610T060619Z.zip`, ROUTES 5,269). Built per
`finance/recal/G50-APPLY-SPEC.json` (LB-67 overlay-only: full #49 unzip → overlay changed blobs).
**Route count 5,269 → 5,276 (+7 mints; 11 in-place geometry repairs; 0 removals).**

## 1. Japan geo-mistag cleanup (LB-72; `_apply_japan_geomistag_g50.py`)
Labels/tags only — geometry byte-untouched:
- 3 routes re-tagged yaeyama-japan → miyako-japan city_ids (ics-3ed6bb6bab, ics-9d0ef0ab38, ics-b5f8142d64) — endpoints are Irabu/Miyako, not Yaeyama.
- 4 routes (ics-22d4c113a1, ics-9adee8a725, ics-b5f8142d64, ics-e689847025): "Uruma" endpoint labels → "Ikema Island" (reverse-geocode: Pref. Road 230 = Ikema Bridge); ics-b5f8142d64 from-label → "Irabu — Sawada". 9 field fixes total.
- bp-8dd3ce6667 (Katsuren causeway piers, operator "Uruma City") parent_city_id miyako-japan → okinawa-main-japan.

## 2. Geometry repairs — 11 existing routes (solver arcs, `finance/recal/water-solver-20260610/`)
distance_nm recomputed from routed arc (haversine, 1dp):
| route_id | old nm | new nm |
|---|---|---|
| edge__hvar-croatia__split | 24.8 | 25.2 |
| e__naples-capri…__marina-grande__…__amalfi-harbour | 17.3 | 17.5 |
| e__milos…__adamas__…__parikia | 47.8 | 49.4 |
| ics-4554674195 (Bora Bora–Apooiti) | 21.3 | 33.4 |
| ics-2fd7c1b2c3 (Bora Bora–Uturoa) | 23.5 | 36.4 |
| rn-c3bf27d8ed75 (Fujairah–Zighy) | 33.2 | 35.3 |
| rn-77894ba04cf9 (Lima–Dibba) | 22.5 | 24.7 |
| rn-b1553fad7fc5 (Zighy–Daba) | 3.6 | 3.8 |
| rn-09d53e163d32 (Zighy–Dibba Al-Hisn) | 5.3 | 6.4 |
| rn-056850d614cc (Zighy–Lima) | 19.8 | 20.5 |
| rn-98dd58a5b283 (Zighy–Port Dibba) | 5.8 | 6.7 |

The Musandam set retires the LB-57 "straight-line clips headland" deferral class for these corridors.

## 3. Mints — 7 fresh routes (LB-71 pattern; `_apply_solver_batch_g50.py`; all bidirectional=true)
| route_id | corridor | nm | vessel |
|---|---|---|---|
| ics-423b647c48 | SG HarbourFront Centre FT → Batam Centre Intl FT | 21.8 | Pioneer II (cross_border) |
| ics-5a042a6812 | Jakarta: Ancol Marina → P. Untung Jawa Dermaga Dishub | 12.4 | Pioneer II |
| ics-321d7c7ebb | Jakarta: Ancol Marina → P. Sepa Resort Jetty (outer Seribu) | 38.9 | Pioneer II |
| ics-2c5451236c | Jakarta: P. Untung Jawa → P. Sepa Resort Jetty | 26.6 | Pioneer II |
| ics-0b3b436e41 | Mombasa Old Port Jetty → Diani Beach Landing | 17.2 | Pioneer II (reef-pass caveat carried in notes) |
| ics-9af3f8289c | Stone Town FT (Zanzibar) → Mkoani Port (Pemba) | 61.5 | Pioneer II (≤70nm cap) |
| ics-739626bfb0 | Palma Port → Mahon Port | **100.2** | Quanta-LR, amber_dashed, H2_2026_plus |

All endpoints solver-verified (OSM refs in each geojson's properties). CLUSTERS untouched —
all endpoint city_ids already gold cluster members (verified; gate_city_ids PASS).

**ANOMALY — palma-mahon:** the ruled "78nm port-to-port" is below the 80.1nm great-circle,
which crosses Mallorca's interior — the ruling was evidently straight-line. True over-water
minimum ≈100nm via Cap Blanc / Cap de ses Salines (clears Cabrera ~4nm). Minted at routed
**100.2nm** per spec rule "use routed nm from arc". Quanta-LR classification unchanged (>70nm).

**NOTE — Batam bp:** gold `bp-d89cb47bc4` ("International Ferry Terminal Batam Centre") sits at
(106.789, −6.284) = JAKARTA, parent_city_id=jakarta-indonesia — a Places mis-geocode ~570nm from
the real terminal (104.055, 1.132, OSM n8396655666). NOT reused (spec's coords-match condition
failed); fresh bp ids minted route-side. The stale POI itself is left for a future cleanup pass.

## 4. Grab featured-route bindings (`_apply_grab_bindings_g50.py`)
`data-clean/partners/grab.json` featured_routes bound **6/81 → 59/81** (54 bound this pass,
16 honest nulls `_link_status=aspirational-no-built-route`, 5 pre-existing binds kept).
Mirrored into `partner-pitch/partners/grab.json` (featured/journey fields only; committed-floor
economics untouched). *Build-order figure "was 9/69" was stale — actual #49 base = 6/81.*
- Confirmed overrides (Jaideep 2026-06-10): SG↔Desaru rn-ef7c059adbde 11.5nm; SG↔Bintan
  rn-f3670ea7d99b 21.9; KK↔Gaya rn-9d4c519ed0df 8.0 (rebind off generic rn-1cdc5ab26bb3);
  KK↔Mantanani rn-2e3ad6eee692 49.2; Phuket→Phi Phi ics-8c6c7ae8ee 22.7; SG↔Batam → mint
  ics-423b647c48 21.8; Jakarta Seribu trio → mints (12.4 / 38.9 / 26.6).
- Geometry-first deviations (documented in script header): Marina↔Sentosa bound ics-69bad8b4c9
  (not retired rn-442eeed97df4); GT↔Butterworth bound ics-7146c7b16e (real cross-strait corridor,
  not the 0.3nm Butterworth-side hop); PhuQuoc↔AnThoi left null (checklist id fails label↔geometry).
- P2 honest nulls kept null: Marina↔Ubin direct, Lombok↔Labuan Bajo, Manila↔Coron/El Nido,
  Cebu↔Boracay, Saigon↔Vung Tau, Kaohsiung↔Cijin, SG↔Riau QLR, SG/Desaru↔East-MY QLR,
  Penang↔Pangkor, Langkawi↔Koh Lipe, KK↔Labuan, KK↔Mengalum, HCMC BachDang↔ThuDuc, GT↔Batu Ferringhi.

## 5. gate_route_id remediation (12 pre-existing dry-run failures → 0; `_fix_gate_route_id_items_g50.py`)
All present in promoted #49; fixed geometry-faithfully (no route_id flips, no economics):
- constance.json ×3: distance_nm 22 → 29.0 (e__mald__cf81f3109b09 arc was rebuilt to 29.0nm in the #48 Maldives recal; display value was stale).
- grab.json ×1 + singapore-mpa.json ×2 (rn-ef7c059adbde SG↔Desaru): item node pair aligned to the gold route's city pair (singapore, singapore).
- qatar.json ×6: from/to_node_id sub-node keys (`doha-qatar__…`) → plain city ids, the file's own passing convention; sub-node detail remains in labels.

**REVIEW FOR CLAUDE:** rn-ef7c059adbde's `to_city_id="singapore"` on a Malaysian-side endpoint
(104.066, 1.456 — Desaru/Johor) is an LB-67 tri-border coord-classifier artifact. Items were
aligned to the gold property for gate consistency; the route property itself deserves a
geometry-first re-classification pass (desaru-coast-malaysia is a valid gold node).

## 6. Gates & audit (all green)
- `gate_endpoint_labels.py`: **0 HARD** / 13 WEAK single-token (same known-benign set as #48/#49: sentosa/changi/desaru/singapore×2/cebu/manukan/gaya/mantanani/nujuma×4; build-order's "9" was stale).
- `gate_city_ids.py`: **PASS** — 198 valid nodes, 5,276 routes, 75 clusters, all city_ids resolve.
- `gate_route_id.py`: **0 featured / 0 journey nulled** (331 binds all pass distance + endpoint gates) after §5 fixes.
- datastore_audit: see seal report (run post-zip on synced live data-clean).

## 7. Economics sidecar (LB-28)
97 resolved / 5 pending (`endpoints_city_level_not_pinned` grab honest defers — unchanged set).
By partner: grab 31, careem 14, jih-global 43, qatar 3, red-sea-global 2, saudi-redsea-pif 4.
Grounded 54 / estimated 36. Copied to `finance/economics_by_route_id.latest.json`. New mints add
no records (no committed corridor rows — record-neutral by design, cf. Gold #45 lesson).

## 8. NOTE FOR CLAUDE — front-end rebuild required
**The deployed Atlas build is still baked from pre-recal data**: it shows pre-recal vessel counts
(e.g. SG Phase 3 "148 vessels") and unbound SG featured routes. Rebuild the front end from THIS
zip (`data-clean/` surface: ROUTES 5,276 + partners/grab.json 59/81 bound + economics sidecar 97)
to pick up the recal vessel counts and the new Grab route highlights.
