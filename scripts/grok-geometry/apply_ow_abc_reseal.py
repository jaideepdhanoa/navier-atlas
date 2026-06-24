#!/usr/bin/env python3
"""Apply PR #97 ABC scale-vision re-seal to ocean-whisperer partner JSON."""
from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOGO_URL = "https://drive.google.com/uc?export=download&id=1v8v6PYYwX1-o9rH071WzVrT7nEns4cA6"

JOURNEY_TEMPLATES = [
    {
        "from": "Hato (Curaçao Int'l) airport waterfront",
        "to": "Baoase Luxury Resort (south coast, near Willemstad)",
        "today": "A diesel shuttle or road transfer — loud, off-brand for an aviation-luxury operator.",
        "with_navier": "A silent foiling run from the air gateway to Baoase — an existing Ocean Whisperer air destination, now at sea.",
        "from_node_id": "curacao-curacao__hato-airport-waterfront",
        "to_node_id": "curacao-curacao__baoase-luxury-resort",
        "route_id": "rn-838ccd054530",
        "render": "solid",
        "economics_status": "bound",
    },
    {
        "from": "Willemstad / Sint Anna Bay (cruise mega-pier)",
        "to": "Sandals Royal Curaçao (Spanish Water)",
        "today": "Cruise pax move by bus or diesel shuttle to the flagship resort.",
        "with_navier": "A premium silent foiling run from the UNESCO waterfront to Sandals Royal Curaçao.",
        "from_node_id": "curacao-curacao__willemstad-sint-anna-bay",
        "to_node_id": "curacao-curacao__sandals-royal-curacao-spanish-water",
        "route_id": "rn-d1eb05689785",
        "render": "solid",
        "economics_status": "bound",
    },
    {
        "from": "Spanish Water / Jan Thiel",
        "to": "Baoase Luxury Resort",
        "today": "A short diesel hop between resort clusters.",
        "with_navier": "A curated inter-resort foiling hop — silent, premium, on-brand.",
        "from_node_id": "curacao-curacao__spanish-water-jan-thiel",
        "to_node_id": "curacao-curacao__baoase-luxury-resort",
        "route_id": "rn-43c96cef749c",
        "render": "solid",
        "economics_status": "bound",
    },
    {
        "from": "Curaçao (Spanish Water)",
        "to": "Aruba (Oranjestad / Renaissance Marina)",
        "today": "A turboprop inter-island hop or no direct sea link.",
        "with_navier": "A Quanta-LR network leg — the standardization story, island-to-island (roadmap).",
        "from_node_id": "curacao-curacao__spanish-water-jan-thiel",
        "to_node_id": "aruba-aruba__oranjestad-renaissance-marina",
        "route_id": "rn-e96930f83c0f",
        "platform": "Quanta-LR",
        "render": "roadmap-amber-dashed",
        "economics_status": "roadmap_excluded",
    },
]

ROUTE_META = {
    "rn-a3a94b8dbc88": {"distance_nm": 9.4, "platform": "Pioneer II"},
    "rn-838ccd054530": {"distance_nm": 6.3, "platform": "Pioneer II"},
    "rn-d1eb05689785": {"distance_nm": 5.6, "platform": "Pioneer II"},
    "rn-43c96cef749c": {"distance_nm": 3.2, "platform": "Pioneer II"},
    "rn-29425ce31839": {"distance_nm": 2.7, "platform": "Pioneer II"},
    "rn-09a43a616a1a": {"distance_nm": 14.0, "platform": "Pioneer II"},
    "rn-0f8e77cfef46": {"distance_nm": 33.3, "platform": "Pioneer II", "render": "roadmap-amber-dashed", "economics_status": "roadmap_excluded"},
    "rn-e96930f83c0f": {"distance_nm": 74.7, "platform": "Quanta-LR", "render": "roadmap-amber-dashed", "economics_status": "roadmap_excluded"},
}


def journey_shell(tmpl: dict) -> dict:
    rid = tmpl["route_id"]
    meta = ROUTE_META.get(rid, {})
    return {
        "from": tmpl["from"],
        "to": tmpl["to"],
        "today": tmpl["today"],
        "with_navier": tmpl["with_navier"],
        "distance_nm": meta.get("distance_nm"),
        "platform": tmpl.get("platform") or meta.get("platform", "Pioneer II"),
        "archetype": "hospitality",
        "from_node_id": tmpl["from_node_id"],
        "to_node_id": tmpl["to_node_id"],
        "route_id": rid,
        "_link_status": "linked-grok-node",
        "_link_kind": "corridor-label",
        "_link_source": "grok/apply_ow_abc_reseal",
        "economics_status": tmpl.get("economics_status") or meta.get("economics_status", "bound"),
        "render": tmpl.get("render") or meta.get("render", "solid"),
        "route_ids": [rid],
        **({"_economics_source": "economics_by_route_id.json"} if tmpl.get("economics_status", "bound") == "bound" else {}),
    }


