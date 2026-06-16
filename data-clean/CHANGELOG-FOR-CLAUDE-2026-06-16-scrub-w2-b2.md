# CHANGELOG — Gold #79n — Wave 2 bite 2 scrub+enrich splice+seal (2026-06-16)

**Bite scope:** Caribbean — San Juan/Puerto Rico + St-Maarten/St-Barths + Antigua-Barbuda + St-Lucia/Grenadines.
Counterpart to staged delta from `navier-scrub-enrich-wave` subagent (`/tmp/scrub-wave-2-bite2/`). Sealed by `navier-scrub-wave-splice-seal` worker.

## Counts (Gold #79m -> #79n)

- Routes: 5,449 -> 5,438 (delta -11 = orphan-endpoint kills net of 31 new aspirational real-world Caribbean ferry mesh mints).
- POIs: 11,206 -> 11,192 (delta -14 = -27 OSM-noise BPs + 13 marquee enrich BPs).
- Cities: 170 -> 170 (no anchor-city mint this bite).
- Clusters: 83 -> 85 (delta +2 greenfield meta-clusters, single-member-start, LB-174-compliant: leeward-antilles-northern, windward-antilles).
- Sidecar economics_by_route_id.json: 82 records / 44 pending — unchanged vs #79m.

## Kills (27 BPs)

- san-juan-puerto-rico: 3 (Condominio Isleta Marina, Punta Cana Yacht Rentals PCYR, Yacht & You Punta Cana).
- st-maarten-st-barths: 9 (Harbour Rose, Harbour View Apartment, Christophe Harbour Development Co., Suite Harbour, Beautiful Craft Villa Harbour Views, ...).
- antigua-barbuda: 3 (Jolly Harbour Clearwater Villa 217b, Harbour View Apartment, Harbour View Heights Street).
- st-lucia-grenadines: 12 (Harbour Vista Inn, 17 The Harbour - 3 Bed Family Villa, Hess Oil Terminal, Clifton Harbour Oceanfront Guest House, Harbour View Drive, ...).

New noise pattern this bite: Caribbean "Harbour View ___" toponym chain — promote regex `view drive|house|street|look out` as noise_toponym_view.
Endpoint-protected rescues: 0 across all 4 metros (no overrides needed).

## Enrich (13 BPs, 31 routes, 2 greenfield meta-clusters)

13 new BPs minted (Mapbox+Wikidata+OSM grounding, LB-55):
- st-maarten-st-barths (2): Gustavia Public Ferry Dock (St-Barths), Charles A. Woodcock Memorial Harbour (Statia).
- antigua-barbuda (3): Barbuda Codrington Public Dock, Heritage Quay (St John's cruise_terminal), English Harbour Public Pier.
- st-lucia-grenadines (6): Fort-de-France Inter-Caribbean Ferry Terminal (Martinique), Vieux Fort Town Wharf, Soufriere Town Pier, Port Elizabeth Government Jetty (Bequia), Britannia Bay Public Dock (Mustique), Clifton Government Pier (Union Island).
- san-juan-puerto-rico (2): Esperanza Town Pier (Vieques), Dewey Public Dock (Culebra).

31 new routes — real-world Caribbean ferry mesh: Puerto Rico Ferry (Ceiba<->Vieques/Culebra Pioneer II + Vieques water taxi); St-Maarten/St-Barths/Statia (Voyager, Great Bay Express, Anguilla Ferries, Edge II, Calypso Charters, Saba Ferry, Makana Ferry); Antigua-Barbuda (Barbuda Express, Jaden Sun MV Admiral); St-Lucia/Grenadines (L'Express des Iles, Hi-Speed Ferries, Bequia Express, MV Admiral, Grenadines mesh, Martinique<->Castries).

2 new meta-clusters (single-member-start, LB-174):
- leeward-antilles-northern anchor [-63.0477, 18.0125] (Anguilla/St-Maarten corridor).
- windward-antilles anchor [-60.9952, 14.0144] (Martinique/St-Lucia corridor).

## LB-174 re-anchor sweep (4 Caribbean single-metro clusters)

Re-anchored to real cruise-port BPs. ~13 audit candidates remain across the system (carry-forward).

## Notable mints / advisory

- 13 new operator/brand rescue tokens slated for permanent RESCUE_PHRASES promotion: Voyager, Great Bay Express, Anguilla Ferries, Calypso Charters, Edge II, Saba Ferry, Makana Ferry, L'Express des Iles, Hi-Speed Ferries, Bequia Express, Barbuda Express, Jaden Sun, MV Admiral.
- Captive-marquee rescue pattern (NEW): for bp_type in {hotel_jetty, marina, cruise_terminal, yacht_club} with marquee-context tokens (resort/hotel/& spa/marina/yacht club), WEAK negatives (villa/suite/spa/inn) must be overridden. Promote to classify_marine_bp.py.
- Greenfield meta-cluster mint: single-member-start safe; widen later via member_city_ids without renaming.

## Gates (all PASS)

| Gate | Result |
|---|---|
| gate_endpoint_labels.py | 0 hard FLAG (3 pre-existing WEAK single-token binds carry: SG Marina Bay<->Changi, MLE Velana x2) |
| gate_city_ids.py | PASS — 205 valid nodes / 5,438 routes / 85 clusters; all 13 new BPs and 2 new clusters resolve |
| gate_partner_rationale_leak.py recursive over partner-pitch/partners/*.json | clean (0 hits) |
| gate_osm_noise_bp.py (advisory) on 4 bite-2 metros | 0 new flags (bite already scrubbed) |
| gate_premint_pair.py | 0 / 5,438 routes flagged — 3rd consecutive 0-flag at scale; LB-179 inline name-veto triangulation validated again |
| LB-175a pre-build (ROUTES >= floor 5,072 + pier-coord verify all 13 new BPs) | PASS |
| datastore_audit.py post-seal | PASS — 0 fail / 0 warn (DUAL-SEAL-WRITE applied per LB-182 standing rule) |

## Pre-existing carries (NOT introduced this bite)

- Oman cluster anchor orphan bp-095a41dfcb.
- Philippines cluster anchor orphan bp-d4738f6ad2.
- Wakatobi duplicate POIs.
- Re-anchor scheduled for upcoming bite.

## Phase-reorder + DUAL-SEAL-WRITE

Prior gold zip deleted BEFORE cp new zip (LB-181/LB-182 standing rule).
Recomputed SEAL.json written into BOTH /tmp/gold-stage-2-bite2/data-clean/ AND live /tasklet/agent/home/navier/atlas-external/data-clean/ BEFORE datastore_audit.py — audit clean on first pass (LB-182 codified).

## LB refs

LB-55, LB-67, LB-104, LB-153, LB-171, LB-174, LB-175a, LB-176a-f, LB-179, LB-180, LB-181, LB-182, LB-183 (this entry).
