# Country-opex holds receipt — 2026-07-11

**At:** 2026-07-11T16:58:07Z
**Gate:** PASS · active **1358** · held **6** (was 1348 / 16)

## Added country-reference rows
- Costa Rica, Argentina, Namibia, Cameroon, Congo (Brazzaville)
- **Deferred:** Venezuela (no current World Bank cost_index)

## Corridor holds cleared (10)
| Market | n | Note |
|--------|--:|------|
| costa-rica | 2 | A1 demand ready; country gate unblocked |
| yango-namibia | 3 | Country row complete |
| yango-cameroon | 3 | Country row complete |
| yango-congo-brazzaville | 2 | Country row complete |

## Corridor holds retained (6)
| Market | n | Why |
|--------|--:|-----|
| argentina | 2 | demand_not_exact_annual_oneway (benchmark only) |
| yango-venezuela | 3 | no current cost_index / country row |
| caribbean-mobility | 1 | USVI→BVI cross_border_home_port_unverified |

## Seals
- Null beats wrong on captain/marina: T4/T5 **planning allowances**, explicitly not operator quotes.
- Energy/cost_index sourced from published secondary + World Bank PLI.
- No finance aggregate/sheet cascade run without greenlight.

See JSON ledger for full field sources.
