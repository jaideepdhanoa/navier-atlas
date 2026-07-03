# GROK-SPEC — R3 Greenfield/Anchor Real-World Deepening (seed-and-seal)

**Author:** Tasklet · **Date:** 2026-07-02 · **Lane:** Grok geometry (mint BPs + seal corridors + hand-waypoints)
**Rule:** ID-based match only · null-beats-wrong · broad-footprint-first, exact-bind-second · additive only · under-construction/planned/suspended stops held **null** (never sealed until real). Seal every corridor at **0 km land** — use explicit hand waypoints (no land crossings). Re-run land-crossing QA each pass; hold the program-wide 0-crossing record.

**Tasklet-side binding:** after Grok mints/seals, Tasklet binds each partner JSON's `journeys_unlocked` from the mint receipt (both trees; data-clean `ensure_ascii=True`, partner-pitch `ensure_ascii=False`). Do NOT seal aspirational stations that remain under construction.

Source dossier: `dossiers/R3/SOURCED-NETWORKS.md` (official operators / Wikipedia route diagrams).

---

## 1. manila-pasig-ferry — deepen 5 → 13 operational stations (linear Pasig+Marikina line)
Node convention: existing `bp-<hash>`. **Reuse existing manila-pasig nodes by geo-match** (Escolta, Guadalupe, Lawton, PUP, Sta Ana likely already minted); mint net-new as `bp-*`. Seed IDs below are Tasklet labels for mapping only.

| # | Station (city) | approx lat,lon | status |
|---|---|---|---|
| 1 | Pinagbuhatan (Pasig) | 14.5586, 121.0997 | mint |
| 2 | Kalawaan (Pasig) | 14.5620, 121.0870 | mint |
| 3 | San Joaquin (Pasig) | 14.5636, 121.0790 | mint |
| 4 | Maybunga (Pasig) | 14.5697, 121.0842 | mint |
| 5 | Guadalupe (Makati) | 14.5668, 121.0470 | reuse if present |
| 6 | Hulo (Mandaluyong) | 14.5741, 121.0378 | reuse/mint |
| 7 | Valenzuela (Makati) | 14.5820, 121.0300 | mint |
| 8 | Lambingan (Sta Ana) | 14.5876, 121.0155 | mint |
| 9 | Santa Ana (Manila) | 14.5906, 121.0110 | reuse if present |
| 10 | PUP Manila (Sta Mesa) | 14.5985, 121.0110 | reuse if present |
| 11 | Quinta (Quiapo) | 14.5966, 120.9878 | mint |
| 12 | Lawton (Manila) | 14.5936, 120.9800 | reuse if present |
| 13 | Escolta (Binondo) | 14.5977, 120.9782 | reuse if present |

**Corridors (12 consecutive linear hops):** 1↔2↔3↔4↔5↔6↔7↔8↔9↔10↔11↔12↔13. Follow the Pasig River thalweg; hand-waypoint each hop so the polyline stays in-channel (river bends near Guadalupe, Sta Ana loop, Sta Mesa). **Hold null:** Plaza Mexico, Bridgetowne, Eastwood, Riverbanks (proposed/not-in-service).

## 2. kochi-water-metro — seal operational 10-station / 6-route network
Node convention: readable `kch-*` (already in file). 4 featured journeys currently `aspirational-no-built-route` (rid null) — seal these + complete the operational route set. **Hold planned stations null** (38 planned; only 10-12 operational).

| kch-id | Station | approx lat,lon |
|---|---|---|
| kch-high-court | High Court (hub) | 9.9847, 76.2760 |
| kch-vypin | Vypin | 9.9700, 76.2560 |
| kch-vyttila | Vyttila (hub) | 9.9680, 76.3200 |
| kch-kakkanad | Kakkanad | 10.0130, 76.3410 |
| kch-south-chittoor | South Chittoor | 10.0430, 76.2870 |
| kch-bolgatty | Bolgatty | 9.9990, 76.2720 |
| kch-mulavukad-north | Mulavukad North | 10.0230, 76.2790 |
| kch-eloor | Eloor | 10.0680, 76.2900 |
| kch-cheranallur | Cheranallur | 10.0520, 76.2820 |
| kch-fort-kochi | Fort Kochi | 9.9650, 76.2420 |
| kch-willingdon-island | Willingdon Island | 9.9500, 76.2700 |
| kch-mattancherry | Mattancherry | 9.9580, 76.2560 |

**Operational routes (seal each corridor/chain):**
- R1 kch-vypin ↔ kch-high-court
- R2 kch-vyttila ↔ kch-kakkanad
- R3 kch-high-court ↔ kch-bolgatty ↔ kch-mulavukad-north ↔ kch-south-chittoor
- R4 kch-south-chittoor ↔ kch-eloor ↔ kch-cheranallur
- R5 kch-high-court ↔ kch-fort-kochi
- R6 kch-high-court ↔ kch-willingdon-island ↔ kch-mattancherry

