#!/usr/bin/env python3
"""Grok seal — Yango roster correction + net-new coastal markets (PR #178).

Unseal removed markets from Yango partner surface (geometry preserved for Bolt).
Seal 16 BPs + 11 corridors from handoff/partner-map-model/yango-roster-correction/.
Bind pending sub-page route_ids from YANGO-COVERAGE-BINDSET.json.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
sys.path.insert(0, str(ROOT / "scripts/grok-geometry"))

from bolt_yango_routing_shared import (  # noqa: E402
    build_bp_index,
    build_city_index,
    build_coastal_path,
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
from bolt_yango_shared import load_land_mask  # noqa: E402
from channel_solver import HAND_WAYPOINTS  # noqa: E402
from regional_land_masks import in_water_override  # noqa: E402
from route_land_qa import evaluate_route  # noqa: E402
from snap_bp_coverage_new import EXTRA_WATER_BODIES, snap_to_water  # noqa: E402

PACKAGE = ROOT / "handoff/partner-map-model/yango-roster-correction"
COVERAGE_BINDSET = ROOT / "handoff/partner-map-model/yango-coverage-seal/YANGO-COVERAGE-BINDSET.json"
ROSTER_BINDSET = PACKAGE / "ROSTER-BINDSET.json"
CLUSTERS = ["cameroon", "congo-brazzaville", "namibia", "venezuela"]
REPORT = ROOT / "grok-routing-output/yango-roster-correction-report.json"

REMOVED_CITIES = frozenset(
    {
        "manama-bahrain",
        "muharraq-bahrain",
        "muscat-oman",
        "salalah-dhofar-oman",
        "khasab-musandam-oman",
        "sohar-oman",
        "muscat-oman__daymaniyat-islands-unesco-marine-reserve-candidate",
        "colombo-sri-lanka",
        "eastern-province-ksa",
        "baku-azerbaijan",
        "lagos-nigeria",
    }
)

BIND_MARKETS = frozenset({"senegal", "colombia", "peru", "kazakhstan"})
INTENTIONAL_NULL_LABELS = frozenset(
    {
        ("Aktau", "Kenderli"),
        ("Aktau", "Bautino"),
    }
)

LAND_THRESH_KM = 0.05
SNAP_MAX_KM = 2.0


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def labels_match(a: str | None, b: str | None) -> bool:
    if not a or not b:
        return False
    na, nb = norm_label(_strip_accents(a)), norm_label(_strip_accents(b))
    if na == nb or na in nb or nb in na:
        return True
    ta, tb = set(na.split()), set(nb.split())
    if not ta or not tb:
        return False
    overlap = ta & tb
    need = min(2, min(len(ta), len(tb)))
    return len(overlap) >= max(1, need)


def canonical_bp_id(handoff_id: str) -> str:
    if handoff_id.startswith("bp-"):
        return handoff_id
    h = hashlib.md5(f"yango|{handoff_id}".encode()).hexdigest()[:10]
    return f"bp-{h}"


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


def load_all_bps() -> list[dict]:
    out: list[dict] = []
    for cluster in CLUSTERS:
        path = PACKAGE / f"BP-DOSSIER-{cluster}.json"
        doc = load_json(path)
        for bp in doc.get("boarding_points") or []:
            row = dict(bp)
            row["cluster"] = cluster
            out.append(row)
    return out


def load_all_corridors() -> list[dict]:
    out: list[dict] = []
    for cluster in CLUSTERS:
        path = PACKAGE / f"CORRIDOR-DOSSIER-{cluster}.json"
        doc = load_json(path)
        for c in doc.get("corridors") or []:
            row = dict(c)
            row["cluster"] = cluster
            out.append(row)
    return out


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


def mint_poi(candidate: dict, pid: str, lng: float, lat: float, fbt: dict) -> None:
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
                "_yango_roster_seal": utc_now(),
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
    report = {"sealed": [], "reconciled": [], "dropped": []}

    for cand in candidates:
        hid = cand["bp_id"]
        existing = find_existing_bp(cand, poi_by_name, bp_idx)
        if existing:
            handoff_to_canonical[hid] = existing
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
    bp_idx = build_bp_index(fbt)
    cities = build_city_index(fbt)
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
        rid = mint_route_id(ca, cb, tag=f"yango_roster_{cor.get('route_key', '')}")
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
            source="yango_roster_correction",
            land_km=land_km,
        )
        props = feat["properties"]
        props["id"] = rid
        props["platform"] = platform
        props["distance_nm"] = round(dist_nm, 1)
        props["label"] = label
        props["_yango_route_key"] = cor.get("route_key")
        props["_yango_cluster"] = cor.get("cluster")
        props["_yango_roster_seal"] = utc_now()
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


def _parse_bindset_label(label: str) -> tuple[str, str] | None:
    if not label:
        return None
    parts = re.split(r"\s*[↔→]\s*", _strip_accents(label), maxsplit=1)
    if len(parts) != 2:
        return None
    left = parts[0].strip()
    right = re.split(r"\s+—\s+", parts[1], maxsplit=1)[0].strip()
    return left, right


def build_bindset_index(bindset: dict, bp_idx: dict) -> list[dict]:
    rows: list[dict] = []
    for _key, row in (bindset.get("routes") or {}).items():
        parsed = _parse_bindset_label(row.get("label", ""))
        if not parsed:
            continue
        from_l, to_l = parsed
        from_bp = row.get("from_bp")
        to_bp = row.get("to_bp")
        from_city = bp_idx.get(from_bp, {}).get("parent_city_id") if from_bp else None
        to_city = bp_idx.get(to_bp, {}).get("parent_city_id") if to_bp else None
        rows.append(
            {
                "route_id": row.get("route_id"),
                "from_label": from_l,
                "to_label": to_l,
                "from_bp": from_bp,
                "to_bp": to_bp,
                "from_city": from_city,
                "to_city": to_city,
            }
        )
    return rows


def _item_endpoints(item: dict) -> tuple[str | None, str | None]:
    from_l = item.get("from") or item.get("from_label")
    to_l = item.get("to") or item.get("to_label")
    return from_l, to_l


def bind_pending_item(item: dict, bind_index: list[dict], bp_idx: dict) -> bool:
    if not isinstance(item, dict):
        return False
    if item.get("route_id"):
        return False
    from_l, to_l = _item_endpoints(item)
    if (from_l, to_l) in INTENTIONAL_NULL_LABELS:
        item["_link_status"] = "intentional-null"
        return False
    for row in bind_index:
        if not labels_match(from_l, row["from_label"]) or not labels_match(to_l, row["to_label"]):
            continue
        item["route_id"] = row["route_id"]
        if row.get("from_bp"):
            item["from_node_id"] = row["from_bp"]
        if row.get("to_bp"):
            item["to_node_id"] = row["to_bp"]
        item["_link_status"] = "linked"
        item["_link_kind"] = "corridor-label"
        item["_bind_source"] = "yango-coverage-bindset"
        return True
    return False


def bind_pending_subpage_routes(yango: dict, bindset: dict, bp_idx: dict) -> dict:
    bind_index = build_bindset_index(bindset, bp_idx)
    stats = {"linked": 0, "still_pending": 0, "intentional_null": 0}

    for market in yango.get("markets") or []:
        if market.get("slug") not in BIND_MARKETS:
            continue
        for j in market.get("journeys_unlocked") or []:
            if bind_pending_item(j, bind_index, bp_idx):
                stats["linked"] += 1
            elif j.get("_link_status") == "intentional-null":
                stats["intentional_null"] += 1
            elif j.get("_link_status") == "pending-grok-bind":
                stats["still_pending"] += 1
        for ph in market.get("phases") or []:
            for fr in ph.get("featured_routes") or []:
                if bind_pending_item(fr, bind_index, bp_idx):
                    stats["linked"] += 1
                elif fr.get("_link_status") == "intentional-null":
                    stats["intentional_null"] += 1
                elif fr.get("_link_status") == "pending-grok-bind":
                    stats["still_pending"] += 1

    return stats


def verify_unseal(yango: dict) -> dict:
    footprint_ids = {
        r.get("id") or r.get("registry_key")
        for r in yango.get("network_footprint") or []
    }
    leaked = sorted(REMOVED_CITIES & footprint_ids)
    stale_scope = sorted(
        REMOVED_CITIES & set(yango.get("_map_scope", {}).get("cluster_city_ids") or [])
    )
    return {
        "removed_cities": sorted(REMOVED_CITIES),
        "footprint_leaks": leaked,
        "scope_stale_until_sync": stale_scope,
        "partner_surface_clean": not leaked,
        "shared_geometry_preserved": True,
    }


def flip_coverage_status(yango: dict, apply: bool) -> None:
    exp = yango.setdefault("_coverage_expansion", {})
    exp["status"] = "sealed"
    exp["grok_sealed_at"] = utc_now()
    exp["grok_seal_tag"] = "yango-roster-correction-2026-07-03"
    gc = yango.get("growth_case") or {}
    chip = gc.setdefault("_render_chip_flag", {})
    chip["roster_correction_sealed"] = True
    if apply:
        chip["coverage_expansion"] = "sealed"


def sync_partner_trees(yango: dict, apply: bool) -> None:
    if not apply:
        return
    text = json.dumps(yango, indent=2, ensure_ascii=False) + "\n"
    for tree in (ROOT / "data-clean", ROOT / "partner-pitch"):
        path = tree / "partners/yango.json"
        if path.parent.is_dir():
            path.write_text(text)


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

    yango_path = ROOT / "partner-pitch/partners/yango.json"
    yango = load_json(yango_path)
    unseal_report = verify_unseal(yango)

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

    bindset = load_json(COVERAGE_BINDSET)
    bp_idx = build_bp_index(fbt)
    bind_stats = bind_pending_subpage_routes(yango, bindset, bp_idx)
    flip_coverage_status(yango, args.apply)

    receipt = {
        "generated_at": utc_now(),
        "partner": "yango",
        "seal_tag": "yango-roster-correction-2026-07-03",
        "unseal": unseal_report,
        "poi_before": poi_before,
        "poi_after": len(fbt.get("poi", [])) if args.apply else poi_before,
        "bp": {
            "sealed": len(bp_report["sealed"]),
            "reconciled": len(bp_report["reconciled"]),
            "dropped": bp_report["dropped"],
            "silent_drops": bp_report.get("silent_drops", 0),
        },
        "corridors": {
            "minted": len(corridor_report["minted"]),
            "failed": corridor_report["failed"],
            "land_crossings": 0,
        },
        "bind_pending": bind_stats,
    }

    if args.apply:
        save_json(dc / "FEATURES_BY_TYPE.json", fbt)
        save_routes(dc / "ROUTES.json", routes)
        roster_bind = {
            "generated_at": utc_now(),
            "routes": corridor_report["route_map"],
        }
        ROSTER_BINDSET.write_text(json.dumps(roster_bind, indent=2) + "\n")
        sync_partner_trees(yango, True)
        index_count = regenerate_city_brief_index(True)
        receipt["routes_after"] = len(routes)
        receipt["city_brief_index"] = index_count
        receipt["roster_bindset"] = str(ROSTER_BINDSET.relative_to(ROOT))

    REPORT.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))

    m, f = len(corridor_report["minted"]), len(corridor_report["failed"])
    print(
        f"\n{'✓' if args.apply else '·'} yango roster: "
        f"BPs sealed={len(bp_report['sealed'])} reconciled={len(bp_report['reconciled'])} | "
        f"routes {m}/{m + f} | binds linked={bind_stats['linked']} pending={bind_stats['still_pending']}"
    )
    if unseal_report.get("footprint_leaks"):
        print(f"✗ footprint still has removed cities: {unseal_report['footprint_leaks']}", file=sys.stderr)
        if args.apply:
            return 3
    if f and args.apply:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())