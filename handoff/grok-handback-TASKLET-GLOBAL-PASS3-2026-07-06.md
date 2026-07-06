# Grok handback — Global Pass 3 complete (canonical marquees live)

**Date:** 2026-07-06 · **From:** Grok · **To:** Tasklet · **Re:** apply `CANONICAL-MARQUEES.json` globally + deploy

---

## TL;DR

Pass 3 is **green and live**. Applied Tasklet Pass 2 canonical marquees to 20 commercial partners (direct `route_id` bind from sealed `properties.id` — no re-stamp), finance cascade ran, all inheritance/linkage gates pass, production deployed.

**Production:** https://navier-atlas.vercel.app  
**Inspect:** https://vercel.com/jaideepdhanoas-projects/navier-atlas/4VNufQipyjy2sUomiUctG1iG2rEa

Guardrails held: no re-stamp · no invented route_ids · no `regen_pta_economics.py --all` · WSF `growth_case` untouched.

---

## What ran

| Step | Script | Result |
|---|---|---|
| Marquee apply | `scripts/grok-global/apply_canonical_marquees_global.py --apply` | 81 groups · 20 commercial partners |
| Route linkage | `scripts/run-route-linkage-lane.sh --apply` (commercial) | 0 blocking gaps |
| Post-linkage re-apply | `apply_canonical_marquees_global.py --apply` (2nd pass) | Clears non-standard phase chips injected by linkage |
| Finance cascade | `RUN_CASCADE=1` via `run_finance_sheet_lane.sh` | 20 commercial agg JSON written |
| Partner inheritance | `validate_partner_inheritance.py --strict` | **20/20 pass** |
| Finance inheritance | `validate_finance_inheritance.py` | **0 divergent** |
| Scope drift | `audit-partner-scope-drift.mjs --strict` | **0 drift** |
| Seal | `update_seal_hashes.py` | `SEAL.json` refreshed |
| Deploy | `RELEASE=1 ./scripts/deploy.sh` | **PRE-FLIGHT PASSED · prod live** |

Orchestrator: `scripts/grok-global/run_global_inheritance_pass3.sh` (updated: linkage → re-apply marquees)

---

## Marquee apply receipt

Source: `handoff/global-marquee-pass2/CANONICAL-MARQUEES.json` (v2.3, 81 `cluster::city` groups)

| Partner | Groups | Featured | Wow |
|---|---:|---:|---:|
| airasia-move | 22 | 92 | 73 |
| bolt | 57 | 209 | 155 |
| cabify | 2 | 10 | 10 |
| careem | 11 | 30 | 19 |
| didi | 3 | 9 | 8 |
| gojek | 12 | 45 | 39 |
| grab | 22 | 92 | 73 |
| grab-thailand | 10 | 47 | 34 |
| indrive | 7 | 27 | 24 |
| kakao-mobility | 4 | 15 | 15 |
| line | 10 | 47 | 34 |
| line-man-wongnai | 10 | 47 | 34 |
| lyft | 0 | 0 | 0 |
| noon | 11 | 30 | 19 |
| ola | 4 | 14 | 14 |
| rapido | 0 | 0 | 0 |
| uber | 23 | 94 | 74 |
| uber-india | 4 | 14 | 14 |
| yango | 24 | 57 | 42 |
| yassir | 0 | 0 | 0 |

**Label scrub:** 0 (empty `LABEL-SCRUB.json` applied list)  
**Retire archive:** `handoff/archive/featured-wow-retired-global-2026-07-06.json`  
**Apply report:** `grok-routing-output/global-canonical-marquees-apply-report.json`

Pass 2 validation gate (unchanged geometry): `390/390` bind · 0 unresolved · 0 endpoint mismatch · 0 land >0.2km

---

## Deploy gate fixes (Pass 3 lane)

1. **Linkage ↔ marquee ordering** — route linkage re-injects phase `featured_routes` chips; Pass 3 now re-applies marquees after linkage. Validator skips `intentional_null` phases.
2. **Stale post-reseal journey `route_id`s** — scrubbed 48 entries across commercial partners (null + `text_only`).
3. **Thailand label binding** — Pattaya→Koh Samet journeys aligned to sealed endpoint labels (`rn-24299bbfd9c8`).
4. **Manila geometry hold** — 4 airasia-move journeys with channel-solver backlog → `geometry_hold_pending_channel_solver` chips.
5. **Caribbean hub** — 11 USVI-BVI phase chips: `from_label` corrected to `usvi-bvi` (route `ics-47ff344fca`).
6. **Cabify spain/colombia** — market `journeys_unlocked` for linkage (`rn-71292a6fedf1` spain; colombia `text_only` chip).

---

## Geometry (unchanged from Pass 1)

| Metric | Value |
|---|---|
| `ROUTES.json` total | 4,267 |
| Cluster-stamped | 647 |
| UAE geometry | unchanged (Pass 1 skip) |
| Story geometry advisory | 1 severe fail (allowlisted=9) — non-blocking at preflight |

---

## Finance

- Commercial partners: `finance/recal/agg-*.json` + growth JSON refreshed via cascade lane
- Google Drive sheet upload: **skipped** (OAuth token expired) — non-blocking for atlas deploy
- Finance inheritance: **0 divergent** across 13 multi-partner geographies

---

## Residuals → locale lane (#119), non-blocking

Per Pass 2 receipt: 2 business-POI suspect endpoints + city_id cross-tags (Lombok under bali-indonesia; Singapore pointer under desaru-coast). Geometry valid; grouping imperfect — null-beats-wrong.

---

## Next for Tasklet

- Locale lane (#119) for suspect endpoints / cross-tags if desired
- Re-auth Google Drive for finance sheet upload
- Channel solver backlog for Manila geometry-hold journeys