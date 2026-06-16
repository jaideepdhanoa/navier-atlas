# Gold #79j — Wave 1A bite 1 scrub+enrich (2026-06-16)

**Base:** Gold #79i (`navier-atlas-gold-79i.zip`, route_count=5395).
**Slug:** `scrub-w1a-b1` — LB-179.
**Metros touched:** Miami, Cape Cod / Nantucket / MV, Hamptons / Montauk / Block Island.

## Counts
- POIs: 11,336 → 11,316 (−20).
- Routes: 5,395 → 5,388 (−7) = −11 noise + 4 aspirational.
- Clusters: 75 → 75 (unchanged).

## Scrub (22 noise BPs deleted, 11 noise routes deleted)
**Miami (14 BPs, 11 routes):**
- BPs: The Harbour Condominium (×2 dup), Harbour Gourmet, Harbour Medical and Aesthetics (×2 dup), JETSET Pilates – Sunset Harbour, The Hangar at Regatta Harbour, Brickell Harbour Condominium, Harbour Pointe of Miami Condominium Association, Harbour Residential, HARBOUR | Miami Showroom, Regal Marina / Regal Lounge, Annazon Carinderia, Discover Boating Miami International Boat Show.
- Routes: 11 auto-permutation pairs (`Miami: …Harbour Showroom/Condominium/Gourmet/Pointe…` — LB-176a residue).

**Cape Cod / Nantucket / MV (8 BPs, 0 routes):**
- Harbor Freight (hardware), Harbor Community Health Center–Hyannis, Harbor Lounge, Safe Harbour Insurance, East Harbour Motel & Cottages, Harbour House: Family Shelter, Harbour Insurance Agency Inc, "Luxurious Harbor 'Elizabeth' Cottage" (Airbnb).

**Hamptons / Montauk / Block Island:** no deletes.

## Enrich (2 new BPs, 4 new aspirational routes)
- `bp-7f4e7a7984` **Edgartown (Memorial Wharf)** — `[-70.5128, 41.3893]`, `ferry_terminal`, parent `cape-cod-islands-usa`. Source: OSM + Wikidata (Falmouth-Edgartown seasonal ferry endpoint).
- `bp-e3fe2a7c96` **Three Mile Harbor — East Hampton Town Marina** — `[-72.1893, 41.0265]`, `marina`, parent `the-hamptons-east-end-usa`. Source: OSM + Wikidata (East Hampton Town Marina, Gann Road).

New routes (all `aspirational: true`, Pioneer II, intra_island/intra_cluster):
- `ics-386fbbf122` Edgartown → Oak Bluffs (4.58 nm).
- `ics-e6600f77e9` Edgartown → Vineyard Haven (5.61 nm).
- `ics-e811c30ae5` Three Mile Harbor → Sag Harbor (4.88 nm).
- `ics-063f7a4d18` Three Mile Harbor → Montauk (11.79 nm).

## Sidecar
- `economics_by_route_id.json` regenerated: 82 records / 44 pending (unchanged vs #79i baseline — bite touches no partner-pinned corridors).

## Gates (all PASS)
| Gate | Result |
|---|---|
| `gate_endpoint_labels.py` | 0 FLAG (3 pre-existing WEAK single-token binds carried forward) |
| `gate_city_ids.py` | PASS (201 valid nodes, 5,388 routes, 75 clusters) |
| `gate_partner_rationale_leak.py` | clean (0 hits) |
| `gate_osm_noise_bp.py` (advisory) | 0 new flags in 1A metros vs baseline |
| `gate_premint_pair.py` | 0 / 5,388 routes flagged |
| LB-175a pre-build (ROUTES floor 5,072 + pier-coord verify) | PASS |

## Judgment calls
- Pioneer-range lock honored: no NYC→Hamptons direct route minted.
- Cape Cod region BP density already strong; enrichment limited to Edgartown Memorial Wharf (the most-cited gap).
- Hamptons enrichment limited to Three Mile Harbor (canonical East Hampton water-access node missing from the mesh).
- No clusters created/modified. Existing clusters anchor on real BPs (LB-174 compliant).

## Carried follow-ups
- Boston metro scrub (Hingham Shipyard ↔ Safe Harbour Insurance auto-permutation class) deferred to next bite.
- `gate_delta_consistency.py` (--delta-mode audit) tool not yet built — recommended for sub-bite scope.
- City brief `signature_routes[]` updates: scope ownership to be clarified (currently geometry-only per DATA-STORE-MAP).
