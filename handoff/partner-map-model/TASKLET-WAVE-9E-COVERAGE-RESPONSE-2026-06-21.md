# Tasklet Wave 9E coverage response — 2026-06-21

Status: **Tasklet response ready for Grok**. This is a source-led sign-off packet only; Grok still owns deterministic mint/bind/relink/render QA and economics reseal.

## Guardrails

- Do not restructure phases[].
- Do not change hub markets[] topology.
- Do not touch rakta / bahrain-motc reference tier.
- Do not overwrite cascaded model_link / route_id / route_ids.
- Null beats confidently-wrong; exact-bind only.
- Roadmap amber cards with economics_status: roadmap_excluded remain excluded.

## P0 — hospitality mint sign-off

### Discovery Land — approved Bahamas flagship

- **Approved mint:** `nassau-bahamas` — Marsh Harbour Airport jetty ↔ Baker's Bay Marina / villas, Great Guana Cay.
- **Why:** This is Discovery Land's Bahamas flagship and the only P0 corridor needed to unblock the hospitality tail; do not substitute Nassau Harbour/Albany for the Abaco endpoints. If Abaco cannot be exact-minted, leave the endpoint null.
- **Candidate endpoints:**
  - Marsh Harbour Airport jetty / Marsh Harbour ferry-waterfront access — `bp_id:null` until Grok exact-mints it.
  - Baker's Bay 33-acre / 200-slip marina and villa docks — `bp_id:null` until Grok exact-mints it.
- **Source facts:**
  - Baker's Bay is a Discovery Land Company community on Great Guana Cay in the Abaco Islands, Bahamas.
  - Baker's Bay describes itself as a members-only community between the Sea of Abaco and the Atlantic Ocean.
  - Baker's Bay page describes a 33-acre, 200-slip full-service deep-water marina and village.
- **Instruction:** Parent under `nassau-bahamas` only as the existing Atlas display-market container. Do not silently substitute Nassau Harbour for Abaco if Abaco cannot be exactly minted.

### aman — approved top 5 flagship corridors

| Rank | City ID | Approved flagship corridor | Platform | Mint note |
|---:|---|---|---|---|
| 1 | `venice-italy` | Marco Polo Airport / airport water dock ↔ Aman Venice, Grand Canal | Pioneer II | Highest-value visible zero-wake proof; current featured route gap. Use existing Venice city, mint exact hotel/airport-water endpoints only if missing. |
| 2 | `palawan-philippines` | Amanpulo / Pamalican Island ↔ Cuyo / Manamoc / Palawan reef excursion endpoints | Pioneer II | Aman official page places Amanpulo on Pamalican Island, Cuyo, Palawan with Manila airport transfer; mint exact resort/reef excursion BPs only. |
| 3 | `bali-indonesia` | Bali / Amankila coast ↔ Lombok / Moyo / Amanwana collection connector | Quanta-LR | Preserve existing route_ids where already bound; use this only to improve featured geometry, not to restructure the phase. |
| 4 | `komodo-flores-indonesia` | Lombok / Sumbawa ↔ Komodo / Flores luxury chain | Quanta-LR flagged for review if >150 nm | Use only if Grok confirms long-leg geometry/range flag. Do not leave on Pioneer II; amber/review is preferable to wrong certainty. |
| 5 | `phuket-phang-nga-thailand` | Amanpuri / Pansea Beach ↔ Phang Nga Bay island excursion mesh | Pioneer II / N35 by sealed distance | Portfolio breadth pick after the three existing phases; mint exact resort/waterfront endpoints only if already in Atlas or source-backed. |

**Instruction:** Use these five as the approved Aman property flagship mint order. Do not restructure phases[]; fill featured geometry/journey bindings only. Preserve existing route_ids/model links.

### six-senses — approved top 5 flagship corridors

| Rank | City ID | Approved flagship corridor | Platform | Mint note |
|---:|---|---|---|---|
| 1 | `male-maldives` | Velana / Kadhdhoo transfer spine ↔ Six Senses Laamu, Laamu Atoll | Quanta-LR / Pioneer II by sealed leg | Top Maldives flagship; use existing Maldives/JIH sealed network where exact. Keep route_id/model links intact. |
| 2 | `mahe-seychelles` | Praslin / La Digue / Mahé inner-island transfer ↔ Six Senses Zil Pasyon, Félicité Island | Pioneer II | Official page identifies Zil Pasyon as the private-island Félicité property; mint exact Félicité/Angel Fish Bay/Praslin/La Digue endpoints only as evidenced. |
| 3 | `ho-chi-minh-city-vietnam` | Vung Tau / Con Dao airport-waterfront ↔ Six Senses Con Dao | Quanta-LR | Current Vietnam phase is geometry-relevant; bind to exact Con Dao water endpoints, not generic HCMC city center. |
| 4 | `phuket-phang-nga-thailand` | Phuket / Phang Nga Bay ↔ Six Senses Yao Noi | Pioneer II / N35 by sealed distance | Asia portfolio breadth pick with high water relevance; exact-bind only. |
| 5 | `nadi-fiji` | Nadi / Port Denarau ↔ Six Senses Fiji, Malolo Island | Pioneer II / N35 by sealed distance | South Pacific portfolio breadth pick; avoid Musandam/RAKTA cross-talk in this Wave 9E response. |

