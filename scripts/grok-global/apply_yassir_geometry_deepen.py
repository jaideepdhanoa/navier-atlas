#!/usr/bin/env python3
"""Yassir geometry deepen — Tangier / Al Hoceima / Algiers channel-solver pass.

Spec: handoff/GROK-SPEC-yassir-geometry-deepen-2026-07-07.md

Mint 5 missing corridors via solve_hand, re-geometry rn-9b522e50433f, stamp cluster_id,
sync finance/partner/city-brief surfaces.

Usage:
  python3 scripts/grok-global/apply_yassir_geometry_deepen.py --dry-run
  python3 scripts/grok-global/apply_yassir_geometry_deepen.py --apply
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "grok-geometry"))
sys.path.insert(0, str(ROOT / "scripts" / "grok-bolt-yango"))
sys.path.insert(0, str(ROOT / "scripts"))

from bolt_yango_routing_shared import (  # noqa: E402
    build_bp_index,
    build_city_index,
    load_json,
    make_route_feature,
    mint_route_id,
    route_features,
    save_json,
    save_routes,
)
from channel_solver import get_land_checker, solve_hand  # noqa: E402

DC = ROOT / "data-clean"
ROUTES_PATH = DC / "ROUTES.json"
FBT_PATH = DC / "FEATURES_BY_TYPE.json"
CORRIDORS_PATH = ROOT / "finance" / "model" / "corridors.json"
REPORT_PATH = ROOT / "grok-routing-output" / "yassir-geometry-deepen-report.json"

TUNISIA_ROUTE_REBIND = {
    ("jorf (mainland)", "ajim (djerba island)"): "rn-4668b16ef32c",
    ("la goulette", "sidi bou said"): "rn-d0ef490c589b",
    ("tunis (la goulette)", "la marsa / gammarth"): "rn-3a88bb1bc7a3",
    ("tunis (tunis marine)", "la goulette"): None,
    ("yasmine hammamet", "nabeul"): None,
    ("sousse (port el kantaoui)", "monastir (marina)"): "rn-27da217834e5",
}

YASSIR_OVERLAY = {"archetype": "super_app", "partner": "yassir"}

MINT_CORRIDORS = [
    {
        "from_bp": "bp-ce43828929",
        "to_bp": "bp-e9cfcaf56d",
        "city_id": "tangier-morocco",
        "cluster_id": "morocco",
        "waypoints": [[-5.74, 35.815], [-5.60, 35.90]],
        "tag": "yassirgeom",
    },
    {
        "from_bp": "bp-ce43828929",
        "to_bp": "bp-470c8ff7bb",
        "city_id": "tangier-morocco",
        "cluster_id": "morocco",
        "waypoints": [[-5.74, 35.815], [-5.55, 35.92]],
        "tag": "yassirgeom",
    },
    {
        "from_bp": "bp-f474677a42",
        "to_bp": "bp-8eb3a85230",
        "city_id": "al-hoceima-morocco",
        "cluster_id": "morocco",
        "waypoints": [[-4.14, 35.19], [-4.25, 35.17]],
        "tag": "yassirgeom",
    },
    {
        "from_bp": "bp-98d845b6b1",
        "to_bp": "bp-996024d3e8",
        "city_id": "algiers-algeria",
        "cluster_id": "algeria",
        "waypoints": [[2.94, 36.815]],
        "tag": "yassirgeom",
    },
    {
        "from_bp": "bp-996024d3e8",
        "to_bp": "bp-9a382970b3",
        "city_id": "algiers-algeria",
        "cluster_id": "algeria",
        "waypoints": [[3.12, 36.785]],
        "tag": "yassirgeom",
    },
]

REGEOMETRY = {
    "rn-011ec4cf5db4": {
        "from_bp": "bp-ce43828929",
        "to_bp": "bp-2bf061805f",
        "waypoints": [],
        "city_id": "tangier-morocco",
        "cluster_id": "morocco",
    },
    "rn-9b522e50433f": {
        "from_bp": "bp-f474677a42",
        "to_bp": "bp-a088ecf7e0",
        "waypoints": [],
        "city_id": "al-hoceima-morocco",
        "cluster_id": "morocco",
    },
}

CITY_ROUTE_BINDINGS = {
    "tangier-morocco": {
        "Tanger City Port <-> Cap Malabata": "rn-011ec4cf5db4",
        "Tanger City Port <-> Ksar es-Seghir": None,  # filled after mint
        "Tanger City Port <-> Tanger Med": None,
    },
    "al-hoceima-morocco": {
        "Al Hoceima port <-> Cala Bonita": "rn-9b522e50433f",
        "Al Hoceima <-> Cala Iris (Quanta-LR)": None,
    },
    "algiers-algeria": {
        "Sidi Fredj <-> Port d'Alger": None,
        "Port d'Alger <-> Aïn Taya": None,
    },
}

MOROCCO_FINANCE_REBIND = {
    "rn-c2a689f7600d": None,  # stale Cala Iris placeholder → new mint id
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def props(feat: dict) -> dict:
    return feat.get("properties") or feat


def norm_label(s: str | None) -> str:
    return (s or "").strip().lower()


def corridor_key(c: dict) -> tuple[str, str]:
    return norm_label(c.get("from")), norm_label(c.get("to"))


def solve_corridor(lc, bp_idx: dict, from_bp: str, to_bp: str, waypoints: list) -> dict | None:
    a = bp_idx[from_bp]["coords"]
    b = bp_idx[to_bp]["coords"]
    return solve_hand(lc, a, b, waypoints)


def mint_or_skip(
    spec: dict,
    routes: list,
    bp_idx: dict,
    cities: dict,
    lc,
    existing_ids: set[str],
    existing_eps: set[tuple[str, str]],
    report: dict,
    *,
    apply: bool,
) -> str | None:
    from_bp = spec["from_bp"]
    to_bp = spec["to_bp"]
    ep = (from_bp, to_bp)
    if ep in existing_eps or (ep[1], ep[0]) in existing_eps:
        for r in routes:
            p = props(r)
            if {p.get("from_node"), p.get("to_node")} == {from_bp, to_bp}:
                report["skipped"].append({"pair": ep, "reason": "exists", "route_id": p.get("id")})
                return p.get("id")
        report["skipped"].append({"pair": ep, "reason": "endpoint_pair_exists"})
        return None

    if not apply:
        rid = mint_route_id(from_bp, to_bp, tag=spec.get("tag", "yassirgeom"))
        report["routes_minted"].append({"route_id": rid, "pair": ep, "dry": True})
        return rid

    solved = solve_corridor(lc, bp_idx, from_bp, to_bp, spec["waypoints"])
    if not solved or not solved.get("qa_pass"):
        report["skipped"].append({"pair": ep, "reason": "solver_fail", "qa": solved})
        return None

    feat = make_route_feature(
        from_bp,
        to_bp,
        bp_idx[from_bp]["name"],
        bp_idx[to_bp]["name"],
        spec["city_id"],
        spec["city_id"],
        solved["geometry"],
        cities,
        source="yassir_geometry_deepen",
        land_km=solved.get("interior_land_km", 0.0),
        cluster_id=spec["cluster_id"],
        cluster_city_id=spec["city_id"],
    )
    p = props(feat)
    rid = mint_route_id(from_bp, to_bp, tag=spec.get("tag", "yassirgeom"))
    while rid in existing_ids:
        rid = mint_route_id(from_bp, to_bp, tag=spec.get("tag", "yassirgeom") + "x")
    p["id"] = rid
    p["distance_nm"] = solved["sea_nm"]
    p["cluster_id"] = spec["cluster_id"]
    p["cluster_city_id"] = spec["city_id"]
    p["_yassir_geometry_deepen"] = utc_now()
    p["_channel_solver_method"] = solved.get("method")
    routes.append(feat)
    existing_ids.add(rid)
    existing_eps.add(ep)
    existing_eps.add((ep[1], ep[0]))
    report["routes_minted"].append(
        {
            "route_id": rid,
            "pair": ep,
            "nm": solved["sea_nm"],
            "land_km": solved.get("interior_land_km", 0.0),
            "qa_pass": solved.get("qa_pass"),
        }
    )
    return rid


def regeometry_route(
    rid: str,
    spec: dict,
    routes: list,
    bp_idx: dict,
    lc,
    report: dict,
    *,
    apply: bool,
) -> None:
    for feat in routes:
        p = props(feat)
        if p.get("id") != rid:
            continue
        solved = solve_corridor(lc, bp_idx, spec["from_bp"], spec["to_bp"], spec["waypoints"])
        if not solved or not solved.get("qa_pass"):
            report["regeometry"].append({"route_id": rid, "status": "solver_fail"})
            return
        report["regeometry"].append(
            {
                "route_id": rid,
                "status": "ok",
                "before_nm": p.get("distance_nm"),
                "after_nm": solved["sea_nm"],
                "land_km": solved.get("interior_land_km", 0.0),
            }
        )
        if apply:
            feat["geometry"] = {"type": "LineString", "coordinates": solved["geometry"]}
            p["distance_nm"] = solved["sea_nm"]
            p["_land_km_interior"] = round(solved.get("interior_land_km", 0.0), 4)
            p["cluster_id"] = spec["cluster_id"]
            p["cluster_city_id"] = spec["city_id"]
            p["_yassir_geometry_deepen"] = utc_now()
        return
    report["regeometry"].append({"route_id": rid, "status": "not_found"})


def stamp_cluster_ids(routes: list, report: dict, *, apply: bool) -> None:
    targets = {"tangier-morocco", "al-hoceima-morocco", "algiers-algeria"}
    for feat in routes:
        p = props(feat)
        cc = p.get("cluster_city_id") or p.get("from_city_id") or p.get("to_city_id")
        if cc not in targets:
            continue
        want = "morocco" if cc.endswith("-morocco") else "algeria"
        if p.get("cluster_id") != want:
            report["cluster_stamps"].append({"route_id": p.get("id"), "cluster_id": want})
            if apply:
                p["cluster_id"] = want


def apply_yassir_overlay(c: dict) -> dict:
    out = copy.deepcopy(c)
    out.update(YASSIR_OVERLAY)
    if out.get("archetype") in ("ridehail", "tourism", "commute", "intercity", "urban_coastal"):
        out["archetype"] = "super_app"
    return out


def route_row_from_atlas(routes: list, route_id: str) -> dict | None:
    for feat in routes:
        p = props(feat)
        if p.get("id") != route_id:
            continue
        return {
            "route_id": route_id,
            "from": p.get("from_label") or p.get("from"),
            "to": p.get("to_label") or p.get("to"),
            "distance_nm": p.get("distance_nm"),
            "vessel": "Pioneer II",
            "from_node_id": p.get("from_node"),
            "to_node_id": p.get("to_node"),
            "from_city_id": p.get("from_city_id"),
            "to_city_id": p.get("to_city_id"),
            "country": "Algeria",
            **YASSIR_OVERLAY,
            "_atlas_spine": True,
        }
    return None


def finance_patch(corridors_doc: dict, routes: list, minted: dict[tuple[str, str], str], report: dict, *, apply: bool) -> None:
    markets = corridors_doc.setdefault("markets", {})

    # Tunisia dedupe
    tunisia = markets.get("yassir-tunisia")
    if tunisia:
        fixes = []
        for c in tunisia.get("corridors", []):
            key = corridor_key(c)
            new_rid = TUNISIA_ROUTE_REBIND.get(key)
            if new_rid is None and key in TUNISIA_ROUTE_REBIND:
                if c.get("route_id") is not None:
                    fixes.append({"od": f"{c.get('from')} ↔ {c.get('to')}", "from": c.get("route_id"), "to": None})
                    if apply:
                        c["route_id"] = None
                        c["_tunisia_route_rebind"] = utc_now()
            elif new_rid and c.get("route_id") != new_rid:
                fixes.append({"od": f"{c.get('from')} ↔ {c.get('to')}", "from": c.get("route_id"), "to": new_rid})
                if apply:
                    c["route_id"] = new_rid
                    c["_tunisia_route_rebind"] = utc_now()
        report["finance"]["tunisia_rebinds"] = fixes

    # Morocco stale Cala Iris id
    for market_key in ("yassir-morocco", "morocco"):
        market = markets.get(market_key)
        if not market:
            continue
        iris_rid = minted.get(("bp-f474677a42", "bp-8eb3a85230"))
        if not iris_rid:
            continue
        for c in market.get("corridors", []):
            if c.get("route_id") == "rn-c2a689f7600d":
                report["finance"]["morocco_cala_iris_rebind"] = {
                    "market": market_key,
                    "from": "rn-c2a689f7600d",
                    "to": iris_rid,
                }
                if apply:
                    c["route_id"] = iris_rid
                    c["from_node_id"] = "bp-f474677a42"
                    c["to_node_id"] = "bp-8eb3a85230"
                    c["_yassir_geometry_deepen"] = utc_now()

    # Algeria reconcile to full atlas spine
    algeria_ids = sorted(
        {
            props(r).get("id")
            for r in routes
            if props(r).get("cluster_id") == "algeria" and str(props(r).get("id", "")).startswith("rn-")
        }
    )
    existing = markets.get("yassir-algeria", {})
    by_rid = {c.get("route_id"): c for c in existing.get("corridors", []) if c.get("route_id")}
    new_corridors: list[dict] = []
    for rid in algeria_ids:
        if rid in by_rid:
            new_corridors.append(apply_yassir_overlay(by_rid[rid]))
        else:
            row = route_row_from_atlas(routes, rid)
            if row:
                row["L3_locals"] = {}
                row["_economics_status"] = "spine_only_pending_l3"
                new_corridors.append(row)
    report["finance"]["yassir_algeria"] = {
        "before": len(existing.get("corridors", [])),
        "after": len(new_corridors),
        "route_ids": algeria_ids,
    }
    if apply:
        existing.update(
            {
                "partner": "yassir",
                "label": "Yassir Algeria — sealed Maghreb corridors",
                "capture_rate": 0.15,
                "fleet_basis": "aspirational",
                "_source_market_inheritance": "algeria_atlas_spine",
            }
        )
        existing["corridors"] = new_corridors
        markets["yassir-algeria"] = existing


def patch_city_briefs(route_map: dict[str, dict[str, str]], report: dict, *, apply: bool) -> None:
    bindings = {
        "tangier-morocco": [
            ("Tanger City Port <-> Cap Malabata", route_map["tangier-morocco"].get("cap_malabata")),
            ("Tanger City Port <-> Ksar es-Seghir", route_map["tangier-morocco"].get("ksar")),
            ("Tanger City Port <-> Tanger Med", route_map["tangier-morocco"].get("tanger_med")),
        ],
        "al-hoceima-morocco": [
            ("Al Hoceima port <-> Cala Bonita", route_map["al-hoceima-morocco"].get("cala_bonita")),
            ("Al Hoceima <-> Cala Iris (Quanta-LR)", route_map["al-hoceima-morocco"].get("cala_iris")),
        ],
        "algiers-algeria": [
            ("Sidi Fredj <-> Port d'Alger", route_map["algiers-algeria"].get("sidi_fredj")),
            ("Port d'Alger <-> Aïn Taya", route_map["algiers-algeria"].get("ain_taya")),
        ],
    }
    for city_id, sigs in bindings.items():
        path = DC / "city_briefs" / f"{city_id}.json"
        if not path.exists():
            continue
        doc = load_json(path)
        doc["signature_routes"] = [{"label": label, "route_id": rid} for label, rid in sigs if rid]
        doc["_yassir_geometry_deepen"] = utc_now()
        if "no boarding points are sealed" in (doc.get("summary") or "").lower():
            doc["summary"] = doc["summary"].replace(
                "Note: no boarding points are sealed here yet — Al Hoceima is a priority mint candidate.",
                "Sealed boarding points and corridors now bound on Atlas.",
            ).replace(
                "Note: no boarding points are sealed here yet — Tangier is a priority mint candidate.",
                "Sealed boarding points and corridors now bound on Atlas.",
            )
        report["city_briefs"][city_id] = [s[1] for s in sigs if s[1]]
        if apply:
            save_json(path, doc)


def patch_yassir_partner(route_map: dict[str, dict[str, str]], report: dict, *, apply: bool) -> None:
    journeys = [
        {
            "market_id": "yassir-morocco",
            "entries": [
                {
                    "from": "Tanger City Port",
                    "to": "Cap Malabata",
                    "route_id": route_map["tangier-morocco"].get("cap_malabata"),
                    "distance_nm": 3.4,
                    "city_id": "tangier-morocco",
                },
                {
                    "from": "Tanger City Port",
                    "to": "Ksar es-Seghir",
                    "route_id": route_map["tangier-morocco"].get("ksar"),
                    "city_id": "tangier-morocco",
                },
                {
                    "from": "Tanger City Port",
                    "to": "Tanger Med",
                    "route_id": route_map["tangier-morocco"].get("tanger_med"),
                    "city_id": "tangier-morocco",
                },
                {
                    "from": "Al Hoceima port",
                    "to": "Cala Bonita",
                    "route_id": route_map["al-hoceima-morocco"].get("cala_bonita"),
                    "city_id": "al-hoceima-morocco",
                },
                {
                    "from": "Al Hoceima",
                    "to": "Cala Iris",
                    "route_id": route_map["al-hoceima-morocco"].get("cala_iris"),
                    "city_id": "al-hoceima-morocco",
                },
            ],
        },
        {
            "market_id": "yassir-algeria",
            "entries": [
                {
                    "from": "Sidi Fredj marina",
                    "to": "Port d'Alger",
                    "route_id": route_map["algiers-algeria"].get("sidi_fredj"),
                    "city_id": "algiers-algeria",
                },
                {
                    "from": "Port d'Alger",
                    "to": "Aïn Taya",
                    "route_id": route_map["algiers-algeria"].get("ain_taya"),
                    "city_id": "algiers-algeria",
                },
            ],
        },
    ]
    for base in (ROOT / "partner-pitch" / "partners", DC / "partners"):
        path = base / "yassir.json"
        if not path.exists():
            continue
        doc = load_json(path)
        for block in journeys:
            market = next((m for m in doc.get("markets", []) if m.get("id") == block["market_id"]), None)
            if not market:
                continue
            unlocked = []
            for e in block["entries"]:
                if not e.get("route_id"):
                    continue
                unlocked.append(
                    {
                        "from": e["from"],
                        "to": e["to"],
                        "with_navier": "Sealed Atlas corridor — geometry deepen pass.",
                        "route_id": e["route_id"],
                        "_link_status": "geometry_sealed",
                        "display": "map",
                        "economics_status": "spine_only_pending_l3",
                        "city_id": e.get("city_id"),
                    }
                )
            if unlocked:
                market["journeys_unlocked"] = unlocked + [
                    j for j in market.get("journeys_unlocked", []) if not j.get("route_id")
                ]
                if block["market_id"] == "yassir-morocco":
                    market["status"] = "country-supported; Tangier + Al Hoceima corridors sealed"
                if block["market_id"] == "yassir-algeria":
                    market["status"] = "home-market geometry sealed; Algiers bay deepened"
            geom = doc.setdefault("geometry_update_2026_07_07", {})
            geom["deepened_markets"] = list(
                set((geom.get("deepened_markets") or []) + [block["market_id"].replace("yassir-", "")])
            )
            geom["sealed_at"] = utc_now()
        report["partner"][str(path.relative_to(ROOT))] = "patched"
        if apply:
            save_json(path, doc)


def audit_routes(routes: list, report: dict) -> None:
    null_cluster = []
    land_crossers = []
    for feat in routes:
        p = props(feat)
        rid = p.get("id")
        if not p.get("cluster_id"):
            null_cluster.append(rid)
        land = p.get("_land_km_interior")
        if land and float(land) > 0.4:
            land_crossers.append({"route_id": rid, "land_km": land})
    per_market = {}
    for city in ("tangier-morocco", "al-hoceima-morocco", "algiers-algeria"):
        rts = [
            props(r).get("id")
            for r in routes
            if props(r).get("cluster_city_id") == city or props(r).get("from_city_id") == city
        ]
        per_market[city] = sorted(set(r for r in rts if r))
    report["audit"] = {
        "null_cluster_count": len(null_cluster),
        "null_cluster_sample": null_cluster[:10],
        "land_crossers": land_crossers,
        "per_market_route_ids": per_market,
    }


def update_seal(report: dict, *, apply: bool) -> None:
    if not apply:
        return
    import subprocess

    subprocess.run([sys.executable, str(ROOT / "scripts" / "grok-econ-reseal" / "update_seal_hashes.py")], check=True)
    report["seal_updated"] = True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    apply = args.apply and not args.dry_run

    fbt = load_json(FBT_PATH)
    routes = route_features(load_json(ROUTES_PATH))
    corridors_doc = load_json(CORRIDORS_PATH)
    bp_idx = build_bp_index(fbt)
    cities = build_city_index(fbt)
    lc = get_land_checker()

    existing_ids = {props(r).get("id") for r in routes}
    existing_eps: set[tuple[str, str]] = set()
    for r in routes:
        p = props(r)
        fn, tn = p.get("from_node"), p.get("to_node")
        if fn and tn:
            existing_eps.add((fn, tn))
            existing_eps.add((tn, fn))

    report: dict = {
        "generated": utc_now(),
        "mode": "apply" if apply else "dry-run",
        "routes_minted": [],
        "regeometry": [],
        "skipped": [],
        "cluster_stamps": [],
        "finance": {},
        "city_briefs": {},
        "partner": {},
    }

    minted: dict[tuple[str, str], str] = {}
    for spec in MINT_CORRIDORS:
        rid = mint_or_skip(
            spec, routes, bp_idx, cities, lc, existing_ids, existing_eps, report, apply=apply
        )
        if rid:
            minted[(spec["from_bp"], spec["to_bp"])] = rid

    for rid, spec in REGEOMETRY.items():
        regeometry_route(rid, spec, routes, bp_idx, lc, report, apply=apply)

    stamp_cluster_ids(routes, report, apply=apply)
    finance_patch(corridors_doc, routes, minted, report, apply=apply)

    route_map = {
        "tangier-morocco": {
            "cap_malabata": "rn-011ec4cf5db4",
            "ksar": minted.get(("bp-ce43828929", "bp-e9cfcaf56d")),
            "tanger_med": minted.get(("bp-ce43828929", "bp-470c8ff7bb")),
        },
        "al-hoceima-morocco": {
            "cala_bonita": "rn-9b522e50433f",
            "cala_iris": minted.get(("bp-f474677a42", "bp-8eb3a85230")),
        },
        "algiers-algeria": {
            "sidi_fredj": minted.get(("bp-98d845b6b1", "bp-996024d3e8")),
            "ain_taya": minted.get(("bp-996024d3e8", "bp-9a382970b3")),
        },
    }
    patch_city_briefs(route_map, report, apply=apply)
    patch_yassir_partner(route_map, report, apply=apply)
    audit_routes(routes, report)

    if apply:
        save_routes(ROUTES_PATH, routes)
        save_json(CORRIDORS_PATH, corridors_doc)
        update_seal(report, apply=True)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    save_json(REPORT_PATH, report)
    print(json.dumps({"summary": report["audit"], "minted": report["routes_minted"], "regeometry": report["regeometry"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())