# NODES-JEDDAH — network design (geometry authored here; NO Atlas corridor set exists for Jeddah)

Internal audit file. All geometry is NEW, authored for later Grok seal — **no route IDs invented**; lines carry working names only. Coordinates: verified where a primary/authoritative source exists, else DERIVED from map evidence with an explicit flag. Distances: haversine from coordinates [DERIVED]. Times: 25 kn open water, 8 kn creek/harbour regime (see SPEED-RULES), +3 min dwell per intermediate stop. Research date: 2026-08-16.

## Shoreline architecture
Jeddah's waterfront is LONG and LINEAR (~30 km corniche) with one deep sheltered inlet (Obhur Creek) at the north and a major working port (JIP) at the south. Natural architecture: **coastal trunk line + creek feeder + north leisure line**, hub at Jeddah Yacht Club. The existing 3-station water taxi (Al-Balad/port ↔ JYC ↔ Obhur) already traces the trunk — the network below EXTENDS the city's own announced 20-station ambition.

## Node inventory (9 catalogued: 6 verified-active, 2 status-flagged, 1 roadmap)
| # | Node | Coordinates | Evidence | Status |
|---|---|---|---|---|
| N1 | **Jeddah Yacht Club & Marina** (HUB) | 21.6482 N, 39.0992 E | jeddahyc.com berth-holder guidebook coordinates [PRIMARY]; ~91 berths, to 115–120 m [SECONDARY]; live water-taxi station [PRIMARY-quality report] | VERIFIED-ACTIVE |
| N2 | **Al-Balad / Port-side station** (Historic Jeddah via JIP) | ≈21.490 N, 39.155 E [DERIVED approx — station sits in port waters serving Al-Balad; exact berth TBC with JTC/Mawani] | Operating water-taxi station; golf-cart last-mile to Al-Balad (Ministry of Culture agreement) [PRIMARY-quality report, Arab News 2592678] | VERIFIED-ACTIVE (coords approx) |
| N3 | **Sharm Obhur mouth station** (south bank, creek entrance) | ≈21.708 N, 39.093 E [DERIVED approx] | Announced third water-taxi station "Sharm Obhur (opening soon)" [SECONDARY, Saudi Gazette/TimeOut corroborating PRIMARY-quality report] | ANNOUNCED — status-flag |
| N4 | **Red Sea Marina, North Obhur** | 21.7225 N, 39.1062 E [SECONDARY — marina-directory chart position; operator confirms North Obhur creek bank] | redseamarina.com [PRIMARY operator]: 300 wet berths, 3 jetties, yachts to 60 m; SRSA-licensed 2024 [SECONDARY citing SRSA] | VERIFIED-ACTIVE |
| N5 | **Al Ahlam Marina, Obhur Creek** | ≈21.740 N, 39.130 E [DERIVED approx — mid-creek; verify berth-side coords in seal pass] | Active charter marina; SRSA first-cohort tourist-marina license 2024 [SECONDARY citing SRSA]; charter scene evidence [SECONDARY] | VERIFIED-ACTIVE (coords approx) |
| N6 | **Al-Nawras Island marina** (north corniche) | ≈21.625 N, 39.103 E [DERIVED approx — north corniche, adjacent Prince Faisal bin Fahd walkway] | Amanah rec-zone incl. "a marina for boats" [SECONDARY citing Saudipedia]; Tarfeeh Fakieh + Samaco Marine agreement to develop/operate Al Nawras Marina, vessels to 30 m+ — alnahlagroup.com [PRIMARY corporate] | VERIFIED (development-stage — status-flag) |
| N7 | **Durrat Al-Arus Marina** (north resort town) | 21.9375 N, 38.9547 E [SECONDARY — latitude.to gazetteer] | Operating resort marina, full-service [SECONDARY directories]; Visit Saudi promotion [PRIMARY existence] | VERIFIED-ACTIVE |
| N8 | **Jeddah Central marina/pier** (JCDC) | ≈21.510 N, 39.160 E [DERIVED approx — 9.5 km waterfront site, central corniche; fix at seal] | Marina + pier in Phase 1, complete end-2027 — jeddahcentral.com [PRIMARY] | PLANNED — status-flag, roadmap infill |
| N9 | **Bay La Sun Marina, KAEC** (~40+ nm north) | ≈22.349 N, 39.078 E [DERIVED approx] | KAEC operating marina [SECONDARY]; Haramain rail links KAEC [SECONDARY] | VERIFIED-ACTIVE — **ROADMAP-ONLY node** (range/positioning) |
Held out (fail closed): Al-Hamra corniche landing and South Corniche landings — no verified existing berth/jetty found [UNSOURCED — candidates for the Mayoralty's 20-station buildout; do not render]. Bayada Island — experience waypoint, no fixed landing verified [UNSOURCED].

## Line design (3 lines + 1 roadmap; MECE; interchanges: N1 hub + N3)
MECE check: Obhur cluster {N3,N4,N5} is touched by 2 lines ≤ ceil(3/2)=2 ✓; corniche cluster {N1,N2,N6,N8} by 1 base line ✓; north {N7} by 1 ✓. Two interchanges total (N1, N3) ✓.

### JED-1 · Corniche Spine (south ↔ north) — extends the live water-taxi trunk
Al-Balad/Port (N2) → [N8 Jeddah Central, infill 2027+] → Al-Nawras (N6, when open) → JYC (N1) → Sharm Obhur mouth (N3)
| Leg | nm [DERIVED] | Time @25 kn | Regime |
|---|---|---|---|
| N2 → N1 | 10.0 | 24 min | first/last ~1 nm harbour regime adds ~4 min → **~28 min** |
| N1 → N3 | 3.6 | 9 min | open water |
| Full spine N2→N3 (2 intermediate dwells when N6/N8 active: base = 1 stop at N1) | 13.5 direct | **~40 min end-to-end incl. dwell + harbour regime** | |
Infill legs: N2→N8 1.2 nm (~7 min harbour regime); N8→N1 9.0 min 22 min; N6→N1 ~2.4 nm ~6 min.
Purpose: the commuter + visitor trunk; the water-taxi trial proves the alignment, Navier upgrades speed (30-min leisure ride → ~28-min N2↔N1 express with 25-kn cruise vs displacement).
Southern constraint: N2 sits in JIP waters — fairway crossing/harbour speed per harbourmaster (SPEED-RULES).

### JED-2 · Obhur Creek Feeder (in-creek, low-wake)
Sharm Obhur mouth (N3) → Red Sea Marina (N4) → Al Ahlam (N5), 8 kn creek regime
| Leg | nm | Time @8 kn |
|---|---|---|
| N3 → N4 | 1.1 | 8 min |
| N4 → N5 | 1.7 | 13 min |
| Full feeder + 1 dwell | 2.8 | **~24 min** |
Purpose: connects the creek's marina/resort economy to the spine at N3; doubles as experience staging (charters originate in the creek).

### JED-3 · North Leisure Line (weekend/experience)
JYC (N1) → Sharm Obhur mouth (N3) → Durrat Al-Arus (N7)
| Leg | nm | Time @25 kn |
|---|---|---|
| N1 → N3 | 3.6 | 9 min |
| N3 → N7 | 15.8 | 38 min |
| Full N1→N7 + 1 dwell | 19.4 | **~50 min** |
Purpose: resort-day/leisure loops north; tourism-weighted per addendum (L3 headline). Weekend-shaped schedule.

### JED-X · KAEC Express (ROADMAP ONLY — do not render as base network)
JYC (N1) → Bay La Sun, KAEC (N9): **42.1 nm, ~101 min @25 kn** [DERIVED]. Roadmap flag: distance is commercially long for a scheduled N45 line; render amber-dashed roadmap only, no economics. KAEC is also Haramain-rail-served [SECONDARY] — water value is leisure/event, not commute.

## Design notes for seal pass
- Verify exact berth coordinates for N2, N3, N5, N6, N8 on-map before Grok seal; all flagged DERIVED-approx above.
- Reef passes: bind JED-1/JED-3 alignments to the SRSA/GEOSA Red Sea navigation map when obtainable (redsea.gov.sa geo-blocked this pass).
- F1 weekend: JED-1 segment N6↔N1 runs alongside the circuit; expect event exclusion windows + surge charter ops from JYC.
- No existing Atlas corridors for Jeddah; the partner-file Jeddah journey ("Jeddah Corniche — North Public Pier ↔ Jeddah Yacht Club & Marina", route rn-05bf6ff26cb5) is Atlas-side background only — its "North Public Pier" label was NOT verifiable as an existing landing this pass [UNSOURCED — not in node inventory; flag for Grok locale cleanup (#119) if that route renders a stop there].
