# Deterministic deck edit-plan contract (Tasklet → Grok)

_The fix for the Bolt-deck failures. Moves all authoring intelligence to a Tasklet-emitted, object-keyed edit plan; collapses Grok's job to "assert baseline → apply batchUpdate verbatim → leak-scan + render QA → receipt." No improvisation surface._

## Operating model change

**Before (broken):** Tasklet hands Grok narrative artifacts (slide-manifest, content-source) and Grok decides *how* to edit the live deck. Grok copies the gold file and pokes text → style resets, overflow, leaked prior-partner content.

**After (this contract):** Tasklet emits a single `deck.editplan.json` per partner — a literal, ordered list of Slides API `batchUpdate` requests keyed by the gold template's object IDs, with every run's style captured and re-applied, every string length-budgeted, and every image either replaced or fall-back-replaced (never inherited). Grok applies it verbatim.

```
Tasklet                                   Grok
───────                                   ────
1. golden-template-map.json  (built once from the Grab gold deck)
2. per-partner deck.editplan.json   ───►  3. copy gold deck → partner deck
                                          4. assert live objectIds == plan baseline (drift gate)
                                          5. apply editplan.requests via batchUpdate (verbatim)
                                          6. run leak-scan + render QA
                                          7. return receipt (deck id, op count, leak-scan result, render thumbs)
```

## 1. Golden template object-map (build once, reuse for all partners)

Extract from the Grab gold deck (`18yDAgO0Sj9PJlgf6paxtgni8Pk1xRAmNwE2TD_NCdSs`) — all 23 slides. For **every** page element, record:

```jsonc
{
  "object_id": "p1_i9",
  "slide_index": 1,
  "slide_object_id": "p1",
  "type": "text" | "image" | "shape_solid" | "table",
  "role": "hero.subtitle",            // controlled vocabulary (see §6)
  "char_budget": 90,                  // max chars before overflow at captured font/box
  "autofit": "SHAPE_AUTOFIT",         // capture; NEVER change it
  "paragraph_style": { "alignment": "START" },
  "runs": [                           // ordered; preserves multi-run styling
    { "len": 87, "style": { "fontFamily": "Poppins", "weightedFontFamily": {"fontFamily":"Poppins","weight":400},
                            "fontSize": {"magnitude":13.5,"unit":"PT"},
                            "foregroundColor": {"opaqueColor":{"rgbColor":{"red":0.953,"green":0.953,"blue":0.953}}},
                            "bold": false } }
  ]
}
```

The map is the **canonical baseline**. Because every partner deck is a copy of this template, the object IDs are stable across partners — that is the whole reason this works.

> Tasklet builds `golden-template-map.json` by paging the gold deck slide-by-slide (mode:"slides") and flattening the element/style tree. This is deterministic and should be regenerated whenever the gold Grab deck template changes (and the change reviewed).

## 2. Style-preserving text replace (the core mechanic)

A `deleteText` + `insertText` pair **loses all styling** — this is the Arial-14-black bug. Every text edit MUST be a 3-phase op group per object:

```jsonc
// (a) clear
{ "deleteText": { "objectId": "p1_i9", "textRange": { "type": "ALL" } } }
// (b) insert new content at index 0
{ "insertText": { "objectId": "p1_i9", "insertionIndex": 0, "text": "<new copy ≤ char_budget>" } }
// (c) RE-APPLY captured style to each run range  (one updateTextStyle per run)
{ "updateTextStyle": {
    "objectId": "p1_i9",
    "textRange": { "type": "FIXED_RANGE", "startIndex": 0, "endIndex": <len> },
    "style": { /* captured run style from golden map */ },
    "fields": "fontFamily,weightedFontFamily,fontSize,foregroundColor,bold,italic,backgroundColor,underline" } }
// (d) re-apply paragraph alignment if non-default
{ "updateParagraphStyle": { "objectId": "p1_i9", "textRange": {"type":"ALL"},
    "style": { "alignment": "START" }, "fields": "alignment" } }
```

Rules:
- **Never** flip `autofit`. Leave it exactly as captured (`SHAPE_AUTOFIT` boxes self-shrink; flipping to NONE caused the title overflow).
- New copy length **must be ≤ `char_budget`**. If the partner story needs more, Tasklet trims at source; Grok never receives an over-budget string.
- For multi-run lines (KPIs, mixed emphasis), emit one `updateTextStyle` per run range — see §3.

### Unit-economics header eyebrow (`econ.header_market`)

The gold eyebrow string is `WHAT ONE BOAT EARNS · {MARKET_LABEL}` on every unit-econ slide (7–9, 19–23).

