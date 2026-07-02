# Proposal fidelity — lyft

**Verdict:** PASS
**Checked:** 2026-07-02T19:35:41Z

## Summary

- Items audited: 76
- KEEP: 76
- DROP: 0
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 0

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Wall St / Pier 11 → Long Island City / Williamsbur | `—` | **KEEP** | — |
| journey | — | Manhattan (E 34th St) → Montauk / the Hamptons | `—` | **KEEP** | — |
| journey | — | Downtown Miami / Bayside → Miami Beach / South Bea | `—` | **KEEP** | — |
| journey | — | SF Ferry Building → Sausalito / Larkspur | `—` | **KEEP** | — |
| featured | 3 | Piraeus, Athens → Hydra Port | `rn-678c1b2769a9` | **KEEP** | — |
| journey | market:new-york | Wall St / Pier 11 → Long Island City / Williamsbur | `—` | **KEEP** | — |
| journey | market:new-york | Midtown (W 39th) → Hoboken / Jersey City waterfron | `—` | **KEEP** | — |
| journey | market:new-york | Manhattan (E 34th) → Montauk / the Hamptons | `—` | **KEEP** | — |
| journey | market:new-york | Lower Manhattan → Governors Island / Rockaway | `—` | **KEEP** | — |
| featured | new-york/p1 | Pier 11 / Wall Street → Long Island City | `—` | **KEEP** | — |
| featured | new-york/p1 | Midtown (W 39th) ↔ Hoboken / Jersey City waterfron | `—` | **KEEP** | — |
| featured | new-york/p1 | Manhattan (E 34th) ↔ Montauk / the Hamptons | `—` | **KEEP** | — |
| featured | new-york/p2 | Lower Manhattan ↔ Governors Island / Rockaway | `—` | **KEEP** | — |
| featured | new-york/p2 | LaGuardia (Marine Air) ↔ Wall St / Midtown | `—` | **KEEP** | — |
| featured | new-york/p3 | Pier 11 / Wall Street → Long Island City | `—` | **KEEP** | — |
| featured | new-york/p3 | Midtown (W 39th) ↔ Hoboken / Jersey City waterfron | `—` | **KEEP** | — |
| featured | new-york/p3 | Manhattan (E 34th) ↔ Montauk / the Hamptons | `—` | **KEEP** | — |
| journey | market:miami | Miami → Miami | `—` | **KEEP** | — |
| journey | market:miami | Downtown → Key Biscayne | `—` | **KEEP** | — |
| journey | market:miami | Nassau Cruise Port → Paradise Island Ferry Termina | `—` | **KEEP** | — |
| journey | market:miami | Palm Beach / Treasure Coast → Miami | `—` | **KEEP** | — |
| featured | miami/p1 | Miami → Miami | `—` | **KEEP** | — |
| featured | miami/p1 | Downtown ↔ Key Biscayne | `—` | **KEEP** | — |
| featured | miami/p1 | Miami → Nassau & The Bahamas | `—` | **KEEP** | — |
| featured | miami/p2 | Palm Beach / Treasure Coast → Miami | `—` | **KEEP** | — |
| featured | miami/p2 | Miami → Nassau & The Bahamas | `—` | **KEEP** | — |
| featured | miami/p3 | Miami → Miami | `—` | **KEEP** | — |
| featured | miami/p3 | Downtown ↔ Key Biscayne | `—` | **KEEP** | — |
| featured | miami/p3 | Miami → Nassau & The Bahamas | `—` | **KEEP** | — |
| journey | market:bay-area | San Francisco Bay Area → San Francisco Bay Area | `—` | **KEEP** | — |
| journey | market:bay-area | San Francisco Bay Area → San Francisco Bay Area | `—` | **KEEP** | — |
| journey | market:bay-area | SF → Redwood City / South Bay | `—` | **KEEP** | — |
| journey | market:bay-area | SF → Monterey | `—` | **KEEP** | — |
| featured | bay-area/p1 | San Francisco Bay Area → San Francisco Bay Area | `—` | **KEEP** | — |
| featured | bay-area/p1 | San Francisco Bay Area → San Francisco Bay Area | `—` | **KEEP** | — |
| featured | bay-area/p1 | SF ↔ Redwood City / South Bay | `—` | **KEEP** | — |
| featured | bay-area/p2 | SF ↔ Monterey | `—` | **KEEP** | — |
| featured | bay-area/p2 | SF ↔ Tiburon / Angel Island | `—` | **KEEP** | — |
| featured | bay-area/p3 | San Francisco Bay Area → San Francisco Bay Area | `—` | **KEEP** | — |
| featured | bay-area/p3 | San Francisco Bay Area → San Francisco Bay Area | `—` | **KEEP** | — |
| featured | bay-area/p3 | SF ↔ Redwood City / South Bay | `—` | **KEEP** | — |
| journey | market:seattle | Seattle & Puget Sound → Seattle & Puget Sound | `—` | **KEEP** | — |
| journey | market:seattle | Seattle & Puget Sound → Seattle & Puget Sound | `—` | **KEEP** | — |
| journey | market:seattle | Seattle & Puget Sound → Seattle & Puget Sound | `—` | **KEEP** | — |
| journey | market:seattle | Seattle & Puget Sound → Seattle & Puget Sound | `—` | **KEEP** | — |
| featured | seattle/p1 | Seattle & Puget Sound → Seattle & Puget Sound | `—` | **KEEP** | — |
| featured | seattle/p1 | Colman Dock (Seattle Ferry Terminal) → Bremerton F | `—` | **KEEP** | — |
| featured | seattle/p1 | Seattle & Puget Sound → Seattle & Puget Sound | `—` | **KEEP** | — |
| featured | seattle/p2 | Seattle & Puget Sound → Seattle & Puget Sound | `—` | **KEEP** | — |
| featured | seattle/p3 | Seattle & Puget Sound → Seattle & Puget Sound | `—` | **KEEP** | — |
| featured | seattle/p3 | Seattle & Puget Sound → Seattle & Puget Sound | `—` | **KEEP** | — |
| featured | seattle/p3 | Seattle & Puget Sound → Seattle & Puget Sound | `—` | **KEEP** | — |
| journey | market:boston | Boston & New England → Boston & New England | `—` | **KEEP** | — |
| journey | market:boston | Long Wharf (Boston) → Hingham Shipyard | `—` | **KEEP** | — |
| journey | market:boston | Boston → Provincetown | `—` | **KEEP** | — |
| journey | market:boston | Boston → Martha's Vineyard / Nantucket | `—` | **KEEP** | — |
| featured | boston/p1 | Long Wharf (Boston) → Salem Ferry Wharf | `—` | **KEEP** | — |
| featured | boston/p1 | Long Wharf (Boston) → Provincetown (MacMillan Pier | `—` | **KEEP** | — |
| featured | boston/p1 | Long Wharf (Boston) → Provincetown (MacMillan Pier | `—` | **KEEP** | — |
| featured | boston/p2 | Hyannis Terminal → Oak Bluffs (Martha's Vineyard) | `—` | **KEEP** | — |
| featured | boston/p2 | Long Wharf (Boston) → Hull / Pemberton | `—` | **KEEP** | — |
| featured | boston/p3 | Boston & New England → Boston & New England | `—` | **KEEP** | — |
| featured | boston/p3 | Long Wharf (Boston) → Hingham Shipyard | `—` | **KEEP** | — |
| featured | boston/p3 | Long Wharf (Boston) → Provincetown (MacMillan Pier | `—` | **KEEP** | — |
| journey | market:athens-cyclades | E1 Gate Ferry to Kos - Piraeus Port → View Yacht - | `rn-7f7c38a84c7c` | **KEEP** | — |
| journey | market:athens-cyclades | E1 Gate Ferry to Kos - Piraeus Port → Skala Marina | `rn-16fa8284adf1` | **KEEP** | — |
| journey | market:athens-cyclades | Mykonos & the Cyclades → Santorini & the South Cyc | `—` | **KEEP** | — |
| journey | market:athens-cyclades | Mykonos New Port (Tourlos) → Naxos Port (Chora) | `rn-dc595b5a6ab8` | **KEEP** | — |
| featured | athens-cyclades/p1 | E1 Gate Ferry to Kos - Piraeus Port → View Yacht - | `rn-7f7c38a84c7c` | **KEEP** | — |
| featured | athens-cyclades/p1 | E1 Gate Ferry to Kos - Piraeus Port → Skala Marina | `rn-16fa8284adf1` | **KEEP** | — |
| featured | athens-cyclades/p1 | Mykonos & the Cyclades → Santorini & the South Cyc | `—` | **KEEP** | — |
| featured | athens-cyclades/p2 | Mykonos New Port (Tourlos) → Naxos Port (Chora) | `rn-dc595b5a6ab8` | **KEEP** | — |
| featured | athens-cyclades/p2 | Marina Zeas (Piraeus) → 2nd Glyfada Marina | `rn-89552c9786ec` | **KEEP** | — |
| featured | athens-cyclades/p3 | E1 Gate Ferry to Kos - Piraeus Port → View Yacht - | `rn-7f7c38a84c7c` | **KEEP** | — |
| featured | athens-cyclades/p3 | E1 Gate Ferry to Kos - Piraeus Port → Skala Marina | `rn-16fa8284adf1` | **KEEP** | — |
| featured | athens-cyclades/p3 | Mykonos & the Cyclades → Santorini & the South Cyc | `—` | **KEEP** | — |
