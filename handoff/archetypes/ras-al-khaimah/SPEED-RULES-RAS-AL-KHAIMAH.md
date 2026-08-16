# SPEED-RULES-RAS-AL-KHAIMAH (internal audit file — never renders)

**As of:** 2026-08-16 · All sources accessed 2026-08-16.
**Primary basis: ABSENT-NUMERIC (expected per addendum — AD safety maps do not cover RAK).** No published numeric speed/no-wake limits for RAK waters were verifiable this run. Base schedule math therefore uses a **conservative planning basis** consistent with Abu Dhabi's codified tiers, explicitly labeled; **every corridor time in REVENUE-STACK-RAS-AL-KHAIMAH.md is conservative-basis flagged.**

## 1 · Who sets and enforces (verified)

- **RAKTA** is the designated competent body for licensing and operating maritime vessels emirate-wide under **Law No. (13) of 2023** and its **Executive Regulation (May 2026)**, which covers "maritime safety requirements, technical and environmental specifications, inspection and oversight procedures" and a penalties system. PRIMARY: https://www.rakta.gov.ae/news/mohammed-bin-saud-issues-the-executive-regulation-of-the-law-on-licensing-and-operating-marine-vessels-in-ras-al-khaimah/ ; law text index: https://www.rak.ae/wps/portal/rak/legislative-committee/legislation-search — the rak.ae legislation text includes an operator duty **"not to exceed speed limits in maritime routes"** (numeric values not published in the English text located this run).
- **RAK Ports** (harbor master) governs port waters under **Act No. (9) of 2008**: ships "shall sail in a **fair speed** inside the port and in accordance with weather conditions" (Art. 40); penalty schedule fines "Driving in a speed exceeding permitted limits" (AED 500); mandatory pilotage rules. PRIMARY PDF: https://rakports.ae/wp-content/uploads/2019/12/rak-ports-regulation-2008-1.pdf — no numeric knot limits in the Act.
- **Federal layer:** UAE Ministry of Energy & Infrastructure / Federal Transport Authority – Land & Maritime navigation and registration rules apply nationally; no RAK-specific numeric speed schedule located on federal portals this run.
- **NOT FOUND this run:** any RAK equivalent of Abu Dhabi's published safety maps or Dubai's DMCA numeric zone limits; any published no-wake-zone map for Al Hamra lagoon, Mina Al Arab lagoons or the RAK Creek. State this honestly; re-verify each run — the May 2026 Executive Regulation is new, and implementing circulars with numeric limits may follow.

## 2 · Conservative planning basis (ASSUMPTION — labeled, used in all schedule math)

Mirrors Abu Dhabi Maritime's codified General Speed Limit Rules (primary in abu-dhabi/SPEED-RULES-ABU-DHABI.md) as the nearest codified UAE tier set; applied conservatively to RAK geography:

| Segment type | Planning basis | Rationale |
|---|---|---|
| Within 50 m of shore, piers, marinas, any facility (incl. abra stations) | **5 kn** | AD Rule 1 analog; universal marina practice |
| RAK Creek (full length — shared with abras, moored dhows) | **8 kn** | narrow, heritage traffic; stricter than AD channel tier on purpose |
| Lagoon/channel approaches (Al Hamra lagoon, Mina Al Arab lagoons, Al Marjan breakwater approaches) | **12 kn** | AD mid-zone tier analog |
| Open coastal water | **25 kn N45 service speed (canon)** | vessel-capability bound; well inside AD's 50 kn open-water analog |
| Night (sunset–sunrise), all waters | **20 kn** | AD Rule 5 analog; matters for the 16-hr day — evening legs re-timed |
| Port limits (Saqr Port approaches, RAK Maritime City), if ever transited | harbor-master direction; "fair speed" | Act 9/2008, primary |

Every rendered schedule states: *times computed on a conservative planning basis; RAK publishes no numeric limits; final schedules set with RAKTA under the Executive Regulation.*

## 3 · What this means on our corridors (times in REVENUE-STACK §2)

- **Al Marjan ↔ Al Hamra Marina (≈4 nm):** breakwater/lagoon-heavy — roughly half the leg at 12 kn planning basis.
- **Mina Al Arab ↔ Corniche (≈10 nm)** and **Al Marjan ↔ Corniche (≈17 nm):** mostly open coastal water at 25 kn; 5 kn/12 kn collars at both ends; corniche stations sit at the creek mouth zone — 8 kn basis applies inside the creek line.
- **RAK Creek/Old Town ↔ Jazirat Al Hamra (≈13 nm):** in-creek segment at 8 kn both directions (the abra corridor), then open coast.

## 4 · What relief unlocks (framing only — never a schedule assumption)

The purpose behind no-wake and lagoon caution rules — wake damage to reclaimed-island revetments and moored craft, noise near resorts and the heritage creek, shallow-lagoon safety — is served *better* by a foiling vessel: near-zero wake at speed, near-silent electric drive, software-geofenced no-foil zones at every lagoon entrance and berth. If RAKTA's implementing rules ever grant purpose-based relief in lagoon segments, the Al Hamra and Mina Al Arab legs compress materially. **All base math uses the conservative planning basis; relief appears only as this labeled sensitivity.**

## 5 · Confidence register

| Item | Status |
|---|---|
| RAKTA as marine rule-maker/enforcer (Law 13/2023 + Exec Reg 2026) | PRIMARY |
| RAK Ports "fair speed" + speeding penalty inside port limits | PRIMARY (Act 9/2008 PDF) |
| Numeric emirate-wide limits (knots) | **NOT VERIFIED — none published/located; conservative planning basis used, flagged everywhere** |
| No-wake zone maps for lagoons/creek | NOT FOUND — assumed 5 kn/50 m collar + 8 kn creek, labeled |
| Night cap 20 kn | ASSUMPTION (AD analog), labeled |
