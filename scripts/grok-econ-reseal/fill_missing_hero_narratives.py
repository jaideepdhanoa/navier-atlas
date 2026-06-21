#!/usr/bin/env python3
"""Fill missing hero fields for flagged standalone/hub partners."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PARTNERS = ROOT / "partner-pitch" / "partners"
DC = ROOT / "data-clean" / "partners"

HERO_PATCHES = {
    "didi": {
        "title": "Didi × Navier — foiling layer for China's waterfront cities",
        "subtitle": "Premium electric marine mobility across Didi's dense urban waterfront demand surface.",
    },
    "discovery-land": {
        "title": "Discovery Land × Navier — resort archipelago connectivity",
        "subtitle": "Silent foiling hops linking Discovery's private island and coastal destinations.",
    },
    "indrive": {
        "title": "inDrive × Navier — demand-led foiling corridors",
        "subtitle": "Community-priced waterfront legs powered by Navier's electric foiling fleet.",
    },
}


def main() -> int:
    for slug, hero in HERO_PATCHES.items():
        path = PARTNERS / f"{slug}.json"
        if not path.exists():
            continue
        doc = json.loads(path.read_text())
        h_raw = doc.get("hero")
        if isinstance(h_raw, str):
            h = {"title": h_raw}
            doc["hero"] = h
        else:
            h = doc.setdefault("hero", {})
        for k, v in hero.items():
            cur = h.get(k) if isinstance(h, dict) else None
            if not (cur or "").strip():
                h[k] = v
        path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        dc = DC / f"{slug}.json"
        if dc.exists():
            dc.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        print(f"patched {slug}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())