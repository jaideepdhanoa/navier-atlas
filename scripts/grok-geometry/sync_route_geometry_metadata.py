#!/usr/bin/env python3
"""Sync ROUTES.json _geometry_land_km from live evaluate_route() — single source of truth."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "grok-geometry"))

from route_land_qa import evaluate_route  # noqa: E402

ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--route", nargs="*")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    raw = json.loads(ROUTES_PATH.read_text())
    feats = raw if isinstance(raw, list) else raw.get("features", [])
    want = set(args.route or [])
    updated = 0

    for f in feats:
        p = f.get("properties") or {}
        rid = p.get("id")
        if want and rid not in want:
            continue
        coords = (f.get("geometry") or {}).get("coordinates") or []
        if len(coords) < 2:
            continue
        ev = evaluate_route(coords, sea_nm=p.get("distance_nm"))
        new_land = round(float(ev.get("interior_land_km") or 0), 4)
        old = p.get("_geometry_land_km")
        if old is not None and abs(float(old) - new_land) < 0.001:
            continue
        if args.apply:
            p["_geometry_land_km"] = new_land
            p["_geometry_sync_at"] = utc_now()
            p["_geometry_sync_source"] = "grok/sync_route_geometry_metadata"
        updated += 1
        print(f"{rid}: {old} → {new_land} pass={ev.get('qa_pass')}")

    if args.apply and updated:
        ROUTES_PATH.write_text(json.dumps(feats, ensure_ascii=False) + "\n")
    print(f"synced {updated} route(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())