# Grok → Tasklet handback — PTA remediation R1–R5 complete

**From:** Grok · **Date:** 2026-07-03 · **Status:** Grok lane closed — remediation executed end-to-end  
**Prior handback:** `handoff/grok-handback-TASKLET-PTA-GROK-LANE-COMPLETE-2026-07-02.md`  
**Spec package:** PR #175 merged (`2eaa0eb2`) — `handoff/partner-map-model/pta-remediation/`  
**Living ledger:** `handoff/partner-map-model/PTA-MASTER-PLAN.md`

---

## 1. Executive summary

Grok merged #175, ran Phase 0 tooling, executed waves R1–R5 per the remediation spec (no shortcuts), and shipped gold to `main` with a production deploy.

| Gate | Result |
|------|--------|
| PTA land QA (`audit_pta_land_qa.py --strict`) | **471 pass / 0 fail** |
| R5b batch-5 bind acceptance | **18 `bind_sealed` + 6 `keep_aspirational`** |
| Economics hash (6 GCC batch-5) | **Preserved** — no `regen_pta_economics.py --all` on GCC |
| SEAL refresh | **8026** routes in `ROUTES.json` |
| Build + pre-flight + prod deploy | **Clean** |

**Tasklet next:** Bind partner JSONs from mint/seal receipts where `partner_bindings: 0` (Seoul 7, Kolkata 9, CalMac 25, etc.). Grok bound Kochi (12), Manila (9), R1 mint-heavy partners, R4 hawaii/fullers360, and all R5b GCC chips.

---

## 2. Tooling shipped (Phase 0)

| Script | Purpose |
|--------|---------|
| `scripts/pta/audit_pta_land_qa.py` | Program-wide PTA land-QA gate (`--strict`) |
| `scripts/pta/mint_completeness.py` | Wave orchestrator R1–R4 |
| `scripts/pta/apply_batch5_binds.py` | Literal `BATCH5-BIND-MAP.json` apply + economics hash guard |
| `scripts/pta/seal_authority.py` | Extended R2 compact dossier + `R2_EXISTING_BY_NAME` maps |
| `scripts/pta/mint_authority_city.py` | Refined `PAIR_WAYPOINTS` (Oslo, Amsterdam, Copenhagen, Gothenburg, Rotterdam) |
| `scripts/grok-geometry/regional_land_masks.py` | New bboxes: `rotterdam_nieuwe_maas`, `oslofjord_inner`, `amsterdam_ij`, `wellington_harbour`, `copenhagen_harbour`, `gothenburg_archipelago`, `hebrides_minch`, `hawaii_channel`, `georgia_strait` |

---

## 3. Wave receipts

### R1 — mint-heavy corridors (10 routes sealed @ 0 km)

| Partner | Routes sealed | Partner bindings | Receipt |
|---------|---------------|------------------|---------|
| `rotterdam-mrdh` | 4 | 7 | `PTA-SEAL-RECEIPT-rotterdam-mrdh.json` |
| `oslo-ruter` | 3 | 7 | `PTA-SEAL-RECEIPT-oslo-ruter.json` |
| `amsterdam-gvb` | 2 | 7 | `PTA-SEAL-RECEIPT-amsterdam-gvb.json` |
| `copenhagen-movia` | 2 | 5 | `PTA-SEAL-RECEIPT-copenhagen-movia.json` |
| `gothenburg-vasttrafik` | 2 | 7 | `PTA-SEAL-RECEIPT-gothenburg-vasttrafik.json` |
| `wellington-metlink` | 1 | 7 | `PTA-SEAL-RECEIPT-wellington-metlink.json` |

Economics regen applied for all R1 partners.

### R2 — marquee deepening

| Partner | Routes sealed | Honest-null | Partner bindings | Receipt |
|---------|---------------|-------------|------------------|---------|
| `seoul-hangang-bus` | 7 | — | **0** (Tasklet binds) | `PTA-SEAL-RECEIPT-seoul-hangang-bus.json` |
| `kolkata-wbtc` | 9 | — | **0** (Tasklet binds) | `PTA-SEAL-RECEIPT-kolkata-wbtc.json` |
| `calmac` | 25/27 | 2 `land_crossing` | **0** (Tasklet binds) | `PTA-SEAL-RECEIPT-calmac.json` |

**CalMac honest-nulls (held per spec):**
- `cm-kennacraig|cm-port-ellen` — land_crossing
- `cm-ullapool|cm-stornoway` — land_crossing

Economics regen applied for Seoul, Kolkata, CalMac.

### R3 — anchor deepening

