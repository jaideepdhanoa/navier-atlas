#!/usr/bin/env python3
"""Bind Bucket-C route mesh onto grab-thailand partner JSON + market cross-refs."""
from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PARTNER_SRC = ROOT / "partner-pitch/partners/grab-thailand.json"
PARTNER_DST = ROOT / "data-clean/partners/grab-thailand.json"
ROUTES = ROOT / "data-clean/ROUTES.json"

MARKET_BY_CITY = {
    "koh-samui-thailand": "koh_samui_gulf",
    "koh-phangan-thailand": "koh_samui_gulf",
    "koh-tao-thailand": "koh_samui_gulf",
    "pattaya-thailand": "bangkok",
    "koh-larn-thailand": "bangkok",
    "koh-chang-thailand": "bangkok",
    "krabi-thailand": "phuket_andaman",
    "koh-phi-phi-thailand": "phuket_andaman",
}

CONNECTED_BY_MARKET = {
    "koh_samui_gulf": ["koh-phangan-thailand", "koh-tao-thailand"],
    "phuket_andaman": ["krabi-thailand", "koh-phi-phi-thailand"],
    "bangkok": ["pattaya-thailand", "koh-larn-thailand", "koh-chang-thailand"],
}


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def route_features(obj):
    return obj if isinstance(obj, list) else obj.get("features", [])


def journey_from_route(props: dict) -> dict:
    dist = props.get("distance_nm", 0)
    platform = props.get("platform") or ("Quanta-LR" if dist >= 70 else "Pioneer II")
    return {
        "from": props.get("from_label") or props.get("from"),
        "to": props.get("to_label") or props.get("to"),
        "today": "Slow diesel ferries or speedboats on fixed schedules — weather-exposed, no in-app premium tier.",
        "with_navier": "An on-demand foiling hop — smooth, fast, near-silent, booked in Grab.",
        "distance_nm": dist,
        "platform": platform,
        "render": "solid",
        "range_status": "now",
        "from_node_id": props.get("from_city_id"),
        "to_node_id": props.get("to_city_id"),
        "from_bp_id": props.get("from"),
        "to_bp_id": props.get("to"),
        "route_id": props.get("id"),
        "_link_status": "linked-bucketC-thailand",
        "_link_source": "bucketC-thailand",
        "economics_status": "pending_demand_anchor",
    }


def patch_bangkok(market: dict) -> None:
    market["corridors_note"] = (
        "Chao Phraya river tier sealed (2 corridors). Gulf connected cities minted — "
        "Pattaya, Koh Larn and Koh Chang have Bucket-C BP routes; long Bangkok↔gulf gateway "
        "legs (~100–205nm) remain Quanta-LR roadmap (no demand record yet)."
    )
    for phase in market.get("phases", []):
        if phase.get("n") == 2:
            phase["featured_legs"] = [
                "Pattaya (Bali Hai) <-> Koh Larn (Na Ban)",
                "Koh Chang (Ao Sapparot) <-> Bang Bao",
            ]
            phase["narrative"] = "Connected gulf cities live on Bucket-C geometry; validate premium coastal corridors."
        if phase.get("n") == 3:
            phase["featured_legs"] = [
                "Bangkok <-> Pattaya / Koh Chang / Samui (Quanta-LR gateway — aspirational)",
            ]
            phase["narrative"] = "Quanta-LR gulf gateway from Bangkok once demand anchors land."


def patch_samui(market: dict) -> None:
    for phase in market.get("phases", []):
        if phase.get("n") == 3:
            phase["featured_legs"] = [
                "Bangrak <-> Thong Sala (Phangan)",
                "Samui north arc (Nathon / Maenam / Bophut)",
                "Samui <-> Koh Tao (Mae Haad)",
            ]
            phase["narrative"] = "Steady-state Gulf mesh on sealed Bucket-C routes."


