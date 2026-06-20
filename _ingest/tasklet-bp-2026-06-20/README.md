# Tasklet → Grok BP-research handoff — 2026-06-20 (second-endpoint boarding points)

Second GitHub-native handoff. Adds real, sourced `endpoint_boarding_points` to corridor rows that were
blocked on a missing pier label, so Grok's seal lane can pin them. Scope: 34 corridor rows across 14 markets.

## Method (exactness over coverage)
- Researched each endpoint against operator / port-authority / govt sources (LASWA/LagFerry directory,
  NParks, Chao Phraya Express, Alilaguna, KPT, Red Sea Global, delostours). Tier per endpoint: T1 operator/govt,
  T2 reputable travel/encyclopedic, T3 weak.
- **Null beats confidently-wrong:** where no specific passenger pier could be verified, the endpoint was left
  null and the row marked `aspirational:true` (renders as visibly aspirational, not pinned).

## Outcome
- **19 corridors now pin-ready** (full, real BP labels both sides).
- **7 corridors marked `aspirational:true`** — honest null side or speculative inter-development link:
  Sihanoukville→Koh Kong (no verified Cardamom pier), Abidjan→Grand-Bassam (road-served), Abidjan→Jacqueville
  (ferry superseded by 2015 bridge, T3), The Red Sea→AMAALA ×2 (two separate giga-developments), NEOM Sindalah→
  Magna/Oxagon ×2 (no passenger pier yet).
- **8 single-pier intra-city loops marked `aspirational:true`** (same pier both ends — sightseeing loops, not
  point-to-point; no honest second endpoint):
- singapore: Clarke Quay (Singapore River)
- singapore: Sentosa / Keppel waterfront
- singapore: Marina Bay (Bayfront)
- bali: Benoa Harbour Cruise Terminal
- bali: Pantai Laguna (Ancol Taman Impian)
- bali: Batavia Marina (Sunda Kelapa)
- phuket: Chalong Pier (Ao Chalong)
- phuket: ICONSIAM Pier (Chao Phraya)

