# R3 Sourced Real-World Networks (deepening)

Sourced from official operators / Wikipedia route diagrams, 2026-07-02.
Coordinates are **approximate seeds** for Grok to geocode + mint precisely.
Rule: broad-footprint-first, exact-bind-second, null-beats-wrong. Under-construction / proposed stations flagged and held null (not sealed) until real.

---

## manila-pasig-ferry  (current: 5 sealed / mesh 7  → real: 13 operational stations, linear Pasig+Marikina River line)
Source: Wikipedia "Pasig River Ferry Service" route diagram; MMDA. System length 28 km, 1 linear line (multi-stop water bus).
**Operational stations (upstream→downstream order):**
1. Pinagbuhatan (Pasig)  ~14.5586, 121.0997
2. Kalawaan (Pasig)  ~14.5620, 121.0870
3. San Joaquin (Pasig)  ~14.5636, 121.0790
4. Maybunga (Pasig)  ~14.5697, 121.0842
5. Guadalupe (Makati)  ~14.5668, 121.0470
6. Hulo (Mandaluyong)  ~14.5741, 121.0378
7. Valenzuela (Makati/Mandaluyong)  ~14.5820, 121.0300
8. Lambingan (Sta Ana, Manila)  ~14.5876, 121.0155
9. Santa Ana (Manila)  ~14.5906, 121.0110
10. PUP Manila (Sta Mesa)  ~14.5985, 121.0110
11. Quinta (Quiapo, Manila)  ~14.5966, 120.9878
12. Lawton / Liwasang Bonifacio (Manila)  ~14.5936, 120.9800
13. Escolta (Binondo, Manila)  ~14.5977, 120.9782
(Proposed / NOT in service — hold null: Plaza Mexico, Bridgetowne, Eastwood, Riverbanks.)
Corridors = 12 consecutive linear hops Pinagbuhatan↔…↔Escolta. Reuse existing 5 sealed endpoints by ID where names match (Escolta/Guadalupe/Lawton/PUP/Sta Ana likely already meshed as manila-pasig-* nodes — ID-match, no re-mint).

## kochi-water-metro  (current: 14 sealed + 4 pending / mesh 16  → real: 10 operational stations / 6 operational routes)
Source: Wikipedia "Kochi Water Metro" (stations-in-service table + routes). 38 terminals / 16 routes PLANNED; only 10 stations + 6 routes OPERATIONAL. Deepen to operational truth; hold planned under-construction null.
**Operational stations:**
1. High Court  ~9.9847, 76.2760  (hub)
2. Vypin  ~9.9700, 76.2560
3. Vyttila  ~9.9680, 76.3200  (hub)
4. Kakkanad  ~10.0130, 76.3410
5. South Chittoor  ~10.0430, 76.2870
6. Bolgatty  ~9.9990, 76.2720
7. Mulavukad North  ~10.0230, 76.2790
8. Eloor  ~10.0680, 76.2900
9. Cheranallur  ~10.0520, 76.2820
10. Fort Kochi  ~9.9650, 76.2420
11. Willingdon Island  ~9.9500, 76.2700
12. Mattancherry  ~9.9580, 76.2560
**Operational routes (seal each as corridor chain):**
- R1 Vypin ↔ High Court
- R2 Vyttila ↔ Kakkanad
- R3 High Court ↔ Bolgatty ↔ Mulavukad North ↔ South Chittoor
- R4 South Chittoor ↔ Eloor ↔ Cheranallur
- R5 High Court ↔ Fort Kochi
- R6 High Court ↔ Willingdon Island ↔ Mattancherry
The 4 currently-pending corridors most likely = R5/R6 legs (High Court↔Fort Kochi, HC↔Willingdon, Willingdon↔Mattancherry, + one R3/R4 leg). Seal these; confirm against bound route_ids.

