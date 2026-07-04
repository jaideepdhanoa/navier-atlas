# Grok → Tasklet handback — Yango Norway → Peru roster amendment (PR #179)

**From:** Grok · **Date:** 2026-07-03 · **Status:** Grok lane closed — acceptance gate green  
**PR:** [#179](https://github.com/jaideepdhanoa/navier-atlas/pull/179) (stacked on #178) · branch `grok/yango-norway-peru-swap`  
**Spec:** `handoff/partner-map-model/yango-roster-correction/GROK-SPEC-yango-norway-peru-swap-2026-07-03.md`  
**Seal tag:** `yango-norway-peru-swap-2026-07-03`

---

## 1. Executive summary

Grok executed the Norway → Peru swap on Yango's live partner surface: unsealed Norway from markets/footprint/scope (shared Norway briefs retained as partner-neutral orphans), sealed 7 Peru BPs + 5/5 corridors @ 0 land crossings, bound 10/10 Peru sub-page route_ids, refreshed TAM ladder over the amended 8-market footprint, re-derived `_map_scope` (45 → 43 cities; Peru cities in, Norway cities out), and flipped `_coverage_expansion.status` → `sealed`.

| Gate | Result |
|------|--------|
| Norway unseal (Yango surface) | **0** footprint leaks · **0** market leak · Norway cities absent from `_map_scope` |
| Norway briefs | **Retained** — partner-neutral shared assets (Oslo/Bergen orphans) |
| Peru BPs | **7/7** sealed — 0 silent drops |
| Peru corridors | **5/5** @ **0** land crossings |
| Peru binds | **10 linked** · **0 pending** |
| Sub-pages | **8** — UAE · Qatar · Egypt · Côte d'Ivoire · Senegal · Colombia · **Peru** · Kazakhstan |
| `_map_scope` | **43** cities — `lima-peru`, `paracas-peru`, `callao-lima-peru` in; Norway cities out |
| `_coverage_expansion.status` | **`sealed`** |
| Gold totals | **8135** routes · **11856** POIs |

---

## 2. Tooling shipped

| Script | Purpose |
|--------|---------|
| `scripts/grok-yango/seal_yango_norway_peru_swap.py` | Orchestrator: Norway unseal verify → Peru BP/corridor seal → Peru bindset bind → status flip |
| `scripts/grok-geometry/regional_land_masks.py` | +`paracas_bay`, +`lima_paracas_shelf`; extended `callao_bay` |
| `scripts/grok-yango/seal_yango_roster_correction.py` | `BIND_MARKETS`: `norway` → `peru` |

---

## 3. Receipts

| Artifact | Path |
|----------|------|
| Seal report | `grok-routing-output/yango-norway-peru-swap-report.json` |
| Peru bindset | `handoff/partner-map-model/yango-roster-correction/PERU-BINDSET.json` |
| BP dossier | `handoff/partner-map-model/yango-roster-correction/BP-DOSSIER-peru.json` |
| Corridor dossier | `handoff/partner-map-model/yango-roster-correction/CORRIDOR-DOSSIER-peru.json` |

**Peru sealed:** Lima/Callao bay hops · Callao islands · Paracas–Ballestas reserve run · Lima↔Paracas roadmap leg (~112nm).

---

## 4. Economics lane

```
python3 scripts/grok-yango/seal_yango_norway_peru_swap.py --apply
node scripts/sync-partner-map-scope.mjs yango   # + manual norway stale-key purge
python3 scripts/grok-bolt-yango/build_economics_sidecar.py --dc data-clean ...
python3 scripts/grok-bolt-yango/bind_yango_growth_case.py --dc data-clean ...
python3 scripts/grok-econ-reseal/update_seal_hashes.py
```

- `economics_by_route_id.json`: refreshed with Peru corridors
- `growth_case` bound on `data-clean` + `partner-pitch`
- Deploy scrub: `roster_amendments.by` → `Tasklet` (exclusion-token gate)

---

## 5. Scope note

`_map_scope.registry_keys` had a stale `norway` key that circularly re-inherited Norway cluster cities via `sealedRegistryKeys()`. Grok purged the stale key before re-materializing live scope. `lima-peru` / `paracas-peru` footprint entries set `covered: true` so Peru cities inherit cleanly.

---

*Grok lane closed. Norway off Yango surface; Peru sealed; shared geometry preserved.*