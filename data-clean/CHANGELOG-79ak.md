# Gold #79ak — 2026-06-17 forward-delta on #79aj-v2

## Scope
Consolidated 4 Phase-1 Bolt/Yango partner-mint waves (cluster-mint-only sub-archetype, LB-227 "2+1"):

| Wave | Markets | +city | +POI | +cluster | widen |
|---|---|---|---|---|---|
| BoltA1-v2 | Portugal · Estonia · Cyprus · Ireland | 5 | 7 | 3 | portugal |
| YangoB1-v2 | Israel · Kazakhstan-Caspian · Azerbaijan | 4 | 4 | 3 | — |
| BoltA2 | KSA-commercial (Jeddah/Yanbu/Dammam-Khobar) | 1 | 0 | 1 | — |
| YangoB2 | Pakistan · Côte d'Ivoire · Senegal · Mozambique | 6 | 4 | 3 | mozambique |
| **Total** | | **16** | **15** | **10** | **2** |

## Counts (vs #79aj-v2)
- ROUTES: 5,199 → 5,199 (Δ 0, no mints)
- POI: 10,646 → 10661 (+15)
- City: 176 → 192 (+16)
- Cluster: 107 → 117 (+10)

## Gates
- SEAL bytes-truth: file_hashes + blobs recomputed from on-disk bytes (LB-212 / LB-218).
- Pre-build base = #79aj-v2 GOLD-COPY top (LB-192a / LB-226 Phase 0).
- Sovereign isolation: `saudi-arabia` (RSG/NEOM/AMAALA) untouched; `ksa-commercial` minted as parallel scope-isolated cluster.

## Sovereign-scope flags
- `israel` cluster carries `sovereign_data_only: true` (Yango Israel = atlas/data only, no outreach planning until coordinated).
