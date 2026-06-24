# Grok routing guidance — Ocean Whisperer (Curaçao)

**From:** Tasklet · **Date:** 2026-06-24 · **Lane:** Tasklet diagnoses + specifies; Grok seals geometry.

## TL;DR
The live Curaçao map shows routes fanning out to a **phantom convergence point in open water south of the island**. Root cause is **not** the corridor source or the node coordinates — it is that the three **Hato airport-origin legs circumnavigate the island**, because Hato is on the **north / windward** coast while every resort is on the **south / leeward** coast. The corridor source has been corrected (airport legs repointed to a leeward embarkation). Grok needs to (1) reseal those legs and (2) add a detour-ratio QA gate so this class of error is caught next time.

## Evidence (from `data-clean/ROUTES.json`, sealed geometry)
| route_id | leg | straight nm | **sealed path nm** | detour | south dip |
|---|---|---|---|---|---|
| `rn-838ccd054530` | Hato → Baoase | 6.3 | **29.2** | **×4.6** | to 11.98°N |
| `rn-a88f7e7cffc2` | Hato → Spanish Water | 8.7 | **30.8** | **×3.5** | to 11.98°N |
| `rn-a3a94b8dbc88` | Hato → Sandals | 9.4 | **30.4** | **×3.2** | to 11.98°N |

All three originate at Hato (12.183 N, north shore), can't cross the island, so the sea-router takes them ~30 nm around the SE tip, dipping to **11.98°N in open water** — the convergence fan in the screenshot. Their stored `distance_nm` (6–9) disagrees with the rendered path (~30), so the label and the line also contradict each other.

The other 7 Curaçao legs are clean (detour ≤ ×1.2). Node coordinates in the BP spec are all correct.

## Why `route_land_qa.py` passed it
The current gate only checks **land-crossing** (`land_km`). The offshore fix (`grok-routing-output/abc-curacao-offshore-fix.json`) drove `land_km → 0.0`, so QA went green — but a `land_km=0` route can still be a 30 nm circumnavigation through open water. **Land-free is necessary but not sufficient.**

## Fix 1 — reseal the airport legs (source already corrected)
In `ocean-whisperer-corridors.json`, the two grounded airport legs now carry:
- `proposed_from_node_id: curacao-curacao__piscadera-bay-resort-cluster` (leeward embarkation; was `…hato-airport-waterfront`)
- `approx_distance_nm: null` (reseal exact leeward geometry — null beats confidently-wrong)
- a `_routing_correction` block with the rationale + Option B.

**Action:** reseal both legs as short leeward south-coast runs (Piscadera → Sandals ≈ 8 nm; Piscadera → Baoase ≈ 4 nm), and **retire/repoint** the three windward route_ids above so no Curaçao leg renders north of ~12.13°N or dips below ~12.05°N. The air-arrival demand basis is unchanged; only the embarkation moved to calm water (short land transfer from Hato).

**Decision — RESOLVED (Jaideep, 2026-06-24): OPTION A.** Keep the airport as the demand source and embark at the leeward Piscadera marina via a short land transfer; the CORE air-arrival revenue pool is preserved and the leg is made honest. **Proceed with the Option A reseal below — do not apply Option B.** (Option B, rejected: drop air→resort from grounded Navier sea corridors and treat the airport purely as OW's air domain.)

## Fix 2 — add a detour-ratio + bbox gate to land QA
Add to `scripts/grok-geometry/route_land_qa.py` (or the reseal acceptance step), alongside the land check:

```python
# reject visually-absurd routing even when land_km == 0
DETOUR_MAX = 1.35          # sealed path / great-circle
straight = haversine_nm(coords[0], coords[-1])
path = sum(haversine_nm(coords[i], coords[i+1]) for i in range(len(coords)-1))
if straight > 0.5 and path / straight > DETOUR_MAX:
    fail(route_id, f"detour ×{path/straight:.1f} (> {DETOUR_MAX}) — likely wrong-coast circumnavigation")

# optional regional guard for Curaçao leeward set
if route_id in CURACAO_LEEWARD_SET:
    min_lat = min(c[1] for c in coords)
    if min_lat < 12.05:
        fail(route_id, f"dips to {min_lat:.3f}°N — open water / windward, not leeward")
```

## Reseal acceptance criteria
1. No Curaçao grounded leg has detour > ×1.35 vs great-circle.
2. No Curaçao leeward leg dips below ~12.05°N or rises above ~12.13°N (stay on the south coast).
3. Every leg's stored `distance_nm` is within ±10% of its sealed path length.
4. `land_km == 0` for all grounded legs (unchanged).
5. Roadmap legs (Bonaire `rn-0f8e77cfef46`, Aruba `rn-e96930f83c0f`) stay amber-dashed and excluded from grounded economics — their straight-line geometry is fine.
6. Re-run the economics cascade on the resealed (shorter) airport-leg distances; the SOM floor will shift — that is expected and correct.

## What Tasklet already did
- Repointed the two airport legs in the corridor source + set `approx_distance_nm: null`.
- Corrected the §3 geography error in `OCEAN-WHISPERER-FINE-TUNING.md` (Hato = north/windward air gateway, not a leeward sea node).
- Set Klein Curaçao `season_days: 90`.
- De-jargoned the partner-facing narrative in `partners/ocean-whisperer.json` (no geometry touched).
