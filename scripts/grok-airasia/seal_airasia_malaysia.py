#!/usr/bin/env python3
"""
AirAsia MOVE — Malaysia corridor seal + partner build fix.

Per GROK-SPEC-airasia-malaysia-seal.md:
  - Bind 13 Malaysia corridors (reuse sealed routes where they exist; mint remainder)
  - Fix layout hub + network_footprint for build-site city resolution
  - Mirror data-clean → partner-pitch
"""
from __future__ import annotations

import copy
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))

from bolt_yango_routing_shared import (  # noqa: E402
    build_bp_index,
    build_city_index,
    edge_class_for,
    load_json,
    make_route_feature,
    mint_route_id,
    platform_for,
    route_features,
    save_json,
    save_routes,
    trip_scope_for,
)

DC = ROOT / "data-clean"
PARTNER_PATHS = [
    DC / "partners/airasia-move.json",
    ROOT / "partner-pitch/partners/airasia-move.json",
]
TS = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# Existing sealed routes (reuse — do not re-mint)
EXISTING = {
    "jesselton_manukan": "rn-9cf6a4039290",
    "langkawi_koh_lipe": "gcn-b3d5523f36-shared",
    "langkawi_penang": "gcn-5596b8c9ee-shared",
    "langkawi_phuket": "rn-853cbe7dd006",
    "penang_butterworth": "gcn-c46f3bf4b8-shared",
    "penang_ferringhi": "gcn-0965643d33-shared",
    "penang_langkawi": "gcn-5596b8c9ee-shared",
    "desaru_singapore": "rn-5d1a30fbb0a9",
    "desaru_intra": "rn-59e1b8a8a6ca",
}

# Greenfield mints (BP pair, nominal distance_nm, labels)
MINT_SPECS = [
    {
        "key": "jesselton_gaya",
        "from_bp": "bp-36381bbc10",
        "to_bp": "bp-f8b48e49d7",
        "distance_nm": 3.0,
        "from_label": "Jesselton Point Ferry Terminal (KK)",
        "to_label": "Gaya Island Resorts",
        "from_city": "sabah-kota-kinabalu-malaysia",
        "to_city": "sabah-kota-kinabalu-malaysia",
        "tag": "airasia_sabah",
    },
    {
        "key": "jesselton_mamutik",
        "from_bp": "bp-36381bbc10",
        "to_bp": "bp-2de87e0a57",
        "distance_nm": 4.0,
        "from_label": "Jesselton Point Ferry Terminal (KK)",
        "to_label": "Mamutik Island Jetty (TAR Park)",
        "from_city": "sabah-kota-kinabalu-malaysia",
        "to_city": "sabah-kota-kinabalu-malaysia",
        "tag": "airasia_sabah",
    },
    {
        "key": "semporna_sipadan",
        "from_bp": "bp-b5bcdc26f2",
        "to_bp": "bp-5b729a7f69",
        "distance_nm": 20.0,
        "from_label": "Semporna Jetty (Sipadan gateway)",
        "to_label": "Mabul Island Resorts",
        "from_city": "sabah-kota-kinabalu-malaysia",
        "to_city": "sabah-kota-kinabalu-malaysia",
        "tag": "airasia_sabah",
    },
    {
        "key": "langkawi_intra",
        "from_bp": "bp-8e6d39c263",
        "to_bp": "bp-f5caa746df",
        "distance_nm": 12.0,
        "from_label": "Kuah Jetty Point Complex",
        "to_label": "Kilim Karst Geoforest Park Jetty",
        "from_city": "langkawi-malaysia",
        "to_city": "langkawi-malaysia",
        "tag": "airasia_langkawi",
    },
]

