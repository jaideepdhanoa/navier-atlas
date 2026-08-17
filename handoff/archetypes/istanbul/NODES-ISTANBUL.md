# NODES-ISTANBUL — network design
Internal research record. Anti-spaghetti discipline: Istanbul has 50+ public piers; we pick 12 nodes and 4 lines, each with one nameable purpose. We do NOT mirror Şehir Hatları. All geometry here is NEW AUTHORED, coordinate-derived — no invented route IDs; Atlas cluster `istanbul-turkey` exists for later inheritance (corridor-inheritance skill applies at bind time, not here).

## 1 · Node inventory (12 active + 3 roadmap)
Coordinates: pier/marina locations read from map imagery of known public facilities — DERIVED; verify against Şehir Hatları iskeleler page / marina operators at bind time. Status: all ACTIVE nodes are existing, operating piers/marinas (Şehir Hatları pier list, İDO terminals, licensed marinas) — no "planned" facilities used.

| # | Node | Lat, Lon | What it is | Serves |
|---|---|---|---|---|
| 1 | Bakırköy | 40.9738, 28.8710 | Public pier (İDO/city services legacy) | IST-1 west anchor |
| 2 | Ataköy Marina | 40.9700, 28.8770 | Licensed marina | IST-1 west alt/charter base |
| 3 | Yenikapı | 41.0005, 28.9530 | Ferry terminal + Marmaray/M1/M2 superhub | IST-1 rail interchange |
| 4 | Karaköy / Galataport | 41.0242, 28.9838 | Public pier + cruise port | IST-3, cruise/L3 |
| 5 | Kabataş | 41.0311, 28.9932 | Major pier; tram/funicular interchange | IST-2 alt origin, IST-4 |
| 6 | Eminönü | 41.0175, 28.9722 | Historic pier cluster | IST-3 alt, L3 |
| 7 | Üsküdar | 41.0262, 29.0158 | Major Asian pier + Marmaray | reserve (no line seed — avoid duplicating vapur) |
| 8 | Kadıköy | 40.9930, 29.0233 | Biggest Asian interchange (M4, Marmaray at Ayrılık Çeşmesi, ferries) | **Interchange A** — IST-1×IST-2×IST-3 |
| 9 | Bostancı | 40.9525, 29.0937 | Pier + legacy seabus terminal | IST-1 east anchor, IST-2 feeder |
| 10 | Kalamış / Fenerbahçe Marina | 40.9765, 29.0369 | Largest Asian marina (4-kn entry corridor) | charter/L3 base only — NOT a line stop |
| 11 | Büyükada | 40.8767, 29.1289 | Islands main pier | IST-2 |
| 12 | Heybeliada | 40.8778, 29.0999 | Second island pier | IST-2 tail |
| R1 | İstinye | 41.1105, 29.0577 | Mid-Bosphorus cove pier | roadmap (IST-4) — berth to verify |
| R2 | Anadolu Kavağı | 41.1743, 29.0855 | Upper-Bosphorus village pier | roadmap (IST-4) |
| R3 | Maltepe/Kartal | ~40.9198, 29.1256 | E Asian-shore piers | roadmap IST-1 extension — pier condition to verify |

MECE check: 12 active stops → ceiling ceil(12/2)=6 lines; we use **4**. Interchanges: **Kadıköy** (A) and **Kabataş** (B) only.

## 2 · Line design (keyed to SPEED-RULES)
Time model: legal speed per segment — **25 kn service on open Marmara** (south of İnci Burnu–Ahırkapı line, no blanket cap), **10 kn SOG inside Bosphorus limits**, 4-kn zones respected, **+2 min slow-approach allowance per harbor call (DERIVED), +3 min dwell per intermediate stop**. Distances: great-circle × 1.12 coastal routing factor (DERIVED from coordinates above). Current allowance: over-ground cap makes strait legs current-neutral; ±1 kn on Islands legs noted.

