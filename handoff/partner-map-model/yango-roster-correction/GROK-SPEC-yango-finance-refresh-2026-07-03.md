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

## Roll-up markets NOW LANDED (2026-07-04 follow-on, this PR)
Cameroon, Congo (Brazzaville), Namibia, Venezuela are now in `corridors.json` as Yango finance markets with conservative provenance-tagged L3 (11 corridors). They lift the Yango TAM. Include them in the `PARTNERS=yango` cascade above.
- `yango-namibia` (3) · `yango-venezuela` (3, capture 0.15) · `yango-cameroon` (3) · `yango-congo-brazzaville` (2).
- Corridors flagged `_needs_sourcing: true` carry **modeled** demand estimates (honest low-confidence pending firmer sourcing) — renderer should guard/label; do not treat as high-confidence. Real anchors: Los Roques ~70k visitors/yr, Walvis Bay dolphin/seal cruises, Manoka boat-only captive.
- `route_id: null` on all 11 — bind at seal; never invent route_ids.
- Do **not** run `regen` that overwrites these modeled records with global-median fallbacks.

## Cross-partner overlap — Colombia / Cartagena (Grok cascade + scope call)
See `CROSS-PARTNER-COVERAGE-MATRIX-2026-07-04.md`. Cartagena is a **shared** corridor geography. The grounded `yango-colombia` L3 (fares + Cartagena tourism demand pool) is reusable to seed overlapping partners:
- **DiDi (primary):** has the full Cartagena corridor set built but `economics_pending` and **no finance block**. Recommend instantiating `didi-colombia` by copying the `yango-colombia` corridor fare/demand records onto DiDi's own Cartagena corridors (Rosario 18.3 nm, Barú 12.2 nm, Santa Marta 92.7 nm), then applying **DiDi's** capture rate in cascade. Whether DiDi enters the transparent-sheet universe is Jaideep's scope call.
- **Cabify (light):** one built corridor — same treatment, smaller.
- **Uber / inDrive (HOLD):** Cartagena is an aspirational coverage node with no built corridors — do **not** seed economics (null beats confidently-wrong).
Tasklet has done the L3 sourcing; instantiation + capture rates are the cascade lane.

## QA gate
- Yango finance markets == 11: `uae, qatar, egypt, cote-divoire, senegal, caspian-kz, morocco, mozambique, pakistan, peru, colombia`.
- No `turkey / ksa-commercial / lagos / caspian-az / israel / tunisia` under `partner==yango`.
- Peru + Colombia present in `country-reference.countries`.
- Yango transparent sheet re-emits with Peru + Colombia rows; Norway absent; TAM ladder recomputes clean.