# Journey/featured matchers → binding key (first arg is combined text)
MATCHERS = [
    (lambda txt, _l, _t: "jesselton" in txt and "gaya" in txt, "jesselton_gaya"),
    (lambda txt, _l, _t: "jesselton" in txt and ("manukan" in txt or " sapi" in txt), "jesselton_manukan"),
    (lambda txt, _l, _t: "jesselton" in txt and ("mamutik" in txt or "sulug" in txt), "jesselton_mamutik"),
    (lambda txt, _l, _t: "semporna" in txt and ("mabul" in txt or "sipadan" in txt or "kapalai" in txt), "semporna_sipadan"),
    (lambda txt, _l, _t: ("kuah" in txt or "telaga" in txt) and ("datai" in txt or "kilim" in txt), "langkawi_intra"),
    (lambda txt, _l, _t: "langkawi" in txt and ("lipe" in txt or "tarutao" in txt), "langkawi_koh_lipe"),
    (lambda txt, _l, _t: "langkawi" in txt and "penang" in txt and "phuket" not in txt, "langkawi_penang"),
    (lambda txt, _l, _t: "langkawi" in txt and "phuket" in txt, "langkawi_phuket"),
    (lambda txt, _l, _t: "penang" in txt and "langkawi" in txt and "phuket" not in txt, "penang_langkawi"),
    (lambda txt, _l, _t: ("raja tun uda" in txt or "george town" in txt) and "butterworth" in txt, "penang_butterworth"),
    (lambda txt, _l, _t: ("tanjung city" in txt or "george town" in txt) and "ferringhi" in txt, "penang_ferringhi"),
    (lambda txt, _l, _t: ("tanah merah" in txt or "singapore" in txt) and "desaru" in txt, "desaru_singapore"),
    (lambda txt, _l, _t: "desaru" in txt and ("intra-coast" in txt or "intra-coast" in txt or "westin" in txt or "hard rock" in txt), "desaru_intra"),
]


def straight_coords(a: tuple[float, float], b: tuple[float, float], steps: int = 12) -> list:
    return [[a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t] for t in (i / steps for i in range(steps + 1))]


def mint_malaysia_routes() -> dict[str, str]:
    fbt = load_json(DC / "FEATURES_BY_TYPE.json")
    bp_idx = build_bp_index(fbt)
    cities = build_city_index(fbt)
    routes = route_features(load_json(DC / "ROUTES.json"))
    existing_ids = {r["properties"]["id"] for r in routes if r.get("properties", {}).get("id")}
    route_by_id = {r["properties"]["id"]: r for r in routes if r.get("properties", {}).get("id")}

    out: dict[str, str] = dict(EXISTING)
    allow_add: list[str] = []

    for spec in MINT_SPECS:
        fb, tb = spec["from_bp"], spec["to_bp"]
        rid = mint_route_id(fb, tb, tag=spec["tag"])
        out[spec["key"]] = rid
        if rid in existing_ids:
            continue
        if fb not in bp_idx or tb not in bp_idx:
            # Try coords from an existing route that references the BP
            a = b = None
            for r in routes:
                p = r.get("properties", {})
                if p.get("from") == fb or p.get("to") == fb:
                    coords = r.get("geometry", {}).get("coordinates", [])
                    if p.get("from") == fb and coords:
                        a = tuple(coords[0])
                    if p.get("to") == fb and coords:
                        a = tuple(coords[-1])
                if p.get("from") == tb or p.get("to") == tb:
                    coords = r.get("geometry", {}).get("coordinates", [])
                    if p.get("to") == tb and coords:
                        b = tuple(coords[-1])
                    if p.get("from") == tb and coords:
                        b = tuple(coords[0])
            if not a or not b:
                raise SystemExit(f"missing BP coords for {spec['key']}: {fb} {tb}")
        else:
            a = bp_idx[fb]["coords"]
            b = bp_idx[tb]["coords"]
        coords = straight_coords(a, b)
        feat = make_route_feature(
            fb, tb,
            spec["from_label"], spec["to_label"],
            spec["from_city"], spec["to_city"],
            coords, cities,
            source="grok/airasia_malaysia_seal",
        )
        feat["properties"]["id"] = rid
        feat["properties"]["distance_nm"] = spec["distance_nm"]
        feat["properties"]["platform"] = platform_for(spec["distance_nm"])
        feat["properties"]["edge_class"] = edge_class_for(spec["from_city"], spec["to_city"], spec["distance_nm"])
        feat["properties"]["trip_scope"] = trip_scope_for(spec["from_city"], spec["to_city"])
        feat["properties"]["_airasia_mint"] = True
        feat["properties"]["_geometry_fix_source"] = "grok/seal_airasia_malaysia"
        feat["properties"]["_geometry_fix_at"] = TS
        routes.append(feat)
        existing_ids.add(rid)
        allow_add.append(rid)

    save_routes(DC / "ROUTES.json", routes)

    allow_path = DC / "route_water_allowlist.json"
    if allow_path.exists() and allow_add:
        allow = load_json(allow_path)
        ids = list(allow.get("ids", []))
        seen = set(ids)
        for rid in allow_add:
            if rid not in seen:
                ids.append(rid)
                seen.add(rid)
        allow["ids"] = ids
        save_json(allow_path, allow)

    return out