### IST-1 · Marmara Trunk Express — "the fast south shore"
**Bakırköy → Yenikapı → Kadıköy → Bostancı** (open Marmara the whole way; the Yenikapı→Kadıköy leg routes south of the Ahırkapı–İnciburnu line)
- Legs: Bakırköy–Yenikapı 4.5 nm / 11 min · Yenikapı–Kadıköy 3.6 nm / 9 min · Kadıköy–Bostancı 4.5 nm / 11 min (all @25 kn)
- End-to-end **Bakırköy→Bostancı ≈ 45 min** incl. 2 dwells + approaches; **Yenikapı→Kadıköy ≈ 13 min** pier-to-pier.
- vs today: no direct fast water service on this axis; road/rail alternatives: Bakırköy→Kadıköy driving 70–110 min peak (INDICATIVE); Marmaray Yenikapı→Ayrılıkçeşmesi ~12 min + access (SECONDARY schedule — honest note: Marmaray wins Yenikapı↔Kadıköy; the water product wins Bakırköy/Ataköy↔Kadıköy/Bostancı and seat comfort).
- Purpose: THE trunk where 25 kn is legal and the foiler beats road decisively west↔east along the Marmara shore. Roadmap extension: Maltepe/Kartal (R3).

### IST-2 · Islands Express — "Adalar in a third of the time"
**Kadıköy → Büyükada → Heybeliada** (+ Bostancı→Büyükada short shuttle at peak)
- Legs: Kadıköy–Büyükada 9.5 nm / 23 min · Büyükada–Heybeliada 1.5 nm / 4 min · (Bostancı–Büyükada 5.4 nm / 13 min)
- **Kadıköy→Büyükada ≈ 26 min** vs existing services ~50–100 min (INDICATIVE — verify current ŞH/Turyol schedules). Categorical win, year-round.
- Kabataş origin variant: 12.5 nm total, first ~1.3 nm inside strait limits @10 kn → ≈ 37–40 min — still a big win vs ~90 min (INDICATIVE); keep as peak-season variant, Kadıköy is the base origin.
- Purpose: the flagship time-win line; residents (car-free islands, water-only access) + weekenders + tourists; strong counter-seasonal mix with IST-1 commuters.

### IST-3 · Cross-strait Premium Shuttle — CONSTRAINED, comfort tier only
**Karaköy/Galataport ↔ Kadıköy** (2.9 nm, entirely inside Bosphorus limits → 10 kn cap → ~17 min + dwell; hull-borne, no foiling)
- Honest read: **no time win** vs vapur (~20 min) or Marmaray. Case = comfort/quiet/zero-emission + cruise-passenger and hotel-linked premium hops + guaranteed seat. Keep SHORT, off-peak weighted, priced as premium comfort. Mark **CONSTRAINED** everywhere; do not build economics on speed here.

### IST-4 · Upper-Bosphorus Leisure — ROADMAP
**Kabataş → İstinye → Anadolu Kavağı** (10.7 nm all inside strait @10 kn ≈ 64 min sailing)
- Leisure/experience only (yalı shoreline, Kavağı lunch run, sunset returns); zero-emission + low-wake + ≤85 dB is the licence-to-operate story on this shoreline. No commuter claims. Activate with charter/L3 demand; İstinye berth to verify.

### Explicit exclusions
- **Golden Horn (Haliç):** excluded from service design — 10-kn cap, bridge-crossing bans, documented wake damage to moored craft (harbor-master letter 02.12.2024), shallow, sensitive. Charter transits at displacement speed only.
- **Üsküdar/Beşiktaş/Eminönü vapur triangle:** deliberately NOT overlaid — the vapur serves it superbly at $1.2; a 10-kn premium duplicate has no honest purpose beyond IST-3's single corridor.

## 3 · Honest comparison table (render-safe once verified)
| OD | Navier | Existing water | Road (peak, INDICATIVE) |
|---|---|---|---|
| Bakırköy→Kadıköy | ~29 min (1 stop) | none direct (verify) | 70–110 min |
| Yenikapı→Kadıköy | ~13 min | none direct | Marmaray ~12 min + access |
| Kadıköy→Büyükada | ~26 min | ~50–100 min (verify) | n/a (no road) |
| Bostancı→Büyükada | ~15 min | ~30–45 min motor (verify) | n/a |
| Karaköy→Kadıköy | ~19 min (10-kn cap) | vapur ~20 min | 45–80 min |

## 4 · Geometry & Atlas notes
- All lat/lon and nm figures are DERIVED (coordinates × haversine × 1.12); no sealed route_ids exist for these lines; partner JSON `_ref-partner-sehir-hatlari.json` journeys are aspirational chips with null route_ids — consistent, nothing to inherit yet.
- Cluster `istanbul-turkey` exists in Atlas (per partner JSON `_public_transit_authority.home_cities`) — later geometry sealing binds there; mis-geocode risk not assessed this pass.
- Fail closed: İstinye/Maltepe/Kartal berth suitability UNVERIFIED → roadmap flags; Bakırköy pier operational status for new services to verify.
