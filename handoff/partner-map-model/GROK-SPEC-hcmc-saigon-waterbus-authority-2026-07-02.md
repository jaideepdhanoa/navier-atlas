# GROK SPEC — Ho Chi Minh City / Saigon Waterbus · authority mint-seal + economics

**From:** Tasklet · **Date:** 2026-07-02 · **Phase:** D (Batch-8) Wave 1 · **Slug:** `hcmc-saigon-waterbus`

## State (Tasklet lane complete)
- New PTA authority, both trees. Fidelity **PASS** (items=8 keep=8 bp_err=0 journey_bp=0).
- City node `ho-chi-minh-city-vietnam` + **4 real Line-1 `bp-` stations** anchored. Corridors **pending-seal** (route_id null).
- Archetype `public_transit`. No `growth_case` (honest-pending). Renderer guards on null → builds clean.

## Boarding points (real, anchored)
| node | bp_id | station | lng,lat |
|---|---|---|---|
| hcmc-bach-dang | bp-a6e129fa04 | Bach Dang Wharf (D1) | 106.70677, 10.770864 |
| hcmc-binh-an | bp-7868601ce6 | Binh An (Thu Duc) | 106.728415, 10.797366 |
| hcmc-thanh-da | bp-dec4b9ef5a | Thanh Da (Binh Thanh) | 106.716374, 10.819355 |
| hcmc-linh-dong | bp-3c865bb81b | Linh Dong (Thu Duc) | 106.746376, 10.834971 |

## Corridors to MINT (Saigon Waterbus Line 1 — Saigon River, hand waypoints, NO land crossings)
| pair | approx nm |
|---|---|
| Bach Dang ↔ Binh An | 1.7 |
| Binh An ↔ Thanh Da | 1.5 |
| Thanh Da ↔ Linh Dong | 2.1 |
| Bach Dang ↔ Linh Dong (Line 1 through-run) | 5.3 |

## Grok asks
1. **Mint** the 4 corridors above with hand-waypointed river geometry (follows Saigon River + Thanh Da Canal; the Thanh Da peninsula bend needs explicit waypoints — no land crossing). Bind `rn-` route_ids back into `journeys_unlocked` + `phases[].featured_routes` (`_link_status: sealed`).
2. **Economics regen** — authority public-value pass (add slug to Phase-D set).

## Guardrails
- Do **not** bind the existing long-haul `rn-` (Vung Tau / Con Dao express, 25–34 nm) — those are NOT Line 1.
- Exclude Phu Quoc / Ha Tien "Binh An" POIs (mis-matches). Null beats wrong.
