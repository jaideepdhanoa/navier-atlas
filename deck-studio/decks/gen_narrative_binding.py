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
# PROOF CHIPS REMOVED (2026-06-22, partner-comment pass).
#   The bottom KPI strip created cross-slide number redundancy (slide-2 ~100/250 vessels
#   vs slide-4 1,000+) and review risk, and crowded the copy. Slide 2 is now
#   kicker + lockup + positioning + thesis + the_deal + the 2x2 "Your world" beats only.
#   Quantified proof lives on slide 4 (THE REGION) and in the economics sidecar.
#   network_thesis.stats is STILL distilled into narrative-slide2-<partner>.json (for the
#   sidecar / provenance), it is simply no longer painted on slide 2. The chip object IDs
#   (narr2_chip{1..4}_{v,c}) are retired; if a deck still carries them from the old
#   gold-create, the per-deck paint step deletes them (see RETIRED_OBJECT_IDS).
RETIRED_OBJECT_IDS = [f"narr2_chip{i}_{s}" for i in (1, 2, 3, 4) for s in ("v", "c")]

BG_IMAGE_ID = "narr2_bg_img"   # full-bleed market background (N30 archetype A2); wired in the image step
SCRIM_ID    = "narr2_scrim"    # full-bleed navy legibility scrim, sits above the bg image, below the text
RULE_ID     = "narr2_rule"     # thin gold accent rule under "Your world"

# ---- Geometry (EMU). Single left-weighted text column over a full-bleed market image.
#   Rhythm matches the human-tuned live Grab slide (content shifted up; KPI strip removed;
#   the 2x2 beats enlarged and spread into the freed lower third). UI-tunable post-create.
GEO = {
    "narr2_kicker":      dict(x=430000,  y=300000,  w=4600000, h=320000),
    "narr2_lockup":      dict(x=430000,  y=543800,  w=5200000, h=760000),
    "narr2_positioning": dict(x=430000,  y=1055200, w=5200000, h=420000),
    "narr2_thesis":      dict(x=430000,  y=1455200, w=5200000, h=560000),
    "narr2_deal":        dict(x=430000,  y=2055200, w=5200000, h=620000),
    "narr2_world_label": dict(x=430000,  y=2705200, w=2600000, h=280000),
    RULE_ID:             dict(x=430000,  y=2985200, w=5200000, h=14000),
    SCRIM_ID:            dict(x=0,       y=0,       w=EMU_W,   h=EMU_H),
}
# 2x2 beat grid (lower-left), enlarged (head 11pt / body 10pt) and spread into the
# space the proof-chip strip vacated. Text boxes do not clip (only the page edge clips);
# row2 body ends ~4665000, inside the 5143500 page edge.
_bx = [430000, 3050000]
_by_head = [3055200, 3900000]
_by_body = [3300000, 4145000]
for i, (h, b) in enumerate(WORLD_SLOTS):
    col, row = i % 2, i // 2
    GEO[h] = dict(x=_bx[col], y=_by_head[row], w=2480000, h=240000)
    GEO[b] = dict(x=_bx[col], y=_by_body[row], w=2480000, h=520000)

