# Grok → Tasklet handback — PTA stack merged (#150–#161)

**From:** Grok (Jaideep merge) · **Date:** 2026-07-02 · **`main` HEAD:** `64c2b8cc`  
**Merged:** PRs **#150–#161** (12 PRs, stack order) · **Open PTA PRs:** 0  
**Living ledger:** `handoff/partner-map-model/PTA-MASTER-PLAN.md` (update checkboxes as work lands)

---

## 1. What just landed on `main`

### Phase A — Batch-5 completion (#150–#154) ✅ MERGED

| PR | Work | Post-merge state |
|----|------|------------------|
| **#150** | Economics presentation scrub, all 24 batch-5 authorities | `_render_chip_flag` / `_marine_tam_split_provenance` removed; authority fare systems in `operating_model`; public-value headlines relabeled |
| **#151** | `mumbai-mmb` fidelity TRIM | Audit **PASS**; 2 routes flagged `geometry_seal_pending` for Grok re-seal |
| **#152** | NYC, SF Bay, TfNSW, Boston, Stockholm TRIM | All **PASS** |
| **#153** | Brisbane + Hamburg TRIM | Both **PASS** |
| **#154** | Hero voice pass (5 authorities) | Authority-proposal eyebrows + place-specific titles |

**Grok guardrail (locked):** Do **not** re-run `regen_pta_economics.py --all` on the 24 batch-5 partners — it will revert Tasklet's presentation fields (`operating_model`, levers, headlines).

### Phase B — Outside-lane rewrites (#155–#159) ✅ MERGED

| PR | Partner | Post-merge state |
|----|---------|------------------|
| **#155** | `bc-ferries` | Dossier + GROK-SPEC + authority rewrite; **no `growth_case`** (economics off until Grok regen) |
| **#156** | `hawaii` | Same |
| **#157** | `fullers360` | Same; sailing-club junk corridors replaced |
| **#158** | `maldives-government` | Same; resort→public RTL correction |
| **#159** | `norway-fjords` | Same; 2026 fjord mandate framing |

### Phase C — Anchor-ready net-new (#160–#161) ✅ MERGED

| PR | Partner | Post-merge state |
|----|---------|------------------|
| **#160** | `kolkata-wbtc` | **5 sealed `route_id`s bound**; dossier + spec; fidelity **PASS**; `archetype: essential_mobility` |
| **#161** | `helsinki-hsl` | **7 sealed `route_id`s bound**; dossier + spec; fidelity **PASS**; `archetype: essential_mobility` |

**Intentionally not merged:** `shun-tak` — deferred per scope memo (commercial cross-boundary franchise, not domestic PTA).

---

## 2. What Grok owns next (do not ask Tasklet)

These are **Grok seal/economics lanes** — Tasklet should not author geometry or regen numbers until Grok completes each step.

### 2a. Batch-5 follow-ups (from merged TRIMs)

| Partner | Grok action | Trigger |
|---------|-------------|---------|
| `mumbai-mmb` | Re-seal 2 corridors (`Belapur ↔ Nerul`, `Gateway ↔ Rewas`) — currently `geometry_seal_pending`, `route_id: null` | #151 merged |
| `bahrain-motc` | Fix phase-1 inner-harbour `distance_nm: 21.2` → ~1.5–2 nm (or null until sealed) | #154 flag |

### 2b. Phase B — seal + economics (5 partners)

For each of `bc-ferries`, `hawaii`, `fullers360`, `maldives-government`, `norway-fjords`:

1. Execute GROK-SPEC domestic seal (mint/bind BPs, hand-waypoint, land QA `interior_land_km == 0`)
2. Bind `route_id`s into partner JSON; remove `pending-seal`
3. `python3 scripts/pta/regen_pta_economics.py --partner <slug> --apply`
4. Add `_public_transit_authority` block if missing (renderer uses this + `archetype: public_transit`)
5. Fidelity + linkage audit → PASS
6. Grok rebuild + deploy

**Norway special rule:** repair + promote only — **no full `relink_hub_market_featured.py` pass** (do-not-touch per handoff).

### 2c. Phase C anchor-ready — economics + archetype (2 partners)

`kolkata-wbtc` and `helsinki-hsl` have **real sealed geometry** already. Grok should:

1. Confirm route geometry QA clean (already bound)
2. `regen_pta_economics.py --partner kolkata-wbtc --apply` and `--partner helsinki-hsl --apply`
3. Set `archetype: public_transit` (or ensure `_public_transit_authority` + `growth_case._economics_status: pta_regenerated` so `_ptaEconomicsHtml` renders)
4. Deploy — intro step 2 will then show public-value economics

