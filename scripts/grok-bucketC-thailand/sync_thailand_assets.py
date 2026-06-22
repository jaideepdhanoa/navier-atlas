#!/usr/bin/env python3
"""Sync Thailand city briefs + locale briefs to data-clean."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
THAI_BRIEFS = [
    "bangkok-thailand.json", "koh-samui-thailand.json", "koh-phangan-thailand.json",
    "koh-tao-thailand.json", "pattaya-thailand.json", "koh-chang-thailand.json",
    "koh-larn-thailand.json", "krabi-thailand.json", "koh-phi-phi-thailand.json",
    "phuket-phang-nga-thailand.json",
]


def main() -> int:
    src_b = ROOT / "partner-pitch/city_briefs"
    dst_b = ROOT / "data-clean/city_briefs"
    dst_b.mkdir(parents=True, exist_ok=True)
    for name in THAI_BRIEFS:
        s = src_b / name
        if s.exists():
            shutil.copy2(s, dst_b / name)

    # Merge koh-larn into _index
    idx_path = src_b / "_index.json"
    if idx_path.exists():
        idx = json.loads(idx_path.read_text())
        if not any(e.get("city_id") == "koh-larn-thailand" for e in idx.get("index", [])):
            idx["index"].append({
                "city_id": "koh-larn-thailand",
                "display_name": "Koh Larn",
                "region": "SEA",
                "tier": "connected",
                "posture": "grab_thailand_gulf",
            })
            idx["total_anchors"] = len(idx["index"])
            idx["briefs"] = len(idx["index"])
            idx_path.write_text(json.dumps(idx, indent=1) + "\n")
        shutil.copy2(idx_path, dst_b / "_index.json")

    src_l = ROOT / "partner-pitch/locale_briefs"
    dst_l = ROOT / "data-clean/locale_briefs"
    dst_l.mkdir(parents=True, exist_ok=True)
    for f in src_l.glob("*.json"):
        shutil.copy2(f, dst_l / f.name)

    print(f"synced {len(THAI_BRIEFS)} city briefs + locale_briefs -> data-clean/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())