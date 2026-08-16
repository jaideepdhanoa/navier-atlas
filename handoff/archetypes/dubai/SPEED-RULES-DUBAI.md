# SPEED-RULES-DUBAI (internal audit file — never renders)

Accessed 2026-08-16. Governs schedule math in REVENUE-STACK-DUBAI.md.

## Who sets and enforces limits (PRIMARY-VERIFIED)

- **Legal basis:** Executive Council Resolution No. 9 of 2020 (amending ECR 11/2013, implementing Law 11/2010 — Licensing of Vessels in the Emirate of Dubai), Art. 52(a)(5): the DMA/DMCA, in coordination with concerned government entities, **"determine[s] authorised speed limits"** and (52(a)(4)) the authorised/prohibited routes and areas. Full text loaded: https://dlp.dubai.gov.ae/Legislation%20Reference/2020/Executive%20Council%20Resolution%20No.%20(9)%20of%202020%20Amending%20Executive%20Council%20Resolution%20No.%20(11)%20of%202013.html
- **Fine schedule (same primary source, Schedule 2):** for vessels <24 m — exceeding the limit by 2 kn: AED 1,000 (item 18); by 5 kn: AED 2,000 (item 19); by 7 kn: AED 3,000 (item 20). Navigating prohibited areas: AED 5,000 (item 24). Purpose of the regime as expressed in the schedule: navigation safety, wake/disturbance ("annoying or disturbing others during use of Vessels", AED 2,000, item 39), and environment (untreated discharge AED 20,000; low-sulphur fuel requirement item 71).
- **Enforcement:** Dubai Police hand-held marine radar targeting ports/marinas (secondary, Jan 2026 — see below).

## The numeric limits (SECONDARY-VERIFIED — flag)

The zone-by-zone numeric limits below are consistently reported but were captured this run only from a secondary reproduction (glamour-yacht.com, 26 Jan 2026, reproducing superyachtnews.com: https://www.glamour-yacht.com/dmca-imposed-new-speed-limits-and-no-wake-zones-in-uae/ — content matches the long-standing DMCA safe-navigation regime). **No DMA local order / navigation circular PDF was primary-loaded this run.** Treatment: schedule math uses these values as CONSERVATIVE CONTROLLING LIMITS; any corridor whose time depends on them is flagged conservative-basis.

| Zone | Limit | Status |
|---|---|---|
| Inside Dubai ports, marinas, harbour basins (incl. Dubai Marina, Dubai Harbour, Mina Rashid basins) | **5 kn** | secondary-verified |
| Dubai Creek (Khor Dubai) and Al Mamzar waters | **7 kn** | secondary-verified |
| Narrow waterways ≤600 m wide; passing between two islands or island↔coast (applies to Palm Jumeirah lagoons/fronds and World Islands interior passages) | **7 kn** | secondary-verified |
| Within 300 m of a beach (emergency entry only), within anchorage areas for small craft, within 50 m of moorings/diving platforms/loading docks | **7 kn** | secondary-verified |
| Dubai Water Canal | high-speed prohibited; **no numeric limit primary- or secondary-captured** → planning basis **6 kn average** (ASSUMPTION, conservative; canal hosts RTA heritage-abra service at AED 25/hr sightseeing pace) | NOT VERIFIED — conservative basis |
| Open Gulf coast (offshore, away from signed areas) | high-speed cruising permitted only in approved open-water zones; no numeric cap captured | foiling transit modeled at N45 service speed 25 kn (canon vessel spec — flag for confirmation) |
| Signed local limits | posted navigation signs override everything above | — |

## Purpose of each rule → relief logic ("what relief unlocks" only; never base math)

- The 5/7-kn zones exist for **wake damage, moored-vessel disturbance, swimmer/small-craft safety, and noise** (fine schedule items 25, 28, 39). A foiling hull at speed produces minimal wake and near-zero noise — the rules' own stated purposes are served at higher speed than a planing hull can manage. A DMA-granted corridor-specific relief (e.g., 12–15 kn foil-borne in the outer Marina channel or Water Canal) would cut the spine corridor time by ~10–12 min (see REVENUE-STACK zone table). **Base schedules do NOT assume any relief.**
- Prohibited areas (item 24) and DMA route determination (Art. 52) mean corridor design is a licensing conversation, not a unilateral choice — consistent with the "extend your network" posture.

## Corridor time basis (fed to REVENUE-STACK)

- Harbor/marina entry-exit segments: 5 kn.
- Creek segments: 7 kn. Water Canal segments: 6 kn (conservative assumption, above).
- Palm lagoon / island-passage segments: 7 kn.
- Open-coast segments: 25 kn (N45 service speed, canon — flag).
- Dock dwell: 2 min per call (assumption).

All GEOMETRY-DUBAI.json distances are route nm; segment splits per corridor are estimates from chart geography (labeled in stack file).
