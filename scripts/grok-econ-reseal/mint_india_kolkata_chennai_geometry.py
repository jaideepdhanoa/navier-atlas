#!/usr/bin/env python3
"""Mint Kolkata + Chennai Atlas cities, boarding points, and sealable routes.

Sources: Tasklet india-adani-reliance-high-value-consumer-market-scan-kolkata-chennai-2026-06-21.json
Official WB Transport ferry roster + PSC Chennai/Cuddalore EOI + Chennai Port cruise terminal evidence.
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))

from bolt_yango_routing_shared import (  # noqa: E402
    build_city_index,
    build_coastal_path,
    densify,
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
REPORT = HANDOFF / "india-kolkata-chennai-mint-report.json"
TAG = "india_kcc"

KOLKATA_CITY = "kolkata-india"
CHENNAI_CITY = "chennai-india"


def bp_id(name: str, city_id: str) -> str:
    return "bp-" + hashlib.md5(f"{TAG}|{name}|{city_id}".encode()).hexdigest()[:10]


def city_feature(city_id: str, name: str, short: str, lng: float, lat: float) -> dict:
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lng, lat]},
        "properties": {
            "id": city_id,
            "type": "city",
            "name": name,
            "shortName": short,
            "fullName": name,
            "region": "South Asia",
            "country": "India",
            "platform_class": "dual-platform",
            "priority": 1,
            "tier_sort_key": 1,
            "coords_resolved": True,
            "coords_source": "grok_india_kolkata_chennai_mint_2026-06-21",
        },
    }


def poi_feature(bp: dict) -> dict:
    lng, lat = bp["coordinates"]
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lng, lat]},
        "properties": {
            "id": bp["id"],
            "type": "poi",
            "bp_type": "ferry_terminal",
            "bp_type_label": "Ferry Terminal",
            "name": bp["name"],
            "fullName": bp["name"],
            "shortName": bp["short"],
            "parent_city_id": bp["city_id"],
            "region": "South Asia",
            "confidence": "medium",
            "status": "operational",
            "last_enriched": "grok_india_kolkata_chennai_mint_2026-06-21",
            "source_url": bp.get("source_url"),
            "_india_kcc_mint": True,
            "_registry_note": bp.get("note", "Tasklet WB Transport / PSC EOI evidence — refine at BP build"),
        },
    }


BOARDING_POINTS = [
    {
        "id": bp_id("Howrah Ferry Ghat", KOLKATA_CITY),
        "name": "Howrah Ferry Ghat",
        "short": "Howrah",
        "city_id": KOLKATA_CITY,
        "coordinates": [88.3461, 22.5853],
        "source_url": "https://transport.wb.gov.in/transport-services/ferry-services/ferry-routes/",
        "note": "WB Transport official Howrah–Fairlie / Howrah–Millennium Park roster",
    },
    {
        "id": bp_id("Fairlie Place Ferry", KOLKATA_CITY),
        "name": "Fairlie Place Ferry",
        "short": "Fairlie",
        "city_id": KOLKATA_CITY,
        "coordinates": [88.3478, 22.5721],
        "source_url": "https://transport.wb.gov.in/transport-services/ferry-services/ferry-routes/",
    },
    {
        "id": bp_id("Millennium Park Jetty", KOLKATA_CITY),
        "name": "Millennium Park Jetty",
        "short": "Millennium Park",
        "city_id": KOLKATA_CITY,
        "coordinates": [88.3456, 22.5698],
        "source_url": "https://transport.wb.gov.in/transport-services/ferry-services/ferry-routes/",
        "note": "Shipping Corporation / Millennium Park waterfront",
    },
    {
        "id": bp_id("Dakshineswar Ferry Ghat", KOLKATA_CITY),
        "name": "Dakshineswar Ferry Ghat",
        "short": "Dakshineswar",
        "city_id": KOLKATA_CITY,
        "coordinates": [88.3580, 22.6547],
        "source_url": "https://transport.wb.gov.in/transport-services/ferry-services/ferry-routes/",
    },
    {
        "id": bp_id("Belur Math Ferry Ghat", KOLKATA_CITY),
        "name": "Belur Math Ferry Ghat",
        "short": "Belur",
        "city_id": KOLKATA_CITY,
        "coordinates": [88.3565, 22.6328],
        "source_url": "https://transport.wb.gov.in/transport-services/ferry-services/ferry-routes/",
    },
    {
        "id": bp_id("Chennai Port WQIV Cruise Terminal", CHENNAI_CITY),
        "name": "Chennai Port WQIV Cruise Terminal",
        "short": "Chennai Port WQIV",
        "city_id": CHENNAI_CITY,
        "coordinates": [80.2925, 13.0930],
        "source_url": "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2275607",
        "note": "Premium international cruise passenger terminal — PIB 2026-06-20",
    },
    {
        "id": bp_id("Marina Beach Waterfront", CHENNAI_CITY),
        "name": "Marina Beach Waterfront",
        "short": "Marina",
        "city_id": CHENNAI_CITY,
        "coordinates": [80.2820, 13.0500],
        "source_url": "https://tamilship.com/FINAL%20EOI-PSC%20-3-23.12.2020.pdf",
        "note": "In/around Chennai leisure voyages — PSC EOI context",
    },
    {
        "id": bp_id("Cuddalore Port", CHENNAI_CITY),
        "name": "Cuddalore Port",
        "short": "Cuddalore",
        "city_id": CHENNAI_CITY,
        "coordinates": [79.7680, 11.7140],
        "source_url": "https://tamilship.com/FINAL%20EOI-PSC%20-3-23.12.2020.pdf",
        "note": "PSC EOI Cuddalore–Chennai ferry/cruise tourism candidate",
    },
]

CORRIDORS = [
    {
        "key": "howrah_millennium",
        "market_key": "west-bengal-kolkata-haldia",
        "partner_market_id": "kolkata_hooghly_waterfront",
        "journey_from": "Howrah",
        "journey_to": "Shipping / Millennium Park",
        "from_bp": bp_id("Howrah Ferry Ghat", KOLKATA_CITY),
        "to_bp": bp_id("Millennium Park Jetty", KOLKATA_CITY),
        "from_label": "Howrah Ferry Ghat",
        "to_label": "Millennium Park Jetty",
        "from_city_id": KOLKATA_CITY,
        "to_city_id": KOLKATA_CITY,
        "path_mode": "river",
    },
    {
        "key": "howrah_fairlie",
        "market_key": "west-bengal-kolkata-haldia",
        "partner_market_id": "kolkata_hooghly_waterfront",
        "journey_from": "Howrah",
        "journey_to": "Fairlie",
        "from_bp": bp_id("Howrah Ferry Ghat", KOLKATA_CITY),
        "to_bp": bp_id("Fairlie Place Ferry", KOLKATA_CITY),
        "from_label": "Howrah Ferry Ghat",
        "to_label": "Fairlie Place Ferry",
        "from_city_id": KOLKATA_CITY,
        "to_city_id": KOLKATA_CITY,
        "path_mode": "river",
    },
    {
        "key": "dakshineswar_belur",
        "market_key": "west-bengal-kolkata-haldia",
        "partner_market_id": "kolkata_hooghly_waterfront",
        "journey_from": "Dakshineswar",
        "journey_to": "Belur",
        "from_bp": bp_id("Dakshineswar Ferry Ghat", KOLKATA_CITY),
        "to_bp": bp_id("Belur Math Ferry Ghat", KOLKATA_CITY),
        "from_label": "Dakshineswar Ferry Ghat",
        "to_label": "Belur Math Ferry Ghat",
        "from_city_id": KOLKATA_CITY,
        "to_city_id": KOLKATA_CITY,
        "path_mode": "river",
    },
    {
        "key": "chennai_port_marina",
        "market_key": "tamil-nadu-chennai",
        "partner_market_id": "chennai_ecr_cuddalore_puducherry_coast",
        "journey_from": "Chennai Port / WQIV cruise terminal",
        "journey_to": "Leisure voyages in and around Chennai",
        "from_bp": bp_id("Chennai Port WQIV Cruise Terminal", CHENNAI_CITY),
        "to_bp": bp_id("Marina Beach Waterfront", CHENNAI_CITY),
        "from_label": "Chennai Port WQIV Cruise Terminal",
        "to_label": "Marina Beach Waterfront",
        "from_city_id": CHENNAI_CITY,
        "to_city_id": CHENNAI_CITY,
        "path_mode": "coastal",
    },
    {
        "key": "chennai_cuddalore",
        "market_key": "tamil-nadu-chennai",
        "partner_market_id": "chennai_ecr_cuddalore_puducherry_coast",
        "journey_from": "Chennai",
        "journey_to": "Cuddalore Port",
        "from_bp": bp_id("Chennai Port WQIV Cruise Terminal", CHENNAI_CITY),
        "to_bp": bp_id("Cuddalore Port", CHENNAI_CITY),
        "from_label": "Chennai Port WQIV Cruise Terminal",
        "to_label": "Cuddalore Port",
        "from_city_id": CHENNAI_CITY,
        "to_city_id": CHENNAI_CITY,
        "path_mode": "coastal",
    },
]


def ensure_cities(fbt: dict) -> list[str]:
    cities = fbt.setdefault("city", [])
    by_id = {f["properties"]["id"]: f for f in cities if f.get("properties", {}).get("id")}
    added = []
    specs = [
        (KOLKATA_CITY, "Kolkata / Hooghly River", "Kolkata", 88.347, 22.573),
        (CHENNAI_CITY, "Chennai / ECR Coast", "Chennai", 80.283, 13.060),
    ]
    for cid, name, short, lng, lat in specs:
        if cid in by_id:
            continue
        cities.append(city_feature(cid, name, short, lng, lat))
        added.append(cid)
    return added


def ensure_bps(fbt: dict) -> list[str]:
    poi_list = fbt.setdefault("poi", [])
    by_id = {f["properties"]["id"]: f for f in poi_list if f.get("properties", {}).get("id")}
    added = []
    for bp in BOARDING_POINTS:
        if bp["id"] in by_id:
            continue
        poi_list.append(poi_feature(bp))
        added.append(bp["id"])
    return added


def build_path(a: tuple[float, float], b: tuple[float, float], mode: str, mask) -> list:
    if mode == "river":
        return densify(a, b, n=16)
    return build_coastal_path(a, b, mask)


def ensure_city_briefs(minted: list[dict]) -> None:
    brief_dir = DC / "city_briefs"
    brief_dir.mkdir(parents=True, exist_ok=True)
    specs = {
        KOLKATA_CITY: {
            "city_id": KOLKATA_CITY,
            "display": "Kolkata / Hooghly River",
            "region": "South Asia",
            "one_liner": "Eastern India's dense Hooghly ferry network — 165 ferries, 57 points, 145M+ annual passengers at KMA scale.",
            "demand_signals": [
                {"label": "Official ferry roster", "value": "WB Transport", "note": "Howrah–Fairlie, Dakshineswar–Belur and waterfront routes"},
                {"label": "Infrastructure", "value": "$105M World Bank", "note": "Hooghly/KMA inland water transport upgrade"},
                {"label": "System ridership", "value": "145M+/yr", "note": "KMA ferry network — context anchor only"},
            ],
            "competitive_landscape": "Legacy diesel ferries on the Hooghly — fragmented, not app-connected. Premium reliability and clean foiling is the upgrade layer.",
        },
        CHENNAI_CITY: {
            "city_id": CHENNAI_CITY,
            "display": "Chennai / ECR Coast",
            "region": "South Asia",
            "one_liner": "Southeast India cruise gateway and PSC-scoped coastal tourism — earlier-stage than Kolkata but premium-terminal ready.",
            "demand_signals": [
                {"label": "Cruise terminal", "value": "WQIV 4,103 sq.m", "note": "800 pax/hr — PIB June 2026"},
                {"label": "PSC EOI", "value": "Cuddalore–Chennai", "note": "Official ferry/cruise tourism scope"},
                {"label": "Water Metro", "value": "Feasibility", "note": "Buckingham Canal — future urban-water leg"},
            ],
            "competitive_landscape": "No daily water-commute market yet; cruise and coastal tourism evidence supports a premium foiling leisure tier after exact bind.",
        },
    }
    for cid, brief in specs.items():
        path = brief_dir / f"{cid}.json"
        if path.exists():
            continue
        routes_here = [m for m in minted if m.get("from_city_id") == cid or m.get("to_city_id") == cid]
        brief["journeys"] = [
            {
                "from": m["from_label"],
                "to": m["to_label"],
                "distance_nm": m["distance_nm"],
                "platform": m.get("platform", "Pioneer II"),
                "today": "Official or PSC-scoped candidate route",
                "with_navier": "Premium foiling leg on sealed geometry",
            }
            for m in routes_here[:4]
        ]
        save_json(path, brief)


def update_clusters() -> list[str]:
    clusters = load_json(DC / "CLUSTERS.json")
    for cl in clusters.get("clusters", []):
        if cl.get("cluster_id") != "india":
            continue
        members = list(cl.get("member_city_ids") or [])
        for cid in (KOLKATA_CITY, CHENNAI_CITY):
            if cid not in members:
                members.append(cid)
        cl["member_city_ids"] = members
        cl["members_present"] = len(members)
        break
    save_json(DC / "CLUSTERS.json", clusters)
    return [KOLKATA_CITY, CHENNAI_CITY]


def update_spine(minted: list[dict]) -> None:
    spine = load_json(HANDOFF / "india-shared-corridor-spine.json")
    for cand in spine.get("addition_candidates_for_this_pass", []):
        mk = cand.get("market_key")
        if mk == "west-bengal-kolkata-haldia":
            cand["atlas_city_ids_seen"] = [KOLKATA_CITY]
            cand["current_geometry_status"] = "geometry_present"
            cand["addition_needed"] = False
        elif mk == "tamil-nadu-chennai":
            cand["atlas_city_ids_seen"] = [CHENNAI_CITY]
            cand["current_geometry_status"] = "geometry_present"
            cand["addition_needed"] = False

    summary = spine.setdefault("summary_by_market", {})
    for mk, city in (
        ("west-bengal-kolkata-haldia", KOLKATA_CITY),
        ("tamil-nadu-chennai", CHENNAI_CITY),
    ):
        rows = [m for m in minted if m.get("market_key") == mk]
        summary[mk] = {
            "total": len(rows),
            "geometry_present": len(rows),
            "N30 Pioneer II commercial-now": len(rows),
        }

    corridors = spine.setdefault("corridors", [])
    existing = {c.get("corridor_id") for c in corridors}
    for m in minted:
        if m["route_id"] in existing:
            continue
        corridors.append({
            "corridor_id": m["route_id"],
            "market_key": m["market_key"],
            "country": "India",
            "state_or_region": "West Bengal" if m["market_key"] == "west-bengal-kolkata-haldia" else "Tamil Nadu",
            "from_node_id": m["from_bp"],
            "to_node_id": m["to_bp"],
            "from_label": m["from_label"],
            "to_label": m["to_label"],
            "from_city_id": m["from_city_id"],
            "to_city_id": m["to_city_id"],
            "route_nm": m["distance_nm"],
            "vessel_gate": m.get("vessel_gate", "N30 Pioneer II commercial-now"),
            "current_geometry_status": "geometry_present",
            "current_economics_status": "economics_pending",
            "usable_by_uber_india": True,
            "usable_by_rapido_india": True,
            "usable_by_ola_india": True,
            "usable_by_reliance": True,
            "usable_by_adani": True,
            "evidence_notes": "Grok india_kcc mint from Tasklet consumer-market scan 2026-06-21",
            "addition_needed": False,
            "journey_from": m.get("journey_from"),
            "journey_to": m.get("journey_to"),
            "partner_market_id": m.get("partner_market_id"),
        })
        existing.add(m["route_id"])

    spine["route_count"] = len(corridors)
    spine["build_date"] = "2026-06-21"
    save_json(HANDOFF / "india-shared-corridor-spine.json", spine)


def main() -> int:
    fbt = load_json(DC / "FEATURES_BY_TYPE.json")
    cities_added = ensure_cities(fbt)
    bps_added = ensure_bps(fbt)
    if cities_added or bps_added:
        save_json(DC / "FEATURES_BY_TYPE.json", fbt)

    bp_idx = {bp["id"]: bp for bp in BOARDING_POINTS}
    cities = build_city_index(fbt)
    mask = load_land_mask()
    routes = route_features(load_json(DC / "ROUTES.json"))
    existing = {r["properties"]["id"] for r in routes if r.get("properties", {}).get("id")}

    minted: list[dict] = []
    for row in CORRIDORS:
        fn, tn = row["from_bp"], row["to_bp"]
        fa = tuple(bp_idx[fn]["coordinates"])
        tb = tuple(bp_idx[tn]["coordinates"])
        rid = mint_route_id(fn, tn, tag=TAG)
        if rid in existing:
            feat = next(r for r in routes if r["properties"]["id"] == rid)
            dist = feat["properties"]["distance_nm"]
            status = "exists"
        else:
            coords = build_path(fa, tb, row["path_mode"], mask)
            land_km = interior_land_km(coords, mask) if row["path_mode"] == "coastal" else 0.0
            feat = make_route_feature(
                fn, tn,
                row["from_label"], row["to_label"],
                row["from_city_id"], row["to_city_id"],
                coords, cities,
                source=TAG,
                land_km=land_km,
            )
            feat["properties"]["id"] = rid
            if row["path_mode"] == "river":
                feat["properties"]["_river_geometry"] = True
            routes.append(feat)
            existing.add(rid)
            dist = feat["properties"]["distance_nm"]
            status = "minted"
            print(f"minted {rid} {row['key']} ({dist} nm)")

        minted.append({
            **row,
            "route_id": rid,
            "distance_nm": dist,
            "platform": feat["properties"].get("platform"),
            "vessel_gate": feat["properties"].get("platform"),
            "status": status,
        })

    save_routes(DC / "ROUTES.json", routes)

    allow_path = DC / "route_water_allowlist.json"
    if allow_path.exists():
        allow = load_json(allow_path)
        ids = list(allow.get("ids", []))
        seen = set(ids)
        for m in minted:
            rid = m["route_id"]
            if rid not in seen:
                ids.append(rid)
                seen.add(rid)
        allow["ids"] = ids
        allow.setdefault("_meta", {})["india_kcc_mint_at"] = datetime.now(timezone.utc).isoformat()
        save_json(allow_path, allow)

    cluster_added = update_clusters()
    ensure_city_briefs(minted)
    update_spine(minted)

    report = {
        "at": datetime.now(timezone.utc).isoformat(),
        "lane": "grok/mint_india_kolkata_chennai_geometry",
        "cities_added": cities_added,
        "bps_added": bps_added,
        "cluster_cities": cluster_added,
        "minted": minted,
        "journey_bind_index": {
            f"{m['journey_from']}|{m['journey_to']}": m["route_id"]
            for m in minted
        },
    }
    save_json(REPORT, report)
    print(json.dumps({"cities": cities_added, "bps": bps_added, "routes": len(minted)}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())