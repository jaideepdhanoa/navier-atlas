#!/usr/bin/env python3
"""Build hospitality appendix edit-plan (values + binding → Slides API ops, #112)."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def page_fill_op(page_oid: str, url: str) -> dict:
    return {
        "updatePageProperties": {
            "objectId": page_oid,
            "pageProperties": {
                "pageBackgroundFill": {
                    "stretchedPictureFill": {
                        "contentUrl": url,
                    }
                }
            },
            "fields": "pageBackgroundFill",
        }
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: plan_hospitality_appendix.py <deck-key>", file=sys.stderr)
        return 2
    deck = sys.argv[1]
    d = ROOT / "decks" / deck
    cfg = json.loads((d / "deck.config.json").read_text())
    binding = json.loads((d / "economics-binding.json").read_text())
    values = json.loads((d / f"deck-economics-values-{deck}.json").read_text())

    if binding.get("deck_type") != "hospitality":
        raise SystemExit(f"{deck} is not hospitality deck_type")

    ops = []
    for bg in binding.get("appendix_backgrounds") or []:
        url = bg.get("source_url")
        if not url:
            continue
        ops.append({
            "op_id": f"hosp-bg-{bg['slide_index']}",
            "slide_object_id": bg["page_object_id"],
            "slide_index": bg["slide_index"],
            "kind": "page_background_fill",
            "asset_ref": bg.get("asset_ref"),
            "google_slides_request": page_fill_op(bg["page_object_id"], url),
        })

    plan = {
        "deck_key": deck,
        "presentation_id": cfg.get("deck_id"),
        "mode": "slides_api_batch_update",
        "deck_type": "hospitality",
        "request_summary": f"Hospitality appendix page-fills + values ({len(ops)} bg ops)",
        "safety": {
            "no_pptx_roundtrip": True,
            "no_full_deck_replace": True,
            "preserve_object_ids": True,
            "human_review_required_for_external_send": True,
        },
        "operations": ops,
        "appendix_values_ref": str(d / f"deck-economics-values-{deck}.json"),
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "_note": "Text ops for appendix_cards require live object_id map — bind separately after manifest pull.",
    }
    out = d / "deck-hospitality-appendix-plan.json"
    out.write_text(json.dumps(plan, indent=2) + "\n")
    print(json.dumps({"operations": len(ops), "out": str(out)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())