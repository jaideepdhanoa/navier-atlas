#!/usr/bin/env python3
"""
AirAsia MOVE — Philippines corridor seal (Phase 2).

Per handoff/GROK-SPEC-airasia-phase2-seal.md:
  - Bind 18 Philippines corridors (reuse sealed routes where they exist; mint remainder)
  - Flip PH network_footprint render label → geometry
  - Mirror data-clean → partner-pitch
  - Add _philippines_seal block (economics stay model-pass-pending)
"""
from __future__ import annotations

import json
import math
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

PH_SLUGS = frozenset({"manila", "cebu", "boracay", "palawan", "siargao"})

# Registry routes — reuse, do not re-mint
EXISTING: dict[str, str] = {
    "manila_corregidor": "rn-30120bc0105a",
    "manila_nasugbu": "rn-e9ddb844af0a",
    "manila_bataan": "rn-6193fc15dcee",
    "cebu_bohol": "rn-66e9451f405f",
    "cebu_mactan_resorts": "rn-4f6e8fe32136",
    "bor_caticlan": "rn-95cb8fe771c3",
    "bor_station1": "rn-1a4e733333cd",
    "bor_carabao": "rn-609ddbca5a68",
    "sia_sohoton": "ics-2193fd3739",
    "sia_naked": "rn-c13d8e22a145",
}

# Synthetic / greenfield mints
MINT_SPECS = [
    {
        "key": "manila_subic",
        "from_bp": "bp-2817a86d83",
        "to_bp": "bp-c09cbfe85f",
        "distance_nm": 44.0,
        "from_label": "Esplanade Seaside Terminal (Manila South Harbor)",
        "to_label": "Port Of Subic Bay",
        "from_city": "manila-philippines",
        "to_city": "manila-philippines",
        "display_city": "Manila",
        "tag": "airasia_manila",
    },
    {
        "key": "cebu_camotes",
        "from_bp": "bp-644376be1d",
        "to_bp": "bp-06ab57b702",
        "distance_nm": 28.0,
        "from_label": "Cebu-Mactan Ferry Terminal",
        "to_label": "Camotes Consuelo Wharf",
        "from_city": "cebu-philippines",
        "to_city": "cebu-philippines",
        "display_city": "Cebu",
        "tag": "airasia_cebu",
    },
    {
        "key": "cebu_malapascua",
        "from_bp": "bp-644376be1d",
        "to_bp": "bp-airasia-malapascua-logon",
        "distance_nm": 34.0,
        "from_label": "Cebu-Mactan Ferry Terminal",
        "to_label": "Malapascua Island (Logon Beach landing)",
        "from_city": "cebu-philippines",
        "to_city": "cebu-philippines",
        "display_city": "Cebu",
        "tag": "airasia_cebu",
        "to_coords": (124.117, 11.333),
    },
    {
        "key": "pal_honda",
        "from_bp": "bp-2f28142179",
        "to_bp": "bp-72e6d87c8a",
        "distance_nm": 8.0,
        "from_label": "Honda Bay Boat Terminal (Sta. Lourdes)",
        "to_label": "Luli Island Wharf (Honda Bay)",
        "from_city": "palawan-philippines",
        "to_city": "palawan-philippines",
        "display_city": "Palawan",
        "tag": "airasia_palawan",
    },
    {
        "key": "pal_bacuit",
        "from_bp": "bp-aa63fff1b4",
        "to_bp": "bp-6a775eb33c",
        "distance_nm": 10.0,
        "from_label": "El Nido Town / Corong-Corong bangka landings",
        "to_label": "Miniloc Island Resort jetty (Bacuit Bay)",
        "from_city": "palawan-philippines",
        "to_city": "palawan-philippines",
        "display_city": "Palawan",
        "tag": "airasia_palawan",
    },
    {
        "key": "pal_coron",
        "from_bp": "bp-f6a85e10f9",
        "to_bp": "bp-8d441a16a5",
        "distance_nm": 12.0,
        "from_label": "Coron Town Pier (Coron Port)",
        "to_label": "Busuanga Bay Lodge jetty (Coron Bay)",
        "from_city": "palawan-philippines",
        "to_city": "palawan-philippines",
        "display_city": "Palawan",
        "tag": "airasia_palawan",
    },
    {
        "key": "pal_pp_elnido",
        "from_bp": "bp-2148e0bc5c",
        "to_bp": "bp-755c28bf38",
        "distance_nm": 125.0,
        "from_label": "Puerto Princesa Port",
        "to_label": "El Nido Ferry Terminal",
        "from_city": "palawan-philippines",
        "to_city": "palawan-philippines",
        "display_city": "Palawan",
        "tag": "airasia_palawan_lr",
        "roadmap": True,
    },
    {
        "key": "sia_dinagat",
        "from_bp": "bp-4dbd5a9ec0",
        "to_bp": "bp-airasia-dinagat-sanjose",
        "distance_nm": 24.0,
        "from_label": "Dapa Port (Siargao)",
        "to_label": "Dinagat Islands (San Jose Port)",
        "from_city": "siargao-philippines",
        "to_city": "siargao-philippines",
        "display_city": "Siargao",
        "tag": "airasia_siargao",
        "to_coords": (125.594, 10.128),
    },
]

