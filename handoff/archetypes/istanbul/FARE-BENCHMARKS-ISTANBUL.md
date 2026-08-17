# FARE-BENCHMARKS-ISTANBUL
Internal research record — audit language, never renders. Date: 2026-08-16. **FX: 47.76 TRY/USD (TCMB, 2026-08-16).** All TRY figures from the 16 Feb 2026 İstanbul tariff update unless noted; TRY fares are repriced several times a year — re-verify before render.

## 1 · Public network (İstanbulkart) — the floor
| Product | TRY | USD | Source/confidence |
|---|---|---|---|
| İstanbulkart base transit fare (16 Feb 2026) | 42.00 | $0.88 | SECONDARY (press reporting UKOME tariff decision); PRIMARY check: istanbulkart.istanbul |
| Şehir Hatları vapur, cross-Bosphorus full fare | 53.20–65.21 (Üsküdar–Eminönü 58.52; Kadıköy–Eminönü/Beşiktaş 65.21) | $1.11–1.37 | SECONDARY (2026 tariff reporting, birgun.net et al.); PRIMARY check: sehirhatlari.istanbul ücretler page |
| Adalar (Islands) line, full | 114.57 (Adakart 68.71) | $2.40 | SECONDARY (tariff reporting) |
| Bostancı–Adalar | 171.89 | $3.60 | SECONDARY |
| Kabataş–Adalar (private motor tariff) | 206.20 | $4.32 | SECONDARY |
- Reading: the public floor is ~$1–1.4 cross-strait and ~$2.4–4.3 to the Islands. Heavily subsidized, İstanbulkart-integrated, massive coverage. A premium tier does not compete with this — it sells time (Marmara/Islands) and comfort.

## 2 · İBB Deniz Taksi (sea taxi) — the on-demand premium anchor İBB itself set
2026 tariff: **500 TL opening incl. first mile; then 310 TL/mile (band 1), 250 TL/mile (band 2), 200 TL/mile (band 3+)** per vessel (small craft). [SECONDARY — 2026 tariff tracker (eleman.net) reporting İBB/UKOME tariff; VERIFY at deniztaksi.istanbul before render]
- Worked anchors (DERIVED): Karaköy→Kadıköy (~2.9 nm): ≈ 500 + 1.9×310 ≈ **1,089 TL ≈ $23/vessel-trip**; Kabataş→Büyükada (~12.5 nm): ≈ 500 + 11.5×~230 ≈ **3,145 TL ≈ $66/vessel-trip**. At 6–8 pax ≈ $3–11/seat. **This is İBB's own proof that premium water pricing exists in Istanbul.**

## 3 · Road premium substitutes
- **Yellow taxi tariff (16 Feb 2026, İTEO/UKOME):** opening 65.40 TL; **43.56 TL/km**; minimum fare (indi-bindi) 210 TL. [SECONDARY — tariff reporting; earlier Sept-2025 tariff was 54.5 open/36.30 per km — superseded]
- Worked anchor (DERIVED): **Kadıköy→Levent ~15 km ≈ 65.4 + 15×43.56 ≈ 719 TL ≈ $15** + bridge toll, **60–90 min in peak** (INDICATIVE — traffic time unsourced, flag). Kadıköy→Bakırköy ~30 km ≈ 1,372 TL ≈ $29, 70–110 min peak (INDICATIVE).
- Ride-hail (Uber operates via yellow taxis in Istanbul + premium tiers): treat as taxi-anchored; premium tiers above metered fare. [UNSOURCED multiplier — not used in economics]

## 4 · Charter / experience market — the ceiling
- Private Bosphorus yacht charter, hourly: **from 6,250 TL/hr** (SU Yatçılık listing, Google 4.9/563 reviews) and **6,000–8,000+ TL/hr** typical; marketplace range 3,000–140,000 TL. [PRIMARY vendor listings (their own published prices); market breadth SECONDARY]
- → **$131–168/hr** typical private-charter anchor at 47.76. Sunset/tour segment is deep and year-round.
- Tourist excursion (mass-market Bosphorus tour, Şehir Hatları/Turyol/Dentur): short tours run in the low-hundreds TRY per seat [SECONDARY, band only — re-verify seat prices before using in L3].

## 5 · Extracted anchors for the premium express tier
Positioning: **above İstanbulkart ferry, at-or-below Deniz Taksi per-seat, far below private charter.**
| Anchor | Per-seat value |
|---|---|
| Public ferry cross-strait | $1.1–1.4 |
| Public/private Islands fare | $2.4–4.3 |
| Deniz Taksi per-seat equivalent (6 pax) | $4–11 |
| Taxi cross-city (1 pax) | $15–29 + 60–110 min |
| Private charter (hourly, whole vessel) | $131–168/hr |
- **DERIVED per-trip premium-express anchors:** Marmara trunk legs (Bakırköy/Yenikapı↔Kadıköy/Bostancı) **150–220 TL ($3.1–4.6)/seat**; Islands express **250–400 TL ($5.2–8.4)/seat**. Rationale: 3–4× the public fare, ≈Deniz-Taksi-per-seat, 15–25% of the taxi alternative it beats on time. Istanbul purchasing power (net min wage $588/mo) rules out Gulf-style pricing — stay in single-digit USD per seat. **Flag for Jaideep confirmation.**

## 6 · Fail-closed list (fares file)
- Şehir Hatları official fare page not directly captured (numbers from tariff press) → re-verify at sehirhatlari.istanbul before render.
- İDO seabus per-route fares: not captured this pass → not used (İDO is now mostly inter-city).
- Peak road travel times: INDICATIVE only, no primary source → never render as fact, only "traffic-dependent".
- VIP transfer / hotel boat-transfer rates: not captured → not used.
