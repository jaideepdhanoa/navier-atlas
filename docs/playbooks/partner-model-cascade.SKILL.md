---
name: partner-model-cascade
description: Deterministic pipeline for Navier partner unit-economics. Use when anything affecting partner economics changes (new partner, corridor, demand/parameter update, geometry binding) to cascade it through model, partner JSON, sheet, and master tracker.
---

# Partner model cascade

The single source of truth for "when economics change, what do I run and in what order." Tasklet owns
source-backed country/city/BP research, demand/fare assumptions, and model building; Grok owns deterministic route sealing, render-check, and building the sidecar into the gold zip.

**Completion-status rule:** do not call economics or a proposal complete until the full chain exists: Tasklet research evidence → Grok route IDs/render QA → Tasklet country-reference/model/growth/sheet cascade → Grok/data-clean/economics sidecar → delivery receipt. If city/BP evidence or demand/fare assumptions are still missing, the status is `research-needed`, not `ready` or `complete`.

All scripts live in `/tasklet/agent/home/navier/finance/` (model engine in `finance/model/`).

## When to run this

Trigger the cascade whenever any of these change:
- **New partner** to materialize (deck-only → modeled). → start at §A.
- **New corridor / boarding-point binding** (e.g. a Bucket-C geometry pass lands). → start at §B from the affected partners.
- **Demand update** (`L3_locals.L3_locals`/fare/`_demand_record` edits in `corridors.json`). → §B.
- **Parameter change** (`vessel-constants.json`, `growth-config.json`, capture rate). → §B for **every** partner (global blast radius).

## Golden rules (exactness over coverage)

