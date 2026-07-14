#!/usr/bin/env python3
"""Alexandria candidate marine geography — BPs + corridors, economics null.

Implements GROK-SPEC-alexandria-candidate-geography-2026-07-14.md:
  - Mint candidate boarding points at named facilities (authoritative coords)
  - Mint candidate corridors (heritage loop + coastal hop)
  - No demand, fares, or economics
  - Exclude Marina El Alamein / North Coast and Cairo Nile

Hard gates before any economics remain in the receipt.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))

from bolt_yango_routing_shared import (  # noqa: E402
    interior_land_km,
    load_land_mask,
    load_json,
    make_route_feature,
    mint_route_id,
    path_length_km,
    route_features,
    save_json,
    save_routes,
    is_water,
)

DC = ROOT / "data-clean"
FBT_PATH = DC / "FEATURES_BY_TYPE.json"
ROUTES_PATH = DC / "ROUTES.json"
CLUSTERS_PATH = DC / "CLUSTERS.json"
PARTNER_DC = DC / "partners/indrive.json"
PARTNER_PITCH = ROOT / "partner-pitch/partners/indrive.json"
MARKET_SCOPE = ROOT / "deck-studio/decks/indrive-egypt/market-scope.json"
RECEIPT = (
    ROOT
    / "handoff/partner-map-model/indrive-scope-expansion-2026-07-13"
    / "ALEXANDRIA-CANDIDATE-GEOGRAPHY-RECEIPT-2026-07-14.json"
)

NOW = datetime.now(timezone.utc).isoformat()
CITY_ID = "alexandria-egypt"
CLUSTER_ID = "egypt"
LAND_GATE_KM = 0.35
NM_PER_KM = 0.539957

# Authoritative named-facility coordinates (lng, lat)
# Qaitbay: Wikipedia Citadel of Qaitbay 31.2130°N 29.8852°E
# Bibliotheca: Wikipedia Bibliotheca Alexandrina 31.20889°N 29.90917°E
# Montaza: Wikipedia Montaza Palace 31°17′19″N 30°0′56″E → 31.28861, 30.01556;
#   BP boarding anchor is nearest water north of the palace into Montaza Bay
#   (facility is on land; passenger rides depart the bay — candidate only).
BPS = {
    "bp-alex-qaitbay": {
        "name": "Eastern Harbour — Qaitbay Citadel (Pharos Island)",
        "shortName": "Qaitbay Citadel",
        "bp_type": "harbour_landing",
        "bp_type_label": "Harbour Landing",
        "coords": [29.8852, 31.2130],  # Wikipedia Citadel of Qaitbay
        "coord_source": "en.wikipedia.org/wiki/Citadel_of_Qaitbay (31.2130N 29.8852E)",
        "notes": "Departure area for private Eastern-Harbour excursion boats; candidate only.",
    },
    "bp-alex-bibliotheca-corniche": {
        "name": "Corniche / Bibliotheca Alexandrina waterfront",
        "shortName": "Bibliotheca / Corniche",
        "bp_type": "waterfront",
        "bp_type_label": "Waterfront",
        "coords": [29.90917, 31.20889],  # Wikipedia Bibliotheca Alexandrina
        "coord_source": "en.wikipedia.org/wiki/Bibliotheca_Alexandrina (31.20889N 29.90917E)",
        "notes": "Eastern Harbour south shore cultural waterfront; candidate only.",
    },
    "bp-alex-montaza-marina": {
        "name": "Montaza Palace marina (Montaza Bay)",
        "shortName": "Montaza marina",
        "bp_type": "marina",
        "bp_type_label": "Marina",
        # Nearest water to Montaza Palace facility (palace itself is on land)
        "coords": [30.0156, 31.2926],
        "facility_coords": [30.01556, 31.28861],
        "coord_source": (
            "Montaza Palace facility: Wikipedia Montaza Palace ~31.28861N 30.01556E; "
            "boarding anchor = nearest water north into Montaza Bay (candidate; not a surveyed berth)"
        ),
        "notes": "Existing ~$5 harbour boat rides; candidate only — no scheduled network boardings.",
    },
}

# Hand-spine waypoints keep paths in navigable water (local land mask QA)
CORRIDORS = [
    {
        "key": "alex-qaitbay|alex-bibliotheca",
        "from_bp": "bp-alex-qaitbay",
        "to_bp": "bp-alex-bibliotheca-corniche",
        "label": "Eastern-Harbour heritage loop: Qaitbay ↔ Bibliotheca/Corniche",
        "spine": [
            [29.892, 31.214],
            [29.900, 31.213],
            [29.905, 31.211],
        ],
    },
    {
        "key": "alex-bibliotheca|alex-montaza",
        "from_bp": "bp-alex-bibliotheca-corniche",
        "to_bp": "bp-alex-montaza-marina",
        "label": "Coastal Corniche hop: Eastern Harbour ↔ Montaza",
        "spine": [
            [29.91, 31.22],
            [29.93, 31.245],
            [29.96, 31.27],
            [29.99, 31.29],
            [30.01, 31.30],
        ],
    },
]


def densify(coords: list, step_km: float = 0.3) -> list:
    out = [list(coords[0])]
    for i in range(1, len(coords)):
        lon1, lat1 = coords[i - 1]
        lon2, lat2 = coords[i]
        dlon, dlat = lon2 - lon1, lat2 - lat1
        km = ((dlon * 111 * math.cos(math.radians(lat1))) ** 2 + (dlat * 111) ** 2) ** 0.5
        n = max(1, int(km / step_km))
        for j in range(1, n + 1):
            t = j / n
            out.append([lon1 + t * dlon, lat1 + t * dlat])
    return out


def bp_id_stable(key: str) -> str:
    """Keep human-readable stable ids for candidate BPs (not random hash)."""
    return key if key.startswith("bp-") else "bp-" + hashlib.md5(key.encode()).hexdigest()[:10]


def ensure_city(fbt: dict) -> None:
    cities = fbt.setdefault("city", [])
    if any((c.get("properties") or {}).get("id") == CITY_ID for c in cities):
        return
    cities.append(
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [29.9245, 31.2001]},  # city centroid (Alexandria)
            "properties": {
                "id": CITY_ID,
                "name": "Alexandria (Mediterranean)",
                "fullName": "Alexandria (Mediterranean waterfront)",
                "shortName": "Alexandria",
                "type": "city",
                "country": "Egypt",
                "region": "MENA",
                "cluster_id": CLUSTER_ID,
                "platform_class": "dual-platform",
                "tier_sort_key": 2,
                "coords_resolved": True,
                "coords_source": "city centroid near Eastern Harbour; BPs carry facility coords",
                "_candidate_city": True,
                "_candidate_at": NOW,
                "_candidate_reason": "Mediterranean waterfront candidate geography; no scheduled marine transit network with published boardings",
            },
        }
    )


def ensure_bps(fbt: dict) -> list[str]:
    pois = fbt.setdefault("poi", [])
    by_id = {(p.get("properties") or {}).get("id"): p for p in pois}
    minted = []
    for pid, meta in BPS.items():
        if pid in by_id:
            # refresh candidate flags / coords if already present
            props = by_id[pid].setdefault("properties", {})
            props["status"] = "candidate"
            props["_economics_hold"] = True
            props["_candidate_at"] = NOW
            continue
        feat = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": list(meta["coords"])},
            "properties": {
                "id": pid,
                "name": meta["name"],
                "fullName": meta["name"],
                "shortName": meta["shortName"],
                "type": "poi",
                "bp_type": meta["bp_type"],
                "bp_type_label": meta["bp_type_label"],
                "parent_city_id": CITY_ID,
                "cluster_id": CLUSTER_ID,
                "region": "MENA",
                "country": "Egypt",
                "status": "candidate",
                "confidence": "medium",
                "charging_status": "unknown",
                "operator": None,
                "source_url": meta["coord_source"],
                "coords_source": meta["coord_source"],
                "notes": meta["notes"],
                "_candidate_bp": True,
                "_candidate_at": NOW,
                "_economics_hold": True,
                "_economics_hold_reason": (
                    "Candidate geography only. No scheduled marine service with published "
                    "route-level boardings or comparable scheduled fare. Gates: (1) validated "
                    "facility coordinates (2) published boardings (3) comparable fare."
                ),
            },
        }
        if meta.get("facility_coords"):
            feat["properties"]["facility_coords"] = meta["facility_coords"]
            feat["properties"]["boarding_anchor_note"] = (
                "geometry uses nearest water to named facility; facility_coords retained for QA"
            )
        pois.append(feat)
        minted.append(pid)
    return minted


def ensure_cluster() -> None:
    doc = load_json(CLUSTERS_PATH)
    clusters = doc.get("clusters") or []
    for c in clusters:
        if c.get("cluster_id") == CLUSTER_ID:
            members = c.setdefault("member_city_ids", [])
            if CITY_ID not in members:
                members.append(CITY_ID)
                c["members_present"] = len(members)
            # do not rewrite Red Sea label into Mediterranean — keep note
            c["_alexandria_candidate_note"] = (
                "alexandria-egypt is a Mediterranean candidate member; economics stay null "
                "until scheduled network + boardings + fare gates pass. Not North Coast (Alamein)."
            )
            break
    save_json(CLUSTERS_PATH, doc)


def mint_corridors(routes: list, mask) -> list[dict]:
    existing = {((r.get("properties") or {}).get("id")) for r in routes}
    cities = {CITY_ID: "Alexandria"}
    minted = []
    for corr in CORRIDORS:
        fbp, tbp = corr["from_bp"], corr["to_bp"]
        rid = mint_route_id(fbp, tbp, tag="alexandria_candidate")
        if rid in existing:
            continue
        a = BPS[fbp]["coords"]
        b = BPS[tbp]["coords"]
        coords = densify([list(a)] + [list(p) for p in corr["spine"]] + [list(b)])
        land_km = interior_land_km(coords, mask)
        feat = make_route_feature(
            fbp,
            tbp,
            BPS[fbp]["shortName"],
            BPS[tbp]["shortName"],
            CITY_ID,
            CITY_ID,
            coords,
            cities,
            source="alexandria_candidate",
            land_km=land_km,
            cluster_id=CLUSTER_ID,
            cluster_city_id=CITY_ID,
        )
        props = feat["properties"]
        props["id"] = rid
        props["name"] = corr["label"]
        props["label"] = f"Alexandria: {corr['label']}"
        props["status"] = "candidate"
        props["_candidate_route"] = True
        props["_candidate_at"] = NOW
        props["_hand_waypoints_key"] = corr["key"]
        props["_hand_waypoints_at"] = NOW
        props["_geometry_source"] = "hand_waypoints+candidate_spine"
        props["demand"] = None
        props["fare"] = None
        props["_economics_hold"] = True
        props["_economics_hold_reason"] = (
            "Candidate corridor only. No route-level annual boardings or scheduled fare sourced. "
            "Not in grounded floor or any market total."
        )
        props["_qa_land_flag"] = land_km > LAND_GATE_KM
        routes.append(feat)
        existing.add(rid)
        minted.append(
            {
                "route_id": rid,
                "key": corr["key"],
                "label": corr["label"],
                "from_bp": fbp,
                "to_bp": tbp,
                "nm": round(path_length_km(coords) * NM_PER_KM, 2),
                "land_km": round(land_km, 4),
                "geom_pts": len(coords),
                "status": "pass" if land_km <= LAND_GATE_KM else "land_flag",
            }
        )
    return minted


def patch_partner_markets() -> None:
    """Mark Alexandria as candidate geography with minted IDs; economics stay null."""
    ladder_note = (
        "Candidate boarding points + corridors minted 2026-07-14 "
        "(bp-alex-qaitbay, bp-alex-bibliotheca-corniche, bp-alex-montaza-marina). "
        "Economics null until scheduled network boardings + fare gates. "
        "See ALEXANDRIA-CANDIDATE-GEOGRAPHY-RECEIPT-2026-07-14.json."
    )
    for path in (PARTNER_DC, PARTNER_PITCH):
        if not path.exists():
            continue
        doc = load_json(path)
        for m in doc.get("markets") or []:
            if not isinstance(m, dict):
                continue
            if m.get("id") not in ("egypt-red-sea",) and "egypt" not in str(m.get("id") or "").lower():
                continue
            ev = m.setdefault("_evidence_status", {})
            ev["alexandria"] = "candidate_geography_minted_economics_null"
            ev["alexandria_note"] = ladder_note
            # optional journeys_unlocked candidate rows (no economics)
            journeys = m.setdefault("journeys_unlocked", [])
            existing_labels = {
                (j.get("from_label") or j.get("from"), j.get("to_label") or j.get("to"))
                for j in journeys
                if isinstance(j, dict)
            }
            for corr in CORRIDORS:
                f_lab = BPS[corr["from_bp"]]["shortName"]
                t_lab = BPS[corr["to_bp"]]["shortName"]
                if (f_lab, t_lab) in existing_labels or (t_lab, f_lab) in existing_labels:
                    continue
                rid = mint_route_id(corr["from_bp"], corr["to_bp"], tag="alexandria_candidate")
                journeys.append(
                    {
                        "from": f_lab,
                        "to": t_lab,
                        "from_label": f_lab,
                        "to_label": t_lab,
                        "route_id": rid,
                        "_link_status": "candidate-geometry-only",
                        "_economics_hold": True,
                        "_economics_hold_reason": "Alexandria candidate; no published boardings or scheduled fare",
                        "narrative": (
                            f"Candidate waterfront link: {corr['label']}. "
                            "Not scheduled transit; economics held null."
                        ),
                    }
                )
        save_json(path, doc)


def patch_market_scope(minted_routes: list[dict]) -> None:
    if not MARKET_SCOPE.exists():
        return
    doc = load_json(MARKET_SCOPE)
    for row in doc.get("candidate_markets_null") or []:
        if row.get("city") == "Alexandria":
            row["status"] = "candidate"
            row["economics"] = None
            row["boarding_point_ids"] = list(BPS.keys())
            row["route_ids"] = [r["route_id"] for r in minted_routes]
            row["note"] = (
                "Candidate BPs + corridors minted 2026-07-14. Economics null until "
                "authoritative berth validation + published route-level boardings + comparable fare. "
                "Excludes North Coast (Alamein/Marassi)."
            )
    save_json(MARKET_SCOPE, doc)


def main() -> int:
    fbt = load_json(FBT_PATH)
    routes = route_features(load_json(ROUTES_PATH))
    mask = load_land_mask()

    ensure_city(fbt)
    bp_minted = ensure_bps(fbt)
    ensure_cluster()
    route_minted = mint_corridors(routes, mask)

    save_json(FBT_PATH, fbt)
    save_routes(ROUTES_PATH, routes)
    patch_partner_markets()
    patch_market_scope(route_minted)

    # hand waypoint catalog (PTA-style) for Alexandria candidate pairs
    wp_path = DC / "pta_hand_waypoints_alexandria_candidate.json"
    wp_doc = {
        "partner": "alexandria-candidate",
        "generated_at": NOW,
        "policy": "candidate only; economics null; no North Coast",
        "waypoints": {c["key"]: c["spine"] for c in CORRIDORS},
        "waypoint_notes": {
            c["key"]: c["label"] for c in CORRIDORS
        },
    }
    save_json(wp_path, wp_doc)

    receipt = {
        "receipt": "ALEXANDRIA-CANDIDATE-GEOGRAPHY-RECEIPT-2026-07-14",
        "generated_at": NOW,
        "spec": "GROK-SPEC-alexandria-candidate-geography-2026-07-14.md",
        "city_id": CITY_ID,
        "boarding_points_minted": bp_minted,
        "boarding_points_all": list(BPS.keys()),
        "corridors_minted": route_minted,
        "economics": None,
        "economics_policy": "null until three gates: validated berth coords, published boardings, comparable fare",
        "exclusions": [
            "Marina El Alamein / Porto Marina / Marassi (North Coast ~100km west)",
            "Cairo Nile / river product",
        ],
        "land_gate_km": LAND_GATE_KM,
        "qa": {
            "all_corridors_under_gate": all(
                r["land_km"] <= LAND_GATE_KM for r in route_minted
            )
            if route_minted
            else True,
        },
        "status": "candidate geography sealed; not partner-ready economics; no external release",
    }
    save_json(RECEIPT, receipt)
    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
