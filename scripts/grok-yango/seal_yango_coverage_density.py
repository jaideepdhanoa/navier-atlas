#!/usr/bin/env python3
"""Grok seal — Yango coverage-density expansion (#79cu).

Mint 108 BPs, seal 82 corridors from handoff/partner-map-model/yango-coverage-seal/.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
sys.path.insert(0, str(ROOT / "scripts/grok-geometry"))

from bolt_yango_routing_shared import (  # noqa: E402
    build_bp_index,
    build_city_index,
    build_coastal_path,
    interior_land_km,
    load_json,
    make_route_feature,
    mint_route_id,
    norm_label,
    NM_PER_KM,
    path_length_km,
    route_features,
    route_id_of,
    save_json,
    save_routes,
)
from bolt_yango_shared import load_land_mask, save_json as by_save  # noqa: E402
from channel_solver import HAND_WAYPOINTS  # noqa: E402
from regional_land_masks import in_water_override  # noqa: E402
from route_land_qa import evaluate_route  # noqa: E402
from snap_bp_coverage_new import EXTRA_WATER_BODIES, snap_to_water  # noqa: E402

PACKAGE = ROOT / "handoff/partner-map-model/yango-coverage-seal"
CLUSTERS = [
    "east-africa-south-asia",
    "gulf-bahrain-ksa-qatar",
    "latam-caspian",
    "nordics",
    "oman",
    "west-africa",
]
DEEPENED_CITIES = frozenset(
    {
        "muscat-oman",
        "cartagena-colombia",
        "manama-bahrain",
        "bergen-norway",
        "lagos-nigeria",
        "doha-qatar",
        "colombo-sri-lanka",
        "fujairah-uae",
        "salalah-dhofar-oman",
        "eastern-province-ksa",
        "helsinki-finland",
        "stavanger-norway",
        "geiranger-norway",
        "abidjan",
        "al-wakrah",
    }
)
LAND_THRESH_KM = 0.05
SNAP_MAX_KM = 2.0


def in_navigable_water(lon: float, lat: float, mask) -> bool:
    if in_water_override(lon, lat):
        return True
    for body in EXTRA_WATER_BODIES:
        bbox = body.get("bbox")
        if bbox and len(bbox) == 4:
            min_lon, max_lon, min_lat, max_lat = bbox
            if min_lon <= lon <= max_lon and min_lat <= lat <= max_lat:
                return True
    try:
        from bolt_yango_shared import is_water

        return is_water(lon, lat, mask)
    except Exception:
        return False
REPORT = ROOT / "grok-routing-output/yango-coverage-seal-report.json"
BINDSET = PACKAGE / "YANGO-COVERAGE-BINDSET.json"
REGION_AFRICA = frozenset({"west-africa", "east-africa-south-asia"})
REGION_CASPIAN = frozenset({"latam-caspian"})


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def canonical_bp_id(handoff_id: str) -> str:
    if handoff_id.startswith("bp-"):
        return handoff_id
    h = hashlib.md5(f"yango|{handoff_id}".encode()).hexdigest()[:10]
    return f"bp-{h}"


def load_all_bps() -> list[dict]:
    out: list[dict] = []
    for cluster in CLUSTERS:
        path = PACKAGE / "boarding-points" / f"BP-DOSSIER-{cluster}.json"
        doc = load_json(path)
        for bp in doc.get("boarding_points") or []:
            row = dict(bp)
            row["cluster"] = cluster
            out.append(row)
    return out


def load_all_corridors() -> list[dict]:
    out: list[dict] = []
    for cluster in CLUSTERS:
        path = PACKAGE / "corridors" / f"CORRIDOR-DOSSIER-{cluster}.json"
        doc = load_json(path)
        for c in doc.get("corridors") or []:
            row = dict(c)
            row["cluster"] = cluster
            out.append(row)
    return out


def load_hand_waypoint_catalogs() -> None:
    for cluster in CLUSTERS:
        path = PACKAGE / "hand_waypoints" / f"yango_hand_waypoints_{cluster}.json"
        if not path.is_file():
            continue
        catalog = load_json(path)
        for key, wps in (catalog.get("waypoints") or {}).items():
            parts = key.split("|", 1)
            if len(parts) == 2:
                HAND_WAYPOINTS[(parts[0], parts[1])] = wps


def poi_name_index(fbt: dict) -> dict[tuple[str, str], str]:
    idx: dict[tuple[str, str], str] = {}
    for poi in fbt.get("poi", []):
        props = poi.get("properties", poi)
        pid = props.get("id")
        city = props.get("parent_city_id")
        name = props.get("name") or props.get("shortName")
        if pid and city and name:
            idx[(city, norm_label(name))] = pid
    return idx


def _bp_coords_ok(pid: str, candidate: dict, bp_idx: dict) -> bool:
    row = bp_idx.get(pid)
    if not row:
        return False
    lng, lat = row["coords"]
    if abs(lng) < 0.01 and abs(lat) < 0.01:
        return False
    if pid.startswith("minor-hotels__") or pid.startswith("major-hotels__"):
        return False
    olng, olat = float(candidate["lng"]), float(candidate["lat"])
    d_km = math.sqrt((lng - olng) ** 2 + (lat - olat) ** 2) * 111.0
    return d_km <= 25.0


def find_existing_bp(
    candidate: dict,
    poi_by_name: dict[tuple[str, str], str],
    bp_idx: dict,
) -> str | None:
    hid = candidate.get("bp_id")
    if hid and hid in bp_idx:
        return hid
    city = candidate["city_id"]
    nl = norm_label(candidate.get("name"))
    if (city, nl) in poi_by_name:
        pid = poi_by_name[(city, nl)]
        if _bp_coords_ok(pid, candidate, bp_idx):
            return pid
    for (c, name), pid in poi_by_name.items():
        if c != city:
            continue
        if not _bp_coords_ok(pid, candidate, bp_idx):
            continue
        if nl in name or name in nl:
            return pid
        ta = set(nl.split())
        tb = set(name.split())
        if len(ta & tb) >= min(2, len(ta), len(tb)):
            return pid
    return None


def mint_poi(
    candidate: dict,
    pid: str,
    lng: float,
    lat: float,
    fbt: dict,
) -> None:
    pois = fbt.setdefault("poi", [])
    name = candidate["name"]
    pois.append(
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lng, lat]},
            "properties": {
                "id": pid,
                "type": "poi",
                "name": name,
                "shortName": name[:40],
                "fullName": name,
                "parent_city_id": candidate["city_id"],
                "bp_type": candidate.get("type", "harbour"),
                "bp_type_label": "Waterfront",
                "status": "operational",
                "confidence": "high" if candidate.get("coords_confidence") != "approx" else "medium",
                "_yango_handoff_bp_id": candidate.get("bp_id"),
                "_yango_coverage_seal": utc_now(),
                "_yango_cluster": candidate.get("cluster"),
            },
        }
    )


def vessel_and_render(dist_nm: float) -> tuple[str, str, str]:
    if dist_nm > 150:
        return "Quanta-LR", "roadmap-amber-dashed", "aspirational"
    if dist_nm >= 70:
        return "Quanta-LR", "roadmap-amber-dashed", "roadmap"
    return "Pioneer II", "solid", "sealed"


def _qa_accept(coords: list[list[float]]) -> tuple[bool, float]:
    ev = evaluate_route(coords)
    return bool(ev.get("qa_pass")), float(ev.get("interior_land_km", 0.0))


def route_geometry(
    a: tuple[float, float],
    b: tuple[float, float],
    handoff_a: str,
    handoff_b: str,
    canonical_a: str,
    canonical_b: str,
    corridor: dict,
    mask,
) -> tuple[list[list[float]], float] | None:
    from channel_solver import connect_chain, densify, get_land_checker, solve_chain, solve_hand  # noqa: WPS433

    manual = corridor.get("hand_waypoints") or []
    wps = [(w[0], w[1]) for w in manual if isinstance(w, (list, tuple)) and len(w) >= 2]
    for key in (
        (handoff_a, handoff_b),
        (handoff_b, handoff_a),
        (canonical_a, canonical_b),
        (canonical_b, canonical_a),
    ):
        if key in HAND_WAYPOINTS and HAND_WAYPOINTS[key]:
            wps = [(w[0], w[1]) for w in HAND_WAYPOINTS[key]]
            break

    lc = get_land_checker()
    mid_lists: list[list[tuple[float, float]]] = []
    if wps:
        mid_lists.append(list(wps))
    if lc:
        chain = connect_chain(lc, [a, b])
        if chain:
            geom = densify(chain)
            ok, land = _qa_accept(geom)
            if ok and land <= LAND_THRESH_KM:
                return geom, land
            if len(chain) > 2:
                mid_lists.append([tuple(p) for p in chain[1:-1]])
    mid_lists.append([])

    for mids in mid_lists:
        if lc:
            for solver, args in (
                (solve_hand, (lc, a, b, list(mids))),
                (solve_chain, (lc, a, b, list(mids))),
            ):
                res = solver(*args)
                if res and res.get("qa_pass") and res.get("geometry"):
                    coords = res["geometry"]
                    land = float(res.get("interior_land_km", 0.0))
                    ok, land2 = _qa_accept(coords)
                    if ok and min(land, land2) <= LAND_THRESH_KM:
                        return coords, min(land, land2) if land > 0 else land2
        if mids:
            coords = build_coastal_path(a, b, mask, manual_waypoints=mids)
            ok, land = _qa_accept(coords)
            if ok and land <= LAND_THRESH_KM:
                return coords, land

    coords = build_coastal_path(a, b, mask)
    ok, land = _qa_accept(coords)
    if ok and land <= LAND_THRESH_KM:
        return coords, land
    return None


def seal_bps(fbt: dict, mask, apply: bool) -> dict:
    candidates = load_all_bps()
    poi_by_name = poi_name_index(fbt)
    bp_idx = build_bp_index(fbt)
    handoff_to_canonical: dict[str, str] = {}
    report = {"sealed": [], "reconciled": [], "dropped": [], "dedupe_deepened": 0}

    for cand in candidates:
        hid = cand["bp_id"]
        existing = find_existing_bp(cand, poi_by_name, bp_idx)
        if existing:
            handoff_to_canonical[hid] = existing
            if cand["city_id"] in DEEPENED_CITIES:
                report["dedupe_deepened"] += 1
            report["reconciled"].append(
                {"handoff_id": hid, "canonical_id": existing, "city_id": cand["city_id"], "name": cand["name"]}
            )
            continue
        pid = canonical_bp_id(hid)
        olng, olat = float(cand["lng"]), float(cand["lat"])
        lng, lat, residual = snap_to_water(olng, olat, mask, max_km=SNAP_MAX_KM)
        if residual > 0.35 and not in_navigable_water(lng, lat, mask):
            if in_navigable_water(olng, olat, mask):
                lng, lat = olng, olat
                residual = 0.0
            else:
                report["dropped"].append(
                    {"handoff_id": hid, "reason": "water_snap_fail", "residual_km": round(residual, 3)}
                )
                continue
        handoff_to_canonical[hid] = pid
        if apply:
            mint_poi(cand, pid, lng, lat, fbt)
            poi_by_name[(cand["city_id"], norm_label(cand["name"]))] = pid
            bp_idx[pid] = {
                "coords": (lng, lat),
                "parent_city_id": cand["city_id"],
                "name": cand["name"],
            }
        report["sealed"].append(
            {"handoff_id": hid, "canonical_id": pid, "city_id": cand["city_id"], "name": cand["name"]}
        )

    silent = len(candidates) - len(report["sealed"]) - len(report["reconciled"]) - len(report["dropped"])
    report["silent_drops"] = max(0, silent)
    report["handoff_to_canonical"] = handoff_to_canonical
    return report


def seal_corridors(
    fbt: dict,
    routes: list,
    handoff_to_canonical: dict[str, str],
    mask,
    apply: bool,
) -> dict:
    load_hand_waypoint_catalogs()
    bp_idx = build_bp_index(fbt)
    cities = build_city_index(fbt)
    existing_ids = {route_id_of(r) for r in routes}
    corridors = load_all_corridors()
    minted: list[dict] = []
    failed: list[dict] = []
    route_map: dict[str, dict] = {}

    for cor in corridors:
        ha, hb = cor["a"], cor["b"]
        ca = handoff_to_canonical.get(ha)
        cb = handoff_to_canonical.get(hb)
        if not ca or not cb or ca not in bp_idx or cb not in bp_idx:
            failed.append({"route_key": cor.get("route_key"), "reason": "missing_bp"})
            continue
        a = tuple(bp_idx[ca]["coords"])
        b = tuple(bp_idx[cb]["coords"])
        geom = route_geometry(a, b, ha, hb, ca, cb, cor, mask)
        if not geom:
            failed.append({"route_key": cor.get("route_key"), "reason": "land_crossing"})
            continue
        coords, land_km = geom
        from_city = bp_idx[ca].get("parent_city_id")
        to_city = bp_idx[cb].get("parent_city_id")
        from_name = bp_idx[ca].get("name", ca)
        to_name = bp_idx[cb].get("name", cb)
        rid = mint_route_id(ca, cb, tag=f"yango_cov_{cor.get('route_key', '')}")
        dist_nm = path_length_km(coords) * NM_PER_KM
        platform, render, link_status = vessel_and_render(dist_nm)
        label = cor.get("name") or f"{from_name} → {to_name}"
        if cor.get("descriptor"):
            label = f"{label} — {cor['descriptor']}"

        feat = make_route_feature(
            ca,
            cb,
            from_name,
            to_name,
            from_city,
            to_city,
            coords,
            cities,
            source="yango_coverage_seal",
            land_km=land_km,
        )
        props = feat["properties"]
        props["id"] = rid
        props["platform"] = platform
        props["distance_nm"] = round(dist_nm, 1)
        props["label"] = label
        props["_yango_route_key"] = cor.get("route_key")
        props["_yango_cluster"] = cor.get("cluster")
        props["_yango_coverage_seal"] = utc_now()
        props["_link_status"] = link_status
        props["_render"] = render

        if apply:
            replaced = False
            for i, r in enumerate(routes):
                if route_id_of(r) == rid:
                    routes[i] = feat
                    replaced = True
                    break
            if not replaced:
                routes.append(feat)
            existing_ids.add(rid)
        if rid not in {m.get("route_id") for m in minted}:
            minted.append(
                {
                    "route_key": cor.get("route_key"),
                    "route_id": rid,
                    "land_km": land_km,
                    "distance_nm": round(dist_nm, 1),
                    "platform": platform,
                    "render": render,
                    "cluster": cor.get("cluster"),
                }
            )
            route_map[cor.get("route_key", rid)] = {
                "route_id": rid,
                "label": label,
                "platform": platform,
                "distance_nm": round(dist_nm, 1),
                "render": render,
                "from_bp": ca,
                "to_bp": cb,
                "cluster": cor.get("cluster"),
            }

    return {"minted": minted, "failed": failed, "route_map": route_map}


def cities_from_manifest() -> list[str]:
    manifest = load_json(PACKAGE / "seal-manifest.json")
    cities: set[str] = set()
    for row in (manifest.get("clusters") or {}).values():
        cities.update(row.get("cities") or [])
    return sorted(cities)


def expand_render_scope(route_map: dict, apply: bool) -> dict:
    cities = cities_from_manifest()
    for tree in (ROOT / "data-clean", ROOT / "partner-pitch"):
        path = tree / "partners/yango.json"
        if not path.is_file():
            continue
        doc = load_json(path)
        footprint_ids = {r.get("id") or r.get("registry_key") for r in doc.get("network_footprint") or []}
        for cid in cities:
            if cid not in footprint_ids:
                doc.setdefault("network_footprint", []).append(
                    {
                        "id": cid,
                        "registry_key": cid,
                        "covered": True,
                        "tier": "corridor_ready",
                        "render": "geometry",
                        "map_promote": True,
                        "label": cid.replace("-", " ").title(),
                        "_binding_source": "grok/yango_coverage_seal",
                    }
                )
        scope = doc.setdefault("_map_scope", {})
        scope["cluster_city_ids"] = cities
        scope["generated"] = utc_now()
        scope["_source"] = "grok/yango_coverage_seal"
        doc.pop("_growth_case_pending", None)
        if apply:
            path.write_text(json.dumps(doc, indent=2) + "\n")
    return {"cities": len(cities), "routes_bound": len(route_map)}


def populate_region_signature_routes(route_map: dict, apply: bool) -> dict:
    regions = load_json(ROOT / "data-clean/region_briefs.json")
    africa_routes: list[dict] = []
    caspian_routes: list[dict] = []
    for _key, row in route_map.items():
        cluster = row.get("cluster")
        entry = {"label": row["label"], "route_id": row["route_id"]}
        if cluster in REGION_AFRICA:
            africa_routes.append(entry)
        elif cluster in REGION_CASPIAN:
            caspian_routes.append(entry)
    if africa_routes:
        existing = regions.get("africa", {}).get("signature_routes") or []
        seen = {e.get("route_id") for e in existing if isinstance(e, dict)}
        for e in africa_routes[:6]:
            if e["route_id"] not in seen:
                existing.append(e)
        regions["africa"]["signature_routes"] = existing
    if caspian_routes:
        regions["caspian"]["signature_routes"] = caspian_routes[:6]
    if apply:
        (ROOT / "data-clean/region_briefs.json").write_text(json.dumps(regions, indent=2) + "\n")
    return {"africa": len(africa_routes), "caspian": len(caspian_routes)}


def regenerate_city_brief_index(apply: bool) -> int:
    brief_dir = ROOT / "data-clean/city_briefs"
    entries = []
    for path in sorted(brief_dir.glob("*.json")):
        if path.name == "_index.json":
            continue
        doc = load_json(path)
        entries.append(
            {
                "city_id": doc.get("city_id") or path.stem,
                "display_name": doc.get("display_name"),
                "region": doc.get("region"),
                "tier": doc.get("tier"),
                "posture": doc.get("posture"),
            }
        )
    index = {
        "generated": utc_now(),
        "total_anchors": len(entries),
        "briefs": len(entries),
        "index": sorted(entries, key=lambda e: e["city_id"]),
    }
    if apply:
        (brief_dir / "_index.json").write_text(json.dumps(index, indent=2) + "\n")
    return len(entries)


def update_coverage_gap(bp_report: dict, corridor_report: dict, apply: bool) -> None:
    gap_path = PACKAGE / "BP-COVERAGE-GAP-yango.json"
    gap = load_json(gap_path)
    canonical_by_handoff = bp_report.get("handoff_to_canonical") or {}
    for row in gap.get("boarding_points") or []:
        hid = row.get("bp_id")
        if hid in canonical_by_handoff:
            row["status"] = "reconciled" if any(
                r["handoff_id"] == hid for r in bp_report.get("reconciled", [])
            ) else "sealed"
            row["canonical_id"] = canonical_by_handoff[hid]
        else:
            drop = next((d for d in bp_report.get("dropped", []) if d.get("handoff_id") == hid), None)
            if drop:
                row["status"] = "dropped"
                row["drop_reason"] = drop.get("reason")
    gap["sealed"] = len(bp_report.get("sealed", []))
    gap["reconciled"] = len(bp_report.get("reconciled", []))
    gap["dropped"] = len(bp_report.get("dropped", []))
    gap["routes_minted"] = len(corridor_report.get("minted", []))
    gap["routes_failed"] = len(corridor_report.get("failed", []))
    gap["updated_at"] = utc_now()
    if apply:
        gap_path.write_text(json.dumps(gap, indent=2) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    dc = ROOT / "data-clean"
    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    routes_raw = load_json(dc / "ROUTES.json")
    routes = route_features(routes_raw)
    mask = load_land_mask()
    poi_before = len(fbt.get("poi", []))

    bp_report = seal_bps(fbt, mask, args.apply)
    if bp_report.get("silent_drops", 0) > 0:
        print(f"✗ silent BP drops: {bp_report['silent_drops']}", file=sys.stderr)
        if args.apply:
            return 1

    corridor_report = seal_corridors(
        fbt,
        routes,
        bp_report["handoff_to_canonical"],
        mask,
        args.apply,
    )

    receipt = {
        "generated_at": utc_now(),
        "partner": "yango",
        "seal_tag": "#79cu-yango-coverage-density",
        "poi_before": poi_before,
        "poi_after": len(fbt.get("poi", [])) if args.apply else poi_before,
        "routes_before": len(route_features(routes_raw)),
        "bp": bp_report,
        "corridors": {
            "minted": len(corridor_report["minted"]),
            "failed": corridor_report["failed"],
        },
    }

    if args.apply:
        save_json(dc / "FEATURES_BY_TYPE.json", fbt)
        save_routes(dc / "ROUTES.json", routes)
        BINDSET.write_text(json.dumps({"generated_at": utc_now(), "routes": corridor_report["route_map"]}, indent=2) + "\n")
        scope_report = expand_render_scope(corridor_report["route_map"], True)
        region_report = populate_region_signature_routes(corridor_report["route_map"], True)
        index_count = regenerate_city_brief_index(True)
        update_coverage_gap(bp_report, corridor_report, True)
        receipt["scope"] = scope_report
        receipt["regions"] = region_report
        receipt["city_brief_index"] = index_count
        receipt["routes_after"] = len(routes)

    REPORT.write_text(json.dumps(receipt, indent=2) + "\n")

    print(json.dumps(receipt, indent=2))
    m, f = len(corridor_report["minted"]), len(corridor_report["failed"])
    print(f"\n{'✓' if args.apply else '·'} yango coverage: BPs sealed={len(bp_report['sealed'])} reconciled={len(bp_report['reconciled'])} | routes {m}/{m+f}")
    if f and args.apply:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())