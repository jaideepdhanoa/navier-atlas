#!/usr/bin/env python3
"""MX+EG expansion hand-waypoints (2026-07-20).

Hardens soft-pass / high-land routes from mx-eg-expansion-2026-07-20 seal:

  A  cairo-r1 (Nile channel) — mask false-positive riverine
  B  cancun-r4, cairo-r2, alex-r3, sayulita-r2, elgouna-r1
  C  holbox-r1 (optional polish)

Uses hand-authored mid-channel spines + densify / solve_hand (Brazil/WETA pattern).
Does not invent economics. Leaves zero-land open-ocean routes untouched.
"""
from __future__ import annotations

import json
import math
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
sys.path.insert(0, str(ROOT / "scripts/grok-geometry"))

from bolt_yango_routing_shared import (  # noqa: E402
    interior_land_km,
    is_water,
    load_land_mask,
    path_length_km,
    save_routes,
)
from channel_solver import get_land_checker, solve_hand  # noqa: E402

DC = ROOT / "data-clean"
HANDOFF = ROOT / "handoff/partner-map-model/mx-eg-expansion-2026-07-20"
FBT_PATH = DC / "FEATURES_BY_TYPE.json"
ROUTES_PATH = DC / "ROUTES.json"
WP_CATALOG = HANDOFF / "mx_eg_expansion_hand_waypoints.json"
CANDIDATES = HANDOFF / "MX-EG-HAND-WP-CANDIDATES-2026-07-20.json"
RECEIPT = HANDOFF / "MX-EG-HAND-WAYPOINTS-RECEIPT-2026-07-20.json"
SEAL_TAG = "mx-eg-expansion-2026-07-20"
TAG = "mx-eg-hand-wp-2026-07-20"
NOW = datetime.now(timezone.utc).isoformat()
LAND_GATE = 0.40
LAND_GATE_ACCEPT = 1.25
# Nile: ocean mask treats river as land — hand spine + allowlist acceptance.
RIVER_MARKETS = {"cairo-egypt"}
LAND_GATE_RIVER = 15.0  # accept after hand spine (mask FP), require spine applied
NM_PER_KM = 0.539957

# ---------------------------------------------------------------------------
# Hand spines keyed by atlas BP pair (sorted later for lookup).
# Coordinates are mid-channel / lagoon / coastal water (not land cuts).
# ---------------------------------------------------------------------------
# Inventory → atlas endpoints from live seal:
#   cairo-r1: bp-cairo-maadi → bp-cairo-zamalek
#   cairo-r2: bp-cairo-zamalek → bp-cairo-maspero
#   cancun-r4: bp-231d7e9357 (Punta Sam) → bp-d08462d3d9 (Isla Mujeres)
#   alex-r3: bp-7852f808de (Montaza) → bp-39ade94a0f (Abu Qir)
#   sayulita-r2: bp-7041a3312f (La Cruz) → bp-3d39a27b9a (Punta Mita)
#   elgouna-r1: bp-f9ca9e18d4 (Abu Tig) → bp-d1f6f24823 (Downtown)
#   holbox-r1: bp-65ae9d38cf (Chiquilá) → bp-holbox-puerto

