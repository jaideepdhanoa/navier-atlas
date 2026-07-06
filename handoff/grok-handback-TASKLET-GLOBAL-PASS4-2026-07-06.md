# Grok Handback — Global Pass 4 (Scope-Key Normalization)

**Lane:** `global-inheritance-pass4`  
**Date:** 2026-07-06  
**Status:** ✅ Complete — gates green (careem/noon skipped per directive)

## What was done

Pass 4 normalizes `_map_scope.registry_keys` across 18 commercial partners so `partner ∩ global` inheritance lights up wherever sealed geometry already exists.

### 1. Resolution algorithm (`scripts/grok-global/scope_key_resolution.py`)

Ordered pipeline: **hygiene → direct → city-member → normalize → classify**

- `P4-ALIAS-MAP.json` — 12 spelling-only aliases (underscore→hyphen, UAE sub-keys)
- `P4-CITY-MEMBER-MAP.json` — 49 shorthand→canonical city/cluster mappings (fixed `kota-kinabalu`→`sabah-kota-kinabalu-malaysia`, `tioman`→`tioman-island`, added `phuket`→`phuket-phang-nga-thailand`)
- `P4-PREFIX-JUNK.json` — 15 partner-prefix duplicates dropped (no prefix stripping)
- `P4-UNKNOWN-DROP.json` — 32 keys with no geometry (+ `bolt-france-riviera`)
- `P4-YANGO-LOCKED-NON-MARKETS.json` — Turkey/KSA/Norway gate

### 2. Apply (`scripts/grok-global/apply_scope_key_normalization_pass4.py`)

Updates per partner:
- `registry_keys` → canonical cluster/city keys
- `cluster_city_ids` → expanded from resolved keys + cluster membership
- `contested_cluster_ids` → aligned to resolved clusters
- `aspirational_registry_keys` → unsealed-registered keys (phuket-andaman, yango accra/lobito)
- `scope_key_resolution` audit block

### 3. Hard gate (`scripts/validate_scope_resolution.py`)

Every key must resolve, be aspirational, or be dropped. Fails on:
- Silent-dark markets (geometry exists but scope lacks cities)
- Yango keys resolving to Turkey/KSA/Norway
- Hygiene keys still in `registry_keys`

## Results (high-signal)

| Partner | Keys before→after | Cities | Dropped | Aspirational |
|---------|-------------------|--------|---------|--------------|
| rapido | 8→1 | 9 | 4 | 0 |
| lyft | 24→9 | 34 | 1 | 0 |
| bolt | 92→21 | 107 | 16 | 0 |
| uber | 74→25 | 99 | 21 | 0 |
| yango | 43→16 | 50 | 2 | 2 |

**View-parity wins:**
- **rapido** — `mumbai`, `goa`, `kerala`, `andaman` now in `cluster_city_ids` (was 2 cities)
- **lyft** — `new-york`, `hawaii-usa`, `bay-area`/`san-francisco-bay-usa`, `miami` resolved
- **bolt/uber** — partner-prefix junk (`bolt-greece`, `yango-turkey`, etc.) dropped; city keys normalized

## Gates

| Gate | Result |
|------|--------|
| `validate_scope_resolution.py --strict` | 18/18 applied partners OK (careem/noon skipped) |
| `validate_partner_inheritance.py --strict` | 20/20 OK |
| `update_seal_hashes.py` | SEAL.json refreshed (ROUTES d329bb18… 4267) |

Receipt: `grok-routing-output/global-inheritance-pass4-report.json`

## Skipped — pending Jaideep confirm

**careem + noon** `_map_scope.registry_keys` collapsed to `["uae"]` only (1 key each). Both are MENA-wide — possible regression from UAE unification. **Not touched** per directive.

## Sealing (Tasklet lane)

204 unsealed-registered keys tagged aspirational where applicable. **Maghreb seal (PR #185)** remains top priority — Morocco/Algeria/Tunisia geometry will light up yassir/indrive on merge. India thin markets (chennai/kerala/kolkata) → sourcing.

## Guardrails held

- No invented geometry
- null-beats-wrong
- No partner-prefix stripping (`yango-turkey` dropped as junk, not aliased to `turkey`)
- Yango Turkey/KSA/Norway stay locked out

## Runbook

```bash
bash scripts/grok-global/run_scope_key_pass4.sh
```

Or stepwise:
```bash
python3 scripts/grok-global/apply_scope_key_normalization_pass4.py --apply
python3 scripts/validate_scope_resolution.py --strict
python3 scripts/validate_partner_inheritance.py --strict
```