def patch_route_refs(obj, routes: dict):
    if isinstance(obj, dict):
        rid = obj.get("route_id")
        if rid and rid in routes:
            obj["distance_nm"] = routes[rid]["distance_nm"]
            if routes[rid].get("platform"):
                obj["platform"] = routes[rid]["platform"]
        for v in obj.values():
            patch_route_refs(v, routes)
    elif isinstance(obj, list):
        for item in obj:
            patch_route_refs(item, routes)


def main() -> int:
    paths = [
        ROOT / "partner-pitch/partners/ocean-whisperer.json",
        ROOT / "data-clean/partners/ocean-whisperer.json",
    ]
    for path in paths:
        shutil.copy(path, str(path) + ".bak-pre-abc-reseal")
        data = json.loads(path.read_text())
        data["logo_url"] = LOGO_URL
        data["_authoring_status"] = (
            "GEOMETRY_RESEALED — ABC scale-vision restored (PR #97); economics bound; offshore routing fix applied."
        )

        by_rid = {j.get("route_id"): j for j in data.get("journeys_unlocked", []) if j.get("route_id")}
        for tmpl in JOURNEY_TEMPLATES:
            if tmpl["route_id"] not in by_rid:
                data.setdefault("journeys_unlocked", []).append(journey_shell(tmpl))
                by_rid[tmpl["route_id"]] = data["journeys_unlocked"][-1]

        # Ensure Bonaire roadmap render
        for j in data["journeys_unlocked"]:
            if j.get("route_id") == "rn-0f8e77cfef46":
                j["render"] = "roadmap-amber-dashed"
                j["economics_status"] = "roadmap_excluded"
                j["platform"] = "Pioneer II"
                j.pop("_economics_source", None)

        patch_route_refs(data, ROUTE_META)

        for ph in data.get("phases", []):
            if ph.get("n") == 3:
                ph["cities"] = ["curacao-curacao", "bonaire-bonaire", "aruba-aruba"]
                ph["route_scope"] = "cross-border"
                ph["featured_routes"] = [
                    {
                        "label": "Curaçao (Spanish Water) ↔ Bonaire (Kralendijk)",
                        "from_node_id": "curacao-curacao__spanish-water-jan-thiel",
                        "to_node_id": "bonaire-bonaire__kralendijk-town-pier",
                        "distance_nm": 33.3,
                        "platform": "Pioneer II",
                        "route_id": "rn-0f8e77cfef46",
                        "render": "roadmap-amber-dashed",
                        "economics_status": "roadmap_excluded",
                        "route_ids": ["rn-0f8e77cfef46"],
                        "_link_kind": "abc-scale-vision",
                        "_link_status": "linked-grok-node",
                        "_link_source": "grok/apply_ow_abc_reseal",
                    },
                    {
                        "label": "Curaçao (Spanish Water) ↔ Aruba (Oranjestad / Renaissance Marina)",
                        "from_node_id": "curacao-curacao__spanish-water-jan-thiel",
                        "to_node_id": "aruba-aruba__oranjestad-renaissance-marina",
                        "distance_nm": 74.7,
                        "platform": "Quanta-LR",
                        "route_id": "rn-e96930f83c0f",
                        "render": "roadmap-amber-dashed",
                        "economics_status": "roadmap_excluded",
                        "route_ids": ["rn-e96930f83c0f"],
                        "_link_kind": "abc-scale-vision",
                        "_link_status": "linked-grok-node",
                        "_link_source": "grok/apply_ow_abc_reseal",
                    },
                ]

        es = data.setdefault("end_state", {})
        es["addressable_market_count"] = 3
        es["end_state_cities"] = ["curacao-curacao", "bonaire-bonaire", "aruba-aruba"]
        es["addressable_regions"] = ["caribbean"]
        ss = es.setdefault("steady_state", {})
        ss["total_markets"] = "Curaçao captive core + Bonaire/Aruba roadmap (ABC scale-vision)"
        ss["total_corridors"] = "6 grounded + 1 seasonal + 2 roadmap network legs (sealed)"

        data["_abc_reseal_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        path.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
        print(f"wrote {path.relative_to(ROOT)} journeys={len(data['journeys_unlocked'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())