HAND_SPINES: dict[str, list[list[float]]] = {
    # Nile main stem Maadi (S) → Zamalek (N): stay in river corridor (lng ~31.22–31.24)
    # Even when mask marks water as land, spine follows the navigable channel for render.
    "bp-cairo-maadi|bp-cairo-zamalek": [
        [31.245, 29.975],
        [31.240, 29.995],
        [31.235, 30.015],
        [31.230, 30.035],
        [31.226, 30.050],
    ],
    # Zamalek → Maspero (short Downtown hop on Nile)
    "bp-cairo-maspero|bp-cairo-zamalek": [
        [31.228, 30.058],
        [31.230, 30.057],
    ],
    # Punta Sam → Isla Mujeres: stay in known water cells west/north of island
    "bp-231d7e9357|bp-d08462d3d9": [
        [-86.810, 21.235],
        [-86.800, 21.242],
        [-86.785, 21.248],
        [-86.770, 21.252],
        [-86.755, 21.254],
    ],
    # Montaza → Abu Qir: open Med north of Corniche (water-probed)
    "bp-39ade94a0f|bp-7852f808de": [
        [30.02, 31.32],
        [30.04, 31.34],
        [30.06, 31.35],
        [30.07, 31.34],
    ],
    # La Cruz → Punta Mita: deep Banderas Bay
    "bp-3d39a27b9a|bp-7041a3312f": [
        [-105.42, 20.720],
        [-105.48, 20.730],
        [-105.52, 20.745],
        [-105.53, 20.760],
    ],
    # El Gouna lagoon
    "bp-d1f6f24823|bp-f9ca9e18d4": [
        [33.698, 27.398],
        [33.695, 27.404],
        [33.690, 27.408],
    ],
    # Chiquilá → Holbox channel (known water samples)
    "bp-65ae9d38cf|bp-holbox-puerto": [
        [-87.345, 21.490],
        [-87.355, 21.500],
        [-87.365, 21.510],
        [-87.375, 21.518],
    ],
    # PV south shore open bay
    "bp-6a0861aed5|bp-b2b39b84a5": [
        [-105.35, 20.55],
        [-105.40, 20.52],
        [-105.44, 20.50],
    ],
    "bp-1948509deb|bp-b2b39b84a5": [
        [-105.30, 20.60],
        [-105.36, 20.56],
        [-105.42, 20.51],
        [-105.45, 20.49],
    ],
    "bp-549d2a0cf3|bp-5d305cd04e": [
        [-105.30, 20.62],
        [-105.34, 20.56],
        [-105.36, 20.52],
    ],
    # Alexandria harbour — eastern harbour is water; stay offshore north
    "bp-7852f808de|bp-9b5e22b2d9": [
        [29.900, 31.220],
        [29.940, 31.250],
        [29.980, 31.280],
        [30.005, 31.295],
    ],
    "bp-8b38c37fd3|bp-9b5e22b2d9": [
        [29.885, 31.208],
        [29.886, 31.211],
    ],
}

