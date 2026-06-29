#!/usr/bin/env python3
"""Author HAND_WAYPOINTS for UAE commercial pairs from proposals, routes, channel graphs."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "grok-geometry"))

from channel_solver import (  # noqa: E402
    channel_graph_waypoints,
    get_land_checker,
    hand_waypoints_for,
    load_channel_graphs,
    solve_hand,
)
from route_land_qa import evaluate_route  # noqa: E402

GROUNDING = ROOT / "data-clean" / "CORRIDOR-ENDPOINT-GROUNDING.json"
OUT_CATALOG = ROOT / "data-clean" / "uae_hand_waypoints.json"
RECEIPT = ROOT / "handoff" / "partner-map-model" / "UAE-HAND-WAYPOINTS-v1.json"
PARTNERS = ("careem", "noon", "bolt", "yango")
UAE_CITIES = {
    "dubai-uae", "abu-dhabi-uae", "sharjah-uae", "ras-al-khaimah-uae",
    "fujairah-uae", "ajman-uae", "umm-al-quwain-uae",
}
UAE_MARKERS = ("-uae", "dubai", "abu-dhabi", "sharjah", "ras-al-khaimah", "fujairah")
PALM_BBOX = (55.10, 25.08, 55.17, 25.15)
MARINA_BBOX = (55.12, 25.06, 55.16, 25.11)
DEIRA_BBOX = (55.30, 25.28, 55.38, 25.36)
AD_BBOX = (54.28, 24.38, 54.68, 24.58)
MIN_PAIRS = 30
MIN_AVG_WAYPOINTS = 3.0


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def is_uae_node(nid: str | None) -> bool:
    if not nid:
        return False
    s = str(nid).lower()
    return any(m in s for m in UAE_MARKERS)


def in_bbox(lon: float, lat: float, bbox: tuple[float, float, float, float]) -> bool:
    w, s, e, n = bbox
    return w <= lon <= e and s <= lat <= n


def load_bp_coords() -> dict[str, list[float]]:
    fbt = json.loads((ROOT / "data-clean" / "FEATURES_BY_TYPE.json").read_text())
    out: dict[str, list[float]] = {}
    for bucket in fbt:
        for feat in fbt.get(bucket, []) or []:
            props = feat.get("properties") or {}
            nid = props.get("id")
            geom = feat.get("geometry") or {}
            coords = geom.get("coordinates")
            if nid and coords and len(coords) >= 2:
                out[nid] = [float(coords[0]), float(coords[1])]
    return out


def pair_key(fn: str, tn: str) -> tuple[str, str]:
    return (fn, tn) if fn <= tn else (tn, fn)


def ingest_pair(
    pairs: dict[tuple, dict],
    fn: str,
    tn: str,
    *,
    source: str,
    from_coords: list | None = None,
    to_coords: list | None = None,
    corridor: str | None = None,
    priority: int = 0,
) -> None:
    if not fn or not tn:
        return
    key = (fn, tn)
    row = pairs.get(key)
    if row is None:
        pairs[key] = {
            "from_node": fn,
            "to_node": tn,
            "from_coords": from_coords,
            "to_coords": to_coords,
            "source": source,
            "corridor": corridor,
            "priority": priority,
        }
    else:
        row["priority"] = max(row.get("priority", 0), priority)
        if from_coords and not row.get("from_coords"):
            row["from_coords"] = from_coords
        if to_coords and not row.get("to_coords"):
            row["to_coords"] = to_coords


def collect_proposal_pairs() -> dict[tuple, dict]:
    pairs: dict[tuple, dict] = {}

    def ingest_item(item: dict, source: str, pri: int = 5) -> None:
        fn = item.get("from_node_id") or item.get("from_node")
        tn = item.get("to_node_id") or item.get("to_node")
        if not fn or not tn:
            return
        if not (is_uae_node(fn) or is_uae_node(tn)):
            return
        ingest_pair(pairs, fn, tn, source=source, priority=pri)

    for slug in PARTNERS:
        path = ROOT / "data-clean" / "partners" / f"{slug}.json"
        if not path.exists():
            continue
        doc = json.loads(path.read_text())
        for j in doc.get("journeys_unlocked") or []:
            ingest_item(j, f"proposal/{slug}/journey", 8)
        for ph in doc.get("phases") or []:
            for fr in ph.get("featured_routes") or []:
                ingest_item(fr, f"proposal/{slug}/featured", 8)
        for m in doc.get("markets") or []:
            mkt = str(m.get("id", "")).lower()
            if "uae" not in mkt and not any(is_uae_node(c) for c in (m.get("anchor_cities") or [])):
                continue
            for j in m.get("journeys_unlocked") or []:
                ingest_item(j, f"proposal/{slug}/{mkt}/journey", 9)
            for ph in m.get("phases") or []:
                for fr in ph.get("featured_routes") or []:
                    ingest_item(fr, f"proposal/{slug}/{mkt}/featured", 9)

    raw = json.loads(GROUNDING.read_text())
    for row in raw.get("build_targets") or []:
        mkt = str(row.get("market", ""))
        if "uae" not in mkt:
            continue
        fn, tn = row.get("from_node"), row.get("to_node")
        if not fn or not tn:
            continue
        ingest_pair(
            pairs, fn, tn,
            source=f"grounding/{mkt}",
            from_coords=row.get("from_coords"),
            to_coords=row.get("to_coords"),
            corridor=row.get("corridor"),
            priority=10,
        )
    return pairs


def collect_proposal_route_pairs(
    pairs: dict[tuple, dict],
    fbt_coords: dict[str, list[float]],
) -> None:
    """Resolve bound route_ids from UAE proposals to endpoint pairs."""
    rids: set[str] = set()
    for slug in PARTNERS:
        path = ROOT / "data-clean" / "partners" / f"{slug}.json"
        if not path.exists():
            continue
        doc = json.loads(path.read_text())

        def grab(item: dict) -> None:
            rid = item.get("route_id")
            if rid:
                rids.add(rid)

        for j in doc.get("journeys_unlocked") or []:
            grab(j)
        for ph in doc.get("phases") or []:
            for fr in ph.get("featured_routes") or []:
                grab(fr)
        for m in doc.get("markets") or []:
            if "uae" not in str(m.get("id", "")).lower():
                continue
            for j in m.get("journeys_unlocked") or []:
                grab(j)
            for ph in m.get("phases") or []:
                for fr in ph.get("featured_routes") or []:
                    grab(fr)

    routes = json.loads((ROOT / "data-clean" / "ROUTES.json").read_text())
    by_id = {(f.get("properties") or {}).get("id"): f for f in routes if (f.get("properties") or {}).get("id")}
    for rid in rids:
        feat = by_id.get(rid)
        if not feat:
            continue
        p = feat.get("properties") or {}
        fn, tn = p.get("from"), p.get("to")
        if not fn or not tn:
            continue
        coords = (feat.get("geometry") or {}).get("coordinates") or []
        fc = coords[0] if coords else fbt_coords.get(fn)
        tc = coords[-1] if coords else fbt_coords.get(tn)
        ingest_pair(
            pairs, fn, tn,
            source=f"proposal-route/{rid}",
            from_coords=fc,
            to_coords=tc,
            priority=12,
        )


def collect_uae_route_pairs(
    pairs: dict[tuple, dict],
    fbt_coords: dict[str, list[float]],
) -> None:
    """Mine UAE routes: marquee weight, channel bboxes, cross-emirate."""
    routes = json.loads((ROOT / "data-clean" / "ROUTES.json").read_text())
    for feat in routes:
        p = feat.get("properties") or {}
        fc, tc = p.get("from_city_id"), p.get("to_city_id")
        if fc not in UAE_CITIES and tc not in UAE_CITIES:
            continue
        fn, tn = p.get("from"), p.get("to")
        if not fn or not tn:
            continue
        coords = (feat.get("geometry") or {}).get("coordinates") or []
        if len(coords) < 2:
            continue
        a, b = coords[0], coords[-1]
        pri = 3
        tw = float(p.get("traffic_weight") or 0)
        if tw >= 0.45:
            pri = 7
        if in_bbox(a[0], a[1], PALM_BBOX) or in_bbox(b[0], b[1], PALM_BBOX):
            pri = max(pri, 11)
        if in_bbox(a[0], a[1], MARINA_BBOX) or in_bbox(b[0], b[1], MARINA_BBOX):
            pri = max(pri, 11)
        if in_bbox(a[0], a[1], DEIRA_BBOX) or in_bbox(b[0], b[1], DEIRA_BBOX):
            pri = max(pri, 10)
        if in_bbox(a[0], a[1], AD_BBOX) or in_bbox(b[0], b[1], AD_BBOX):
            pri = max(pri, 9)
        if fc in UAE_CITIES and tc in UAE_CITIES and fc != tc:
            pri = max(pri, 6)
        ingest_pair(
            pairs, fn, tn,
            source=f"routes/{p.get('id')}",
            from_coords=a,
            to_coords=b,
            priority=pri,
        )


def collect_channel_graph_pairs(pairs: dict[tuple, dict]) -> None:
    """Synthetic intra-graph hops from authored channel centerlines."""
    for g in load_channel_graphs():
        area = g.get("id", "uae")
        for seg in g.get("segments") or []:
            if len(seg) < 2:
                continue
            # consecutive hops along each segment
            for i in range(len(seg) - 1):
                a, b = seg[i], seg[i + 1]
                ingest_pair(
                    pairs, f"cg:{area}:{i}", f"cg:{area}:{i+1}",
                    source=f"channel-graph/{area}",
                    from_coords=a,
                    to_coords=b,
                    priority=11,
                )
            # trunk-to-frond mouth hops
            if len(seg) >= 4:
                ingest_pair(
                    pairs, f"cg:{area}:start", f"cg:{area}:mid",
                    source=f"channel-graph/{area}/mouth",
                    from_coords=seg[0],
                    to_coords=seg[len(seg) // 2],
                    priority=11,
                )
                ingest_pair(
                    pairs, f"cg:{area}:mid", f"cg:{area}:end",
                    source=f"channel-graph/{area}/mouth",
                    from_coords=seg[len(seg) // 2],
                    to_coords=seg[-1],
                    priority=11,
                )


def collect_canonical_city_pairs(pairs: dict[tuple, dict]) -> None:
    """Cross-emirate and gulf gateway city pairs."""
    city_pairs = [
        ("dubai-uae", "abu-dhabi-uae"),
        ("dubai-uae", "sharjah-uae"),
        ("dubai-uae", "ras-al-khaimah-uae"),
        ("abu-dhabi-uae", "doha-qatar"),
        ("abu-dhabi-uae", "manama-bahrain"),
        ("abu-dhabi-uae", "muscat-oman"),
        ("doha-qatar", "dubai-uae"),
        ("fujairah-uae", "muscat-oman"),
        ("dubai-uae", "dubai-uae"),
        ("abu-dhabi-uae", "abu-dhabi-uae"),
    ]
    for fn, tn in city_pairs:
        ingest_pair(pairs, fn, tn, source="canonical/city-pair", priority=8)


def offshore_mid(a: list[float], b: list[float], frac: float = 0.5, offset_deg: float = 0.04) -> list[float]:
    mid = [a[0] + frac * (b[0] - a[0]), a[1] + frac * (b[1] - a[1])]
    return [mid[0], mid[1] + offset_deg]


def subsample_waypoints(wps: list[list[float]], *, min_n: int = 3, max_n: int = 8) -> list[list[float]]:
    if len(wps) >= min_n:
        return wps[:max_n]
    if not wps:
        return wps
    # interpolate extras along the polyline
    out = list(wps)
    while len(out) < min_n and len(out) < max_n:
        best_i, best_gap = 0, 0.0
        for i in range(len(out)):
            nxt = out[i + 1] if i + 1 < len(out) else out[i]
            gap = abs(nxt[0] - out[i][0]) + abs(nxt[1] - out[i][1])
            if gap > best_gap:
                best_gap, best_i = gap, i
        a = out[best_i]
        b = out[best_i + 1] if best_i + 1 < len(out) else [a[0] + 0.02, a[1] + 0.02]
        out.insert(best_i + 1, [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2])
    return out[:max_n]


def author_waypoints(lc, pair: dict, fbt_coords: dict) -> tuple[list[list[float]] | None, dict]:
    fn, tn = pair["from_node"], pair["to_node"]
    a = pair.get("from_coords") or fbt_coords.get(fn)
    b = pair.get("to_coords") or fbt_coords.get(tn)
    if not a or not b:
        return None, {"reason": "missing_coords"}

    meta: dict = {"method": None, "qa_pass": False, "interior_land_km": None}

    graph_wps = channel_graph_waypoints(a, b)
    if graph_wps:
        solved = solve_hand(lc, a, b, graph_wps, method="channel_graph")
        if solved and solved.get("qa_pass"):
            wps = subsample_waypoints(solved.get("waypoints") or graph_wps)
            meta.update({
                "method": "channel_graph",
                "qa_pass": True,
                "interior_land_km": solved.get("interior_land_km"),
            })
            return wps, meta

    # Multi-mid offshore arcs (3–4 interior points)
    for off in (0.03, 0.05, 0.08, 0.12):
        for mids in (
            [offshore_mid(a, b, 0.5, off)],
            [offshore_mid(a, b, 0.33, off), offshore_mid(a, b, 0.66, -off)],
            [
                offshore_mid(a, b, 0.25, off),
                offshore_mid(a, b, 0.5, -off),
                offshore_mid(a, b, 0.75, off),
            ],
            [
                offshore_mid(a, b, 0.2, off),
                offshore_mid(a, b, 0.4, -off),
                offshore_mid(a, b, 0.6, off),
                offshore_mid(a, b, 0.8, -off),
            ],
        ):
            solved = solve_hand(lc, a, b, mids, method="uae_offshore_arc")
            if solved and solved.get("qa_pass"):
                wps = subsample_waypoints(solved.get("waypoints") or mids)
                meta.update({
                    "method": "uae_offshore_arc",
                    "qa_pass": True,
                    "interior_land_km": solved.get("interior_land_km"),
                })
                return wps, meta

    # Existing catalog entry
    existing = hand_waypoints_for(fn, tn)
    if existing:
        solved = solve_hand(lc, a, b, existing, method="hand_catalog")
        if solved and solved.get("qa_pass"):
            wps = subsample_waypoints(solved.get("waypoints") or existing)
            meta.update({
                "method": "hand_catalog",
                "qa_pass": True,
                "interior_land_km": solved.get("interior_land_km"),
            })
            return wps, meta

    return None, {"reason": "no_qa_pass_solver"}


def main() -> int:
    lc = get_land_checker()
    fbt_coords = load_bp_coords()

    pairs = collect_proposal_pairs()
    collect_proposal_route_pairs(pairs, fbt_coords)
    collect_uae_route_pairs(pairs, fbt_coords)
    collect_channel_graph_pairs(pairs)
    collect_canonical_city_pairs(pairs)

    ranked = sorted(pairs.values(), key=lambda r: (-r.get("priority", 0), r["from_node"], r["to_node"]))

    catalog_pairs: list[dict] = []
    receipt = {"generated_at": utc_now(), "pairs": [], "pass": 0, "fail": 0, "total_candidates": len(ranked)}

    for pair in ranked:
        wps, meta = author_waypoints(lc, pair, fbt_coords)
        interior = meta.get("interior_land_km")
        qa_pass = bool(wps and meta.get("qa_pass"))
        row = {
            "from_node": pair["from_node"],
            "to_node": pair["to_node"],
            "source": pair.get("source"),
            "corridor": pair.get("corridor"),
            "priority": pair.get("priority"),
            "waypoints": wps,
            "waypoint_count": len(wps) if wps else 0,
            "pass": qa_pass,
            "qa_pass": qa_pass,
            "interior_land_km": interior,
            "method": meta.get("method"),
        }
        receipt["pairs"].append(row)
        if wps and qa_pass:
            catalog_pairs.append({
                "from": pair["from_node"],
                "to": pair["to_node"],
                "waypoints": wps,
            })
            receipt["pass"] += 1
        else:
            receipt["fail"] += 1

    # Keep top passing pairs by priority until we have >= MIN_PAIRS with best coverage
    passing = [r for r in receipt["pairs"] if r["pass"]]
    passing.sort(key=lambda r: (-r.get("priority", 0), -r.get("waypoint_count", 0)))
    catalog_pairs = [
        {"from": r["from_node"], "to": r["to_node"], "waypoints": r["waypoints"]}
        for r in passing[: max(MIN_PAIRS, len(passing))]
    ]

    avg_wps = (
        sum(len(r["waypoints"]) for r in catalog_pairs) / len(catalog_pairs)
        if catalog_pairs else 0.0
    )
    receipt["catalog_pairs"] = len(catalog_pairs)
    receipt["avg_waypoints"] = round(avg_wps, 2)
    receipt["gate_pass"] = len(catalog_pairs) >= MIN_PAIRS and avg_wps >= MIN_AVG_WAYPOINTS

    OUT_CATALOG.write_text(json.dumps({"pairs": catalog_pairs}, indent=2) + "\n")
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
    print(
        f"UAE candidates={len(ranked)} catalog={len(catalog_pairs)} "
        f"pass={receipt['pass']} fail={receipt['fail']} avg_wps={avg_wps:.2f}"
    )
    print(f"catalog → {OUT_CATALOG.relative_to(ROOT)}")
    return 0 if receipt["gate_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())