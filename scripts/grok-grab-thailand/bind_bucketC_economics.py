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
PARTNER_DC = ROOT / "data-clean/partners/grab-thailand.json"
REPORT = ROOT / "grok-routing-output/grab-thailand-bucketC-econ-report.json"

# route_id -> parent route_id (explicit inherit; no demand-anchor required)
INHERIT_FROM: dict[str, str] = {
    # Samui / Phangan mesh
    "rn-b6a6920513fc": "rn-db5e83248f9d",
    "rn-4cc25e9c8dba": "rn-db5e83248f9d",
    "rn-f2ca85cdc57b": "rn-db5e83248f9d",
    "rn-a103dc26f160": "rn-db5e83248f9d",
    "rn-459f23f12c58": "rn-21d437d2bf84",
    "rn-4aea78887c2b": "rn-21d437d2bf84",
    "rn-bb8b5b800f2d": "rn-db5e83248f9d",
    "rn-0e850c291876": "ics-5038f54700",
    # Andaman mesh
    "rn-884b63688113": "gcn-9ae16d4c34-shared",
    "rn-cad7f6d9ba79": "gcn-9ae16d4c34-shared",
    "rn-c1aa6c63734d": "gcn-e927fe8958-shared",
    "rn-5f7af958b634": "gcn-e927fe8958-shared",
    "rn-a6bcbbd67192": "gcn-e927fe8958-shared",
    "rn-42fff7b8d918": "gcn-e927fe8958-shared",
    # Pattaya / Koh Chang mesh (short-hop inherit from island triangle anchor)
    "rn-f09e06bc2910": "rn-db5e83248f9d",
    "rn-2c544de0b887": "rn-f09e06bc2910",
    "rn-b11478b5cb27": "rn-db5e83248f9d",
}


def route_features(obj):
    return obj if isinstance(obj, list) else obj.get("features", [])


def mesh_economics_status(by_rid: dict, rid: str | None) -> tuple[str, str | None]:
    """Return (economics_status, inherit_parent_id) for a mesh route."""
    if not rid:
        return "pending_demand_anchor", None
    rec = by_rid.get(rid)
    if not rec or not rec.get("mid"):
        return "pending_demand_anchor", None
    inherit = rec.get("_economics_inherit")
    if inherit or rec.get("economics_status") == "bound_inherit":
        return "bound_inherit", inherit
    return "bound", None


def patch_partner_mesh_economics(partner: dict, by_rid: dict) -> dict:
    bound = bound_inherit = pending = 0
    for j in partner.get("connected_city_mesh", []):
        status, inherit = mesh_economics_status(by_rid, j.get("route_id"))
        j["economics_status"] = status
        if status == "bound_inherit":
            j["_economics_source"] = "economics_by_route_id.json"
            j["_economics_inherit"] = inherit
            bound_inherit += 1
        elif status == "bound":
            j["_economics_source"] = "economics_by_route_id.json"
            j.pop("_economics_inherit", None)
            bound += 1
        else:
            j.pop("_economics_source", None)
            j.pop("_economics_inherit", None)
            pending += 1
    for market in partner.get("markets", []):
        for j in market.get("journeys_unlocked", []):
            if j.get("_link_source") != "bucketC-thailand":
                continue
            status, inherit = mesh_economics_status(by_rid, j.get("route_id"))
            j["economics_status"] = status
            if status == "bound_inherit":
                j["_economics_source"] = "economics_by_route_id.json"
                j["_economics_inherit"] = inherit
            elif status == "bound":
                j["_economics_source"] = "economics_by_route_id.json"
                j.pop("_economics_inherit", None)
            else:
                j.pop("_economics_source", None)
                j.pop("_economics_inherit", None)
    meta = partner.setdefault("connected_city_mesh_meta", {})
    meta["economics_bound"] = bound + bound_inherit
    meta["economics_bound_inherit"] = bound_inherit
    meta["economics_pending"] = pending
    meta["note"] = (
        f"{bound + bound_inherit}/{bound + bound_inherit + pending} mesh routes bound "
        f"({bound_inherit} inherit from anchor corridors; no demand-anchor required)."
    )
    if partner.get("growth_case", {}).get("_status") == "cascade_complete":
        partner["economics_status"] = {
            **(partner.get("economics_status") or {}),
            "state": "grounded_floor_cascade_complete",
            "grounded_floor": "3 cascade-ready corridors (Samui↔Phangan, Phuket↔Phi Phi, Chao Phraya)",
            "mesh_inherit": f"{bound_inherit} Bucket-C routes inherit anchor economics",
        }
    return {"bound": bound, "bound_inherit": bound_inherit, "pending": pending}


def clone_record(parent_rec: dict, rid: str, props: dict, parent_id: str) -> dict:
    rec = copy.deepcopy(parent_rec)
    rec["route_id"] = rid
    rec["corridor"] = (
        f"{props.get('from_label') or props.get('from')} -> "
        f"{props.get('to_label') or props.get('to')}"
    )
    rec["distance_nm"] = props.get("distance_nm")
    rec["authored_for"] = "grab-thailand"
    rec["status"] = parent_rec.get("status", "grounded")
    rec["_economics_inherit"] = parent_id
    rec["_bucketC_thailand"] = True
    rec["economics_status"] = "bound_inherit"
    rec["provenance"] = {
        **(rec.get("provenance") or {}),
        "inherit": f"anchor {parent_id} (BP-exact Bucket-C mesh; explicit inherit rule)",
    }
    return rec


def main() -> int:
    side = json.loads(SIDECAR.read_text())
    by_rid = {r["route_id"]: r for r in side["records"]}
    feats = {f["properties"]["id"]: f for f in route_features(json.loads(ROUTES.read_text()))}

    inherited = []
    missing_parent = []
    missing_feat = []
    pending = []

    # Multi-pass so chained inherits resolve (Ocean Marina -> Bali Hai -> Samui anchor)
    for _ in range(3):
        for rid, parent_id in INHERIT_FROM.items():
            if rid in by_rid and by_rid[rid].get("_economics_inherit"):
                continue
            parent_rec = by_rid.get(parent_id)
            feat = feats.get(rid)
            if not parent_rec:
                if parent_id not in missing_parent:
                    missing_parent.append(parent_id)
                continue
            if not feat:
                missing_feat.append(rid)
                continue
            by_rid[rid] = clone_record(parent_rec, rid, feat["properties"], parent_id)
            inherited.append(rid)

    for rid in INHERIT_FROM:
        if rid not in by_rid or not by_rid[rid].get("mid"):
            feat = feats.get(rid)
            if feat and rid not in pending:
                pending.append(rid)

    side["records"] = list(by_rid.values())
    side["_meta"]["records"] = len(side["records"])
    side["_meta"]["generated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    SIDECAR.write_text(json.dumps(side, indent=1) + "\n")

    partner = json.loads(PARTNER.read_text())
    mesh_counts = patch_partner_mesh_economics(partner, by_rid)
    PARTNER.write_text(json.dumps(partner, indent=1) + "\n")
    PARTNER_DC.write_text(json.dumps(partner, indent=1) + "\n")

    report = {
        "inherited": len(inherited),
        "inherited_route_ids": sorted(set(inherited)),
        "still_pending": pending,
        "missing_parent": missing_parent,
        "missing_feat": missing_feat,
        "partner_mesh": mesh_counts,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())