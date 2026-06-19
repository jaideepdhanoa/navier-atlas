# LB-242 Notes — route_water_allowlist.json

Generated: 2026-06-18

## Deliverables

| File | Purpose |
|------|---------|
| `data-clean/route_water_allowlist.json` | Gate hook — `postflight.sh` subtracts `ids` from Tier A + Tier B |
| `data-clean/qa_baseline.json` | Frozen Tier-B baseline (4818 flagged @ 0.05 km) |
| `data-clean/SEAL.prior.json` | Frozen Tier-A geom-hash reference |
| `grok-routing-output/restored-routes-LB-242.json` | 3 scrubbed legit routes to merge back into ROUTES |
| `grok-routing-output/build_route_water_allowlist.py` | Reproducible builder |

## Tier-B math

| Metric | Value |
|--------|------:|
| Baseline flagged | 4818 |
| Allowlisted | 4791 |
| Denied (active Grok fixes) | 25 |
| **Effective flagged** | **25** |

Denied ids = `route-requests.jsonl` resolve `route_id`s (20 densify + 6 ICS + `edge-0684`). These stay gate-visible while Phase 3 geometry apply is in flight.

Palm-9 + Hud synthesize rows are not in baseline (not minted yet) — they will enter via Tier A on apply.

## Categories (allowlisted)

| Category | Count |
|----------|------:|
| global_inland_water_fp | 4394 |
| palm_archipelago | 289 |
| bora_bora_lagoon | 58 |
| penghu | 27 |
| mafia_channel | 14 |
| belize_lagoon | 8 |
| great_lakes | 1 |

Classification: route-id regex + geometry bbox overlap against known FP water bodies.

## Restored routes (LB-240 scrub undo)

Merge `restored-routes-LB-242.json` features into ROUTES before reseal:

1. `e__chicago-lake-michigan-usa__dusable-harbor-chicago__new-buffalo-municipal-marina`
2. `e__belize-city-cayes-belize__belize-city-water-taxi__placencia-belize__placencia-village-pier`
3. `e__mafia-tanzania__kilindoni-port__dar-es-salaam-tanzania__dar-ferry-terminal`

## Tasklet apply

1. Commit/copy `route_water_allowlist.json` + gate refs into canonical `data-clean/`
2. Merge 3 restored route features
3. Run `postflight.sh` — expect Tier B effective ≈ 25 (was 4818)
4. Proceed with Phase 3 candidate apply → #79al