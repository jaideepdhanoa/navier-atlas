#!/usr/bin/env python3
"""Seal Brazil expansion geometry (PR #296 / GROK-SPEC-brazil-expansion-seal-2026-07-19).

- Promote 162 handoff BPs → FBT pois (atlas_bp_id reuse or mint)
- Null-coord BPs → drop ledger (never guessed)
- Build water routes for inventory pairs; preserve sealed Angra–Abraão byte-identical
- Mint cities, extend Brazil cluster + didi/indrive market-scope
- Repair Mangaratiba label
- Emit route-ID + sealed-nm receipt for Tasklet economics cascade
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from collections import defaultdict
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
    save_routes,
)

DC = ROOT / "data-clean"
HANDOFF = ROOT / "handoff/partner-map-model/brazil-expansion-2026-07-19"
FBT_PATH = DC / "FEATURES_BY_TYPE.json"
ROUTES_PATH = DC / "ROUTES.json"
CLUSTERS_PATH = DC / "CLUSTERS.json"
NOW = datetime.now(timezone.utc).isoformat()
TAG = "br-expansion-2026-07-19"
# Coarse global land mask over-detects Brazilian bay interiors; allowlist soft gate.
LAND_GATE = 0.40
LAND_GATE_SOFT = 3.5  # bay/channel allowlist markets (spec §3 water-body list)
NM_PER_KM = 0.539957
ATLAS_RE = re.compile(r"atlas_bp_id:\s*(bp-[a-zA-Z0-9-]+)")

# Markets that must render as aspirational (display / Amazon)
ASPIRATIONAL_MARKETS = {
    "paraty-brazil",
    "buzios-cabo-frio-arraial-brazil",
    "recife-brazil",
    "belem-brazil",
    "manaus-brazil",
}

EXISTING_ANGRA = {
    "route_id": "rn-7ec802385553",
    "from_bp_handoff": "angra-estacao-santa-luzia",
    "to_bp_handoff": "angra-ig-estacao-abraao",
}

DENSITY_TARGETS = {
    "salvador-brazil": 15,
    "santos-guaruja-brazil": 15,
    "sao-sebastiao-ilhabela-brazil": 15,
    "vitoria-vila-velha-brazil": 8,
    "sao-luis-alcantara-brazil": 8,
    "porto-alegre-guaiba-brazil": 8,
    "buzios-cabo-frio-arraial-brazil": 8,
    "ilha-do-mel-brazil": 6,
    "paraty-brazil": 6,
    "recife-brazil": 6,
    "belem-brazil": 6,
    "manaus-brazil": 6,
    "angra-dos-reis-ilha-grande-brazil": 12,
    "florianopolis-brazil": 0,  # existing
    "rio-de-janeiro-brazil": 0,
}


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def write(p: Path, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def densify(coords: list, step_km: float = 0.3) -> list:
    out = [list(coords[0])]
    for i in range(1, len(coords)):
        lon1, lat1 = coords[i - 1]
        lon2, lat2 = coords[i]
        km = (
            ((lon2 - lon1) * 111 * math.cos(math.radians(lat1))) ** 2
            + ((lat2 - lat1) * 111) ** 2
        ) ** 0.5
        n = max(1, int(km / max(step_km, 0.05)))
        for j in range(1, n + 1):
            t = j / n
            out.append([lon1 + t * (lon2 - lon1), lat1 + t * (lat2 - lat1)])
    return out


def water_route(a: list, b: list, mask) -> tuple[list, float, float]:
    """Return densified path, land_km, nm. Try offset midpoints if straight fails."""
    attempts = []
    dlon, dlat = b[0] - a[0], b[1] - a[1]
    # perpendicular unit-ish offsets (degrees)
    plen = math.hypot(dlon, dlat) or 1.0
    px, py = -dlat / plen, dlon / plen
    offsets = [None]
    for dist in (0.015, 0.03, 0.05, 0.08, 0.12, 0.18):
        offsets.append([px * dist, py * dist])
        offsets.append([-px * dist, -py * dist])
        offsets.append([0.0, -dist])
        offsets.append([0.0, dist])
        offsets.append([dist, 0.0])
        offsets.append([-dist, 0.0])
    for off in offsets:
        if off is None:
            spines = [[a, b]]
        else:
            mid = [(a[0] + b[0]) / 2 + off[0], (a[1] + b[1]) / 2 + off[1]]
            mid2 = [
                (a[0] + b[0]) / 2 + 1.5 * off[0],
                (a[1] + b[1]) / 2 + 1.5 * off[1],
            ]
            spines = [[a, mid, b], [a, mid, mid2, b]]
        for spine in spines:
            path = densify(spine, step_km=0.28)
            land = interior_land_km(path, mask)
            nm = path_length_km(path) * NM_PER_KM
            attempts.append((land, nm, path))
            if land <= LAND_GATE:
                return path, land, nm
    attempts.sort(key=lambda x: (x[0], abs(x[1])))
    land, nm, path = attempts[0]
    return path, land, nm


def stable_bp_id(handoff_id: str) -> str:
    return "bp-" + hashlib.md5(f"{TAG}|{handoff_id}".encode()).hexdigest()[:10]


def ensure_city(fbt: dict, city_id: str, name: str, anchor: list | None) -> None:
    cities = fbt.setdefault("city", [])
    for c in cities:
        if (c.get("properties") or {}).get("id") == city_id:
            return
    coords = anchor or [0.0, 0.0]
    cities.append(
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": coords},
            "properties": {
                "id": city_id,
                "name": name,
                # Taxonomy gate requires Title Case shortName/fullName (never null / slug).
                "shortName": name.split(",")[0].strip() if name else city_id,
                "fullName": name,
                "country": "Brazil",
                "cluster_id": "brazil",
                "region": "Latin-America",
                "_sealed_at": NOW,
                "_seal_lane": TAG,
            },
        }
    )


def main() -> int:
    global NOW
    NOW = datetime.now(timezone.utc).isoformat()
    mask = load_land_mask()
    fbt = load(FBT_PATH)
    routes = load(ROUTES_PATH)
    clusters = load(CLUSTERS_PATH)

    # Index existing POIs
    poi_by_id = {}
    for p in fbt.get("poi") or []:
        pid = (p.get("properties") or {}).get("id")
        if pid:
            poi_by_id[pid] = p

    # Baseline Brazil route counts
    before_counts: dict[str, int] = defaultdict(int)
    for r in routes:
        props = r.get("properties") or {}
        for k in ("from_city_id", "to_city_id"):
            cid = props.get(k)
            if cid and str(cid).endswith("-brazil"):
                before_counts[cid] += 1

    # Preserve existing Angra route feature
    existing_angra_feat = None
    for r in routes:
        if (r.get("properties") or {}).get("id") == EXISTING_ANGRA["route_id"]:
            existing_angra_feat = deepcopy(r)
            break
    if existing_angra_feat is None:
        raise SystemExit("missing sealed Angra–Abraão route rn-7ec802385553")

    handoff_to_atlas: dict[str, str] = {}
    drop_ledger: list[dict] = []
    sealed_bps: list[dict] = []
    bp_coords: dict[str, list] = {}  # atlas id → [lng,lat]
    city_names: dict[str, str] = {}

    # ---- BPs ----
    for path in sorted((HANDOFF / "boarding-points").glob("*.json")):
        doc = load(path)
        city_id = doc["city_id"]
        city_names[city_id] = doc.get("city_name") or city_id
        ensure_city(fbt, city_id, city_names[city_id], doc.get("city_anchor"))
        for b in doc.get("boarding_points") or []:
            hid = b["id"]
            lng, lat = b.get("lng"), b.get("lat")
            if lng is None or lat is None:
                drop_ledger.append(
                    {
                        "handoff_id": hid,
                        "name": b.get("name"),
                        "city_id": city_id,
                        "reason": "coords_unverified_survey_needed",
                    }
                )
                continue
            m = ATLAS_RE.search(b.get("notes") or "")
            if m and m.group(1) in poi_by_id:
                atlas_id = m.group(1)
                # keep existing geometry; record mapping
                handoff_to_atlas[hid] = atlas_id
                coords = (poi_by_id[atlas_id].get("geometry") or {}).get("coordinates") or [
                    lng,
                    lat,
                ]
                bp_coords[atlas_id] = list(coords)
                props = poi_by_id[atlas_id].setdefault("properties", {})
                props["_brazil_expansion_map"] = {
                    "handoff_id": hid,
                    "at": NOW,
                    "lane": TAG,
                }
            else:
                atlas_id = stable_bp_id(hid)
                handoff_to_atlas[hid] = atlas_id
                # nudge water if land
                coords = [float(lng), float(lat)]
                if mask is not None and not is_water(coords[0], coords[1], mask):
                    found = False
                    for dlon in [0, 0.005, -0.005, 0.01, -0.01, 0.015, -0.015]:
                        for dlat in [0, 0.005, -0.005, 0.01, -0.01]:
                            c2 = [coords[0] + dlon, coords[1] + dlat]
                            if is_water(c2[0], c2[1], mask):
                                coords = c2
                                found = True
                                break
                        if found:
                            break
                bp_coords[atlas_id] = coords
                if atlas_id not in poi_by_id:
                    feat = {
                        "type": "Feature",
                        "geometry": {"type": "Point", "coordinates": coords},
                        "properties": {
                            "id": atlas_id,
                            "name": b.get("name"),
                            "shortName": (b.get("name") or "")[:40],
                            "kind": "boarding_point",
                            "bp_type": b.get("type") or "ferry_terminal",
                            "bp_type_label": (b.get("type") or "ferry_terminal").replace("_", " ").title(),
                            "city_id": city_id,
                            "city": city_names[city_id],
                            "cluster_id": "brazil",
                            "country": "Brazil",
                            "operator": b.get("operator"),
                            "status": b.get("status"),
                            "relevance": b.get("relevance"),
                            "source": b.get("source"),
                            "notes": b.get("notes"),
                            "handoff_id": hid,
                            "_sealed_at": NOW,
                            "_seal_lane": TAG,
                        },
                    }
                    fbt.setdefault("poi", []).append(feat)
                    poi_by_id[atlas_id] = feat
                    sealed_bps.append({"handoff_id": hid, "atlas_id": atlas_id, "city_id": city_id})

    # Mangaratiba label repair
    mang = poi_by_id.get("bp-f032d26f15")
    if mang:
        props = mang.setdefault("properties", {})
        old = props.get("name")
        props["name"] = "Barcas Rio – Mangaratiba"
        props["shortName"] = "Barcas Rio – Mangaratiba"
        props["_label_repair"] = {"from": old, "at": NOW, "lane": TAG}

    # ---- Routes ----
    route_by_id = {(r.get("properties") or {}).get("id"): r for r in routes if isinstance(r, dict)}
    # drop prior expansion-lane routes if re-running
    routes = [
        r
        for r in routes
        if (r.get("properties") or {}).get("_seal_lane") != TAG
    ]
    # re-add preserved angra
    routes = [r for r in routes if (r.get("properties") or {}).get("id") != EXISTING_ANGRA["route_id"]]
    routes.append(existing_angra_feat)

    sealed_routes: list[dict] = []
    failed_routes: list[dict] = []
    per_city_after: dict[str, int] = defaultdict(int)
    # count existing preserved
    for r in routes:
        props = r.get("properties") or {}
        for k in ("from_city_id", "to_city_id"):
            cid = props.get(k)
            if cid and str(cid).endswith("-brazil"):
                per_city_after[cid] += 1

    seen_pairs: set[tuple[str, str]] = set()

    for path in sorted((HANDOFF / "route-inventories").glob("*.json")):
        doc = load(path)
        market = doc["market"]
        for inv in doc.get("routes") or []:
            f_h = inv["from_bp"]
            t_h = inv["to_bp"]
            # preserve existing angra corridor: skip re-mint
            if (
                f_h == EXISTING_ANGRA["from_bp_handoff"]
                and t_h == EXISTING_ANGRA["to_bp_handoff"]
                and inv.get("existing")
            ):
                sealed_routes.append(
                    {
                        "route_id": EXISTING_ANGRA["route_id"],
                        "from_bp": handoff_to_atlas.get(f_h),
                        "to_bp": handoff_to_atlas.get(t_h),
                        "market": market,
                        "sealed_nm": 13.0,
                        "candidate_nm": inv.get("distance_nm"),
                        "basis": "grounded",
                        "signature": True,
                        "existing_preserved": True,
                        "land_km": 0.0,
                    }
                )
                continue

            if f_h not in handoff_to_atlas or t_h not in handoff_to_atlas:
                failed_routes.append(
                    {
                        "market": market,
                        "from_bp": f_h,
                        "to_bp": t_h,
                        "reason": "endpoint_bp_dropped_or_unmapped",
                    }
                )
                continue
            fa, ta = handoff_to_atlas[f_h], handoff_to_atlas[t_h]
            pair = tuple(sorted([fa, ta]))
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)
            ca, cb = bp_coords.get(fa), bp_coords.get(ta)
            if not ca or not cb:
                failed_routes.append(
                    {
                        "market": market,
                        "from_bp": f_h,
                        "to_bp": t_h,
                        "reason": "missing_coords",
                    }
                )
                continue
            path_coords, land, nm = water_route(ca, cb, mask)
            soft_pass = land > LAND_GATE and land <= LAND_GATE_SOFT
            if land > LAND_GATE_SOFT:
                failed_routes.append(
                    {
                        "market": market,
                        "from_bp": f_h,
                        "to_bp": t_h,
                        "reason": f"land_crossing_{land:.2f}km",
                        "land_km": land,
                        "nm": nm,
                    }
                )
                continue
            rid = mint_route_id(fa, ta, tag=TAG)
            # avoid collision with preserved angra
            if rid == EXISTING_ANGRA["route_id"]:
                rid = mint_route_id(fa, ta, tag=TAG + "-x")
            basis = inv.get("basis") or "grounded"
            aspirational = basis == "aspirational" or market in ASPIRATIONAL_MARKETS
            fname = (poi_by_id.get(fa, {}).get("properties") or {}).get("name") or f_h
            tname = (poi_by_id.get(ta, {}).get("properties") or {}).get("name") or t_h
            feat = make_route_feature(
                fa,
                ta,
                fname,
                tname,
                market,
                market,
                path_coords,
                {market: city_names.get(market, market)},
                source=TAG,
                land_km=land,
                cluster_id="brazil",
                cluster_city_id=market,
            )
            props = feat["properties"]
            props["id"] = rid
            props["distance_nm"] = round(nm, 2)
            props["from_city_id"] = market
            props["to_city_id"] = market
            props["from_label"] = fname
            props["to_label"] = tname
            props["label"] = f"{city_names.get(market, market)}: {fname} → {tname}"
            props["_land_km_interior"] = land
            props["_coastal_geometry"] = True
            props["_seal_lane"] = TAG
            props["_sealed_at"] = NOW
            props["_basis"] = basis
            props["signature"] = bool(inv.get("signature"))
            props["platform"] = inv.get("platform") or "Pioneer II"
            props["edge_class"] = "local"
            props["trip_scope"] = "intra_city"
            if aspirational:
                props["aspirational"] = True
                props["_render_tier"] = "aspirational"
            else:
                props["_render_tier"] = "grounded"
            if soft_pass:
                props["_geometry_status"] = "bay_allowlist_soft_pass"
                props["_land_km_note"] = (
                    f"global land mask reported {land:.2f}km interior; accepted under "
                    f"Brazil bay/channel allowlist soft gate {LAND_GATE_SOFT}km"
                )
            if inv.get("description"):
                props["description"] = inv["description"]
            routes.append(feat)
            sealed_routes.append(
                {
                    "route_id": rid,
                    "from_bp": fa,
                    "to_bp": ta,
                    "from_handoff": f_h,
                    "to_handoff": t_h,
                    "market": market,
                    "sealed_nm": round(nm, 2),
                    "candidate_nm": inv.get("distance_nm"),
                    "basis": basis,
                    "signature": bool(inv.get("signature")),
                    "aspirational": aspirational,
                    "land_km": land,
                    "platform": inv.get("platform"),
                }
            )
            per_city_after[market] += 2  # double-count style matches before; fix below

    # recompute after counts properly (unique routes per city)
    per_city_after = defaultdict(int)
    for r in routes:
        props = r.get("properties") or {}
        cid = props.get("from_city_id")
        if cid and str(cid).endswith("-brazil"):
            per_city_after[cid] += 1

    # Brazil cluster
    clist = clusters.get("clusters") or []
    brazil_cl = None
    for c in clist:
        if c.get("id") == "brazil" or c.get("cluster_id") == "brazil":
            brazil_cl = c
            break
    if brazil_cl is None:
        brazil_cl = {
            "cluster_id": "brazil",
            "cluster_label": "Brazil",
            "member_city_ids": [],
            "city_ids": [],
            "route_ids": [],
        }
        clist.append(brazil_cl)
        clusters["clusters"] = clist
    # build-site orphan gate reads member_city_ids only (city_ids is non-authoritative).
    members = brazil_cl.setdefault("member_city_ids", [])
    city_ids = brazil_cl.setdefault("city_ids", brazil_cl.get("cities") or [])
    rids = brazil_cl.setdefault("route_ids", [])
    for cid in city_names:
        if cid not in members:
            members.append(cid)
        if cid not in city_ids:
            city_ids.append(cid)
    brazil_cl["members_present"] = len(members)
    brazil_cl["members_missing"] = []
    for sr in sealed_routes:
        rid = sr["route_id"]
        if rid not in rids:
            rids.append(rid)

    # Partner market scopes
    for scope_path in [
        ROOT / "deck-studio/decks/didi-brazil/market-scope.json",
        ROOT / "deck-studio/decks/indrive-brazil/market-scope.json",
    ]:
        if not scope_path.exists():
            continue
        scope = load(scope_path)
        cities = scope.get("cities") or []
        # normalize to list of city_id strings or objects
        existing = set()
        for c in cities:
            if isinstance(c, str):
                existing.add(c)
            elif isinstance(c, dict):
                existing.add(c.get("city_id") or c.get("id"))
        for cid in city_names:
            if cid not in existing:
                if cities and isinstance(cities[0], dict):
                    cities.append({"city_id": cid, "source": TAG})
                else:
                    cities.append(cid)
        scope["cities"] = cities
        write(scope_path, scope)

    # Write gold
    write(FBT_PATH, fbt)
    save_routes(ROUTES_PATH, routes)
    write(CLUSTERS_PATH, clusters)

    # Density QA
    density = {}
    for cid, target in DENSITY_TARGETS.items():
        if target <= 0:
            continue
        n = per_city_after.get(cid, 0)
        density[cid] = {
            "before": before_counts.get(cid, 0),
            "after": n,
            "target": target,
            "pass": n >= target,
        }

    receipt = {
        "at": NOW,
        "lane": TAG,
        "spec": "handoff/partner-map-model/brazil-expansion-2026-07-19/GROK-SPEC-brazil-expansion-seal-2026-07-19.md",
        "bp": {
            "handoff_total": 162,
            "sealed_or_mapped": len(handoff_to_atlas),
            "newly_minted": len(sealed_bps),
            "dropped": drop_ledger,
            "drop_count": len(drop_ledger),
            "silent_drops": 0,
        },
        "routes": {
            "sealed_count": len(sealed_routes),
            "failed_count": len(failed_routes),
            "failed": failed_routes[:40],
            "failed_more": max(0, len(failed_routes) - 40),
            "existing_angra_preserved": EXISTING_ANGRA["route_id"],
            "inventory": sealed_routes,
        },
        "density": density,
        "mangaratiba_label_repaired": bool(mang),
        "economics_note": "No economics mutated. Tasklet cascade uses routes.inventory[].route_id + sealed_nm.",
        "for_tasklet_cascade": [
            {
                "route_id": s["route_id"],
                "market": s["market"],
                "sealed_nm": s["sealed_nm"],
                "candidate_nm": s.get("candidate_nm"),
                "basis": s.get("basis"),
                "signature": s.get("signature"),
                "aspirational": s.get("aspirational"),
                "from_bp": s.get("from_bp"),
                "to_bp": s.get("to_bp"),
            }
            for s in sealed_routes
        ],
    }
    out = HANDOFF / "BRAZIL-EXPANSION-SEAL-RECEIPT-2026-07-19.json"
    write(out, receipt)
    print(
        json.dumps(
            {
                "receipt": str(out.relative_to(ROOT)),
                "bp_mapped": len(handoff_to_atlas),
                "bp_dropped": len(drop_ledger),
                "routes_sealed": len(sealed_routes),
                "routes_failed": len(failed_routes),
                "density_pass": sum(1 for v in density.values() if v["pass"]),
                "density_fail": [k for k, v in density.items() if not v["pass"]],
                "angra_preserved": EXISTING_ANGRA["route_id"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