1. **Market keys are `partner-geography`.** Never a partner name as a geography. No catch-all / "rollup" / "TBD"
   pseudo-geographies in `corridors.json` — enumerate the real places instead. (The `yango-*-rollup` buckets were
   removed 2026-06-19 for exactly this reason; deck-side breadth lives in the partner JSON's `roll_up_markets[]`.)
2. **Null beats confidently-wrong.** A partner with **no geometry-ready overlap materializes nothing** and stays
   deck-only. Proven examples: DiDi (LatAm only, zero bound geometry) and Soneva/Six Senses/Villa/Sun Siyam
   (resort islands not yet bound in `maldives-jih`). Do not fabricate a number to fill a cell.
3. **Greenfield: never borrow a *peer's* census; the global template band is OK when labelled (LB-250).**
   The fatal trap is silently inheriting another partner's specific census — e.g. Bolt/Yango with no census of
   their own pulled `grab-greenfield-census.json` at Grab's 4.9× width and spuriously hit "Grab parity." That is
   confidently-wrong. Two acceptable modes:
   - **Partner has its own census →** greenfield ON with that census.
   - **Partner has no census (most non-Grab partners) →** greenfield ON using the **global template band
     (3.44 / 4.9 / 6.36)**, *clearly labelled a template assumption pending a partner-specific census* — NOT
     presented as a measured count. (Jaideep 2026-06-19: our sourced network under-counts real crossings, so a
     labelled greenfield band belongs in the headline; an exact match to a peer's TAM is then a template artifact,
     say so.) Swap in a real census when one exists.
   - **Never** point a partner's census at another partner's census file. If you can't label the width honestly,
     fall back to the grounded floor only.
   The **grounded SOM floor is greenfield-independent** (demand × fare × capture), so it never moves with this lever
   — use it as the invariant when sanity-checking a greenfield change.
4. **Shared network, not copied.** The global corridor network is shared across partners. Inheriting partners get a
   **scoped view** of it (written to `/tmp`), never a duplicated copy in the durable `corridors.json`.
5. **Prefer the commercial/grounded corridor version** over a sovereign `_forward_sam` (future-dated) copy when the
   same corridor exists in multiple markets — `grounding_score()` in `materialize_partner_economics.py` does this.
6. **In-place edits only.** Edit `corridors.json` and Google Sheets in place; live Slides via the Slides API; no
   full-replace / PPTX round-trip.
7. **Two cost engines must agree (LB-243/250).** Economics are computed *twice*, independently: the model
   (`aggregate.py`) and the standalone transparent sheet (`build_transparent_sheet.py`). Every global cost rule
   (opex, greenfield width, CAPEX) lives in **both**, and each has its **own** per-partner override map (e.g. the
   sheet's greenfield override block, ~L520). After any global rule change, verify the partner JSON and the sheet
   tell the *same* story — a mismatch ships a deck that contradicts its own backing sheet.
8. **Every partner country needs a `country-reference.json` row (LB-243).** Both engines silently fall back to
   **Singapore** opex/energy/grid-CO₂/crew/marina costs for any country missing from `model/country-reference.json`.
   That is invisible and confidently-wrong (it once put Singapore captain salaries on Greece, Croatia, Senegal…).
   Before cascading a partner with new markets, run the preflight in §B.0. Add honest source-tiered rows for any
   gap, *then* cascade.
9. **CAPEX is region-keyed for commercial, $1M for hospitality (LB-243 + LB-260):**
   - **Commercial / ride-hail (region rule, LB-243):** **US + EU = $900K/vessel; everywhere else = $600K.** Keyed on
     the corridor's country in `aggregate.py`, rendered as a **per-country CAPEX column** in the transparent sheet
     (payback/depreciation look it up by country — not a single global CAPEX cell).
   - **Hospitality / captive-luxury (LB-260, Jaideep 2026-06-24):** **$1M/vessel — the N30 luxury hull direct-sale
     list price, region-independent.** This is the standard going forward for hospitality/captive-luxury proposals
     (French Polynesia, Ocean Whisperer, Minor Hotels, …) and **OVERRIDES** the region rule. Mechanism: mark the
     market `"capex_tier": "hospitality"` in `corridors.json` → `aggregate.py:capex_for(country, market_obj)` returns
     $1M; the transparent sheet must be built with **`--capex-tier hospitality`** so both engines tell the same story
     (golden rule #7). For a partner that scopes a *shared* market (e.g. Minor on `maldives-jih`), tag the **scoped
     view** rather than the durable shared market so other inheritors aren't blasted.
   - CAPEX only shifts payback/margin, never the SOM/SAM revenue rungs or fleet counts. Changing either tier is
     global within its class — re-cascade every affected partner.

10. **Vessel is range-gated, and the registry drifts (LB-252).** Every corridor's hull follows the gate: **≤ 70nm →
   Pioneer II** (N35 Shuttle on dense legs at scale); **75–150nm → Quanta-LR** (roadmap, amber); **> 150nm → Quanta-LR
   flagged for review** — a long leg is *never* left on a 70nm boat. The `vessel` field in `corridors.json` drifts
   (long legs mislabelled `Pioneer II`, casing like `pioneer-ii`/`quanta-lr`); **re-gate on every cascade** via
   `partner-pitch/subproposals/build_scaffold.py`, which normalizes hulls and emits a `VESSEL-REGATE-LEDGER`. This
   feeds the per-phase vessel sizing on partner sub-pages (see partner-proposal-parity Gate C.1).

11. **The TAM-ladder capture MUST equal the capture that built the floor — captive ≠ contested (LB-254, Jaideep
    2026-06-19).** The single deadliest sizing bug. The growth ladder anchors on `M_today` (the total transport-spend
    pool); every rung is one multiplication off it. The **old, wrong** way recovered the pool by `M_today =
    SOM_floor / 0.10`, hard-coding a **contested** 10% capture. But **captive** corridors (`captive:true` /
    `luxury_charter` / `hospitality` — Maldives/JIH, Red Sea, French Polynesia, captive resort transfers) build the
    floor at **~90% capture**. Dividing a 90%-capture floor by 0.10 inflates `M_today` and **every rung ~9×** — e.g.
    JIH journey-GMV TAM read **$23B** (4× the entire Maldives tourism economy) instead of ~$2.6B.
    - **The rule in one line:** *at 90% capture the floor already IS ~the whole pool; you cannot also multiply it by
      10. Pick one.* Headroom for captive markets is **induced demand + greenfield WIDTH (more guests, more islands)**,
      **never** a 10×→capture-share expansion.
    - **The fix (now in the engines):** `aggregate.py` emits per-market `transport_spend_pool_yr` (Σ demand×fare) and
      `effective_capture` (= floor/pool: ~0.90 captive, ~0.10 contested, blended for mixed). `growth.py` anchors
      `M_today = transport_spend_pool_yr` (legacy `floor/som_capture` only as a fallback for pre-LB-254 aggs) and
      clamps **mature capture ≥ floor capture** (captive markets get a flat floor-capture band + a thin 0.95 lock-up
      ceiling; contested unchanged). The contested **0.15/0.25/0.40 ramp is wrong-signed for captive** (it implies
      maturing *down* from 90%).
    - **All FOUR surfaces must carry it (grep for hard-coded `0.10`/`/0.1`/"10% capture"):** `growth.py`,
      `splice_growth_into_partner.py` (`build_ladder_transitions`), `growth_frontend_block.py`, and the standalone
      `build_transparent_sheet.py` Market-sizing tab (golden rule #7 — the second engine reads `effective_capture`
      from the agg via `--agg`). A miss ships a deck that contradicts its own backing sheet.
    - **The floor never moves** — it's the honest grounded number we actually sell. Only the inflated upper rungs come
      down. Sanity gate: a captive market whose **journey-GMV TAM exceeds its country's whole tourism economy** is the
      tell. **Bespoke/stale builds** (e.g. Saudi-PIF / Red Sea Global anchor on a 2030 forward-SAM bucket, not a
      grounded floor) do NOT re-cascade from a naive `--partner` run — reconcile their original build before applying.

## §A — Materialize a new partner (deck-only → modeled)

Use `materialize_partner_economics.py` to build a `/tmp/corridors-<partner>.json` **scoped view** of the shared
network. First check the partner's real overlap in `finance/partner_geography_matrix.json` (`geometry_ready` /
`needs_minting`). Pick the mode by archetype:

- **Ride-hail / super-app → `inherit-markets`** (PARITY). Mirror the peer markets so the new partner's per-country
  scope exactly matches Bolt/Yango — no cross-track union, no double-count of sovereign demand:
  ```
  python3 materialize_partner_economics.py --partner uber --mode inherit-markets \
    --source-markets "bolt-uae,bolt-ksa-commercial,bolt-qatar,bolt-greece,bolt-croatia,bolt-italy,bolt-france-riviera,yango-egypt,yango-turkey,yango-lagos"
  ```
  (Uber → $26M grounded floor, parity with Bolt+Yango. `inherit-country` exists too but UNIONs every partner's
  corridors for a country and over-counts — only use it when there is exactly one source treatment.)
- **Hospitality brand → `captive-maldives`** (villa-scoped). Filters the `maldives-jih` captive corridors to the
  brand's own resort islands via `jih-villa-counts-*.json`, so a 2-resort brand never inherits the archipelago fleet:
  ```
  python3 materialize_partner_economics.py --partner four-seasons --mode captive-maldives --brands "Four Seasons"
  ```
  If a brand's resorts aren't in the bound `maldives-jih` set, it materializes **nothing** (honest null) until a
  resort-corridor binding pass lands.

The driver exits 3 and prints "NOTHING to materialize" when there's no geometry-ready overlap — that's a correct
outcome, not an error.

## §B — The cascade (run for each affected partner `P`)

Engine reads `corridors.json` by default; pass `--corridors /tmp/corridors-P.json` for a scoped-view (inheriting)
partner. Run from `finance/model/` unless noted. `openpyxl` isn't preinstalled → run sheet builders via
`uv run --with openpyxl python3 ...`.

**§B.0 — Preflight: country-reference coverage (do this before step 1 whenever P has new markets).**
Catches the silent Singapore-opex fallback (golden rule #8). Add honest rows for any miss, then proceed.
```
python3 - << 'EOF'
import json
corr=json.load(open('corridors.json'))['markets']
cref=set(json.load(open('country-reference.json'))['countries'])
P='bolt'  # set to the partner you're cascading
need={m['country'] for k,m in corr.items() if k.startswith(P+'-') for c in [m] }  # adapt to your shape
print('missing from country-reference:', sorted(need - cref) or 'none ✅')
EOF
```

```
# 1. aggregate corridors → rollup (grounded floor + cascade-estimated upside)
#    FOOTGUN: the output flag is --json (NOT --out). With the wrong flag it prints to stdout and silently
#    leaves the OLD agg-P.json in place. After running, confirm the file's mtime moved and spot-check a value.
python3 aggregate.py --partner P [--corridors /tmp/corridors-P.json] --json ../recal/agg-P.json

# 2. growth ladder (SOM floor → SAM depth → TAM journey-GMV → partner platform revenue)
#    --greenfield: 'off' = grounded floor only; default census band = labelled template upside (golden rule #3).
#    Use the global template band for partners with no census; never point at a peer's census file.
python3 growth.py --partner P --agg ../recal/agg-P.json [--greenfield off] --json ../P-growth-case.json

# 3. frontend block (phase economics for the deck/partner page)
python3 growth_frontend_block.py --partner P --growth ../P-growth-case.json --rollup ../recal/agg-P.json \
        --out ../../partner-pitch/partners/_growth-draft/P.growth.json

# 4. splice growth_case + frontend into the partner JSON (preserves phases/featured_routes/committed_fleet)
cd .. && python3 splice_growth_into_partner.py --partner P --growth P-growth-case.json \
        --frontend ../partner-pitch/partners/_growth-draft/P.growth.json

# 5. transparent unit-econ sheet (formula-driven, standalone) — xlsx
uv run --with openpyxl python3 build_transparent_sheet.py --partner P --out /tmp/P_unit_econ.xlsx

# 6. master tracker (one row per partner). Add P to the SHEETS list in build_master_sheet.py with its
#    Google-Sheet ID from PARTNER-SHEET-IDS.json. It reads /tmp/agg-<partner>.json, so stage them:
cp ../recal/agg-*.json /tmp/ && uv run --with openpyxl python3 build_master_sheet.py
```

`growth.py` headline ladder (MID): **SOM floor → SAM Navier transport rev → TAM journey GMV → partner platform
revenue**. Sanity-check the floor against peers (ride-hail partners sharing UAE/KSA/Qatar should land near the same
~$25–26M Gulf floor; a 10× gap means a dedup/flag bug — investigate before shipping).

## §C — Delivery & sidecar

- **Economics sidecar** (`economics_by_route_id.json`) is built **into every gold zip** — this is Grok's
  seal lane now (`build_economics_sidecar.py --gold <data-clean> --aggdir <aggs> --out ...`). Hand it the refreshed
  `agg-*.json`; don't build/seal locally.
- **Finance/gold exports** → share as the approved Drive/Sheets links and post to `#tasklet-jaideep`. Upload sheets
  in place to the existing Sheet IDs (Google Drive connection) — don't create new files. In-place update =
  `google_drive_upload_file` with `fileIdToReplace` (from `PARTNER-SHEET-IDS.json`) — this preserves the URL.
  **Staging footgun:** the upload tool only reads paths under `/tasklet/`. Building xlsx in `/tmp` then uploading
  from `/tmp` fails — copy to a `/tasklet/...` staging dir (`finance/_sheet_out/`) first.
- **External outreach stays draft.** Internal Slack + approved Drive uploads are allowed.

## §E — The front end is a SEPARATE world (don't stop at the sheet)

Cascading economics refreshes the **Sheets + master tracker** only. It does **not** update the **Atlas
front end** (the live map + partner hub/spoke pages) — that's a separate render graph Grok seals from
`atlas-external/boarding-points/*.json` → `atlas-repo/data-clean/`. After any cascade that adds or changes
**geography** (new partner, market, corridor, or boarding points), the front end is **stale** until you
hand the new graph + corrected economics to Grok to reseal. Tell-tale: `data-clean/partners/<P>.json`
still shows old `census` / `*-aggregate` provenance, or new markets are missing from `ROUTES.json`.

→ Run the **`grok-seal-handoff`** skill: assemble the input zip (all BPs + coverage audit + LB-242
allowlist + seal manifest + `economics_url` map + sidecar builder + partner scope specs), post to
`#tasklet-jaideep`. That skill also covers the **`economics_url`** field that deep-links the TAM ladder to
the live economics Sheet, and the **"0 silent drops" BP coverage audit** so researched boarding points
never vanish silently.

## §D — Hygiene

- Stage large JSON writes durably, then atomic copy/sync. The durable store enforces an **inode + byte quota**; if a
  write fails with "Disk quota exceeded", delete **more regenerable files than you add** (old `recal/*.bak*`
  snapshots, superseded gold builds, regenerable deck renders) and retry.
- Keep only the newest gold build. Keep learnings in the ledger / reusable recipes.
- Back up before destructive edits (`cp corridors.json /tmp/corridors.pre-<change>.bak.json`).
