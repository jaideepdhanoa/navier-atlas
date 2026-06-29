# Proposal fidelity — caribbean

**Verdict:** REWRITE
**Checked:** 2026-06-29T15:13:42Z

## Summary

- Items audited: 112
- KEEP: 101
- DROP: 11
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 11

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Nassau Cruise Port → Paradise Island Ferry Termina | `ics-05ae8c432d` | **KEEP** | — |
| journey | — | San Juan → Spanish Virgins / marina day-trip layer | `—` | **KEEP** | — |
| journey | — | USVI/BVI → short inter-island hops | `—` | **KEEP** | — |
| journey | — | Barbados → licensed taxi + coastal resort water la | `—` | **KEEP** | — |
| featured | 1 | Nassau Cruise Port → Paradise Island Ferry Termina | `ics-05ae8c432d` | **KEEP** | — |
| featured | 1 | Puerto Rico (San Juan & the Spanish Virgins) → Pue | `ics-0eef25abd8` | **KEEP** | — |
| featured | 1 | US & British Virgin Islands → US & British Virgin  | `ics-47ff344fca` | **DROP** | bp_binding: labels ≠ route endpoints: card 'US & British Virgin Islands' |
| featured | 2 | Bridgetown Harbour → Port Barbados Main Gate | `rn-3a37afb0fb5c` | **KEEP** | — |
| featured | 2 | St Lucia & Grenadines island layer | `—` | **KEEP** | — |
| featured | 3 | Falmouth Jamaica Cruise Ship Pier best day tour →  | `ics-68472200b9` | **KEEP** | — |
| featured | 3 | Samaná Peninsula & Bay — Dominican Republic → Las  | `rn-342daebb3603` | **KEEP** | — |
| featured | 3 | ABC islands marina layer | `—` | **KEEP** | — |
| journey | market:bahamas | Nassau Cruise Port → Paradise Island Ferry Termina | `ics-05ae8c432d` | **KEEP** | — |
| featured | bahamas/p1 | Nassau Cruise Port → Paradise Island Ferry Termina | `ics-05ae8c432d` | **KEEP** | — |
| featured | bahamas/p1 | Puerto Rico (San Juan & the Spanish Virgins) → Pue | `ics-0eef25abd8` | **KEEP** | — |
| featured | bahamas/p1 | US & British Virgin Islands → US & British Virgin  | `ics-47ff344fca` | **DROP** | bp_binding: labels ≠ route endpoints: card 'US & British Virgin Islands' |
| featured | bahamas/p2 | Bridgetown Harbour → Port Barbados Main Gate | `rn-3a37afb0fb5c` | **KEEP** | — |
| featured | bahamas/p2 | St Lucia & Grenadines island layer | `—` | **KEEP** | — |
| featured | bahamas/p3 | Falmouth Jamaica Cruise Ship Pier best day tour →  | `ics-68472200b9` | **KEEP** | — |
| featured | bahamas/p3 | Samaná Peninsula & Bay — Dominican Republic → Las  | `rn-342daebb3603` | **KEEP** | — |
| featured | bahamas/p3 | ABC islands marina layer | `—` | **KEEP** | — |
| journey | market:puerto-rico | Puerto Rico / San Juan → marina/resort/coastal cat | `—` | **KEEP** | — |
| featured | puerto-rico/p1 | Nassau Cruise Port → Paradise Island Ferry Termina | `ics-05ae8c432d` | **KEEP** | — |
| featured | puerto-rico/p1 | Puerto Rico (San Juan & the Spanish Virgins) → Pue | `ics-0eef25abd8` | **KEEP** | — |
| featured | puerto-rico/p1 | US & British Virgin Islands → US & British Virgin  | `ics-47ff344fca` | **DROP** | bp_binding: labels ≠ route endpoints: card 'US & British Virgin Islands' |
| featured | puerto-rico/p2 | Bridgetown Harbour → Port Barbados Main Gate | `rn-3a37afb0fb5c` | **KEEP** | — |
| featured | puerto-rico/p2 | St Lucia & Grenadines island layer | `—` | **KEEP** | — |
| featured | puerto-rico/p3 | Falmouth Jamaica Cruise Ship Pier best day tour →  | `ics-68472200b9` | **KEEP** | — |
| featured | puerto-rico/p3 | Samaná Peninsula & Bay — Dominican Republic → Las  | `rn-342daebb3603` | **KEEP** | — |
| featured | puerto-rico/p3 | ABC islands marina layer | `—` | **KEEP** | — |
| journey | market:usvi-bvi | US & British Virgin Islands → marina/resort/coasta | `—` | **KEEP** | — |
| featured | usvi-bvi/p1 | Nassau Cruise Port → Paradise Island Ferry Termina | `ics-05ae8c432d` | **KEEP** | — |
| featured | usvi-bvi/p1 | Puerto Rico (San Juan & the Spanish Virgins) → Pue | `ics-0eef25abd8` | **KEEP** | — |
| featured | usvi-bvi/p1 | US & British Virgin Islands → US & British Virgin  | `ics-47ff344fca` | **DROP** | bp_binding: labels ≠ route endpoints: card 'US & British Virgin Islands' |
| featured | usvi-bvi/p2 | Bridgetown Harbour → Port Barbados Main Gate | `rn-3a37afb0fb5c` | **KEEP** | — |
| featured | usvi-bvi/p2 | St Lucia & Grenadines island layer | `—` | **KEEP** | — |
| featured | usvi-bvi/p3 | Falmouth Jamaica Cruise Ship Pier best day tour →  | `ics-68472200b9` | **KEEP** | — |
| featured | usvi-bvi/p3 | Samaná Peninsula & Bay — Dominican Republic → Las  | `rn-342daebb3603` | **KEEP** | — |
| featured | usvi-bvi/p3 | ABC islands marina layer | `—` | **KEEP** | — |
| journey | market:barbados | Bridgetown Harbour → Port Barbados Main Gate | `rn-3a37afb0fb5c` | **KEEP** | — |
| featured | barbados/p1 | Nassau Cruise Port → Paradise Island Ferry Termina | `ics-05ae8c432d` | **KEEP** | — |
| featured | barbados/p1 | Puerto Rico (San Juan & the Spanish Virgins) → Pue | `ics-0eef25abd8` | **KEEP** | — |
| featured | barbados/p1 | US & British Virgin Islands → US & British Virgin  | `ics-47ff344fca` | **DROP** | bp_binding: labels ≠ route endpoints: card 'US & British Virgin Islands' |
| featured | barbados/p2 | Bridgetown Harbour → Port Barbados Main Gate | `rn-3a37afb0fb5c` | **KEEP** | — |
| featured | barbados/p2 | St Lucia & Grenadines island layer | `—` | **KEEP** | — |
| featured | barbados/p3 | Falmouth Jamaica Cruise Ship Pier best day tour →  | `ics-68472200b9` | **KEEP** | — |
| featured | barbados/p3 | Samaná Peninsula & Bay — Dominican Republic → Las  | `rn-342daebb3603` | **KEEP** | — |
| featured | barbados/p3 | ABC islands marina layer | `—` | **KEEP** | — |
| journey | market:jamaica | Montego Bay & Jamaica → marina/resort/coastal catc | `—` | **KEEP** | — |
| featured | jamaica/p1 | Nassau Cruise Port → Paradise Island Ferry Termina | `ics-05ae8c432d` | **KEEP** | — |
| featured | jamaica/p1 | Puerto Rico (San Juan & the Spanish Virgins) → Pue | `ics-0eef25abd8` | **KEEP** | — |
| featured | jamaica/p1 | US & British Virgin Islands → US & British Virgin  | `ics-47ff344fca` | **DROP** | bp_binding: labels ≠ route endpoints: card 'US & British Virgin Islands' |
| featured | jamaica/p2 | Bridgetown Harbour → Port Barbados Main Gate | `rn-3a37afb0fb5c` | **KEEP** | — |
| featured | jamaica/p2 | St Lucia & Grenadines island layer | `—` | **KEEP** | — |
| featured | jamaica/p3 | Falmouth Jamaica Cruise Ship Pier best day tour →  | `ics-68472200b9` | **KEEP** | — |
| featured | jamaica/p3 | Samaná Peninsula & Bay — Dominican Republic → Las  | `rn-342daebb3603` | **KEEP** | — |
| featured | jamaica/p3 | ABC islands marina layer | `—` | **KEEP** | — |
| journey | market:dominican-republic | Samaná / Dominican Republic → marina/resort/coasta | `—` | **KEEP** | — |
| featured | dominican-republic/p1 | Nassau Cruise Port → Paradise Island Ferry Termina | `ics-05ae8c432d` | **KEEP** | — |
| featured | dominican-republic/p1 | Puerto Rico (San Juan & the Spanish Virgins) → Pue | `ics-0eef25abd8` | **KEEP** | — |
| featured | dominican-republic/p1 | US & British Virgin Islands → US & British Virgin  | `ics-47ff344fca` | **DROP** | bp_binding: labels ≠ route endpoints: card 'US & British Virgin Islands' |
| featured | dominican-republic/p2 | Bridgetown Harbour → Port Barbados Main Gate | `rn-3a37afb0fb5c` | **KEEP** | — |
| featured | dominican-republic/p2 | St Lucia & Grenadines island layer | `—` | **KEEP** | — |
| featured | dominican-republic/p3 | Falmouth Jamaica Cruise Ship Pier best day tour →  | `ics-68472200b9` | **KEEP** | — |
| featured | dominican-republic/p3 | Samaná Peninsula & Bay — Dominican Republic → Las  | `rn-342daebb3603` | **KEEP** | — |
| featured | dominican-republic/p3 | ABC islands marina layer | `—` | **KEEP** | — |
| journey | market:st-lucia-grenadines | St Lucia & the Grenadines → marina/resort/coastal  | `—` | **KEEP** | — |
| featured | st-lucia-grenadines/p1 | Nassau Cruise Port → Paradise Island Ferry Termina | `ics-05ae8c432d` | **KEEP** | — |
| featured | st-lucia-grenadines/p1 | Puerto Rico (San Juan & the Spanish Virgins) → Pue | `ics-0eef25abd8` | **KEEP** | — |
| featured | st-lucia-grenadines/p1 | US & British Virgin Islands → US & British Virgin  | `ics-47ff344fca` | **DROP** | bp_binding: labels ≠ route endpoints: card 'US & British Virgin Islands' |
| featured | st-lucia-grenadines/p2 | Bridgetown Harbour → Port Barbados Main Gate | `rn-3a37afb0fb5c` | **KEEP** | — |
| featured | st-lucia-grenadines/p2 | St Lucia & Grenadines island layer | `—` | **KEEP** | — |
| featured | st-lucia-grenadines/p3 | Falmouth Jamaica Cruise Ship Pier best day tour →  | `ics-68472200b9` | **KEEP** | — |
| featured | st-lucia-grenadines/p3 | Samaná Peninsula & Bay — Dominican Republic → Las  | `rn-342daebb3603` | **KEEP** | — |
| featured | st-lucia-grenadines/p3 | ABC islands marina layer | `—` | **KEEP** | — |
| journey | market:turks-caicos | Turks & Caicos → marina/resort/coastal catchment | `—` | **KEEP** | — |
| featured | turks-caicos/p1 | Nassau Cruise Port → Paradise Island Ferry Termina | `ics-05ae8c432d` | **KEEP** | — |
| featured | turks-caicos/p1 | Puerto Rico (San Juan & the Spanish Virgins) → Pue | `ics-0eef25abd8` | **KEEP** | — |
| featured | turks-caicos/p1 | US & British Virgin Islands → US & British Virgin  | `ics-47ff344fca` | **DROP** | bp_binding: labels ≠ route endpoints: card 'US & British Virgin Islands' |
| featured | turks-caicos/p2 | Bridgetown Harbour → Port Barbados Main Gate | `rn-3a37afb0fb5c` | **KEEP** | — |
| featured | turks-caicos/p2 | St Lucia & Grenadines island layer | `—` | **KEEP** | — |
| featured | turks-caicos/p3 | Falmouth Jamaica Cruise Ship Pier best day tour →  | `ics-68472200b9` | **KEEP** | — |
| featured | turks-caicos/p3 | Samaná Peninsula & Bay — Dominican Republic → Las  | `rn-342daebb3603` | **KEEP** | — |
| featured | turks-caicos/p3 | ABC islands marina layer | `—` | **KEEP** | — |
| journey | market:cayman | Cayman Islands → marina/resort/coastal catchment | `—` | **KEEP** | — |
| featured | cayman/p1 | Nassau Cruise Port → Paradise Island Ferry Termina | `ics-05ae8c432d` | **KEEP** | — |
| featured | cayman/p1 | Puerto Rico (San Juan & the Spanish Virgins) → Pue | `ics-0eef25abd8` | **KEEP** | — |
| featured | cayman/p1 | US & British Virgin Islands → US & British Virgin  | `ics-47ff344fca` | **DROP** | bp_binding: labels ≠ route endpoints: card 'US & British Virgin Islands' |
| featured | cayman/p2 | Bridgetown Harbour → Port Barbados Main Gate | `rn-3a37afb0fb5c` | **KEEP** | — |
| featured | cayman/p2 | St Lucia & Grenadines island layer | `—` | **KEEP** | — |
| featured | cayman/p3 | Falmouth Jamaica Cruise Ship Pier best day tour →  | `ics-68472200b9` | **KEEP** | — |
| featured | cayman/p3 | Samaná Peninsula & Bay — Dominican Republic → Las  | `rn-342daebb3603` | **KEEP** | — |
| featured | cayman/p3 | ABC islands marina layer | `—` | **KEEP** | — |
| journey | market:antigua | Antigua & Barbuda → marina/resort/coastal catchmen | `—` | **KEEP** | — |
| featured | antigua/p1 | Nassau Cruise Port → Paradise Island Ferry Termina | `ics-05ae8c432d` | **KEEP** | — |
| featured | antigua/p1 | Puerto Rico (San Juan & the Spanish Virgins) → Pue | `ics-0eef25abd8` | **KEEP** | — |
| featured | antigua/p1 | US & British Virgin Islands → US & British Virgin  | `ics-47ff344fca` | **DROP** | bp_binding: labels ≠ route endpoints: card 'US & British Virgin Islands' |
| featured | antigua/p2 | Bridgetown Harbour → Port Barbados Main Gate | `rn-3a37afb0fb5c` | **KEEP** | — |
| featured | antigua/p2 | St Lucia & Grenadines island layer | `—` | **KEEP** | — |
| featured | antigua/p3 | Falmouth Jamaica Cruise Ship Pier best day tour →  | `ics-68472200b9` | **KEEP** | — |
| featured | antigua/p3 | Samaná Peninsula & Bay — Dominican Republic → Las  | `rn-342daebb3603` | **KEEP** | — |
| featured | antigua/p3 | ABC islands marina layer | `—` | **KEEP** | — |
| journey | market:abc-islands | Spanish Water / Caracasbaai (Jan Thiel) → Kralendi | `rn-0f8e77cfef46` | **KEEP** | — |
| journey | market:abc-islands | Kralendijk Town Pier → Klein Bonaire dive transfer | `rn-f23a5af76773` | **KEEP** | — |
| journey | market:abc-islands | Oranjestad Cruise Terminal (Aruba) → Palm Beach re | `rn-7839c5ad6d42` | **KEEP** | — |
| journey | market:abc-islands | Renaissance Marina (Oranjestad) → Spanish Water /  | `rn-e96930f83c0f` | **KEEP** | — |
| featured | abc-islands/p1 | Kralendijk Town Pier → Klein Bonaire dive transfer | `rn-f23a5af76773` | **KEEP** | — |
| featured | abc-islands/p1 | Oranjestad Cruise Terminal → Palm Beach resort str | `rn-7839c5ad6d42` | **KEEP** | — |
| featured | abc-islands/p2 | Kralendijk Town Pier → Klein Bonaire dive transfer | `rn-f23a5af76773` | **KEEP** | — |
| featured | abc-islands/p2 | Oranjestad Cruise Terminal → Palm Beach resort str | `rn-7839c5ad6d42` | **KEEP** | — |
| featured | abc-islands/p3 | Kralendijk Town Pier → Klein Bonaire dive transfer | `rn-f23a5af76773` | **KEEP** | — |
| featured | abc-islands/p3 | Oranjestad Cruise Terminal → Palm Beach resort str | `rn-7839c5ad6d42` | **KEEP** | — |
