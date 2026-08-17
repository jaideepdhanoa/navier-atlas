# FARE-BENCHMARKS-PREMIUM-ISTANBUL
Internal research record — audit language, never renders. Date: 2026-08-16 (research pass). **FX: 47.76 TRY/USD (TCMB, 2026-08-16, per principal instruction).**

**Mandate:** fares anchored on PREMIUM substitutes (Deniz Taksi / black taxi / VIP transfer / charter), **NOT** on İstanbulkart ferry parity. This file supersedes the derivation in §5 of `FARE-BENCHMARKS-ISTANBUL.md` (do not delete that file; its public-floor data remains valid context).

---

## 1 · İBB Deniz Taksi — the anchor, now PRIMARY-verified (and corrected)

**Correction vs prior file:** the banded tariff (500 opening; 310/250/200 TL/mile) recorded earlier is **wrong for 2026**. The bands (420 opening; 310/250/200) were the **July 2024 UKOME tariff** (UKOME karar 2024/5-14.A, 25.07.2024 — Chamber of Shipping circular No. 669, 01.10.2024, denizticaretodasi.org.tr — PRIMARY document of the old decision). The current tariff is flat per-mile and much higher:

| Item | Value | Source / confidence |
|---|---|---|
| Opening fee (first mile incl.) | **500 TL** | **PRIMARY** — operator FAQ, sehirhatlari.istanbul/tr/ibb-deniz-taksi-sikca-sorulan-sorular ("Açılış ücreti 500 TL"); first-mile-inclusive structure per eleman.net tariff tracker (SECONDARY) |
| Per nautical mile thereafter | **750 TL** | **PRIMARY** — same operator FAQ ("sonrasında mil başı 750 TL") |
| Pricing basis | Per **vessel**, not per person (FAQ #14) | PRIMARY |
| Capacity | **10 pax** + 2 crew (FAQ #3, #19) | PRIMARY |
| Booking | App-only, 24/7, reservation up to 5 days ahead; card-only payment; 5-min pier wait then full charge; cancellation 100%/50%/0% at 24h/–/1h | PRIMARY |
| **Shared-ride per-seat rule** | "Paylaşımlı" mode: a joining passenger pays **1/10 of the vessel fare** (FAQ #29) | PRIMARY — **İBB itself defines the per-seat equivalent as fare÷10** |

Private-sector mirror: **istanbuldeniztaksi.com** (private operator, PRIMARY vendor listing): same 500 TL opening + 750 TL/mile **+20% VAT**; waiting 2,500 TL/30 min; hourly tour hire 5,750 TL +20% VAT (≈6,900 TL ≈ **$144/hr**). Serves Şehir Hatları piers **and hotel docks** (Çırağan, Four Seasons, Ajia, Sumahan, Les Ottomans…) and island piers — i.e., a functioning VIP water-transfer market at these prices, including Adalar.

### Worked Deniz Taksi anchors (DERIVED: 500 + (nm−1)×750; nm from NODES file; ÷10 = İBB's own per-seat rule; ÷6 = realistic group)
| OD | nm | Vessel TL | Vessel USD | Per-seat ÷10 | Per-seat ÷6 |
|---|---|---|---|---|---|
| Karaköy→Kadıköy | 2.9 | 1,925 | $40 | **$4.0** | $6.7 |
| Yenikapı→Kadıköy | 3.6 | 2,450 | $51 | **$5.1** | $8.6 |
| Bostancı→Büyükada | 5.4 | 3,800 | $80 | **$8.0** | $13.3 |
| Bakırköy→Kadıköy | 8.1 | 5,825 | $122 | **$12.2** | $20.3 |
| Kadıköy→Büyükada | 9.5 | 6,875 | $144 | **$14.4** | $24.0 |
| Bakırköy→Bostancı | 12.6 | 9,200 | $193 | **$19.3** | $32.1 |

Note: these are ~2.4–2.9× the prior file's worked anchors ($23 → $40 Karaköy–Kadıköy; $66 → $144-class Islands runs). The premium ceiling İBB itself set is much higher than previously recorded.

## 2 · Road premium — taxi classes, Uber, VIP transfer

### 2.1 Taxi tariff status — TWO 2026 updates (prior file is stale)
- **16 Feb 2026 tariff** (İTEO/UKOME; full class table via taksim.taxi guide, SECONDARY): sarı 65.40 open / 43.56 per km / 210 min; **turkuaz 75.21 / 50.09 / 240**; **8+1 minivan 85.02 / 56.63 / 270**; **VIP siyah (black) 111.18 / 74.05 / 360**; sarı waiting 544.45 TL/hr.
- **20 July 2026 tariff** (+10%, İBB Meclisi — CNN Türk, SECONDARY): sarı **71.94 open / 47.92 per km / 230 min**; waiting 598.90 TL/hr. Class figures partially reported (İTEO Instagram, SECONDARY): "Z taksi" 82.73 / 55.10. Black-class post-July figures not press-verified → **DERIVED ×1.1: ≈122.3 open / ≈81.5 per km**.
- **Class multipliers (verified from Feb table): turkuaz = 1.15× yellow; 8+1 = 1.30×; black = 1.70×.** (The 2.3× black multiplier hypothesis is NOT supported by current tariffs — it's 1.7×.)

Worked anchors (DERIVED, + bridge toll, times INDICATIVE traffic-dependent):
| OD | Yellow (Jul-26) | Black (Feb-26 verified / Jul-26 est.) | Time |
|---|---|---|---|
| Kadıköy→Levent ~15 km | 791 TL ≈ $17 | 1,222 TL ≈ $26 / ~1,344 TL ≈ **$28** | 60–90 min peak |
| Kadıköy→Bakırköy ~30 km | 1,510 TL ≈ $32 | 2,333 TL ≈ $49 / ~2,566 TL ≈ **$54** | 70–110 min peak |

### 2.2 Uber in Istanbul
- Uber operates via licensed taxis; **Black Taxi tier is live on the Uber app in Istanbul** (Uber TR blog — PRIMARY: "Black Taxi now available on Uber in Istanbul"; metered at the black-taxi tariff above, i.e., 1.7× yellow).
- Turquoise tier listed but frequently unavailable; UberXL (private van product) reported discontinued — taxi 8+1 minivan class covers it (SECONDARY: traveler guides/Reddit 2026). No surge-style premium multiplier beyond UKOME tariffs → **use UKOME black tariff as the ride-hail premium anchor** [no UNSOURCED multipliers used].

### 2.3 VIP road transfer (named vendors, per vehicle)
| Vendor | Product | Price | Confidence |
|---|---|---|---|
| merrytourism.com | IST airport→city: Mercedes E sedan / Vito (7) / Sprinter (16) | **€25 / €40 / €70** | PRIMARY (vendor's published fixed prices) |
| istanbulairportstransfer.net | IST→Old City, Vito VIP | **from €60** | PRIMARY (vendor) |
| Tripadvisor/Viator product (Private Mercedes Istanbul VIP Transfer) | airport/hotel group transfer | **$58–76 per group** (4–5 pax) | SECONDARY (marketplace listing) |
- Per-person equivalent at 4–6 pax: **≈$8–16/person** for a 45–90-min premium road transfer. This is the road-VIP willingness band for a single premium leg in Istanbul.

## 3 · Fast-ferry premium precedent (İDO) — per-seat class pricing exists
- İDO İstanbul–Bursa (Yenikapı/Kadıköy→Güzelyalı, ~1h35m, dynamic pricing): **promo 765–795 TL ($16.0–16.6), economy 825–845 TL ($17.3–17.7)**; BUDO flat 625 TL ($13.1). [SECONDARY — denizde.com.tr 2026 fare table; İDO site is dynamic-priced, exact business fare not scrapable]
- **Business Class exists** on Yenikapı–Bursa and Yenikapı–Bandırma fast ferries ("üst salon" comfort; upgrade "from 71 TL" over economy — SECONDARY, picodi/İDO promo copy; İDO historically sold Promosyon/Ekonomi/Business/VIP classes — SECONDARY denizhaber.net). → Precedent: Istanbul market already pays **~$17–19/seat** for a ~1.5h fast-ferry seat and accepts paid class upgrades on water.

## 4 · Charter / experience / air — the ceiling
| Anchor | Value | Source/confidence |
|---|---|---|
| Kolayyat (marketplace, İstanbul piers: Bebek, Karaköy, Eminönü, Kabataş…) | motoryachts **₺2,700–8,400/hr** typical (to ₺39,750/hr, 80-pax); sells "Deniz Transferi" incl. Adalar/Yalova/Bursa transfers, quote-based | PRIMARY (published hourly rates) |
| Teknevia | speedboat (sürat teknesi) hire **from ₺11,000/hr ≈ $230/hr** | PRIMARY (vendor) |
| Getmyboat | 26 m yacht, Bosphorus, 12 pax | **$455/hr** (2h min) | PRIMARY (listing) |
| Viator | 2h private Bosphorus luxury yacht cruise incl. hotel transfer, ≤8 pax | **$1,140/group ≈ $71/person·hr** | SECONDARY (marketplace) |
| Private deniz taksi hourly (istanbuldeniztaksi.com) | 5,750 TL+VAT ≈ **$144/hr** | PRIMARY (vendor) |
| Helicopter charter (İst Aviation, Airjet; Avione Jet tours) | **€3,000–6,000/hr**; 30–45-min city tours €4,000–5,000 +20% VAT | PRIMARY (vendors' published ranges). No scheduled helicopter shuttle found — charter only. |
| Prior file's charter anchors (SU Yatçılık 6,250 TL/hr etc.) | ₺6,000–8,000/hr typical | unchanged, consistent with Kolayyat band |

## 5 · Premium demand evidence, Adalar
- İBB Deniz Taksi serves island piers; a Kadıköy/Bostancı-area private sea-taxi operator advertises 7/24 Adalar↔Anadolu-yakası VIP service at the 500+750/mile tariff (istanbuldeniztaksi.com — PRIMARY; plus Instagram operators, SECONDARY). Kolayyat sells private yacht transfers to Büyükada/Heybeliada (quote). Viravira: Büyükada boat hire from ₺25,004/day.
- No scheduled premium fast-boat line to Adalar exists today → the express-seat slot between **$1.4 public ferry** and **$80–144 per private vessel** is empty. That's the IST-2 opportunity.

## 6 · DERIVED premium-anchored fare recommendation (per corridor)
Positioning rule (per principal): anchor on (a) Deniz Taksi per-seat (÷10, İBB's own rule), (b) black-taxi trip replaced + time saved, (c) VIP-transfer per-person — **not** on İstanbulkart parity. All figures DERIVED; TL rounded; USD at 47.76. **Flag for Jaideep confirmation before any render.**

### IST-1 Marmara Trunk — short legs (Yenikapı↔Kadıköy, Kadıköy↔Bostancı; ~13 min)
- Anchors: Deniz Taksi per-seat $5.1; VIP-transfer per-person $8–16; black taxi single-rider $26–28 (Kadıköy–Levent class trip).
- **Spot: 250–350 TL ($5.2–7.3)/seat** — at/just above İBB's own per-seat equivalent, ~half the road-VIP per-person band, guaranteed seat + schedule (Deniz Taksi is on-demand, we're scheduled).

### IST-1 Marmara Trunk — long legs (Bakırköy↔Kadıköy/Bostancı, Yenikapı↔Bostancı; ~29–45 min vs 70–110-min road)
- Anchors: Deniz Taksi per-seat $12.2–19.3; black taxi replaced $49–54 + 70–110 min; VIP Vito per-person $8–16.
- **Spot: 500–750 TL ($10.5–15.7)/seat** — 80–85% of Deniz-Taksi-per-seat, ~20–30% of the black-taxi fare it beats by ~an hour, ≈ İDO Bursa fast-ferry seat ($16–18) for a shorter, faster premium ride.

### IST-2 Islands Express (Kadıköy→Büyükada ~26 min; Bostancı→Büyükada ~15 min)
- Anchors: Deniz Taksi per-seat $14.4 (Kadıköy) / $8.0 (Bostancı); private vessel $80–144/trip; charter $130–230/hr; İDO class precedent $17+/seat.
- **Spot: Kadıköy→Büyükada 450–650 TL ($9.4–13.6)/seat; Bostancı→Büyükada 300–450 TL ($6.3–9.4)/seat.** Peak/weekend (tourist) yield-managed up to **800 TL ($16.7)**. Logic: at-or-below Deniz-Taksi-per-seat, 10–20% of a private vessel, categorical 2–4× time win no road can contest.

### IST-3 Cross-strait Comfort Shuttle (Karaköy↔Kadıköy, 10-kn cap, NO time win)
- Anchors: Deniz Taksi per-seat $4.0; VIP-transfer per-person $8–16 (comfort willingness); vapur $1.4 (floor, not anchor).
- **Spot: 150–250 TL ($3.1–5.2)/seat** — parked exactly at the İBB per-seat equivalent; sold as guaranteed-seat/quiet/zero-emission comfort + hotel/cruise (Galataport) hops. Keep CONSTRAINED; no economics built on speed here.

### Committed-commuter seat bundles (~40 legs/mo, ~35% off mid-spot — Blade-commuter-pass logic)
| Product | TL/month | USD/month | vs alternative |
|---|---|---|---|
| Trunk short-leg pass | **7,000–9,000** | **$147–188** | daily black-taxi commuter pays 4–6× more |
| Trunk long-leg pass (Bakırköy↔Asian side) | **14,000–18,000** | **$293–377** | ~15–20% of 40 black-taxi legs (≈$2,100); saves ~40–70 h/mo |
| Islands resident/commuter pass | **12,000–15,000** | **$251–314** | island access is water-only; premium alternative is $80+/trip private |
- Affordability note: bundles target professionals/employers (net min wage $588/mo — these are 25–60% of it; sell B2B/employer-paid first, consistent with employer-network playbook).

### Spot-seat summary band & charter
- **Spot seats: 150–800 TL ($3.1–16.7)** across the network (comfort shuttle floor → Islands peak).
- **Charter/experience: 9,000–15,000 TL/hr ($188–314)** per foiler — above the conventional motoryacht market (₺2,700–8,400/hr) and speedboat (₺11,000/hr) on novelty/zero-emission/speed, ~10% of helicopter (€3,000–6,000/hr ceiling).

## 7 · Fail-closed list
- **deniztaksi.istanbul unreachable** (scrape failed this pass) — tariff instead PRIMARY-verified via operator Şehir Hatları FAQ page; re-check deniztaksi.istanbul/app before render.
- İDO **business-class exact fare** not captured (dynamic pricing, JS-only site; only "from 71 TL upgrade" promo copy) → use economy band only in economics; business = precedent claim, not a number.
- **Post-July-2026 black/turkuaz taxi tariff table** not press-verified → black Jul-26 figures are ×1.1 DERIVED; verify İTEO/UKOME table before render.
- Named **hotel boat-transfer rates** (e.g., Vakko Hotel boat, bosphorustour.com point-to-point) — quote-only, no published prices → not used numerically.
- **Büyükada fixed-price private speedboat transfer** (named vendor, per-trip) — market is quote-based; only hourly/daily rates captured.
- **No scheduled helicopter or seaplane service** found IST↔city/Adalar — charter-only ceiling.
- Uber in-app price estimates (real-time) not captured — metered UKOME tariffs used instead; no Uber-specific premium multiplier applied.
- Peak road times remain INDICATIVE (unchanged from prior file) — render only as "traffic-dependent".

## 8 · Source URLs
- https://sehirhatlari.istanbul/tr/ibb-deniz-taksi-sikca-sorulan-sorular (PRIMARY — Deniz Taksi tariff/capacity/booking/shared-ride)
- https://www.denizticaretodasi.org.tr/tr/sirkuler/deniz-taksi-ucret-tarifesi-21294 (PRIMARY doc of superseded 2024 banded tariff)
- http://www.istanbuldeniztaksi.com/deniz-taksi-ucret-tarifesi/ (PRIMARY vendor — private sea taxi, hotel piers, hourly)
- https://www.eleman.net/is-rehberi/guncel/istanbul-toplu-ulasim-ve-taksi-ucretleri-tarifesi-h3216 (SECONDARY tracker)
- https://taksim.taxi/rehber/taksi-tarifesi-2026 (SECONDARY — Feb-2026 taxi class table)
- https://www.cnnturk.com/turkiye/istanbul-taksi-ucretleri-tarifesi-indi-bindi-ve-kisa-mesafe-ucreti-ne-kadar-oldu-yeni-istanbul-zamli-taksi-tarifesi-2026-3444538 (SECONDARY — 20 July 2026 +10% tariff)
- https://www.uber.com/tr/en/blog/black-taxi-now-available-on-uber-in-istanbul/ (PRIMARY — Uber black taxi tier)
- https://denizde.com.tr/tr/feribot/istanbul-bursa (SECONDARY — İDO/BUDO 2026 fares); https://www.picodi.com/tr/ido (SECONDARY — business class promo)
- https://www.merrytourism.com/en/istanbul-private-transfer ; https://www.istanbulairportstransfer.net/... (PRIMARY vendors — VIP road transfer)
- https://kolayyat.net/hizmetlerimiz/deniz-transferi (PRIMARY marketplace — hourly yacht rates, transfer product); https://www.teknevia.com/surat-teknesi-kiralama (PRIMARY — speedboat); https://www.getmyboat.com/trips/MYL4VR7Y/ ; https://www.viator.com/tours/Istanbul/2-Hour-Bosphorus-Yacht-Cruise-with-Transfers/d585-11522P4
- https://istaviation.com/helikopter-kiralama-fiyatlari/ ; https://airjet.com.tr/helikopter-kiralama-fiyatlari.html ; https://www.avionejet.com/tr/helikopter-kiralama/istanbul-helikopter-kiralama (PRIMARY vendors — helicopter ceiling)
