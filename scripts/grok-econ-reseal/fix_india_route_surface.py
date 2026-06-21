#!/usr/bin/env python3
"""
Repair India gold route surface: Mandwa jetty geometry, BP endpoint grounding,
and cityIdOf-resolvable from/to nodes for the full india-shared-corridor-spine.

Run before execute_pr58_india_gcc.py and relink_partner_journeys.py --apply.
"""
from __future__ import annotations

import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DC = ROOT / "data-clean"
HANDOFF = ROOT / "handoff" / "partner-map-model"
REPORT = HANDOFF / "india-route-surface-fix-report.json"

sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
from bolt_yango_routing_shared import (  # noqa: E402
    build_bp_index,
    build_city_index,
    build_coastal_path,
    interior_land_km,
    load_land_mask,
    resolve_bp_by_label,
    save_json,
    save_routes,
)

# Canonical Mandwa — BSA Mandwa jetty (M2M Ro-Pax terminal), not offshore alias
MANDWA_BP = "bp-23928783c7"
GATEWAY_BP = "bp-bbf16aee29"
FERRY_WHARF_BP = "bp-ceb6233334"

CITY_DISPLAY_TO_ID = {
    "goa": "goa-india",
    "mumbai harbour": "mumbai-india",
    "kerala backwaters & kochi": "kerala-backwaters-india",
    "andaman & nicobar islands": "andaman-india",
}

LABEL_BP_OVERRIDES: dict[str, str] = {
    "mandwa jetty": MANDWA_BP,
    "mandwa jetty (alibaug)": MANDWA_BP,
    "bsa mandwa": MANDWA_BP,
    "gateway of india": GATEWAY_BP,
    "mumbai harbour": FERRY_WHARF_BP,
    "bhaucha dhakka": "bp-c62d26083c",
    "bhaucha dhakka ferry boat service": "bp-d63ba7c11e",
    "ferry wharf (bhaucha dhakka)": FERRY_WHARF_BP,
    "elephanta caves": "bp-74883ead4d",
    "elephanta island jetty": "bp-758332246f",
    "mora": "bp-e9f5763810",
    "bambooflat jetty": "bp-96da0f1d7c",
    "shaheed dweep jetty": "bp-56fad569af",
}

PHANTOM_BP_REMAP: dict[str, str] = {
    "bp-f3a60ae926": MANDWA_BP,
    "bp-571dfc0761": MANDWA_BP,
    "bp-bfee4933bd": FERRY_WHARF_BP,
    "bp-22ab41507a": FERRY_WHARF_BP,
    "bp-d74b6cb609": GATEWAY_BP,
    "bp-31136bbc1c": "bp-d63ba7c11e",
    "bp-b378b4561f": "bp-c62d26083c",
    "bp-60cbf83148": "bp-2130ef485c",
    "bp-26488d2f93": "bp-e9f5763810",
    "bp-da6440fb58": "bp-74883ead4d",
    "bp-173d84a334": "bp-e72baeed4b",
    "bp-af908e47ec": "bp-647ad213b3",
    "bp-68bbe75303": "bp-7982c70b13",
    "bp-fcf5a98fc8": "bp-410c233a2d",
    "bp-99fc48f192": "bp-7e541e75f4",
    "bp-bfee4933bd": FERRY_WHARF_BP,
}


