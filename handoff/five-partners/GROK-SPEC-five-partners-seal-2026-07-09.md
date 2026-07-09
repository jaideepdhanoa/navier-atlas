# GROK SPEC — Five new partners: seal + scope derivation (2026-07-09)

## Partners (all proposal JSONs committed, Gates F+G green, schema-passing)
| partner | archetype | geography spine | markets (full sub-pages) |
|---|---|---|---|
| marti | super_app | Turkey (canonical `turkey` cluster) | istanbul, izmir-cesme, bodrum, antalya (4) |
| swing | super_app | South Korea (kakao-mobility spine) | korea (Seoul/Busan/Jeju) |
| naver | super_app | South Korea (kakao-mobility spine) | korea (Seoul/Busan/Jeju) |
| dott | ridehail | EMEA (bolt spine) | uae, ksa-commercial, greece, italy, spain, finland, france-riviera (7) + israel roll-up (held — sovereign coordination) |
| voi | ridehail | EMEA (bolt spine) | sweden, finland, italy, spain, france-riviera (5) |

## Grok lane (deterministic)
1. **Scope derivation:** run `scripts/partner-scope.mjs` for each new partner — `_map_scope.registry_keys` are committed; derive `source: live_cluster_inheritance` membership. Corridor inheritance contract applies 1:1 (no curation, no new geometry).
2. **data-clean build:** `data-clean/partners/{marti,swing,naver,dott,voi}.json` from partner-pitch sources; run `validate_partner_inheritance.py` + `validate_finance_inheritance.py`.
3. **route_id verification:** all featured_routes carry canonical `rn-` ids inherited from ROUTES.json (marti: Istanbul/İzmir/Bodrum/Antalya; swing/naver: 3 Seoul canonical `bp-kakao-*` corridors; dott/voi: bolt-market canonical). Null beats wrong — flag, never mint here.
4. **Economics sidecar:** rebuild `economics_by_route_id.json` with the five new `agg-*.json` (committed in `finance/recal/`).
5. **Gate G re-run** on generated data-clean files: `scripts/audit_partner_copy.py` must PASS.

## Guardrails
- **Dott israel market = held-sovereign-coordination** (`sovereign_data_only: true` in `finance/recal/corridors-dott.json`). Roll-up only — do NOT promote to map/sub-page. Haifa↔Limassol 147.1nm leg must be Quanta-LR if ever surfaced (mis-vesselled Pioneer II in the archived source; re-gate applies).
- **No Turkey on Yango surfaces** — marti is the ONLY partner surfacing turkey clusters besides global atlas.
- Greenfield for all five = global template band (labelled template assumption) — no partner census exists. Never borrow a peer census.
- Sheet IDs registered in `finance/PARTNER-SHEET-IDS.json`; `economics_url` wired in all five proposals. Master tracker rows = Grok cascade lane after seal.
