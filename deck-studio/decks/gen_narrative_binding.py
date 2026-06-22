#!/usr/bin/env python3
"""
gen_narrative_binding.py  —  the slide-2 exec-summary PAINT PATH.

Emits two artifacts that mirror the economics layer:

  1. <deck>/narrative-binding.json
         The deterministic field -> object_id pin map (the "WHERE").
         Reads like economics-binding.json: the proposal/narrative JSON says WHAT,
         this file says WHERE. Object IDs are FIXED constants (the contract), so
         every partner deck — being a gold copy — inherits identical IDs.

  2. <deck>/narrative-slide2.gold-create.editplan.json
         The ONE-TIME slide-creation editplan, run ONCE against the Grab gold deck.
         createSlide @ insertionIndex 1 (becomes slide 2) + createShape per slot with
         PRE-ASSIGNED objectIds + styling + Grab seed text. Because IDs are pre-assigned,
         determinism is preserved and the slide propagates to every future gold copy.
         After this runs once, per-deck painting is pure style-preserving
         deleteText(ALL)+insertText into the known IDs — identical to economics.

Usage:
    python3 gen_narrative_binding.py grab
    python3 gen_narrative_binding.py grab --validate   # reproduce committed artifacts

Design notes:
  * The gold deck is the canonical 18yDAgO0Sj9PJlgf6paxtgni8Pk1xRAmNwE2TD_NCdSs.
  * Slide is 10in x 5.625in widescreen = 9144000 x 5143500 EMU.
  * Geometry below is a sensible starting layout; because the slide is created ONCE as
    a real object, it is UI-tunable afterwards — that is the whole benefit of one-time
    creation over per-build programmatic geometry.
  * null beats confidently-wrong: a missing narrative field emits a binding pin with
    "present": false and is SKIPPED in the gold-create seed (no invented prose).
"""
import json, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GOLD_PRESENTATION_ID = "18yDAgO0Sj9PJlgf6paxtgni8Pk1xRAmNwE2TD_NCdSs"
EMU_W, EMU_H = 9144000, 5143500

# ---- The CONTRACT: fixed object IDs for the exec-summary slide (inherited by every gold copy)
PAGE_ID = "narr2_page"
SLOTS = {
    # field_key (in narrative-slide2 JSON) : object_id
    "kicker":         "narr2_kicker",        # static "PARTNER PROPOSAL"
    "partner_lockup": "narr2_lockup",
    "positioning":    "narr2_positioning",
    "thesis":         "narr2_thesis",
    "the_deal":       "narr2_deal",
    "world_label":    "narr2_world_label",   # static "Your world"
}
# four "Your world" beats -> head/body object_ids, in render order
WORLD_SLOTS = [
    ("narr2_w1_h", "narr2_w1_b"),
    ("narr2_w2_h", "narr2_w2_b"),
    ("narr2_w3_h", "narr2_w3_b"),
    ("narr2_w4_h", "narr2_w4_b"),
]
# four proof chips -> value/caption object_ids
CHIP_SLOTS = [
    ("narr2_chip1_v", "narr2_chip1_c"),
    ("narr2_chip2_v", "narr2_chip2_c"),
    ("narr2_chip3_v", "narr2_chip3_c"),
    ("narr2_chip4_v", "narr2_chip4_c"),
]
IMAGE_ID = "narr2_image"   # filled by N30 image archetype A2 (image-manifest), not here
RULE_ID  = "narr2_rule"    # thin gold accent rule

# ---- Geometry (EMU). Left text column + right image zone. UI-tunable post-create.
GEO = {
    "narr2_kicker":      dict(x=430000,  y=300000,  w=4600000, h=320000),
    "narr2_lockup":      dict(x=430000,  y=620000,  w=5200000, h=760000),
    "narr2_positioning": dict(x=430000,  y=1360000, w=5200000, h=420000),
    "narr2_thesis":      dict(x=430000,  y=1760000, w=5200000, h=560000),
    "narr2_deal":        dict(x=430000,  y=2360000, w=5200000, h=620000),
    "narr2_world_label": dict(x=430000,  y=3010000, w=2600000, h=280000),
    RULE_ID:             dict(x=430000,  y=3290000, w=5200000, h=14000),
    IMAGE_ID:            dict(x=5900000, y=0,       w=3244000, h=5143500),
}
# 2x2 beat grid (lower-left) — beats are 2-line teasers; rows tightened so the
# proof-chip strip below clears them AND the 2-line chip captions clear the slide
# bottom edge (Slides does not clip text to the box; only the page edge clips). LB-256.
_bx = [430000, 3050000]; _by = [3360000, 3960000]
for i,(h,b) in enumerate(WORLD_SLOTS):
    col, row = i % 2, i // 2
    GEO[h] = dict(x=_bx[col], y=_by[row],          w=2480000, h=220000)
    GEO[b] = dict(x=_bx[col], y=_by[row]+225000,   w=2480000, h=340000)
