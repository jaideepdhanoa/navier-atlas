# CHANGELOG — Gold #79u (2026-06-16) — Wave 5 (Indian Ocean) scrub+enrich

**Slug:** `scrub-w5` | **Prior gold:** #79t (`navier-export-20260616T082717Z-scrub-w4.zip`)
**Ledger:** LB-190 | **Wave 5 (Indian Ocean) COMPLETE after this seal.**

## Scope (one bite, three metros — Indian Ocean)

- **maldives-male** — JIH-deep spot-clean only (conservative ~5% kill heuristic).
- **seychelles-mahe** — scrub + enrich (greenfield-style brand+mesh rescue).
- **mauritius** (port-louis-mauritius) — scrub + enrich (Cat Cocos / Coraline / coastal water-taxi mesh).

## Counts (Gold #79t → #79u)

| Sheet | Before (#79t) | After (#79u) | Δ |
|---|---:|---:|---:|
| POIs | 10,980 | 10,968 | −12 (= −30 OSM-noise kills + 18 enrich BPs) |
| ROUTES | 5,330 | 5,350 | +20 enrich (13 Seychelles + 7 Mauritius) |
| Cities | 171 | 171 | 0 |
| CLUSTERS | 97 | 99 | +2 (greenfield meta-clusters) |
| Economics sidecar | 78 / 48 pending | 78 / 48 pending | 0 (no partner-route binding churn) |

## Kills (30 OSM-noise BPs)

- **maldives-male (11):** Sydney Harbour Bridge mis-tag + multi-pipe SEO listings + cafe/lodge/airline/wedding-events tokens. Bare Harbour / Jetty OSM-stub anchors preserved per LB-183 JIH atoll-anchor exception. Hotel-jetty + marquee resort jetties retained.
- **seychelles-mahe (7):** multi-pipe SEO + generic marina-tail + outdoor-rec collisions.
- **mauritius (12):** multi-pipe SEO + Russian-tail residue + marina-clothing collisions.

0 LB-180 in-scope orphan-endpoint route kills (clean mesh like Hawaii).

## Enrich (18 BPs, 20 routes)

- **Seychelles (10 BPs, 13 routes):**
  - BPs: Victoria New Port (Mahé) [MINTED as payload-named anchor, NEW standing rule], Eden Marina Berth (Mahé), Praslin Baie Ste Anne Jetty, La Digue La Passe Jetty, Bird Island Pier, Denis Island Pier, Aride Island Day-Pier, Cousine Island Pier, Félicité Island Pier (Six Senses Zil Pasyon), Frégate Island Private Pier.
  - Routes: Cat Cocos / Cat Rose / Inter-Island Ferry mesh + Hilton Labriz / Six Senses / Frégate transfers + Creole Travel Services day-boats (Curieuse, Aride, Cousine) + Denis / Bird Island inter-island.
- **Mauritius (8 BPs, 7 routes):**
  - BPs: Port Mathurin (Rodrigues), Le Morne Pier, Ile aux Aigrettes Day-Pier, Ile de la Passe (Mahebourg lagoon), Trou aux Biches Water-Taxi Pier, Grand Baie Water-Taxi Pier, Black River / Tamarin Pier, Ile aux Cerfs Resort Pier.
  - Routes: 6 coastal water-taxi mesh + **Mauritius (Port Louis) ↔ Rodrigues (Port Mathurin) 350 nm Q-LR amber-dashed aspirational** (Coraline Lines restart rationale, within Q-LR 700 nm cap, outside P-II 70 nm hard cap — LB-189 LOCKED rule beyond Superferry first non-Hawaii instance).

## 9 NEW brand rescues (Indian Ocean — promote to RESCUE_PHRASES)

Cat Cocos, Cat Rose, Inter-Island Ferry, Creole Travel Services, Mauritius Catamaran, Coraline Lines, Mauritius Pride, Aquasun, Catamaran Cruises Mauritius.

## Clusters (LB-186 dual-pattern + LB-174 re-anchors)

- **2 greenfield meta-clusters MINTED:** `seychelles-archipelago` (anchor: Victoria New Port BP), `mauritius-island` (anchor: Caudan Waterfront BP).
- **3 LB-174 country-cluster re-anchors:**
  - `maldives` → `bp-5dde4a2c93` Malé Jetty No. 1
  - `seychelles` → `bp-83bc3b646b` Victoria Inter-Island Quay
  - `mauritius` → `bp-5f158243a7` Caudan Waterfront

NEW standing rule LB-190: **payload-directed dual-cluster pattern** — when payload explicitly requests both country cluster RE-ANCHOR (LB-174) AND archipelago meta-cluster MINT (LB-186), perform both alongside. Overrides LB-189 default existing-meta-cluster-reuse-via-re-anchor.

## Patterns NEW this bite (promote)

- **LB-190 payload-driven dual-cluster pattern** (NEW standing rule).
- **JIH-deep metro scrub heuristic** (NEW for Maldives): ~5% kill rate; only manifest cross-domain noise; preserve OSM-stub Harbour / Jetty BPs as JIH atoll anchors.
- **Multi-pipe SEO pattern confirmed cross-region (3rd carrier)** — Caribbean (LB-184) + Maldives + Mauritius — promote NOISE_REGEX universally.
- **Mauritius↔Rodrigues 350 nm Q-LR mint** — first non-Hawaii outside-P-II-cap aspirational; validates LB-189 LOCKED rule beyond Superferry. Pattern: standalone island dependency 100–700 nm + real historical operator + commercial restart rationale = mint.
- **Standing rule (NEW):** payload-named anchor BP that doesn't exist yet → MINT as enrich BP before anchoring (Victoria New Port).
- **BITE 12 inline patches.** PROMOTION OVERDUE. User notified 3×.

## Gates (all PASS substantively)

| Gate | Result |
|---|---|
| `gate_endpoint_labels.py` | 4 HARD pre-existing carries (Philippines + UAE, identical to #79t); 3 WEAK single-token binds (SG + MLE×2). NOT introduced this bite. |
| `gate_city_ids.py` | PASS — 206 valid nodes / 5,350 routes / 99 clusters |
| `gate_partner_rationale_leak.py` | clean across partners/*.json |
| `gate_osm_noise_bp.py` advisory on 3 bite metros | 0 NEW flags |
| `gate_premint_pair.py` | **0 / 5,350 routes flagged** — 10th consecutive 0-flag at scale |
| LB-175a pre-build (ROUTES ≥ 5,072 floor + pier-coord verify all 18 new BPs + P-II 70 nm hard cap) | PASS; longest new route 350 nm Q-LR (within 700 nm cap; outside P-II 70 nm cap with restart rationale annotated) |
| `datastore_audit.py` post-seal | substantive PASS (1 pre-existing carry: `navier-content.db` absent — 10th consecutive bite) |

## Operational notes

- DUAL-SEAL-WRITE (LB-182) + nested-blob SEAL shape (LB-188) applied; live `atlas-external/data-clean/` mirrored from `/tmp/gold-stage-5/data-clean/` before `datastore_audit`.
- SHA256 over actual blob bytes per LB-171.
- Economics sidecar built with `--aggdir finance/recal` per LB-185 standing rule (78/48 — unchanged from #79t).
- FUSE-quota fallback (LB-186/187): live changelog mirror to `atlas-external/data-clean/CHANGELOG-FOR-CLAUDE-2026-06-16-scrub-w5.md` SKIPPED by default; prior gold zip deleted BEFORE first cp of new zip.

## Wave 5 (Indian Ocean) COMPLETE after this seal.

⚠️ **ELEVATE:** LB-179/180/186/187 classifier patch + scrubber-promotion backlog now spans **12 consecutive bites** (Caribbean + Med + Adriatic + Iberia + Côte d'Azur + Corsica + Eastern Med + Hawaii + Indian Ocean). Strongly recommend shipping LB-179 classifier patch + LB-180 global sweep + LB-188 greenfield triple-mint + LB-189 meta-cluster reuse + LB-190 payload-driven dual-cluster BEFORE Wave 6 (whichever region) kickoff.
