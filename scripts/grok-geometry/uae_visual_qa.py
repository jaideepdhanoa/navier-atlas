#!/usr/bin/env python3
"""Programmatic visual-truth proxy for UAE partner pages (A5 receipt)."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "grok-geometry"))

from route_land_qa import evaluate_route  # noqa: E402

ROUTES = ROOT / "data-clean" / "ROUTES.json"
RECEIPT = ROOT / "handoff" / "partner-map-model" / "UAE-VISUAL-QA-RECEIPT.json"
PARTNERS = ("careem", "noon", "bolt", "yango")
UAE_CITIES = {
    "dubai-uae", "abu-dhabi-uae", "sharjah-uae", "ras-al-khaimah-uae",
    "fujairah-uae", "ajman-uae", "umm-al-quwain-uae",
}


def collect_route_ids() -> set[str]:
    rids: set[str] = set()
    for slug in PARTNERS:
        path = ROOT / "data-clean" / "partners" / f"{slug}.json"
        if not path.exists():
            continue
        doc = json.loads(path.read_text())

        def grab(item: dict) -> None:
            rid = item.get("route_id")
            if rid:
                rids.add(rid)

        for j in doc.get("journeys_unlocked") or []:
            grab(j)
        for ph in doc.get("phases") or []:
            for fr in ph.get("featured_routes") or []:
                grab(fr)
        for m in doc.get("markets") or []:
            if "uae" not in str(m.get("id", "")).lower():
                continue
            for j in m.get("journeys_unlocked") or []:
                grab(j)
            for ph in m.get("phases") or []:
                for fr in ph.get("featured_routes") or []:
                    grab(fr)
    return rids


def main() -> int:
    rids = collect_route_ids()
    routes = json.loads(ROUTES.read_text())
    by_id = {(f.get("properties") or {}).get("id"): f for f in routes if (f.get("properties") or {}).get("id")}

    rows = []
    pass_n = fail_n = 0
    for rid in sorted(rids):
        feat = by_id.get(rid)
        if not feat:
            rows.append({"route_id": rid, "status": "missing_route"})
            fail_n += 1
            continue
        p = feat.get("properties") or {}
        coords = (feat.get("geometry") or {}).get("coordinates") or []
        ev = evaluate_route(coords, sea_nm=p.get("distance_nm"))
        ok = ev["qa_pass"] and ev["interior_land_km"] <= 0.4
        row = {
            "route_id": rid,
            "from": p.get("from"),
            "to": p.get("to"),
            "from_city": p.get("from_city_id"),
            "to_city": p.get("to_city_id"),
            "interior_land_km": ev["interior_land_km"],
            "qa_pass": ev["qa_pass"],
            "visual_pass": ok,
            "traffic_weight": p.get("traffic_weight"),
            "method": p.get("_geometry_fix_source"),
        }
        rows.append(row)
        if ok:
            pass_n += 1
        else:
            fail_n += 1

    receipt = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "partners": list(PARTNERS),
        "pages": ["/careem", "/noon", "/bolt", "/yango"],
        "proposal_routes": len(rids),
        "visual_pass": pass_n,
        "visual_fail": fail_n,
        "gate_pass": fail_n == 0,
        "note": "Live evaluate_route() proxy; browser screenshot pass recommended for final sign-off.",
        "routes": rows,
    }
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"UAE visual QA: {pass_n}/{len(rids)} pass fail={fail_n}")
    return 0 if fail_n == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())