| Rule | Requirement |
|---|---|
| **Full market label** | Never truncate the suffix to fit a shorter Grab residue sample (e.g. `CRO`, `AZUR`). Use `CROATIA`, `RIVIERA`, etc. |
| **Char budget** | All `econ.header_market` objects share the same text-box geometry — use canonical budget **31** (Singapore reference), not the Bali/Phuket sample budgets (26/28) on slides 8–9 |
| **Source** | `deck_bolt_wave2.ECON_BINDINGS[].market_label` → `econ_header_market_text()` |
| **Validation** | `python builders/deck_bolt_wave2.py validate-econ-headers` before apply |

**Failure mode (Bolt 2026-06-22):** slides 8–9 shipped `CRO` / `AZUR` because `char_budget` was taken from shorter Grab sample strings on duplicated template slides.

### Economics table value cells (revenue build · annual run cost · the result)

These are **single-value** cells, not multi-run narrative. Use `builders/deck_edit_ops.py`
`econ_value_replace_ops()` (or equivalent) — **never** reuse golden-map run lengths from a shorter
sample string.

| Rule | Requirement |
|---|---|
| **Style range** | One `updateTextStyle` over `startIndex: 0, endIndex: len(value_text)` — the **entire** inserted string |
| **Font** | Exo 2, 10pt, bold, white (`rgb 1,1,1`) |
| **Paragraph alignment** | `END` (right-aligned). Do **not** map shape `contentAlignment: MIDDLE` to `CENTER` for value columns |
| **Overflow group** | Insurance (`g3f213b2845d_0_5`) and Charging berth (`g3f213b2845d_0_7`) live outside the main golden-map pull — treat them like any other value cell (full-range style, not a 2-char fallback run) |

**Failure mode (Bolt 2026-06-22):** styling only the first 2 characters of `$22,500` because the
fallback golden element was sampled from a 2-char cell (`15`) → `$2` white Exo-2, `2,500` default Arial 14 black.

## 3. Market-slide marquee routes (slides 4–6, 14–18)

Example and backup market slides carry **four** signature/marquee routes in the route-list text box
(`example-market-routes` role — object IDs like `g3eec5122801_0_114`).

| Rule | Requirement |
|---|---|
| **Route count** | Exactly **4** routes per market slide |
| **Separator** | Blank line between route blocks (`\n\n`) |
| **Format** | `▸  From → To` then indented `~X nm · tagline` on the next line |
| **Bullet color** | Only the `▸` character: amber/gold `rgb(0.773, 0.616, 0.373)` |
| **Body color** | Route title + detail line: white `rgb(1, 1, 1)` |
| **Font** | Exo 2, 11pt, bold for the full block |
| **Source** | `decks/{deck}/market-route-bindings.json` → `data-clean/partners/{partner}.json` `markets[].journeys_unlocked` |
| **Builder** | `builders/deck_market_routes.py` → `market_route_replace_ops()` (amber/white multi-run styling) |

**Failure mode (Bolt 2026-06-22):** only 2 routes hardcoded in `NARRATIVE_TEXT`, entire block styled
gold from the golden-map single run. Fix: bindings file + bullet-only amber styling.

## 4. Multi-run KPI / emphasis lines (rebuild, don't skip)

The economics KPI line is 10 runs alternating gold figures (Exo 2 700) and grey connectors (Exo 2 400). Tasklet emits the full run sequence from the **economics sidecar** (never hand-typed):

```jsonc
"runs": [
  { "text": "$<rev>",        "style_ref": "kpi.figure" },
  { "text": " revenue  −  ", "style_ref": "kpi.connector" },
  { "text": "$<cost>",       "style_ref": "kpi.figure" },
  { "text": " run cost  =  ","style_ref": "kpi.connector" },
  { "text": "$<profit>",     "style_ref": "kpi.figure" },
  { "text": " profit / boat·yr  ·  ", "style_ref": "kpi.connector" },
  { "text": "<margin>% margin", "style_ref": "kpi.figure" },
  { "text": "  ·  ",         "style_ref": "kpi.connector" },
  { "text": "<payback> yrs",  "style_ref": "kpi.figure" },
  { "text": " payback",       "style_ref": "kpi.connector" }
]
```
Grok inserts the concatenated string, then applies `updateTextStyle` over each computed run range using the `style_ref` palette from the golden map. **If the partner has no published economics sidecar, the entire economics slide is nulled to the held template (see §5), never left carrying Grab's numbers.**

## 4. Image discipline (split logo from background)

Two image classes, two rules. **Never inherit the prior partner's image** under any condition.

