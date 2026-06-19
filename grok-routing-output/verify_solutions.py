#!/usr/bin/env python3
"""Post-process route-solutions.jsonl with official qa_land_crossing gate."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CODE = ROOT / "_review/grok-routing-v2/grok-routing-v2/code"
sys.path.insert(0, str(CODE))

from qa_land_crossing import evaluate_route, load_overlay

INP = Path(__file__).parent / "route-solutions.jsonl"
OUT = INP
WKB = Path(__file__).parent / "uae_gulf_land_v2.wkb"
THRESH = 0.05


def main():
    try:
        from global_land_mask import globe as coarse
    except Exception:
        coarse = None

    overlay, tree = load_overlay(WKB)
    rows = [json.loads(l) for l in INP.read_text().splitlines() if l.strip()]
    ok = 0
    for row in rows:
        if not row.get("geometry"):
            continue
        coords = row["geometry"]["coordinates"]
        sea_nm = row.get("distance_nm_geom") or 0
        step = 0.15 if sea_nm > 30 else 0.05
        m = evaluate_route(coords, coarse, overlay, tree, step_km=step)
        row["interior_land_km"] = m["interior_land_km"]
        if m["interior_land_km"] > THRESH:
            row["qa_pass"] = False
            row["reason"] = f"qa_land_crossing interior_land_km={m['interior_land_km']} > {THRESH}"
            row["geometry"] = None
            row.pop("waypoints_authored", None)
            row.pop("distance_nm_geom", None)
        else:
            row["qa_pass"] = True
            row.pop("reason", None)
            ok += 1

    with OUT.open("w") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")

    qa_fc = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"id": r.get("route_id") or f"{r['from_id']}->{r['to_id']}", "distance_nm": r.get("distance_nm_geom", 1)},
                "geometry": r["geometry"],
            }
            for r in rows if r.get("geometry")
        ],
    }
    (Path(__file__).parent / "ROUTES-solutions-qa.json").write_text(json.dumps(qa_fc))
    print(f"QA pass: {ok}/{sum(1 for r in rows if r.get('geometry') or r.get('qa_pass'))} with geometry")
    solved = sum(1 for r in rows if r.get("qa_pass"))
    print(f"Solved: {solved}/{len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())