def patch_phuket(market: dict) -> None:
    market["connected_cities"] = CONNECTED_BY_MARKET["phuket_andaman"]
    market["connected_cities_note"] = (
        "Krabi and Koh Phi Phi are minted connected cities with pier-exact Bucket-C routes "
        "(Klong Jilad ↔ Tonsai, Ao Nang ↔ Railay). Anchor corridors above use corridors.json "
        "labels; mesh below uses sealed BP endpoints."
    )
    for j in market.get("journeys_unlocked", []):
        dest = (j.get("to") or "").lower()
        if "krabi" in dest:
            j["to_node_id"] = "krabi-thailand"
            j["_connected_city_ref"] = "krabi-thailand"
        if "phi phi" in dest or "tonsai" in dest:
            j["to_node_id"] = "koh-phi-phi-thailand"
            j["_connected_city_ref"] = "koh-phi-phi-thailand"
    for phase in market.get("phases", []):
        if phase.get("n") == 2:
            phase["featured_legs"] = [
                "Klong Jilad (Krabi) <-> Tonsai (Phi Phi)",
                "Ao Nang <-> Railay East",
            ]


def main() -> int:
    routes = route_features(json.loads(ROUTES.read_text()))
    mesh = []
    by_market: dict[str, list] = {k: [] for k in ("koh_samui_gulf", "phuket_andaman", "bangkok")}

    for feat in routes:
        props = feat.get("properties", feat)
        if not props.get("_bucketC_thailand"):
            continue
        j = journey_from_route(props)
        mesh.append(j)
        fc = props.get("from_city_id")
        tc = props.get("to_city_id")
        for cid in (fc, tc):
            mk = MARKET_BY_CITY.get(cid)
            if mk:
                by_market[mk].append(j)

    partner = json.loads(PARTNER_SRC.read_text())
    # Strip prior Bucket-C mesh rows before re-link
    for market in partner.get("markets", []):
        market["journeys_unlocked"] = [
            j for j in market.get("journeys_unlocked", [])
            if j.get("_link_source") != "bucketC-thailand"
        ]
    partner["connected_city_mesh"] = mesh
    partner["connected_city_mesh_meta"] = {
        "bound_at": now_iso(),
        "route_count": len(mesh),
        "_link_source": "bucketC-thailand",
        "note": "Pier-exact BP↔BP routes; economics pending Tasklet demand anchors.",
    }

    for market in partner.get("markets", []):
        mid = market.get("id")
        if mid in CONNECTED_BY_MARKET:
            market["connected_cities"] = CONNECTED_BY_MARKET[mid]
        if mid == "koh_samui_gulf":
            patch_samui(market)
        if mid == "phuket_andaman":
            patch_phuket(market)
        if mid == "bangkok":
            patch_bangkok(market)
        # Append mesh journeys to market (dedupe by route_id)
        existing = {j.get("route_id") for j in market.get("journeys_unlocked", [])}
        for j in by_market.get(mid, []):
            if j["route_id"] not in existing:
                market.setdefault("journeys_unlocked", []).append(j)
                existing.add(j["route_id"])

    partner["expansion_lanes_exact_bind_only"] = [
        "Gulf + Andaman connected-city Bucket-C mesh linked on partner surface",
        "Cross-border: Phuket <-> Langkawi/Penang via Grab regional lane (not in grab-thailand)",
        "Bangkok gulf gateway long-legs (Bangkok↔Pattaya/Samui/Chang ~100–205nm) — aspirational",
    ]
    partner.setdefault("_provenance", {})["geometry"] = (
        f"15 anchor corridors + {len(mesh)} Bucket-C mesh routes linked; "
        "19 BPs gazetteer-validated; 8 cities (7 connected + Koh Larn)"
    )
    partner["proposal_status"] = "grok_sealed_geometry_and_mesh_linked"

    PARTNER_SRC.write_text(json.dumps(partner, indent=1) + "\n")
    shutil.copy2(PARTNER_SRC, PARTNER_DST)
    print(json.dumps({
        "mesh_routes": len(mesh),
        "samui_mesh": len(by_market["koh_samui_gulf"]),
        "phuket_mesh": len(by_market["phuket_andaman"]),
        "bangkok_mesh": len(by_market["bangkok"]),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())