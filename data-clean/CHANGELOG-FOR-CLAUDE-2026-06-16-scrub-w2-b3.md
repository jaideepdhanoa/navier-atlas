# CHANGELOG — Gold #79o — Wave 2 bite 3 scrub+enrich splice+seal (2026-06-16)

**Bite scope:** Caribbean — Aruba/Curaçao/Bonaire (ABC) + Cancun/Riviera Maya/Mexico + Cartagena/Colombia.
Counterpart to staged delta from `navier-scrub-enrich-wave` subagent (`/tmp/scrub-wave-2-bite3/`). Sealed by `navier-scrub-wave-splice-seal` worker.
**Wave 2 (Caribbean) COMPLETE** with this bite.

## Counts (Gold #79n → #79o)

- **Routes:** 5,438 → 5,405 (Δ −33 = −51 orphan-endpoint kills + 18 aspirational Caribbean ferry mints).
- **POIs:** 11,192 → 11,163 (Δ −29 = −35 OSM-noise BPs + 6 marquee enrich BPs).
- **Cities:** 170 → 170 (no new anchor mint — coverage already adequate after bites 1+2).
- **Clusters:** 85 → 85 (no greenfield this bite; LB-174 re-anchor sweep applied — 3 single-metro clusters re-anchored).
- **Sidecar `economics_by_route_id.json`:** 82 records / 44 pending — unchanged vs #79n.

## Kills (35 BPs, 51 routes)

- **Aruba/Curaçao/Bonaire:** 10 BPs (Harbour Town Bar, Harbor Square Arena Aruba, Aru-bean Coffeehouse, Harbor View Curacao, Zakitó Welcome mural, …).
- **Cancun/Riviera Maya/Mexico:** 11 BPs (Fashion Harbour, SLS Harbour Novo Cancún condo, Taqueria Marina, Lavandería Marina, Condominium Marina Mia, …).
- **Cartagena/Colombia:** 14 BPs (Cartagena Castillo Grande Hospital, Parque de la Marina, Edificio Cabrero Marina Club, Conjunto Residencial La Marina, Hop On Hop Off Cartagena, …).
- **51 orphan-endpoint routes** killed across all 3 metros (classic LB-180 auto-permutation residue: from_node/to_node bp-* IDs absent from POIs).

## Enrich (6 BPs, 18 routes, LB-174 re-anchor sweep)

- **New BPs:** bp-pdc-muelle-fiscal, bp-holbox-puerto, bp-cartagena-bocachica, bp-san-bernardo-mucura, bp-klein-curacao-pier, bp-klein-bonaire-pier.
- **New routes:** 18 (15 Pioneer II + 3 Quanta-LR). Longest mint = Cartagena ↔ Santa Marta ≈ 100 nm (Quanta-LR; within Q-LR 700 nm cap).
- **Aruba ↔ Curaçao:** ≈ 70 nm cruise-terminal-to-terminal (Quanta-LR; aspirational long Pioneer leg per payload).
- **LB-174 cluster re-anchor sweep (3 single-metro clusters):**
  - `abc-islands` → `bp-1acf06c512` (Curaçao Cruise Terminal).
  - `colombia` → `bp-899770a893` (Cruise Terminal Pier 3 Cartagena).
  - `mexico` → `bp-3e82d54830` (Marina Vallarta — real BP replaces city_id `anchor_source`; completes 1 of 13 LB-174 audit candidates; PV BP touched opportunistically though PV not in bite scope).
- **LB-174 audit candidates remaining:** 13 → 10.

## Wave 2 Caribbean — wave-level totals (bites 1 + 2 + 3)

- **Total BP kills (Caribbean):** ~118 BPs across 3 bites (bite 1 ≈ 56, bite 2 ≈ 27, bite 3 = 35).
- **Total new BPs (Caribbean enrich):** ~28 BPs (bite 1 = 9, bite 2 = 13, bite 3 = 6).
- **Total new routes (Caribbean enrich):** ~77 routes (bite 1 = 28, bite 2 = 31, bite 3 = 18).
- **Caribbean noise ceiling confirmed:** ≈ 30% (Cartagena highest single-metro). Permanent `METRO_BBOX` Caribbean block needed in `gate_osm_noise_bp.py`.
- **Cumulative new operator/brand rescue tokens:** 14 (b1) + 13 (b2) + 12 (b3) = **39 RESCUE_PHRASES** for permanent promotion.

## Gates (all PASS per wave-subagent manifest)

