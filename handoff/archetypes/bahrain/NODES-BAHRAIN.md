# NODES-BAHRAIN — network design file (internal audit file — does not render)

Researched 2026-08-16. Geometry rule (addendum): **fail closed** — every rendered stop must be a research-verified real landing. Coordinates: OSM/Nominatim or operator map evidence where available (tagged); map-read approximations tagged DERIVED ±. Distances are **straight-line great-circle nm computed from the coordinates below (DERIVED)**; routed distances on constrained legs run ~15–25% longer (noted per line). Times at **25 kn service speed + 3 min dwell per intermediate stop**.

## 1 · Node inventory (14 verified landings)

| # | Node | Coordinates (lat, lon) | Verification | Status |
|---|---|---|---|---|
| N1 | **Water Garden City station** | 26.2450, 50.5560 (DERIVED map-read ±300m) | Live Masar water-taxi station (masargroup.bh — PRIMARY) | LIVE station |
| N2 | **Reef Island Marina** | 26.2425, 50.5695 (OSM island + marina east side, DERIVED ±200m) | Reef Island marina (ART Marine-managed, ~80 berths — SECONDARY) | Existing marina |
| N3 | **Bahrain Financial Harbour / Harbour House** | 26.2394, 50.5724 (OSM node) | Live Masar station "Harbour House"; Bahrain Harbour marinas 450 berths (bahrainharbour.com PRIMARY-developer; GFH Harbour Row marina press PRIMARY-corporate) | LIVE station · **HUB** |
| N4 | **The Avenues (Manama corniche)** | 26.2450, 50.5848 (OSM mall) | Live Masar station (masargroup.bh — PRIMARY) | LIVE station |
| N5 | **Four Seasons Bahrain Bay jetty** | 26.2446, 50.5877 (DERIVED map-read ±300m; OSM ambiguous) | Live Masar station (masargroup.bh — PRIMARY); FS runs own marine experiences (PRIMARY-operator) | LIVE station |
| N6 | **Manama East Coast Corniche station** | 26.2270, 50.5975 (DERIVED map-read ±400m) | Live Masar station "Manama East Coast" (masargroup.bh — PRIMARY) | LIVE station |
| N7 | **Sa'ada Marina (Muharraq)** | 26.2477, 50.6052 (Navily port page static-map coords — SECONDARY-map) | Live Masar station + Qatar-ferry international berth (masargroup.bh PRIMARY; ferry SECONDARY×3) | LIVE station · international gateway |
| N8 | **Galali Marina** | 26.2760, 50.6540 (DERIVED from OSM suburb + shoreline ±400m) | Existing harbour/marina; spine label "Galali Marina" (bp-3a280297b3) | Existing marina |
| N9 | **Amwaj Marina** | 26.2920, 50.6578 (OSM leisure=marina) | Operating marina, ~145 berths (amwajmarinabh.com — PRIMARY-operator) | Existing marina |
| N10 | **Marassi Beach Jetty (Diyar Al Muharraq)** | 26.3100, 50.6070 (DERIVED map-read ±500m) | Marassi Beach Jetty listed as existing attraction (findbahrain/mindtrip — SECONDARY); Marassi beachfront + hotels open (PRIMARY-developer) | Existing jetty — verify commercial-use terms |
| N11 | **Bahrain Yacht Club (Sitra)** | 26.1155, 50.6220 (DERIVED map-read ±500m) | Established club marina, Al Dar shuttle departs adjacent Sitra fisherman's port (aldarislands.com PRIMARY; spine bp-8d366c2583) | Existing marina |
| N12 | **Al Dar Island jetty** | 26.1305, 50.6573 (OSM islet) | Operating day-resort with continuous passenger shuttle (aldarislands.com — PRIMARY) | Existing jetty |
| N13 | **Durrat Marina / Durrat Al Bahrain Pavilion** | 25.8950, 50.6120 (DERIVED map-read ±800m — marina at Durrat's NE link; OSM only gives Durrat entrance 25.8454,50.5857) | Hawar Resort boats depart "Durrat Al Bahrain Pavilion" at Durrat Marina (hawarresort.com + all.accor.com — PRIMARY; Tripadvisor guest "welcome pavilion at Durrat Marina" — SECONDARY) | Existing pavilion berth · **HUB (south)** |
| N14 | **Hawar Resort jetty (Hawar Island NW)** | 25.6960, 50.7660 (DERIVED map-read ±800m; OSM island centroid 25.6530,50.7527) | Resort open, exclusive boat access 25–30 min from Durrat (PRIMARY-operator) | Existing resort jetty |

**Flagged, NOT in the network (fail closed):**
- **Jarada sandbank** — seasonal tidal sandbank, **no fixed landing**; anchorage-only experience product (L3 charter destination, never a scheduled stop). bahrain.com Jarada page — PRIMARY.
- **Marina West (Budaiya)** — project stalled/auctioned (Sumou acquisition reports, SECONDARY); spine labels exist (bp-db3eeed751/bp-f14a602ce1) but **no operating landing** — excluded.
- **Sofitel Zallaq beach jetty** — spine label exists (bp-a78871f1dd); hotel operates beach water-sports but a scheduled-service-grade jetty is **unverified** — roadmap only (BH-5).
- **Bilaj Al Jazayer** — under construction; **no public marine landing yet** (developer PRIMARY) — roadmap only (BH-5).
- **Ad Dur (Sitra) "Hawar Ferry Terminal"** — historical Hawar day-trip departure point; real Ad Dur is at ~25.968, 50.607, i.e., **8.9 nm from BYC — the spine's 1.2 nm "Sitra (Ad-Dur)↔BYC" corridor (rn-063a88bc18d1) is a mis-located BP** (probably the Sitra fisherman's port beside BYC). Cited by label only; mis-geocode recorded in §4.
- Mina Salman Customs Pier, Khalifa Bin Salman Port — port/security facilities, constraint zones not passenger nodes.

