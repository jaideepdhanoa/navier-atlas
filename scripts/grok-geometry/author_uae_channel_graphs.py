#!/usr/bin/env python3
"""Author + self-validate UAE channel graph v1 (Palm, Creek, Marina)."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "grok-geometry"))

from shapely import wkb
from shapely.geometry import LineString, mapping, shape

from route_land_qa import evaluate_route  # noqa: E402

OUT_DIR = ROOT / "data-clean" / "channel_graphs"
WKB_V2 = ROOT / "grok-routing-output" / "uae_gulf_land_v2.wkb"
RECEIPT = ROOT / "handoff" / "partner-map-model" / "UAE-CHANNEL-GRAPHS-v2.json"

# Hand-authored centerlines from satellite/OSM + LB-208 Palm land mask gaps.
GRAPHS: dict[str, dict] = {
    "uae-palm": {
        "label": "Palm Jumeirah trunk + frond channels",
        "bbox": [55.10, 25.08, 55.17, 25.15],
        "segments": {
            "trunk_spine": [
                [55.1412, 25.084],
                [55.1414, 25.098],
                [55.1415, 25.112],
                [55.1416, 25.124],
                [55.1410, 25.136],
            ],
            "west_frond_W": [
                [55.1412, 25.105],
                [55.128, 25.100],
                [55.118, 25.098],
                [55.110, 25.106],
            ],
            "west_frond_M": [
                [55.1412, 25.108],
                [55.125, 25.104],
                [55.115, 25.100],
            ],
            "east_frond_FIVE": [
                [55.1415, 25.102],
                [55.148, 25.104],
                [55.152, 25.110],
            ],
            "east_frond_RIXOS": [
                [55.1415, 25.115],
                [55.150, 25.118],
                [55.153, 25.126],
            ],
            "crescent_arc": [
                [55.152, 25.108],
                [55.158, 25.114],
                [55.160, 25.122],
                [55.155, 25.130],
            ],
        },
    },
    "uae-marina": {
        "label": "Dubai Marina / JBR / Harbour basin",
        "bbox": [55.12, 25.06, 55.16, 25.11],
        "segments": {
            "marina_channel": [
                [55.138, 25.068],
                [55.140, 25.074],
                [55.142, 25.080],
                [55.144, 25.086],
                [55.146, 25.092],
            ],
            "jbr_offshore": [
                [55.146, 25.078],
                [55.150, 25.082],
                [55.154, 25.088],
            ],
            "harbour_approach": [
                [55.154, 25.088],
                [55.152, 25.094],
                [55.148, 25.098],
                [55.142, 25.100],
            ],
            "bluewaters_link": [
                [55.146, 25.092],
                [55.148, 25.096],
                [55.150, 25.100],
            ],
        },
    },
    "uae-creek": {
        "label": "Dubai Creek + Business Bay connector",
        "bbox": [55.28, 25.20, 55.36, 25.28],
        "segments": {
            "creek_mouth": [
                [55.300, 25.265],
                [55.310, 25.258],
                [55.320, 25.252],
                [55.330, 25.248],
            ],
            "creek_upper": [
                [55.330, 25.248],
                [55.338, 25.242],
                [55.345, 25.236],
            ],
            "business_bay": [
                [55.345, 25.236],
                [55.352, 25.228],
                [55.358, 25.220],
            ],
            "festival_city_apron": [
                [55.320, 25.252],
                [55.328, 25.245],
                [55.335, 25.238],
            ],
        },
    },
    "uae-abudhabi": {
        "label": "Abu Dhabi islands — Yas / Saadiyat / Lulu / Reem / Hudayriyat",
        "bbox": [54.28, 24.38, 54.68, 24.58],
        "segments": {
            "yas_saadiyat": [
                [54.606, 24.481],
                [54.580, 24.500],
                [54.550, 24.520],
                [54.520, 24.535],
                [54.490, 24.545],
            ],
            "saadiyat_lulu": [
                [54.490, 24.545],
                [54.450, 24.530],
                [54.410, 24.510],
                [54.370, 24.495],
                [54.341, 24.501],
            ],
            "lulu_reem": [
                [54.341, 24.501],
                [54.360, 24.495],
                [54.390, 24.492],
                [54.403, 24.492],
            ],
            "reem_hudayriyat": [
                [54.403, 24.492],
                [54.380, 24.470],
                [54.350, 24.440],
                [54.320, 24.420],
                [54.300, 24.405],
            ],
            "yas_marina_apron": [
                [54.606, 24.481],
                [54.620, 24.470],
                [54.630, 24.460],
            ],
        },
    },
    "uae-deira": {
        "label": "Deira Islands / Palm Deira apron channels",
        "bbox": [55.30, 25.28, 55.38, 25.36],
        "segments": {
            "deira_coast_apron": [
                [55.320, 25.285],
                [55.330, 25.295],
                [55.340, 25.305],
                [55.350, 25.315],
            ],
            "palm_deira_spine": [
                [55.350, 25.315],
                [55.355, 25.325],
                [55.360, 25.335],
                [55.365, 25.345],
            ],
            "deira_creek_mouth": [
                [55.320, 25.285],
                [55.310, 25.278],
                [55.300, 25.270],
            ],
            "island_ring_W": [
                [55.340, 25.305],
                [55.332, 25.312],
                [55.325, 25.320],
            ],
            "island_ring_E": [
                [55.350, 25.315],
                [55.358, 25.322],
                [55.365, 25.330],
            ],
        },
    },
}


def line_feature(seg_id: str, coords: list, area: str, label: str) -> dict:
    return {
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": coords},
        "properties": {
            "id": f"{area}__{seg_id}",
            "area": area,
            "segment": seg_id,
            "label": label,
            "authored_by": "grok/author_uae_channel_graphs",
            "version": "v2",
        },
    }


def validate_segment(coords: list, land) -> dict:
    ls = LineString(coords)
    ev = evaluate_route(coords, sea_nm=ls.length * 60.0)
    samples = 0
    land_hits = 0
    for i in range(1, len(coords)):
        mid = [(coords[i - 1][0] + coords[i][0]) / 2, (coords[i - 1][1] + coords[i][1]) / 2]
        samples += 1
        if land.contains(shape({"type": "Point", "coordinates": mid})):
            land_hits += 1
    return {
        "qa_pass": ev["qa_pass"],
        "interior_land_km": ev["interior_land_km"],
        "sinuosity": ev.get("sinuosity"),
        "midpoint_land_hits": land_hits,
        "midpoint_samples": samples,
    }


def main() -> None:
    land = wkb.loads(WKB_V2.read_bytes())
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    receipt = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "version": "v2",
        "areas": {},
    }

    for area, spec in GRAPHS.items():
        features = []
        seg_reports = {}
        for seg_id, coords in spec["segments"].items():
            features.append(line_feature(seg_id, coords, area, spec["label"]))
            seg_reports[seg_id] = validate_segment(coords, land)

        fc = {
            "type": "FeatureCollection",
            "properties": {
                "area": area,
                "label": spec["label"],
                "bbox": spec["bbox"],
                "authored_by": "grok/author_uae_channel_graphs",
                "version": "v2",
            },
            "features": features,
        }
        out_path = OUT_DIR / f"{area}.geojson"
        out_path.write_text(json.dumps(fc, indent=1) + "\n")

        fails = [k for k, v in seg_reports.items() if not v["qa_pass"]]
        receipt["areas"][area] = {
            "path": str(out_path.relative_to(ROOT)),
            "segments": len(features),
            "segment_qa": seg_reports,
            "pass": len(fails) == 0,
            "failing_segments": fails,
        }
        status = "PASS" if not fails else f"FAIL ({len(fails)} segments)"
        print(f"{area}: {len(features)} segments — {status}")

    RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"receipt → {RECEIPT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()