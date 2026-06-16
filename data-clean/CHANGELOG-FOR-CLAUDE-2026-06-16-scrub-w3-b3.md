# Gold #79r — Wave 3 bite 3 scrub+enrich splice+seal (2026-06-16)

**Scope:** Third bite of Wave 3 (Western Mediterranean). Metros: Mallorca/Balearics + Côte d'Azur (French Riviera) + Corsica. Counterpart to staged delta `/tmp/scrub-wave-3-bite3/` produced by `navier-scrub-enrich-wave` subagent. Sealed by `navier-scrub-wave-splice-seal` worker.

## Counts (Gold #79q → #79r)
- Routes: 5,388 → 5,340 (Δ −48 = 88 LB-180 orphan-endpoint route kills + 40 aspirational Western-Med ferry/island mints).
- POIs: 11,109 → 11,045 (Δ −64 = −77 OSM-noise BPs + 13 marquee enrich BPs).
- Cities: 170 → 170 (no new anchor; LB-174 `spain`/`france` country re-anchors only).
- Clusters: 90 → 93 (Δ +3 greenfield meta-clusters: `balearic-islands-spain` [Puerto de Palma anchor; 3-member Mallorca+Ibiza+Menorca per LB-186 archipelago consolidation], `cote-dazur-france-archipelago` [Port de Nice anchor; Nice+Monaco], `corsica-island-france` [Ajaccio anchor]).
- Sidecar `economics_by_route_id.json`: 78 records / 48 pending — unchanged vs #79q (no new partner-route bindings this bite; route_id churn well below partner-pinned set).

## Kills (77 BPs, 88 orphan-endpoint routes)
- mallorca-balearics: 30 BPs (samples: Marina Palmanova Apartamentos, Freedom Boat Club Oficinas, HARBOUR LOFTS).
- cote-dazur-french-riviera: 47 BPs (samples: Old Harbour chic studio, VIEW OF HARBOUR OF STE MAXIME LUXURY VILLA WITH SPA, NEWLY RENOVATED Harbour View Balcony).
- corsica: 0 (thin-starter, node-id BPs only — sister to LB-186 Ionian pattern).
- 88 LB-180 orphan-endpoint route kills swept in-scope.

## New Spanish noise tokens (promote NOISE_STRONG)
`apartamentos`, `hostal`, `pensión`, `marisqueria`, `chiringuito`, `lonja`, `residencial`, `urbanización`, `terraza`, `yates`, `oficinas`, `tienda de suministros`.

## New French noise tokens (promote NOISE_STRONG)
`résidence`, `hébergement`, `location de bateau/yachts`, `camping`, `tabac`, `musée`, `parc à bateaux`, `taxiboat`, regex `view of harbour|luxury villa with spa`. `Club nautique` + `capitainerie` KEPT marine CAPTIVE_RESCUE.

## New clothing/lifestyle brand-collision pattern (promote NOISE_STRONG override of `marina` CAPTIVE)
Marina Rinaldi (Italian fashion house), Marina Yacht Wear, Marina Style Studio, Marina Caffé, Tabac Presse de la Marina, Sur la Marina, Camping Marina Paradise.

## New Western-Med brand rescues (20 — promote RESCUE_PHRASES)
Baleària, Trasmediterranea, Iscomar, Pitra Lines, Aquabus, Grimaldi Trasmed, Trans-Côte-d'Azur, TLV-TVM, TPM, Compagnie Maritime Cassidaigne, Monaco Marine, Safe Harbor, IGY, La Méridionale, Corsica Ferries, Corsica Linea, Mobylines/Moby Lines, Saremar, Naviera Balear, Odyssey.

