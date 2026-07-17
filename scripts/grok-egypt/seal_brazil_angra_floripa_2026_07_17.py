#!/usr/bin/env python3
"""Seal Angra + Floripa provisional corridors → named rn- geometry.

Implements GROK-SPEC-brazil-egypt-tam-2026-07-17.md §1:
  rn-angra-abraao-PROV  → sealed rn- (13.0 nm)
  rn-floripa-r3-PROV    → sealed rn- (4.99 nm)
  rn-floripa-r4-PROV    → sealed rn- (4.79 nm)

Repoint finance model + recal + deck bindings pending_seal → supported.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))

from bolt_yango_routing_shared import (  # noqa: E402
    interior_land_km,
    is_water,
    load_land_mask,
    make_route_feature,
    mint_route_id,
    path_length_km,
    save_json,
    save_routes,
)

DC = ROOT / "data-clean"
FBT_PATH = DC / "FEATURES_BY_TYPE.json"
ROUTES_PATH = DC / "ROUTES.json"
CLUSTERS_PATH = DC / "CLUSTERS.json"
CORR_PATH = ROOT / "finance/model/corridors.json"
NOW = datetime.now(timezone.utc).isoformat()
LAND_GATE_KM = 0.35
NM_PER_KM = 0.539957
TAG = "br-angra-floripa-2026-07-17"

# Boarding points: existing POIs reused where possible; Floripa terminals minted
# on Baía Norte water anchors (government EVTE corridor endpoints; not surveyed berths).
BPS = {
    "bp-angra-estacao-barcas": {
        "name": "Angra dos Reis Terminal (Costa Verde)",
        "shortName": "Angra terminal",
        "bp_type": "ferry_terminal",
        "bp_type_label": "Ferry Terminal",
        "coords": [-44.316171, -23.025],  # water just south of Pier Angra (existing pier landside)
        "facility_coords": [-44.316171, -23.009494],
        "coord_source": "Existing atlas POI Pier Angra Dos Reis bp-dbf5302ce6; boarding anchor nudged water-south into bay",
        "city_id": "angra-dos-reis-ilha-grande-brazil",
        "reuse_poi": "bp-dbf5302ce6",
    },
    "bp-abraao-cais-barcas": {
        "name": "Abraão Terminal (Ilha Grande)",
        "shortName": "Abraão",
        "bp_type": "ferry_terminal",
        "bp_type_label": "Ferry Terminal",
        "coords": [-44.1682984, -23.125],  # water north of Cais das Barcas pier
        "facility_coords": [-44.1682984, -23.1390587],
        "coord_source": "Photon/OSM pier Cais das Barcas Abraão; boarding anchor nudged water-north",
        "city_id": "angra-dos-reis-ilha-grande-brazil",
        "reuse_poi": "bp-2b61ecbd63",
    },
    "bp-barreiros-sj-terminal": {
        "name": "Barreiros Terminal (São José / continent)",
        "shortName": "Barreiros",
        "bp_type": "ferry_terminal",
        "bp_type_label": "Ferry Terminal",
        "coords": [-48.62, -27.54],
        "coord_source": "Baía Norte mainland water anchor west of Miramar (EVTE R3 continent end); not a surveyed berth",
        "city_id": "florianopolis-brazil",
    },
    "bp-miramar-floripa-terminal": {
        "name": "Miramar Terminal (Florianópolis island)",
        "shortName": "Miramar",
        "bp_type": "ferry_terminal",
        "bp_type_label": "Ferry Terminal",
        "coords": [-48.535, -27.565],
        "coord_source": "Baía Norte island-side water anchor (EVTE R3/R4 island end); not a surveyed berth",
        "city_id": "florianopolis-brazil",
    },
    "bp-beira-mar-continent-terminal": {
        "name": "Beira Mar Terminal (continent)",
        "shortName": "Beira Mar continent",
        "bp_type": "ferry_terminal",
        "bp_type_label": "Ferry Terminal",
        "coords": [-48.625, -27.54],
        "coord_source": "Baía Norte mainland water anchor for EVTE R4 continent end; not a surveyed berth",
        "city_id": "florianopolis-brazil",
    },
}

# Hand spines validated: interior_land_km == 0, nm within corridor target band
CORRIDORS = [
    {
        "prov_id": "rn-angra-abraao-PROV",
        "from_bp": "bp-angra-estacao-barcas",
        "to_bp": "bp-abraao-cais-barcas",
        "target_nm": 13.0,
        "city_id": "angra-dos-reis-ilha-grande-brazil",
        "label": "Angra dos Reis Terminal → Abraão Terminal (Ilha Grande)",
        "spine": [
            [-44.316, -23.025],
            [-44.30, -23.05],
            [-44.24, -23.08],
            [-44.18, -23.06],
            [-44.168, -23.125],
        ],
    },
    {
        "prov_id": "rn-floripa-r3-PROV",
        "from_bp": "bp-barreiros-sj-terminal",
        "to_bp": "bp-miramar-floripa-terminal",
        "target_nm": 4.99,
        "city_id": "florianopolis-brazil",
        "label": "Barreiros Terminal → Miramar Terminal",
        "spine": [
            [-48.62, -27.54],
            [-48.5775, -27.5525],
            [-48.535, -27.565],
        ],
    },
    {
        "prov_id": "rn-floripa-r4-PROV",
        "from_bp": "bp-beira-mar-continent-terminal",
        "to_bp": "bp-miramar-floripa-terminal",
        "target_nm": 4.79,
        "city_id": "florianopolis-brazil",
        "label": "Beira Mar Terminal → Miramar Terminal",
        "spine": [
            [-48.625, -27.54],
            [-48.58, -27.5425],
            [-48.535, -27.545],
        ],
    },
]


def densify(coords: list, step_km: float = 0.25) -> list:
    out = [list(coords[0])]
    for i in range(1, len(coords)):
        lon1, lat1 = coords[i - 1]
        lon2, lat2 = coords[i]
        km = (
            ((lon2 - lon1) * 111 * math.cos(math.radians(lat1))) ** 2
            + ((lat2 - lat1) * 111) ** 2
        ) ** 0.5
        n = max(1, int(km / step_km))
        for j in range(1, n + 1):
            t = j / n
            out.append([lon1 + t * (lon2 - lon1), lat1 + t * (lat2 - lat1)])
    return out


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def ensure_bp(fbt: dict, bp_id: str, meta: dict) -> dict:
    pois = fbt.setdefault("poi", [])
    for p in pois:
        props = p.get("properties") or {}
        if props.get("id") == bp_id:
            return p
    # Prefer reusing existing POI id if specified and present
    reuse = meta.get("reuse_poi")
    if reuse:
        for p in pois:
            if (p.get("properties") or {}).get("id") == reuse:
                # clone as named terminal id pointing same coords (or keep reuse)
                return p
    city_id = meta["city_id"]
    # city display
    city_name = city_id
    for c in fbt.get("city") or []:
        if (c.get("properties") or {}).get("id") == city_id:
            city_name = (c.get("properties") or {}).get("name") or city_id
            break
    feat = {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": list(meta["coords"])},
        "properties": {
            "id": bp_id,
            "name": meta["name"],
            "shortName": meta.get("shortName") or meta["name"],
            "kind": "boarding_point",
            "bp_type": meta.get("bp_type") or "ferry_terminal",
            "bp_type_label": meta.get("bp_type_label") or "Ferry Terminal",
            "city_id": city_id,
            "city": city_name,
            "cluster_id": "brazil",
            "country": "Brazil",
            "coord_source": meta.get("coord_source"),
            "_sealed_at": NOW,
            "_seal_lane": TAG,
            "_candidate_note": meta.get("coord_source"),
        },
    }
    if meta.get("facility_coords"):
        feat["properties"]["facility_coords"] = meta["facility_coords"]
    pois.append(feat)
    return feat


def ensure_cluster_membership(clusters: dict, city_id: str, route_ids: list[str]) -> None:
    clist = clusters.get("clusters") or []
    target = None
    for c in clist:
        if c.get("id") == "brazil" or c.get("cluster_id") == "brazil":
            target = c
            break
    if target is None:
        # try find by city
        for c in clist:
            cities = c.get("city_ids") or c.get("cities") or []
            if city_id in cities:
                target = c
                break
    if target is None:
        target = {
            "id": "brazil",
            "name": "Brazil",
            "city_ids": [city_id],
            "route_ids": [],
        }
        clist.append(target)
        clusters["clusters"] = clist
    # add city
    cities = target.setdefault("city_ids", target.get("cities") or [])
    if isinstance(cities, list) and city_id not in cities:
        cities.append(city_id)
    rids = target.setdefault("route_ids", [])
    for rid in route_ids:
        if rid not in rids:
            rids.append(rid)


def main() -> int:
    mask = load_land_mask()
    fbt = load_json(FBT_PATH)
    routes = load_json(ROUTES_PATH)
    clusters = load_json(CLUSTERS_PATH)
    corr = load_json(CORR_PATH)

    # Ensure BPs
    bp_resolved = {}
    for bp_id, meta in BPS.items():
        # Use reuse_poi as the actual from/to when present and exists
        reuse = meta.get("reuse_poi")
        existing = None
        if reuse:
            for p in fbt.get("poi") or []:
                if (p.get("properties") or {}).get("id") == reuse:
                    existing = p
                    break
        if existing:
            # Keep existing id; update seal meta lightly
            props = existing.setdefault("properties", {})
            props.setdefault("_seal_lane", TAG)
            props["_sealed_ref"] = {
                "as": bp_id,
                "at": NOW,
                "name": meta["name"],
            }
            bp_resolved[bp_id] = props["id"]
            # Prefer water boarding coords for routing even if POI is landside
            bp_resolved[bp_id + ":coords"] = meta["coords"]
            bp_resolved[bp_id + ":name"] = meta["name"]
        else:
            ensure_bp(fbt, bp_id, meta)
            bp_resolved[bp_id] = bp_id
            bp_resolved[bp_id + ":coords"] = meta["coords"]
            bp_resolved[bp_id + ":name"] = meta["name"]

    cities = {
        "angra-dos-reis-ilha-grande-brazil": "Angra dos Reis + Ilha Grande (Costa Verde)",
        "florianopolis-brazil": "Florianópolis & Santa Catarina",
    }

    id_map = {}  # prov → sealed
    sealed_features = []
    receipt_routes = []

    existing_ids = {
        (r.get("properties") or {}).get("id")
        for r in routes
        if isinstance(r, dict)
    }

    for c in CORRIDORS:
        from_logical = c["from_bp"]
        to_logical = c["to_bp"]
        from_id = bp_resolved[from_logical]
        to_id = bp_resolved[to_logical]
        from_name = bp_resolved[from_logical + ":name"]
        to_name = bp_resolved[to_logical + ":name"]
        from_coords = bp_resolved[from_logical + ":coords"]
        to_coords = bp_resolved[to_logical + ":coords"]

        # Build path: densify spine, pin endpoints to BP water anchors
        spine = [list(from_coords)] + [list(x) for x in c["spine"][1:-1]] + [list(to_coords)]
        coords = densify(spine, step_km=0.25)
        land = interior_land_km(coords, mask)
        nm = path_length_km(coords) * NM_PER_KM
        if land > LAND_GATE_KM:
            raise SystemExit(f"{c['prov_id']}: land_km {land:.3f} > gate {LAND_GATE_KM}")
        # nm should be near target (within 15%)
        if abs(nm - c["target_nm"]) / c["target_nm"] > 0.20:
            print(f"WARN {c['prov_id']}: path {nm:.2f} nm vs target {c['target_nm']}")

        rid = mint_route_id(from_id, to_id, tag=TAG)
        if rid in existing_ids:
            # already sealed?
            print(f"route {rid} already in ROUTES — reusing")
        feat = make_route_feature(
            from_id,
            to_id,
            from_name,
            to_name,
            c["city_id"],
            c["city_id"],
            coords,
            cities,
            source=TAG,
            land_km=land,
            cluster_id="brazil",
            cluster_city_id=c["city_id"],
        )
        # Force minted id stability and labels
        props = feat["properties"]
        props["id"] = rid
        props["distance_nm"] = round(nm, 2)
        props["label"] = f"{cities[c['city_id']]}: {from_name} → {to_name}"
        props["from_label"] = from_name
        props["to_label"] = to_name
        props["from_city_id"] = c["city_id"]
        props["to_city_id"] = c["city_id"]
        props["_land_km_interior"] = land
        props["_coastal_geometry"] = True
        props["_prov_id"] = c["prov_id"]
        props["_target_nm"] = c["target_nm"]
        props["_sealed_at"] = NOW
        props["_seal_lane"] = TAG
        props["platform"] = "Pioneer II"
        props["edge_class"] = "local"
        props["trip_scope"] = "intra_city"

        # replace if same prov already sealed under different id
        routes = [
            r
            for r in routes
            if (r.get("properties") or {}).get("_prov_id") != c["prov_id"]
            and (r.get("properties") or {}).get("id") != rid
        ]
        routes.append(feat)
        existing_ids.add(rid)
        sealed_features.append(feat)
        id_map[c["prov_id"]] = rid
        receipt_routes.append(
            {
                "prov_id": c["prov_id"],
                "sealed_id": rid,
                "from": from_id,
                "to": to_id,
                "nm": round(nm, 2),
                "target_nm": c["target_nm"],
                "land_km": land,
                "city_id": c["city_id"],
            }
        )
        ensure_cluster_membership(clusters, c["city_id"], [rid])

    # Repoint finance corridors.json
    br = corr["markets"]["brazil"]
    for cor in br["corridors"]:
        old = cor.get("route_id")
        if old in id_map:
            new = id_map[old]
            cor["route_id"] = new
            cor["_prev_prov_id"] = old
            cor["_sealed_at"] = NOW
            # bind boarding points
            for c in CORRIDORS:
                if c["prov_id"] == old:
                    cor["endpoint_boarding_points"] = {
                        "from": bp_resolved[c["from_bp"]],
                        "to": bp_resolved[c["to_bp"]],
                    }
                    cor["distance_nm"] = next(
                        r["nm"] for r in receipt_routes if r["prov_id"] == old
                    )
                    break

    # Write geometry
    write_json(FBT_PATH, fbt)
    save_routes(ROUTES_PATH, routes)
    write_json(CLUSTERS_PATH, clusters)
    write_json(CORR_PATH, corr)

    # Repoint scoped recal corridors
    for path, mkey in [
        (ROOT / "finance/recal/corridors-didi.json", "brazil"),
        (ROOT / "finance/recal/corridors-indrive.json", "indrive-brazil"),
    ]:
        doc = load_json(path)
        m = doc["markets"][mkey]
        for cor in m.get("corridors") or []:
            old = cor.get("route_id")
            if old in id_map:
                cor["route_id"] = id_map[old]
                cor["_prev_prov_id"] = old
                cor["_sealed_at"] = NOW
                for c in CORRIDORS:
                    if c["prov_id"] == old:
                        cor["endpoint_boarding_points"] = {
                            "from": bp_resolved[c["from_bp"]],
                            "to": bp_resolved[c["to_bp"]],
                        }
                        cor["distance_nm"] = next(
                            r["nm"] for r in receipt_routes if r["prov_id"] == old
                        )
        write_json(path, doc)

    # Repoint aggregates
    for path in [
        ROOT / "finance/recal/agg-didi.json",
        ROOT / "finance/recal/agg-indrive.json",
    ]:
        doc = load_json(path)
        for row in doc.get("rows") or []:
            rid = row.get("route_id")
            if rid in id_map:
                new = id_map[rid]
                row["route_id"] = new
                row["_prev_prov_id"] = rid
                for band in ("thin", "mid", "full"):
                    if isinstance(row.get(band), dict) and row[band].get("route_id") == rid:
                        row[band]["route_id"] = new
        write_json(path, doc)

    # Repoint deck bindings: pending_seal → supported
    for deck in ["didi-brazil", "indrive-brazil"]:
        bpath = ROOT / f"deck-studio/decks/{deck}/economics-binding.json"
        b = load_json(bpath)
        ct = b.setdefault("country_total", {})
        supported = list(ct.get("supported_route_ids") or [])
        pending = list(ct.get("pending_seal_route_ids") or [])
        new_pending = []
        for rid in pending:
            if rid in id_map:
                sealed = id_map[rid]
                if sealed not in supported:
                    supported.append(sealed)
            else:
                new_pending.append(rid)
        ct["supported_route_ids"] = supported
        if new_pending:
            ct["pending_seal_route_ids"] = new_pending
        else:
            ct.pop("pending_seal_route_ids", None)
            ct.pop("pending_seal_note", None)
        # economics_routes: add Angra + Floripa representatives if missing
        eroutes = b.get("economics_routes") or []
        have = {e.get("route_id") for e in eroutes}
        extras = [
            {
                "label": "Angra dos Reis → Abraão",
                "route_id": id_map.get("rn-angra-abraao-PROV"),
                "desc": "Costa Verde mainland–Ilha Grande car-free island access.",
            },
            {
                "label": "Barreiros → Miramar",
                "route_id": id_map.get("rn-floripa-r3-PROV"),
                "desc": "Florianópolis North Bay R3 (government pre-viability projection).",
            },
            {
                "label": "Beira Mar → Miramar",
                "route_id": id_map.get("rn-floripa-r4-PROV"),
                "desc": "Florianópolis North Bay R4 (government pre-viability projection).",
            },
        ]
        for e in extras:
            if e["route_id"] and e["route_id"] not in have:
                eroutes.append(e)
        b["economics_routes"] = eroutes
        write_json(bpath, b)

    receipt = {
        "at": NOW,
        "lane": TAG,
        "id_map": id_map,
        "routes": receipt_routes,
        "bp_resolved": {k: v for k, v in bp_resolved.items() if not k.endswith(":coords") and not k.endswith(":name")},
        "land_gate_km": LAND_GATE_KM,
        "spec": "handoff/finance/GROK-SPEC-brazil-egypt-tam-2026-07-17.md",
    }
    out = (
        ROOT
        / "handoff/partner-map-model/brazil-tam-2026-07-17"
        / "BRAZIL-ANGRA-FLORIPA-SEAL-RECEIPT-2026-07-17.json"
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    write_json(out, receipt)
    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
