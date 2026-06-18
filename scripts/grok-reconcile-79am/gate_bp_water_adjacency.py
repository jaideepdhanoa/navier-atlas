#!/usr/bin/env python3
"""Lane #3 — geometry-first water-adjacency for KEEP+HOLD boarding points."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def haversine_km(a, b):
    r = 6371.0088
    lon1, lat1 = math.radians(a[0]), math.radians(a[1])
    lon2, lat2 = math.radians(b[0]), math.radians(b[1])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * r * math.asin(min(1.0, math.sqrt(h)))


def load_mask():
    try:
        from global_land_mask import globe

        return globe
    except Exception:
        return None


def is_water(lon: float, lat: float, mask) -> bool:
    if mask is None:
        return True
    try:
        return not bool(mask.is_land(lat, lon))
    except Exception:
        return True


def water_distance_km(lon: float, lat: float, mask, step_km: float = 0.05, max_km: float = 0.35) -> float:
    if is_water(lon, lat, mask):
        return 0.0
    bearings = [i * 45 for i in range(8)]
    best = max_km
    for deg in bearings:
        br = math.radians(deg)
        d = step_km
        while d <= max_km:
            dlat = (d / r_earth_km) * math.cos(br) * (180 / math.pi)
            dlon = (d / r_earth_km) * math.sin(br) / max(math.cos(math.radians(lat)), 1e-6) * (180 / math.pi)
            if is_water(lon + dlon, lat + dlat, mask):
                best = min(best, d)
                break
            d += step_km
    return round(best, 4)


r_earth_km = 6371.0088


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--max-inland-km", type=float, default=0.15)
    args = ap.parse_args()

    work = Path(args.work)
    dc = work / "atlas-repo" / "data-clean"
    cand_path = work / "grok-routing-output" / "bp-candidates.json"
    candidates = json.loads(cand_path.read_text())
    mask = load_mask()

    report = {"pass": [], "fail": [], "threshold_km": args.max_inland_km}
    for row in candidates:
        lon, lat = row["coords"]
        dist = water_distance_km(lon, lat, mask)
        row["water_distance_km"] = dist
        ok = dist <= args.max_inland_km
        (report["pass"] if ok else report["fail"]).append(
            {"id": row["id"], "name": row["name"], "water_distance_km": dist, "verdict": row["verdict"]}
        )
        row["water_adjacency_pass"] = ok

    out = work / "grok-routing-output" / "bp-water-adjacency-report.json"
    out.write_text(json.dumps(report, indent=2) + "\n")
    cand_path.write_text(json.dumps(candidates, indent=2) + "\n")
    print(f"water-adjacency: pass={len(report['pass'])} fail={len(report['fail'])}")


if __name__ == "__main__":
    main()