# Targets to re-solve (inventory_id)
TARGET_INVENTORY = {
    "cairo-r1",
    "cairo-r2",
    "cancun-r4",
    "alex-r3",
    "sayulita-r2",
    "elgouna-r1",
    "holbox-r1",
    # minor C polish if still soft
    "pv-r2",
    "pv-r3",
    "alex-r1",
    "alex-r2",
}


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def write(p: Path, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def pair_key(a: str, b: str) -> str:
    return f"{a}|{b}" if a <= b else f"{b}|{a}"


def snap_water(pt: list, mask, max_r: float = 0.08, toward: list | None = None) -> list:
    """Snap to nearest water cell; break ties by proximity toward the other endpoint."""
    if mask is None or is_water(pt[0], pt[1], mask):
        return list(pt)
    lng, lat = pt[0], pt[1]
    pref_ang = None
    if toward and len(toward) >= 2:
        pref_ang = math.atan2(toward[1] - lat, toward[0] - lng)
    best = None
    best_score = 1e18
    for step in range(1, 50):
        r = step * 0.002
        if r > max_r:
            break
        ring_best = None
        ring_score = 1e18
        for k in range(36):
            ang = 2 * math.pi * k / 36
            c2 = [lng + r * math.cos(ang), lat + r * math.sin(ang)]
            if not is_water(c2[0], c2[1], mask):
                continue
            score = r
            if pref_ang is not None:
                da = abs((ang - pref_ang + math.pi) % (2 * math.pi) - math.pi)
                score += 0.015 * da
            if score < ring_score:
                ring_score = score
                ring_best = c2
        if ring_best is not None:
            # Return the first ring that hits water (true nearest-water snap).
            return ring_best
    return list(pt)


def water_polyline(a: list, b: list, mask, n: int = 36) -> list:
    """Sample nearest water cells along the chord — avoids densify cutting corners over land."""
    pts: list[list[float]] = []
    for i in range(n + 1):
        t = i / n
        lng = a[0] + t * (b[0] - a[0])
        lat = a[1] + t * (b[1] - a[1])
        best = None
        best_d = 1e9
        for step in range(0, 25):
            r = step * 0.002
            for k in range(16):
                ang = 2 * math.pi * k / 16
                p = [lng + r * math.cos(ang), lat + r * math.sin(ang)]
                if is_water(p[0], p[1], mask) and r < best_d:
                    best_d = r
                    best = p
            if best is not None and (r > 0 or is_water(lng, lat, mask)):
                break
        if best:
            if not pts or abs(best[0] - pts[-1][0]) > 1e-5 or abs(best[1] - pts[-1][1]) > 1e-5:
                pts.append(best)
    return pts if len(pts) >= 2 else [list(a), list(b)]


def densify(coords: list, step_km: float = 0.28) -> list:
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


def spine_for(fa: str, ta: str) -> list[list[float]]:
    k = pair_key(fa, ta)
    if k in HAND_SPINES:
        wps = HAND_SPINES[k]
        a, b = k.split("|", 1)
        return list(wps) if a == fa else list(reversed(wps))
    for key, wps in HAND_SPINES.items():
        parts = key.split("|")
        if set(parts) == {fa, ta}:
            return list(wps) if parts[0] == fa else list(reversed(wps))
    return []


def adaptive_water_spine(a: list, b: list, mask, n: int = 6) -> list[list[float]]:
    mids: list[list[float]] = []
    dlon, dlat = b[0] - a[0], b[1] - a[1]
    plen = math.hypot(dlon, dlat) or 1.0
    px, py = -dlat / plen, dlon / plen
    for i in range(1, n + 1):
        t = i / (n + 1)
        base = [a[0] + t * dlon, a[1] + t * dlat]
        best = base
        found = mask is None
        for dist in (0.0, 0.008, 0.015, 0.03, 0.05, 0.08, 0.12, 0.18, 0.28):
            for sign in (0, 1, -1) if dist == 0 else (1, -1):
                pt = [base[0] + sign * px * dist, base[1] + sign * py * dist]
                if mask is None or is_water(pt[0], pt[1], mask):
                    best = pt
                    found = True
                    break
            if found and dist > 0:
                break
            if found and dist == 0:
                break
        mids.append(best)
    return mids


def path_for(a: list, b: list, mids: list, mask, lc, accept_km: float) -> tuple[list, float, float, str]:
    best: tuple[float, float, list, str] | None = None

    def consider(path: list, method: str) -> bool:
        nonlocal best
        if not path or len(path) < 2:
            return False
        land = interior_land_km(path, mask)
        nm = path_length_km(path) * NM_PER_KM
        cand = (land, nm, path, method)
        if best is None or land < best[0] or (abs(land - best[0]) < 1e-9 and nm < best[1]):
            best = cand
        return land <= LAND_GATE

    hand = list(mids or [])
    adaptive = adaptive_water_spine(a, b, mask, n=6)

    # 1) solve_hand first when we have hand mids (A* between water anchors)
    if hand:
        try:
            res = solve_hand(lc, tuple(a), tuple(b), [tuple(p) for p in hand])
            if res and res.get("geometry"):
                coords = res["geometry"]
                if isinstance(coords, dict):
                    coords = coords.get("coordinates") or []
                if coords and consider(coords, "hand+solve_hand"):
                    return best[2], best[0], best[1], best[3]  # type: ignore[index]
                if best and best[0] <= accept_km:
                    return best[2], best[0], best[1], best[3]  # type: ignore[index]
        except Exception:
            pass

    # 2) water-cell polyline (robust coastal)
    if consider(water_polyline(a, b, mask, n=40), "water_polyline"):
        return best[2], best[0], best[1], best[3]  # type: ignore[index]

    # 3) densified hand / adaptive spines
    for label, midset in (("hand", hand), ("adaptive", adaptive)):
        if not midset:
            continue
        spine = [a] + [list(p) for p in midset] + [b]
        if consider(densify(spine, 0.28), f"{label}_spine"):
            return best[2], best[0], best[1], best[3]  # type: ignore[index]
        if best and best[0] <= accept_km and label == "hand":
            return best[2], best[0], best[1], best[3]  # type: ignore[index]

    # 4) solve_hand on adaptive
    if adaptive:
        try:
            res = solve_hand(lc, tuple(a), tuple(b), [tuple(p) for p in adaptive])
            if res and res.get("geometry"):
                coords = res["geometry"]
                if isinstance(coords, dict):
                    coords = coords.get("coordinates") or []
                if coords:
                    consider(coords, "adaptive+solve_hand")
                    if best and best[0] <= accept_km:
                        return best[2], best[0], best[1], best[3]  # type: ignore[index]
        except Exception:
            pass

    dlon, dlat = b[0] - a[0], b[1] - a[1]
    plen = math.hypot(dlon, dlat) or 1.0
    px, py = -dlat / plen, dlon / plen
    for dist in (0.03, 0.06, 0.10, 0.18, 0.30, 0.45):
        for sign in (1, -1):
            mid = [(a[0] + b[0]) / 2 + sign * px * dist, (a[1] + b[1]) / 2 + sign * py * dist]
            if consider(densify([a, mid, b], 0.28), "offset_search"):
                return best[2], best[0], best[1], best[3]  # type: ignore[index]

    consider(densify([a, b], 0.28), "straight")
    assert best is not None
    return best[2], best[0], best[1], best[3]


def main() -> int:
    global NOW
    NOW = datetime.now(timezone.utc).isoformat()
    mask = load_land_mask()
    lc = get_land_checker()
    fbt = load(FBT_PATH)
    routes = load(ROUTES_PATH)
    if isinstance(routes, dict):
        routes = routes.get("features") or routes.get("routes") or []

    poi_by_id = {}
    for p in fbt.get("poi") or []:
        pid = (p.get("properties") or {}).get("id")
        if pid:
            poi_by_id[pid] = p

    # Phase 0 candidates snapshot
    candidates = []
    for r in routes:
        props = r.get("properties") or {}
        if props.get("_seal_lane") != SEAL_TAG:
            continue
        land = float(props.get("_land_km_interior") or 0)
        inv = props.get("_inventory_id")
        if land < 0.05 and inv not in TARGET_INVENTORY:
            continue
        fa = props.get("from_bp_id")
        ta = props.get("to_bp_id")
        candidates.append(
            {
                "inventory_id": inv,
                "route_id": props.get("id"),
                "land_km_before": land,
                "from_bp": fa,
                "to_bp": ta,
                "market": props.get("from_city_id") or props.get("cluster_city_id"),
                "targeted": inv in TARGET_INVENTORY or land >= 0.35,
            }
        )
    write(CANDIDATES, {"at": NOW, "n": len(candidates), "candidates": candidates})

    results = []
    catalog_entries = []

    for r in routes:
        props = r.get("properties") or {}
        if props.get("_seal_lane") != SEAL_TAG:
            continue
        inv = props.get("_inventory_id")
        land_before = float(props.get("_land_km_interior") or 0)
        if inv not in TARGET_INVENTORY and land_before < 0.35:
            continue

        fa = props.get("from_bp_id")
        ta = props.get("to_bp_id")
        if not fa or not ta or fa not in poi_by_id or ta not in poi_by_id:
            results.append(
                {
                    "inventory_id": inv,
                    "route_id": props.get("id"),
                    "status": "skip_missing_endpoints",
                    "land_before": land_before,
                }
            )
            continue

        a = list((poi_by_id[fa].get("geometry") or {}).get("coordinates") or [])
        b = list((poi_by_id[ta].get("geometry") or {}).get("coordinates") or [])
        if len(a) < 2 or len(b) < 2:
            results.append(
                {
                    "inventory_id": inv,
                    "route_id": props.get("id"),
                    "status": "skip_missing_coords",
                    "land_before": land_before,
                }
            )
            continue

        market = props.get("from_city_id") or props.get("cluster_city_id") or ""
        river = market in RIVER_MARKETS or inv.startswith("cairo-")
        accept = LAND_GATE_RIVER if river else LAND_GATE_ACCEPT

        hand = spine_for(fa, ta)
        # Prefer paths from original pier coords (water_polyline snaps mid-chord cells).
        # Only fall back to endpoint water-snap if still above accept.
        path, land, nm, method = path_for(a, b, hand, mask, lc, accept)
        if not river and land > LAND_GATE:
            a2 = snap_water(a, mask, toward=b)
            b2 = snap_water(b, mask, toward=a)
            path2, land2, nm2, method2 = path_for(a2, b2, hand, mask, lc, accept)
            if land2 < land:
                path, land, nm, method = path2, land2, nm2, method2 + "+endsnap"

        # Nile: ocean mask treats the river as land — force densified hand channel for render.
        if river and hand:
            river_path = densify([a] + [list(p) for p in hand] + [b], 0.25)
            path, land, nm, method = (
                river_path,
                interior_land_km(river_path, mask),
                path_length_km(river_path) * NM_PER_KM,
                "nile_hand_channel",
            )

        # Never apply a worse land score (tolerance 0.05 km for float noise).
        improved = land < land_before - 0.01
        non_worse_hard = land <= LAND_GATE and land <= land_before + 0.05
        river_hand = river and hand and method == "nile_hand_channel"

        if non_worse_hard:
            ok, gate = True, "hard"
        elif improved and land <= LAND_GATE:
            ok, gate = True, "hard"
        elif improved and land <= LAND_GATE_ACCEPT:
            ok, gate = True, "accept_improved"
        elif improved:
            ok, gate = True, "improved_only"
        elif river_hand:
            ok, gate = True, "river_allowlist_hand"
        else:
            ok, gate = False, "fail"

        if not ok:
            results.append(
                {
                    "inventory_id": inv,
                    "route_id": props.get("id"),
                    "status": "no_improvement",
                    "land_before": land_before,
                    "land_after": land,
                    "method": method,
                    "gate": gate,
                }
            )
            continue

        # Apply geometry in place (same route_id)
        r["geometry"] = {"type": "LineString", "coordinates": path}
        props["distance_nm"] = round(nm, 2)
        props["_land_km_interior"] = land
        props["_hand_waypoint_lane"] = TAG
        props["_hand_waypoint_at"] = NOW
        props["_hand_waypoint_method"] = method
        props["_land_km_before_hand_wp"] = land_before
        if land <= LAND_GATE:
            props["_geometry_status"] = "hand_waypoint_hard_pass"
            props.pop("_land_km_note", None)
        elif river:
            props["_geometry_status"] = "nile_allowlist_hand_spine"
            props["_land_km_note"] = (
                f"Nile riverine: global ocean mask reports {land:.2f}km interior; "
                f"hand channel spine applied; economics remain geometry_only"
            )
        else:
            props["_geometry_status"] = "hand_waypoint_accept"
            props["_land_km_note"] = (
                f"hand spine reduced interior land {land_before:.2f}→{land:.2f}km "
                f"(accept gate {accept}km)"
            )

        if hand:
            catalog_entries.append(
                {
                    "from_bp": fa,
                    "to_bp": ta,
                    "inventory_id": inv,
                    "route_id": props.get("id"),
                    "waypoints": hand,
                    "method": method,
                    "land_km": land,
                }
            )

        results.append(
            {
                "inventory_id": inv,
                "route_id": props.get("id"),
                "status": "updated",
                "land_before": land_before,
                "land_after": land,
                "nm": round(nm, 2),
                "method": method,
                "gate": gate,
                "had_hand_spine": bool(hand),
            }
        )

    save_routes(ROUTES_PATH, routes)
    write(
        WP_CATALOG,
        {
            "at": NOW,
            "lane": TAG,
            "n": len(catalog_entries),
            "entries": catalog_entries,
        },
    )

    updated = [x for x in results if x.get("status") == "updated"]
    hard_pass = [x for x in updated if x.get("land_after", 99) <= LAND_GATE]
    receipt = {
        "at": NOW,
        "lane": TAG,
        "seal_lane": SEAL_TAG,
        "land_gate_hard": LAND_GATE,
        "land_gate_accept": LAND_GATE_ACCEPT,
        "land_gate_river": LAND_GATE_RIVER,
        "n_targeted": len([c for c in candidates if c.get("targeted")]),
        "n_updated": len(updated),
        "n_hard_pass": len(hard_pass),
        "results": results,
        "gates": {
            "cairo_r1_hand_applied": any(
                x.get("inventory_id") == "cairo-r1" and x.get("status") == "updated" for x in results
            ),
            "all_A_B_updated_or_hard": all(
                any(
                    x.get("inventory_id") == inv
                    and (x.get("status") == "updated" or (x.get("land_before") or 0) <= LAND_GATE)
                    for x in results
                )
                for inv in ("cairo-r1", "cairo-r2", "cancun-r4", "alex-r3", "sayulita-r2", "elgouna-r1")
            ),
        },
    }
    write(RECEIPT, receipt)

    print(f"updated={len(updated)} hard_pass={len(hard_pass)}")
    for x in sorted(results, key=lambda z: -(z.get("land_before") or 0)):
        if x.get("status") == "updated":
            print(
                f"  {x['inventory_id']:14} {x['land_before']:.3f}→{x['land_after']:.3f}km "
                f"method={x['method']} gate={x['gate']}"
            )
        else:
            print(f"  {x.get('inventory_id')} {x.get('status')} land={x.get('land_before')}")
    print(f"receipt: {RECEIPT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
