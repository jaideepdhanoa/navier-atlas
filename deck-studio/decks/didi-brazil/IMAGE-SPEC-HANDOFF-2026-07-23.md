# DiDi Brazil — image spec locked + 4-deck cascade handoff
*2026-07-23 · companion to `DIDI-BRAZIL-IMAGE-GAP-2026-07-23.md` (Tasklet's audit)*

Tasklet diagnosed the gap; this locks the **enforceable spec** so generation can't drift again, and
extends the audit to the three sibling decks. **No images were generated** (no image-gen capability in
this environment) — the composites themselves still need Grok (or the image-gen tool).

---

## 1. What changed this session (repo files, didi-brazil)

- **`image-manifest.json` — rebuilt from a 4-entry stub to all 24 slides.** Every image role is now wired
  to its **real** live slide object id (from `slide-manifest.json`, synced 2026-07-20), with correct
  status per what exists. The old stub carried pre-build placeholder ids (`planned_didi_brazil_0N`) and the
  obsolete Grab-gold slide numbering — both gone.
- **`slide-image-bindings.json` — created.** This is the "authoritative per-deck wiring" the
  `IMAGE-ROLE-CONTRACT` references but which was **absent** for didi-brazil (and every sibling deck). 23
  bindings across five slide families.
- **Stale doc pointer fixed.** `role_contract` now points at `deck-studio/assets/IMAGE-ROLE-CONTRACT.md`
  (was `deck-studio/docs/ASSET-ROLE-CONTRACT.md`, which 404s).

Manifest status roll-up: **12 `needs_generation`**, **1 `needs_registration`** (cover on disk), **1
`checked_in`** (three_c — correct, do not touch), **9 `human_insertion_only`** (Atlas route maps),
**1 `no_image_role`** (slide 13 "Next steps", text-only).

---

## 2. Critical rule — resolve image-ELEMENT ids from live inventory, never guess

`target_slide_object_id` (the slide) is known for all 24 slides. The **image-element** id inside each slide
is resolved for **only slide 3** (`three_c_bg → g3ec744d37d2_0_4`). Every other `target_object_id` is
`null` with a resolver note. Element ids **do not** derive from slide ids (verified: slide-5's map element
is `g3f4f7400edf_0_1`) and **must not** be borrowed from sibling decks (bolt's slide-5 element differs).
Before any `replaceImage`: pull the per-slide object inventory from the live deck and bind the full-bleed
background element. Null beats confidently-wrong.

---

## 3. DiDi Brazil generation worklist (12 composites)

All are N30-neutral-reference composites, provenance required, `no Atlas imagery`. Paths below are the
manifest's suggested check-in locations.

| # | image_key | slide | scope | prompt_tier | check-in path |
|---|---|---|---|---|---|
| 1 | `didi-brazil-value_prop_bg` | 2 | deck·Rio | `value_prop_booking_berth` | `backgrounds/decks/didi-brazil/` |
| 2 | `didi-brazil-econ_market_bg-rio-de-janeiro` | 8 | market | `econ_unit_landmark` | `backgrounds/markets/rio-de-janeiro/` |
| 3 | `didi-brazil-econ_market_bg-angra-dos-reis` | 9 | market | `econ_unit_landmark` | `backgrounds/markets/angra-dos-reis/` |
| 4 | `didi-brazil-econ_market_bg-florianopolis` | 10 | market | `econ_unit_landmark` | `backgrounds/markets/florianopolis/` |
| 5 | `didi-brazil-tam_bg` | 11 | deck | `tam_background` | `backgrounds/decks/didi-brazil/` |
| 6 | `didi-brazil-partner_roles_bg` | 12 | deck | `partner_roles_background` | `backgrounds/decks/didi-brazil/` |
| 7 | `didi-brazil-close_bg` | 14 | deck | `close_background` | `backgrounds/decks/didi-brazil/` |
| 8 | `didi-brazil-econ_market_bg-salvador` | 20 | market | `econ_unit_landmark` | `backgrounds/markets/salvador/` |
| 9 | `didi-brazil-econ_market_bg-ilha-do-mel` | 21 | market | `econ_unit_landmark` | `backgrounds/markets/ilha-do-mel/` |
| 10 | `didi-brazil-econ_market_bg-santos-guaruja` | 22 | market | `econ_unit_landmark` | `backgrounds/markets/santos-guaruja/` |
| 11 | `didi-brazil-econ_market_bg-vitoria` | 23 | market | `econ_unit_landmark` | `backgrounds/markets/vitoria/` |
| 12 | `didi-brazil-econ_market_bg-ilhabela` | 24 | market | `econ_unit_landmark` | `backgrounds/markets/ilhabela/` |

The **8 `econ_market_bg`** plates are *city-keyed and reusable* — once generated, any future deck featuring
that city binds the same file. This is the fix for "slides 8/9/10 (and 20–24) look identical": no per-city
plate ever existed, so all fell back to one image. The **`partner_roles_bg` (slide 12)** is the slot that
repeats *across decks* — no deck ever generated a deck-scoped one.

---

## 4. Cover — ready-to-register (asset already on disk)

`deck-studio/assets/didi/didi-cover-rio-n30.png` exists but is unregistered; the manifest still said
`needs_sourcing`. Physical facts captured so registration is a paste (still needs a published stable URL +
the live element id before apply):

```json
{
  "role": "cover_hero", "scope": "deck", "partner": "didi", "market_slug": "rio-de-janeiro",
  "atlas_city_id": null, "local_path": "deck-studio/assets/didi/didi-cover-rio-n30.png",
  "dimensions": "1536x864", "bytes": 1874033,
  "sha256": "b9b9e109fbae73ad7c862c99b42c61d8a27847cf63c833b6d92a02127434758e",
  "version": "v1", "composited": true, "license": "navier-internal", "reproducible": true,
  "source_url": null,
  "used_by": [{ "deck": "didi-brazil", "slide_index": 1, "target_object_id": null }],
  "status": "needs_stable_url_and_element_id",
  "delivery": { "method": "slides_api_image_url", "stable_url_status": "pending_publish" },
  "market_specific": true
}
```

---

## 5. Cascade audit — all four country decks share the gap

| Deck | Live slides | Manifest image roles | `slide-image-bindings.json` | Registered bg/cover assets |
|---|---|---|---|---|
| **didi-brazil** | 24 | ~~4~~ → **24 (fixed)** | ~~absent~~ → **created** | only `three_c_bg` |
| **didi-mexico** | 18 | 12 (cover + atlas + route-maps; **no** econ/tam/roles/value_prop/close) | **absent** | **none** |
| **indrive-brazil** | 24 | 4 (cover + 3 atlas) | **absent** | **none** |
| **indrive-egypt** | 12 | 6 (cover + atlas + route-maps) | **absent** | **none** |

Two structural gaps are **universal** and explain what Jaideep saw:
1. **No `slide-image-bindings.json` on any deck** → nothing forces backgrounds to be deck/city-specific.
2. **Econ/narrative background roles are undeclared** in every sibling manifest, and **near-zero** bg
   composites are registered (only didi-brazil's three_c). Every deck is running on inherited template
   placeholders for `value_prop_bg` / `tam_bg` / `partner_roles_bg` / `close_bg` / per-city `econ_market_bg`
   — which is exactly why **slide 12 is identical across decks**.

**Replicate the didi-brazil fix on the other three:** rebuild each manifest to its full slide set, create
each `slide-image-bindings.json`, then generate + register the per-deck and per-city composites. (I can do
the manifest/bindings repo work for those three the same way on request; generation stays with Grok.)

---

## 6. Apply sequence (per image)

generate composite (N30-neutral ref, provenance) → check in under the path above → **register in
`ASSET-REGISTRY.json` + publish a stable `source_url`** (no `googleusercontent` temp urls) → resolve the
live **element id** for that slide → `replaceImage` → QA thumbnail. Do **not** touch slide 3 or the
human Atlas slots (4–7, 15–19).
