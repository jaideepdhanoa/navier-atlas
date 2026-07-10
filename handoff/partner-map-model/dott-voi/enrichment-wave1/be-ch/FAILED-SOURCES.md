# Failed / partial sources — Belgium + Switzerland lane

Accessed 2026-07-10. These failures are non-blocking unless stated.

| Source | Result | Replacement / disposition |
|---|---|---|
| `https://visit.gent.be/en/see-do/boat-ghent` | Returned Visit Gent 404 page. | Replaced with official Visit Gent pages for Gent Watertoerist (`/en/see-do/gent-watertoerist`) and Portus Ganda (`/en/see-do/portus-ganda`). |
| Direct operator timetable PDFs for ZSG and SBS | Binary/PDF extraction was partial in web tooling. | Used official operator timetable pages and retained 2026 timetable provenance. Grok must independently validate exact schedule/landing records before banking. |
| Herstal-specific passenger landing search | No authoritative specific named Herstal pier/terminal was verified. | `bp_id: null`; Herstal remains a hold. Do not substitute a Liège BP by proximity. |
| Goldach passenger-stop search | No scheduled passenger stop was verified, but the municipality documents the named Hafen Rietli marina. | Kept as a named marina candidate with `bp_id: null`; public-pickup/access QA required. |
| Biel boarding-point research | Not attempted; outside the payload's named priority set. | Kept as P2 `new_city_brief_needed`; no BP or route candidate. |

## Important source caveat

Official Dott/Voi city directories prove current partner city/service-area listing, not marine pickup, pier access, route viability, or every-city coverage from a country row. Marine-system and BP evidence is separately cited in the handoff.
