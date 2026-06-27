#!/usr/bin/env python3
"""#121 — repoint 3 hospitality partners to correct Velana resort jetties."""
from __future__ import annotations

import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROUTES = ROOT / "data-clean/ROUTES.json"
ALLOW = ROOT / "data-clean/route_water_allowlist.json"
PARTNERS = ROOT / "data-clean/partners"
REPORT = ROOT / "handoff/partner-map-model/maldives-121-repoint-report.json"

VELANA = [73.529, 4.1918]
VELANA_FROM = "male-maldives__velana-seaplane-terminal"

# partner -> (route_id, to_node, to_label, to_coords, distance_nm, platform)
REPOINTS = {
    "crown-champa": (
        "e__velana__kuredu-jetty",
        "male-maldives__kuredu-resort",
        "Kuredu Island Resort",
        [73.47, 5.46],
        76.2,
        "Quanta-LR",
    ),
    "villa-hotels": (
        "e__velana__sun-island-jetty",
        "male-maldives__sun-resort",
        "Sun Island Resort",
        [72.817729, 3.482408],
        60.2,
        "Quanta-LR",
    ),
    "sun-siyam": (
        "e__velana__iru-fushi-jetty",
        "male-maldives__iru-fushi-jetty",
        "Sun Siyam Iru Fushi",
        [73.32, 5.74],
        93.8,
        "Quanta-LR",
    ),
}

VELANA_JOURNEY_KEYS = (
    ("velana international airport (malé)", "north & south malé atoll resorts"),
    ("velana international airport", "greater malé / hulhumalé urban waterfront"),
    ("velana international", "north & south malé atoll resorts"),
)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").lower().strip())


def lerp_line(a: list[float], b: list[float], n: int = 10) -> list[list[float]]:
    return [[a[0] + (b[0] - a[0]) * i / (n - 1), a[1] + (b[1] - a[1]) * i / (n - 1)] for i in range(n)]


def mint_route(rid: str, to_node: str, to_label: str, to_coords: list[float], dist: float, platform: str) -> dict:
    return {
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": lerp_line(VELANA, to_coords)},
        "properties": {
            "id": rid,
            "distance_nm": round(dist, 1),
            "edge_class": "inter-island",
            "from": VELANA_FROM,
            "from_city": "Malé",
            "from_city_id": "male-maldives",
            "from_label": "Velana Seaplane",
            "to": to_node,
            "to_city": "Malé",
            "to_city_id": "male-maldives",
            "to_label": to_label,
            "label": f"Malé: Velana Seaplane → {to_label}",
            "platform": platform,
            "trip_scope": "intra_city",
            "relevance": "hide",
            "traffic_weight": 0.58,
            "_maldives_121_mint": utc_now(),
        },
    }


def journey_key(item: dict) -> bool:
    fr, to = norm(item.get("from", "")), norm(item.get("to", ""))
    for a, b in VELANA_JOURNEY_KEYS:
        if a in fr and b in to:
            return True
    if "velana" in fr and ("malé" in to or "male" in to or "resort" in to):
        return True
    return False


def bind_item(item: dict, rid: str, route: dict) -> None:
    p = route["properties"]
    item["route_id"] = rid
    item["route_ids"] = [rid]
    item["distance_nm"] = p["distance_nm"]
    item["platform"] = p["platform"]
    item["from_node_id"] = p["from"]
    item["to_node_id"] = p["to"]
    item["_link_kind"] = "velana-resort"
    item["_link_status"] = "linked-grok-scoped"
    item["_link_source"] = "grok/maldives-121-repoint"
    item.pop("_hold_reason", None)


def repoint_partner(slug: str, rid: str, route: dict) -> dict:
    path = PARTNERS / f"{slug}.json"
    doc = json.loads(path.read_text())
    jj = jf = 0
    for j in doc.get("journeys_unlocked") or []:
        if isinstance(j, dict) and journey_key(j):
            bind_item(j, rid, route)
            jj += 1
    for ph in doc.get("phases") or []:
        for fr in ph.get("featured_routes") or []:
            if isinstance(fr, dict) and "velana" in norm(fr.get("label", "")):
                bind_item(fr, rid, route)
                jf += 1
    doc.setdefault("_velana_hospitality_bind", {})["applied_at"] = utc_now()
    doc["_velana_hospitality_bind"]["route_id"] = rid
    doc["_velana_hospitality_bind"]["journeys"] = jj
    doc["_velana_hospitality_bind"]["featured"] = jf
    doc["_velana_hospitality_bind"]["maldives_121"] = True
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    pj = ROOT / "partner-pitch/partners" / f"{slug}.json"
    if pj.exists():
        pj.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    return {"partner": slug, "route_id": rid, "journeys": jj, "featured": jf}


def main() -> int:
    routes = json.loads(ROUTES.read_text())
    by_id = {f["properties"]["id"]: f for f in routes}
    minted = []

    for slug, spec in REPOINTS.items():
        rid, to_node, to_label, coords, dist, platform = spec
        if rid not in by_id:
            feat = mint_route(rid, to_node, to_label, coords, dist, platform)
            routes.append(feat)
            by_id[rid] = feat
            minted.append(rid)
        repoint_partner(slug, rid, by_id[rid])

    ROUTES.write_text(json.dumps(routes, ensure_ascii=False) + "\n")

    allow = json.loads(ALLOW.read_text())
    ids = list(allow.get("ids", []))
    seen = set(ids)
    for rid in minted:
        if rid not in seen:
            ids.append(rid)
            seen.add(rid)
    allow["ids"] = ids
    allow.setdefault("_meta", {})["maldives_121_at"] = utc_now()
    ALLOW.write_text(json.dumps(allow, indent=2, ensure_ascii=False) + "\n")

    # update bind_velana script mapping for future runs
    bind_script = ROOT / "scripts/grok-econ-reseal/bind_velana_hospitality_corridors.py"
    text = bind_script.read_text()
    text = text.replace(
        '"crown-champa": "e__velana__kurumba-jetty",',
        '"crown-champa": "e__velana__kuredu-jetty",',
    )
    text = text.replace(
        '"villa-hotels": "e__velana__baros-jetty",',
        '"villa-hotels": "e__velana__sun-island-jetty",',
    )
    text = text.replace(
        '"sun-siyam": "e__velana__westin-miriandhoo-jetty",',
        '"sun-siyam": "e__velana__iru-fushi-jetty",',
    )
    bind_script.write_text(text)

    out = {"at": utc_now(), "minted": minted, "repoints": list(REPOINTS.keys())}
    REPORT.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())