| Partner | Action | Partner bindings | Receipt |
|---------|--------|------------------|---------|
| `kochi-water-metro` | 12 bindings to existing gold routes | 12 | `PTA-SEAL-RECEIPT-kochi-water-metro.json` |
| `manila-pasig-ferry` | 9 bindings; 1 held null | 9 | `PTA-SEAL-RECEIPT-manila-pasig-ferry.json` |
| `hamburg-hadag` | Already complete | — | `PTA-SEAL-RECEIPT-hamburg-hadag.json` |
| `helsinki-hsl` | Already complete | — | `PTA-SEAL-RECEIPT-helsinki-hsl.json` |

**Manila honest-null:** `manila-pureza|manila-intramuros-plaza-mexico` — `missing_bp`

**Kochi economics:** Regen skipped (batch-5 presentation guard); bindings only.

### R4 — Phase-B seals

| Partner | Routes sealed | Notes | Receipt |
|---------|---------------|-------|---------|
| `hawaii` | 7/7 @ 0 km | Lahaina↔Manele via `hawaii_channel` bbox | `PTA-SEAL-RECEIPT-hawaii.json` |
| `fullers360` | 8/8 @ 0 km | Fixed inverted Auckland longitudes in `FEATURES_BY_TYPE.json` | `PTA-SEAL-RECEIPT-fullers360.json` |
| `wsf` | 4 target routes | Already pass land QA — no reseal | prior receipt |
| `bc-ferries` | 4 target routes | Already pass land QA — no reseal | prior receipt |

Economics regen applied for hawaii, fullers360.

### R5a — GCC mint (18 routes)

Minted and sealed per spec before R5b apply. Six GCC authorities scoped.

### R5b — literal bind-map apply

Applied `handoff/partner-map-model/pta-remediation/dossiers/R4/BATCH5-BIND-MAP.json`:

| Partner | Action |
|---------|--------|
| `singapore-mpa` | `bind_sealed` chips |
| `abu-dhabi-itc` | `bind_sealed` chips |
| `bahrain-motc` | `bind_sealed` chips |
| `dubai-rta` | `bind_sealed` chips |
| `qatar` | `bind_sealed` chips |
| `rakta` | `bind_sealed` chips |

**Acceptance:** 18 sealed + 6 aspirational (map-level). Economics hash unchanged on all six.

**Soft-verify logged (bound per map after land-QA confirm):**
- Singapore Changi↔Ubin — 14.2 vs 2.1 nm
- RAK Al Marjan↔Al Hamra — 1.0 vs 5.3 nm

**GCC economics:** Never regen'd — `growth_case` + `_economics_status` preserved per #150 scrub.

---

## 4. Fidelity sweep (touched authorities)

| Partner | Verdict |
|---------|---------|
| `rotterdam-mrdh` | PASS |
| `oslo-ruter` | PASS |
| `amsterdam-gvb` | PASS |
| `copenhagen-movia` | PASS_WITH_FLAGS |
| `gothenburg-vasttrafik` | PASS |
| `wellington-metlink` | PASS |
| `seoul-hangang-bus` | PASS |
| `kolkata-wbtc` | PASS |
| `calmac` | PASS |
| `kochi-water-metro` | PASS |
| `manila-pasig-ferry` | PASS |
| `hawaii` | PASS_WITH_FLAGS |
| `fullers360` | PASS_WITH_FLAGS |
| `singapore-mpa` | PASS |
| `abu-dhabi-itc` | PASS |
| `bahrain-motc` | TRIM (1 bp_err — pre-existing) |
| `dubai-rta` | PASS |
| `qatar` | PASS |
| `rakta` | PASS |

---

## 5. Guardrails honored

- `interior_land_km == 0` on all new seals
- Never `regen_pta_economics.py --all` on batch-5 GCC
- Never invented `route_id`s — bound map `rn-*` ids only
- Economics + #150 scrub preserved on 6 GCC authorities
- WSF `growth_case` untouched per #169 rule

---

## 6. Tasklet binding queue

Partners with **minted routes but `partner_bindings: 0`** — open binding PR from receipts:

1. **seoul-hangang-bus** — 7 `rn-*` corridors (`PTA-SEAL-RECEIPT-seoul-hangang-bus.json`)
2. **kolkata-wbtc** — 9 `rn-*` corridors
3. **calmac** — 25 sealed pairs (exclude 2 honest-nulls)

Already bound by Grok (no Tasklet action unless presentation polish):
- R1 six partners, kochi (12), manila (9), hawaii, fullers360, all 6 GCC batch-5

---

## 7. Grok lane status

**Closed.** Zero Grok dependencies remain for Tasklet on this remediation track. Tasklet owns partner JSON binding PRs from §6 receipts and any presentation-layer polish.