## hamburg-hadag  (current: 15 sealed / mesh 16  → real: 21 landing bridges / 7 scheduled lines)
Source: Wikipedia "HADAG" scheduled harbour ferries table. 26.3 km, 8 lines (HBL suspended), 21 terminals.
**Landing bridges (pontoons):**
Landungsbrücken (Brücke 1/2/3 hub) ~53.5460,9.9700 · Altona/Fischmarkt ~53.5455,9.9430 · Dockland ~53.5460,9.9360 · Neumühlen/Övelgönne ~53.5460,9.9160 · Bubendey-Ufer ~53.5360,9.8900 · Finkenwerder ~53.5290,9.8760 · Rüschpark ~53.5340,9.8560 · Teufelsbrück ~53.5470,9.8710 · Airbus (Finkenwerder) ~53.5360,9.8380 · Elbphilharmonie ~53.5415,9.9840 · Arningstraße ~53.5390,9.9740 · Theater im Hafen ~53.5460,9.9690 · Norderelbstraße ~53.5310,9.9900 · Argentinienbrücke ~53.5230,9.9820 · Ernst-August-Schleuse (Wilhelmsburg) ~53.5080,9.9910 · Steinwerder ~53.5390,9.9600 · Waltershof ~53.5230,9.9200 · Neuhof ~53.5130,9.9600 · Blankenese ~53.5580,9.8100 · Neuenfelde/Este-Sperrwerk ~53.5230,9.7900 · Cranz ~53.5380,9.7780
**Lines (seal consecutive hops):**
- 61: Landungsbrücken – Altona/Fischmarkt – Dockland – Waltershof – Neuhof
- 62: Landungsbrücken – Altona/Fischmarkt – Dockland – Neumühlen/Övelgönne – Bubendey-Ufer – Finkenwerder
- 64: Finkenwerder – Rüschpark – Teufelsbrück
- 68: Teufelsbrück – Airbus
- 72: Landungsbrücken – Arningstraße – Elbphilharmonie
- 73: Landungsbrücken – Theater im Hafen – Norderelbstraße – Argentinienbrücke – Ernst-August-Schleuse
- 75: Landungsbrücken – Steinwerder
(HBL Blankenese–Neuenfelde–Cranz currently suspended — hold null.)

## helsinki-hsl  (current: 4 sealed  → real: HSL Suomenlinna ferry + island network)
Source: HSL, suomenlinna.fi, jt-line.fi, lonna.fi. HSL runs Market Square (Kauppatori) ↔ Suomenlinna Main Pier year-round; JT-Line/FRS run seasonal island routes.
**Piers:**
- Market Square / Kauppatori (mainland hub) ~60.1670,24.9550
- Suomenlinna Main Pier ~60.1455,24.9880
- Lonna ~60.1530,24.9760
- Vallisaari (Luotsipiha pier) ~60.1420,25.0120
- Suomenlinna King's Gate (Kuninkaanportti) ~60.1385,24.9910
- Vasikkasaari ~60.1600,25.0250
**Routes:** Kauppatori↔Suomenlinna Main (HSL, anchor, already sealed); Kauppatori↔Lonna; Kauppatori↔Vallisaari; Kauppatori↔Vasikkasaari; Suomenlinna Main↔King's Gate (internal). Additive only; validate seasonal ones.

---

## VALIDATED AT / NEAR REAL-WORLD SCALE (complete — no or minimal deepening)

## rio-ccr-barcas  (current: 4 sealed → real: 4 lines)  **COMPLETE**
Source: barcasrio.com.br, riomap360, Wikipedia Praça Quinze. All lines radiate from Praça XV: ↔Araribóia (Niterói), ↔Cocotá (Ilha do Governador), ↔Paquetá, ↔Charitas. 4 sealed = 4 real lines. No deepening. (Angra dos Reis / Ilha Grande are separate Costa Verde operation, out of Guanabara Bay scope.)

## toronto-island-ferry  (current: 3 sealed → real: 3 destinations)  **COMPLETE**
Jack Layton Terminal ↔ Ward's Island / Centre Island / Hanlan's Point. 3 sealed = real network. No deepening.

## mersey-ferries  (current: 3 sealed → real: 3 landing stages)  **COMPLETE**
Pier Head ↔ Seacombe / Woodside (Mersey Ferries commuter + River Explorer triangle). 3 sealed = real network. No deepening.

## hcmc-saigon-waterbus  (current: 4 sealed / mesh 4 → real: Line 1, 5-6 stops)  **NEAR-COMPLETE**
Source: saigonwaterbus.com, Vietnam Coracle. Line 1 (south→north): Bach Dang, [Saigon Pearl], Binh An, Thanh Da, Hiep Binh Chanh, Linh Dong. 4 sealed corridors = 5-stop linear line. OPTIONAL additive: Saigon Pearl intermediate + Thu Thiem (new). Hold Line 2 (planned) null. Effectively complete.

## brisbane-citycat  (current: 20 sealed / mesh 23 → real: ~22-25 terminals)  **NEAR-COMPLETE**
Source: Brisbane City Council ("network of 22 terminals"), Hamilton Today ("25 terminals"). F1 CityCat Northshore Hamilton↔UQ St Lucia + CityHopper cross-river. Mesh 23 ≈ real. OPTIONAL additive named terminals if absent: Milton, Mowbray Park, Bulimba, Hawthorne. Effectively at-scale.