# proof chips: horizontal strip along the bottom (value clears beat row2 @ 4525000;
# 2-line caption ends ~5060000, inside the 5143500 page edge)
_cx0, _cw, _cgap = 430000, 1230000, 80000
for i,(v,c) in enumerate(CHIP_SLOTS):
    x = _cx0 + i*(_cw+_cgap)
    GEO[v] = dict(x=x, y=4585000, w=_cw, h=190000)
    GEO[c] = dict(x=x, y=4780000, w=_cw, h=330000)

# ---- Styles (applied once at gold-create; inherited thereafter)
STYLE = {
    "narr2_kicker":      dict(size=10,  bold=True,  color="C9A227", italic=False),
    "narr2_lockup":      dict(size=26,  bold=True,  color="FFFFFF", italic=False),
    "narr2_positioning": dict(size=15,  bold=False, color="C9A227", italic=True),
    "narr2_thesis":      dict(size=15,  bold=True,  color="FFFFFF", italic=False),
    "narr2_deal":        dict(size=11,  bold=False, color="E8E8E8", italic=False),
    "narr2_world_label": dict(size=10,  bold=True,  color="C9A227", italic=False),
    "_beat_head":        dict(size=10,  bold=True,  color="FFFFFF", italic=False),
    "_beat_body":        dict(size=8.5, bold=False, color="CFCFCF", italic=False),
    "_chip_value":       dict(size=12,  bold=True,  color="C9A227", italic=False),
    "_chip_caption":     dict(size=7,   bold=False, color="BDBDBD", italic=False),
}

def load_narrative(partner):
    p = os.path.join(ROOT, "deck-studio", "decks", partner, f"narrative-slide2-{partner}.json")
    with open(p) as f:
        return json.load(f), p

def field_present(nar, key):
    v = nar.get(key)
    return v is not None and v != "" and v != []

def build_binding(partner, nar, src_rel):
    pins = {}
    for fk, oid in SLOTS.items():
        if fk in ("kicker", "world_label"):
            pins[fk] = {"object_id": oid,
                        "static": "PARTNER PROPOSAL" if fk == "kicker" else "Your world",
                        "present": True}
        else:
            present = field_present(nar, fk)
            pins[fk] = {"object_id": oid, "present": present,
                        "sample": (nar.get(fk) if present else None)}
    world = []
    src_world = nar.get("your_world", []) or []
    for i,(h,b) in enumerate(WORLD_SLOTS):
        item = src_world[i] if i < len(src_world) else None
        world.append({"head_object_id": h, "body_object_id": b,
                      "present": item is not None,
                      "sample_label": (item or {}).get("label"),
                      "sample_text": (item or {}).get("text")})
    chips = []
    src_chips = nar.get("proof_strip", []) or []
    for i,(v,c) in enumerate(CHIP_SLOTS):
        item = src_chips[i] if i < len(src_chips) else None
        chips.append({"value_object_id": v, "caption_object_id": c,
                      "present": item is not None,
                      "sample_value": (item or {}).get("value"),
                      "sample_caption": (f"{(item or {}).get('label','')} · {(item or {}).get('sub','')}".strip(" ·")
                                         if item else None),
                      "external": bool((item or {}).get("_external"))})
    return {
        "deck_key": partner,
        "presentation_id": GOLD_PRESENTATION_ID if partner == "grab" else None,
        "generated_from": "gen_narrative_binding.py",
        "source_narrative": src_rel,
        "slide_index": 2,
        "slide_object_id": PAGE_ID,
        "purpose": ("Deterministic field->object_id binding for the slide-2 exec-summary/thesis. "
                    "Grok pulls VALUES from narrative-slide2-<partner>.json (DISTILLED from the "
                    "proposal, never authored) and writes them into these object_ids via "
                    "style-preserving deleteText(ALL)+insertText — identical to the economics layer. "
                    "This file says WHERE; the proposal says WHAT. The slide itself is created ONCE in "
                    "gold via narrative-slide2.gold-create.editplan.json with these exact IDs, then "
                    "inherited by every gold copy. Never author prose; never invent object_ids."),
        "image_slot": {"object_id": IMAGE_ID, "filled_by": "N30 image archetype A2 (image-manifest.json)"},
        "accent_rule": {"object_id": RULE_ID},
        "fields": pins,
        "your_world": world,
        "proof_strip": chips,
        "render_order": ["kicker","partner_lockup","positioning","thesis","the_deal",
                         "world_label","your_world[0..3]","proof_strip[0..3]"],
        "paint_protocol": ("Per-deck (after one-time gold-create): for each present pin, "
                           "deleteText{objectId,textRange:ALL} then insertText{objectId,insertionIndex:0}. "
                           "Skip pins where present=false (null beats confidently-wrong). "
                           "Numbers in proof_strip must trace to narrative proof_sources or FLAG."),
        "qa_gates": ["leak_denylist","char_budget_scan","orphan_number_check",
                     "style_reset_scan","drift_gate","render_thumbnails"],
    }

