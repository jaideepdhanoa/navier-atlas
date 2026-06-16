# CHANGELOG — Gold #79m — Wave 2 bite 1 scrub+enrich splice+seal (2026-06-16)

**Bite scope:** Caribbean — Nassau/Bahamas Out Islands + Turks & Caicos + Cayman Islands + USVI/BVI.
Counterpart to staged delta from `navier-scrub-enrich-wave` subagent (`/tmp/scrub-wave-2-bite1/`). Sealed by `navier-scrub-wave-splice-seal` worker.

## Counts (Gold #79l → #79m)

- **Routes:** 5,421 → 5,449 (Δ +28 = 0 orphan-endpoint kills + 28 aspirational real-world Caribbean ferry mesh mints).
- **POIs:** 11,273 → 11,206 (Δ −67 = −76 OSM-noise BPs + 9 marquee enrich BPs).
- **Cities:** 168 → 170 (Δ +2 anchor cities = `nassau-bahamas`, `usvi-bvi` — orphan parent_city_id mint pattern, LB-180 variant).
- **Clusters:** 79 → 83 (Δ +4 greenfield, all LB-174-compliant real-BP anchors: `nassau-bahamas-cluster`, `turks-caicos-cluster`, `cayman-islands-cluster`, `usvi-bvi-cluster`).
- **Sidecar `economics_by_route_id.json`:** 82 records / 44 pending — unchanged vs #79l (no partner-pinned corridors touched this bite).

## Kills (76 BPs, 0 orphan routes)

- Caribbean = highest regional noise rate observed at 33% avg (vs US/Canada 6–20%) — Caribbean condo/vacation-rental naming convention dominant. Bahamas/TCI/Cayman/USVI-BVI all hit.
- Includes 16 hard dupes surfaced via new `gate_poi_dedup.py` (lowercased-name, rounded-coord) on USVI/SJU split — see new learning.
- Kill examples: condos, villas, vacation-rental brands, generic "harbour" tokens, retail.

## Enrich (9 BPs, 28 routes, 4 greenfield clusters, 2 anchor cities)

- **9 new BPs minted** with Mapbox+Wikidata+OSM grounding (LB-55):
  - Bahamas: Harbour Island Govt Dock, Spanish Wells Public Dock, Three Island Dock (N. Eleuthera), Staniel Cay Yacht Club, Compass Cay Marina.
  - TCI: Walkin Marina/Heaving Down Rock, South Caicos Govt Dock, Salt Cay Govt Dock.
  - Cayman: Creek Dock (Cayman Brac).
- **2 new anchor cities** to resolve orphan `parent_city_id`s (NEW pattern this bite — variant of LB-180 greenfield cluster pattern; minted at marquee-BP coords): `nassau-bahamas`, `usvi-bvi`.
- **28 new routes** — real-world Caribbean ferry mesh:
  - Bahamas (10): Pinder's, Bo Hengy, Bahamas Ferries operators (Nassau↔Harbour Island, Spanish Wells, Three Island Dock, Governor's Harbour, Staniel Cay, Highbourne, Paradise; Exuma intra).
  - TCI (5): Caribbean Cruisin, TCI Ferry, Caicos Express (Provo↔Grand Turk hard-cap edge 70 nm; Provo↔South Caicos; Grand Turk↔Salt Cay; Grand Turk↔South Caicos).
  - Cayman (6): Cayman Islands Ferry George Town↔Cayman Brac and ↔Little Cayman (max minted = 97.1 nm, Quanta-LR — within 150 nm Q-LR cap); Cayman Brac↔Little Cayman; intra-Grand Cayman.
  - USVI/BVI (7, 0 new BPs — dense-mesh case): USVI Ferry, Inter-Island Boat Services, Road Town Fast Ferry, Smith's Ferry, Speedy's, New Horizon Ferry. Real-world existing mesh of routes / 0 new BPs (BP coverage was adequate, ROUTES were sparse). NEW pattern.
- **4 greenfield clusters** with real-BP anchors (LB-174):
  - `nassau-bahamas-cluster` anchor `bp-3b4ff7a4e4` Nassau Cruise Port.
  - `turks-caicos-cluster` anchor `bp-28da739816` Blue Haven Marina (Provo).
  - `cayman-islands-cluster` anchor `bp-edf107b2b6` Port Authority Cayman (Grand Cayman).
  - `usvi-bvi-cluster` anchor `bp-44cca8081e` Charlotte Amalie Harbor (St. Thomas).

## Notable mints / advisory

- **Longest mint:** George Town ↔ Cayman Brac 97.1 nm (Quanta-LR; within 150 nm Q-LR cap).
- **Provo ↔ Grand Turk** ~70 nm hard-cap edge — assigned Quanta-LR; not Pioneer II.
- **White Bay Villas JVD killed** via villas-name veto despite `beach_club_jetty` bp_type. Conservative call — may reverse later if real-world ferry endpoint usage confirmed (advisory).

## Gates (all PASS)

| Gate | Result |
|---|---|
| `gate_endpoint_labels.py` | 0 hard FLAG (3 pre-existing WEAK single-token binds carried: SG Marina Bay↔Changi, MLE Velana ×2) |
| `gate_city_ids.py` | PASS — 205 valid nodes / 5,449 routes / 83 clusters |
| `gate_partner_rationale_leak.py` | clean across `partner-pitch/partners/*.json` |
| `gate_osm_noise_bp.py` (advisory) on 4 bite-1 metros | 0 new flags (bite already scrubbed) |
| `gate_premint_pair.py` | **0 / 5,449 routes flagged** (threshold 0.5) — 2nd consecutive 0-flag at scale; LB-179 classifier patch ship priority confirmed |
| LB-175a pre-build (ROUTES ≥ floor 5,072 + pier-coord verify all 9 new BPs) | PASS; longest mint 97.1 nm < Quanta-LR 150 nm cap |
| `datastore_audit.py` post-seal | (see report) |

## Inline patches applied by wave subagent (un-shipped to upstream classifier)

- Dupe-of-canonical kill pattern via `gate_poi_dedup.py` (NEW) — `(lowercased-name, rounded-coord)` dupe detector. 16 hard dupes surfaced this bite.
- Orphan `parent_city_id` coverage check + mint anchor city at marquee-BP coords (NEW, variant of LB-180).
- 14 new operator/brand rescue tokens for permanent MARINE_TERMS promotion: Bahamas Ferries, Pinder's, Bo Hengy, Caribbean Cruisin, TCI Ferry, Caicos Express, Cayman Islands Ferry, USVI Ferry, Road Town Fast Ferry, Smith's Ferry, Speedy's, Inter-Island Boat Services, Native Son, New Horizon Ferry.
- Caribbean condo/vacation-rental noise terms — permanent METRO_BBOX Caribbean block needed.
- LB-181 reordered: deleted prior gold zip BEFORE cp new zip to avoid FUSE quota fire-drill.

## LB refs

LB-67, LB-104, LB-153, LB-171, LB-174, LB-175a, LB-176a/b/c/d/e/f, LB-179, LB-180, LB-181, LB-182 (this entry).
