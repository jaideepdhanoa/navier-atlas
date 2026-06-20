#!/usr/bin/env python3
"""Mint e__ corridor routes from CORRIDOR-ENDPOINT-GROUNDING build_targets + POI scan fixes.

Covers P1 (Kaohsiung↔Cijin, Soneva Kiri hop), P2 (19 build_targets), P3 (Taiwan/Koh Kood POIs).
Routes are visible (no quarantine) and added to route_water_allowlist.
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))

from bolt_yango_routing_shared import (  # noqa: E402
    build_bp_index,
    build_city_index,
    build_coastal_path,
    city_display,
    edge_class_for,
    interior_land_km,
    load_json,
    load_land_mask,
    platform_for,
    route_features,
    save_json,
    save_routes,
    trip_scope_for,
)

DC = ROOT / "data-clean"
GROUNDING_PATH = DC / "CORRIDOR-ENDPOINT-GROUNDING.json"

# P1 + P3 priority corridors (resolved after POI scan)
PRIORITY_CORRIDORS = [
    {
        "market": "taiwan",
        "corridor": "Kaohsiung harbour (Gushan) -> Cijin Island",
        "from_node": "bp-78479cbbc5",
        "to_node": "bp-b5c6de26ca",
        "from_label": "Gushan Ferry Pier (Cijin route — mainland side)",
        "to_label": "Cijin Ferry Pier (Cijin Island side)",
        "from_city_id": "kaohsiung-taiwan",
        "to_city_id": "kaohsiung-taiwan",
        "distance_nm": 2.0,
        "tag": "kaohsiung-taiwan",
    },
    {
        "market": "taiwan",
        "corridor": "Donggang (Pingtung) -> Xiaoliuqiu (Liuqiu Island)",
        "from_node": "bp-67975e4eb0",
        "to_node": "bp-1016bdecea",
        "from_label": "Donggang Ferry Wharf (to Xiaoliuqiu / Lambai)",
        "to_label": "Baisha Tourist Harbor (Xiaoliuqiu / Lambai Island)",
        "from_city_id": "kaohsiung-taiwan",
        "to_city_id": "kaohsiung-taiwan",
        "distance_nm": 8.0,
        "tag": "kaohsiung-taiwan",
    },
    {
        "market": "thailand-soneva",
        "corridor": "Koh Mai Si airstrip -> Soneva Kiri (Koh Kood)",
        "from_node": "bp-koh-mai-si-airstrip",
        "to_node": "bp-d5427b5e8b",
        "from_label": "Koh Mai Si airstrip (Soneva Kiri)",
        "to_label": "Soneva Kiri (Koh Kood) — resort jetty",
        "from_city_id": "koh-rong-cambodia",
        "to_city_id": "koh-rong-cambodia",
        "distance_nm": 8.0,
        "tag": "kood",
    },
]

# Maldives JIH build_targets → already-promoted e__velana legs (skip re-mint)
VELANA_BY_RESORT = {
    "kurumba": "e__velana__kurumba-jetty",
    "gili lankanfushi": "e__velana__gili-lankanfushi-jetty",
    "baros": "e__velana__baros-jetty",
    "constance halaveli": "e__velana__constance-halaveli-jetty",
    "conrad": "e__velana__conrad-rangali-jetty",
    "waldorf astoria": "e__velana__waldorf-ithaafushi-jetty",
    "one&only reethi": "e__velana__oneonly-reethi-rah-jetty",
    "ritz-carlton": "e__velana__ritz-fari-jetty",
    "patina": "e__velana__patina-fari-jetty",
    "westin": "e__velana__westin-miriandhoo-jetty",
}

KOHH_MAI_SI_POI = {
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [102.318611, 10.021389]},
    "properties": {
        "id": "bp-koh-mai-si-airstrip",
        "type": "poi",
        "bp_type": "airstrip_jetty",
        "bp_type_label": "Private airstrip + speedboat pier",
        "confidence": "high",
        "fullName": "Koh Mai Si airstrip (Soneva Kiri)",
        "name": "Koh Mai Si airstrip (Soneva Kiri)",
        "shortName": "Koh Mai Si airstrip",
        "parent_city_id": "koh-rong-cambodia",
        "region": "SEA",
        "status": "operational",
        "source_url": "https://soneva.com/resorts/soneva-kiri/",
        "_poi_scan": "koh-kood-2026-06",
    },
}

SONEVA_LOCALE = {
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [102.527674, 11.69425]},
    "properties": {
        "id": "cambodia__koh-rong-krabey-koh-kood-thailand-soneva-kiri",
        "type": "locale",
        "name": "Koh Kood — Soneva Kiri resort cluster",
        "shortName": "Soneva Kiri (Koh Kood)",
        "parent_city_id": "koh-rong-cambodia",
        "confidence": "high",
        "status": "operational",
        "_poi_scan": "koh-kood-2026-06",
    },
}


def e_route_id(tag: str, from_id: str, to_id: str) -> str:
    seed = f"{from_id}|{to_id}"
    h = hashlib.md5(seed.encode()).hexdigest()[:12]
    return f"e__{tag}__{h}"


def city_coords(fbt: dict, city_id: str) -> tuple[float, float] | None:
    for key in ("city", "priority_city"):
        for feat in fbt.get(key, []):
            p = feat.get("properties") or {}
            if p.get("id") == city_id:
                c = feat.get("geometry", {}).get("coordinates")
                if c and len(c) >= 2:
                    return (c[0], c[1])
    return None


def resolve_coords(node_id: str, bp_idx: dict, fbt: dict) -> tuple[float, float] | None:
    if node_id in bp_idx:
        return bp_idx[node_id]["coords"]
    cc = city_coords(fbt, node_id)
    if cc:
        return cc
    return None


def make_e_feature(
    row: dict,
    coords: list,
    cities: dict[str, str],
    *,
    land_km: float = 0.0,
) -> dict:
    from_id = row["from_node"]
    to_id = row["to_node"]
    from_city = row.get("from_city_id")
    to_city = row.get("to_city_id")
    from_name = row.get("from_label") or from_id
    to_name = row.get("to_label") or to_id
    tag = row.get("tag") or row.get("market", "corr").replace("-", "_")[:20]
    rid = e_route_id(tag, from_id, to_id)

    dist_km = 0.0
    for i in range(1, len(coords)):
        from bolt_yango_routing_shared import hav_km

        dist_km += hav_km(
            (coords[i - 1][0], coords[i - 1][1]),
            (coords[i][0], coords[i][1]),
        )
    dist_nm = round(dist_km / 1.852, 1)
    if row.get("distance_nm"):
        dist_nm = float(row["distance_nm"])

    fc = city_display(from_city, cities)
    tc = city_display(to_city, cities)
    label = f"{from_name} → {to_name}"

    return {
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": coords},
        "properties": {
            "id": rid,
            "platform": platform_for(dist_nm),
            "distance_nm": dist_nm,
            "edge_class": edge_class_for(from_city, to_city, dist_nm),
            "from": from_id,
            "to": to_id,
            "from_node": from_id,
            "to_node": to_id,
            "from_label": from_name,
            "to_label": to_name,
            "from_city": fc,
            "to_city": tc,
            "from_city_id": from_city,
            "to_city_id": to_city,
            "label": label,
            "trip_scope": trip_scope_for(from_city, to_city),
            "traffic_weight": 0.45,
            "_corridor_mint": True,
            "_corridor_market": row.get("market"),
            "_land_km_interior": round(land_km, 4),
            "_coastal_geometry": True,
        },
    }


def apply_poi_scan(fbt: dict) -> list[str]:
    """P3: fix parent_city_id, add Koh Mai Si POI + Soneva locale."""
    changes: list[str] = []
    poi_list = fbt.setdefault("poi", [])
    locale_list = fbt.setdefault("locale", [])

    by_id = {f["properties"]["id"]: f for f in poi_list if f.get("properties", {}).get("id")}

    if "bp-koh-mai-si-airstrip" not in by_id:
        poi_list.append(KOHH_MAI_SI_POI)
        changes.append("added bp-koh-mai-si-airstrip")

    for pid in ("bp-d5427b5e8b", "bp-7c6116d860"):
        if pid in by_id:
            p = by_id[pid]["properties"]
            if p.get("parent_city_id") != "koh-rong-cambodia":
                p["parent_city_id"] = "koh-rong-cambodia"
                changes.append(f"parent_city_id→koh-rong-cambodia for {pid}")

    locale_ids = {f["properties"]["id"] for f in locale_list if f.get("properties", {}).get("id")}
    if SONEVA_LOCALE["properties"]["id"] not in locale_ids:
        locale_list.append(SONEVA_LOCALE)
        changes.append("added locale cambodia__koh-rong-krabey-koh-kood-thailand-soneva-kiri")

    return changes


def build_target_rows(grounding: dict) -> list[dict]:
    rows: list[dict] = []
    seen: set[tuple[str, str]] = set()

    def add(row: dict):
        key = (row["from_node"], row["to_node"])
        if key in seen or not row.get("from_node") or not row.get("to_node"):
            return
        seen.add(key)
        rows.append(row)

    for spec in PRIORITY_CORRIDORS:
        add(spec)

    for bt in grounding.get("build_targets") or []:
        fn, tn = bt.get("from_node"), bt.get("to_node")
        if not fn or not tn:
            continue
        market = bt.get("market", "corr")
        tag = market.split("-")[0] if market else "corr"
        if market.startswith("maldives"):
            to_txt = (bt.get("to_text") or "").lower()
            skip = False
            for key, vel_id in VELANA_BY_RESORT.items():
                if key in to_txt:
                    skip = True
                    break
            if skip:
                continue
        fc = (bt.get("from_city_cands") or [None])[0] if isinstance(bt.get("from_city_cands"), list) else None
        tc = (bt.get("to_city_cands") or [None])[0] if isinstance(bt.get("to_city_cands"), list) else None
        if fn.startswith("bp-"):
            fc = fc or None
        if tn.startswith("bp-"):
            tc = tc or None
        # infer city from node when city cands empty
        if not fc and not fn.startswith("bp-"):
            fc = fn if "-" in fn else None
        if not tc and not tn.startswith("bp-"):
            tc = tn if "-" in tn else None
        add({
            "market": market,
            "corridor": bt.get("corridor"),
            "from_node": fn,
            "to_node": tn,
            "from_label": bt.get("from_label") or bt.get("from_text"),
            "to_label": bt.get("to_label") or bt.get("to_text"),
            "from_city_id": fc or resolve_city_from_bp(fn, bt),
            "to_city_id": tc or resolve_city_from_bp(tn, bt),
            "distance_nm": bt.get("distance_nm"),
            "tag": tag.replace("saudi", "ksa").replace("uae", "uae")[:24],
        })

    # Penghu outer islands — fix bad grounding coords
    add({
        "market": "taiwan",
        "corridor": "Magong (Penghu) -> Wang'an Island",
        "from_node": "bp-552e493efe",
        "to_node": "bp-811346767d",
        "from_label": "Magong Harbor",
        "to_label": "Wang An Tanmengang",
        "from_city_id": "penghu-taiwan",
        "to_city_id": "penghu-taiwan",
        "distance_nm": 18.0,
        "tag": "penghu-taiwan",
    })

    return rows


def resolve_city_from_bp(node_id: str, bt: dict) -> str | None:
    cands = bt.get("from_city_cands") or bt.get("to_city_cands") or []
    if cands:
        return cands[0]
    return None


def main():
    fbt = load_json(DC / "FEATURES_BY_TYPE.json")
    poi_changes = apply_poi_scan(fbt)
    save_json(DC / "FEATURES_BY_TYPE.json", fbt)

    grounding = load_json(GROUNDING_PATH)
    bp_idx = build_bp_index(fbt)
    cities = build_city_index(fbt)
    mask = load_land_mask()
    routes = route_features(load_json(DC / "ROUTES.json"))
    existing = {r["properties"]["id"] for r in routes if r.get("properties", {}).get("id")}

    minted: list[dict] = []
    skipped: list[dict] = []

    for row in build_target_rows(grounding):
        fn, tn = row["from_node"], row["to_node"]
        a = resolve_coords(fn, bp_idx, fbt)
        b = resolve_coords(tn, bp_idx, fbt)
        if not a or not b:
            skipped.append({**row, "reason": "missing_coords"})
            continue
        rid = e_route_id(row.get("tag", "corr"), fn, tn)
        if rid in existing:
            skipped.append({**row, "reason": "exists", "route_id": rid})
            continue
        coords = build_coastal_path(a, b, mask)
        land_km = interior_land_km(coords, mask)
        feat = make_e_feature(row, coords, cities, land_km=land_km)
        routes.append(feat)
        existing.add(feat["properties"]["id"])
        minted.append({
            "route_id": feat["properties"]["id"],
            "corridor": row.get("corridor"),
            "market": row.get("market"),
            "nm": feat["properties"]["distance_nm"],
        })

    save_routes(DC / "ROUTES.json", routes)

    allow_path = DC / "route_water_allowlist.json"
    allow = load_json(allow_path)
    ids = list(allow.get("ids", []))
    seen = set(ids)
    added = []
    for m in minted:
        rid = m["route_id"]
        if rid not in seen:
            ids.append(rid)
            seen.add(rid)
            added.append(rid)
    allow["ids"] = ids
    meta = allow.setdefault("_meta", {})
    meta["build_target_mint_at"] = datetime.now(timezone.utc).isoformat()
    meta["build_target_mint_count"] = len(added)
    meta["build_target_poi_scan"] = poi_changes
    save_json(allow_path, allow)

    report = {
        "at": datetime.now(timezone.utc).isoformat(),
        "poi_changes": poi_changes,
        "minted": minted,
        "skipped": skipped,
        "allowlist_added": len(added),
    }
    out = ROOT / "navier/handoff/journey-relink/build-target-mint-report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    save_json(out, report)

    print(f"POI scan: {poi_changes}")
    print(f"minted {len(minted)} corridors, skipped {len(skipped)}, allowlist +{len(added)}")
    for m in minted:
        print(f"  {m['route_id']} {m['corridor'][:50]} ({m['nm']} nm)")


if __name__ == "__main__":
    main()