**Instruction:** Use these five as the approved Six Senses property flagship mint order. Do not restructure phases[]; fill featured geometry/journey bindings only. Preserve existing route_ids/model links.

## P1 — hub featured market picks

### Lyft +4 picks to clear 85%

| Rank | Market | City ID | Route chip | Reason |
|---:|---|---|---|---|
| 1 | `new-york` | `new-york-harbor-usa` | Midtown (W 39th) ↔ Hoboken / Jersey City waterfront | dense commute, existing Lyft/Citi Bike waterfront story, high route utility |
| 2 | `new-york` | `new-york-harbor-usa` | Lower Manhattan ↔ Governors Island / Rockaway | NYC harbour leisure + commuter breadth; strengthens already top-priority New York market |
| 3 | `miami` | `miami-florida-usa` | Downtown Miami / Bayside ↔ Miami Beach / South Beach | highest-value Miami water-taxi proof; short, visible, consumer-now corridor |
| 4 | `bay-area` | `san-francisco-bay-area-usa` | SF Ferry Building ↔ Sausalito / Larkspur | Bay Area ferry-demand proof and Lyft/Bay Wheels multimodal fit |

Fallback if exact binding fails: Seattle ↔ Bainbridge, Boston ↔ Hingham/South Shore, then Downtown ↔ Key Biscayne. No hub `markets[]` topology change.

### Kakao Mobility +3 picks — Jeju + Seoul Han River confirmed

| Rank | Market | City ID | Route chip | Reason |
|---:|---|---|---|---|
| 1 | `jeju` | `jeju-korea` | Seongsan ↔ Udo | marquee Jeju islet run; short, consumer-now, high tourism fit |
| 2 | `jeju` | `jeju-korea` | Moseulpo ↔ Marado / Gapado | second Jeju island-hop; strengthens Jeju as the priority leisure cluster |
| 3 | `seoul-han-river` | `seoul-incheon-korea` | Gimpo / Yeouido ↔ Jamsil / Ttukseom | strategic Han River commute hero and explicit Grok-requested Seoul priority |

Seoul official Hangang Bus source confirms the seven-pier Magok↔Jamsil river service context; use it to support the Han River hero. No hub `markets[]` topology change.

## P3 — India demand/fare inputs for Adani Ports + Reliance Industries

Tasklet confirms the **source-input sidecar only**; no Tasklet model cascade is being claimed complete here. Grok may build/reseal economics from admitted facts plus explicitly labelled assumptions.

| Market | Fare admitted | Demand admitted | Ops admitted | Use |
|---|---|---|---|---|
| `mumbai-india` | {"passenger": 400, "basis": "M2M official passenger fare from ₹400 onwards; not average fare"} | null | {"year_round": true, "ropax": true, "vehicle_deck_capacity_fact": "over 120 cars/two-wheelers/buses; exact mix not specified"} | fare/ops anchor only; demand remains null unless Grok applies a labelled template assumption. |
| `kerala-backwaters-india` | null | {"daily_ridership_reported": 5873, "daily_ridership_date": "2026-06-19", "cumulative_passengers_reported": 7070083} | {"e_boats": "75+", "routes": "15", "network_km": "75+"} | demand/ops anchor only; fare remains null unless official fare chart is independently verified. |
| `goa-india` | {"foot_passenger": 0, "two_wheeler": 0, "three_wheeler": 0, "basis": "government toll/public-ferry baseline, not premium Navier fare"} | null | {"regular_routes": 21, "service_hours": "about 18-20 hours/day plus on-request service"} | route/ops context and baseline toll only; do not turn vehicle toll into premium passenger fare without explicit model choice. |
| `andaman-india` | null | null | null | route candidate only; fare/demand/ops null until official PDF or other official DSS table is retrieved. |

**Do not overwrite:** `model_link`, `route_id`, `route_ids`, or `economics_status: roadmap_excluded`. If a cell is null in the sidecar, leave it null unless Grok independently verifies a source.

## Grok post-mint command sequence

```bash
python3 scripts/grok-econ-reseal/bind_hospitality_flagship_corridors.py aman six-senses discovery-land
```
```bash
python3 scripts/relink_partner_journeys.py --apply --partner aman six-senses discovery-land
```
```bash
python3 scripts/grok-econ-reseal/relink_hub_market_featured.py lyft kakao-mobility
```
```bash
python3 scripts/audit_partner_page_qa.py
```
```bash
python3 scripts/grok-econ-reseal/audit_partner_coverage_rollup.py
```
