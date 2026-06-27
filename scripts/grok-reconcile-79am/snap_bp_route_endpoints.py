#!/usr/bin/env python3
"""Snap route-referenced bp-* POIs toward navigable water (#119 triage wave)."""
from __future__ import annotations

import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
from bolt_yango_shared import is_water, load_land_mask, water_distance_km  # noqa: E402

DC = ROOT / "data-clean"
REPORT_IN = ROOT / "grok-routing-output/bp-water-adjacency-report.json"
REPORT_OUT = ROOT / "grok-routing-output/bp-snap-route-endpoints-report.json"
R_EARTH_KM = 6371.0088


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def snap_to_water(lon: float, lat: float, mask, max_km: float = 0.5) -> tuple[float, float, float]:
    if is_water(lon, lat, mask):
        return lon, lat, 0.0
    best = (lon, lat, water_distance_km(lon, lat, mask, max_km=max_km))
    if best[2] <= 0.15:
        return best
    step = 0.025
    for ring in range(1, int(max_km / step) + 1):
        r_km = ring * step
        for deg in range(0, 360, 15):
            br = math.radians(deg)
            dlat = (r_km / R_EARTH_KM) * math.cos(br) * (180 / math.pi)
            dlon = (r_km / R_EARTH_KM) * math.sin(br) / max(math.cos(math.radians(lat)), 1e-6) * (180 / math.pi)
            nlng, nlat = lon + dlon, lat + dlat
            if is_water(nlng, nlat, mask):
                dist = water_distance_km(lon, lat, mask, max_km=r_km)
                if dist <= 0.15:
                    return nlng, nlat, 0.0
                if dist < best[2]:
                    best = (nlng, nlat, dist)
    return best


def main() -> int:
    report = json.loads(REPORT_IN.read_text())
    targets = {r["id"] for r in report.get("true_fail", report.get("fail", [])) if r["id"].startswith("bp-")}
    if not targets:
        print("no bp-* true_fail targets")
        return 0

    mask = load_land_mask()
    fbt = json.loads((DC / "FEATURES_BY_TYPE.json").read_text())
    by_id: dict[str, dict] = {}
    for feat in fbt.get("poi", []):
        pid = (feat.get("properties") or {}).get("id")
        if pid:
            by_id[pid] = feat

    snapped = []
    missing = []
    unchanged = []
    for pid in sorted(targets):
        feat = by_id.get(pid)
        if not feat:
            missing.append(pid)
            continue
        coords = feat.get("geometry", {}).get("coordinates")
        if not coords or len(coords) < 2:
            missing.append(pid)
            continue
        lon, lat = float(coords[0]), float(coords[1])
        slon, slat, residual = snap_to_water(lon, lat, mask)
        if slon == lon and slat == lat and residual > 0.15:
            unchanged.append({"id": pid, "residual_km": residual})
            continue
        feat["geometry"]["coordinates"] = [round(slon, 6), round(slat, 6)]
        p = feat.setdefault("properties", {})
        p.setdefault("_bp_snap_log", []).append(
            {
                "at": utc_now(),
                "from": [lon, lat],
                "to": [slon, slat],
                "residual_km": residual,
                "lane": "grok/snap_bp_route_endpoints",
            }
        )
        snapped.append({"id": pid, "residual_km": residual, "name": p.get("name")})

    (DC / "FEATURES_BY_TYPE.json").write_text(json.dumps(fbt, indent=2, ensure_ascii=False) + "\n")
    out = {
        "at": utc_now(),
        "targets": len(targets),
        "snapped": len(snapped),
        "unchanged": len(unchanged),
        "missing": len(missing),
        "snapped_sample": snapped[:20],
        "still_inland_sample": unchanged[:20],
    }
    REPORT_OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(f"snapped={len(snapped)} unchanged={len(unchanged)} missing={len(missing)}")
    print(f"report: {REPORT_OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())