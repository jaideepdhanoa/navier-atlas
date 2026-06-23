#!/usr/bin/env python3
"""Côte d'Azur de-bundle: mint city nodes, rekey POIs, rebuild route endpoints (PR #81)."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
from bolt_yango_shared import infer_country_region, load_json, save_json  # noqa: E402

HANDOFF = ROOT / "navier/handoff/cote-dazur-debundle"
NODE_MAP = HANDOFF / "node-map.json"
REPORT_PATH = ROOT / "grok-routing-output/cote-dazur-debundle-report.json"

CATCHALL_KEYWORDS = (
    "menton", "villefranche", "sanremo", "portofino", "hyères", "hyeres", "toulon",
    "porquerolles", "port-cros", "lerins", "honorat", "marguerite", "planaria",
)

NODE_DEFS = [
    ("nice-france", "Nice", "Nice", 7.284, 43.695, "Port Lympia gateway"),
    ("cannes-france", "Cannes", "Cannes", 7.017, 43.551, "Vieux Port / Pierre Canto"),
    ("antibes-france", "Antibes", "Antibes", 7.128, 43.585, "Port Vauban"),
    ("saint-tropez-france", "Saint-Tropez", "St-Tropez", 6.638, 43.272, "Port de Saint-Tropez"),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def slug(s: str) -> str:
    s = re.sub(r"[^\w\s-]", "", s.lower())
    return re.sub(r"\s+", "-", s.strip())


def classify_poi(name: str, label_map: dict[str, str]) -> str:
    n = (name or "").lower()
    for label, node in label_map.items():
        if label.lower() in n:
            return node
    if any(k in n for k in ("monaco", "hercule", "fontvieille")):
        return "monaco-monaco"
    if "nice" in n or "lympia" in n or "saint-laurent" in n:
        return "nice-france"
    if "cannes" in n or "canto" in n and "cannes" not in n:
        if "canto" in n or "cannes" in n:
            return "cannes-france"
    if "cannes" in n or "lerins" in n or "marguerite" in n:
        return "cannes-france"
    if "antibes" in n or "vauban" in n or "juan-les-pins" in n or "juan les pins" in n:
        return "antibes-france"
    if "tropez" in n or "pampelonne" in n or "sainte-maxime" in n or "ste maxime" in n:
        return "saint-tropez-france"
    if any(k in n for k in CATCHALL_KEYWORDS):
        return "cote-dazur-france"
    # default: catch-all cluster parent
    return "cote-dazur-france"


def city_feature(cid: str, name: str, short: str, lng: float, lat: float, parent_cluster: str) -> dict:
    country, region = infer_country_region(cid, name)
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lng, lat]},
        "properties": {
            "id": cid,
            "type": "city",
            "name": name,
            "shortName": short,
            "fullName": name,
            "country": country or "France",
            "region": region or "europe-med",
            "parent_cluster": parent_cluster,
            "platform_class": "dual-platform",
            "coords_resolved": True,
            "coords_source": "grok_cote_dazur_debundle_2026-06-23",
            "confidence": "high",
            "status": "operational",
            "_cote_dazur_debundle": True,
        },
    }


def rekey_endpoint(val: str | None, bp_parent: dict[str, str]) -> str | None:
    if not val or "cote-dazur-france" not in val:
        return val
    if val == "cote-dazur-france":
        return val
    suffix = val.split("__", 1)[-1] if "__" in val else val
    for old_parent, new_parent in bp_parent.items():
        if old_parent == "cote-dazur-france":
            continue
    # map slug endpoint to new city prefix
    mapping = {
        "port-de-nice": "nice-france",
        "vieux-port-cannes": "cannes-france",
        "cannes-quai-laubeuf-l-rins-ferry": "cannes-france",
        "port-vauban-antibes": "antibes-france",
        "port-de-saint-tropez": "saint-tropez-france",
        "saint-tropez-vieux-port-bateaux-verts": "saint-tropez-france",
    }
    new_city = mapping.get(suffix)
    if new_city:
        return f"{new_city}__{suffix}"
    return val


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dc", default="data-clean")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    dc = ROOT / args.dc
    node_map = load_json(NODE_MAP)
    parent_cluster = node_map.get("cluster_parent", "cote-dazur-france")
    label_map = node_map.get("poi_rekey_rule", {}).get("label_to_node", {})

    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    routes_raw = load_json(dc / "ROUTES.json")
    routes = routes_raw if isinstance(routes_raw, list) else routes_raw.get("features", [])
    clusters = load_json(dc / "CLUSTERS.json")

    poi_before = sum(
        1 for p in fbt.get("poi", [])
        if (p.get("properties") or {}).get("parent_city_id") == "cote-dazur-france"
    )
    rekey_actions: list[dict] = []

    cities = fbt.setdefault("city", [])
    city_ids = {f["properties"]["id"] for f in cities if f.get("properties", {}).get("id")}
    minted = []
    for cid, name, short, lng, lat, note in NODE_DEFS:
        if cid not in city_ids:
            cities.append(city_feature(cid, name, short, lng, lat, parent_cluster))
            minted.append(cid)
            city_ids.add(cid)

    # tag monaco in cluster family
    for f in cities:
        p = f.get("properties", {})
        if p.get("id") == "monaco-monaco":
            p["parent_cluster"] = parent_cluster
            p["_cote_dazur_cluster_member"] = True

    bp_parent: dict[str, str] = {}
    new_pois = []
    per_node: dict[str, int] = {}
    for poi in fbt.get("poi", []):
        props = poi.get("properties", poi)
        if props.get("parent_city_id") != "cote-dazur-france":
            new_pois.append(poi)
            continue
        old_id = props.get("id")
        name = props.get("name") or ""
        new_parent = classify_poi(name, label_map)
        per_node[new_parent] = per_node.get(new_parent, 0) + 1
        if new_parent != "cote-dazur-france":
            props["parent_city_id"] = new_parent
            props["_rekey_from"] = "cote-dazur-france"
            props["_rekey_at"] = utc_now()
            rekey_actions.append({"id": old_id, "name": name, "from": "cote-dazur-france", "to": new_parent})
        if old_id:
            bp_parent[old_id] = new_parent
        new_pois.append(poi)

    route_updates = 0
    for feat in routes:
        p = feat.get("properties", feat)
        changed = False
        for key in ("from_city_id", "to_city_id", "from_city", "to_city"):
            v = p.get(key)
            if v == "cote-dazur-france":
                # inter-city routes keep catch-all unless endpoint slug hints
                pass
        for key in ("from", "to", "from_node", "to_node"):
            old = p.get(key)
            new = rekey_endpoint(old, bp_parent)
            if new != old:
                p[key] = new
                changed = True
        if changed:
            route_updates += 1
            p["_cote_dazur_repoint"] = utc_now()

    # update cluster membership
    for cl in clusters.get("clusters") or []:
        if cl.get("cluster_id") == "cote-dazur-france-archipelago":
            members = list(cl.get("member_city_ids") or [])
            for cid in ("nice-france", "cannes-france", "antibes-france", "saint-tropez-france"):
                if cid not in members:
                    members.append(cid)
            if "monaco-monaco" not in members:
                members.append("monaco-monaco")
            cl["member_city_ids"] = members
            cl["members_present"] = len(members)
            cl["_debundle_at"] = utc_now()

    if args.apply:
        fbt["poi"] = new_pois
        save_json(dc / "FEATURES_BY_TYPE.json", fbt)
        if isinstance(routes_raw, list):
            save_json(dc / "ROUTES.json", routes)
        else:
            routes_raw["features"] = routes
            save_json(dc / "ROUTES.json", routes_raw)
        save_json(dc / "CLUSTERS.json", clusters)

    poi_after_catchall = per_node.get("cote-dazur-france", 0)
    report = {
        "at": utc_now(),
        "lane": "grok/apply_cote_dazur_debundle",
        "apply": args.apply,
        "nodes_minted": minted,
        "poi_before_parent_cote_dazur": poi_before,
        "poi_rekeyed": len(rekey_actions),
        "poi_per_node": per_node,
        "poi_catchall_remaining": poi_after_catchall,
        "routes_repointed": route_updates,
        "aspirational_empty_nodes": [cid for cid, _, _, _, _, _ in NODE_DEFS if per_node.get(cid, 0) == 0],
        "silent_drops": 0,
        "partner_view_anchor_cities": node_map.get("partner_view", {}).get("anchor_cities"),
        "sample_rekeys": rekey_actions[:15],
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    save_json(REPORT_PATH, report)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())