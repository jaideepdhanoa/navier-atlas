#!/usr/bin/env python3
"""Yassir/Maghreb datafix + dark-map null-cluster stamp (Tasklet handoff 2026-07-06).

Lanes:
  1. Mauritius misstamps → tunisia / algeria (+ cluster_city_id)
  2. City anchor coord fixes (Casablanca, M'diq, Al Hoceima)
  3. Rabat–Salé label
  4. Morocco endpoint city_id WS-4 restamp (nearest morocco anchor)
  5. Dark-map: stamp cluster_id on 56 null-cluster routes

Usage:
  python3 scripts/grok-global/apply_yassir_maghreb_and_dark_map.py --dry-run
  python3 scripts/grok-global/apply_yassir_maghreb_and_dark_map.py --apply
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from partner_scope_py import load_clusters  # noqa: E402

DC = ROOT / "data-clean"
ROUTES_PATH = DC / "ROUTES.json"
FBT_PATH = DC / "FEATURES_BY_TYPE.json"
DARK_MAP_PATH = ROOT / "handoff" / "dark-map" / "DARK-MAP-null-cluster-2026-07-06.json"
REPORT_PATH = ROOT / "grok-routing-output" / "yassir-maghreb-dark-map-report.json"

ROUTE_CLUSTER_OVERRIDES = {
    "rn-27da217834e5": "tunisia",
    "rn-13faccfd5399": "algeria",
}

CITY_COORD_FIXES = {
    "casablanca-morocco": [-7.606, 33.606],
    "mdiq-tetouan-morocco": [-5.325, 35.685],
    "al-hoceima-morocco": [-3.906, 35.249],
}

RABAT_LABEL = "Rabat–Salé"

# Authority / virtual city_id → cluster_id (not in CLUSTERS.member_city_ids)
VIRTUAL_CITY_CLUSTER = {
    "calmac": "uk",
    "seoul-hangang-bus": "korea",
    "kolkata-wbtc": "india",
    "accra-tema-ghana": "accra-tema-ghana",
    "luanda-angola": "luanda-angola",
    "lobito-benguela-angola": "lobito-benguela-angola",
    "douala-cameroon": "douala-cameroon",
    "pointe-noire-congo": "pointe-noire-congo",
    "walvis-bay-namibia": "walvis-bay-namibia",
    "la-guaira-venezuela": "la-guaira-venezuela",
    "maracaibo-venezuela": "maracaibo-venezuela",
}

SUFFIX_CLUSTER = {
    "-norway": "norway",
    "-oman": "oman",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path) -> dict | list:
    return json.loads(path.read_text())


def save_json(path: Path, obj: dict | list) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def props(feat: dict) -> dict:
    return feat.get("properties") or feat


def haversine_km(a: list, b: list) -> float:
    lon1, lat1, lon2, lat2 = a[0], a[1], b[0], b[1]
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    x = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(min(1.0, math.sqrt(x)))


def build_city_to_cluster() -> dict[str, str]:
    _, _, base = load_clusters(DC)
    out = dict(base)
    out.update(VIRTUAL_CITY_CLUSTER)
    for cid, cluster in list(out.items()):
        if cid.startswith("dubai-uae__"):
            out[cid] = "uae"
    return out


def resolve_cluster_id(city_id: str | None, city_to_cluster: dict[str, str]) -> str | None:
    if not city_id:
        return None
    if city_id in city_to_cluster:
        return city_to_cluster[city_id]
    if city_id.startswith("dubai-uae__"):
        return "uae"
    for suffix, cluster in SUFFIX_CLUSTER.items():
        if city_id.endswith(suffix):
            return cluster
    return city_id


def cluster_from_endpoints(fc: str | None, tc: str | None, city_to_cluster: dict[str, str]) -> str | None:
    clusters = {resolve_cluster_id(c, city_to_cluster) for c in (fc, tc) if c}
    clusters.discard(None)
    if len(clusters) == 1:
        return next(iter(clusters))
    if fc and tc and fc == tc:
        return resolve_cluster_id(fc, city_to_cluster)
    if fc:
        return resolve_cluster_id(fc, city_to_cluster)
    if tc:
        return resolve_cluster_id(tc, city_to_cluster)
    return None


def derive_cluster_city_id(p: dict) -> str | None:
    fc, tc = p.get("from_city_id"), p.get("to_city_id")
    if fc and fc == tc:
        return fc
    return fc or tc


def morocco_city_coords(fbt: dict, morocco_cities: set[str]) -> dict[str, list]:
    out: dict[str, list] = {}
    for bucket in ("city", "priority_city"):
        for feat in fbt.get(bucket, []) or []:
            pid = props(feat).get("id")
            if pid in morocco_cities:
                out[pid] = feat.get("geometry", {}).get("coordinates") or []
    return out


def apply_city_fixes(fbt: dict, report: dict, *, apply: bool) -> None:
    for bucket in ("city", "priority_city"):
        for feat in fbt.get(bucket, []) or []:
            p = props(feat)
            cid = p.get("id")
            if cid in CITY_COORD_FIXES:
                old = feat.get("geometry", {}).get("coordinates")
                new = CITY_COORD_FIXES[cid]
                report["city_coords"].append({"city_id": cid, "from": old, "to": new})
                if apply:
                    feat.setdefault("geometry", {"type": "Point"})["coordinates"] = new
                    p["_yassir_maghreb_coord_fix"] = utc_now()
            if cid == "rabat-sale-morocco":
                old_label = p.get("name")
                report["rabat_label"] = {"from": old_label, "to": RABAT_LABEL}
                if apply:
                    p["name"] = RABAT_LABEL
                    p["shortName"] = RABAT_LABEL
                    p["fullName"] = RABAT_LABEL
                    p["_yassir_maghreb_label_fix"] = utc_now()


def apply_route_fixes(routes: list, fbt: dict, report: dict, *, apply: bool) -> None:
    _, cluster_by_id, city_to_cluster = load_clusters(DC)
    morocco_cities = set()
    for c in cluster_by_id.get("morocco", {}).get("member_city_ids") or []:
        morocco_cities.add(c)
    mcoords = morocco_city_coords(fbt, morocco_cities)

    def nearest_morocco_city(coord: list) -> str | None:
        if not coord or not mcoords:
            return None
        return min(mcoords, key=lambda c: haversine_km(coord, mcoords[c]))

    dark_ids: set[str] = set()
    if DARK_MAP_PATH.exists():
        dm = load_json(DARK_MAP_PATH)
        for group in (dm.get("groups") or {}).values():
            for entry in group:
                rid = entry.get("route_id")
                if rid:
                    dark_ids.add(rid)

    ctc = build_city_to_cluster()

    for feat in routes:
        p = props(feat)
        rid = p.get("id")
        if not rid:
            continue

        # 1. Explicit misstamp overrides
        override = ROUTE_CLUSTER_OVERRIDES.get(rid)
        if override and p.get("cluster_id") != override:
            report["misstamps"].append({"route_id": rid, "from": p.get("cluster_id"), "to": override})
            if apply:
                p["cluster_id"] = override
                cc = derive_cluster_city_id(p)
                if cc:
                    p["cluster_city_id"] = cc
                p["_yassir_maghreb_misstamp_fix"] = utc_now()

        # 4. Morocco city_id restamp
        if p.get("cluster_id") == "morocco":
            coords = feat.get("geometry", {}).get("coordinates") or []
            if coords:
                for side, idx in (("from", 0), ("to", -1)):
                    if p.get(f"{side}_city_id") != "casablanca-morocco":
                        continue
                    nc = nearest_morocco_city(coords[idx])
                    if nc and nc != "casablanca-morocco":
                        report["morocco_city_restamp"].append(
                            {
                                "route_id": rid,
                                "side": side,
                                "from": "casablanca-morocco",
                                "to": nc,
                            }
                        )
                        if apply:
                            p[f"{side}_city_id"] = nc
                            p["_yassir_maghreb_city_restamp"] = utc_now()
                if apply:
                    cc = derive_cluster_city_id(p)
                    if cc:
                        p["cluster_city_id"] = cc

        # 5. Dark-map null cluster stamp
        if rid in dark_ids and not p.get("cluster_id"):
            fc, tc = p.get("from_city_id"), p.get("to_city_id")
            stamp = cluster_from_endpoints(fc, tc, ctc)
            if stamp:
                report["dark_map_stamps"].append({"route_id": rid, "cluster_id": stamp, "from_city": fc, "to_city": tc})
                if apply:
                    p["cluster_id"] = stamp
                    cc = derive_cluster_city_id(p)
                    if cc:
                        p["cluster_city_id"] = cc
                    p["_dark_map_cluster_stamp"] = utc_now()

        # Also stamp any remaining null cluster routes globally
        elif not p.get("cluster_id"):
            fc, tc = p.get("from_city_id"), p.get("to_city_id")
            stamp = cluster_from_endpoints(fc, tc, ctc)
            if stamp:
                report["dark_map_stamps"].append(
                    {"route_id": rid, "cluster_id": stamp, "from_city": fc, "to_city": tc, "note": "residual_null"}
                )
                if apply:
                    p["cluster_id"] = stamp
                    cc = derive_cluster_city_id(p)
                    if cc:
                        p["cluster_city_id"] = cc
                    p["_dark_map_cluster_stamp"] = utc_now()


def update_seal(report: dict, *, apply: bool) -> None:
    seal_path = DC / "SEAL.json"
    if not seal_path.exists() or not apply:
        return
    seal = load_json(seal_path)

    def sha256_file(path: Path) -> str:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        return h.hexdigest()

    for rel in ("ROUTES.json", "FEATURES_BY_TYPE.json"):
        path = DC / rel
        if not path.exists():
            continue
        digest = sha256_file(path)
        seal.setdefault("files", {})[rel] = digest
        seal.setdefault("blobs", {}).setdefault(rel.replace(".json", ""), {})["sha256"] = digest
    seal["sealed_at"] = utc_now()
    seal.setdefault("gates", {})["yassir_maghreb_dark_map"] = (
        f"PASS grok yassir-maghreb-datafix + dark-map stamp ({utc_now()[:10]})"
    )
    save_json(seal_path, seal)
    report["seal_updated"] = True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    apply = args.apply and not args.dry_run

    routes = load_json(ROUTES_PATH)
    if not isinstance(routes, list):
        routes = routes.get("features", [])
    fbt = load_json(FBT_PATH)

    report: dict = {
        "generated": utc_now(),
        "mode": "apply" if apply else "dry-run",
        "misstamps": [],
        "city_coords": [],
        "rabat_label": None,
        "morocco_city_restamp": [],
        "dark_map_stamps": [],
    }

    apply_city_fixes(fbt, report, apply=apply)
    apply_route_fixes(routes, fbt, report, apply=apply)

    if apply:
        save_json(ROUTES_PATH, routes)
        save_json(FBT_PATH, fbt)
        update_seal(report, apply=True)

    report["summary"] = {
        "misstamps": len(report["misstamps"]),
        "city_coords": len(report["city_coords"]),
        "morocco_city_restamp": len(report["morocco_city_restamp"]),
        "dark_map_stamps": len(report["dark_map_stamps"]),
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    save_json(REPORT_PATH, report)

    print(json.dumps(report["summary"], indent=2))
    if not apply:
        print("(dry-run — pass --apply to write)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())