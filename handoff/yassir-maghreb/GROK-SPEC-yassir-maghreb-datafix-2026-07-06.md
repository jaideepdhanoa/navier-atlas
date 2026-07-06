# GROK SPEC — Yassir/Maghreb data fixes
_2026-07-06 · Tasklet flags, Grok applies. Nobody invents a pier. All values sourced below._

Small, deterministic Maghreb hygiene ahead of the Yassir deck. All need a reseal + deploy; bundle with the current cluster-merge deploy cycle if convenient.

## 1. Cross-country cluster_id misstamps (2 routes → `mauritius`)
Both are on-water Maghreb corridors wrongly stamped `mauritius` (WS-4 spatial-anchor collision) and missing `cluster_city_id`.

| route_id | from → to | current cluster_id | correct cluster_id |
|---|---|---|---|
| `rn-27da217834e5` | `sousse-tunisia` → `monastir-tunisia` (Port El Kantaoui → Cap Monastir Marina) | `mauritius` | **`tunisia`** |
| `rn-13faccfd5399` | `algiers-algeria` → `algiers-algeria` (Port de Sidi Fredj → El Djamila / Aïn Bénian) | `mauritius` | **`algeria`** |

Also set `cluster_city_id` per your canonical convention (currently null on both). Re-inherit after.

## 2. City anchor coordinate corrections (FEATURES_BY_TYPE.json, `city` features)
Sourced from official port/marina locations. `[lon, lat]`.

| city_id | current (wrong) | correct | note |
|---|---|---|---|
| `casablanca-morocco` | `[-7.16325, 33.8465]` | **`[-7.606, 33.606]`** | ~49 km off; Port of Casablanca / Marina |
| `mdiq-tetouan-morocco` | `[-5.038, 35.722]` | **`[-5.325, 35.685]`** | ~26 km off (sits in the sea); M'diq marina |
| `al-hoceima-morocco` | `[-4.0055, 35.201]` | **`[-3.906, 35.249]`** | ~10 km off; Al Hoceima port |

If any boarding points for these cities inherit the anchor coord, re-check them for on-water after the move (BP hygiene scanner).

## 3. City label fix
| city_id | current label | correct label |
|---|---|---|
| `rabat-sale-morocco` | `Rabat Sale Morocco` | **`Rabat–Salé`** |

(Position is fine — 1 km. Label only. Drop the country suffix to match every sibling label; use en-dash.)

## 4. Morocco endpoint city_id mis-tag (70 routes) — WS-4 spatial re-stamp
70 routes carry `from_city_id`/`to_city_id` = **`casablanca-morocco`** but their endpoints are actually elsewhere on the Atlantic coast (Agadir, Essaouira, Sidi Kaouki, Mirleft, Tamri, Taghazout, Aglou, Légzira, Anchor Point, and some real Rabat/El Jadida). The whole central-Atlantic coast appears to have been defaulted to `casablanca-morocco` at the city grain.
- **Impact:** cluster_id (`morocco`) is correct, so the map isn't dark — but **city-level route grouping is wrong**. Casablanca's city page would surface Agadir/Essaouira routes; Agadir/Essaouira/etc. pages under-count. This bites the deck's per-city route slides.
- **Fix:** re-stamp endpoint `from_city_id`/`to_city_id` by nearest-anchor to the correct member city (spatial anchor, your WS-4 lane). Keep `cluster_id = morocco`.
- **Scanner note:** these are endpoint-label ↔ city_id disagreements — deterministic to detect.

## Isolated cities (context, not this spec)
- **Tangier and Al Hoceima have 0 sealed corridors** — they'll render as empty dots. Both are BP/corridor mint candidates (Tangier especially: Tanger City Port marina, Cap Malabata/Spartel, Tanger Med, cross-Strait). Tasklet will source real piers into the BP wishlist; not a re-stamp.

## Acceptance
- `rn-27da217834e5` → `tunisia`, `rn-13faccfd5399` → `algeria`; both carry a valid `cluster_city_id`; 0 Maghreb routes stamped `mauritius`.
- Three city anchors move to the sourced coords; BP hygiene clean on affected cities.
- `rabat-sale-morocco` label = `Rabat–Salé`.
- Maghreb corridors render on `/yassir` (and country pages) after deploy.

## NOT in this spec (separate lanes)
- 3 missing city briefs (Casablanca, Tangier, Al Hoceima) — **Tasklet authoring**, source-led.
- Algeria home-market depth (only ~5 routes today; "held" status) — pending Jaideep decision to mint real Algeria ports now vs Phase-2.
- Economics sheet in-place publish (`1ba9Zp…`) — deck source of truth.
