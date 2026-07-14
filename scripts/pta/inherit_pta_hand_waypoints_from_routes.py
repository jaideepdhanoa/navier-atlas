#!/usr/bin/env python3
"""Fill empty PTA hand-waypoint pairs by inheriting midpoints from existing ROUTES geometry.

Why many PTA files are empty
----------------------------
`pta_hand_waypoints_*.json` is a **PTA pair-key catalog** (from|to node slugs) used by the
PTA seal / densify pipeline. Canonical `ROUTES.json` often already has water geometry for
the same markets (coastal solver, earlier hand spines, ics-*/rn-* seals). Those geometries
were never copied back into the PTA pair catalog, so the files look "empty" even when the
map already routes correctly.

This script:
  1. Loads PTA dossier boarding-point anchors + empty pair keys
  2. Matches each pair to an existing ROUTES feature by endpoint proximity
  3. Extracts interior vertices as hand waypoints (or densified midpoints)
  4. Writes filled waypoints when a confident match is found
  5. Leaves unmatched pairs empty (still need human/spine authoring)

Does not invent new routes or economics.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DC = ROOT / "data-clean"
HANDOFF = ROOT / "handoff/partner-map-model"

R_EARTH_KM = 6371.0


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def hav_km(a, b) -> float:
    lon1, lat1 = math.radians(a[0]), math.radians(a[1])
    lon2, lat2 = math.radians(b[0]), math.radians(b[1])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * R_EARTH_KM * math.asin(min(1.0, math.sqrt(h)))


def load_routes():
    raw = json.loads((DC / "ROUTES.json").read_text())
    feats = raw if isinstance(raw, list) else raw.get("features") or []
    out = []
    for f in feats:
        geom = f.get("geometry") or {}
        coords = geom.get("coordinates") or []
        if len(coords) < 2:
            continue
        props = f.get("properties") or {}
        out.append(
            {
                "id": props.get("id"),
                "coords": coords,
                "a": coords[0],
                "b": coords[-1],
                "props": props,
            }
        )
    return out


def extract_waypoints(coords: list, max_pts: int = 12) -> list:
    """Interior vertices; subsample if very dense."""
    if len(coords) <= 2:
        # synthesize a midpoint
        a, b = coords[0], coords[-1]
        return [[(a[0] + b[0]) / 2, (a[1] + b[1]) / 2]]
    interior = coords[1:-1]
    if len(interior) <= max_pts:
        return [[float(c[0]), float(c[1])] for c in interior]
    # even subsample
    step = max(1, len(interior) // max_pts)
    sampled = interior[::step][:max_pts]
    return [[float(c[0]), float(c[1])] for c in sampled]


def match_route(from_coord, to_coord, routes, max_end_km: float = 2.5):
    """Best route whose endpoints are near (from,to) in either direction."""
    best = None
    for r in routes:
        d1 = hav_km(from_coord, r["a"]) + hav_km(to_coord, r["b"])
        d2 = hav_km(from_coord, r["b"]) + hav_km(to_coord, r["a"])
        d = min(d1, d2)
        fwd = d1 <= d2
        if d > max_end_km * 2:
            continue
        # each end should be reasonably close
        if fwd:
            ea, eb = hav_km(from_coord, r["a"]), hav_km(to_coord, r["b"])
        else:
            ea, eb = hav_km(from_coord, r["b"]), hav_km(to_coord, r["a"])
        if ea > max_end_km or eb > max_end_km:
            continue
        score = d
        if best is None or score < best[0]:
            best = (score, r, fwd, ea, eb)
    return best


def process_partner(slug: str, routes: list, *, apply: bool, max_end_km: float) -> dict:
    dossier_path = HANDOFF / f"PTA-DOSSIER-{slug}.json"
    wp_path = DC / f"pta_hand_waypoints_{slug.replace('-', '_')}.json"
    # also try without replace edge cases
    if not wp_path.exists():
        alt = DC / f"pta_hand_waypoints_{slug}.json"
        if alt.exists():
            wp_path = alt

    report = {
        "partner": slug,
        "generated_at": utc_now(),
        "filled": [],
        "already_filled": [],
        "unmatched": [],
        "no_dossier": False,
        "no_wp_file": False,
    }

    if not wp_path.exists():
        report["no_wp_file"] = True
        return report

    wp_doc = json.loads(wp_path.read_text())
    catalog = wp_doc.setdefault("waypoints", {})

    nodes = {}
    pairs = []
    if dossier_path.exists():
        dossier = json.loads(dossier_path.read_text())
        dn = dossier.get("domestic_network") or {}
        nodes = {b["node"]: b for b in dn.get("boarding_points") or [] if "node" in b}
        pairs = list(dn.get("domestic_pairs") or [])
    else:
        # synthesize pairs from empty catalog keys node|node
        for key, val in catalog.items():
            if "|" not in key:
                continue
            if val:
                report["already_filled"].append(key)
                continue
            report["unmatched"].append({"key": key, "reason": "no_dossier_and_no_node_coords"})
        report["no_dossier"] = True
        if apply:
            wp_doc["generated_at"] = utc_now()
            wp_doc["_inherit_note"] = (
                "Empty PTA pairs need dossier node anchors or human spines; "
                "inheritance requires PTA-DOSSIER-* boarding_points with anchor_lnglat."
            )
            wp_path.write_text(json.dumps(wp_doc, indent=2) + "\n")
        return report

    # index keys
    for pair in pairs:
        fn, tn = pair.get("from"), pair.get("to")
        key = f"{fn}|{tn}"
        if catalog.get(key):
            report["already_filled"].append(key)
            continue
        if fn not in nodes or tn not in nodes:
            report["unmatched"].append({"key": key, "reason": "missing_node"})
            continue
        a = tuple(nodes[fn]["anchor_lnglat"])
        b = tuple(nodes[tn]["anchor_lnglat"])
        m = match_route(a, b, routes, max_end_km=max_end_km)
        if not m:
            report["unmatched"].append({"key": key, "reason": "no_route_within_end_km", "max_end_km": max_end_km})
            continue
        score, r, fwd, ea, eb = m
        coords = r["coords"] if fwd else list(reversed(r["coords"]))
        wps = extract_waypoints(coords)
        catalog[key] = wps
        report["filled"].append(
            {
                "key": key,
                "route_id": r["id"],
                "waypoints": len(wps),
                "end_km": [round(ea, 3), round(eb, 3)],
                "match_score_km": round(score, 3),
            }
        )

    # also try any empty catalog keys not in pairs
    for key, val in list(catalog.items()):
        if val or "|" not in key:
            continue
        if any(f.get("key") == key for f in report["filled"]):
            continue
        fn, tn = key.split("|", 1)
        if fn not in nodes or tn not in nodes:
            if not any(u.get("key") == key for u in report["unmatched"]):
                report["unmatched"].append({"key": key, "reason": "empty_key_missing_node"})
            continue
        a = tuple(nodes[fn]["anchor_lnglat"])
        b = tuple(nodes[tn]["anchor_lnglat"])
        m = match_route(a, b, routes, max_end_km=max_end_km)
        if not m:
            if not any(u.get("key") == key for u in report["unmatched"]):
                report["unmatched"].append({"key": key, "reason": "no_route_within_end_km"})
            continue
        score, r, fwd, ea, eb = m
        coords = r["coords"] if fwd else list(reversed(r["coords"]))
        wps = extract_waypoints(coords)
        catalog[key] = wps
        report["filled"].append(
            {
                "key": key,
                "route_id": r["id"],
                "waypoints": len(wps),
                "end_km": [round(ea, 3), round(eb, 3)],
                "match_score_km": round(score, 3),
            }
        )

    if apply and report["filled"]:
        wp_doc["generated_at"] = utc_now()
        wp_doc["_inherit_from_routes_at"] = utc_now()
        wp_doc["_inherit_policy"] = (
            "Waypoints subsampled from existing ROUTES geometry matched by endpoint proximity; "
            "not new invented corridors."
        )
        wp_path.write_text(json.dumps(wp_doc, indent=2) + "\n")
        receipt = HANDOFF / f"PTA-HAND-WAYPOINTS-INHERIT-{slug}.json"
        receipt.write_text(json.dumps(report, indent=2) + "\n")

    return report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--partner", action="append", help="PTA slug; default=all with empty wp files")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--max-end-km", type=float, default=2.5)
    ap.add_argument("--all-empty", action="store_true", help="process every pta_hand_waypoints_* file")
    args = ap.parse_args()

    routes = load_routes()
    partners = args.partner or []
    if args.all_empty or not partners:
        for path in sorted(DC.glob("pta_hand_waypoints_*.json")):
            slug = path.name.replace("pta_hand_waypoints_", "").replace(".json", "").replace("_", "-")
            # skip already fully filled or alexandria candidate
            try:
                doc = json.loads(path.read_text())
                w = doc.get("waypoints") or {}
                if w and all(v for v in w.values()):
                    continue
            except Exception:
                pass
            partners.append(slug)
        partners = sorted(set(partners))

    summary = {"generated_at": utc_now(), "partners": {}}
    total_filled = 0
    total_unmatched = 0
    for slug in partners:
        rep = process_partner(slug, routes, apply=args.apply, max_end_km=args.max_end_km)
        summary["partners"][slug] = {
            "filled": len(rep.get("filled") or []),
            "already_filled": len(rep.get("already_filled") or []),
            "unmatched": len(rep.get("unmatched") or []),
            "no_dossier": rep.get("no_dossier"),
            "no_wp_file": rep.get("no_wp_file"),
        }
        total_filled += len(rep.get("filled") or [])
        total_unmatched += len(rep.get("unmatched") or [])
        print(
            f"{slug}: filled={len(rep.get('filled') or [])} "
            f"already={len(rep.get('already_filled') or [])} "
            f"unmatched={len(rep.get('unmatched') or [])}"
        )

    summary["total_filled"] = total_filled
    summary["total_unmatched"] = total_unmatched
    out = HANDOFF / "PTA-HAND-WAYPOINTS-INHERIT-SUMMARY-2026-07-14.json"
    if args.apply:
        out.write_text(json.dumps(summary, indent=2) + "\n")
        print(f"wrote {out}")
    print(json.dumps({"total_filled": total_filled, "total_unmatched": total_unmatched}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