# ---- Styles (applied once at gold-create; inherited thereafter)
STYLE = {
    "narr2_kicker":      dict(size=10,  bold=True,  color="C9A227", italic=False),
    "narr2_lockup":      dict(size=26,  bold=True,  color="FFFFFF", italic=False),
    "narr2_positioning": dict(size=15,  bold=False, color="C9A227", italic=True),
    "narr2_thesis":      dict(size=15,  bold=True,  color="FFFFFF", italic=False),
    "narr2_deal":        dict(size=11,  bold=False, color="E8E8E8", italic=False),
    "narr2_world_label": dict(size=10,  bold=True,  color="C9A227", italic=False),
    "_beat_head":        dict(size=11,  bold=True,  color="FFFFFF", italic=False),
    "_beat_body":        dict(size=10,  bold=False, color="CFCFCF", italic=False),
}
# Full-bleed navy legibility scrim (matches the live deck): rgb(0.039,0.071,0.125), alpha 0.5.
SCRIM_FILL = dict(red=0.039215688, green=0.07058824, blue=0.1254902, alpha=0.5)

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
    for i, (h, b) in enumerate(WORLD_SLOTS):
        item = src_world[i] if i < len(src_world) else None
        world.append({"head_object_id": h, "body_object_id": b,
                      "present": item is not None,
                      "sample_label": (item or {}).get("label"),
                      "sample_text": (item or {}).get("text")})
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
        "background": {"image_object_id": BG_IMAGE_ID,
                       "filled_by": "N30 image archetype A2 (image-manifest.json), full-bleed",
                       "scrim_object_id": SCRIM_ID,
                       "note": "Background is a full-bleed market image with a navy scrim for legibility; "
                               "text sits above the scrim. No right-zone image box."},
        "accent_rule": {"object_id": RULE_ID},
        "proof_strip": {"painted_on_slide2": False,
                        "retired_object_ids": RETIRED_OBJECT_IDS,
                        "note": "KPI chips removed 2026-06-22 (cross-slide redundancy + copy room). "
                                "network_thesis.stats remains in narrative JSON for the economics "
                                "sidecar and slide 4, but is NOT painted on slide 2."},
        "fields": pins,
        "your_world": world,
        "render_order": ["background", "scrim", "kicker", "partner_lockup", "positioning",
                         "thesis", "the_deal", "world_label", "rule", "your_world[0..3]"],
        "paint_protocol": ("Per-deck (after one-time gold-create): for each present pin, "
                           "deleteText{objectId,textRange:ALL} then insertText{objectId,insertionIndex:0}. "
                           "Skip pins where present=false (null beats confidently-wrong). "
                           "If the deck still carries RETIRED_OBJECT_IDS, deleteObject them. "
                           "No numbers are painted on slide 2; quantified proof lives on slide 4 + sidecar."),
        "qa_gates": ["leak_denylist", "char_budget_scan", "orphan_number_check",
                     "style_reset_scan", "drift_gate", "render_thumbnails"],
    }

def _rgb(hexc):
    return {"red": int(hexc[0:2], 16) / 255, "green": int(hexc[2:4], 16) / 255, "blue": int(hexc[4:6], 16) / 255}

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

def _scrim_reqs():
    """Full-bleed navy legibility scrim, created right after the slide so text sits on top
    and the market bg image (page-background stretchedPictureFill, applied in the image step)
    sits behind it."""
    g = GEO[SCRIM_ID]
    return [
        {"createShape": {"objectId": SCRIM_ID, "shapeType": "RECTANGLE",
                         "elementProperties": {"pageObjectId": PAGE_ID,
                             "size": {"width": {"magnitude": g["w"], "unit": "EMU"},
                                      "height": {"magnitude": g["h"], "unit": "EMU"}},
                             "transform": {"scaleX": 1, "scaleY": 1,
                                           "translateX": g["x"], "translateY": g["y"], "unit": "EMU"}}}},
        {"updateShapeProperties": {"objectId": SCRIM_ID,
            "shapeProperties": {"shapeBackgroundFill": {"solidFill": {
                "color": {"rgbColor": {"red": SCRIM_FILL["red"], "green": SCRIM_FILL["green"],
                                       "blue": SCRIM_FILL["blue"]}}, "alpha": SCRIM_FILL["alpha"]}},
                "outline": {"propertyState": "NOT_RENDERED"}},
            "fields": "shapeBackgroundFill.solidFill,outline.propertyState"}},
    ]

