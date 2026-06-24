"""Slide-2 exec-summary paint ops with gold-create style pins."""
from __future__ import annotations

from pathlib import Path

from deck_edit_ops import text_replace_ops

ROOT = Path(__file__).resolve().parents[1]
STYLE_PINS_PATH = ROOT / "decks/grab/narrative-slide2-style-pins.json"


def load_json(path: Path) -> dict:
    import json

    return json.loads(path.read_text(encoding="utf-8"))


def narr2_element(oid: str, text: str) -> dict:
    pins = load_json(STYLE_PINS_PATH)["pins"]
    if oid not in pins:
        raise KeyError(f"no narr2 style pin for {oid}")
    pin = pins[oid]
    return {
        **pin,
        "char_budget": max(pin.get("char_budget", 48), len(text) + 8),
        "runs": [{"start": 0, "end": len(text), "style": pin["style"]}],
    }


def build_narrative_paint_ops(binding: dict, narrative: dict, *, deck_key: str, source_name: str) -> list[dict]:
    slide_oid = binding["slide_object_id"]
    ops: list[dict] = []
    for field_key, pin in binding["fields"].items():
        if not pin.get("present"):
            continue
        text = pin["static"] if pin.get("static") else (narrative.get(field_key) or "")
        if not text:
            continue
        el = narr2_element(pin["object_id"], text)
        ops.extend(
            text_replace_ops(
                slide_oid,
                pin["object_id"],
                text,
                el,
                op_prefix=f"{deck_key}-narr2-{pin['object_id']}",
                source_pointer=source_name,
            )
        )
    for i, beat_pin in enumerate(binding["your_world"]):
        if not beat_pin.get("present"):
            continue
        beat = narrative["your_world"][i]
        for part, oid_key in (("label", "head_object_id"), ("text", "body_object_id")):
            oid = beat_pin[oid_key]
            text = beat[part]
            el = narr2_element(oid, text)
            ops.extend(
                text_replace_ops(
                    slide_oid,
                    oid,
                    text,
                    el,
                    op_prefix=f"{deck_key}-narr2-{oid}",
                    source_pointer=source_name,
                )
            )
    return ops