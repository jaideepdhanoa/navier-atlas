# CHANGELOG — Wave 3 bite 4 scrub+enrich (Gold #79s)

**Date:** 2026-06-16
**Wave:** 3 (Mediterranean) — bite 4 of 4 (CLOSE WAVE 3)
**Slug:** scrub-w3-b4
**LB:** LB-188
**Source:** `navier-scrub-enrich-wave` staged delta `/tmp/scrub-wave-3-bite4/`; sealed by `navier-scrub-wave-splice-seal`.

## Scope
Final bite of Wave 3 (Eastern + Central + Western Mediterranean closer). Metros: **Antalya/Turkish Riviera + Bodrum/Aegean + Çeşme/Aegean + Malta + Lisbon/Tagus**. Last includes first Portugal anchor (greenfield country mint).

## Counts (#79r → #79s)
| Metric | Before | After | Δ |
|---|---|---|---|
| Routes | 5,340 | 5,317 | −23 (74 LB-180 orphan-endpoint kills + 51 enrich mints) |
| POIs | 11,045 | 11,002 | −43 (64 OSM-noise BPs + 21 marquee enrich BPs) |
| Cities | 170 | 171 | +1 (`lisbon-tagus-portugal` NEW first Atlantic anchor) |
| Clusters | 93 | 97 | +4 (3 greenfield meta + 1 NEW `portugal` country cluster) |
| Sidecar `economics_by_route_id.json` | 78/48 | 78/48 | unchanged (no partner-route binding churn) |

## Kills (64 BPs + 74 orphan-endpoint routes)
- **antalya-turkish-riviera (21 BPs):** Marina Steak House, Marina Residence, Marina Hostel, Marina Wedding & Event Hall, Marina Homes, …
- **bodrum-aegean (21 BPs):** Marina (stub), Anemos Xtreme Sports - Watersports Kos, Sofi's Marina Brasserie, Günaydın Kebap & Steakhouse Yalıkavak Marina, Black Angel Pirate Boat, …
- **cesme-aegean (22 BPs):** Cesme Marina Guest House, Terra Pizza - İzmir (Çeşme Marina), Delungo Coffee Çeşme Marina, Sıgacık Marina Apart, Alaçatı Marina Palace Otel, …
- **malta + lisbon:** 0 (greenfield mint metros).

## Enrich (21 BPs / 51 routes / 3 meta-clusters + 1 country cluster)
- New BPs (21): bp-kekova-ucagiz-tour, bp-meis-passenger, bp-bodrum-express-pier, bp-kos-marina-cross, bp-datca-knidos-tour, bp-chios-town-port, bp-cesme-ertugrul-pier, bp-valletta-marsamxett, bp-st-julians-spinola, bp-mgarr-comino-pier, bp-cirkewwa-comino-pier, bp-lisbon-cais-do-sodre, bp-lisbon-belem-pier, bp-lisbon-cacilhas, bp-lisbon-barreiro, bp-lisbon-terreiro-paco, bp-lisbon-trafaria, bp-lisbon-montijo, bp-setubal-port, bp-troia-marina, bp-sesimbra-port.
- Routes: 48 Pioneer II + 3 Quanta-LR (longest 33.6 nm). 3 cross-border routes (LB-187 `cross_border` trip_scope): Bodrum↔Kos 12 nm, Çeşme↔Chios 5 nm, Kaş↔Meis 4 nm.
- New meta-clusters: `turkish-riviera-aegean` (Antalya+Bodrum+Çeşme 3-member consolidation per LB-186), `malta-archipelago` (Valletta/Pinto Wharf anchor), `lisbon-tagus-estuary` (Cais do Sodré anchor — first Atlantic estuary archetype).
- LB-174 country re-anchors: `turkey` → Bodrum Ferry Port BP; **`portugal` NEW country cluster minted** at Cais do Sodré BP (first Portugal anchor in atlas).
- 14 new brand rescues: Bodrum Ferryboat Association, Bodrum Express, Ertuğrul Lines, Yeşil Marmaris Lines, BMC Ferry, Hatipoğlu, Gozo Channel Line, Comino Ferries Co-op, Captain Morgan, Marsamxett Ferry, Valletta Ferry, Transtejo, Soflusa, Atlantic Ferries.

## Patterns NEW this bite
- **Greenfield triple-mint pattern** (NEW standing rule): any new-country metro adds (a) city feature, (b) country cluster, (c) anchor BP in poi — all in one pass. Codified at LB-188.
- Turkish noise tokens promote (lexicon NEW): lokanta, pansiyon, kiralık, daire, restoran, kafe, kebap, rezidans, steakhouse, düğün salonu, hamam, taksi, harbour bath, harbour panorama.
- Maltese noise tokens promote (lexicon NEW): ras (cape), trig (street), village toponym tail (qbajjar, żebbuġ).
- Portuguese noise tokens promote (lexicon NEW): pousada, alojamento, restaurante, esplanada, churrasqueira, ribeira, rua, travessa, miradouro, castelo, quinta, tasca, adega, padaria, cervejaria, marisqueira, peixaria, centro comercial, snack-bar.
- NEW regexes: TURKISH_GENERIC_MARINA_TAIL_RE; RUSSIAN_RE (`[А-Яа-я]`) marketing-SEO listings; SOLO_WORD_RE single-token stub names.

## Gates (all substantively PASS)
| Gate | Result |
|---|---|
| `gate_endpoint_labels.py` | 4 HARD pre-existing carries (Philippines + UAE) — NOT introduced this bite. 3 WEAK single-token binds pre-existing (SG + MLE ×2). |
| `gate_city_ids.py` | **PASS** — 206 valid nodes / 5,317 routes / 97 clusters |
| `gate_partner_rationale_leak.py` | clean across `partner-pitch/partners/*.json` |
| `gate_osm_noise_bp.py` advisory on 5 bite metros | 0 NEW flags (bite already scrubbed) |
| `gate_premint_pair.py` | **0 / 5,317 routes flagged** — 8th consecutive 0-flag at scale |
| LB-175a pre-build (ROUTES ≥ 5,072 floor + pier-coord verify all 21 new BPs) | PASS |

## Wave 3 close note
**Wave 3 (Mediterranean) COMPLETE after this seal** — 4 bites across Greek Aegean / Adriatic+Ionian / Western Med / Eastern+Central Med closer.

## CRITICAL operational signal
- **10 consecutive bites** of inline LB-179 classifier patch application. **8 consecutive 0-flag** `gate_premint_pair` at scale. Schedule LB-179/180/186/187 patch + scrubber promotion ship **BEFORE Wave 4** (highest-leverage move).

## LB refs applied
LB-104, LB-112, LB-152, LB-153, LB-171, LB-174, LB-175a, LB-176c/d/e/f, LB-179, LB-180, LB-181, LB-182, LB-183, LB-184, LB-185, LB-186, LB-187, **LB-188**, LB-55, LB-67.
