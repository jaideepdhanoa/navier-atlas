"""Shared style-preserving Slides API edit-plan operations."""
from __future__ import annotations

STYLE_FIELDS = (
    "fontFamily,weightedFontFamily,fontSize,foregroundColor,bold,italic,backgroundColor,underline"
)

# Canonical style for economics table value cells (revenue / opex / result columns).
ECON_VALUE_STYLE = {
    "font": "Exo 2",
    "sizePt": 10,
    "bold": True,
    "color": [1.0, 1.0, 1.0],
}

ECON_VALUE_PARAGRAPH_ALIGNMENT = "END"


def rgb_color(rgb: list[float]) -> dict:
    return {"red": rgb[0], "green": rgb[1], "blue": rgb[2]}


def golden_style_to_api(style: dict) -> dict:
    weight = 700 if style.get("bold") else 400
    font = style.get("font", "Arial")
    return {
        "fontFamily": font,
        "weightedFontFamily": {"fontFamily": font, "weight": weight},
        "fontSize": {"magnitude": style.get("sizePt", 12), "unit": "PT"},
        "foregroundColor": {"opaqueColor": {"rgbColor": rgb_color(style.get("color", [0, 0, 0]))}},
        "bold": bool(style.get("bold")),
    }


def make_op(
    op_key: str,
    slide_object_id: str,
    target_object_id: str,
    request: dict,
    *,
    rationale: str,
    source_pointer: str,
) -> dict:
    return {
        "op_key": op_key,
        "slide_object_id": slide_object_id,
        "target_object_id": target_object_id,
        "rationale": rationale,
        "source_pointer": source_pointer,
        "google_slides_request": request,
    }


def text_replace_ops(
    slide_object_id: str,
    target_object_id: str,
    new_text: str,
    element: dict,
    *,
    op_prefix: str,
    source_pointer: str,
    alignment: str | None = None,
    style_full_text: bool = False,
) -> list[dict]:
    """3-phase text replace with optional multi-run styling.

    When style_full_text=True, apply the element's primary style across the entire
    inserted string (required for economics value cells whose new text length may
    exceed the golden-map sample run length).
    """
    if len(new_text) > element.get("char_budget", 9999):
        raise ValueError(
            f"{target_object_id}: text len {len(new_text)} exceeds char_budget {element.get('char_budget')}"
        )
    ops: list[dict] = []
    ops.append(
        make_op(
            f"{op_prefix}-clear",
            slide_object_id,
            target_object_id,
            {"deleteText": {"objectId": target_object_id, "textRange": {"type": "ALL"}}},
            rationale=f"Clear text on {target_object_id}",
            source_pointer=source_pointer,
        )
    )
    ops.append(
        make_op(
            f"{op_prefix}-insert",
            slide_object_id,
            target_object_id,
            {"insertText": {"objectId": target_object_id, "text": new_text, "insertionIndex": 0}},
            rationale=f"Insert text on {target_object_id}",
            source_pointer=source_pointer,
        )
    )

    if style_full_text:
        primary = (element.get("runs") or [{}])[0].get("style") or element.get("style") or ECON_VALUE_STYLE
        ops.append(
            make_op(
                f"{op_prefix}-style-full",
                slide_object_id,
                target_object_id,
                {
                    "updateTextStyle": {
                        "objectId": target_object_id,
                        "textRange": {"type": "FIXED_RANGE", "startIndex": 0, "endIndex": len(new_text)},
                        "style": golden_style_to_api(primary),
                        "fields": STYLE_FIELDS,
                    }
                },
                rationale=f"Re-apply full-range style on {target_object_id}",
                source_pointer=source_pointer,
            )
        )
    else:
        runs = element.get("runs") or [{"start": 0, "end": len(new_text), "style": element.get("style", {})}]
        cursor = 0
        for i, run in enumerate(runs):
            run_len = min(run.get("end", len(new_text)) - run.get("start", 0), len(new_text) - cursor)
            if run_len <= 0:
                continue
            end = cursor + run_len
            style = golden_style_to_api(run.get("style") or element.get("style", {}))
            ops.append(
                make_op(
                    f"{op_prefix}-style-{i}",
                    slide_object_id,
                    target_object_id,
                    {
                        "updateTextStyle": {
                            "objectId": target_object_id,
                            "textRange": {"type": "FIXED_RANGE", "startIndex": cursor, "endIndex": end},
                            "style": style,
                            "fields": STYLE_FIELDS,
                        }
                    },
                    rationale=f"Re-apply run style on {target_object_id}",
                    source_pointer=source_pointer,
                )
            )
            cursor = end
        if cursor < len(new_text):
            primary = (element.get("runs") or [{}])[0].get("style") or element.get("style") or {}
            ops.append(
                make_op(
                    f"{op_prefix}-style-tail",
                    slide_object_id,
                    target_object_id,
                    {
                        "updateTextStyle": {
                            "objectId": target_object_id,
                            "textRange": {"type": "FIXED_RANGE", "startIndex": cursor, "endIndex": len(new_text)},
                            "style": golden_style_to_api(primary),
                            "fields": STYLE_FIELDS,
                        }
                    },
                    rationale=f"Re-apply tail style on {target_object_id}",
                    source_pointer=source_pointer,
                )
            )

    if alignment in ("START", "CENTER", "END", "JUSTIFIED"):
        para_align = alignment
    else:
        content_align = element.get("contentAlignment", "TOP")
        align_map = {"TOP": "START", "MIDDLE": "CENTER", "BOTTOM": "END"}
        para_align = align_map.get(content_align, "START")

    ops.append(
        make_op(
            f"{op_prefix}-para",
            slide_object_id,
            target_object_id,
            {
                "updateParagraphStyle": {
                    "objectId": target_object_id,
                    "textRange": {"type": "ALL"},
                    "style": {"alignment": para_align},
                    "fields": "alignment",
                }
            },
            rationale=f"Re-apply paragraph alignment on {target_object_id}",
            source_pointer=source_pointer,
        )
    )
    return ops


def image_replace_op(
    slide_object_id: str,
    target_object_id: str,
    url: str,
    *,
    op_key: str,
    source_pointer: str,
    method: str = "CENTER_INSIDE",
) -> dict:
    return make_op(
        op_key,
        slide_object_id,
        target_object_id,
        {
            "replaceImage": {
                "imageObjectId": target_object_id,
                "url": url,
                "imageReplaceMethod": method,
            }
        },
        rationale=f"Replace image {target_object_id}",
        source_pointer=source_pointer,
    )


def econ_value_replace_ops(
    slide_object_id: str,
    target_object_id: str,
    value_text: str,
    *,
    op_prefix: str,
    source_pointer: str,
    style: dict | None = None,
) -> list[dict]:
    """Economics table value cell: full-string Exo-2 style + right alignment."""
    element = {
        "char_budget": max(len(value_text), 12),
        "style": style or ECON_VALUE_STYLE,
        "runs": [{"start": 0, "end": len(value_text), "style": style or ECON_VALUE_STYLE}],
    }
    return text_replace_ops(
        slide_object_id,
        target_object_id,
        value_text,
        element,
        op_prefix=op_prefix,
        source_pointer=source_pointer,
        alignment=ECON_VALUE_PARAGRAPH_ALIGNMENT,
        style_full_text=True,
    )