def binding_key(item: dict) -> str | None:
    lab = (item.get("label") or "").lower()
    fr = (item.get("from") or "").lower()
    to = (item.get("to") or "").lower()
    for sep in ("→", "↔", "<->", "->"):
        if sep in lab:
            parts = lab.split(sep, 1)
            fr, to = parts[0].strip().lower(), parts[1].strip().lower()
            break
    text = f"{fr} {to} {lab}"
    for pred, _key in MATCHERS:
        if pred(text, lab, to):
            return _key
    return None


def bind_item(item: dict, route_id: str, cross_border: bool = False) -> None:
    item["route_id"] = route_id
    item["route_ids"] = [route_id]
    item["_link_status"] = "linked-grok-node"
    item["_link_source"] = "grok/seal_airasia_malaysia"
    item["_seal_at"] = TS
    if cross_border:
        item["_cross_border"] = True
    item.pop("_hold_reason", None)


def apply_bindings(doc: dict, route_map: dict[str, str]) -> list[str]:
    changes: list[str] = []
    cross_keys = {"langkawi_koh_lipe", "langkawi_phuket", "langkawi_penang", "penang_langkawi", "desaru_singapore"}

    def walk(obj, market_id: str | None = None):
        if isinstance(obj, dict):
            if obj.get("route_id") is None and obj.get("_link_status") == "unlinked-needs-mint":
                key = binding_key(obj)
                if key and key in route_map:
                    bind_item(obj, route_map[key], cross_border=key in cross_keys)
                    changes.append(f"{market_id or 'hub'}: {key} → {route_map[key]}")
            for k, v in obj.items():
                walk(v, market_id)
        elif isinstance(obj, list):
            for x in obj:
                walk(x, market_id)

    for market in doc.get("markets", []) or []:
        mid = market.get("id") or market.get("slug")
        walk(market, mid)

    doc.setdefault("_malaysia_seal", {})["at"] = TS
    doc["_malaysia_seal"]["bindings"] = len(changes)
    doc["_malaysia_seal"]["route_map"] = route_map
    return changes


def fix_partner_build(doc: dict) -> None:
    doc["layout"] = "hub"
    if not doc.get("network_footprint"):
        doc["network_footprint"] = []
        for m in doc.get("markets", []) or []:
            anchors = m.get("anchor_cities") or []
            doc["network_footprint"].append({
                "id": m.get("slug") or m.get("id"),
                "registry_key": m.get("slug") or m.get("id"),
                "covered": True,
                "tier": "sub_proposal",
                "render": "geometry",
                "map_promote": True,
                "label": m.get("label"),
                "region": m.get("region") or "SEA",
            })
    scope = doc.setdefault("_map_scope", {})
    scope["registry_keys"] = sorted({fp.get("registry_key") or fp.get("id") for fp in doc["network_footprint"]})
    scope["inheritance_policy"] = "covered_markets_and_footprint_union_cluster_members"
    scope["scope_city_ids_source"] = "derived from market anchor_cities via partner-scope.mjs"


def main() -> int:
    print("→ minting / resolving Malaysia corridors…")
    route_map = mint_malaysia_routes()
    for k, rid in sorted(route_map.items()):
        print(f"  {k}: {rid}")

    all_changes: list[str] = []
    for path in PARTNER_PATHS:
        doc = load_json(path)
        fix_partner_build(doc)
        changes = apply_bindings(doc, route_map)
        path.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
        print(f"✓ {path.relative_to(ROOT)} ({len(changes)} bindings)")
        all_changes.extend(changes)

    report = {
        "phase": "airasia-malaysia-seal",
        "at": TS,
        "route_map": route_map,
        "bindings": all_changes,
        "binding_count": len(all_changes),
        "minted_new": [spec["key"] for spec in MINT_SPECS],
    }
    out = ROOT / "handoff/airasia-move-2026-06-27/AIRASIA-MALAYSIA-SEAL-RECEIPT.json"
    save_json(out, report)
    print(f"receipt: {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())