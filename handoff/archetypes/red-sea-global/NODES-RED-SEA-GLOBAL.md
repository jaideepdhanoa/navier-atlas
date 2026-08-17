# NODES — Red Sea Global network design (archipelago hub-and-spoke)

Internal audit file. Research date: 2026-08-16. **No Atlas corridors exist for these waters in a usable state — all geometry below is new, no invented IDs.** Distances DERIVED from listed coordinates (haversine × 1.15 routing factor, ±15%); times at 25 kn + 6 min dwell/harbor allowance, with 8 kn reef/harbor regime assumption per SPEED-RULES. Coordinate precision varies — flagged per node.

## 1 · Node inventory
### Cluster A — The Red Sea (Al Wajh lagoon) · hub: Shura Island Marina
| # | Node | Status | Coordinates | Source | Confidence |
|---|---|---|---|---|---|
| A1 | **Shura Island Marina (HUB)** | OPERATIONAL (island opened 2025; arrival "by boat to the island's marina"; 115–118 berths, Foster + Partners) | 25.504, 36.958 (island; marina position on island DERIVED) | RSG Shura release + Wikipedia coords | PRIMARY (facility) / SECONDARY (coords) |
| A2 | Turtle Bay jetty (TBH Jetty) + Professional Beach Club — mainland gateway | OPERATIONAL (today's boat-transfer origin; 20 km / 30 min EV from RSI) | 25.500, 37.006 | rsiairport.sa (PRIMARY product) + mapcarta (SECONDARY coords) | PRIMARY/SECONDARY |
| A3 | Ummahat islands — St. Regis + Nujuma jetties | OPERATIONAL (both resorts open 2024; served today by speedboat/yacht + seaplane) | ~25.585, 36.770 (map-derived, LOW precision) | resorts + rsiairport.sa; coords DERIVED | PRIMARY (landing exists) / DERIVED (coords) |
| A4 | Sheybarah Island — Shebara resort jetty | OPERATIONAL (open Nov 2024; 30–40 min boat from Turtle Bay) | 25.366, 36.895 | shebara.sa (PRIMARY) + Wikipedia coords (SECONDARY) | PRIMARY/SECONDARY |
| A5 | Red Sea International Airport (RSI) | LAND INTERCHANGE ONLY — has a seaplane terminal; **no marina/jetty at the airport verified**; boat guests drive 20 km to A2. Fail-closed: not a water node. | 25.630, 37.078 | rsiairport.sa + Wikipedia | PRIMARY (process) |
| A6 | Laheq Island marina | ANNOUNCED (115-berth marina, island set to open 2028) — roadmap infill on A1↔A3 axis (~8 nm from Shura) | ~25.6, 36.9 (LOW precision) | RSG Laheq release + marinaworld | PRIMARY (announcement) |
| A7 | Al Wajh town | GATEWAY, NO VERIFIED TOURIST LANDING — Al Wajh Intl Airport (reopened May 2026) is a land gateway; port/jetty for guest service UNSOURCED → roadmap only | 26.246, 36.453 (town, approx) | RSG airport release | PRIMARY (airport) / UNSOURCED (landing) |
| A8 | Umluj town | GATEWAY, NO VERIFIED TOURIST LANDING — roadmap only (~37 nm from Turtle Bay) | 25.021, 37.269 (town, approx) | gazetteer | SECONDARY / UNSOURCED (landing) |
| — | Desert Rock · Six Senses Southern Dunes | INLAND — **excluded from water service**; land connection to A2/A5 noted | — | RSG portfolio | PRIMARY |

### Cluster B — AMAALA (Triple Bay) · hub: Triple Bay Marina / AMAALA Yacht Club
| # | Node | Status | Coordinates | Source | Confidence |
|---|---|---|---|---|---|
| B1 | **AMAALA Yacht Club / Triple Bay Marina (HUB)** | OPERATIONAL/OPENING (destination opening from Nov 2025; yacht club + 10-ha marina, yachts to 130 m; Marina Village adjacent) | 26.647, 36.220 (Four Seasons AMAALA published pin) | RSG opening release + visitredsea AYC + fourseasons.com/amaalaredsea/getting-here | PRIMARY |
| B2 | Triple Bay resort frontages (Equinox/Nammos/Four Seasons/Rosewood/Six Senses; Nammos island venue) | ANNOUNCED AS WATER STOPS — resorts open/opening, but **no individual resort jetties verified**; resorts are linked by the 5 km Wellness Route on land. Water calls beyond B1 fail closed until verified. | within ~2 nm of B1 | RSG opening release | PRIMARY (resorts) / UNSOURCED (jetties) |

### Cluster C — Thuwal Private Retreat (roadmap) · off Jeddah
| # | Node | Status | Coordinates | Source | Confidence |
|---|---|---|---|---|---|
| C1 | KAUST North Marina (Thuwal, north Jeddah) | OPERATIONAL (published departure point: "45-minute private yacht transfer from KAUST North Marina") | ~22.33, 39.09 (approx) | redseaglobal.com/en/portfolio/thuwal/ + thuwalretreat.sa | PRIMARY (facility) / DERIVED (coords) |
| C2 | Thuwal Private Retreat jetty | OPERATIONAL (island opened 2024, buy-out only) | island coords UNSOURCED; 45-min conventional yacht ⇒ **~8–13 nm** [DERIVED band at 12–18 kn] | RSG Thuwal page | PRIMARY (landing) / DERIVED (distance) |

Node count: **12 inventoried** (8 Red Sea + 2 AMAALA + 2 Thuwal); **6 operational water nodes today** (A1–A4, B1, C1/C2 pair), 1 land interchange (A5), 1 announced (A6), 2 unverified gateways (A7, A8), 1 unverified stop-set (B2).

## 2 · Line design (MECE; ≤ ceil(stops/2) lines per cluster; 1 hub per cluster)
Cluster A active water stops = 4 (A1, A2, A3, A4) → max 2 lines. ✓

### RSG-1 · Lagoon North Line — Turtle Bay ↔ Shura ↔ Ummahat
| Leg | Distance | Time @25 kn + dwell | Today's mode |
|---|---|---|---|
| A2 Turtle Bay ↔ A1 Shura Marina | 2.6 nm direct / ~3.0 routed | **~13 min** (mostly harbor-regime; realistic 15 min) | bridge (EV) or boat |
| A1 Shura ↔ A3 Ummahat (St. Regis/Nujuma) | 11.3 nm / ~12.9 routed | **~37 min** | speedboat/yacht ~60 min from A2; seaplane 25–30 min from RSI |
| Through A2→A3 | 13.8 nm / ~15.8 routed | ~44 min (vs ~90 min car+boat today door-to-door) | — |
Role: arrival trunk (airport party → Turtle Bay → island resort) + Shura-based experience trips. Roadmap infill: call at A6 Laheq (~8.3 nm from Shura) when open [ANNOUNCED].

### RSG-2 · Lagoon South Line — Shura ↔ Sheybarah (hub spoke)
| Leg | Distance | Time | Today's mode |
|---|---|---|---|
| A1 Shura ↔ A4 Sheybarah | 9.0 nm / ~10.3 routed | **~31 min** | none direct today |
| (Operating variant: A2 Turtle Bay ↔ A4 direct — today's transfer corridor) | 10.1 nm / ~11.6 routed | **~34 min** (vs 30–40 min conventional today) | shared/private boat |
Role: Shebara arrivals + south-lagoon experiences. Reef-slow flag: Sheybarah approach crosses outer-reef shelf — 8 kn regime last 0.5 nm minimum [DERIVED; RSG zone chart not public].

### RSG-3 · AMAALA Triple Bay Line — marina-based local + coastal roadmap
| Leg | Distance | Time | Status |
|---|---|---|---|
| B1 intra-Triple Bay loop (marina ↔ bay frontages/Nammos island venue) | ~1–2 nm hops | 5–10 min/hop | Experience/shuttle loop anchored at B1 ONLY until resort jetties verified [fail-closed] |
| B1 Triple Bay ↔ A1 Shura (inter-destination) | **79.3 nm direct / ~91 routed** | ~3.7 h at 25 kn — **beyond N45/N30 electric envelope; ROADMAP ONLY, long-range hybrid platform note (Quanta-LR class per addendum); never faked on a 70 nm vessel** | ROADMAP |
| B1 ↔ A7 Al Wajh town/airport | 27.2 nm / ~31 routed | ~81 min | ROADMAP (no verified Al Wajh landing) |

### RSG-T · Thuwal Gateway (roadmap, separate micro-cluster)
| Leg | Distance | Time | Status |
|---|---|---|---|
| C1 KAUST North Marina ↔ C2 Thuwal Private Retreat | ~8–13 nm [DERIVED from 45-min conventional yacht] | **~25–37 min foiling** (vs 45 min today) | Operable with N30-class on day one of a partnership; island coords unverified → ROADMAP flag |

**Line count: 3 active-cluster lines + 1 roadmap line.** Hubs: Shura Marina (Cluster A), Triple Bay Marina (Cluster B). MECE check: every operational water node appears on exactly one line (A2 appears on RSG-1 with an RSG-2 operating variant noted, not a separate line). ✓

## 3 · Notes for geometry sealing (Grok handoff later)
- All coordinates above need re-derivation to jetty-precision before sealing; A3 (Ummahat) and A6/C2 are LOW precision.
- Mis-geocode risk: none inherited — no sealed set used (RSG geography was not in a clean sealed set; fail-closed per addendum).
- Every rendered stop above is a research-verified real landing or explicitly status-flagged (announced/unverified/roadmap).
