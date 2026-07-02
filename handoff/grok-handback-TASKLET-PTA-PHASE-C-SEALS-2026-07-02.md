# Grok → Tasklet handback — Phase C seals + economics (post #162–#169)

**From:** Grok · **Date:** 2026-07-02  
**Context:** Tasklet shipped Phase C (#162–#169, open PRs). Grok executed the **second Grok lane**: mint-heavy pending-seal corridors + authority economics regen.  
**Prior handbacks:** `grok-handback-TASKLET-PTA-GROK-LANE-COMPLETE-2026-07-02.md` · `grok-handback-TASKLET-PTA-POST-MERGE-2026-07-02.md`

---

## 1. PR review (#162–#169) — Grok verdict: **APPROVE stack**

> **Note:** PRs are **open** on GitHub as of this handback; only the master-plan ledger commit (`ca457394`) is on `main`. Merge order below is Jaideep's call.

### #162 — Batch-5 taxonomy scrub (qatar + singapore-mpa) ✅
- Surgical, matches nyc-ferry gold vessel-role wording.
- Clears last `Prove + Scale` / `Forward-SAM` debt from batch-5.
- Guardrail respected — no economics regen.
- **Verdict:** Merge first (no dependencies).

### #163–#168 — Mint-heavy six ✅
Each follows the #160/#161 gold pattern correctly:
- Real minted `bp-` ids from geometry receipts.
- Sealed routes bound where they existed at mint time.
- Remaining corridors honest `pending-seal` (null `route_id`).
- No commercial `growth_case`; economics gated until Grok regen.
- GROK-SPEC per authority with explicit seal asks.
- Fidelity **PASS** on all six at PR time.

| PR | Slug | Decarb anchor (verified framing) | Grok notes |
|----|------|-----------------------------------|------------|
| #163 | `oslo-ruter` | Ruter–Norled fjord electrification | Strong; 4 pending at ship |
| #164 | `amsterdam-gvb` | Free electric IJ ferries | Strong; 4 pending |
| #165 | `copenhagen-movia` | Harbour buses electric since 2020 | Strong; 1 sealed + 3 pending |
| #166 | `wellington-metlink` | *Ika Rere* electric ferry | Strong; 1 sealed + 3 pending |
| #167 | `rotterdam-mrdh` | MRDH Waterbus electrification | Strong; 4 pending |
| #168 | `gothenburg-vasttrafik` | Electric hydrofoil trial | Strong; 1 sealed + 3 pending |

**Minor (non-blocking):** `archetype: essential_mobility` on all six — Grok regen flips to `public_transit` + `_public_transit_authority` (done in Grok lane below).

### #169 — WSF surgical finish ✅
- Close phase-ladder scrub only (economics untouched — correct).
- Batch-6 dossier parity restored in provenance form.
- GROK-SPEC for 4 pending Puget Sound corridors.
- **Verdict:** Merge after mint-heavy stack (or in parallel — no file conflicts).

### Recommended merge order
```
#162 → #163 → #164 → #165 → #166 → #167 → #168 → #169
```
Then merge Grok seal PR (this lane) on top.

---

## 2. What Grok shipped (second lane)

Extended `seal_authority.py` + `regen_pta_economics.py` for Tasklet's compact dossier format (`boarding_points` + `pending_pairs`).

### Mint-heavy seal results

| Partner | Routes minted | Still pending | Economics regen | Fidelity |
|---------|---------------|---------------|-----------------|----------|
| `oslo-ruter` | 1 (Hovedøya↔Bygdøy) | 3 | ✅ 1 corridor | **PASS** |
| `amsterdam-gvb` | 2 (IJ pairs) | 2 | ✅ 2 corridors | **PASS** |
| `copenhagen-movia` | 2 | 2 | ✅ 2 corridors | **PASS** |
| `wellington-metlink` | 3 | 1 | ✅ 3 corridors | **PASS** |
| `rotterdam-mrdh` | 0 | 4 | ✅ (0 sealed — honest floor) | **PASS** |
| `gothenburg-vasttrafik` | 2 | 2 | ✅ 2 corridors | **PASS** |

Receipts: `handoff/partner-map-model/PTA-SEAL-RECEIPT-{slug}.json`

**Land-QA blockers (honest-null, not Tasklet blockers):**
- **Oslo:** Aker Brygge legs (inner-fjord land mask) — flagship Nesoddtangen still pending.
- **Rotterdam:** All 4 river legs — Nieuwe Maas land-QA; economics panel uses honest floor until any route seals.
- **Amsterdam/Copenhagen/Gothenburg/Wellington:** partial seal — remaining pairs pending.

### WSF (#169 spec)
- Seal pass: **0 new routes** (1 `missing_bp` on legacy dossier pair — 4 target corridors still `aspirational-no-built-route`).
- Economics **unchanged** (per #169 — already Grok-regenerated).
- Fidelity **PASS** (12/12).

---

## 3. What Tasklet owns next (zero Grok deps after merge)

### P0 — Merge + verify
1. Merge #162–#169 in stack order.
2. Merge Grok seal branch (seal receipts + economics + tooling).
3. Spot-check intro step 2 on 2–3 mint-heavy authorities (economics panel live where corridors > 0).

### P1 — Optional copy polish (no Grok)
| Item | Action |
|------|--------|
| Rotterdam | Economics floor-only until routes seal — prose already honest; no change required |
| Mint-heavy `essential_mobility` | Already flipped to `public_transit` by Grok regen — verify chip label in UI |
| `PTA-PAIR-GAP-TABLE.json` | Append six new authorities (Tasklet noted) |

### P2 — Phase D (Batch-8)
Greenlit per master plan §6 — **not blocked**. Sequenced after Batch-7 merges land:
Scotland CalMac · Liverpool Mersey · HCMC · Manila · Rio · Toronto · Seoul Hangang (ID hygiene vs `kakao-mobility`).

### P3 — Deferred
- **`shun-tak`** — Jaideep scope call (GBA commercial lane).
- **Residual honest-null seals** (Oslo Aker Brygge, Rotterdam river, WSF 4 corridors, bc-ferries bcf-d04) — optional future Grok pass; fidelity PASS with pending-seal.

---

## 4. Acceptance commands (verified)

```bash
# Mint-heavy fidelity (all PASS post Grok lane)
python3 scripts/audit_proposal_fidelity.py --partner oslo-ruter
python3 scripts/audit_proposal_fidelity.py --partner amsterdam-gvb
python3 scripts/audit_proposal_fidelity.py --partner copenhagen-movia
python3 scripts/audit_proposal_fidelity.py --partner wellington-metlink
python3 scripts/audit_proposal_fidelity.py --partner rotterdam-mrdh
python3 scripts/audit_proposal_fidelity.py --partner gothenburg-vasttrafik

BUILD_PROFILE=public node scripts/build.mjs --profile=public
```

**Guardrails (unchanged):**
- Do **not** `regen_pta_economics.py --all` on batch-5 (#150 scrub).
- Do **not** touch WSF `growth_case` numbers (#169 surgical rule).

---

*Grok seat · navier-atlas · Phase C Tasklet lane reviewed · Grok seal lane executed · Tasklet cleared for Phase D*