## 2 · Line architecture

Clusters: **North/Manama–Muharraq cluster** = N1–N10 (10 stops) → MECE cap ceil(10/2)=5 lines, we use 2. **South cluster** = N11–N14 (+2 shared north stops) → cap ceil(4/2)=2 lines, we use 2. Total **4 lines** (+1 roadmap). Interchanges (max 2): **N3 BFH (primary hub)**, **N13 Durrat Pavilion (south hub)**.

### BH-1 · North Corniche commuter spine — "the live water-taxi corridor, foiling-upgraded"
Purpose: the six live Masar stations + Reef Island, as one high-frequency spine. This is the Phase-1 story: same stops people already ride, faster and cleaner.
| Leg | nm (DERIVED, straight-line) |
|---|---|
| N1 WGC → N2 Reef Island | 0.7 |
| N2 → N3 BFH/Harbour House | 0.2 |
| N3 → N4 The Avenues | 0.7 |
| N4 → N5 Four Seasons | 0.2 |
| N5 → N6 East Coast Corniche | 1.2 |
| N6 → N7 Sa'ada Marina | 1.3 |
**Total 4.4 nm · end-to-end ≈ 26 min** (25 kn + 5×3 min dwell; realistically ~30 min at harbor speeds — much of BH-1 is inner-channel, see SPEED-RULES DERIVED zones. The N30 is the natural BH-1 hull; N45 at peak.)
Spine bindings: no clean corridor_id match for individual BH-1 legs (spine has no station-to-station corridors among these exact labels) — **all legs unbound**. Nearest-label references (context only, not bindings): rn-a5e9b5650887 "Manama↔The Marina" 3.2 nm; rn-b03a4fe50da0 "Bahrain sailing club Muharraq↔Marina Beach Garden Park" 1.0 nm.