def norm(s: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def hav_km(a: tuple[float, float], b: tuple[float, float]) -> float:
    lat1, lon1 = math.radians(a[1]), math.radians(a[0])
    lat2, lon2 = math.radians(b[1]), math.radians(b[0])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 6371.0 * 2 * math.asin(min(1.0, math.sqrt(h)))


def resolve_endpoint(
    node_id: str | None,
    label: str | None,
    city_id: str | None,
    bp_idx: dict,
) -> str | None:
    if node_id and node_id.endswith("-india"):
        return node_id
    if node_id and node_id.startswith("mumbai-india__"):
        return node_id
    if node_id and node_id in PHANTOM_BP_REMAP:
        return PHANTOM_BP_REMAP[node_id]
    if node_id and node_id in bp_idx:
        return node_id
    if label:
        override = LABEL_BP_OVERRIDES.get(label.strip().lower())
        if override:
            return override
        bp = resolve_bp_by_label(city_id, label, bp_idx)
        if bp:
            return bp
    if node_id:
        mapped = CITY_DISPLAY_TO_ID.get(str(node_id).strip().lower())
        if mapped:
            return mapped
    if label:
        mapped = CITY_DISPLAY_TO_ID.get(label.strip().lower())
        if mapped:
            return mapped
    return node_id


def endpoint_coords(node_id: str | None, bp_idx: dict, cities: set[str]) -> tuple[float, float] | None:
    if not node_id:
        return None
    if node_id in bp_idx:
        return bp_idx[node_id]["coords"]
    if node_id in cities:
        return None
    return None


def fix_mandwa_bp(fbt: dict, bp_idx: dict) -> list[str]:
    changes: list[str] = []
    bsa = bp_idx.get(MANDWA_BP, {}).get("coords")
    if not bsa:
        return changes
    for bucket in fbt:
        for feat in fbt.get(bucket, []) or []:
            p = feat.get("properties", {})
            if p.get("id") != "bp-571dfc0761":
                continue
            old = feat.get("geometry", {}).get("coordinates")
            feat["geometry"] = {"type": "Point", "coordinates": [bsa[0], bsa[1]]}
            p["_pr62_relocated"] = "aligned to BSA Mandwa M2M Ro-Pax terminal"
            p["_pr62_relocated_at"] = datetime.now(timezone.utc).isoformat()
            changes.append(f"bp-571dfc0761 coords {old} -> {list(bsa)}")
    return changes


def update_crosswalk_mandwa() -> list[str]:
    path = HANDOFF / "INDIA-PRE-CROSSWALK-CITY-ID-MISMATCH-TABLE-2026-06-20.json"
    if not path.is_file():
        return []
    doc = json.loads(path.read_text())
    changes: list[str] = []
    for row in doc.get("city_crosswalk", []):
        if row.get("atlas_city_id") != "mumbai-india":
            continue
        for hit in row.get("exact_bp_hits", []):
            if "mandwa" in (hit.get("alias") or "").lower():
                if hit.get("bp_id") != MANDWA_BP:
                    changes.append(f"crosswalk Mandwa alias {hit.get('bp_id')} -> {MANDWA_BP}")
                    hit["bp_id"] = MANDWA_BP
    if changes:
        save_json(path, doc)
    return changes


def main() -> int:
    fbt = json.loads((DC / "FEATURES_BY_TYPE.json").read_text())
    routes = json.loads((DC / "ROUTES.json").read_text())
    spine = json.loads((HANDOFF / "india-shared-corridor-spine.json").read_text())
    cities_set = {
        f["properties"]["id"]
        for key in ("city", "priority_city")
        for f in fbt.get(key, [])
        if f.get("properties", {}).get("id")
    }

    bp_idx = build_bp_index(fbt)
    city_names = build_city_index(fbt)
    mask = load_land_mask()

    report: dict = {
        "at": datetime.now(timezone.utc).isoformat(),
        "bp_fixes": fix_mandwa_bp(fbt, bp_idx),
        "crosswalk_fixes": update_crosswalk_mandwa(),
        "routes_updated": [],
        "geometry_reminted": [],
        "spine_updated": [],
    }

    route_by_id = {f["properties"]["id"]: f for f in routes if f.get("properties", {}).get("id")}
    spine_by_id = {c["corridor_id"]: c for c in spine.get("corridors", []) if c.get("corridor_id")}

    for rid, corridor in spine_by_id.items():
        feat = route_by_id.get(rid)
        if not feat:
            continue
        props = feat["properties"]
        city_id = props.get("from_city_id") or corridor.get("from_city_id")
        to_city_id = props.get("to_city_id") or corridor.get("to_city_id")

        from_node = resolve_endpoint(
            corridor.get("from_node_id") or props.get("from"),
            props.get("from_label") or corridor.get("from_label"),
            city_id,
            bp_idx,
        )
        to_node = resolve_endpoint(
            corridor.get("to_node_id") or props.get("to"),
            props.get("to_label") or corridor.get("to_label"),
            to_city_id,
            bp_idx,
        )

        # Mandwa corridor hard-bind
        labels = (
            (props.get("from_label") or "").lower(),
            (props.get("to_label") or "").lower(),
        )
        if rid == "ics-45ea784fef":
            # Signature Mumbai → Alibaug run: Gateway of India → BSA Mandwa (M2M Ro-Pax)
            from_node, to_node = GATEWAY_BP, MANDWA_BP
            props["from_label"] = "Gateway of India"
            props["to_label"] = "BSA Mandwa (Alibaug)"
        elif "mandwa" in labels[0] or "mandwa" in labels[1]:
            if "gateway" in labels[0] or "gateway" in labels[1]:
                from_node, to_node = GATEWAY_BP, MANDWA_BP
                if "mandwa" in labels[0]:
                    from_node, to_node = MANDWA_BP, GATEWAY_BP
            elif "mumbai harbour" in labels[1] or "mumbai harbour" in labels[0]:
                if "mandwa" in labels[0]:
                    from_node, to_node = MANDWA_BP, FERRY_WHARF_BP
                else:
                    from_node, to_node = FERRY_WHARF_BP, MANDWA_BP

        old_from, old_to = props.get("from"), props.get("to")
        if from_node != old_from or to_node != old_to:
            props["from"] = from_node
            props["to"] = to_node
            props["from_node"] = from_node
            props["to_node"] = to_node
            props["from_node_id"] = from_node if (from_node or "").startswith("bp-") else None
            props["to_node_id"] = to_node if (to_node or "").startswith("bp-") else None
            report["routes_updated"].append(
                {"route_id": rid, "from": old_from, "to": old_to, "new_from": from_node, "new_to": to_node}
            )

        if corridor.get("from_node_id") != from_node or corridor.get("to_node_id") != to_node:
            corridor["from_node_id"] = from_node
            corridor["to_node_id"] = to_node
            report["spine_updated"].append({"corridor_id": rid, "from": from_node, "to": to_node})

        a = endpoint_coords(from_node, bp_idx, cities_set)
        b = endpoint_coords(to_node, bp_idx, cities_set)
        if a and b:
            coords = feat.get("geometry", {}).get("coordinates") or []
            end = (coords[-1][0], coords[-1][1]) if coords else None
            start = (coords[0][0], coords[0][1]) if coords else None
            drift = max(
                hav_km(start, a) if start else 99,
                hav_km(end, b) if end else 99,
            )
            if drift > 0.5 or rid in {"ics-45ea784fef", "ics-10990b64b9", "ics-1b14a6bcfe"}:
                path = build_coastal_path(a, b, mask)
                land_km = interior_land_km(path, mask)
                feat["geometry"] = {"type": "LineString", "coordinates": path}
                props["_india_surface_fix"] = True
                props["_land_km_interior"] = round(land_km, 4)
                dist_km = sum(
                    hav_km((path[i][0], path[i][1]), (path[i + 1][0], path[i + 1][1]))
                    for i in range(len(path) - 1)
                )
                props["distance_nm"] = round(dist_km / 1.852, 1)
                report["geometry_reminted"].append(
                    {"route_id": rid, "drift_km": round(drift, 2), "end": list(b)}
                )

    save_json(DC / "FEATURES_BY_TYPE.json", fbt)
    save_routes(DC / "ROUTES.json", routes)
    save_json(HANDOFF / "india-shared-corridor-spine.json", spine)
    save_json(REPORT, report)

    # Post-fix visibility count
    city_ids = cities_set

    def city_id_of(nid: str | None) -> str | None:
        if not nid:
            return None
        if nid in city_ids:
            return nid
        row = bp_idx.get(nid)
        if row and row.get("parent_city_id") in city_ids:
            return row["parent_city_id"]
        pre = str(nid).split("__")[0]
        return pre if pre in city_ids else None

    india = {"mumbai-india", "goa-india", "kerala-backwaters-india", "andaman-india"}
    visible = sum(
        1
        for f in routes
        if city_id_of(f["properties"].get("from")) in india
        or city_id_of(f["properties"].get("to")) in india
    )
    print(f"India-scoped routes now visible: {visible}")
    print(f"Updated {len(report['routes_updated'])} routes, reminted {len(report['geometry_reminted'])}")
    print(f"Report: {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())