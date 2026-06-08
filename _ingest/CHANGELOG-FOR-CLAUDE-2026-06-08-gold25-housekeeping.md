# Gold #25 — Housekeeping: 13 degenerate-route fixes (autonomous lane)
Base: Gold #24. ROUTES 5228->5227 (12 relabeled + 1 self-loop removed).

The 13 routes whose front-end labels read "X -> X" (identical from/to) are fixed.
Resolution method: **exact endpoint-coordinate -> POI identity match (6dp)** — the route's
start/end coords coincide exactly with named boarding-point POIs. (The stored from_node/to_node
IDs were stale and not in the POI registry, so coordinate-identity was used — still exact, not fuzzy.)

**Relabeled (12):**
- Izu Peninsula: Okata Port Ferry Terminal -> Toshima
- Izu Islands: Tako Bay Miura Fishing Port -> Mikurashima
- Izu Peninsula: Inatori -> Marina Shirahama
- Izu Peninsula: Yamaha Marina Numazu -> Fujisanhagoromo Marina
- Izu Peninsula: Izu Oshima -> Toshima
- Busan: Jangnim Port -> Sinho (신호선착장)
- Izu Islands: Miike Port (三池港) -> Mikurashima
- Dubrovnik & South Dalmatia: Mlini Harbour -> Brsecine Harbour
- Dubrovnik & South Dalmatia: Zaton Harbour -> Brsecine Harbour
- Izu Peninsula: Ito Sunrise Marina -> Manazuru Bay Marina
- Dubrovnik & South Dalmatia: Prapratno Ferry Port -> Sobra Ferry Port
- Palm Beach: Gulf Stream Boat Club (Boynton Beach) -> Gulf Stream Boat Club (Lantana)
  [two distinct docks share the same POI name; disambiguated by locale]

**Removed (1):**
- Barbados `rn-77e6d9526f5b` — 0.7nm self-loop entirely within the Bridgetown Harbour /
  Cruise Terminal / Port complex. Not a real corridor. (null > confidently-wrong.)

Route IDs preserved (no downstream reference breakage). Sidecar unchanged at 69.
