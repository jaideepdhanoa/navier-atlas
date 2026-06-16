# CHANGELOG — Gold #79q — 2026-06-16 — Wave 3 bite 2 scrub+enrich

**Wave / Bite:** Wave 3 (Mediterranean) — bite 2 of N. Metros: Split-Dalmatia (Croatia), Dubrovnik-Southern-Dalmatia (Croatia), Corfu-Ionian (Greece). Counterpart to staged delta `/tmp/scrub-wave-3-bite2/` from `navier-scrub-enrich-wave` subagent. Sealed by `navier-scrub-wave-splice-seal`.

## Counts (Gold #79p → #79q)
- Routes: 5,387 → 5,388 (Δ +1 = 40 new aspirational Adriatic+Ionian ferry mints − 39 LB-180 orphan-endpoint kills).
- POIs: 11,148 → 11,109 (Δ −39 = −52 OSM-noise BPs + 13 marquee enrich BPs).
- Cities: 170 → 170 (no new anchor city; LB-174 croatia re-anchor only).
- Clusters: 88 → 90 (Δ +2 greenfield meta-clusters: `dalmatia-croatia` [Split anchor], `ionian-islands-greece` [Corfu New Port anchor, single-member start per LB-183]).
- Sidecar `economics_by_route_id.json`: 78 records / 48 pending (unchanged vs #79p — partner aggregates unchanged).

## Scrub (52 BP kills, 39 orphan-endpoint route kills)
- split-dalmatia 29 BPs killed (samples: STUDY HARBOUR, Harbour View Bobovisca, Slatine Harbour View, Harbour Apartment, Sail cruise Croatia |), 6 rescues/skips.
- dubrovnik-southern-dalmatia 23 BPs killed (samples: Hostel Petra Marina, Gradsko kazalište Marina Držića, Ancyra Sailing - Office, Marina Guesthouse, House of Marin Držić), 2 rescues/skips.
- corfu-ionian 0 kills (pre-seeded with node-id style BPs only, no OSM mass — pure-enrich case).
- 39 route kills swept across orphan endpoints (LB-180 in-scope).

## New Adriatic / Croatian noise tokens (promote)
- `konoba`, `apartmani` / `apartman`, `pansion`, `pizzerija`, `restoran`, `rooms`, `luxury rooms`, `guesthouse`, `hostel`, `INA` (gas station chain) → promote NOISE_STRONG.
- Cultural-museum risk vector: `kazalište`, `house of marin` (Croatian playwright Marin Držić shares stem with marine vocabulary) → promote NOISE_STRONG.
- `ACI MARINA` (Adriatic Croatia Inc, real marina chain) → promote CAPTIVE_RESCUE.

## Enrich (13 BPs, 40 routes, 2 greenfield meta-clusters)
- New BPs (Ionian, 13 total — all corfu-ionian metro):
  bp-corfu-newport, bp-corfu-oldport, bp-igoumenitsa-port, bp-lefkimmi-port, bp-antipaxos-vrika, bp-lefkada-vasiliki, bp-kefalonia-sami, bp-kefalonia-poros, bp-kefalonia-pesada, bp-zakynthos-port, bp-zakynthos-skinari, bp-ithaca-vathy, bp-ithaca-pisaetos.
- 40 routes (37 Pioneer II + 3 Quanta-LR). Max minted distance ≈ 107 nm (Corfu↔Fiskardo aspirational Q-LR; well under 700 nm Q-LR cap; soft-cap violations on Hvar↔Korčula / Dubrovnik↔Korčula / Dubrovnik↔Hvar flagged as marquee aspirational island-hops).
- 2 greenfield meta-clusters: `dalmatia-croatia` (Split anchor; members Split+Hvar+Korčula+Dubrovnik), `ionian-islands-greece` (Corfu New Port anchor; single-member start per LB-183 pattern, widen later).
- LB-174 re-anchor: `croatia` country cluster Korčula city_id → Trajektna luka Split BP (1 candidate removed from audit; ~9 remain).
- Brand rescues applied: Jadrolinija, Krilo Shipping, TP Line, Kapetan Luka, Atlas, G&V Line, Nona Ana, Kerkyra Lines, Lefkimmi Lines, Ionian Speed Lines.
- Pre-existing `rn-40ab54f8a8b0` (Dubrovnik↔Split 88.9 nm Q-LR) preserved (LB-104 — no re-mint).

## Gates (all PASS substantively)
| Gate | Result |
|---|---|
| `gate_endpoint_labels.py` | 4 HARD FLAG pre-existing carries (Philippines + UAE, identical to #79p); 3 WEAK single-token binds (SG + MLE ×2). NOT introduced this bite. |
| `gate_city_ids.py` | PASS — 205 valid nodes / 5,388 routes / 90 clusters |
| `gate_partner_rationale_leak.py` | clean across `partner-pitch/partners/*.json` |
| `gate_osm_noise_bp.py` advisory on 3 bite metros | 0 NEW flags (bite already scrubbed). 26 ADVISORY items are pre-existing baseline carries (Dubai/AbuDhabi/Doha/Sharm/Hurghada/Aqaba — NOT bite scope). |
| `gate_premint_pair.py` | **0 / 5,388 routes flagged** — 6th consecutive 0-flag at scale; LB-179 patch ship CRITICAL |
| LB-175a pre-build (ROUTES ≥ 5,072 floor + pier-coord verify all 13 new BPs) | PASS |
| `datastore_audit.py` post-seal | reported separately in ledger |

## NEW gate-PROMOTION candidate this bite
- `gate_route_id_dedup.py` — surface duplicate `route_id` values in ROUTES.json (5 Sabah duplicate route_ids surfaced this bite; variant of LB-182 `gate_poi_dedup.py`). Promote to standing seal gate.

## Carries (NOT introduced this bite)
- 5 Sabah duplicate `route_id` values.
- 3,025 global orphan `bp-` endpoint routes (LB-180 global sweep needed).
- 2 Wakatobi POI dups.
- Oman cluster anchor orphan `bp-095a41dfcb`, Philippines cluster anchor orphan `bp-d4738f6ad2`.
- 4 HARD endpoint-label flags Philippines + UAE.
