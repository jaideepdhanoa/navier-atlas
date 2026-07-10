# Cross-border country opex policy

**Sealed:** 2026-07-10  
**Code:** `finance/model/country_opex_resolve.py`  
**Agg rule history:** R16 home-port (Singapore default) in `aggregate.py`

## Principles

1. **One VLOOKUP country per corridor** (transparent sheet / atom opex inject).  
2. **Null beats wrong** for *rates*; process defaults must be **labeled**.  
3. Prefer rewriting durable `corridor.country` to a real country-reference key.

## Policies

### A) Dual-leg, both endpoints known (`dual_leg_origin_primary`)

Example: St. Thomas (USVI) → Tortola (BVI).

- `country` = **origin** country-reference key (`U.S. Virgin Islands`)  
- Metadata: `_country_opex_policy.counterpart` = destination country  
- Both keys should exist in country-reference when possible  

### B) Cross-border home-port (`cross_border_r16_homeport`)

Example: Singapore → Desaru / Bintan / Batam / Tioman.

- Vessel **home-port** country drives opex (R16)  
- Current durable rewrite: `CrossBorder` → `Singapore` + policy metadata  
- Destination (Malaysia / Indonesia) may differ; dual-leg review is optional later  

### C) True missing country (`r16_homeport_fallback`)

Example: `South Korea` not in country-reference.

- Opex temporarily uses Singapore  
- **Fail-loud**: stderr, sheet banners, lint exit 1  
- **Not** a substitute for sealing real rates  

## Anti-patterns

- Silent `country = Singapore` with no banner (fixed 2026-07-10)  
- Composite labels like `USVI / BVI` that are not cref keys  
- Publishing partner sheets for a market whose only country is on fallback (Kakao hold)