Backwater/harbour geometry — hand-waypoint around Willingdon Island, Bolgatty Island, and the Ernakulam channel so no leg crosses land.

## 3. hamburg-hadag — deepen 15 → 21 landing bridges / 7 scheduled lines
Node convention: readable `ham-*` (already in file). Mint missing pontoons; seal each scheduled line as consecutive hops. **Hold null:** HBL Blankenese–Neuenfelde–Cranz (suspended).

**Pontoons:** ham-landungsbrucken (hub) 53.5460,9.9700 · ham-altona 53.5455,9.9430 · ham-dockland 53.5460,9.9360 · ham-neumuhlen 53.5460,9.9160 · ham-bubendey-ufer 53.5360,9.8900 · ham-finkenwerder 53.5290,9.8760 · ham-ruschpark 53.5340,9.8560 · ham-teufelsbruck 53.5470,9.8710 · ham-airbus 53.5360,9.8380 · ham-elbphilharmonie 53.5415,9.9840 · ham-arningstrasse 53.5390,9.9740 · ham-theater-im-hafen 53.5460,9.9690 · ham-norderelbstrasse 53.5310,9.9900 · ham-argentinienbrucke 53.5230,9.9820 · ham-ernst-august-schleuse 53.5080,9.9910 · ham-steinwerder 53.5390,9.9600 · ham-waltershof 53.5230,9.9200 · ham-neuhof 53.5130,9.9600

**Lines (seal consecutive hops):**
- 61: landungsbrucken – altona – dockland – waltershof – neuhof
- 62: landungsbrucken – altona – dockland – neumuhlen – bubendey-ufer – finkenwerder
- 64: finkenwerder – ruschpark – teufelsbruck
- 68: teufelsbruck – airbus
- 72: landungsbrucken – arningstrasse – elbphilharmonie
- 73: landungsbrucken – theater-im-hafen – norderelbstrasse – argentinienbrucke – ernst-august-schleuse
- 75: landungsbrucken – steinwerder

Elbe harbour geometry — hand-waypoint around Steinwerder/Waltershof port basins and the Köhlbrand so no leg cuts across quays.

## 4. helsinki-hsl — deepen 4 → island network (additive only)
Node convention: mixed (`bp-<hash>` anchor + readable `bp-vallisaari` etc.). Anchor Market Square = `bp-fe03528b18`. Vallisaari already sealed. **Additive** piers/routes; validate seasonal JT-Line legs before sealing; hold unverified null.

| id | Pier | approx lat,lon | status |
|---|---|---|---|
| bp-fe03528b18 | Market Square / Kauppatori (hub) | 60.1670, 24.9550 | existing |
| (existing) | Suomenlinna Main Pier | 60.1455, 24.9880 | existing (anchor sealed) |
| bp-vallisaari | Vallisaari (Luotsipiha) | 60.1420, 25.0120 | existing sealed |
| bp-lonna | Lonna | 60.1530, 24.9760 | mint |
| bp-vasikkasaari | Vasikkasaari | 60.1600, 25.0250 | mint |
| bp-suomenlinna-kingsgate | Suomenlinna King's Gate | 60.1385, 24.9910 | mint |

**Additive routes:** Kauppatori↔Lonna; Kauppatori↔Vasikkasaari; Suomenlinna Main↔King's Gate (internal). Gulf of Finland open-water — straightforward, but hand-waypoint around Suomenlinna/Vallisaari shoals.

---

## 5. VALIDATED COMPLETE / NEAR-COMPLETE — no Grok deepening required
- **rio-ccr-barcas** — 4 sealed = 4 real Guanabara Bay lines (Araribóia/Cocotá/Paquetá/Charitas). COMPLETE.
- **toronto-island-ferry** — 3 sealed = Ward's/Centre/Hanlan's. COMPLETE.
- **mersey-ferries** — 3 sealed = Pier Head/Seacombe/Woodside. COMPLETE.
- **hcmc-saigon-waterbus** — 4 sealed = Line 1 (Bach Dang↔Linh Dong, 5 stops). NEAR-COMPLETE. *Optional additive:* Saigon Pearl intermediate + Thu Thiem. Hold Line 2 null.
- **brisbane-citycat** — mesh 23 ≈ 22-25 real terminals. NEAR-COMPLETE. *Optional additive if absent:* Milton, Mowbray Park, Bulimba, Hawthorne.

## Definition of done (R3)
- Manila 12 linear corridors sealed at 0 km land; Kochi 6 operational routes sealed; Hamburg 7 lines sealed; Helsinki additive island routes sealed/validated.
- All under-construction/planned/suspended stations held null.
- Land-crossing QA re-run → 0 crossings maintained.
- Grok emits mint receipt → Tasklet binds partner JSONs.