### BH-2 · Amwaj–BFH commuter express — "island residents to the financial core"
Purpose: Amwaj/Diyar premium residential → CBD commute; kills the causeway loop around Muharraq.
| Leg | nm (DERIVED) |
|---|---|
| N9 Amwaj Marina → N8 Galali | 1.0 |
| N8 → N10 Marassi (Diyar) | 3.3 * |
| N10 → N7 Sa'ada Marina | 3.7 |
| N7 → N3 BFH | 1.8 |
**Total 9.8 nm · end-to-end ≈ 33 min** (*Galali→Marassi straight line clips Diyar reclamation; routed ≈ +25% on that leg; realistic end-to-end ~38 min. Peak pattern may skip N10 for a 28-min Amwaj→BFH run.)
Spine bindings: **N9→N8 = rn-9b7189cdb48f "Galali Marina↔Amwaj Marina" 1.4 nm (CLEAN, label match; spine nm ≈ ours + harbor approach)**. End-to-end overlay ≈ rn-c527f3063ee2 "Manama↔Amwaj Marina" 5.8 nm — label-level city-node match only, **approximate, not clean** (spine "Manama" is a city centroid, not BFH). Other legs **unbound** (no Marassi/Sa'ada station corridors in spine; rn-1e00882e3050 "Diyar Al Muharraq Marina↔Raya Port" is east-Diyar, different geometry).

### BH-3 · South leisure line — "Al Dar / Durrat coastal run"
Purpose: weekend/leisure spine from the CBD to the island day-resorts and Durrat; feeds BH-4 at N13.
| Leg | nm (DERIVED) |
|---|---|
| N3 BFH → N6 East Coast | 1.5 |
| N6 → N11 Bahrain Yacht Club (Sitra) | 6.8 |
| N11 → N12 Al Dar Island | 2.1 |
| N12 → N13 Durrat Pavilion | 14.3 |
**Total 24.8 nm · end-to-end ≈ 69 min** (routed +15–20% on the East Coast→BYC leg to clear Mina Salman/KBSP fairways and on Al Dar→Durrat around Sitra shoals → realistic ~80 min. N45 hull; ≤70 nm range gate ✓.)
Spine bindings: rn-063a88bc18d1 "Sitra (Ad-Dur) Hawar Ferry Terminal↔Bahrain Yacht Club" 1.2 nm plausibly matches an N11-adjacent leg **but its Ad-Dur BP is mis-located (see §4) — bind by label only, geometry contaminated → unbound**. rn-3762d8227b6d "Manama↔Durrat Marina" 23.8 nm ≈ BH-3 end-to-end overlay (city-node label match, **approximate**). rn-b8d4040616b9 "Durrat Marina↔Danat Al Bahrain Yacht Club" 1.6 nm — future Durrat local extension, unused. Others **unbound**.

### BH-4 · Hawar express — "the resort island shuttle, upgraded"
Purpose: scheduled premium shuttle on the exact corridor Hawar Resort already operates daily (25–30 min conventional boat → similar time foiling but in comfort/all-weather, and frequency).
| Leg | nm (DERIVED) |
|---|---|
| N13 Durrat Pavilion → N14 Hawar Resort jetty | 14.6 |
**Total 14.6 nm · end-to-end ≈ 35 min** (open water; protected-area low-wake approach at Hawar — see SPEED-RULES).
Spine binding: **rn-fb0e040b36a7 "Hawar Resort Hotel Jetty↔Durrat Marina" 15.0 nm (CLEAN — label match, nm within 3%)**. Also available for experiences variant: rn-c11ae32bc468 "Dukhan Water Sports Club↔Hawar Resort Hotel Jetty" 15.0 nm — **not used** (Dukhan landing unverified).

### BH-5 · West coast (ROADMAP ONLY — not in the network count)
Zallaq/Sofitel ↔ Bilaj Al Jazayer ↔ Durrat Pavilion (~11.7 nm Sofitel→Durrat). Blocked on: Sofitel jetty verification, Bilaj marine landing delivery. Spine references: rn-d8dacfc6690a (Sofitel↔Lost Paradise 3.9), rn-86c2791a51fa, rn-0afa66a6cc4d. Render only as amber-dashed roadmap if at all.

**Cross-border (Bahrain↔Khobar/Dammam, Bahrain↔Qatar): roadmap only — belongs to the Eastern Province market (next in sequence) and the existing Qatar-ferry corridor. NOT part of the Bahrain domestic line network.** Spine refs for later: e__ep-khobar__manama-bahrain 18.9 nm, rn-fffd9a53d482 21.2 nm, rn-7a9fad645ce9 98.3 nm (Quanta-LR gate).

## 3 · Architecture summary
- 14 nodes · 4 lines (BH-1 commuter spine, BH-2 commuter express, BH-3 leisure, BH-4 resort express) + 1 roadmap line.
- Hubs: **BFH (N3)** — BH-1/BH-2/BH-3 interchange; **Durrat Pavilion (N13)** — BH-3/BH-4 interchange. Sa'ada (N7) is a shared stop (international ferry gateway) but not designated a hub (keeps to the ≤2-hub rule).
- MECE check: north cluster 2 lines ≤ 5 cap ✓; south cluster 2 lines ≤ 2 cap ✓; every line has a nameable purpose ✓; no stop is orphaned ✓.
- Vessel gates: all legs ≤ 15 nm ✓ N45/N30 commercial-now; nothing needs Quanta-LR inside the domestic network.

## 4 · Spine data-quality findings (for the research record / Grok locale cleanup — do NOT re-tag Atlas data in the microsite pass)
1. ~20 corridors tagged `market_key: bahrain_domestic` are **KSA locales** (Dammam/Khobar: rn-bd8cc65459cc, rn-8cc0ea41cfdc, rn-1da21c1c8aba, rn-d83121b43cf9, rn-8c9f2859d63e, rn-bee07be06790, rn-1ddf88b01cf6, rn-568a199e0ee6, rn-e7ac989398bd, rn-bb7bd3a7070b …) or **Qatar locales** (Al Khor/Lusail/Doha: rn-66cd5e64c95a, rn-2109f5f48e20, rn-d4b70c269a15, rn-10d219cf88e2, rn-1a241eccd7cf, rn-f5c5ab0fc34f, rn-dc6ee762bf43, rn-74dba06b9ea1, rn-f4e10e8c7382, rn-c11ae32bc468 partially).
2. rn-063a88bc18d1 "Sitra (Ad-Dur) Hawar Ferry Terminal" BP is mis-located: true Ad Dur is 8.9 nm from BYC, spine says 1.2 nm.
3. "Manama" city-centroid corridors (manama-bahrain node) are rollups, not station geometry — usable as overlays only.
4. Ref-partner JSON journey distances are known-bad (three journeys share distance_nm 29.3 with a Dammam label) — never reuse.