def build_gold_create(partner, nar):
    reqs = [{
        "createSlide": {
            "objectId": PAGE_ID,
            "insertionIndex": 1,
            "slideLayoutReference": {"predefinedLayout": "BLANK"},
        }
    }, {
        # On-brand dark base so the white/gold text is legible immediately and remains
        # legible if the image step is deferred. The market background image gets wired
        # onto this page in the image step (page-background stretchedPictureFill, which
        # always sits behind every element); the scrim below provides legibility over it.
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
    # Scrim first (above bg, below text).
    reqs += _scrim_reqs()
    seeds = {
        "narr2_kicker":      ("narr2_kicker", "PARTNER PROPOSAL"),
        "narr2_lockup":      ("narr2_lockup", nar.get("partner_lockup")),
        "narr2_positioning": ("narr2_positioning", nar.get("positioning")),
        "narr2_thesis":      ("narr2_thesis", nar.get("thesis")),
        "narr2_deal":        ("narr2_deal", nar.get("the_deal")),
        "narr2_world_label": ("narr2_world_label", "Your world"),
    }
    for oid, (skey, txt) in seeds.items():
        if txt:
            reqs += _shape_req(oid, GEO[oid], skey, txt)
    reqs += _shape_req(RULE_ID, GEO[RULE_ID], kind="RECTANGLE")
    for i, (h, b) in enumerate(WORLD_SLOTS):
        items = nar.get("your_world", []) or []
        if i < len(items):
            reqs += _shape_req(h, GEO[h], "_beat_head", items[i].get("label"))
            reqs += _shape_req(b, GEO[b], "_beat_body", items[i].get("text"))
    return {
        "deck_key": partner,
        "presentation_id": GOLD_PRESENTATION_ID,
        "run_scope": "ONE_TIME_GOLD_ONLY",
        "mode": "slides_api_batch_update",
        "generated_from": "gen_narrative_binding.py",
        "purpose": ("Create the exec-summary slide ONCE in the Grab gold deck with PRE-ASSIGNED "
                    "object IDs, so it propagates to every future gold copy and the binding can pin "
                    "to fixed IDs. Replay on any deck ALREADY forked from gold; new copies inherit it. "
                    "v2 (2026-06-22): no proof-chip strip; 2x2 beats enlarged (11/10pt) and spread; "
                    "full-bleed market bg + navy scrim (no right-zone image box)."),
        "safety": {"no_pptx_roundtrip": True, "no_full_deck_replace": True,
                   "preserve_object_ids": True, "additive_single_slide_insert": True,
                   "human_review_required_for_external_send": True},
        "retired_object_ids": RETIRED_OBJECT_IDS,
        "post_create_actions": [
            "Capture the realized slide into golden-template-map.json (pre-described entry already added).",
            "Visually nudge layout in Slides UI if needed (IDs are stable; this is the one-time tuning).",
            "Wire the full-bleed market background via image-manifest.json (N30 archetype A2) as the page "
            "background (stretchedPictureFill); the scrim narr2_scrim provides legibility over it.",
            "If replaying onto a deck that already has the old chip strip, deleteObject the retired_object_ids.",
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
                print(f"\u2717 MISSING {os.path.relpath(path,ROOT)}"); ok = False; continue
            old = json.load(open(path))
            if json.dumps(old, sort_keys=True, ensure_ascii=False) == json.dumps(new, sort_keys=True, ensure_ascii=False):
                print(f"\u2713 reproduces {os.path.relpath(path,ROOT)}")
            else:
                print(f"\u2717 DRIFT {os.path.relpath(path,ROOT)}"); ok = False
        return 0 if ok else 1

    with open(b_path, "w") as f:
        json.dump(binding, f, indent=2, ensure_ascii=False)
    print(f"wrote {os.path.relpath(b_path,ROOT)}  "
          f"({sum(1 for v in binding['fields'].values() if v['present'])} scalar pins, "
          f"{sum(1 for w in binding['your_world'] if w['present'])} beats, no chips)")
    if gold:
        with open(g_path, "w") as f:
            json.dump(gold, f, indent=2, ensure_ascii=False)
        print(f"wrote {os.path.relpath(g_path,ROOT)}  ({len(gold['requests'])} Slides API requests, one-time gold-only)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