def _rgb(hexc):
    return {"red": int(hexc[0:2],16)/255, "green": int(hexc[2:4],16)/255, "blue": int(hexc[4:6],16)/255}

def _shape_req(oid, geo, style_key=None, text=None, kind="TEXT_BOX"):
    reqs = [{
        "createShape": {
            "objectId": oid,
            "shapeType": kind,
            "elementProperties": {
                "pageObjectId": PAGE_ID,
                "size": {"width":  {"magnitude": geo["w"], "unit": "EMU"},
                         "height": {"magnitude": geo["h"], "unit": "EMU"}},
                "transform": {"scaleX": 1, "scaleY": 1,
                              "translateX": geo["x"], "translateY": geo["y"], "unit": "EMU"},
            },
        }
    }]
    if text:
        reqs.append({"insertText": {"objectId": oid, "text": text, "insertionIndex": 0}})
    if style_key and style_key in STYLE and text:
        st = STYLE[style_key]
        ts = {"foregroundColor": {"opaqueColor": {"rgbColor": _rgb(st["color"])}},
              "bold": st.get("bold", False),
              "fontSize": {"magnitude": st["size"], "unit": "PT"}}
        fields = "foregroundColor,bold,fontSize"
        if st.get("italic"):
            ts["italic"] = True; fields += ",italic"
        reqs.append({"updateTextStyle": {"objectId": oid, "style": ts,
                     "textRange": {"type": "ALL"}, "fields": fields}})
    return reqs

