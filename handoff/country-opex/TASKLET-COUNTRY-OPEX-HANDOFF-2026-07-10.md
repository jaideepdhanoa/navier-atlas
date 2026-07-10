# Tasklet handoff — missing country opex (2026-07-10)

## Ask

Source and seal **crew / energy / grid CO₂ / berth admin / cost index** for the countries below into:

`finance/model/country-reference.json` → top-level key `countries.<Country Name>`

**Do not invent rates.** If evidence is weak, leave the country out (null beats wrong). Sheets already fail-loud on fallback.

Machine inventory: [`MISSING-COUNTRY-OPEX-INVENTORY.json`](./MISSING-COUNTRY-OPEX-INVENTORY.json)  
Rebuild after seal: [`../../finance/REBUILD-AFTER-COUNTRY-OPEX.md`](../../finance/REBUILD-AFTER-COUNTRY-OPEX.md)

---

## Countries needing rates (true gaps)

| Country (exact key) | Corridor rows (approx) | Partners |
|---------------------|------------------------|----------|
| **South Korea** | 123 | swing, naver, kakao-mobility |
| **Namibia** | 3 | yango |
| **Venezuela** | 3 | yango |
| **Cameroon** | 3 | yango |
| **Congo (Brazzaville)** | 2 | yango |
| **Argentina** | 2 | didi |
| **Costa Rica** | 2 | didi |

Use these **exact strings** as JSON keys (match corridor `country` fields).

---

## Schema (copy Singapore shape)

```json
"South Korea": {
  "captain_usd_yr": {
    "value": 0,
    "source_tier": "T1",
    "confidence": "med",
    "source": "…evidence…"
  },
  "energy_usd_kwh": {
    "value": 0.0,
    "source_tier": "T1",
    "confidence": "high",
    "source": "…evidence…"
  },
  "grid_co2_kg_kwh": {
    "value": 0.0,
    "source_tier": "T2",
    "confidence": "med",
    "source": "…evidence…"
  },
  "marina_overhead_usd_yr": {
    "value": 0,
    "source_tier": "T5",
    "confidence": "low",
    "source": "…evidence…"
  },
  "cost_index": {
    "value": 1.0,
    "confidence": "med"
  }
}
```

### Live example — Singapore (already sealed)

| Field | Value | Notes |
|-------|------:|-------|
| captain_usd_yr | 48000 | Modeled SG marine crew |
| energy_usd_kwh | 0.21 | Regulated tariff |
| grid_co2_kg_kwh | 0.4 | Gas-fired grid |
| marina_overhead_usd_yr | 20000 | High-cost berth modeled |
| cost_index | 1.0 | Index baseline |

Full object is in inventory JSON (`schema_example_singapore`).

### Source tiers

| Tier | Meaning |
|------|---------|
| T1 | Official tariff / regulator / national stats |
| T2 | Reputable secondary (IEA, utility filings) |
| T3 | Industry band / peer market |
| T4 | Analog from similar country (document analog) |
| T5 | Modeled — mark confidence low |

---

## Already fixed without new rates (Grok 2026-07-10)

| Legacy label | Resolution |
|--------------|------------|
| `USVI / BVI` | → `U.S. Virgin Islands` (origin-primary dual-leg; BVI also in ref) |
| `CrossBorder` | → `Singapore` (R16 home-port; current set is SG-origin) |

Resolver: `finance/model/country_opex_resolve.py`  
Lint: `python3 finance/lint_country_opex.py`

---

## Partner impact / rebuild after you seal

| Partner | Sheet | Action after seal |
|---------|-------|-------------------|
| swing | `1PxUtIzZ…` | rebuild + publish (was full Singapore opex) |
| naver | `1Xv-qS4…` | rebuild + publish |
| kakao-mobility | **none** | **hold** until SK sealed — do not publish SG-fallback sheet |
| yango | `1fvB_tc8…` | rebuild if any of NA/VE/CM/CG sealed |
| didi | `1LY0Vp7…` | rebuild if AR + CR sealed (or partial with remaining fallback banner) |
| caribbean-mobility | `1J9rb-rA…` | optional republish (label fix only) |

```bash
bash scripts/grok-econ-reseal/rebuild_after_country_opex.sh --strict-check
bash scripts/grok-econ-reseal/rebuild_after_country_opex.sh --build
# credentials:
bash scripts/grok-econ-reseal/rebuild_after_country_opex.sh --publish
```

---

## Process changes already in mainline worktree

1. **Fail-loud fallback** — `build_transparent_sheet.py` prints stderr warnings, Read-me + Country opex banners; `--strict-country-opex` exits 2.
2. **aggregate.py** — writes `_opex_country_resolution` and stderr on fallback.
3. **Lint** — `finance/lint_country_opex.py`.
4. **Partner inventory seals** — `_opex_country_status.opex_country = singapore_fallback` where still missing.

---

## Parallel backlog (not blocked on this Tasklet)

| Item | Status |
|------|--------|
| Wave1 mints (Belgium, Basel, Zürich, Solent, DE, Nordics, Le Havre, PL, AT/HU, …) | **Held** — coords null; null beats wrong |
| DiDi Colombia C / other geography holds | Unchanged |
| Local Vercel large upload TLS | Broken — use `gh workflow run deploy-dist.yml` only |
| Kakao economics sheet create | Blocked on South Korea opex |

---

## Acceptance

- [ ] Each listed country present under `countries` with all five fields + source notes  
- [ ] `python3 finance/lint_country_opex.py` clean for sealed set (or only remaining intentional gaps)  
- [ ] Affected partner sheets rebuilt; Read-me has **no** COUNTRY OPEX FALLBACK banner for sealed partners  
- [ ] Kakao sheet created only after South Korea is sealed  
