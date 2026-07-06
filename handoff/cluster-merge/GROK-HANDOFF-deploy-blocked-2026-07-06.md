# GROK HANDOFF — cluster-merge + curation DONE · deploy blocked §3.7

**Date:** 2026-07-06  
**Commit:** `7eafcd98` on `main`  
**Seal:** `#cluster-merge-curation-2026-07-06`  
**Production:** not updated (live atlas still ~467 routes; git has 6414)

---

## Cascade complete (acceptance met)

| Item | Result |
|------|--------|
| Clusters | 109 → **106** (retired: `uae-east-coast`, `dammam-eastern-province-ksa`, `ksa-commercial`) |
| Routes | 6883 → **6414** (−469 net) |
| Route rebinds | **286** (190 + 10 + 86) |
| Residual retired `cluster_id` refs | **0** |
| Dedupe | **465** edges / **288** berth-pairs (+ 4 self-berth drops) |
| Sovereign suppression | **99** tagged; **8** single-sovereign trunks kept; **0** intra-sovereign leaks on Bolt KSA commercial render |
| Norway (corrected spec `46bc2714`) | **84** live; global + Uber ✓; Yango `registry_keys` has no `norway` ✓ |
| UAE market group | `{uae}` only |
| Gates clean | linkage **0** · scope drift **0** · taxonomy restamp **0** · exclusion sweep **0** · Bolt §3.7 **PASS** |

**Receipts**

- `grok-routing-output/cluster-merge-curation-report.json`
- `handoff/CLUSTER-MERGE-CURATION-2026-07-06.json`
- Specs: `handoff/cluster-merge/GROK-SPEC-cluster-merge-2026-07-06.md`, `GROK-SPEC-render-curation-2026-07-06.md`

Restore `18f6e0e9` confirmed landed (6414 routes, Taiwan back, Singapore 196, Abu Dhabi 199).

**Commits on main (cascade stack)**

| SHA | Description |
|-----|-------------|
| `15811a96` | Cluster merge + curation cascade |
| `ce1c6b8c` | Scrub exclusion-sweep blocker from CLUSTERS merge seals |
| `dc5c9473` | Post-dedupe route linkage rebinding |
| `077b4ca8` | Clear careem/noon `cluster_city_ids` (scope drift) |
| `7eafcd98` | Bolt Tallinn→Viimsi journey rebound after dedupe |

---

## Deploy status

`RELEASE=1 ./scripts/deploy.sh` **aborts at §3.7 proposal fidelity** — not merge-related. Build-site and all other preflight gates pass on `7eafcd98`.

---

## Tasklet ask: §3.7 fidelity burn-down (8 hub partners)

### What §3.7 is

`deploy.sh` runs a pre-flight checklist before Vercel push. **§3.7 proposal fidelity** runs:

```bash
python3 scripts/audit_proposal_fidelity.py --all-partners --strict-deploy-gate
```

Under `RELEASE=1`, any hub-layout or reference partner that is not a clean **PASS** aborts deploy. This gate checks partner-pitch JSON consistency (journey cards ↔ `route_id`, distance honesty, geometry flags) — **not** routes/clusters/CLUSTERS.json.

Common failure modes:

- Journey card labels don't match bound route endpoints (e.g. Tallinn→Viimsi card pointed at Pirita route — fixed for Bolt in `7eafcd98`)
- Card `distance_nm` doesn't match route geometry → TRIM / PASS_WITH_FLAGS
- Too many broken bindings or geometry mismatches → REWRITE

### Failing partners (pre-existing; not introduced by cluster merge)

| Partner | Verdict / issue |
|---------|-----------------|
| `airasia-move` | PASS_WITH_FLAGS — geom=4 |
| `caribbean` | PASS_WITH_FLAGS — geom=12 |
| `centara-thailand` | PASS_WITH_FLAGS — geom=3 |
| `grab-thailand` | PASS_WITH_FLAGS — geom=4 |
| `line-man-wongnai` | PASS_WITH_FLAGS — geom=4 |
| `yassir` | PASS_WITH_FLAGS — geom=3 |
| `freenow` | REWRITE — journey_bp=2, geom=1 |
| `minor-hotels` | REWRITE — journey_bp=32 |

**Reference:** `handoff/partner-map-model/TASKLET-FIDELITY-DEBT-MANIFEST.json`  
**Per-partner detail:** `handoff/partner-map-model/PROPOSAL-FIDELITY-<partner>.json` + `.md`

**Likely fix pattern (Bolt already done):** post-dedupe canonical `route_id`s changed; journey/featured cards still reference dropped IDs or have distance mismatch. Rebind cards to surviving routes or trim broken entries.

### Acceptance for Grok re-deploy

1. All 8 partners → **PASS** (no PASS_WITH_FLAGS, no REWRITE) on `--strict-deploy-gate` (exit 0)
2. Tasklet pushes fixes to `main`
3. Grok runs `RELEASE=1 ./scripts/deploy.sh`
4. Spot-check: one UAE chip + one Saudi Arabia chip; Fujairah + Dammam corridors render; Norway on global+Uber, absent from Yango surfaces

---

## Deferred (non-blocking)

- `/bolt/ksa-commercial` market slug retained (scope = `saudi-arabia`)
- 2 residual `_corridor_market` metadata keys on routes (`bolt-ksa-commercial`, `yango-ksa-commercial`)
- Jaideep call pending: further sovereign curation on `/bolt` KSA commercial render (suppression active; 0 leaks today)

---

## Sovereign render note (Jaideep)

`saudi-arabia` now co-houses sovereign PIF assets + commercial cities. Bolt inherits KSA scope; **99** pure intra-giga corridors suppressed on commercial render; **8** single-sovereign trunks kept. Full render remains on RSG/PIF decks. No further curation until Jaideep directs.