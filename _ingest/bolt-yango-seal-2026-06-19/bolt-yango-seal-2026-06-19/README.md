# Grok handoff — Bolt/Yango new-market seal + coverage backfill (2026-06-19)

Source of truth = GitHub `main`. This zip is the **input package** for the deterministic seal.
Read `docs/GROK-PROMPT.md` for the full instruction; this README is the contents map.

## Contents
| Path | What it is | Grok action |
|---|---|---|
| `docs/GROK-PROMPT.md` | The handoff prompt (coverage mandate, gates, acceptance) | Execute it |
| `boarding-points/*.json` | **All 215 BP files** (full set, not a delta) | ID-match → seal POIs; **0 silent drops** |
| `inputs/BP-COVERAGE-GAP-2026-06-19.json` | Audit: 786 BP gap, 35 zero-POI cities, ghost-endpoint cities | Reconcile to 0 silent drops |
| `inputs/bp_water_allowlist.json` | LB-242 water/land-crossing allowlist | Fold into routing/mask gate |
| `inputs/seal-manifest.json` | Per-partner markets/countries/corridor counts from finance corridors.json | Inherit country tags + cross-partner overlap |
| `inputs/corridors.json` | Finance economic corridors (source of truth for country tags) | Reference for tagging/overlap |
| `inputs/economics_url_map.json` | **`economics_url`** render-contract field per partner (published Sheet URLs) | Bind to partner view + TAM-ladder rungs |
| `inputs/build_economics_sidecar.py` | Route-keyed econ sidecar builder | Run against NEW gold → `economics_by_route_id.json` |
| `partners/bolt.json` | Bolt partner surface (has `growth_case` TAM ladder; **stale census provenance — refresh**) | Reseal with corrected economics |
| `partners/bolt-scope.json` | Bolt: 18 markets to extend story scope to | Derive `scope_city_ids` via ID-match |
| `partners/yango-scope.json` | Yango: 15 markets, net-new story + PARTNER_VIEWS entry | Stand up view skeleton |
| `subproposals/SCAFFOLD-ALL.json` | **Per-market phase + vessel-sizing scaffold for all 18 Bolt + 16 Yango markets** (range-gated; real node_ids; `route_id` null) | Splice phases into each market sub-page; **bind `route_id` + `model_link` during seal** |
| `subproposals/VESSEL-REGATE-LEDGER.json` | 27 corridors whose `vessel` violated the range gate (now corrected) | Apply corrected hulls; never a long leg on a 70nm boat |
| `subproposals/AUTHORED-ALL-33-markets.json` | **ALL 33 full Grab-depth sub-proposals — 18 Bolt + 15 Yango** (narrative + range-gated phases; QA-clean) | Splice each as a complete market sub-page |
| `subproposals/AUTHORED-yango-hub.json` | **Yango partner hub page** (Dubai-HQ'd framing; markets roster; growth_case = GROK_BIND) | Stand up the Yango partner view from this |
| `subproposals/build_scaffold.py` | The deterministic re-gate + phase generator | Reference |

## The three confirmed directives (Jaideep, 2026-06-19)
1. **Bolt scope-extension + Yango full stand-up ride THIS reseal** (not a follow-on).
2. **`economics_url`** is the render-contract field — bind it to the partner view **and into the
   growth story so TAM-ladder rungs deep-link straight to the live economics Sheet.**
3. **Include ALL boarding points** — 786 are currently unsealed; every BP is sealed OR ledgered with a reason.
4. **Every market is a FULL per-market sub-proposal (Grab/Uber pattern), not a roll-up stub** — with `phases`
   (Prove→Scale→Mature) and **range-gated vessel sizing per phase** (≤70nm Pioneer II / 75–150nm Quanta-LR /
   >150nm flagged). Tasklet authors the narrative (batch 1 = Bolt Spain/Egypt/Sweden here; rest follow); the
   scaffold supplies the deterministic phase + vessel structure with real node_ids. Grok binds `route_id` +
   `model_link` and reconciles per-phase boat counts to the model.

## Division of labor
- **Tasklet owns:** research, financial model, growth-story narrative content, corrected economics, this package.
- **Grok owns:** ID-match/gazetteer promotion, BP↔BP graph, water + land-crossing gates, cascade/dedupe/
  density-cap, reseal to next gold tag, push to `main`, QA report. **economics_by_route_id.json built against new gold.**

## Acceptance (Grok QA report must show)
- BP coverage: **0 silent drops**; 35 zero-POI cities + ghost-endpoint cities resolved.
- 0 land-crossings (post-allowlist); 0 orphan routes; every surviving BP carries a source id.
- bolt/yango carry corrected economics (no stale census provenance).
- `economics_url` wired; TAM-ladder rungs deep-link to the economics Sheet.
- Counts: BPs sealed/dropped(+reason), routes built/culled, before/after POI total, land-crossing=0 proof.