**Tasklet does not need to re-author these partners** unless copy QA finds issues after Grok economics land.

### 2d. Phase C mint-heavy five — geometry mint (Grok BLOCKER)

Tasklet is **correct** that these are blocked on Grok. Here is the precise split:

| Authority | Proposed slug (TBD) | Blocker | What Grok must mint **before** Tasklet dossier/rewrite |
|-----------|---------------------|---------|--------------------------------------------------------|
| **Oslo — Ruter** | `oslo-ruter` (suggested) | No `city` node; only junk POI **"Oslo Road Boat Ramp"** in `FEATURES_BY_TYPE.json` | `priority_city` `oslo-norway` + real BPs (Aker Brygge, Nesoddtangen, Hovedøya, …); purge junk ramp POI from bind candidates |
| **Amsterdam — GVB IJ** | `amsterdam-gvb` | No city node; junk POI **"Fort Amsterdam"** (Caribbean mis-geocode) | `priority_city` `amsterdam-netherlands` + IJ ferry pontoons (Buiksloterweg, IJplein, NDSM, …); quarantine Fort Amsterdam |
| **Wellington — Metlink** | `wellington-metlink` | No city node; junk POIs (Wellington Point AU, US yacht club) | `priority_city` `wellington-new-zealand` + Queens Wharf, Days Bay, Seatoun, Matiu/Somes |
| **Copenhagen — Movia** | `copenhagen-movia` | **Nothing** in atlas for Copenhagen harbour | Full new-geo: city node + harbour bus stops (Nyhavn, Refshaleøen, Opera, …) |
| **Gothenburg — Västtrafik** | `gothenburg-vasttrafik` | **Nothing** | Full new-geo: city node + Älvsnabben / archipelago BPs |
| **Rotterdam — RET/Waterbus** | `rotterdam-ret` | **Nothing** | Full new-geo: city node + Erasmusbrug, Dordrecht, Kinderdijk corridor BPs |

**Verified 2026-07-02:** `data-clean/city_briefs/` has **no** briefs for oslo/amsterdam/wellington/copenhagen/gothenburg/rotterdam. Helsinki (`helsinki-finland`) and Kolkata (`kolkata-india`) **do** exist — that's why #160/#161 could ship.

**Grok deliverable per mint-heavy city (unblocks Tasklet):**

```
handoff/partner-map-model/GEOMETRY-MINT-RECEIPT-<city_id>.json
  - city feature id + [lng,lat] + cluster registration
  - boarding_points[] minted (bp- ids) with on-water QA
  - optional: starter domestic_pairs[] sealed to rn- ids (minimum 2–4 for fidelity spine)
```

Post receipt → Tasklet runs Batch-6-style deliverables (dossier → rewrite → GROK-SPEC) as **one PR per authority**, same pattern as #160/#161.

**Tasklet may research now** (policy targets, operator names, published lines, electrification commitments) into draft dossiers under `handoff/partner-map-model/drafts/` — but **do not** open partner JSON PRs with `route_id: null` pretending geometry exists; fidelity will fail or bind junk.

---

## 3. What Tasklet still owes (no-gap checklist)

### P0 — Copy hygiene (quick, no Grok dependency)

| # | Task | Files | Acceptance |
|---|------|-------|------------|
| 1 | Scrub `_recal_provenance` SAM/TAM strings from batch-5 JSONs (e.g. `qatar.json` still has `Forward-SAM` / `SAM mid lane` in internal provenance — **ships** in `atlas-data.js` because `build.mjs` only strips `deck_only` / `reviewer_notes`) | 24 partners in both trees | `rg 'Forward-SAM|SAM mid|journey_gmv' data-clean/partners/{batch-5}.json` → 0 |
| 2 | Update `PTA-MASTER-PLAN.md` checkboxes: Phase A/B/C merged; mint-heavy five blocked on Grok receipts | master plan | Living doc accurate |
| 3 | Bahrain phase-1 narrative stub (KPI/regulator prose only) — optional polish | `bahrain-motc.json` | No geometry edits |

### P1 — Waiting on Grok (Tasklet: queue research, do not PR partner JSON yet)

| # | Task | Blocked on |
|---|------|------------|
| 4 | Phase C mint-heavy five dossiers + partner PRs | Grok `GEOMETRY-MINT-RECEIPT-*` per city (§2d) |
| 5 | Append mint-heavy five to `PTA-PAIR-GAP-TABLE.json` | Dossier pair counts known post-mint |

### P2 — Scope decisions (Jaideep / Tasklet — not Grok)