MATCHERS: list[tuple] = [
    (lambda t, _l, _to: "corregidor" in t, "manila_corregidor"),
    (lambda t, _l, _to: ("nasugbu" in t or "pico de loro" in t or "anvaya" in t or "hamilo" in t or "calatagan" in t), "manila_nasugbu"),
    (lambda t, _l, _to: "subic" in t, "manila_subic"),
    (lambda t, _l, _to: ("bataan" in t or "las casas" in t or "mariveles" in t) and "camaya" not in t, "manila_bataan"),
    (lambda t, _l, _to: ("bohol" in t or "tagbilaran" in t or "panglao" in t), "cebu_bohol"),
    (lambda t, _l, _to: "mactan" in t and ("resort" in t or "shangri" in t or "mövenpick" in t or "movenpick" in t), "cebu_mactan_resorts"),
    (lambda t, _l, _to: "camotes" in t, "cebu_camotes"),
    (lambda t, _l, _to: "malapascua" in t or "bantayan" in t, "cebu_malapascua"),
    (lambda t, _l, _to: "caticlan" in t and ("cagban" in t or "boracay island" in t), "bor_caticlan"),
    (lambda t, _l, _to: ("station 1" in t or "discovery shores" in t or "henann" in t) and "boracay" in t, "bor_station1"),
    (lambda t, _l, _to: "carabao" in t, "bor_carabao"),
    (lambda t, _l, _to: "honda" in t, "pal_honda"),
    (lambda t, _l, _to: ("bacuit" in t or "miniloc" in t) and "el nido" in t, "pal_bacuit"),
    (lambda t, _l, _to: "coron" in t and ("busuanga" in t or "bay" in t), "pal_coron"),
    (lambda t, _l, _to: "puerto princesa" in t and "el nido" in t, "pal_pp_elnido"),
    (lambda t, _l, _to: "sohoton" in t or "bucas grande" in t, "sia_sohoton"),
    (lambda t, _l, _to: "naked" in t or "daku" in t or "guyam" in t, "sia_naked"),
    (lambda t, _l, _to: "dinagat" in t or ("dapa" in t and "dinagat" in t), "sia_dinagat"),
]

ROADMAP_KEYS = frozenset({"pal_pp_elnido"})


def straight_coords(a: tuple[float, float], b: tuple[float, float], steps: int = 12) -> list:
    return [[a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t] for t in (i / steps for i in range(steps + 1))]


def bp_coords(bp_idx: dict, bp_id: str, routes: list, fallback: tuple[float, float] | None = None) -> tuple[float, float]:
    if bp_id in bp_idx:
        return bp_idx[bp_id]["coords"]
    for r in routes:
        p = r.get("properties", {})
        coords = r.get("geometry", {}).get("coordinates", [])
        if not coords:
            continue
        if p.get("from") == bp_id:
            return tuple(coords[0])
        if p.get("to") == bp_id:
            return tuple(coords[-1])
    if fallback:
        return fallback
    raise SystemExit(f"missing BP coords: {bp_id}")


def mint_philippines_routes() -> dict[str, str]:
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
        if spec["key"] in EXISTING and EXISTING[spec["key"]] in existing_ids:
            out[spec["key"]] = EXISTING[spec["key"]]
            continue

        to_fallback = spec.get("to_coords")
        a = bp_coords(bp_idx, fb, routes)
        b = bp_coords(bp_idx, tb, routes, fallback=to_fallback)
        coords = straight_coords(a, b)
        dc = spec.get("display_city", "Manila")
        feat = make_route_feature(
            fb,
            tb,
            spec["from_label"],
            spec["to_label"],
            spec["from_city"],
            spec["to_city"],
            coords,
            cities,
            source="grok/airasia_philippines_seal",
        )
        feat["properties"]["id"] = rid
        feat["properties"]["distance_nm"] = spec["distance_nm"]
        feat["properties"]["platform"] = platform_for(spec["distance_nm"])
        feat["properties"]["edge_class"] = edge_class_for(spec["from_city"], spec["to_city"], spec["distance_nm"])
        feat["properties"]["trip_scope"] = trip_scope_for(spec["from_city"], spec["to_city"])
        feat["properties"]["from_city"] = dc
        feat["properties"]["to_city"] = dc
        feat["properties"]["from_city_id"] = spec["from_city"]
        feat["properties"]["to_city_id"] = spec["to_city"]
        feat["properties"]["_airasia_mint"] = True
        feat["properties"]["_geometry_fix_source"] = "grok/seal_airasia_philippines"
        feat["properties"]["_geometry_fix_at"] = TS
        if spec.get("roadmap"):
            feat["properties"]["_roadmap"] = True
            feat["properties"]["_quanta_lr_roadmap"] = True
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
    for sep in ("→", "↔", "<->", "->", "<-"):
        if sep in lab:
            parts = lab.split(sep, 1)
            fr, to = parts[0].strip().lower(), parts[1].strip().lower()
            break
    text = f"{fr} {to} {lab}"
    for pred, key in MATCHERS:
        if pred(text, lab, to):
            return key
    return None


