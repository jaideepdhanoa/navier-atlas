#!/usr/bin/env python3
"""Mint RAK↔Abu Dhabi / Sharjah / Fujairah inter-emirate spine rows from coastal geometry."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))

from bolt_yango_routing_shared import (  # noqa: E402
    build_city_index,
    build_coastal_path,
    interior_land_km,
    load_json,
    load_land_mask,
    make_route_feature,
    mint_route_id,
    route_features,
    save_json,
    save_routes,
)

DC = ROOT / "data-clean"
HANDOFF = ROOT / "handoff" / "partner-map-model"
REPORT = HANDOFF / "rak-other-uae-mint-report.json"
TAG = "rak_other_uae"

CITY_COORDS: dict[str, tuple[float, float]] = {
    "dubai-uae": (55.139787, 25.081055),
    "abu-dhabi-uae": (54.609265, 24.475629),
    "ras-al-khaimah-uae": (55.9754, 25.7895),
    "sharjah-uae": (55.3818, 25.3573),
    "fujairah-uae": (56.3414, 25.1213),
}

CORRIDORS = [
    ("ras-al-khaimah-uae", "abu-dhabi-uae", "Ras Al Khaimah", "Abu Dhabi"),
    ("ras-al-khaimah-uae", "sharjah-uae", "Ras Al Khaimah", "Sharjah"),
    ("ras-al-khaimah-uae", "fujairah-uae", "Ras Al Khaimah", "Fujairah"),
    ("abu-dhabi-uae", "ras-al-khaimah-uae", "Abu Dhabi", "Ras Al Khaimah"),
    ("sharjah-uae", "ras-al-khaimah-uae", "Sharjah", "Ras Al Khaimah"),
    ("fujairah-uae", "ras-al-khaimah-uae", "Fujairah", "Ras Al Khaimah"),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def append_spine(minted: list[dict]) -> None:
    spine = load_json(HANDOFF / "uae-gulf-shared-corridor-spine.json")
    corridors = spine.setdefault("corridors", [])
    existing = {c.get("corridor_id") for c in corridors}
    for m in minted:
        rid = m["route_id"]
        if rid in existing:
            continue
        corridors.append({
            "corridor_id": rid,
            "market_key": "inter_emirate_uae",
            "country_or_cross_border_pair": f"{m['from_city_id']} ↔ {m['to_city_id']}",
            "from_node_id": m["from_city_id"],
            "to_node_id": m["to_city_id"],
            "from_city_id": m["from_city_id"],
            "to_city_id": m["to_city_id"],
            "from_label": m["from_label"],
            "to_label": m["to_label"],
            "route_nm": m["distance_nm"],
            "vessel_gate": "N30 Pioneer II commercial-now",
            "domestic_or_cross_border": "inter_emirate",
            "current_geometry_status": "geometry_present",
            "usable_by_rakta": True,
            "authority_or_platform_relevance": "commercial-now candidate",
            "economics_status": "economics_pending",
            "regulatory_note": "Grok rak-other-uae mint 2026-06-21",
        })
        existing.add(rid)
    summary = spine.setdefault("summary_by_market", {}).setdefault("inter_emirate_uae", {})
    rows = [c for c in corridors if c.get("market_key") == "inter_emirate_uae"]
    summary["total"] = len(rows)
    summary["geometry_present"] = len(rows)
    save_json(HANDOFF / "uae-gulf-shared-corridor-spine.json", spine)


def append_ledger(minted: list[dict]) -> None:
    path = HANDOFF / "rakta-route-seal-ledger-2026-06-21.json"
    doc = load_json(path)
    routes = doc.setdefault("routes", [])
    existing = {r.get("spine_corridor_id") for r in routes}
    for m in minted:
        rid = m["route_id"]
        if rid in existing:
            continue
        routes.append({
            "partner_id": "rakta",
            "spine_corridor_id": rid,
            "route_id_for_partner_json": None,
            "route_id_hold_reason": "Grok must re-seal / exact-bind this corridor before live route chips or economics sidecar binding.",
            "classification": "proposal_active_rak_dubai_inter_emirate",
            "market_key": "inter_emirate_uae",
            "from_city_id": m["from_city_id"],
            "to_city_id": m["to_city_id"],
            "from_node_id": m["from_city_id"],
            "to_node_id": m["to_city_id"],
            "from_label": m["from_label"],
            "to_label": m["to_label"],
            "distance_nm_spine": m["distance_nm"],
            "vessel_gate_spine": "N30 Pioneer II commercial-now",
            "geometry_status_spine": "geometry_present",
            "authority_relevance_spine": "commercial-now candidate",
            "economics_status_spine": "economics_pending",
            "guardrail": "RAK↔other-UAE inter-emirate minted from coastal spine extraction.",
        })
        existing.add(rid)
    doc.setdefault("summary", {})["rak_other_uae_minted"] = len(minted)
    save_json(path, doc)


def update_scope() -> None:
    path = HANDOFF / "rakta-scope-2026-06-21.json"
    doc = load_json(path)
    for m in doc.get("markets") or []:
        if m.get("id") == "rak-other-uae":
            m["status"] = "geometry_present_grok_mint"
            m["note"] = "RAK↔Abu Dhabi/Sharjah/Fujairah coastal spines minted in gold ROUTES.json"
    save_json(path, doc)


def main() -> int:
    fbt = load_json(DC / "FEATURES_BY_TYPE.json")
    cities = build_city_index(fbt)
    mask = load_land_mask()
    routes = route_features(load_json(DC / "ROUTES.json"))
    existing = {r["properties"]["id"] for r in routes if r.get("properties", {}).get("id")}

    minted: list[dict] = []
    for fc, tc, fl, tl in CORRIDORS:
        if fc not in CITY_COORDS or tc not in CITY_COORDS:
            continue
        rid = mint_route_id(fc, tc, tag=TAG)
        a, b = CITY_COORDS[fc], CITY_COORDS[tc]
        if rid in existing:
            feat = next(r for r in routes if r["properties"]["id"] == rid)
            dist = feat["properties"]["distance_nm"]
            status = "exists"
        else:
            coords = build_coastal_path(a, b, mask)
            land_km = interior_land_km(coords, mask)
            feat = make_route_feature(fc, tc, fl, tl, fc, tc, coords, cities, source=TAG, land_km=land_km)
            feat["properties"]["id"] = rid
            routes.append(feat)
            existing.add(rid)
            dist = feat["properties"]["distance_nm"]
            status = "minted"
            print(f"minted {rid} {fl} → {tl} ({dist} nm)")

        minted.append({
            "route_id": rid,
            "from_city_id": fc,
            "to_city_id": tc,
            "from_label": fl,
            "to_label": tl,
            "distance_nm": dist,
            "status": status,
        })

    save_routes(DC / "ROUTES.json", routes)

    allow_path = DC / "route_water_allowlist.json"
    if allow_path.exists():
        allow = load_json(allow_path)
        ids = list(allow.get("ids", []))
        seen = set(ids)
        for m in minted:
            if m["route_id"] not in seen:
                ids.append(m["route_id"])
                seen.add(m["route_id"])
        allow["ids"] = ids
        save_json(allow_path, allow)

    append_spine(minted)
    append_ledger(minted)
    update_scope()

    report = {"at": utc_now(), "lane": TAG, "minted": minted}
    save_json(REPORT, report)
    print(json.dumps({"minted": len(minted), "new": sum(1 for m in minted if m["status"] == "minted")}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())