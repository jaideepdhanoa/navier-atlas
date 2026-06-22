#!/usr/bin/env python3
"""Propagate anchor-corridor economics onto Bucket-C BP-exact routes in the sidecar."""
from __future__ import annotations

import copy
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SIDECAR = ROOT / "data-clean/economics_by_route_id.json"
ROUTES = ROOT / "data-clean/ROUTES.json"
PARTNER = ROOT / "partner-pitch/partners/grab-thailand.json"
REPORT = ROOT / "grok-routing-output/grab-thailand-bucketC-econ-report.json"

# anchor route_id -> bucket-C routes that inherit its economics profile
INHERIT = {
    "rn-db5e83248f9d": ["rn-b6a6920513fc", "rn-4cc25e9c8dba", "rn-f2ca85cdc57b", "rn-a103dc26f160"],
    "rn-21d437d2bf84": ["rn-459f23f12c58", "rn-4aea78887c2b"],
    "gcn-9ae16d4c34-shared": ["rn-884b63688113", "rn-cad7f6d9ba79"],
    "gcn-e927fe8958-shared": ["rn-c1aa6c63734d", "rn-5f7af958b634", "rn-a6bcbbd67192", "rn-42fff7b8d918"],
    "gcn-e299366426-shared": [],  # river — mesh routes are bucket-C only elsewhere
}


def route_features(obj):
    return obj if isinstance(obj, list) else obj.get("features", [])


def main() -> int:
    side = json.loads(SIDECAR.read_text())
    by_rid = {r["route_id"]: r for r in side["records"]}
    feats = {f["properties"]["id"]: f for f in route_features(json.loads(ROUTES.read_text()))}

    bound = []
    missing_parent = []
    missing_feat = []

    for parent, children in INHERIT.items():
        parent_rec = by_rid.get(parent)
        if not parent_rec:
            missing_parent.append(parent)
            continue
        for rid in children:
            feat = feats.get(rid)
            if not feat:
                missing_feat.append(rid)
                continue
            p = feat["properties"]
            rec = copy.deepcopy(parent_rec)
            rec["route_id"] = rid
            rec["corridor"] = f"{p.get('from_label') or p.get('from')} -> {p.get('to_label') or p.get('to')}"
            rec["distance_nm"] = p.get("distance_nm")
            rec["authored_for"] = "grab-thailand"
            rec["_economics_inherit"] = parent
            rec["_bucketC_thailand"] = True
            rec["provenance"] = {
                **(rec.get("provenance") or {}),
                "inherit": f"anchor {parent} (BP-exact Bucket-C mesh)",
            }
            by_rid[rid] = rec
            bound.append(rid)

    # Pattaya / Koh Chang / Koh Larn mesh — no anchor economics; mark pending
    partner = json.loads(PARTNER.read_text())
    mesh_ids = [j["route_id"] for j in partner.get("connected_city_mesh", [])]
    for rid in mesh_ids:
        if rid in by_rid:
            continue
        feat = feats.get(rid)
        if not feat:
            continue
        p = feat["properties"]
        by_rid[rid] = {
            "route_id": rid,
            "corridor": f"{p.get('from_label') or p.get('from')} -> {p.get('to_label') or p.get('to')}",
            "distance_nm": p.get("distance_nm"),
            "authored_for": "grab-thailand",
            "status": "pending_demand_anchor",
            "_bucketC_thailand": True,
            "provenance": {"note": "Bucket-C mesh; no cascade-ready demand record yet"},
        }
        bound.append(rid)

    side["records"] = list(by_rid.values())
    side["_meta"]["records"] = len(side["records"])
    side["_meta"]["generated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    SIDECAR.write_text(json.dumps(side, indent=1) + "\n")

    report = {
        "bound_or_pending": len(bound),
        "inherited_from_anchor": len([r for r in bound if r in feats and by_rid[r].get("_economics_inherit")]),
        "missing_parent": missing_parent,
        "missing_feat": missing_feat,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())