| Class | Example objects | Asset source | If asset missing |
|---|---|---|---|
| **Brand logo** (no compositing) | hero `p1_i5` (partner logo), `p1_i4` (Navier logo) | `ASSET-REGISTRY.json` brand entry | **Hard block** — partner logo MUST swap; a deck wearing another partner's logo is never shippable |
| **Market background / N30 composite** | hero `p1_i2`, slide backgrounds (`navierBg_*`) | composited via `n30_composite.py` from approved source + `assets/n30/n30.png` | **Safe fallback**: replace with the canonical generic Navier open-water hero (registry key `a149`), flag `background_pending`; do NOT leave the gold deck's market-specific image |

Image op:
```jsonc
{ "replaceImage": { "imageObjectId": "p1_i5", "url": "<registry url>", "imageReplaceMethod": "CENTER_CROP" } }
```

This resolves Grok's 2026-06-21 asset note correctly: market backgrounds stay `held_null_pending_approved_assets`, **but logos and the generic fallback are not held** — so no deck ships with a foreign brand mark.

## 5. Slide-count parity (don't truncate to 11)

The gold Grab deck is **23 slides**; the playbook's "11-slide base" produced a chopped deck that kept Grab residue on the survivors. The edit plan must address **every** gold slide explicitly:

- `edit` — replace content per object map.
- `hold` — null to the neutral template (e.g., economics with no sidecar) with a visible "pending" treatment, never prior-partner data.
- `remove` — `deleteObject` the whole slide when the partner genuinely lacks that section (e.g., a market spoke). Explicit, logged, not a silent chop.

## 6. Role vocabulary + character budgets (per gold template)

Captured from the gold deck; authoritative budgets:

| role | font / size | budget (ch) |
|---|---|---|
| `hero.eyebrow` | Exo 2 700, 15pt, gold | 14 |
| `hero.title` | Exo 2 700, 33pt, white, SHAPE_AUTOFIT | ~40 |
| `hero.subtitle` | Poppins 400, 13.5pt, light-grey | ~90 |
| `section.header` | Exo 2 700, gold eyebrow + white title | per object |
| `econ.route_subhead` | Poppins 400, 11.5pt, gold | ~80 |
| `econ.kpi_line` | Exo 2 multi-run (figure 700 gold / connector 400 grey) | computed |
| `body.paragraph` | Poppins 400, 13–14pt | ~320 |
| `footer.confidential` | Exo 2 400, 6.5pt, grey | fixed string |

(Full per-object budgets live in `golden-template-map.json` once extracted.)

## 7. New QA gates Grok must run (and return in the receipt)

1. **Drift gate** — before applying, assert every `object_id` in the plan exists on the freshly-copied deck. Abort if the template changed.
2. **Leak scan** — after applying, fail if any prior-partner token survives. Maintain a per-partner denylist seeded from the gold deck: e.g. for any non-Grab partner, scan for `Grab`, `Marina Bay`, `Sentosa`, `Southern Islands`, `Southeast Asia`, the Grab logo registry id, and the gold economics figures (`480,870`, `398,301`, `82,569`). Zero hits required.
3. **Style-reset scan** — fail if any run on an edited object is `Arial` at 14pt with default/black color where the golden map specifies Exo 2/Poppins. (Catches the insert-without-restyle bug.)
4. **Budget scan** — fail if any edited text object's content length exceeds its `char_budget`.
5. **Image scan** — fail if any image object still resolves to the gold deck's source asset (hash/registry compare); every image must be a registry asset or the approved fallback.
6. **Render thumbnails** — return slide thumbnails so a human spot-check is seconds, not minutes.

## 8. New artifacts (replaces "deck is Grok's to figure out")

Per partner, under `deck-studio/decks/<deck>/`:
- `deck.editplan.json` — the ordered batchUpdate request list (this doc's §2–§5), validated against `deck-editplan.schema.json`.
- existing `deck.config.json`, `image-manifest.json` (now must list registry asset keys per image object_id).

Shared, under `deck-studio/`:
- `golden-template-map.json` — §1.
- `assets/ASSET-REGISTRY.json` — image_key → {registry url / drive_file_id, source_url, license, captured_at}.

## 9. Definition of done (low human review)

A partner deck is **apply-ready** when its `deck.editplan.json` validates, every object is `edit|hold|remove`, every string is in budget, every image object maps to a registry asset or approved fallback, and the leak/style/budget/image denylists are attached for Grok's QA. Grok returns a receipt that passes all six §7 gates. Human review is then a thumbnail spot-check, not a rebuild.
