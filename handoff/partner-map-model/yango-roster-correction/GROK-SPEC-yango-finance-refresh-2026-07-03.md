# GROK SPEC — Yango finance refresh + optional full-partner republish (2026-07-03)

Tasklet has landed the corridor L3 + country-reference inputs. This is the **cascade + publish** lane (Grok), per `finance/README.md` division of labor.

## Inputs landed in this PR
- `finance/model/corridors.json` — Yango registry reconciled: **-6 stale markets**, **+`yango-peru` (5 corridors)**, **+`yango-colombia` (6 corridors)**; all new corridors carry grounded `L3_locals` (fare + demand, sourced). `route_id: null` on the 11 new corridors — bind at seal.
- `finance/model/country-reference.json` — **+Peru, +Colombia** opex rows (modeled, hydro-heavy grid CO2).
- Reconciliation log in `corridors.json._meta.yango_roster_reconciliation_2026_07_03`.

## Do (required)
```bash
# 1) re-cascade Yango over the corrected registry
RUN_CASCADE=1 PARTNERS=yango ./scripts/grok-econ-reseal/run_finance_sheet_lane.sh
# 2) rebind the growth_case (marine-TAM-split, Bolt/Grab parity)
python3 scripts/grok-bolt-yango/bind_yango_growth_case.py --dc data-clean
# 3) sync partner-pitch, update seal hashes, commit, redeploy
```

### Bind the 11 new corridors
- Peru: mint `route_id`s for the 5 sealed Peru corridors (from PR #179 seal — 7 BP / 5 corridors already live). Wire `route_id` where grounded; leave null if a corridor isn't minted (never invent).
- Colombia: mint/attach `route_id`s for the 6 Cartagena+Barranquilla corridors (geometry from the #178 Colombia sub-page). If Colombia BPs aren't yet sealed into the gazetteer, seal them first from the sub-page anchors, then bind.

## Do NOT
- Do **not** drop `yango-morocco`, `yango-mozambique`, or `yango-pakistan` — they ARE authoritative Yango markets (Morocco is a roll-up but still Yango). Only the 6 listed in the reconciliation log are retired.
- Do **not** invent L3 demand from geometry — it's already sourced. If you re-anchor, keep the sourced fares/pools and cite.
- Do **not** re-add the 6 dropped markets on a stale-registry fallback.

## Optional — full-partner republish (consistency)
Only Yango's numbers change from this PR (country-reference additions feed Yango only). If you want every partner sheet re-emitted for consistency:
```bash
RUN_CASCADE=1 PARTNERS=all ./scripts/grok-econ-reseal/run_finance_sheet_lane.sh
```
No other partner's roster changed, so expect zero economic delta outside Yango.

## Follow-on (not this PR)
Cameroon / Congo / Namibia / Venezuela are in the Yango footprint but finance-pending (roll-up markets). Corridor dossiers exist (#178, `handoff/partner-map-model/yango-roster-correction/`). Tasklet will source their L3 in a follow-on bite if they should lift the Yango TAM — do not auto-generate their demand.

## QA gate
- Yango finance markets == 11: `uae, qatar, egypt, cote-divoire, senegal, caspian-kz, morocco, mozambique, pakistan, peru, colombia`.
- No `turkey / ksa-commercial / lagos / caspian-az / israel / tunisia` under `partner==yango`.
- Peru + Colombia present in `country-reference.countries`.
- Yango transparent sheet re-emits with Peru + Colombia rows; Norway absent; TAM ladder recomputes clean.
