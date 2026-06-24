# Ocean Whisperer vs Bolt wave-2 — gap matrix

**Root cause:** `deck_ocean_whisperer.py` was forked from a **minimal text-only path** (like an early `deck_minor_hotels.py` stub), not from `deck_bolt_wave2.py` + `deck_bolt_wave2_images.py` + per-deck binding JSONs. It applied **255 text ops** and **one** `replaceImage` (`econ-curacao-v1` on slide 7 only).

## Why slides 1 & 2 were not built

| Role | Bolt | OW shipped | Gap |
|------|------|------------|-----|
| `cover_hero` (`p1_i2`) | `bolt-cover-hero` via `IMAGE_BINDINGS` | **Not in editplan** | No registry key, no generate/publish, no `replaceImage` |
| `partner_logo` (`p1_i5`) | ✓ | ✓ | Done |
| Slide 2 insert (`narr2_page`) | `cmd_insert_slide2()` from gold create plan | **Never run** | Deck still has Grab Three C's as physical slide 2 |
| `value_prop_bg` (`narr2_bg_img`) | `bolt-value-prop-bg` + `apply-slide2-image` | **Missing** | No `narrative-slide2-ocean-whisperer.json`, no image |
| Slide 2 narrative text | `narrative-binding.json` + paint ops | **Missing** | No `build_narrative_paint_ops()` |

## Why slide 11/12 background was not replaced

`IMAGE-ROLE-CONTRACT.md` places `partner_roles_bg` on **slide 11** (`g3ea5e0fb254_4_358`). Thumbnails often label this **slide 12** when slide 2 is absent (off-by-one). Bolt wires it in `IMAGE_BINDINGS`; OW never registered or applied `ow-partner-roles-bg`.

Same gap for **`tam_bg`** on slide 10 (`navierBg_s26`): TAM **text** was updated; the Grab network plate was left in place.

## Why slides 8–9 still show Phuket/Bali

Bolt applies **all** `econ_market_bg` slots via `slide-image-bindings.json` + `ECON_BINDINGS` (slides 8–10 in post-insert numbering = `navierBg_s23`–`s25`). OW only bound **one** corridor on `navierBg_s23`. Slides 8–9 retained gold-template **paintbrush** plates.

**Hospitality single-market rule (now in playbook):** reuse `econ-curacao-v1` on all three econ slots **and** repaint corridor-specific economics from `agg-ocean-whisperer.json` so text matches bg.

## Full role checklist

| Role | Slides (post slide-2 insert) | Bolt artifacts | OW status |
|------|------------------------------|----------------|-----------|
| `cover_hero` | 1 | `IMAGE_BINDINGS`, tier-A generate | **Missing** |
| `value_prop_bg` | 2 | insert + narrative + tier-A | **Missing** |
| `market_overview_kpis` | 3 | sidecar + binding | Text ✓ |
| `atlas_route_screenshot` | 5–7 | `slide-image-bindings.json`, capture | **Missing** |
| `econ_market_bg` | 8–10 | 3 markets / 8 corridors | **1/3 bg only** |
| `tam_bg` | 11 | tier-A | **Missing** |
| `partner_roles_bg` | 12 | tier-A | **Missing** |
| Deck hyperlinks | 3–13 | `slide-link-bindings.json` | **Missing** |
| `three_cs_bg` | 3 | tier-A `ow-three-cs-bg` on `g3f139a0b6ec_0_1` | **Was Grab plate** |
| Market route lists | 5–7, 12 | `market-route-bindings.json` + amber styling | **Fixed** |
| Slide 3 KPI caption align | 4 | center on `_7/_11/_16/_19` | **Fixed** |
| Close body (slide 14) | 14 | `close_atlas_link.body_text` only | **Was long prose** |
| Econ bg integration | 8–10 | Tier-A `curacao-econ-tier-a-v1` | **Was paste-composite** |

## Playbook fix (mandatory before `run-all`)

1. Scaffold `decks/{deck}/slide-image-bindings.json`, `slide-link-bindings.json`, `market-route-bindings.json`, `narrative-binding.json`, `narrative-slide2-{deck}.json`, `image-manifest.json`.
2. Generate **all** deck-level image roles (`cover_hero`, `value_prop_bg`, `tam_bg`, `partner_roles_bg`) — hospitality is **not** exempt.
3. `insert-slide2` on every new gold copy before narrative/image apply.
4. Apply **all** econ slots for the anchor market (reuse market asset by `atlas_city_id`).
5. Capture Atlas screenshots for market side-panels before apply.
6. Run `validate-bindings` + leak scan on **edited slide scope including images**.

## Rerun command (OW)

```bash
cd deck-studio/builders
python deck_ocean_whisperer_images.py generate-all
python deck_ocean_whisperer.py insert-slide2 --presentation-id <id>
python deck_ocean_whisperer.py run-wave2 --presentation-id <id>
```