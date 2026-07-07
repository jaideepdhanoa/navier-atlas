#!/usr/bin/env python3
"""Yassir follow-ups — El Jadida mint/restamp + Senegal/Algeria finance inheritance.

Spec: handoff/dark-map/GROK-SPEC-yassir-followups-2026-07-06.md

Usage:
  python3 scripts/grok-global/apply_yassir_followups.py --dry-run
  python3 scripts/grok-global/apply_yassir_followups.py --apply
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from partner_scope_py import load_clusters  # noqa: E402

DC = ROOT / "data-clean"
FBT_PATH = DC / "FEATURES_BY_TYPE.json"
ROUTES_PATH = DC / "ROUTES.json"
CLUSTERS_PATH = DC / "CLUSTERS.json"
SEAL_PATH = DC / "SEAL.json"
CORRIDORS_PATH = ROOT / "finance" / "model" / "corridors.json"
REPORT_PATH = ROOT / "grok-routing-output" / "yassir-followups-report.json"

EL_JADIDA_ROUTES = {
    "rn-7492176da39c": "to",
    "rn-aacdddb20e68": "to",
    "rn-4873b929b710": "to",
    "rn-ca3c8a1beb62": "to",
}

EL_JADIDA_BPS = [
    {
        "name": "El Jadida fishing/commercial port",
        "lon": -8.501,
        "lat": 33.256,
        "source": "UNESCO #1058; Wikipedia El Jadida",
    },
    {
        "name": "Mazagan Beach & Golf Resort marina",
        "lon": -8.415,
        "lat": 33.363,
        "source": "visitmorocco.com; Mazagan Beach resort",
    },
]

TUNISIA_ROUTE_REBIND = {
    ("jorf (mainland)", "ajim (djerba island)"): "rn-4668b16ef32c",
    ("la goulette", "sidi bou said"): "rn-d0ef490c589b",
    ("tunis (la goulette)", "la marsa / gammarth"): "rn-3a88bb1bc7a3",
    ("tunis (tunis marine)", "la goulette"): None,
    ("yasmine hammamet", "nabeul"): None,
    ("sousse (port el kantaoui)", "monastir (marina)"): "rn-27da217834e5",
}

YASSIR_OVERLAY = {
    "archetype": "super_app",
    "partner": "yassir",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path):
    return json.loads(path.read_text())


def save_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def props(feat: dict) -> dict:
    return feat.get("properties") or feat


def bp_id_for(city_id: str, name: str) -> str:
    h = hashlib.md5(f"el-jadida|{city_id}|{name}".encode()).hexdigest()[:10]
    return f"bp-{h}"


def norm_label(s: str | None) -> str:
    return (s or "").strip().lower()


def corridor_key(c: dict) -> tuple[str, str]:
    return norm_label(c.get("from")), norm_label(c.get("to"))


def mint_el_jadida(fbt: dict, clusters_doc: dict, routes: list, report: dict, *, apply: bool) -> None:
    city_id = "el-jadida-morocco"
    anchor = [-8.501, 33.256]

    found = False
    for bucket in ("city", "priority_city"):
        for feat in fbt.get(bucket, []) or []:
            if props(feat).get("id") == city_id:
                found = True
                if apply:
                    feat.setdefault("geometry", {"type": "Point"})["coordinates"] = anchor
                    props(feat).setdefault("cluster_id", "morocco")
                    props(feat)["_yassir_followup_mint"] = utc_now()
    if not found:
        report["el_jadida"]["city_added"] = True
        if apply:
            fbt.setdefault("city", []).append(
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": anchor},
                    "properties": {
                        "id": city_id,
                        "type": "city",
                        "name": "El Jadida",
                        "shortName": "El Jadida",
                        "fullName": "El Jadida",
                        "country": "Morocco",
                        "region": "Maghreb",
                        "platform_class": "dual-platform",
                        "cluster_id": "morocco",
                        "_yassir_followup_mint": utc_now(),
                    },
                }
            )

    for c in clusters_doc.get("clusters") or []:
        if c.get("cluster_id") != "morocco":
            continue
        members = list(c.get("member_city_ids") or [])
        if city_id not in members:
            report["el_jadida"]["cluster_member"] = True
            if apply:
                members.append(city_id)
                c["member_city_ids"] = members
                c["members_present"] = len(members)
                c["_yassir_followup_mint"] = utc_now()

    pois = fbt.get("poi", []) or []
    for bp in EL_JADIDA_BPS:
        pid = bp_id_for(city_id, bp["name"])
        exists = any(props(p).get("id") == pid for p in pois)
        report["el_jadida"]["bps"].append({"bp_id": pid, "name": bp["name"], "exists": exists})
        if not exists and apply:
            pois.append(
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [bp["lon"], bp["lat"]]},
                    "properties": {
                        "id": pid,
                        "type": "poi",
                        "name": bp["name"],
                        "shortName": bp["name"][:48],
                        "fullName": bp["name"],
                        "parent_city_id": city_id,
                        "bp_type": "marina",
                        "status": "operational",
                        "confidence": "high",
                        "source_url": bp["source"],
                        "_yassir_followup_mint": utc_now(),
                    },
                }
            )
    if apply:
        fbt["poi"] = pois

    for feat in routes:
        p = props(feat)
        rid = p.get("id")
        if rid not in EL_JADIDA_ROUTES:
            continue
        side = EL_JADIDA_ROUTES[rid]
        field = f"{side}_city_id"
        if p.get(field) == "casablanca-morocco":
            report["el_jadida"]["restamps"].append({"route_id": rid, "side": side})
            if apply:
                p[field] = city_id
                if p.get("from_city_id") == p.get("to_city_id") == city_id:
                    p["cluster_city_id"] = city_id
                elif side == "to":
                    p["cluster_city_id"] = p.get("from_city_id") or city_id
                else:
                    p["cluster_city_id"] = p.get("to_city_id") or city_id
                p["_yassir_el_jadida_restamp"] = utc_now()


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


def apply_yassir_overlay(c: dict) -> dict:
    out = copy.deepcopy(c)
    out.update(YASSIR_OVERLAY)
    if out.get("archetype") in ("ridehail", "tourism", "commute", "intercity", "urban_coastal"):
        out["archetype"] = "super_app"
    return out


def finance_inheritance(corridors_doc: dict, routes: list, report: dict, *, apply: bool) -> None:
    markets = corridors_doc.setdefault("markets", {})

    # yassir-senegal from yango-senegal
    yango = markets.get("yango-senegal")
    if yango:
        yassir_sn = copy.deepcopy(yango)
        yassir_sn.update(
            {
                "partner": "yassir",
                "label": "Yassir Senegal — Dakar, Gorée & Petite Côte",
                "capture_rate": 0.18,
                "fleet_basis": "aspirational",
                "_source_market_inheritance": "yango-senegal",
                "_evidence_tier": "country_supported",
                "_partner_evidence": "Yassir operates in Senegal; spine inherits yango-senegal L3 1:1 per finance-corridor inheritance contract.",
            }
        )
        yassir_sn["corridors"] = [apply_yassir_overlay(c) for c in yango.get("corridors", [])]
        report["finance"]["yassir_senegal"] = {
            "corridors": len(yassir_sn["corridors"]),
            "with_route_id": sum(1 for c in yassir_sn["corridors"] if c.get("route_id")),
        }
        if apply:
            markets["yassir-senegal"] = yassir_sn

    # yassir-algeria reconcile to full algeria atlas spine (7 routes)
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

    # Tunisia rn-74a61d330456 dedupe / rebind
    tunisia = markets.get("yassir-tunisia")
    if tunisia:
        fixes = []
        for c in tunisia.get("corridors", []):
            key = corridor_key(c)
            new_rid = TUNISIA_ROUTE_REBIND.get(key)
            if new_rid is None and key in TUNISIA_ROUTE_REBIND:
                if c.get("route_id") != new_rid:
                    fixes.append({"od": f"{c.get('from')} ↔ {c.get('to')}", "from": c.get("route_id"), "to": None})
                    if apply:
                        c["route_id"] = None
                        c["_tunisia_route_rebind"] = utc_now()
            elif new_rid and c.get("route_id") != new_rid:
                fixes.append({"od": f"{c.get('from')} ↔ {c.get('to')}", "from": c.get("route_id"), "to": new_rid})
                if apply:
                    c["route_id"] = new_rid
                    c["_tunisia_route_rebind"] = utc_now()
        report["finance"]["yassir_tunisia_rebinds"] = fixes


def update_seal(report: dict, *, apply: bool) -> None:
    if not apply or not SEAL_PATH.exists():
        return
    seal = load_json(SEAL_PATH)
    import hashlib as hl

    for key in ("ROUTES.json", "FEATURES_BY_TYPE.json", "CLUSTERS.json"):
        path = DC / key
        if path.exists():
            digest = hl.sha256(path.read_bytes()).hexdigest()
            seal.setdefault("files", {})[key] = {"sha256": digest, "updated": utc_now()}
    save_json(SEAL_PATH, seal)
    report["seal_updated"] = True


def patch_yassir_partner_economics(report: dict) -> None:
    """Sync growth_case floor + Senegal/Algeria sub-market economics from cascade."""
    agg = load_json(ROOT / "finance" / "recal" / "agg-yassir.json")
    rollup = agg.get("rollup") or agg
    for slug in ("yassir",):
        for base in (ROOT / "partner-pitch" / "partners", DC / "partners"):
            path = base / f"{slug}.json"
            if not path.exists():
                continue
            doc = load_json(path)
            gc = doc.setdefault("growth_case", {})
            gf = rollup.get("grounded_floor") or {}
            et = rollup.get("estimated_total") or {}
            gc["grounded_floor"] = {
                "fleet": gf.get("fleet"),
                "market_rev_yr": gf.get("market_rev_yr"),
                "co2_saved_t_yr": gf.get("co2_saved_t_yr"),
                "transport_spend_pool_yr": gf.get("transport_spend_pool_yr"),
                "effective_capture": gf.get("effective_capture"),
            }
            gc["estimated_total"] = {
                "fleet": et.get("fleet"),
                "market_rev_yr": et.get("market_rev_yr"),
                "transport_spend_pool_yr": et.get("transport_spend_pool_yr"),
                "effective_capture": et.get("effective_capture"),
            }
            gc["grounded_floor_by_market"] = rollup.get("grounded_floor_by_market")
            by_market = rollup.get("grounded_floor_by_market") or {}
            for m in doc.get("markets") or []:
                mid = m.get("id")
                if mid == "yassir-senegal":
                    m["status"] = "country-supported display-ready; 12 sealed corridors; economics cascaded"
                    m["economics_status"] = "model_cascaded_after_grok_seal"
                    sn = by_market.get("yassir-senegal") or {}
                    for ph in m.get("phases") or []:
                        if ph.get("n") == 1:
                            ph["boats"] = sn.get("fleet") or 1
                            ph.setdefault("_economics", {})["status"] = "cascaded"
                            ph["narrative"] = (
                                "Bring the Yassir water tier to Dakar's peninsula and the Petite Côte; "
                                f"grounded floor ~{sn.get('fleet', 1)} boat(s) on Gorée/Ngor spine."
                            )
                    for j in m.get("journeys_unlocked") or []:
                        if j.get("route_id") and j.get("economics_status") == "pending_cascade":
                            j["economics_status"] = "cascaded"
                    for ph in m.get("phases") or []:
                        for fr in ph.get("featured_routes") or []:
                            if fr.get("economics_status") == "pending_cascade":
                                fr["economics_status"] = "cascaded"
                if mid == "yassir-algeria":
                    dz = by_market.get("yassir-algeria") or {}
                    m["status"] = "home-market geometry sealed; 7 atlas corridors; economics cascaded"
                    m["economics_status"] = "model_cascaded_after_grok_seal"
                    m["summary"] = (
                        "Yassir's home market. Algiers, Oran, Mostaganem, Béjaïa and Annaba carry sealed corridors; "
                        f"grounded floor ~{dz.get('fleet', 1)} boat(s) on sourced L3 spine."
                    )
            for ph in doc.get("phases") or []:
                pe = (doc.get("growth_case") or {}).get("phase_economics") or {}
                horizons = {h.get("id"): h for h in pe.get("horizons") or []}
                if ph.get("n") == 1 and horizons.get("prove"):
                    ph["boats"] = horizons["prove"].get("fleet_boats")
                if ph.get("n") == 2 and horizons.get("scale"):
                    ph["boats"] = horizons["scale"].get("fleet_boats_est")
                if ph.get("n") == 3 and horizons.get("mature"):
                    ph["boats"] = horizons["mature"].get("fleet_boats_est_pioneer_equiv")
            doc["economics_status"] = "model_cascaded_maghreb_senegal_algeria"
            nt = doc.setdefault("network_thesis", {})
            stats = {s.get("label"): s for s in nt.get("stats") or [] if isinstance(s, dict)}
            if "economics status" in stats:
                stats["economics status"]["value"] = "model_cascaded_maghreb_senegal_algeria"
            save_json(path, doc)
    report["partner_economics_patch"] = "ok"


def run_finance_cascade(report: dict) -> None:
    model = ROOT / "finance" / "model"
    recal = ROOT / "finance" / "recal"
    finance = ROOT / "finance"
    partner = "yassir"
    agg_out = recal / f"agg-{partner}.json"
    growth_out = recal / f"growth-{partner}.json"
    frontend_out = recal / f"growth-frontend-{partner}.json"
    partner_json = ROOT / "partner-pitch" / "partners" / f"{partner}.json"

    steps = [
        [sys.executable, str(model / "aggregate.py"), "--partner", partner, "--json", str(agg_out)],
        [sys.executable, str(model / "growth.py"), "--partner", partner, "--agg", str(agg_out), "--json", str(growth_out)],
        [
            sys.executable,
            str(model / "growth_frontend_block.py"),
            "--partner",
            partner,
            "--growth",
            str(growth_out),
            "--rollup",
            str(agg_out),
            "--out",
            str(frontend_out),
        ],
        [
            sys.executable,
            str(finance / "splice_growth_into_partner.py"),
            "--partner",
            partner,
            "--growth",
            str(growth_out),
            "--frontend",
            str(frontend_out),
            "--partner-json",
            str(partner_json),
        ],
    ]
    for cmd in steps:
        subprocess.run(cmd, check=True, cwd=str(ROOT))
    patch_yassir_partner_economics(report)
    report["finance_cascade"] = "ok"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--cascade", action="store_true", help="Run economics cascade after finance patch")
    args = ap.parse_args()
    apply = args.apply and not args.dry_run

    fbt = load_json(FBT_PATH)
    clusters_doc = load_json(CLUSTERS_PATH)
    routes_raw = load_json(ROUTES_PATH)
    routes = routes_raw if isinstance(routes_raw, list) else routes_raw.get("features", [])
    corridors_doc = load_json(CORRIDORS_PATH)

    report: dict = {
        "generated": utc_now(),
        "mode": "apply" if apply else "dry-run",
        "el_jadida": {"bps": [], "restamps": []},
        "finance": {},
    }

    mint_el_jadida(fbt, clusters_doc, routes, report, apply=apply)
    finance_inheritance(corridors_doc, routes, report, apply=apply)

    if apply:
        save_json(FBT_PATH, fbt)
        save_json(CLUSTERS_PATH, clusters_doc)
        save_json(ROUTES_PATH, routes)
        save_json(CORRIDORS_PATH, corridors_doc)
        update_seal(report, apply=True)

    if apply and args.cascade:
        run_finance_cascade(report)

    save_json(REPORT_PATH, report)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())