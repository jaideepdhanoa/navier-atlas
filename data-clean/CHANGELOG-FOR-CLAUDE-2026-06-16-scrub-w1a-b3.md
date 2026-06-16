# CHANGELOG — Gold #79l — Wave 1A bite 3 scrub+enrich splice+seal (2026-06-16)

**Bite scope:** Bay Area SF / Seattle-PNW-San Juans / Victoria-Gulf Islands.
Counterpart to staged delta from `navier-scrub-enrich-wave` subagent (`/tmp/scrub-wave-1A-bite3/`). Sealed by `navier-scrub-wave-splice-seal` worker.

## Counts (Gold #79k → #79l)

- **Routes:** 5,393 → 5,421 (Δ +28 = −9 noise/auto-permutation kills + 37 aspirational mints).
- **POIs:** 11,316 → 11,273 (Δ −43 = −56 OSM-noise BPs + 13 marquee enrich).
- **Cities:** 166 → 168 (Δ +2 = san-juan-islands-usa anchor + gulf-islands-canada anchor).
- **Clusters:** 77 → 79 (Δ +2 greenfield, both LB-174-compliant real-BP anchors).
- **Sidecar `economics_by_route_id.json`:** 82 records / 44 pending — unchanged vs #79k (no partner-pinned corridors touched this bite).

## Kills (56 BPs, 9 routes)

- **Bay Area SF:** 27 BPs (Fog Harbor Fish House, Harbor Freight ×2, Leia D. Harbour MD, Harbor House Ministries, Harbor Bay Isle HOA, Harbor Ready Mix, Harbour [generic], Harbour Way street intersections ×2, Delarosa Marina restaurant, Marina Food Market, Marina Pizza, Bay Area Dragons sports, Pogo Park / Harbour-8, Harbor Park, Harborview Park, Harbor Bay Club fitness, etc.).
- **Seattle PNW San Juans:** ~15 of 27 kills are `harbour pointe` strip-mall macro-pattern (LB-179 promote to NOISE_STRONG).
- **Victoria Gulf Islands:** balance of 56 kills.
- **9 auto-permutation noise routes** (`ics-*` and `rn-*`) killed by LB-180 endpoint-orphan/label-match.

## Enrich (13 BPs, 37 routes, 2 greenfield clusters)

- **Bay Area SF:** 14 hub-and-spoke routes around Ferry Building + Pier 41 (LB-180 NYC pattern extended to dual hubs).
- **Seattle/PNW/San Juans:** 6 BPs + 11 routes; new greenfield cluster `san-juan-islands-usa` (anchor `bp-4f80ff46d4` Friday Harbor WSF Terminal); WSF mesh augment.
- **Victoria/Gulf Islands:** 7 BPs + 12 routes; new greenfield cluster `gulf-islands-bc-canada` (anchor `bp-51fc0afe7f` Ganges Public Wharf, Salt Spring); BC Ferries mesh + cross-border Vancouver↔Victoria + Sidney WSF International.

## Cross-cluster cross-border mints (notable)

- Anacortes ↔ Friday Harbor (cross_market, WSF).
- Sidney ↔ Friday Harbor (cross_border, WSF International, 19 nm).
- Sidney ↔ Anacortes (cross_border, WSF International, 31 nm).
- Vancouver ↔ Victoria (great-circle by water = 53.02 nm, longest mint this bite — within Pioneer II hard cap 70 nm; over LB-180 soft cap 45 nm — payload-acknowledged exception for cross_border BC Ferries spine).

## Pioneer II cap status

- Soft cap: 45 nm (LB-180 proposal carry).
- Hard cap: 70 nm (Pioneer II spec).
- Longest minted this bite: **53.02 nm** Vancouver ↔ Victoria.

## Gates (all PASS)

| Gate | Result |
|---|---|
| `gate_endpoint_labels.py` | 0 hard flags (3 pre-existing WEAK single-token binds carried: SG Marina Bay↔Changi, MLE Velana ×2) |
| `gate_city_ids.py` | PASS — 205 valid nodes / 5,421 routes / 79 clusters |
| `gate_partner_rationale_leak.py` | clean across partner-pitch/partners/*.json |
| `gate_osm_noise_bp.py` (advisory) | 0 new flags in 3 bite-3 metros (27 advisory items are pre-existing baseline carries from MENA/SEA waves) |
| `gate_premint_pair.py` | 0 / 5,421 routes flagged (threshold 0.5) — first 0-flag at this delta size (37 new routes, 13 new BPs); validates LB-179 inline name-veto triangulation at scale |
| LB-175a pre-build (ROUTES ≥ floor 5,072 + pier-coord verify all 13 new BPs) | PASS |
| `datastore_audit.py` post-seal | see SEAL meta |

## Inline patches applied by wave subagent (un-shipped to upstream classifier)

- LB-179 name-veto-before-bp_type-rescue.
- LB-180 endpoint-orphan / label-match kill for noise auto-permutation routes.
- LB-180 hub-and-spoke commuter mesh extended to Bay Area (dual hubs).
- LB-180 greenfield cluster mint for San Juans + Gulf Islands.

## Wave 1 milestone

**After this seal, Wave 1 (US/Canada coastal) scrub+enrich pass is COMPLETE.** Three bites — bite 1 (Miami/Cape/Hamptons), bite 2 (NYC/Boston/Bar Harbor/Halifax), bite 3 (Bay Area/Seattle-San Juans/Victoria-Gulf) — covered the East, NE, and West coasts plus 2 cross-border BC↔WA spines.

## LB refs

LB-67, LB-153, LB-171, LB-174, LB-175a, LB-176a/b/c/d/e/f, LB-179, LB-180, LB-181 (this entry).
