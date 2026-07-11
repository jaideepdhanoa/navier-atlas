# Grok backlog — pending work (living queue)

**Baseline:** `main` @ tip after Wave1 hand-geometry + country-opex holds pass (2026-07-11)  
**Production:** https://navier-atlas.vercel.app  
**Updated:** 2026-07-11 (autonomous backlog pass)  
**Rule:** null beats wrong · exact-ID only · no inventing rates · corridors own geography · merge/mint/deploy under greenlight

---

## Closed this pass (2026-07-11)

| Item | Verdict |
|------|---------|
| **PR #221** DiDi T1–T12 controlled review | ✅ Merged `ca6494e8` (docs-only; AR demand semantics already in #226) |
| **Wave1 hand geometry** (15 pairs) | ✅ Sealed — `GROK-WAVE1-HAND-GEOMETRY-SEAL-RECEIPT-2026-07-11` |
| **Wave1 held BPs** (21) | ✅ Disposition complete — 0 mints (no T1/T2); permanent + research-gated holds recorded |
| **Country-opex CR×2, Namibia×3, Cameroon×3, Congo×2** | ✅ Country-ref rows + holds cleared → active 1358 / held 6 |
| **Living backlog refresh** | ✅ This file |

---

## Active backlog (remaining)

### P0 — Release

| Priority | Track | Status |
|----------|-------|--------|
| **P0** | **Swing deck regen slides 8–11** | **Held** — model/workbook parity done (#232); live deck still claims unsupported Y1 profitability; fix six OPEX lines + sheet links `1PxUt…`. Brief: `handoff/post-224-release-verification/SWING-POST-223-DECK-REGEN-BRIEF.json` |

### P1 — Economics holds (6 corridors)

| Partner | Holds | Why | Next |
|---------|------:|-----|------|
| **DiDi Argentina** | 2 | `demand_not_exact_annual_oneway` (benchmark only) | Exact annual one-way evidence, or leave null |
| **Yango Venezuela** | 3 | No current WB `cost_index` (PLI last 2011) | Source current PLI/PPP + crew/energy/port |
| **caribbean-mobility** | 1 | USVI→BVI `cross_border_home_port_unverified` | Evidenced home-port country for opex inheritance |

Country-ref complete for: Costa Rica (cascade greenlight pending), Namibia, Cameroon, Congo (Brazzaville), Argentina (demand still blocks).

### P1 — Wave1 residual

| Surface | Open | Notes |
|---------|-----:|-------|
| Held BPs | 21 | Dispositioned; mint only on new T1/T2 exact-named landings |
| Hand geometry routes | 0 | All 15 sealed this pass |
| Coord-held routes | ~14 | Depend on held BPs / noncoordinate gates |

### P2 — Sheets / partners

| Item | Notes |
|------|-------|
| **constance / saudi-pif sheets** | Fail-closed skip / low-confidence: no invent rates; constance captive resort; saudi-pif largely 2030-dated / greenfield OFF. Do not force-publish empty corridors. |
| **Costa Rica DiDi finance cascade** | Country gate + A1 demand ready; needs **explicit greenlight** for aggregate → growth → sheet → deck |
| **Yango NAM/CM/CG corridors** | Country gate clear; `route_id` null — no invent demand/geometry |

### P3 — Deferred (not release chain)

| Item | Notes |
|------|-------|
| FE-2 dedup | ~193 referenced-copy groups |
| Mesh geometry | ~3k non-story fails — deferred until proposal surfaces credible |
| Deck OAuth lane (Grab/Minor live apply) | Omitted / skipped per prior AFK directive |

---

## Open PRs

_None at last check (post-#221)._

---

## Locked display / finance rules

- Phase map opacity: current full · prior medium · mesh low  
- Hub map scope: live cluster inheritance at build  
- Country-opex: exact country key + five numerics, or descriptive `_economics_hold_reason` — **no Singapore fallback**  
- Inland-water geometry: named water + water-adjacent endpoints; land-mask false positives recorded, not invented water

---

*Grok seat · Credibility pass: release (Swing deck) → residual holds → deferred mesh*
