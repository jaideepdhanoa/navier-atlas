#!/usr/bin/env python3
"""Abu Dhabi ITC Lane A — local mask, hand-waypoints, corridor repath, partner bind.

Implements GROK-SPEC-abu-dhabi-itc-domestic-routing-2026-06-30 against:
  - 10 PTA pairs (auh-d01..d08, abu-x01..x02)
  - Existing rn-* IDs from PTA-SEAL-RECEIPT (repath geometry; do not invent rids)
  - Island-aware ad_local_mask (Saadiyat/Yas/Reem/Lulu cores = land; channels = water)

Does not invent economics, demand, or undocumented regional links.
"""
from __future__ import annotations

import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-ad"))

from ad_local_mask import (  # noqa: E402
    densify,
    hav_km,
    interior_land_km,
    route_via_spine,
)

DC = ROOT / "data-clean"
ROUTES_PATH = DC / "ROUTES.json"
FBT_PATH = DC / "FEATURES_BY_TYPE.json"
WP_PATH = DC / "pta_hand_waypoints_abu_dhabi_itc.json"
ALLOW_PATH = DC / "route_water_allowlist.json"
PARTNER_PATH = DC / "partners/abu-dhabi-itc.json"
PITCH_PATH = ROOT / "partner-pitch/partners/abu-dhabi-itc.json"
UAE_WP = DC / "uae_hand_waypoints.json"
RECEIPT = ROOT / "handoff/partner-map-model/AD-ITC-LANE-A-GEOMETRY-RECEIPT-2026-07-13.json"

CITY = "abu-dhabi-uae"
CLUSTER = "uae"
NOW = datetime.now(timezone.utc).isoformat()
LAND_GATE_KM = 0.35