## Enrich (13 BPs, 40 routes)
- 13 new BPs across 3 metros — `bp-andratx-port`, `bp-cala-ratjada-port`, `bp-mao-port-cos-nou`, `bp-ciutadella-port`, `bp-cannes-quai-laubeuf`, `bp-lerins-ste-marguerite`, `bp-lerins-st-honorat`, `bp-port-cros-pier`, `bp-hyeres-port`, `bp-toulon-mourillon`, `bp-st-tropez-vieux-port`, `bp-ile-rousse-port`, `bp-propriano-port`.
- 28 Pioneer II + 12 Quanta-LR. Longest mint = 157.4 nm (Q-LR, < 700 nm cap). Palma↔Ibiza placed on Q-LR (right at 70 nm Pioneer-II hard cap). Palma↔Menorca 100 nm Q-LR amber-dashed LOCKED corridor `ics-739626bfb0` PRE-EXISTS — preserved per LB-104 (not re-minted). Existing Nice↔Monaco 6.5 nm Pioneer II `e__cote-dazur-france__port-de-nice__monaco-monaco__port-hercule` preserved (not re-minted).
- NEW `cross_border` trip_scope coined for Bonifacio ↔ Santa Teresa di Gallura (Saremar / Mobylines) 7 nm Pioneer II — uses existing costa-smeralda-italy BP `bp-d0c4a00ad9`. Schema enum needs codification.
- LB-174 country re-anchors (2):
  - `spain` country cluster from mallorca-spain city_id → Puerto de Palma BP.
  - `france` country cluster from cote-dazur-france city_id → Port de Nice BP.

## Pattern notes (NEW this bite)
- LB-186 archipelago consolidation extended to **3-member** (balearic-islands-spain) — co-exists cleanly with country `spain` cluster. Pattern validated up to 3 members.
- Clothing/lifestyle brand-collision pattern formalized — `marina` CAPTIVE rescue must be overridden by NOISE_STRONG on (Rinaldi|Yacht Wear|Style Studio|Caffé|Tabac Presse|Camping|Sur la).
- Spanish noise rate ~16-20%, French Riviera ~25-30% (highest of any Med metro to date — luxury short-term-rental SEO dominates), Corsica 0% (thin-starter).
- 9 consecutive bites of inline LB-179 classifier patch application; 7 consecutive 0-flag `gate_premint_pair` at scale. **CRITICAL ship priority.**
- `gate_premint_pair` extension needed: also flag non-bp-* non-node-id endpoints (city_id-as-endpoint pattern surfaced inline this bite).
- NEW `cross_border` trip_scope enum — schema codification follow-up.

## Gates (all PASS substantively)
| Gate | Result |
|---|---|
| `gate_endpoint_labels.py` | 4 HARD FLAG pre-existing carries (Philippines + UAE, identical to #79q); 3 WEAK single-token binds (SG + MLE ×2). NOT introduced this bite. |
| `gate_city_ids.py` | PASS — 205 valid nodes / 5,340 routes / 93 clusters. |
| `gate_partner_rationale_leak.py` | clean across `partner-pitch/partners/*.json`. |
| `gate_osm_noise_bp.py` advisory on 3 bite metros | 0 NEW flags (bite already scrubbed). |
| `gate_premint_pair.py` | **0 / 5,340 routes flagged** — 7th consecutive 0-flag at scale. |
| LB-175a pre-build (ROUTES ≥ 5,072 floor + pier-coord verify all 13 new BPs) | PASS; max new-route 157.4 nm < Q-LR 700 nm cap. |
| `datastore_audit.py` post-seal | substantive PASS (DB carry per follow-ups). |

## Operational notes
- DUAL-SEAL-WRITE (LB-182) + LB-152 flat-shape overwrite (LB-183) applied; live `atlas-external/data-clean/SEAL.json` mirrored from `/tmp/gold-stage-3-bite3/data-clean/SEAL.json`.
- Economics sidecar built with `--aggdir finance/recal` per LB-185 standing rule (78/48).
- Phase reorder per LB-184/185 honored: prior gold zip copied to `/tmp/prior-gold.zip`, then deleted from FUSE exports BEFORE splice of data-clean blobs. Zero FUSE quota fire-drills.

## Pre-existing carries (NOT introduced this bite)
5 Sabah duplicate route_ids; 3,025 global orphan bp- endpoint routes (LB-180 global sweep needed); 2 Wakatobi POI dups; Oman / Philippines cluster anchor orphans; 4 HARD endpoint-label flags (Philippines + UAE); `atlas-external/content_store/navier-content.db` absent.
