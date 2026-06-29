# Proposal fidelity — lyft

**Verdict:** REWRITE
**Checked:** 2026-06-29T15:10:45Z

## Summary

- Items audited: 76
- KEEP: 59
- DROP: 17
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 17

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Wall St / Pier 11 → Long Island City / Williamsbur | `ics-db90a41958` | **KEEP** | — |
| journey | — | Manhattan (E 34th St) → Montauk / the Hamptons | `—` | **KEEP** | — |
| journey | — | Downtown Miami / Bayside → Miami Beach / South Bea | `—` | **KEEP** | — |
| journey | — | SF Ferry Building → Sausalito / Larkspur | `—` | **KEEP** | — |
| featured | 3 | Piraeus, Athens → Hydra Port | `rn-678c1b2769a9` | **KEEP** | — |
| journey | market:new-york | Wall St / Pier 11 → Long Island City / Williamsbur | `ics-db90a41958` | **KEEP** | — |
| journey | market:new-york | Midtown (W 39th) → Hoboken / Jersey City waterfron | `—` | **KEEP** | — |
| journey | market:new-york | Manhattan (E 34th) → Montauk / the Hamptons | `—` | **KEEP** | — |
| journey | market:new-york | Lower Manhattan → Governors Island / Rockaway | `—` | **KEEP** | — |
| featured | new-york/p1 | Pier 11 / Wall Street → Long Island City | `ics-db90a41958` | **KEEP** | — |
| featured | new-york/p1 | Midtown (W 39th) ↔ Hoboken / Jersey City waterfron | `—` | **KEEP** | — |
| featured | new-york/p1 | Manhattan (E 34th) ↔ Montauk / the Hamptons | `—` | **KEEP** | — |
| featured | new-york/p2 | Lower Manhattan ↔ Governors Island / Rockaway | `—` | **KEEP** | — |
| featured | new-york/p2 | LaGuardia (Marine Air) ↔ Wall St / Midtown | `—` | **KEEP** | — |
| featured | new-york/p3 | Pier 11 / Wall Street → Long Island City | `ics-db90a41958` | **KEEP** | — |
| featured | new-york/p3 | Midtown (W 39th) ↔ Hoboken / Jersey City waterfron | `—` | **KEEP** | — |
| featured | new-york/p3 | Manhattan (E 34th) ↔ Montauk / the Hamptons | `—` | **KEEP** | — |
| journey | market:miami | Miami → Miami | `ics-157f49e9db` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Miami' → 'Miami' vs route 'b |
| journey | market:miami | Downtown → Key Biscayne | `—` | **KEEP** | — |
| journey | market:miami | Nassau Cruise Port → Paradise Island Ferry Termina | `ics-05ae8c432d` | **KEEP** | — |
| journey | market:miami | Palm Beach / Treasure Coast → Miami | `edge-1140` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Palm Beach / Treasure Coast' |
| featured | miami/p1 | Miami → Miami | `ics-1af92cf817` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Miami' → 'Miami' vs route 'b |
| featured | miami/p1 | Downtown ↔ Key Biscayne | `—` | **KEEP** | — |
| featured | miami/p1 | Miami → Nassau & The Bahamas | `edge__miami-florida-usa__nassau-bahamas` | **KEEP** | — |
| featured | miami/p2 | Palm Beach / Treasure Coast → Miami | `edge-1140` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Palm Beach / Treasure Coast' |
| featured | miami/p2 | Miami → Nassau & The Bahamas | `edge__miami-florida-usa__nassau-bahamas` | **KEEP** | — |
| featured | miami/p3 | Miami → Miami | `ics-157f49e9db` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Miami' → 'Miami' vs route 'b |
| featured | miami/p3 | Downtown ↔ Key Biscayne | `—` | **KEEP** | — |
| featured | miami/p3 | Miami → Nassau & The Bahamas | `edge__miami-florida-usa__nassau-bahamas` | **KEEP** | — |
| journey | market:bay-area | San Francisco Bay Area → San Francisco Bay Area | `ics-55f418e3b7` | **KEEP** | — |
| journey | market:bay-area | San Francisco Bay Area → San Francisco Bay Area | `ics-f789facf6a` | **KEEP** | — |
| journey | market:bay-area | SF → Redwood City / South Bay | `—` | **KEEP** | — |
| journey | market:bay-area | SF → Monterey | `—` | **KEEP** | — |
| featured | bay-area/p1 | San Francisco Bay Area → San Francisco Bay Area | `ics-55f418e3b7` | **KEEP** | — |
| featured | bay-area/p1 | San Francisco Bay Area → San Francisco Bay Area | `ics-f789facf6a` | **KEEP** | — |
| featured | bay-area/p1 | SF ↔ Redwood City / South Bay | `—` | **KEEP** | — |
| featured | bay-area/p2 | SF ↔ Monterey | `—` | **KEEP** | — |
| featured | bay-area/p2 | SF ↔ Tiburon / Angel Island | `—` | **KEEP** | — |
| featured | bay-area/p3 | San Francisco Bay Area → San Francisco Bay Area | `ics-55f418e3b7` | **KEEP** | — |
| featured | bay-area/p3 | San Francisco Bay Area → San Francisco Bay Area | `ics-f789facf6a` | **KEEP** | — |
| featured | bay-area/p3 | SF ↔ Redwood City / South Bay | `—` | **KEEP** | — |
| journey | market:seattle | Seattle & Puget Sound → Seattle & Puget Sound | `ics-a89317f4d8` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Seattle & Puget Sound' → 'Se |
| journey | market:seattle | Seattle & Puget Sound → Seattle & Puget Sound | `ics-411349a32d` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Seattle & Puget Sound' → 'Se |
| journey | market:seattle | Seattle & Puget Sound → Seattle & Puget Sound | `ics-87113f8e23` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Seattle & Puget Sound' → 'Se |
| journey | market:seattle | Seattle & Puget Sound → Seattle & Puget Sound | `ics-87113f8e23` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Seattle & Puget Sound' → 'Se |
| featured | seattle/p1 | Seattle & Puget Sound → Seattle & Puget Sound | `ics-f0a554937c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Seattle & Puget Sound' → 'Se |
| featured | seattle/p1 | Colman Dock (Seattle Ferry Terminal) → Bremerton F | `ics-8fd3195215` | **KEEP** | — |
| featured | seattle/p1 | Seattle & Puget Sound → Seattle & Puget Sound | `ics-87113f8e23` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Seattle & Puget Sound' → 'Se |
| featured | seattle/p2 | Seattle & Puget Sound → Seattle & Puget Sound | `ics-87113f8e23` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Seattle & Puget Sound' → 'Se |
| featured | seattle/p3 | Seattle & Puget Sound → Seattle & Puget Sound | `ics-a89317f4d8` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Seattle & Puget Sound' → 'Se |
| featured | seattle/p3 | Seattle & Puget Sound → Seattle & Puget Sound | `ics-411349a32d` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Seattle & Puget Sound' → 'Se |
| featured | seattle/p3 | Seattle & Puget Sound → Seattle & Puget Sound | `ics-87113f8e23` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Seattle & Puget Sound' → 'Se |
| journey | market:boston | Boston & New England → Boston & New England | `ics-411ccfe7ad` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Boston & New England' → 'Bos |
| journey | market:boston | Long Wharf (Boston) → Hingham Shipyard | `ics-1ad04e17ae` | **KEEP** | — |
| journey | market:boston | Boston → Provincetown | `ics-4df4cecf34` | **KEEP** | — |
| journey | market:boston | Boston → Martha's Vineyard / Nantucket | `—` | **KEEP** | — |
| featured | boston/p1 | Long Wharf (Boston) → Salem Ferry Wharf | `ics-3b05a4e262` | **KEEP** | — |
| featured | boston/p1 | Long Wharf (Boston) → Provincetown (MacMillan Pier | `ics-4df4cecf34` | **KEEP** | — |
| featured | boston/p1 | Long Wharf (Boston) → Provincetown (MacMillan Pier | `ics-4df4cecf34` | **KEEP** | — |
| featured | boston/p2 | Hyannis Terminal → Oak Bluffs (Martha's Vineyard) | `e__boston-new-england-usa__hyannis-terminal__oak-bluffs-martha-s-vineyard` | **KEEP** | — |
| featured | boston/p2 | Long Wharf (Boston) → Hull / Pemberton | `ics-dae71e1b16` | **KEEP** | — |
| featured | boston/p3 | Boston & New England → Boston & New England | `ics-411ccfe7ad` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Boston & New England' → 'Bos |
| featured | boston/p3 | Long Wharf (Boston) → Hingham Shipyard | `ics-1ad04e17ae` | **KEEP** | — |
| featured | boston/p3 | Long Wharf (Boston) → Provincetown (MacMillan Pier | `ics-4df4cecf34` | **KEEP** | — |
| journey | market:athens-cyclades | E1 Gate Ferry to Kos - Piraeus Port → View Yacht - | `rn-7f7c38a84c7c` | **KEEP** | — |
| journey | market:athens-cyclades | E1 Gate Ferry to Kos - Piraeus Port → Skala Marina | `rn-16fa8284adf1` | **KEEP** | — |
| journey | market:athens-cyclades | Mykonos & the Cyclades → Santorini & the South Cyc | `rn-cb0ec9d194ca` | **KEEP** | — |
| journey | market:athens-cyclades | Mykonos New Port (Tourlos) → Naxos Port (Chora) | `rn-dc595b5a6ab8` | **KEEP** | — |
| featured | athens-cyclades/p1 | E1 Gate Ferry to Kos - Piraeus Port → View Yacht - | `rn-7f7c38a84c7c` | **KEEP** | — |
| featured | athens-cyclades/p1 | E1 Gate Ferry to Kos - Piraeus Port → Skala Marina | `rn-16fa8284adf1` | **KEEP** | — |
| featured | athens-cyclades/p1 | Mykonos & the Cyclades → Santorini & the South Cyc | `rn-cb0ec9d194ca` | **KEEP** | — |
| featured | athens-cyclades/p2 | Mykonos New Port (Tourlos) → Naxos Port (Chora) | `rn-dc595b5a6ab8` | **KEEP** | — |
| featured | athens-cyclades/p2 | Marina Zeas (Piraeus) → 2nd Glyfada Marina | `rn-89552c9786ec` | **KEEP** | — |
| featured | athens-cyclades/p3 | E1 Gate Ferry to Kos - Piraeus Port → View Yacht - | `rn-7f7c38a84c7c` | **KEEP** | — |
| featured | athens-cyclades/p3 | E1 Gate Ferry to Kos - Piraeus Port → Skala Marina | `rn-16fa8284adf1` | **KEEP** | — |
| featured | athens-cyclades/p3 | Mykonos & the Cyclades → Santorini & the South Cyc | `rn-cb0ec9d194ca` | **KEEP** | — |