| # | Item | Status | Tasklet action |
|---|------|--------|----------------|
| 6 | **`shun-tak`** | Deferred | Hold until scope call: GBA commercial cross-boundary lane vs domestic PTA. Memo exists per master plan. **Do not force domestic rewrite.** |
| 7 | **`wsf` full PTA lane** | Partial | Batch-5 scrub + hero voice done (#150, #154). Still **no PTA dossier**, commercial-adjacent `growth_case` present, 4 pending + 4 sealed routes. **Tasklet:** full dossier + rewrite PR (was planned PR-7; only 5/6 Batch-6 shipped). |
| 8 | **`kolkata-wbtc` / `helsinki-hsl` archetype** | `essential_mobility` | Tasklet decision: keep chip label or flip to `public_transit` when Grok adds economics. Grok can set on regen; Tasklet OK either way if documented. |

### P3 — Phase D (Batch-8) — greenlit, sequenced after Batch-7

Active bench per master plan §6 — **not blocked**, but **lower priority** than mint-heavy five:

- Scotland CalMac · Liverpool Mersey · HCMC Saigon Waterbus · Manila Pasig · Rio CCR Barcas · Toronto Island · **Seoul Hangang** (ID hygiene vs `kakao-mobility` — parallel authority + commercial paths)

Tasklet: maintain research notes; **no PRs** until Batch-7 mint-heavy clears.

### P4 — Deck / non-PTA lanes (unchanged)

Still on Tasklet per prior handback: Centara deck appendix, LINE MAN live Slides, Minor gold deck, bite-2 economics stubs.

---

## 4. Mint-heavy five — precision for Tasklet's "blocked on Grok" note

**Tasklet's statement is accurate.** Expand with ownership boundaries:

| Layer | Owner | Status for mint-heavy five |
|-------|-------|--------------------------|
| City `priority_city` feature | **Grok** | Not minted (except Helsinki/Kolkata already done) |
| Boarding points on water | **Grok** | Not minted |
| Domestic pair routes (`rn-`) | **Grok** | Not sealed — **zero** honest `route_id`s to bind |
| Junk POI quarantine (Oslo ramp, Fort Amsterdam, Wellington AU) | **Grok** | Must not be used as bind targets |
| `CLUSTERS.json` registration | **Grok** | Pending mint |
| Dossier (`PTA-DOSSIER-*.json`) | **Tasklet** | **Blocked** until BPs exist (can draft prose in `drafts/`) |
| Partner rewrite | **Tasklet** | **Blocked** — null `route_id` partners without atlas anchors fail credibility bar |
| GROK-SPEC seal handoff | **Tasklet** | **Blocked** — no pairs to spec |
| Economics regen | **Grok** | **Blocked** — no sealed corridor count |

**What "research the moment nodes land" should mean:**

1. **Now (allowed):** web-verify operator, electrification policy, published line list, decarb targets → save to `handoff/partner-map-model/drafts/PTA-DOSSIER-Draft-<slug>.json` (not shipped partner JSON).
2. **On Grok receipt (required before PR):** copy draft → real `PTA-DOSSIER-<slug>.json` using minted `bp-` ids; build partner JSON binding only to receipt `rn-` ids (Kolkata/Helsinki pattern).
3. **Not now:** do not add `data-clean/partners/oslo-*.json` with invented coordinates — violates null-beats-wrong.

**Grok ETA sequencing (proposed):**

1. Oslo + Amsterdam + Wellington (cleanup + mint — junk POI purge first)
2. Copenhagen + Gothenburg + Rotterdam (greenfield mint)
3. Post each receipt → Tasklet one PR per authority → Grok economics regen → deploy

---

## 5. Suggested Tasklet priority order (post-merge)

1. **P0 #1** — `_recal_provenance` scrub (1 PR, 24 files, fast)
2. **Draft research** — mint-heavy five dossier drafts (no partner JSON)
3. **WSF full PTA lane** — dossier + rewrite (only outstanding Batch-6 authority besides shun-tak)
4. **Wait for Grok** — mint receipts → Phase C PRs for Oslo/Amsterdam/Wellington/Copenhagen/Gothenburg/Rotterdam
5. **Phase D** — after Batch-7 complete

---

## 6. Commands reference

```bash
# Fidelity (after any Tasklet partner edit)
python3 scripts/audit_proposal_fidelity.py --partner <slug>

# Forbidden-key scrub check (batch-5)
rg '_render_chip_flag|_marine_tam_split_provenance|water_transport_market|Forward-SAM' data-clean/partners/

# Build
BUILD_PROFILE=public node scripts/build.mjs --profile=public
```

---

*Grok seat · navier-atlas · post-merge handback for Tasklet · `main@64c2b8cc`*