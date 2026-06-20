# Partner-proposal parity fix — Grab/Bolt/Yango — 2026-06-20

Tasklet → Grok. Source of truth = `jaideepdhanoa/navier-atlas`. Closes the "no use cases even on Grab"
finding and the stale/missing TAM ladders on Bolt/Yango. Follows `partner-proposal-parity` (Gates A–E)
and `partner-model-cascade`.

## What Tasklet already did in THIS PR (content + registry — done, no re-run needed)

### 1. Grab USE CASES — filled (was the headline gap)
`data-clean/partners/grab.json`: every phase USE-CASES block rendered as **blank bars** because all
`use_cases[].summary` were empty strings (the renderer draws one bar per use_case and prints its `summary`).
- Authored **72** grounded, brand-voice one-line summaries across 12 markets (Singapore … Taiwan).
- Added `use_cases` to the **2 Bangkok / Chao Phraya phases** that had none.
- Final audit: **76 use_cases, 0 empty summaries, 0 phases without use_cases.**
- Every summary is fact-grounded in that phase's real `featured_routes`/`cities`; no invented places, no hype tokens.
- NOTE: Bolt (46) and Yango (24) already carry full use-case summaries — so any blank USE-CASES bars on the
  **live** Bolt/Yango pages are a **render/deploy lag, not a data gap**. Please confirm the live build is from
  current `data-clean/partners/*.json`; if blank bars persist after redeploy, it's a renderer bug (flag back).

### 2. SE-Asia Grab corridor buckets — de-contaminated (the bali/phuket misnomer)
`finance/model/corridors.json`: the partnerless Grab shared-network buckets were **overlapping duplicate
supersets** — each geography's corridors were double/triple-counted:
- `bali` ≡ `jakarta` held the **same 12 rows** (Bali-chain + Jakarta) under two names.
- `phuket` ≡ `bangkok` ≡ `koh-samui` held the **same 18 rows** (Phuket + Bangkok + Samui + a stray Penang/Langkawi) under three names.
- Re-scoped each bucket to ONLY its own node-geography (verified **zero corridor lost**; 3 stray Penang/Langkawi
  rows routed into `penang`). New sizes: bali 8, jakarta 5, phuket 8, bangkok 2, koh-samui 7. File 1.64MB→1.33MB.

→ **DETERMINISTIC ACTION FOR GROK (economics impact):** Grab's aggregate previously summed the duplicated rows, so
its published floor/TAM was **inflated by double-counting**. Re-run the Grab cascade on the corrected registry:
```
cd finance/model
python3 aggregate.py --partner grab --json ../recal/agg-grab.json     # confirm mtime moved + spot-check
python3 growth.py --partner grab --agg ../recal/agg-grab.json --json ../grab-growth-case.json
python3 growth_frontend_block.py --partner grab --growth ../grab-growth-case.json --rollup ../recal/agg-grab.json \
        --out ../../partner-pitch/partners/_growth-draft/grab.growth.json
cd .. && python3 splice_growth_into_partner.py --partner grab --growth grab-growth-case.json \
        --frontend ../partner-pitch/partners/_growth-draft/grab.growth.json
```
Grab's floor/TAM **will move down** once duplicates are gone — that's the correct number; reconcile the deck/sheet to it.

## Deterministic work for Grok — Bolt & Yango TAM ladders (Gate B)

Audit of `data-clean/partners/{bolt,yango}.json` vs `grab.json`:

| Partner | growth_case | Anchor | Floor | Capture | Missing vs Grab |
|---|---|---|---|---|---|
| Grab (ref) | full | $782M/yr | $86M | 11% | — |
| **Bolt** | **stale** | $15M/yr | $2M | **10% flat** | `ladder_transitions`, `marine_mobility_tam`, `journey_gmv`, `partner_platform_rev_on_navier`, `modal_headline`, `modal_lead`, `_recal_provenance`, `confidence_label`, `economics_url`; rungs lack `confidence_label`/`model_link` |
| **Yango** | **ABSENT** (`_growth_case_pending:true`) | — | — | — | entire `growth_case` + `journeys_unlocked` |

### Bolt — re-cascade with captive-aware logic (golden rule #11)
Bolt's growth_case is pre-LB-254 (hard-coded 10% / `floor÷0.10` anchoring, missing the ladder-transition "SHOW MATH"
expanders and MODELED/PROJECTED chips). Re-run the full cascade so the ladder anchors on
`transport_spend_pool_yr` (Σ demand×fare) with `effective_capture`, emits `ladder_transitions`, and renders the
MODELED/PROJECTED confidence chips:
```
cd finance/model
python3 - <<'PY'  # §B.0 preflight — confirm every Bolt country has a country-reference row (no silent Singapore opex)
import json
corr=json.load(open('corridors.json'))['markets']; cref=set(json.load(open('country-reference.json'))['countries'])
need={m['country'] for k,m in corr.items() if k.startswith('bolt-') and m.get('country')}
print('missing:', sorted(need-cref) or 'none ✅')
PY
python3 aggregate.py --partner bolt --json ../recal/agg-bolt.json
python3 growth.py   --partner bolt --agg ../recal/agg-bolt.json --json ../bolt-growth-case.json
python3 growth_frontend_block.py --partner bolt --growth ../bolt-growth-case.json --rollup ../recal/agg-bolt.json \
        --out ../../partner-pitch/partners/_growth-draft/bolt.growth.json
cd .. && python3 splice_growth_into_partner.py --partner bolt --growth bolt-growth-case.json \
        --frontend ../partner-pitch/partners/_growth-draft/bolt.growth.json
```
- FOOTGUN reminder: `aggregate.py` output flag is `--json` (NOT `--out`) — confirm `agg-bolt.json` mtime moved.
- Greenfield: Bolt has no own census → use the **global template band (3.44/4.9/6.36) labelled a template assumption**
  (golden rule #3). Never point at `grab-greenfield-census.json`.
- Re-gate vessels first (`partner-pitch/subproposals/build_scaffold.py`) — emits the VESSEL-REGATE-LEDGER (Gate C.1).

### Yango — build growth_case from scratch
Yango has no growth_case (`_growth_case_pending:true`) and no `journeys_unlocked`. Run the same cascade for `yango`
(framing: the **Dubai-HQ'd Yango** — lead with the Dubai-HQ split, Gate E). Confirm `agg-yango.json` aggregates the
full Yango footprint (Egypt, Turkey incl. Bodrum/Antalya/Çeşme, Lagos, …), not a single market.

## Open Tasklet follow-ups (research lane — not in this PR)
- **Sub-page parity (Gate C):** confirm every in-scope Bolt/Yango market is a full sub-page, not a `roll_up_markets`
  stub (LB-251). Promote any market that has economics+corridors.
- **Narrative polish** on the 22 active Bolt/Yango subproposals (brand voice, facts unchanged).
- **`penang` bucket** still mixes a few Sabah/Kota-Kinabalu rows (belong in `borneo`) — left for a follow-up so this
  PR's Grab re-aggregate isn't widened; flag if you want it folded in now.

## Definition of done (this thread)
Grab use-cases render on every phase; Grab/Bolt/Yango TAM ladders render with SHOW-MATH transitions and
MODELED/PROJECTED chips; sheets + master tracker cascade in place; committed to the GitHub source of truth;
links posted to `#tasklet-jaideep`.