# Dossier anchors + existing PTA route ids (from PTA-SEAL-RECEIPT)
PAIRS = {
    "auh-d01": {
        "key": "ad-yas-bay|ad-al-bandar",
        "rid": "rn-2c00a6c6ca01",
        "from_node": "ad-yas-bay",
        "to_node": "ad-al-bandar",
        "from_label": "Yas Bay",
        "to_label": "Al Bandar (Al Raha Beach)",
        "from_coord": [54.604, 24.462],
        "to_coord": [54.606, 24.452],
        "bp_from": "bp-841b80ab3f",
        "bp_to": "bp-02f8bf8d25",
        "class": "existing_AD_Maritime_service",
        "spine": [
            [54.600, 24.460],
            [54.590, 24.456],
            [54.590, 24.450],
            [54.600, 24.449],
        ],
        "journey": True,
        "narrative": "The same Yas–Al Raha crossing, foiling-upgraded — quicker, quieter, low-wake on the dredged Yas Channel.",
    },
    "auh-d02": {
        "key": "ad-corniche-breakwater|ad-louvre-saadiyat",
        "rid": "rn-c91345d867d2",
        "from_node": "ad-corniche-breakwater",
        "to_node": "ad-louvre-saadiyat",
        "from_label": "Abu Dhabi Corniche / Breakwater (Marina Mall)",
        "to_label": "Louvre Abu Dhabi (Saadiyat Cultural District)",
        "from_coord": [54.318, 24.476],
        "to_coord": [54.398, 24.534],
        "bp_from": "bp-358af197cd",
        "bp_to": "bp-465b4a91a4",
        "class": "existing_AD_Maritime_service",
        "spine": [
            [54.320, 24.500],  # north into open Gulf (clear Lulu)
            [54.350, 24.530],
            [54.380, 24.545],
            [54.395, 24.545],
        ],
        "journey": True,
        "narrative": "A direct, low-wake foiling run from the Corniche around the headland to the Saadiyat Cultural District — not the road loop.",
    },
    "auh-d03": {
        "key": "ad-marsa-mina|ad-saadiyat-ferry-terminal",
        "rid": "rn-7586b9ef066c",
        "from_node": "ad-marsa-mina",
        "to_node": "ad-saadiyat-ferry-terminal",
        "from_label": "Marsa Mina (Mina Zayed)",
        "to_label": "Saadiyat Marina & Ferry Terminal",
        "from_coord": [54.378, 24.515],
        "to_coord": [54.422, 24.553],
        "bp_from": "bp-4c4f1e9a98",
        "bp_to": "bp-8cb3366589",
        "class": "existing_AD_Maritime_service",
        "spine": [
            [54.385, 24.528],  # passenger channel clear of commercial Mina
            [54.400, 24.540],
            [54.415, 24.548],
        ],
        "journey": False,
    },
    "auh-d04": {
        "key": "ad-al-qana-marina|ad-rabdan-marina",
        "rid": "rn-d1863ce79449",
        "from_node": "ad-al-qana-marina",
        "to_node": "ad-rabdan-marina",
        "from_label": "Al Qana Marina (ADNEC)",
        "to_label": "Rabdan Marina",
        "from_coord": [54.430, 24.418],
        "to_coord": [54.476, 24.414],
        "bp_from": "bp-e89cff48d8",
        "bp_to": "bp-73f12f88f9",
        "class": "existing_AD_Maritime_service",
        # Maqta dredged centreline — south of marinas through bridge spans
        "spine": [
            [54.432, 24.412],
            [54.445, 24.405],
            [54.460, 24.405],
            [54.472, 24.412],
        ],
        "journey": False,
        "displacement_only": True,
    },
    "auh-d05": {
        "key": "ad-reem-island|ad-corniche-breakwater",
        "rid": "rn-4868214bddb4",
        "from_node": "ad-reem-island",
        "to_node": "ad-corniche-breakwater",
        "from_label": "Reem Island",
        "to_label": "Abu Dhabi Corniche / Breakwater (Marina Mall)",
        "from_coord": [54.400, 24.500],
        "to_coord": [54.318, 24.476],
        "bp_from": "bp-3a0a68ad61",
        "bp_to": "bp-358af197cd",
        "class": "existing_AD_Maritime_service",
        "spine": [
            [54.405, 24.518],  # north of Reem into open channel
            [54.385, 24.530],
            [54.350, 24.528],
            [54.325, 24.505],
            [54.320, 24.490],
        ],
        "journey": True,
        "narrative": "A direct water line relieving the Reem bridges into the Corniche core.",
    },
    "auh-d06": {
        "key": "ad-eastern-mangroves|ad-yas-marina",
        "rid": "rn-675621620739",
        "from_node": "ad-eastern-mangroves",
        "to_node": "ad-yas-marina",
        "from_label": "Eastern Mangroves",
        "to_label": "Yas Marina",
        "from_coord": [54.452, 24.454],
        "to_coord": [54.603, 24.470],
        "bp_from": "bp-a91d63d138",
        "bp_to": "bp-713c426a41",
        "class": "existing_AD_Maritime_service",
        "spine": [
            [54.470, 24.458],
            [54.510, 24.462],
            [54.550, 24.468],
            [54.580, 24.470],
            [54.595, 24.468],
        ],
        "journey": True,
        "narrative": "A quiet, low-wake run along the mangrove channel fairway to Yas — not across the flats.",
    },
    "auh-d07": {
        "key": "ad-saadiyat-ferry-terminal|ad-al-aliah",
        "rid": "rn-8f24df55b0c4",
        "from_node": "ad-saadiyat-ferry-terminal",
        "to_node": "ad-al-aliah",
        "from_label": "Saadiyat Marina & Ferry Terminal",
        "to_label": "Al Aliah Island",
        "from_coord": [54.422, 24.553],
        "to_coord": [54.460, 24.590],
        "bp_from": "bp-8cb3366589",
        "bp_to": "bp-6f2ca0ee0e",
        "class": "existing_AD_Maritime_service",
        "spine": [
            [54.430, 24.565],
            [54.445, 24.580],
        ],
        "journey": False,
    },
    "auh-d08": {
        "key": "ad-hudayriat|ad-corniche-breakwater",
        "rid": "rn-78832aa16e03",
        "from_node": "ad-hudayriat",
        "to_node": "ad-corniche-breakwater",
        "from_label": "Hudayriat Island",
        "to_label": "Abu Dhabi Corniche / Breakwater (Marina Mall)",
        "from_coord": [54.320, 24.400],
        "to_coord": [54.318, 24.476],
        "bp_from": "bp-7ef1aca763",
        "bp_to": "bp-358af197cd",
        "class": "existing_AD_Maritime_service",
        "spine": [
            [54.300, 24.405],  # west breakwater exit
            [54.290, 24.430],
            [54.300, 24.455],
            [54.312, 24.468],
        ],
        "journey": False,
    },
    "abu-x01": {
        "key": "ad-corniche-breakwater|ad-al-muneera",
        "rid": "rn-e50259014a24",
        "from_node": "ad-corniche-breakwater",
        "to_node": "ad-al-muneera",
        "from_label": "Abu Dhabi Corniche / Breakwater (Marina Mall)",
        "to_label": "Al Muneera (Al Raha Beach)",
        "from_coord": [54.318, 24.476],
        "to_coord": [54.596, 24.451],
        "bp_from": "bp-358af197cd",
        "bp_to": "bp-885f4bc4f7",
        "class": "WETA_style_hub_spoke_extension",
        "spine": [
            [54.320, 24.520],
            [54.400, 24.570],  # north Gulf express (clear Saadiyat core)
            [54.500, 24.570],
            [54.560, 24.520],
            [54.590, 24.480],
            [54.595, 24.455],
        ],
        "journey": False,
        "not_core": True,
    },
    "abu-x02": {
        "key": "ad-corniche-breakwater|ad-al-zeina",
        "rid": "rn-8e500e198d6a",
        "from_node": "ad-corniche-breakwater",
        "to_node": "ad-al-zeina",
        "from_label": "Abu Dhabi Corniche / Breakwater (Marina Mall)",
        "to_label": "Al Zeina (Al Raha Beach)",
        "from_coord": [54.318, 24.476],
        "to_coord": [54.617, 24.452],
        "bp_from": "bp-358af197cd",
        "bp_to": "bp-4c40a43f06",
        "class": "WETA_style_hub_spoke_extension",
        "spine": [
            [54.320, 24.520],
            [54.400, 24.570],
            [54.500, 24.570],
            [54.560, 24.520],
            [54.590, 24.480],
            [54.600, 24.460],
            [54.610, 24.452],
        ],
        "journey": False,
        "not_core": True,
    },
}


