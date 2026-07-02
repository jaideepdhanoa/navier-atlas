# Grok → Tasklet handback — PTA Grok lane complete

**From:** Grok · **Date:** 2026-07-02 · **Status:** Grok lane closed — **zero Grok dependencies for Tasklet**  
**Prior handback:** `handoff/grok-handback-TASKLET-PTA-POST-MERGE-2026-07-02.md` (#150–#161 merged)  
**Living ledger:** `handoff/partner-map-model/PTA-MASTER-PLAN.md`

---

## 1. Executive summary

Grok has finished all seal, economics, geometry-mint, and fidelity work that was blocking Tasklet after the #150–#161 merge. Tasklet can proceed on every remaining PTA item **without waiting on Grok**.

| Lane | Status |
|------|--------|
| Phase B seals + economics (5 partners) | ✅ Complete — all fidelity **PASS** |
| Phase C anchor-ready economics (Kolkata, Helsinki) | ✅ Complete — fidelity **PASS**, `archetype: public_transit` |
| Batch-5 follow-ups (Mumbai, Bahrain) | ✅ Complete — fidelity **PASS** |
| Mint-heavy five geometry mint | ✅ Cities + BPs minted; starter routes partial (see §4) |
| Renderer / `regen_pta_economics.py` | ✅ No further Grok edits required |

---

## 2. What Grok shipped (this lane)

### 2a. Phase B — outside-lane authorities

| Partner | Seal receipt | Economics regen | Fidelity |
|---------|--------------|-----------------|----------|
| `bc-ferries` | `PTA-SEAL-RECEIPT-bc-ferries.json` (7/8 pairs; see note) | ✅ 8 corridors | **PASS** |
| `hawaii` | `PTA-SEAL-RECEIPT-hawaii.json` | ✅ 2 corridors | **PASS** |
| `fullers360` | `PTA-SEAL-RECEIPT-fullers360.json` | ✅ 4 corridors | **PASS** |
| `maldives-government` | `PTA-SEAL-RECEIPT-maldives-government.json` | ✅ 7 corridors | **PASS** |
| `norway-fjords` | `PTA-SEAL-RECEIPT-norway-fjords.json` | ✅ 5 corridors | **PASS** |

**bc-ferries note:** `bcf-d04` (Horseshoe Bay ↔ Departure Bay Nanaimo) remains `geometry_seal_pending` — Georgia Strait land-QA could not pass at `interior_land_km ≤ 0.05`. Partner fidelity is still **PASS** (aspirational chip, null `route_id`). Victoria ↔ Vancouver moved to **phase 2** (53 nm too long for phase-1 beachhead).

All five now have `growth_case` with `_economics_status: pta_regenerated` — intro step 2 public-value panel renders.

### 2b. Phase C — anchor-ready

| Partner | Routes bound | Economics | Fidelity |
|---------|--------------|-----------|----------|
| `kolkata-wbtc` | 5 sealed `rn-` | ✅ 5 corridors | **PASS** |
| `helsinki-hsl` | 7 sealed `rn-` | ✅ 7 corridors | **PASS** |

Both: `archetype: public_transit`, `_public_transit_authority` present, economics live.

### 2c. Batch-5 follow-ups

| Partner | Grok action | Fidelity |
|---------|-------------|----------|
| `mumbai-mmb` | 2 mis-bound corridors remain `geometry_seal_pending` (intentional DROP from #151) | **PASS** |
| `bahrain-motc` | Reef Island ↔ Diyar journey distance fixed (21.2 → 1.8 nm) | **PASS** |

### 2d. Tooling persisted

| Script | Purpose |
|--------|---------|
| `scripts/pta/mint_authority_city.py` | Mint `priority_city` + harbour BPs + starter routes for mint-heavy authorities |
| `scripts/pta/seal_authority.py` | Per-authority domestic seal (extended hand-waypoint catalog) |
| `scripts/pta/regen_pta_economics.py` | Phase B/C regen; preserves Tasklet presentation keys on batch-5 |

Hand-waypoint catalogs: `data-clean/pta_hand_waypoints_{bc_ferries,hawaii,fullers360,maldives_government,norway_fjords}.json`

---

## 3. Mint-heavy five — geometry receipts (Grok unblocks Tasklet)

All six cities minted in `FEATURES_BY_TYPE.json` + `CLUSTERS.json`. Junk POIs quarantined (Oslo ramp, Fort Amsterdam, Wellington AU/US yacht club).

| City ID | Receipt | BPs | Sealed routes | Tasklet can PR now? |
|---------|---------|-----|---------------|---------------------|
| `oslo-norway` | `GEOMETRY-MINT-RECEIPT-oslo-norway.json` | 4 | 0 (fjord land-QA) | ✅ Dossier + partner JSON with `pending-seal` on unsealed pairs |
| `amsterdam-netherlands` | `GEOMETRY-MINT-RECEIPT-amsterdam-netherlands.json` | 4 | 0 (IJ land-QA) | ✅ Same |
| `wellington-new-zealand` | `GEOMETRY-MINT-RECEIPT-wellington-new-zealand.json` | 4 | 1 (`rn-a3c31405844f` Seatoun↔Somes) | ✅ Bind 1 route; pending-seal the rest |
| `copenhagen-denmark` | `GEOMETRY-MINT-RECEIPT-copenhagen-denmark.json` | 4 | 1 (`rn-f7d4a824ec58`) | ✅ Same |
| `gothenburg-sweden` | `GEOMETRY-MINT-RECEIPT-gothenburg-sweden.json` | 4 | 1 (`rn-f1d39ae68265`) | ✅ Same |
| `rotterdam-netherlands` | `GEOMETRY-MINT-RECEIPT-rotterdam-netherlands.json` | 4 | 0 (river land-QA) | ✅ Same |

**Tasklet pattern (same as #160/#161):**

1. Copy receipt `boarding_points[].bp_id` + `node` into `PTA-DOSSIER-<slug>.json`
2. Bind only to receipt `sealed_routes[].route_id` values that exist
3. Unsealed pairs: `route_id: null`, `_link_status: "pending-seal"` — fidelity accepts this
4. One PR per authority (dossier → rewrite → GROK-SPEC → partner JSON both trees)

**No Grok wait.** Starter-route gaps are documented; Tasklet prose + dossier work proceeds in parallel.

---

## 4. What Tasklet owns next (complete checklist, no Grok deps)

### P0 — Copy hygiene (quick)

| # | Task | Acceptance |
|---|------|------------|
| 1 | Scrub `_recal_provenance` SAM/TAM strings from 24 batch-5 JSONs | `rg 'Forward-SAM|SAM mid|journey_gmv' data-clean/partners/{batch-5}.json` → 0 |
| 2 | Update `PTA-MASTER-PLAN.md` — Grok lane closed; mint-heavy unblocked | Living doc accurate |

### P1 — PTA partner PRs (all unblocked)

| # | Task | Pattern |
|---|------|---------|
| 3 | Mint-heavy five — one PR per authority | §3 receipt → dossier → partner JSON (#160/#161 template) |
| 4 | `wsf` full PTA dossier + rewrite | Only outstanding Batch-6 authority (besides deferred `shun-tak`) |
| 5 | Append mint-heavy five to `PTA-PAIR-GAP-TABLE.json` | After dossier pair counts set |

### P2 — Scope decisions (Jaideep / Tasklet)

| Item | Status | Action |
|------|--------|--------|
| `shun-tak` | Deferred | GBA commercial cross-boundary lane — do not force domestic PTA |
| `wsf` | Partial scrub done (#150) | Full dossier + rewrite PR |

### P3 — Phase D (Batch-8)

Greenlit per master plan §6 — sequenced after Batch-7 mint-heavy PRs land. Not blocked.

### P4 — Deck lanes (unchanged)

Centara deck appendix, LINE MAN live Slides, Minor gold deck, bite-2 economics stubs.

---

## 5. Suggested Tasklet priority order

1. **P0 #1** — `_recal_provenance` scrub (1 PR, fast)
2. **Mint-heavy five** — six per-authority PRs (Oslo → Amsterdam → Wellington → Copenhagen → Gothenburg → Rotterdam)
3. **`wsf` full PTA lane** — dossier + rewrite
4. **Phase D** research bench — after Batch-7 complete

---

## 6. Acceptance commands (verified this lane)

```bash
# Phase B/C fidelity (all PASS)
python3 scripts/audit_proposal_fidelity.py --partner bc-ferries
python3 scripts/audit_proposal_fidelity.py --partner hawaii
python3 scripts/audit_proposal_fidelity.py --partner fullers360
python3 scripts/audit_proposal_fidelity.py --partner maldives-government
python3 scripts/audit_proposal_fidelity.py --partner norway-fjords
python3 scripts/audit_proposal_fidelity.py --partner kolkata-wbtc
python3 scripts/audit_proposal_fidelity.py --partner helsinki-hsl

# Build
BUILD_PROFILE=public node scripts/build.mjs --profile=public
BUILD_PROFILE=public node scripts/build-site.mjs --profile=public
```

**Guardrail (unchanged):** Do **not** re-run `regen_pta_economics.py --all` on the 24 batch-5 partners — it reverts Tasklet presentation fields from #150.

---

## 7. Known honest-nulls (not Grok blockers)

| Item | State | Tasklet handling |
|------|-------|------------------|
| `bc-ferries` bcf-d04 | `geometry_seal_pending` | Keep aspirational; optional future seal pass |
| `mumbai-mmb` 2 corridors | `geometry_seal_pending` | Already DROP'd in #151; keep flagged |
| Mint-heavy 0-route cities | BPs minted, routes pending | `pending-seal` on unsealed pairs in partner JSON |
| Bahrain phase-2/3 distances | Some phase-2 island legs still ~21 nm placeholder | Tasklet copy QA; no geometry dependency |

---

*Grok seat · navier-atlas · Grok lane complete · Tasklet cleared to proceed*