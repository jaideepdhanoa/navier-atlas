# GROK SEAL PROMPT — Minor Hotels (hotel-developer archetype)

**You are Grok, the deterministic seal/render lane.** Tasklet has finished source-backed research, binds,
seeds, coverage audit, three economics floors, and the archetype/narrative/cluster specs in this package.
Your job is the **deterministic** half only: ID-match promotion, captive intra-portfolio route graph,
cascade, reseal to the next gold tag, and a QA report. **GitHub `main` is source of truth; this zip is an
input package, not a hand-back.**

> ❗ **Status of this package: `research-complete / seal-needed`.** It is NOT `proposal-complete`. Do not
> report completion until the full chain (your route IDs/render QA → Tasklet country-reference/model/growth/
> sheet cascade → economics sidecar → delivery receipt) exists.

---

## 0. Read first
`01-MINOR-ARCHETYPE-GUIDE.md` — Minor is **captive `hospitality_developer`**, NOT ride-hail. Then
`02-MINOR-NARRATIVE-AND-USP.md` and `03-MINOR-CLUSTER-SUBPROPOSAL-PLAN.md`.

## 1. Mandate (archetype-specific — the #1 rule)
Build routes **ONLY** within Minor's own property graph. A leg is valid **iff** at least one endpoint is a
**Minor property** (matched by ID to the inventory `property_name` / bound `atlas_registry_key`) or a
**Minor-curated excursion node**. Three permitted classes only:
- **A. Gateway transfer** (airport/seaport ↔ Minor property)
- **B. Intra-portfolio hop** (Minor property ↔ Minor property)
- **C. Signature excursion** (Minor property ↔ marquee day-trip node)

**Forbidden:** generic city mobility, any leg with no Minor endpoint, network-completeness legs between two
non-Minor nodes, or re-skinning a Bolt/Yango/Grab contested corridor as Minor. If an endpoint's resort-jetty
geometry is absent, keep the bind **city-market/cluster-level** or **future-BP** — **null beats
confidently-wrong; never fabricate jetty coordinates or a route_id.**

## 2. Deterministic field mappings (no interpretation)
| Source field (this package) | Atlas target | Rule |
|---|---|---|
| bind `atlas_registry_key` | sealed `city_id` (country-suffixed) | ID-match; **anchor-city crosswalk** — `dubai-uae`→atlas `dubai` etc. (Gate A) |
| bind `property_name` | POI label / property node | exact string; one POI per property |
| bind `bp_binding` (+ `_note`) | BP geometry | promote if coords exist; else `city-market` bind, flag aspirational |
| seed `proposed_key` / `registry_key` | new `city_market` registry entry | promote at `registry_level`; status `seal-needed`→sealed |
| seed `candidate_boarding_points[].confidence` | BP render confidence | `high`→solid; `medium/low`→amber-dashed/aspirational |
| seed `route_archetypes` | corridor class A/B/C | build only if a Minor endpoint resolves |
| attach `bound_market_key` | existing `gold-coast-australia` | attach as southern extension — **NOT** a new market |
| economics floor `economics_key` | partner sheet `economics_url` | bind chip + TAM-ladder rungs to the Sheet |
| corridor country | `country-reference.json` row | **preflight**: add honest row before cascade or it silently inherits Singapore opex |
| corridor length (nm) | vessel class | ≤70→Pioneer II; 75–150→Quanta-LR amber; >150→Quanta-LR flagged |
| corridor country region | CAPEX | US+EU=$900K; else $600K |

## 3. Eval gates (all must pass in your QA report)
- **G1 — Archetype purity:** 0 routes whose both endpoints are non-Minor. Every sealed leg names its Minor
  endpoint. (This is the gate that distinguishes Minor from every prior partner — make it hard.)
- **G2 — Coverage / 0 silent drops:** reconcile every coastal property in `minor-hotels-COVERAGE-AUDIT.json`
  to **sealed POI**, **seeded market**, **attach**, **pipeline**, or **held_decision (with reason)**. No
  silent drops. The 2 held (Villa Padierna Marbella, AfroChic Diani) stay held — do not seed one-property
  markets.
- **G3 — Anchor-city render parity (Gate A):** every `anchor_cities` id resolves to a real `city_id`; emit a
  `MINOR-ANCHOR-CITY-CROSSWALK.json` with `OK`/`ID_MISMATCH`/`MISSING_GEOMETRY` verdicts; rename all
  `ID_MISMATCH` before render.
- **G4 — Captive economics (LB-254):** the TAM ladder anchors `M_today` on `transport_spend_pool_yr`
  (≈floor at ~0.90 capture), **never** `floor/0.10`. Headroom = WIDTH (keys/openings/clusters), not
  capture-share. Grounded floor unchanged. Sanity: no cluster's journey-GMV TAM exceeds its region's whole
  luxury-transfer economy.
- **G5 — country-reference coverage:** 0 countries silently inheriting Singapore opex.
- **G6 — Vessel + CAPEX gates:** 0 long legs on a 70nm hull; CAPEX region-keyed.
- **G7 — Land-crossing / orphan:** 0 land-crossings post-allowlist; 0 orphan routes; every surviving BP
  carries a source id.
- **G8 — Palm grounding flag:** Palm Jumeirah submarket renders real geometry only after BP grounding;
  otherwise flag visibly aspirational (do not let the $3.75M floor cascade on 0 BPs).

## 4. Deterministic cascade order (per cluster, grounded-first)
Run Phuket → Bali first (both `economics_ready`), then Palm (after grounding), then Tier-2/3 as WIDTH:
`aggregate.py → growth.py → growth_frontend_block.py → splice_growth_into_partner.py →
build_transparent_sheet.py → build_master_sheet.py`, then build the **economics sidecar against the NEW
gold** (`build_economics_sidecar.py`). Use the **captive** capture path, not the contested ramp.

## 5. QA report must show
BPs sealed/dropped (+reason); routes built/culled by class A/B/C; before→after POI total; G1 archetype-purity
count (non-Minor-endpoint legs = 0); anchor-city crosswalk verdicts; land-crossing=0 proof; country-reference
additions; vessel re-gate ledger; per-cluster grounded floor reconciled to `aggregate.py`; `economics_url`
wired to TAM rungs; Palm aspirational-flag proof.

## 6. Out of scope for you (Tasklet owns)
Narrative/USP authoring, demand/fare assumptions, the archetype decision, held-market decisions, external
outreach (stays draft). You do deterministic sealing/cascade/render QA only.