def path_nm(coords: list) -> float:
    return round(sum(hav_km((coords[i][0], coords[i][1]), (coords[i + 1][0], coords[i + 1][1])) for i in range(len(coords) - 1)) / 1.852, 2)


def ensure_bp(fbt: dict, bp_id: str, name: str, coords: list[float], node: str) -> None:
    """Mint PTA boarding point into FBT if missing."""
    for _t, feats in fbt.items():
        for f in feats or []:
            if (f.get("properties") or {}).get("id") == bp_id:
                # refresh coords/name if orphaned
                p = f["properties"]
                p["name"] = p.get("name") or name
                p["label"] = p.get("label") or name
                p["parent_city_id"] = CITY
                p["_pta_abu-dhabi-itc"] = True
                p["_pta_node"] = node
                if not (f.get("geometry") or {}).get("coordinates"):
                    f["geometry"] = {"type": "Point", "coordinates": coords}
                return
    bucket = "poi"
    fbt.setdefault(bucket, [])
    fbt[bucket].append(
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": list(coords)},
            "properties": {
                "id": bp_id,
                "name": name,
                "label": name,
                "parent_city_id": CITY,
                "city_id": CITY,
                "relevance": "show",
                "_pta_abu-dhabi-itc": True,
                "_pta_node": node,
                "_minted_at": NOW,
                "_mint_source": "ad_itc_lane_a_2026_07_13",
            },
        }
    )


