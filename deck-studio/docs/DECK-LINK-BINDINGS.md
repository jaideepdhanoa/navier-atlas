# Deck hyperlink bindings

Gold-template partner decks carry **top-left Poppins link text boxes**. Wire them via
`decks/{deck}/slide-link-bindings.json` + `builders/deck_link_bindings.py`.

All deck links render **white + underlined** (`link_replace_op` in `deck_edit_ops.py`).

## Link roles

| Role | Slides | Label | Target URL |
|------|--------|-------|------------|
| `atlas_partner_hub` | 3 | Interactive link | `https://navier-atlas.vercel.app/{partner_id}` |
| `atlas_market` | 4–6, 14–18 | Interactive link | `/{partner}/{market}` or `.../city/{city_id}` |
| `economics_sheet` | 7–9, 19–23 | Model deepdive | Partner unit-economics Google Sheet |
| `economics_sheet` | 10 | Detailed market sizing | Same economics sheet |

## URL resolution

1. **Partner hub (slide 3):** `{ATLAS_BASE}/{partner_id}`
2. **Market (slides 4–6, 14–18):** resolve market from `data-clean/partners/{partner}.json`
   via `atlas_city_id` (+ optional `atlas_market_slug` override, `link_target: market|city`)
3. **Economics (slides 7–9, 19–23, 10):** first hit among:
   - `decks/{deck}/deck.config.json` → `economics_url`
   - `data-clean/partners/{partner}.json` → `economics_url`
   - `finance/economics_url_map.json`

## Auto-merge

- **Model deepdive** on unit-economics slides is auto-merged from
  `decks/{deck}/economics-binding.json` → `fields.model_link.object_id` (slides 7–9, 19–23).
- **Detailed market sizing** on slide 10 from `tam_sizing_link` in `slide-link-bindings.json`
  (or golden-template lookup).

## Commands

```bash
python builders/deck_link_bindings.py validate-bindings --deck bolt
python builders/deck_link_bindings.py apply --deck bolt
# or: python builders/deck_bolt_wave2.py apply-atlas-links
```

Object IDs for link text boxes: `decks/grab/golden-template-map.json` (search by label text).