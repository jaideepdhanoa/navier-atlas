#!/usr/bin/env python3
"""Sync Kolkata/Chennai brief markets from Rapido template into Uber India derivative."""
from __future__ import annotations

import copy
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PARTNERS = ROOT / "partner-pitch" / "partners"
DRAFT = PARTNERS / "_draft"
BRIEF_IDS = frozenset(
    {"kolkata_hooghly_waterfront", "chennai_ecr_cuddalore_puducherry_coast"}
)
DISPLAY_IDS = frozenset({"mumbai", "goa", "kerala", "andaman"})


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def save(path: Path, doc: dict) -> None:
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")


def uberize(text: str) -> str:
    if not text:
        return text
    text = text.replace("Rapido × Navier", "Uber × Navier")
    text = text.replace("Rapido x Navier", "Uber x Navier")
    text = re.sub(r"\bRapido\b", "Uber", text)
    return text


def uberize_obj(obj):
    if isinstance(obj, str):
        return uberize(obj)
    if isinstance(obj, list):
        return [uberize_obj(x) for x in obj]
    if isinstance(obj, dict):
        return {k: uberize_obj(v) for k, v in obj.items()}
    return obj


def main() -> int:
    rapido = load(PARTNERS / "rapido.json")
    for base in (PARTNERS, DRAFT):
        path = base / "uber-india.json"
        if not path.is_file():
            continue
        doc = load(path)
        ref_brief = [m for m in rapido.get("markets") or [] if m.get("id") in BRIEF_IDS]
        kept = [m for m in doc.get("markets") or [] if m.get("id") in DISPLAY_IDS]
        doc["markets"] = kept + [uberize_obj(copy.deepcopy(m)) for m in ref_brief]
        doc["brief_only_markets"] = [
            {"id": m.get("id"), "label": m.get("label")} for m in ref_brief
        ]
        doc.pop("draft_status", None)
        doc["display"] = "Uber India"
        doc["proposal_status"] = "grok_seal_pass_tasklet_fastlane"
        doc["coverage_note"] = (
            "Six India consumer markets: four display-ready (Mumbai, Goa, Kerala, Andaman) "
            "plus Kolkata and Chennai as brief-only until Atlas city IDs and routes are minted."
        )
        if doc.get("hero"):
            doc["hero"]["title"] = uberize(doc["hero"].get("title", "")).replace("(draft)", "").strip()
            doc["hero"]["subtitle"] = (
                "Six high-value India markets — four sealed on the map; Kolkata and Chennai in proposal until Grok mints geometry."
            )
        save(path, doc)
        dc = ROOT / "data-clean" / "partners" / "uber-india.json"
        save(dc, doc)
        print(f"✓ synced {path.relative_to(ROOT)} — {len(kept)} display + {len(ref_brief)} brief markets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())