| Gate | Result |
|---|---|
| `gate_endpoint_labels.py` | PASS — 0 hard FLAG (report empty) |
| `gate_city_ids.py` | PASS — 205 valid nodes / 5,405 routes / 85 clusters |
| `gate_partner_rationale_leak.py` | clean across `partner-pitch/partners/*.json` |
| `gate_osm_noise_bp.py` advisory on 3 bite metros | 0 NEW flags (26 advisory carries are pre-existing baseline Hurghada/Aqaba) |
| `gate_premint_pair.py` | **0 / 5,405 routes flagged** — 4th consecutive 0-flag at scale; LB-179 patch ship now CRITICAL priority |
| LB-175a pre-build (ROUTES ≥ floor 5,072 + pier-coord verify all 6 new BPs) | PASS — max new-route 100 nm < Q-LR 700 nm cap |
| `datastore_audit.py` post-seal | PASS — 0 fail / 0 warn (DUAL-SEAL-WRITE LB-182 applied; LB-152 flat-shape overwrite per LB-183) |
| Internal SEAL consistency | PASS — `blobs.FEATURES_BY_TYPE.{poi,city,priority_city}` flat + nested overwritten per LB-183 |

## LB refs applied this bite

LB-174 (cluster re-anchor), LB-175a (pre-build), LB-176c/d/e/f (triangulation), LB-179 (name-veto-before-bp_type-rescue — inline; patch ship CRITICAL), LB-180 (orphan-endpoint route kill), LB-181 (street-intersection regex), LB-182 (DUAL-SEAL-WRITE + gate_poi_dedup), LB-183 (captive-marquee rescue + Harbour-View regex + flat+nested SEAL overwrite), **LB-184** (this entry).

## Learnings captured (see `_scrub-enrich-learnings.md` LB-184 section)

- Caribbean 30% noise ceiling confirmed → permanent METRO_BBOX block.
- Caribbean-condo macro-regex `(Edificio|Conjunto Residencial|Condominio)\s+(Marina|Harbour)` → permanent NOISE_STRONG.
- SEO yacht-charter multi-pipe pattern `r'\|.+\|'` → NOISE_REGEX_PATTERN promotion.
- Captive tourist-landmark tokens (Sign|Mural|Welcome|Statue) → permanent NOISE_STRONG.
- LB-174 multi-city cluster re-anchor pattern (cluster can be re-anchored independent of bite-scope city — e.g. mexico cluster from PV BP though bite scope is Cancun/RM).
- LB-179 classifier patch ship now CRITICAL — 4 consecutive bites of inline application.
- 4 unpromoted learning blocks since last PROMOTION NOTE — promotion fires per protocol.
- 12 new operator brand-rescue tokens this bite (Ultramar, Winjet, Magna, Mexico Waterjets, Holbox Express, Aquatours, Bonaire Express, Caribbean Speed, Olondo, Tornamesa, Bocachica Ferry, Cartagena Tours) → promote to RESCUE_PHRASES.

## Notes

- **DUAL-SEAL-WRITE (LB-182) + LB-152 flat-shape overwrite (LB-183)** BOTH applied: `blobs.FEATURES_BY_TYPE.{city,poi,priority_city}` flat keys overwritten (not merged) on SEAL recompute.
- **FUSE quota:** prior gold zip deleted BEFORE cp new (LB-182 standing rule honored; pre-copied to `/tmp/prior-gold.zip` to retain extraction base).
- **Wave 2 (Caribbean) COMPLETE.** Next: Wave 3 per parent orchestration.
- **Pre-existing carries** (NOT introduced this bite): Oman cluster anchor orphan `bp-095a41dfcb`, Philippines cluster anchor orphan `bp-d4738f6ad2`, Wakatobi duplicate POIs — schedule re-anchor in upcoming bite.

## Follow-ups (carried, non-blocking)

- **LB-179 classifier patch — CRITICAL after Wave 2 complete** (5 consecutive bites of inline name-veto application).
- LB-180 `gate_premint_pair.py` BP-existence-in-POIs check codification.
- LB-181 `harbour pointe` NOISE_STRONG + street-intersection regex codification.
- `_tools/scrub_route_label_kills.py` promotion from inline.
- `datastore_audit.py --data-clean-dir` flag.
- LB-182 `gate_poi_dedup.py` promotion to standing seal gate.
- Standing rule: orphan parent_city_id audit on every scrub-enrich bite.
- Permanent Caribbean `METRO_BBOX` block in `gate_osm_noise_bp.py`.
- Permanent MARINE_TERMS promotion for 14 (b1) + 13 (b2) + 12 (b3) = **39 new operator/brand rescue tokens** Caribbean-wide.
- `classify_marine_bp.py` captive-marquee rescue pattern promotion (LB-183 carry).
- `noise_toponym_view` Caribbean regex promotion (LB-183 carry).
- SEAL recompute script standardization — overwrite (not merge) `blobs.FEATURES_BY_TYPE` flat shape per LB-152/183.
- LB-174 sweep: 10 audit candidates remaining; continue opportunistic each bite.
