# GROK SPEC — Yassir map geometry deepen (Tangier · Al Hoceima · Algiers)
_Tasklet → Grok · 2026-07-07 · owner_next: Grok (channel solver + mint + seal + cluster_id stamp)_

**Scope of THIS spec:** the 3 remaining Yassir map-geometry gaps only. Affects the **Atlas map** (Yassir deck slides 3–6 screenshots), NOT the deck slides themselves. Deck is send-ready and locked (`do-not-regenerate`).

**Already closed (do not redo):** El Jadida mint + 4 re-stamps ✓ · Annaba mint ✓ · Senegal finance (7) + Algeria reconcile (3→7) ✓ · growth_case cascade (`7f0e6af5`) ✓. All finance gates green.

---

## Standing rules that bind this work
- **Nobody invents a pier.** All coords below are real & sourced — but **verify exact berth geometry** before minting; don't trust blindly.
- **Hand waypoints, market-specific, NO land crossings.** Every corridor must route entirely over water. Where a straight OD line clips a headland/peninsula, insert offshore hand waypoints to round it. Explicit per-leg asks below.
- **Existence gate ≠ marquee gate.** `<3nm` is a marquee/featured curation gate ONLY — never a corridor-existence gate. A distinct real BP pair, on-water, no land crossing, not duplicate/parallel = valid corridor even at 1nm.
- **cluster_id MUST be stamped** on every minted route (dark-map contract — 0 null-cluster routes fleet-wide). Tangier + Al Hoceima → `morocco`; Algiers legs → `algeria`.
- **Sovereign/international out of scope:** no cross-Strait to Tarifa/Algeciras (Spain); no Peñón de Vélez / Alhucemas islets (Spanish sovereign).

---

## 1 · Tangier (`tangier-morocco`, cluster `morocco`) — isolated, 0 sealed corridors
Strait of Gibraltar gateway. Mint BPs + seal **3 corridors**.

**BPs (verify berth geometry):**
| BP | lat, lon | source |
|---|---|---|
| Tanger City Port (marina / passenger terminal) | 35.7855, -5.8043 | Tanger City Port official |
| Cap Malabata | 35.807, -5.75 | OSM headland |
| Ksar es-Seghir | 35.845, -5.56 | coastal town |
| Tanger Med port | 35.887, -5.499 | Tanger Med official |

**Corridors:**
1. **Tanger City Port ↔ Cap Malabata** (~3 nm) — bay leisure hop. Straight line hugs the bay; keep offshore of the corniche.
2. **Tanger City Port ↔ Ksar es-Seghir** (~12 nm) — coastal. **Hand waypoint:** round **Cap Malabata** offshore (waypoint ~35.815, -5.74) so the leg does not cut across the headland.
3. **Tanger City Port ↔ Tanger Med** (~15 nm) — port-to-port commuter/logistics. Same Cap Malabata offshore rounding; keep the track N of the coastline the whole way.

---

## 2 · Al Hoceima (`al-hoceima-morocco`, cluster `morocco`) — isolated, 0 sealed corridors
Rif coast bay + national park. Mint BPs + seal **2 corridors**.

**BPs (verify berth geometry):**
| BP | lat, lon | source |
|---|---|---|
| Port of Al Hoceima | 35.2474, -3.9178 | OSM port |
| Cala Bonita | 35.256, -3.912 | tripadvisor cove |
| Cala Iris (fishing village) | 35.152, -4.36 | Wikipedia Cala Iris |

**Corridors:**
1. **Al Hoceima port ↔ Cala Bonita** (~1 nm) — intra-bay. Valid existence; marquee-gate only. On-water, no land crossing.
2. **Al Hoceima ↔ Cala Iris** (~22 nm) — coastal OD west along Al Hoceima National Park. **Hand waypoint:** keep the track **offshore of the park headlands** (waypoint ~35.19, -4.14) — the coastline bulges; a straight line clips land. Skip the Peñón/islets (Spanish sovereign).

---

## 3 · Algiers (`algiers-algeria`, cluster `algeria`) — deepen existing mesh
Extend the existing Pêcherie / El Djamila / Tamentfoust mesh with west + east bay piers. Seal **2 corridors**. **Blocker to resolve first:** both legs anchor on **Port d'Alger** — resolve/confirm the Port d'Alger BP node before binding (this is the item that stalled last pass).

**BPs (verify berth geometry):**
| BP | lat, lon | source |
|---|---|---|
| Port d'Alger (city port) | *resolve existing node* | — |
| Sidi Fredj marina | 36.7642, 2.847 | predictwind/navily |
| Aïn Taya / Bordj El Kiffan (east bay) | 36.79, 3.195 | OSM; verify jetty |

**Corridors:**
1. **Sidi Fredj ↔ Port d'Alger** (~15 nm) — west-bay to city port. **Hand waypoint:** round **Pointe Pescade / Cap Caxine** offshore (waypoint ~36.815, 2.94) so the leg stays off the western headland.
2. **Port d'Alger ↔ Aïn Taya** (~11 nm) — east-bay leg. Straight across the bay is open water; verify no clipping of the harbour breakwater at the Algiers end.

---

## Acceptance
- Tangier: 4 BPs minted, **3 corridors** sealed with route_ids, cluster_id=`morocco`, all land_qa clean (Cap Malabata rounded on the 2 longer legs).
- Al Hoceima: 3 BPs minted, **2 corridors** sealed, cluster_id=`morocco`, Cala Iris leg routed offshore of park headlands.
- Algiers: Port d'Alger node resolved; 2 BPs added; **2 corridors** sealed, cluster_id=`algeria`, Cap Caxine rounded on the west-bay leg.
- **0 land-crossing corridors**, **0 null-cluster routes** post-seal (`bp_hygiene.py` / dark-map check clean).
- After seal: Yassir Tangier / Al Hoceima / Algiers light up on the Atlas so Jaideep's slide 3–6 screenshots show full density.

## Non-blocking cleanups (fold in if convenient)
- Unsealed `route_id=None` corridors pending seal: COSAMA overnight RoPax (Senegal), Sfax⇄Kerkennah (Tunisia) — headline L3 present, geometry seal pending.
- `yassir-tunisia`: `rn-74a61d330456` bound **twice** (Jorf⇄Ajim + a TGM placeholder) — dedupe/rebind.
