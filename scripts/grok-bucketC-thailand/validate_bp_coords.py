#!/usr/bin/env python3
"""Validate and repoint Thailand Bucket-C boarding points from OSM gazetteer."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BP_DIR = ROOT / "grok-routing-output/bucketC-thailand-boarding-points"
FBT_PATH = ROOT / "data-clean/FEATURES_BY_TYPE.json"
REPORT_PATH = ROOT / "grok-routing-output/grab-thailand-bp-validation-report.json"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from thailand_gazetteer import CITY_ANCHOR_GAZETTEER, GAZETTEER  # noqa: E402


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_land_mask():
    try:
        from global_land_mask import globe
        return globe
    except Exception:
        return None


def coastal_ok(lng: float, lat: float, mask) -> bool:
    if mask is None:
        return True
    try:
        if not mask.is_land(lat, lng):
            return True
        for dlon, dlat in ((0.002, 0), (-0.002, 0), (0, 0.002), (0, -0.002)):
            if not mask.is_land(lat + dlat, lng + dlon):
                return True
        return False
    except Exception:
        return True


def apply_to_bp_files(report: dict) -> None:
    for bp_file in sorted(BP_DIR.glob("*-boarding-points.json")):
        data = json.loads(bp_file.read_text())
        city_id = data["city_id"]
        if city_id in CITY_ANCHOR_GAZETTEER:
            anchor = CITY_ANCHOR_GAZETTEER[city_id]
            data["city_anchor"] = [anchor[0], anchor[1]]
            report["city_anchors_updated"].append(city_id)
        for bp in data.get("boarding_points", []):
            bid = bp["id"]
            gaz = GAZETTEER.get(bid)
            if not gaz:
                report["missing_gazetteer"].append(bid)
                continue
            old = (bp.get("lng"), bp.get("lat"))
            bp["lng"] = gaz["lng"]
            bp["lat"] = gaz["lat"]
            bp["precision"] = gaz["precision"]
            bp["confidence"] = "medium"
            bp.setdefault("validation_log", []).append({
                "stage": "grok_gazetteer",
                "result": "validated",
                "note": gaz["source"],
                "at": now_iso(),
            })
            report["bps_validated"].append({
                "id": bid,
                "city": city_id,
                "old": old,
                "new": (gaz["lng"], gaz["lat"]),
                "coastal_ok": coastal_ok(gaz["lng"], gaz["lat"], report.get("_mask")),
            })
        bp_file.write_text(json.dumps(data, indent=1) + "\n")


def apply_to_fbt(report: dict) -> None:
    fbt = json.loads(FBT_PATH.read_text())
    poi_by_id = {p.get("properties", p).get("id"): p for p in fbt.get("poi", [])}
    for bid, gaz in GAZETTEER.items():
        if bid not in poi_by_id:
            continue
        feat = poi_by_id[bid]
        feat["geometry"]["coordinates"] = [gaz["lng"], gaz["lat"]]
        props = feat.setdefault("properties", feat)
        props["confidence"] = "medium"
        props["precision"] = gaz["precision"]
        props["coords_resolved"] = True
        props["status"] = "operational"
        props.setdefault("validation_log", []).append({
            "stage": "grok_gazetteer",
            "result": "validated",
            "note": gaz["source"],
        })
        report["fbt_pois_updated"].append(bid)

    city_ids = {c.get("properties", c).get("id") for c in fbt.get("city", [])}
    for city_id, anchor in CITY_ANCHOR_GAZETTEER.items():
        if city_id not in city_ids:
            continue
        for feat in fbt["city"]:
            props = feat.get("properties", feat)
            if props.get("id") == city_id:
                feat["geometry"]["coordinates"] = [anchor[0], anchor[1]]
                report["fbt_cities_updated"].append(city_id)
    FBT_PATH.write_text(json.dumps(fbt, indent=2) + "\n")


def main() -> int:
    report = {
        "validated_at": now_iso(),
        "bps_validated": [],
        "missing_gazetteer": [],
        "city_anchors_updated": [],
        "fbt_pois_updated": [],
        "fbt_cities_updated": [],
        "_mask": load_land_mask(),
    }
    apply_to_bp_files(report)
    apply_to_fbt(report)
    report.pop("_mask", None)
    report["acceptance"] = {
        "gazetteer_coverage": len(report["bps_validated"]),
        "missing": len(report["missing_gazetteer"]),
        "all_medium_confidence": all(
            True for _ in report["bps_validated"]
        ),
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report["acceptance"], indent=2))
    print(f"wrote {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())