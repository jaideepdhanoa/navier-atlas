# Country-reference fail-closed correction — delivery status

**Date:** 2026-07-10  
**Rule:** an active corridor needs an exact country key and all five numeric country-cost fields. Otherwise it carries a descriptive economics hold and is excluded from both engines. No Singapore or neighboring-country fallback is permitted.

## Production decisions

| Country | Decision | Production treatment |
|---|---|---|
| South Korea | **Seal ready** | Source-backed crew, commercial energy, grid factor and price index; transparent conservative official-tariff planning ceiling for berth/port admin. Unlocks Swing/Naver/Kakao economics. |
| Argentina | **Hold** | Two DiDi corridors excluded; fully loaded crew and terminal/Uruguay allocation remain incomplete. |
| Costa Rica | **Hold** | Two DiDi Gulf of Nicoya corridors excluded; exact current terminal/berth overhead remains unresolved. |
| Namibia | **Hold** | Three Yango corridors excluded. |
| Venezuela | **Hold** | Three Yango corridors excluded. |
| Cameroon | **Hold** | Three Yango corridors excluded. |
| Congo (Brazzaville) | **Hold** | Two Yango corridors excluded. |

## Label repairs

- `USVI / BVI` is no longer a fabricated third country. The directed St. Thomas→Tortola record uses U.S. Virgin Islands as origin and British Virgin Islands as destination, but remains economics-held until vessel home port is verified.
- Four `CrossBorder` rows now use their evidenced Singapore origin/home-port assignment and retain explicit Malaysia/Indonesia destination metadata.

## Permanent controls

1. `scripts/validate_country_reference.py` fails on missing, incomplete, pseudo, or composite active country labels.
2. `aggregate.py` has no fallback country and excludes only explicitly held corridors.
3. `build_transparent_sheet.py` has no fallback country and publishes every exclusion on an **Economics holds** tab.
4. The repository and workspace partner-model cascade playbooks now require this gate before aggregate, sheet, sidecar, and deck delivery.

## Delivery gate

Fresh recalculated workbook parity now passes for both partner models. Swing: sheet SOM `$10,453,756.64` versus model `$10,453,754` (formula-rounding delta `$2.64`), with a `$104,537,675` transport pool in both engines. DiDi: sheet and model SOM `$38,163,982`, pool `$386,158,495`; the two Costa Rica and two Argentina corridors appear on the visible **Economics holds** tab and are absent from all economics. Release remains merge + Grok model-to-deck regeneration + live-manifest verification; no production claim may imply held routes are modeled.