def main() -> int:
    fbt = json.loads(FBT_PATH.read_text())
    routes = json.loads(ROUTES_PATH.read_text())
    by_id = {(f.get("properties") or {}).get("id"): f for f in routes}

    receipt = {
        "at": NOW,
        "lane": "A",
        "partner": "abu-dhabi-itc",
        "land_gate_km": LAND_GATE_KM,
        "local_mask": "scripts/grok-ad/ad_local_mask.py",
        "corridors": [],
        "fails": [],
        "bps_ensured": [],
        "partner_journeys": 0,
        "notes": [],
    }

    # Ensure all PTA BPs exist
    seen_bp = set()
    for meta in PAIRS.values():
        for side, lab, coord, node in (
            ("bp_from", meta["from_label"], meta["from_coord"], meta["from_node"]),
            ("bp_to", meta["to_label"], meta["to_coord"], meta["to_node"]),
        ):
            bid = meta[side]
            if bid in seen_bp:
                continue
            ensure_bp(fbt, bid, lab, coord, node)
            seen_bp.add(bid)
            receipt["bps_ensured"].append(bid)

    wp_doc = {
        "partner": "abu-dhabi-itc",
        "generated_at": NOW,
        "local_mask": "scripts/grok-ad/ad_local_mask.py",
        "policy": {
            "empty_array_forbidden_without_note": True,
            "interior_land_km_zero_not_sufficient_without_channel_qa": True,
            "local_mask_gate_km": LAND_GATE_KM,
            "required_cases": [
                "Yas Channel / Al Raha dredged hop",
                "Lulu west fairway (Corniche ↔ Saadiyat)",
                "Mina Zayed passenger channel",
                "Khor Al Maqta / Mussafah centreline (displacement)",
                "Reem north channel to Corniche",
                "Eastern Mangroves lagoon fairway to Yas",
                "Hudayriat west breakwater exit",
                "Coastal navigation lane (Corniche ↔ Al Raha hub-spokes)",
            ],
        },
        "waypoints": {},
        "waypoint_notes": {},
    }

    allow = json.loads(ALLOW_PATH.read_text())
    allow_ids = set(allow.get("ids") or [])
    uae_pairs = []
    if UAE_WP.exists():
        uae_doc = json.loads(UAE_WP.read_text())
        uae_pairs = list(uae_doc.get("pairs") or [])
    else:
        uae_doc = {"pairs": [], "generated_at": NOW}

    journeys = []

    for pair_id, meta in PAIRS.items():
        rid = meta["rid"]
        feat = by_id.get(rid)
        if not feat:
            receipt["fails"].append({"pair_id": pair_id, "rid": rid, "reason": "route_missing"})
            continue

        fr_c = list(meta["from_coord"])
        to_c = list(meta["to_coord"])
        spine = meta["spine"]
        # Prefer densified spines; A* fill only if residual land remains
        coords = route_via_spine(fr_c, to_c, spine, use_astar=False)
        if interior_land_km(coords) > LAND_GATE_KM:
            coords = route_via_spine(fr_c, to_c, spine, use_astar=True)
        land = interior_land_km(coords)
        nm = path_nm(coords)

        p = feat.get("properties") or {}
        feat["geometry"] = {"type": "LineString", "coordinates": coords}
        p["from"] = meta["bp_from"]
        p["to"] = meta["bp_to"]
        p["from_node"] = meta["bp_from"]
        p["to_node"] = meta["bp_to"]
        p["from_label"] = meta["from_label"]
        p["to_label"] = meta["to_label"]
        p["label"] = f"Abu Dhabi: {meta['from_label']} → {meta['to_label']}"
        p["distance_nm"] = nm
        p["from_city_id"] = CITY
        p["to_city_id"] = CITY
        p["from_city"] = "Abu Dhabi"
        p["to_city"] = "Abu Dhabi"
        p["cluster_id"] = CLUSTER
        p["_pta_abu-dhabi-itc"] = True
        p["_pta_pair_id"] = pair_id
        p["_pta_node_from"] = meta["from_node"]
        p["_pta_node_to"] = meta["to_node"]
        p["_weta_service_class"] = meta["class"]  # service class tag (not WETA)
        p["_ad_service_class"] = meta["class"]
        p["_land_km_interior_local_mask"] = round(land, 4)
        p["_land_km_interior"] = round(land, 4)
        p["_land_km_gate"] = LAND_GATE_KM
        p["_hand_waypoints_at"] = NOW
        p["_hand_waypoints_key"] = meta["key"]
        p["_local_mask"] = "ad_local_mask"
        p["_coastal_geometry"] = True
        if meta.get("displacement_only"):
            p["_displacement_only"] = True
            p["_foil_ok"] = False
            p["_hand_waypoints_case"] = "Khor Al Maqta dredged centreline — displacement / no-foil under low bridges"
        else:
            p["_hand_waypoints_case"] = "AD channel / island-exclusion corridor"
        if meta.get("not_core"):
            p["_hub_spoke_extension"] = True
        feat["properties"] = p

        status = "pass" if land <= LAND_GATE_KM else "fail_land"
        if status != "pass":
            receipt["fails"].append({"pair_id": pair_id, "rid": rid, "land_km": round(land, 4), "nm": nm})
        receipt["corridors"].append(
            {
                "pair_id": pair_id,
                "route_id": rid,
                "key": meta["key"],
                "class": meta["class"],
                "nm": nm,
                "land_km_local": round(land, 4),
                "status": status,
                "geom_pts": len(coords),
                "spine_pts": len(spine),
            }
        )
        allow_ids.add(rid)

        wp_doc["waypoints"][meta["key"]] = spine
        wp_doc["waypoint_notes"][meta["key"]] = {
            "status": "hand_reviewed_local_mask",
            "at": NOW,
            "pair_id": pair_id,
            "land_km_local": round(land, 4),
            "gate_km": LAND_GATE_KM,
            "case": p.get("_hand_waypoints_case"),
        }

        # extend uae_hand_waypoints catalog
        uae_pairs.append(
            {
                "from": meta["bp_from"],
                "to": meta["bp_to"],
                "waypoints": spine,
                "source": "ad_itc_lane_a_2026_07_13",
                "pair_id": pair_id,
            }
        )

        if meta.get("journey"):
            # Partner-page display labels (match prior copy)
            disp = {
                "auh-d01": ("Yas Bay", "Al Bandar (Al Raha Beach)"),
                "auh-d02": ("Abu Dhabi Corniche", "Louvre Abu Dhabi (Saadiyat)"),
                "auh-d05": ("Reem Island", "Abu Dhabi Corniche"),
                "auh-d06": ("Eastern Mangroves", "Yas Marina"),
            }.get(pair_id, (meta["from_label"], meta["to_label"]))
            journeys.append(
                {
                    "from": disp[0],
                    "to": disp[1],
                    "today": "Today: road loop, congested bridges, or slower water-taxi where available.",
                    "with_navier": meta.get("narrative")
                    or f"Foiling tier on the {disp[0]} ↔ {disp[1]} domestic corridor.",
                    "platform": "Pioneer II",
                    "distance_nm": nm,
                    "from_node_id": meta["from_node"],
                    "to_node_id": meta["to_node"],
                    "route_id": rid,
                    "route_ids": [rid],
                    "_link_source": "grok/ad_itc_lane_a_2026_07_13",
                    "_pta_bound_at": NOW,
                    "_ad_service_class": meta["class"],
                    "display": "map",
                    "_link_kind": "bound-route",
                    "economics_status": "bound",
                    "render": "live-solid",
                }
            )

    receipt["partner_journeys"] = len(journeys)

    for partner_path in (PARTNER_PATH, PITCH_PATH):
        if not partner_path.exists():
            continue
        partner = json.loads(partner_path.read_text())
        partner["journeys_unlocked"] = journeys
        partner["_ad_itc_lane_a_at"] = NOW
        partner["_ad_local_mask"] = "ad_local_mask"
        partner_path.write_text(json.dumps(partner, indent=2, ensure_ascii=False) + "\n")

    # Deduplicate uae hand waypoints by from|to
    dedup = {}
    for item in uae_pairs:
        k = (item.get("from"), item.get("to"))
        dedup[k] = item
    uae_doc["pairs"] = list(dedup.values())
    uae_doc["ad_itc_lane_a_at"] = NOW

    allow["ids"] = sorted(allow_ids)
    allow.setdefault("_meta", {})["ad_itc_lane_a_at"] = NOW

    FBT_PATH.write_text(json.dumps(fbt, ensure_ascii=False, separators=(",", ":")) + "\n")
    ROUTES_PATH.write_text(json.dumps(routes, ensure_ascii=False, separators=(",", ":")) + "\n")
    WP_PATH.write_text(json.dumps(wp_doc, indent=2, ensure_ascii=False) + "\n")
    ALLOW_PATH.write_text(json.dumps(allow, ensure_ascii=False, separators=(",", ":")) + "\n")
    UAE_WP.write_text(json.dumps(uae_doc, ensure_ascii=False, indent=2) + "\n")

    # Also update handoff PTA waypoints mirror
    handoff_wp = ROOT / "handoff/partner-map-model/PTA-HAND-WAYPOINTS-abu-dhabi-itc.json"
    handoff_wp.write_text(
        json.dumps(
            {
                "partner": "abu-dhabi-itc",
                "generated_at": NOW,
                "local_mask": "scripts/grok-ad/ad_local_mask.py",
                "solved": [
                    {"pair_id": c["pair_id"], "route_id": c["route_id"], "waypoints": c["spine_pts"], "land_km_local": c["land_km_local"], "status": c["status"]}
                    for c in receipt["corridors"]
                ],
                "failed": receipt["fails"],
                "waypoints": wp_doc["waypoints"],
            },
            indent=2,
        )
        + "\n"
    )

    pass_n = sum(1 for c in receipt["corridors"] if c["status"] == "pass")
    receipt["summary"] = {
        "corridors": len(receipt["corridors"]),
        "pass": pass_n,
        "fail": len(receipt["corridors"]) - pass_n,
        "partner_ready": pass_n == len(receipt["corridors"]) and pass_n > 0 and len(journeys) >= 4,
    }
    receipt["notes"] = [
        "Local mask: island land cores + dredged channel water + terminal aprons.",
        "UAE overlay alone is insufficient — Saadiyat/Yas cores were false-water.",
        "Maqta leg marked displacement_only (low bridges).",
        "Hub-spoke abu-x01/x02 repathed on coastal navigation lane; not inventing new commitments.",
    ]
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))
    return 0 if receipt["summary"]["partner_ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
