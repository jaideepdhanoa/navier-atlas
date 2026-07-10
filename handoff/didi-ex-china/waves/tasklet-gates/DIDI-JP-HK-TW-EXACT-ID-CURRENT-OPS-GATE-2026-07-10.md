# DiDi JP–HK–TW exact-ID + current-operation gate — 2026-07-10

**Status:** research-complete / seal-needed; Taiwan hard hold; Hong Kong operation pass; Japan JV-scoped with city holds  
**Repo commit inspected:** `20876d00d6d4d7f9831a5c93ed3dda9b0ee84673` (repository was already very dirty; no repo edits made)

## Operation verdict

- **Japan — conditional pass only as DiDi Mobility Japan taxi JV/partner.** Current official service areas confirm the scoped mainland/airport gateways, Niseko, Miyakojima and Ishigaki as detailed in JSON. **Holds:** Izu Oshima; Taketomi; Kanaya/Futtsu side. Never write this as ordinary direct global DiDi.
- **Hong Kong — PASS.** Current official DiDi Hong Kong passenger and taxi-booking pages provide authoritative local consumer-operation evidence. This clears the 2026-07-09 hold.
- **Taiwan — HARD HOLD.** No authoritative current local consumer-operation receipt was found. Historical launch/travel interoperability, app listings and travel aggregation do not pass.
- **Macau — EXCLUDED/HELD** for scope conflict; do not promote.

## Exact Atlas gate

- City IDs: **12/12 exact** in `CLUSTERS.json`.
- BP candidates: **13/18 exact existing features**; remaining rows are non-BP, berth gaps, dynamic-port alternatives or operation holds.
- Route candidates: **1/8 exact endpoint-ID match**: Hong Kong `rn-d7294a3ddd04` (North Point `bp-3d87991519` → Hung Hom `bp-8b029bcd34`, 1.1 nm, Pioneer II).
- Taiwan `rn-5085d4e1f498` is **not bound** to the candidate: it is quarantined/hidden, uses unresolved endpoint nodes and reports 12.3231 km interior land crossing. Keep candidate `route_id=null`.
- All seven other candidate `route_id` values remain null; no fuzzy stamping.

## No-shrink result

Prior artifact baseline is preserved at **12 cities / 18 BPs / 8 corridors / 9 demand records**; this gate adds one exact finance demand record (10 total). Existing DiDi surfaces (8 Japan IDs + Hong Kong) were not edited, deleted or demoted. Operation holds govern new claims, not destructive repository changes.

## Finance gate

**Zero promotions.** Airport/visitor volumes remain context only. Existing committed finance evidence gives **95,705 direct 2024 one-way passenger carriages** for Kaohsiung–Magong; it is preserved, but Taiwan operation and endpoint/geometry holds block DiDi promotion. Other candidate `annual_one_way_pax` values remain null.

## Ordered Grok actions

1. Preserve existing surfaces; apply Japan JV wording, HK pass, Taiwan/Macau hold.
2. Canonicalize Kurihama/Kanaya/Takeshiba/Oshima and split/confirm Tomari berths.
3. Treat only HK `rn-d7294a3ddd04` as exact route-ready; leave all other candidate route IDs null.
4. Repair and hand-waypoint Taiwan `rn-5085d4e1f498`, but keep hidden while operation is held.
5. Return stable BP/route IDs and render QA; preserve Kaohsiung–Magong demand, but Finance cascades only after Taiwan operation and geometry clear.

## Sources that changed the gate

- Japan current service areas: https://didimobility.co.jp/service/user/
- Japan current company/entity: https://didimobility.co.jp/company/
- Hong Kong passenger: https://didi.com.hk/en/passenger.html
- Hong Kong booking: https://didi.com.hk/en/taxi-booking-app-hong-kong.html

Canonical briefs were scored field-by-field in JSON. Full source, city, BP, route, null/hold, no-shrink and action ledgers are in the JSON artifact.