def bind_item(item: dict, route_id: str, *, roadmap: bool = False) -> None:
    item["route_id"] = route_id
    item["route_ids"] = [route_id]
    item["_link_status"] = "linked-grok-node"
    item["_link_source"] = "grok/seal_airasia_philippines"
    item["_seal_at"] = TS
    if roadmap:
        item["_roadmap"] = True
        item["_quanta_lr_roadmap"] = True
    item.pop("_hold_reason", None)


def apply_bindings(doc: dict, route_map: dict[str, str]) -> list[str]:
    changes: list[str] = []
    seen_per_market: dict[str, set[str]] = {}

    def walk(obj, market_id: str | None = None):
        if isinstance(obj, dict):
            if obj.get("route_id") is None and obj.get("_link_status") == "unlinked-needs-mint":
                key = binding_key(obj)
                if key and key in route_map:
                    bind_item(obj, route_map[key], roadmap=key in ROADMAP_KEYS)
                    changes.append(f"{market_id or 'hub'}: {key} → {route_map[key]}")
            for k, v in obj.items():
                walk(v, market_id)
        elif isinstance(obj, list):
            for x in obj:
                walk(x, market_id)

    for market in doc.get("markets", []) or []:
        mid = market.get("id") or market.get("slug")
        walk(market, mid)

    doc.setdefault("_philippines_seal", {})["at"] = TS
    doc["_philippines_seal"]["bindings"] = len(changes)
    doc["_philippines_seal"]["route_map"] = route_map
    doc["_philippines_seal"]["economics"] = "model-pass-pending"
    return changes


def fix_footprint_flags(doc: dict) -> None:
    for fp in doc.get("network_footprint", []) or []:
        if fp.get("id") in PH_SLUGS:
            fp["render"] = "geometry"
            fp.pop("_seal_status", None)


def ensure_manila_city_node() -> bool:
    """manila-philippines lives in priority_city only — promote to city[] for map resolution."""
    path = DC / "FEATURES_BY_TYPE.json"
    fbt = load_json(path)
    city_ids = {f.get("properties", {}).get("id") for f in fbt.get("city", [])}
    if "manila-philippines" in city_ids:
        return False
    src = None
    for feat in fbt.get("priority_city", []) or []:
        if feat.get("properties", {}).get("id") == "manila-philippines":
            src = feat
            break
    if not src:
        return False
    node = json.loads(json.dumps(src))
    props = node.setdefault("properties", {})
    props["name"] = "Manila"
    props["shortName"] = "Manila"
    props["fullName"] = "Manila & the Bay"
    props["country"] = "Philippines"
    props["region"] = "SEA"
    props["type"] = "city"
    props["_airasia_ph_promote"] = True
    props["_promoted_at"] = TS
    fbt.setdefault("city", []).append(node)
    save_json(path, fbt)
    pitch = ROOT / "partner-pitch/FEATURES_BY_TYPE.json"
    if pitch.exists():
        save_json(pitch, fbt)
    return True


def main() -> int:
    promoted = ensure_manila_city_node()
    if promoted:
        print("✓ promoted manila-philippines → city[]")

    print("→ minting / resolving Philippines corridors…")
    route_map = mint_philippines_routes()
    for k, rid in sorted(route_map.items()):
        print(f"  {k}: {rid}")

    all_changes: list[str] = []
    for path in PARTNER_PATHS:
        doc = load_json(path)
        changes = apply_bindings(doc, route_map)
        fix_footprint_flags(doc)
        path.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
        print(f"✓ {path.relative_to(ROOT)} ({len(changes)} bindings)")
        all_changes.extend(changes)

    report = {
        "phase": "airasia-philippines-seal",
        "at": TS,
        "route_map": route_map,
        "bindings": all_changes,
        "binding_count": len(all_changes),
        "unique_corridors": len(route_map),
        "minted_new": [spec["key"] for spec in MINT_SPECS],
        "reused_existing": list(EXISTING.keys()),
        "held": {
            "economics": "model-pass-pending",
            "roadmap": list(ROADMAP_KEYS),
            "singapore_tioman": "ics-1a53f8237d",
        },
        "manila_city_promoted": promoted,
    }
    out = ROOT / "handoff/airasia-move-2026-06-27/AIRASIA-PHILIPPINES-SEAL-RECEIPT.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    save_json(out, report)
    print(f"receipt: {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())