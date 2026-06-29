#!/usr/bin/env python3
"""Cap UAE intra-city mesh traffic_weight on partner-visible routes (A3 mesh discipline)."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROUTES = ROOT / "data-clean" / "ROUTES.json"
RECEIPT = ROOT / "handoff" / "partner-map-model" / "UAE-MESH-TRAFFIC-CAP-RECEIPT.json"
UAE_CITIES = {
    "dubai-uae", "abu-dhabi-uae", "sharjah-uae", "ras-al-khaimah-uae",
    "fujairah-uae", "ajman-uae", "umm-al-quwain-uae",
}
MESH_CAP = 0.25
MARQUEE_FLOOR = 0.45


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--cap", type=float, default=MESH_CAP)
    args = ap.parse_args()

    feats = json.loads(ROUTES.read_text())
    capped = kept = 0
    rows = []

    for f in feats:
        p = f.get("properties") or {}
        fc, tc = p.get("from_city_id"), p.get("to_city_id")
        if fc not in UAE_CITIES and tc not in UAE_CITIES:
            continue
        ec = p.get("edge_class") or ""
        tw = float(p.get("traffic_weight") or 0)
        if ec not in ("intra-city", "local", "intra-cluster-spoke") and tw < 0.35:
            continue
        if tw <= args.cap or p.get("_marquee"):
            kept += 1
            continue
        new_tw = args.cap
        if tw >= MARQUEE_FLOOR and p.get("_marquee"):
            new_tw = min(tw, 0.55)
        rows.append({"route_id": p.get("id"), "before": tw, "after": new_tw})
        if args.apply:
            p["traffic_weight"] = new_tw
            p["_traffic_cap_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            p["_traffic_cap_source"] = "grok/cap_uae_mesh_traffic"
        capped += 1

    receipt = {"capped": capped, "kept": kept, "cap": args.cap, "rows": rows[:50]}
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")

    if args.apply and capped:
        ROUTES.write_text(json.dumps(feats, ensure_ascii=False) + "\n")

    print(f"UAE mesh traffic cap: capped={capped} kept={kept}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())