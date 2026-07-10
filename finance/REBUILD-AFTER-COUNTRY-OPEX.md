# Rebuild partner economics after country-opex seal

**When:** Tasklet (or Grok with sourced evidence) adds missing countries to  
`finance/model/country-reference.json`.

**Do not:** invent rates, rebuild sheets while lint still reports fallbacks for that country, or publish Kakao until South Korea is sealed.

---

## 0) Prerequisites

Each new country row needs at least:

| Field | Type | Notes |
|-------|------|--------|
| `captain_usd_yr` | `{value, source_tier, confidence, source}` | Fully loaded captain $/yr |
| `energy_usd_kwh` | same | Local electricity $/kWh |
| `grid_co2_kg_kwh` | same | Grid intensity |
| `marina_overhead_usd_yr` | same | Berth + port admin $/yr |
| `cost_index` | `{value, confidence}` | Relative to Singapore ≈ 1.0 |

See Singapore / Taiwan rows in `country-reference.json` for shape.  
`null` beats a wrong number — omit the country rather than invent.

---

## 1) Lint (must go green for the sealed set)

```bash
cd /path/to/navier-atlas
python3 finance/lint_country_opex.py
python3 finance/lint_country_opex.py --json > /tmp/country-opex-lint.json
```

Partner-scoped:

```bash
python3 finance/lint_country_opex.py --partner swing
python3 finance/lint_country_opex.py --partner naver
python3 finance/lint_country_opex.py --partner yango
python3 finance/lint_country_opex.py --partner didi
python3 finance/lint_country_opex.py --partner caribbean-mobility
```

Exit `0` = no R16 fallbacks for that scope.

---

## 2) One-shot rebuild script

```bash
# Dry-run plan (no Drive upload)
bash scripts/grok-econ-reseal/rebuild_after_country_opex.sh --dry-run

# Build local xlsx for affected partners only
bash scripts/grok-econ-reseal/rebuild_after_country_opex.sh --build

# Build + upload to existing Drive sheet IDs (needs credentials)
bash scripts/grok-econ-reseal/rebuild_after_country_opex.sh --publish
```

Default partner set (missing-opex impact as of 2026-07-10):

| Partner | Why |
|---------|-----|
| `swing` | South Korea (full network) |
| `naver` | South Korea |
| `yango` | Namibia, Venezuela, Cameroon, Congo (Brazzaville) |
| `didi` | Argentina, Costa Rica (partial ladder) |
| `caribbean-mobility` | USVI–BVI leg (label fixed; re-publish for honesty) |

**Kakao:** do **not** auto-publish. Create sheet only after South Korea is in country-ref  
(see `handoff/country-opex/KAKAO-ECON-HOLD.md`).

---

## 3) Manual equivalent (if script unavailable)

```bash
PARTNERS="swing naver yango didi caribbean-mobility"
for p in $PARTNERS; do
  python3 finance/build_transparent_sheet.py \
    --partner "$p" \
    --out "finance/_refresh_${p}.xlsx"
  # optional hard gate:
  # python3 finance/build_transparent_sheet.py --partner "$p" --strict-country-opex --out /tmp/x.xlsx
done

# Upload (preserves sheet IDs / economics_url):
# python3 -c "from finance.partner_sheet_build import publish_partner_sheet; ..."
# or finance/refresh_all_sheets.py --partners swing,naver,yango,didi,caribbean-mobility
```

Aggregate re-cascade (floors) after opex change:

```bash
for p in swing naver yango didi; do
  python3 finance/model/aggregate.py --partner "$p" --json "finance/recal/agg-${p}.json"
done
# then re-run growth / five-partner reseal path if that partner is on the sealed ladder
```

---

## 4) Partner inventory after rebuild

Clear or update `_opex_country_status` on:

- `data-clean/partners/{swing,naver,kakao-mobility,yango,didi,caribbean}.json`
- mirrored `partner-pitch/partners/*` via existing sync if used

Set `opex_country=resolved` (or drop the fallback note) only when lint is clean for that partner.

---

## 5) Do not merge rates without evidence

If Tasklet returns partial countries, rebuild **only** partners whose missing set is fully sealed. Leave others on `singapore_fallback` inventory seal.