def build_gold_create(partner, nar):
    reqs = [{
        "createSlide": {
            "objectId": PAGE_ID,
            "insertionIndex": 1,
            "slideLayoutReference": {"predefinedLayout": "BLANK"},
        }
    }, {
        # On-brand dark base so the white/gold text is legible immediately.
        # BLANK predefined layout is white; deck slides are #050505-#111111.
        # The market background image gets wired onto this page in the image step
        # (page-background stretchedPictureFill, which always sits behind text).
        "updatePageProperties": {
            "objectId": PAGE_ID,
            "pageProperties": {
                "pageBackgroundFill": {
                    "solidFill": {"color": {"rgbColor": {"red": 0.0392, "green": 0.0392, "blue": 0.0470}}}
                }
            },
            "fields": "pageBackgroundFill.solidFill.color",
        }
    }]
    seeds = {
        "narr2_kicker":      ("narr2_kicker", "PARTNER PROPOSAL"),
        "narr2_lockup":      ("narr2_lockup", nar.get("partner_lockup")),
        "narr2_positioning": ("narr2_positioning", nar.get("positioning")),
        "narr2_thesis":      ("narr2_thesis", nar.get("thesis")),
        "narr2_deal":        ("narr2_deal", nar.get("the_deal")),
        "narr2_world_label": ("narr2_world_label", "Your world"),
    }
    for oid,(skey,txt) in seeds.items():
        if txt:
            reqs += _shape_req(oid, GEO[oid], skey, txt)
    reqs += _shape_req(RULE_ID, GEO[RULE_ID], kind="RECTANGLE")
    for i,(h,b) in enumerate(WORLD_SLOTS):
        items = nar.get("your_world", []) or []
        if i < len(items):
            reqs += _shape_req(h, GEO[h], "_beat_head", items[i].get("label"))
            reqs += _shape_req(b, GEO[b], "_beat_body", items[i].get("text"))
    for i,(v,c) in enumerate(CHIP_SLOTS):
        chips = nar.get("proof_strip", []) or []
        if i < len(chips):
            ch = chips[i]
            cap = f"{ch.get('label','')} · {ch.get('sub','')}".strip(" ·")
            reqs += _shape_req(v, GEO[v], "_chip_value", ch.get("value"))
            reqs += _shape_req(c, GEO[c], "_chip_caption", cap)
    reqs += _shape_req(IMAGE_ID, GEO[IMAGE_ID], kind="TEXT_BOX")
    return {
        "deck_key": partner,
        "presentation_id": GOLD_PRESENTATION_ID,
        "run_scope": "ONE_TIME_GOLD_ONLY",
        "mode": "slides_api_batch_update",
        "generated_from": "gen_narrative_binding.py",
        "purpose": ("Create the exec-summary slide ONCE in the Grab gold deck with PRE-ASSIGNED "
                    "object IDs, so it propagates to every future gold copy and the binding can pin "
                    "to fixed IDs. Replay on any deck ALREADY forked from gold; new copies inherit it."),
        "safety": {"no_pptx_roundtrip": True, "no_full_deck_replace": True,
                   "preserve_object_ids": True, "additive_single_slide_insert": True,
                   "human_review_required_for_external_send": True},
        "post_create_actions": [
            "Capture the realized slide into golden-template-map.json (pre-described entry already added).",
            "Visually nudge layout in Slides UI if needed (IDs are stable; this is the one-time tuning).",
            "Wire image slot narr2_image via image-manifest.json (N30 archetype A2).",
        ],
        "requests": reqs,
    }

def main():
    if len(sys.argv) < 2:
        print("usage: gen_narrative_binding.py <partner> [--validate]"); return 2
    partner = sys.argv[1]
    validate = "--validate" in sys.argv
    nar, src = load_narrative(partner)
    src_rel = os.path.relpath(src, ROOT)
    binding = build_binding(partner, nar, src_rel)
    deck_dir = os.path.join(ROOT, "deck-studio", "decks", partner)
    b_path = os.path.join(deck_dir, "narrative-binding.json")
    g_path = os.path.join(deck_dir, "narrative-slide2.gold-create.editplan.json")
    gold = build_gold_create(partner, nar) if partner == "grab" else None

    if validate:
        ok = True
        for path, new in [(b_path, binding), (g_path, gold)]:
            if new is None:
                continue
            if not os.path.exists(path):
                print(f"✗ MISSING {os.path.relpath(path,ROOT)}"); ok = False; continue
            old = json.load(open(path))
            if json.dumps(old, sort_keys=True, ensure_ascii=False) == json.dumps(new, sort_keys=True, ensure_ascii=False):
                print(f"✓ reproduces {os.path.relpath(path,ROOT)}")
            else:
                print(f"✗ DRIFT {os.path.relpath(path,ROOT)}"); ok = False
        return 0 if ok else 1

    with open(b_path, "w") as f:
        json.dump(binding, f, indent=2, ensure_ascii=False)
    print(f"wrote {os.path.relpath(b_path,ROOT)}  "
          f"({sum(1 for v in binding['fields'].values() if v['present'])} scalar pins, "
          f"{sum(1 for w in binding['your_world'] if w['present'])} beats, "
          f"{sum(1 for c in binding['proof_strip'] if c['present'])} chips)")
    if gold:
        with open(g_path, "w") as f:
            json.dump(gold, f, indent=2, ensure_ascii=False)
        print(f"wrote {os.path.relpath(g_path,ROOT)}  ({len(gold['requests'])} Slides API requests, one-time gold-only)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
