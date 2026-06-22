# Consolidated deck generation queue

Updated: `2026-06-22T02:17:02Z`

**Current spec:** 6-opex-line unit econ (new field-ID family per-slide), slide-3 market KPIs, slide-10 TAM, cover partner-logo/no-logo, N30 shipped-plate imagery, stable linked-image URLs only (no embedded-only blobs)

## 25 generation-ready decks

| Deck | Type | Logo | Prep refresh | No-reembed | OPEX6 | Slide3 | Slide10 |
|---|---|---:|---|---|---|---|---|
| `abu-dhabi-itc` | create-or-bind | banked | build-on-spec | stable_linked_asset_url_required | build-on-spec | build-on-spec | build-on-spec |
| `bahrain-motc` | create-or-bind | needs_sourcing | build-on-spec | stable_linked_asset_url_required | build-on-spec | build-on-spec | build-on-spec |
| `dubai-rta` | create-or-bind | needs_sourcing | build-on-spec | stable_linked_asset_url_required | build-on-spec | build-on-spec | build-on-spec |
| `gojek` | create-or-bind | banked | build-on-spec | stable_linked_asset_url_required | build-on-spec | build-on-spec | build-on-spec |
| `hong-kong` | create-or-bind | no-logo | build-on-spec | stable_linked_asset_url_required | build-on-spec | build-on-spec | build-on-spec |
| `jih-global` | create-or-bind | banked | build-on-spec | stable_linked_asset_url_required | build-on-spec | build-on-spec | build-on-spec |
| `qatar` | create-or-bind | needs_sourcing | build-on-spec | stable_linked_asset_url_required | build-on-spec | build-on-spec | build-on-spec |
| `rakta` | create-or-bind | needs_sourcing | build-on-spec | stable_linked_asset_url_required | build-on-spec | build-on-spec | build-on-spec |
| `red-sea-global` | create-or-bind | banked | build-on-spec | stable_linked_asset_url_required | build-on-spec | build-on-spec | build-on-spec |
| `saudi-pif` | create-or-bind | source_confirmed_pending_fetch | build-on-spec | stable_linked_asset_url_required | build-on-spec | build-on-spec | build-on-spec |
| `singapore-mpa` | create-or-bind | banked | build-on-spec | stable_linked_asset_url_required | build-on-spec | build-on-spec | build-on-spec |
| `adani-ports` | refresh-to-current-spec | needs_sourcing | prep_contract_refreshed__live_slides_not_mutated | stable_linked_asset_url_required | refresh-required | refresh-required | refresh-required |
| `bolt` | refresh-to-current-spec | needs_sourcing | prep_contract_refreshed__live_slides_not_mutated | stable_linked_asset_url_required | refresh-required | refresh-required | refresh-required |
| `careem` | refresh-to-current-spec | banked | prep_contract_refreshed__live_slides_not_mutated | stable_linked_asset_url_required | refresh-required | refresh-required | refresh-required |
| `caribbean-mobility` | refresh-to-current-spec | no-logo | prep_contract_refreshed__live_slides_not_mutated | stable_linked_asset_url_required | refresh-required | refresh-required | refresh-required |
| `french-polynesia` | refresh-to-current-spec | no-logo | prep_contract_refreshed__live_slides_not_mutated | stable_linked_asset_url_required | refresh-required | refresh-required | refresh-required |
| `grab` | refresh-to-current-spec | banked | prep_contract_refreshed__live_slides_not_mutated | stable_linked_asset_url_required | refresh-required | refresh-required | refresh-required |
| `noon` | refresh-to-current-spec | needs_sourcing | prep_contract_refreshed__live_slides_not_mutated | stable_linked_asset_url_required | refresh-required | refresh-required | refresh-required |
| `ola` | refresh-to-current-spec | needs_sourcing | prep_contract_refreshed__live_slides_not_mutated | stable_linked_asset_url_required | refresh-required | refresh-required | refresh-required |
| `rapido` | refresh-to-current-spec | needs_sourcing | prep_contract_refreshed__live_slides_not_mutated | stable_linked_asset_url_required | refresh-required | refresh-required | refresh-required |
| `reliance-industries` | refresh-to-current-spec | needs_sourcing | prep_contract_refreshed__live_slides_not_mutated | stable_linked_asset_url_required | refresh-required | refresh-required | refresh-required |
| `uber-india` | refresh-to-current-spec | needs_sourcing | prep_contract_refreshed__live_slides_not_mutated | stable_linked_asset_url_required | refresh-required | refresh-required | refresh-required |
| `uber-mena` | refresh-to-current-spec | needs_sourcing | prep_contract_refreshed__live_slides_not_mutated | stable_linked_asset_url_required | refresh-required | refresh-required | refresh-required |
| `yango` | refresh-to-current-spec | needs_sourcing | prep_contract_refreshed__live_slides_not_mutated | stable_linked_asset_url_required | refresh-required | refresh-required | refresh-required |
| `yassir` | refresh-to-current-spec | needs_sourcing | prep_contract_refreshed__live_slides_not_mutated | stable_linked_asset_url_required | refresh-required | refresh-required | refresh-required |

## Notes

- 14 refresh-to-current-spec decks now have prep-contract refresh files (SPEC-REFRESH.json), canonical image roles, and no-reembed linked-asset requirements; live Slides regeneration remains pending.

## Separate prep backlog (not generation-ready yet)

`aman`, `bc-ferries`, `cabify`, `constance`, `cote-dazur`, `crown-champa`, `d-marin`, `didi`, `discovery-land`, `four-seasons`, `freenow`, `fullers360`, `hawaii`, `indian-ocean-luxury`, `indrive`, `kakao-mobility`, `line`, `lyft`, `maldives`, `maldives-government`, `norway-fjords`, `nyc-ferry`, `shun-tak`, `six-senses`, `soneva`, `sun-siyam`, `thames-clippers`, `transport-nsw`, `universal-enterprises`, `villa-hotels`, `wsf`

- `jih-global`: entity confirmed by Jaideep 2026-06-22; official-site logo asset banked from `https://www.jihglobal.com/` / Framer asset.