## Per-corridor detail
| market | corridor | from BP | to BP | status |
|---|---|---|---|---|
| singapore | Changi Point → Pulau Ubin (Main Jetty) | Changi Point Ferry Terminal | Pulau Ubin — Pulau Ubin Jetty (Main Jetty) | pin-ready |
| bali | Marina Ancol → Thousand Islands — inner ring (Bidadari / Ayer / Onrust) | Marina Ancol — Dermaga Marina Ancol (Ancol Marina) | Pulau Bidadari — resort island jetty | pin-ready |
| bali | Marina Ancol → Thousand Islands — outer ring (Macan / Pelangi / Putri / Sepa) | Marina Ancol — Dermaga Marina Ancol (Ancol Marina) | Pulau Putri — resort island jetty | pin-ready |
| bali | Thousand Islands — inner ring → Thousand Islands — outer ring | Pulau Bidadari — resort island jetty | Pulau Putri — resort island jetty | pin-ready |
| phuket | Sathorn (Central) Pier → Phra Arthit Pier | Sathorn (Central) Pier — Saphan Taksin | Phra Arthit Pier (N13) | pin-ready |
| vietnam | Bach Dang Wharf (Saigon) → Can Gio Mangrove Biosphere | Bach Dang Wharf — Bach Dang Speed Ferry Terminal (Dist. 1) | Cần Giờ — Tắc Suất Pier (Cần Thạnh) | pin-ready |
| cambodia | Sihanoukville → Koh Kong / Cardamom coast | Sihanoukville — Serendipity Pier (Autonomous Port Gate 1, Tourist Pier) | — | aspirational (null side) |
| bolt-greece | Mykonos Town → Delos | Mykonos Town — Old Port (harbour ferry pier) | Delos — Delos boat pier (archaeological site landing) | pin-ready |
| bolt-italy | Venice Marco Polo → San Marco | Venice Marco Polo Airport — Alilaguna water dock | San Marco — Alilaguna San Marco pontoon (San Zaccaria) | pin-ready |
| bolt-ksa-commercial | Shura Island Marina → Outer-island resorts (St Regis / Nujuma / Shebara) | Shura Island — yacht marina (The Red Sea) | St. Regis Red Sea Resort jetty (Ummahat Island) | pin-ready |
| bolt-ksa-commercial | The Red Sea → AMAALA (Triple Bay) | The Red Sea — Turtle Bay Jetty (Shura Island gateway) | AMAALA — Triple Bay Marina (AMAALA Yacht Club) | aspirational (speculative link) |
| bolt-ksa-commercial | NEOM — Sindalah → Magna / Oxagon coast | NEOM Sindalah — Sindalah Marina (IGY) | — | aspirational (null side) |
| bolt-ksa-commercial | Outer-island resort → Outer-island resort cluster (Nujuma / Jumeirah / St Regis) | St. Regis Red Sea Resort jetty (Ummahat Island) | Nujuma, a Ritz-Carlton Reserve — island jetty | pin-ready |
| yango-ksa-commercial | Shura Island Marina → Outer-island resorts (St Regis / Nujuma / Shebara) | Shura Island — yacht marina (The Red Sea) | St. Regis Red Sea Resort jetty (Ummahat Island) | pin-ready |
| yango-ksa-commercial | The Red Sea → AMAALA (Triple Bay) | The Red Sea — Turtle Bay Jetty (Shura Island gateway) | AMAALA — Triple Bay Marina (AMAALA Yacht Club) | aspirational (speculative link) |
| yango-ksa-commercial | NEOM — Sindalah → Magna / Oxagon coast | NEOM Sindalah — Sindalah Marina (IGY) | — | aspirational (null side) |
| yango-ksa-commercial | Outer-island resort → Outer-island resort cluster (Nujuma / Jumeirah / St Regis) | St. Regis Red Sea Resort jetty (Ummahat Island) | Nujuma, a Ritz-Carlton Reserve — island jetty | pin-ready |
| yango-pakistan | Karachi (Keamari) → Manora | Keamari — Keamari Boat Basin jetty (KPT) | Manora — Manora ferry jetty (KPT landing) | pin-ready |
| yango-cote-divoire | Abidjan → Grand-Bassam | Abidjan — Gare Lagunaire du Plateau (STL/SOTRA) | — | aspirational (null side) |
| yango-cote-divoire | Abidjan → Jacqueville | Abidjan — Gare Lagunaire du Plateau (STL/SOTRA) | Jacqueville — Bac de Jacqueville (Lagune Tagba ferry landing) | aspirational (T3 & bridge superseded) |
| yango-lagos | CMS (Lagos Island) → Victoria Island | Lagos Island — Marina/CMS Ferry Terminal | Victoria Island — Addax/Sandfill/Maroko jetty | pin-ready |
| yango-lagos | Victoria Island → Lekki Phase 1 | Victoria Island — Addax/Sandfill/Maroko jetty | Lekki Phase 1 — Lekki Ferry Terminal (OMI EKO) | pin-ready |
| yango-lagos | Ikoyi → Apapa | Ikoyi — Five Cowries/Falomo Ferry Terminal | Apapa — Liverpool Jetty | pin-ready |
| yango-lagos | CMS → Ikorodu | Lagos Island — Marina/CMS Ferry Terminal | Ikorodu — Ikorodu/Ipakodo Ferry Terminal | pin-ready |
| yango-lagos | Lekki → Epe | Lekki Phase 1 — Lekki Ferry Terminal (OMI EKO) | Epe — Epe Ayetoro Jetty | pin-ready |
| yango-lagos | Lagos → Badagry | Lagos Island — Marina/CMS Ferry Terminal | Badagry — Jegba Marina/Commando Jetty | pin-ready |

## Notes for Grok
- The `bali` market bucket actually contains **Jakarta / Kepulauan Seribu** corridors, and `phuket` contains
  **Bangkok / Chao Phraya** corridors (node IDs are already correct Jakarta/Bangkok chips — only the market label
  is a legacy misnomer). Geometry binds to the node IDs, so this is cosmetic, but worth a future market-rename.
- Thousand-Islands "ring" endpoints and the KSA outer-island cluster have no single pier; representative resort
  jetties were used (flagged T2). Treat as representative landings.
- After sealing, **backfill minted route_ids** onto these rows (your §7 rule) and **re-run the affected partner
  aggs** (yango-lagos, yango-pakistan, yango-cote-divoire, bolt/yango-ksa-commercial, singapore, bali, phuket,
  vietnam, cambodia, bolt-greece, bolt-italy) since several rows flipped to aspirational.

## Still upstream (not in this PR)
- 92 pending rows that already carry full labels → already in your seal queue, no Tasklet action.
- Jakarta/Bangkok `gcn-*-shared` registry route_id backfill (gold minted, registry still null/ics-*).
