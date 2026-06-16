# CHANGELOG-FOR-CLAUDE — 2026-06-16 — Wave 1A bite 2 scrub+enrich (scrub-w1a-b2)

**Gold:** #79j → **#79k**
**Scope:** Wave 1A bite 2 — NYC Harbor + Boston + Bar Harbor / MDI + Halifax (metros nyc-harbor, boston, bar-harbor-maine, halifax).
**Ledger:** LB-180

## Counts

| | before (#79j) | after (#79k) | Δ |
|---|---:|---:|---:|
| ROUTES | 5,388 | 5,393 | +5 |
| POIs (FBT.poi) | 11,316 | 11,316 | 0 (−14 noise / +14 marquee enrich) |
| Cities (FBT.city) | 164 | 166 | +2 (Bar Harbor MDI, Halifax NS Atlantic) |
| Clusters | 75 | 77 | +2 |
| Sidecar records | 82 | 82 | 0 (no partner-pinned corridors touched) |

## Scrub kills (14 BPs, 14 routes)

**NYC Harbor — 11 BPs / 7 routes:**
- Harbor Freight (hardware retailer) ×3 incl. Transport Corporation + dup
- Harbor NYC Rooftop, Sunken Harbor Club (Brooklyn cocktail bar)
- Harbour View Senior Living, Harbor 1500 (residential)
- Harbor Picture Company (185 Varick St — film studio)
- Blue Harbour Property Management
- New York Harbor School (Governors Island high school)
- American Yacht Harbor (real BP is St Thomas USVI — mis-geocoded)
- 7 auto-permutation noise routes (LB-176a residue)

**Boston — 3 BPs / 7 routes:**
- Harbor House Rehabilitation & Nursing Center
- Harbour Food Service Equipment / Imperial Dade
- Regus — Boston Seaport coworking office
- 7 orphan-endpoint routes incl. carried bite-1 followups (Hingham Shipyard ↔ Safe Harbour Insurance class; Long Wharf → Boston & New England self-reference)

## Enrich (14 BPs, 19 routes, 2 clusters)

**NYC Harbor (existing cluster):** 7 new Pioneer II commuter spine routes — Pier 11 / Wall Street hub to Hoboken (2.16), Paulus Hook (1.41), Long Island City (3.56), DUMBO Pier 1 (0.54), South Williamsburg (1.77); Midtown / Pier 79 ↔ Hoboken (1.92); Whitehall ↔ St. George (4.37). All endpoints pre-existing dense BP set (NY Waterway / NYC Ferry / SI Ferry).

**Boston (existing cluster):** 2 new BPs (Salem Ferry Wharf — Blaney Street; Hull / Pemberton Point Ferry Terminal) + 4 Long Wharf corridor routes — Long Wharf → Hingham Shipyard (8.61), Provincetown / MacMillan Pier (42.86 nm — just under Pioneer II soft cap), Salem (12.34), Hull / Pemberton (6.04).

**Bar Harbor / MDI (greenfield):** new cluster `bar-harbor-mdi-maine-usa` (anchor bp-abcd26ea6e Bar Harbor Town Pier — LB-174 real-BP anchor). 6 new BPs: Bar Harbor Town Pier, Northeast Harbor Municipal Marina, Southwest Harbor Town Dock, Cranberry Isles (Islesford Town Dock), Winter Harbor Municipal Pier, Schoodic Point (Acadia). 4 intra routes: Bar Harbor ↔ Northeast Harbor (6.93), Bar Harbor ↔ Southwest Harbor (8.64), Bar Harbor ↔ Winter Harbor (5.05), Northeast Harbor ↔ Cranberry Isles (2.89).

**Halifax (greenfield):** new cluster `halifax-atlantic-canada` (anchor bp-a7d2c5be26 Cable Wharf / Halifax Ferry Terminal — LB-174). 6 new BPs: Cable Wharf, Alderney Landing (Dartmouth), Woodside Ferry Terminal, Peggy's Cove Public Wharf, Lunenburg Harbour Public Wharf, Mahone Bay Town Wharf. 4 intra routes: Halifax ↔ Alderney (1.04), Halifax ↔ Woodside (1.08), Halifax ↔ Peggy's Cove (17.42), Lunenburg ↔ Mahone Bay (5.0). Halifax ↔ Bar Harbor cross-border NOT minted (exceeds Pioneer II range).

## Gates (all PASS)

| Gate | Result |
|---|---|
| `gate_endpoint_labels.py` | 0 FLAG |
| `gate_city_ids.py` | PASS — 203 valid nodes / 5,393 routes / 77 clusters |
| `gate_partner_rationale_leak.py` | clean across partner-pitch/partners/*.json |
| `gate_premint_pair.py` | 0 / 5,393 flagged (threshold 0.5) |
| `gate_osm_noise_bp.py --check-only` | 0 new flags in 4 bite-2 metros (baseline-only carries from prior waves) |
| LB-175a pre-build (ROUTES ≥ floor 5,072; pier-coord verify all 14 new BPs) | PASS; max new-route 42.86 nm < Pioneer II 50 nm cap |
| `datastore_audit.py` post-seal | (recorded after seal) |

## Sidecar
- `economics_by_route_id.json` regenerated; 82 route-pinned records, 0 in `_pending_route_pin`. No bite-2 corridors are partner-pinned, so counts unchanged from #79j.

## Files changed in zip vs prior gold (#79j)
- `data-clean/FEATURES_BY_TYPE.json` (kills + 14 enrich BPs + 2 anchor cities)
- `data-clean/ROUTES.json` (−14 noise / +19 aspirational; max 42.86 nm)
- `data-clean/CLUSTERS.json` (+2 greenfield clusters with real-BP anchors)
- `data-clean/economics_by_route_id.json` (sidecar regenerated; same record set)
- `data-clean/SEAL.json` (gold label → 79k; file_hashes recomputed on actual blob bytes per LB-171; `blobs` updated to {FBT.city=166, poi=11316, priority_city=37; ROUTES.count=5393}; `sidecars` recorded)
- `data-clean/CHANGELOG-FOR-CLAUDE-2026-06-16-scrub-w1a-b2.md` (this file)

All other files carried byte-identical from #79j (extract-prior-overlay per LB-67).

## Follow-ups (non-blocking — carried to bite 3)
- 6 NYC auto-permutation residue routes flagged-not-killed (Cape Liberty ↔ Elco / Bay Ridge etc.) — advisory.
- `ics-0eb7b6593b` (Encore Ferry Dock → Cambridge Boat Club, freshwater past dam) — advisory.
- `ics-e409b964f1` Palm Beach Harbor Freight noise — deferred to Florida / Caribbean bite.
- METRO_BBOX missing nyc_harbor, boston_inner_harbor, bar_harbor_mdi, halifax — add to standing table.
- `gate_premint_pair.py` BP-existence-in-POIs check (would have caught 4 orphan Cape carries earlier).
- `datastore_audit.py --data-clean-dir` flag for delta-mode runs.
- LB-179 patch `classify_marine_bp.py` name-veto-before-bp_type-rescue not yet shipped to upstream classifier (applied inline here).

## LB refs
LB-55, LB-67, LB-104, LB-112, LB-153, LB-171, LB-174, LB-175a, LB-176a, LB-176b, LB-176c, LB-176d, LB-176e, LB-176f, LB-179, **LB-180**.
