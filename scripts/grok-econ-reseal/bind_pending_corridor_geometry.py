#!/usr/bin/env python3
"""
Bind pending corridor geometry: fix finance node chips, wire existing gold route_ids,
and seed missing Mozambique boarding points.

Run before mint_gcn_corridor_routes.py and mint_pending_corridor_routes.py.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CORRIDORS = ROOT / "finance/model/corridors.json"

sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
from bolt_yango_routing_shared import (  # noqa: E402
    build_bp_index,
    norm_label,
    resolve_corridor_endpoints,
    route_features,
    route_id_of,
)

# Corridor label tokens → sealed city_id (first match wins per side)
CITY_HINTS: list[tuple[tuple[str, ...], str]] = [
    (("vilankulo", "vilanculos", "bazaruto"), "vilanculos-bazaruto-mozambique"),
    (("pemba", "paquitequete", "quirimbas", "ibo island"), "pemba-mozambique"),
    (("inhambane",), "inhambane-mozambique"),
    (("maxixe",), "inhambane-mozambique"),
    (("beira", "porto da beira"), "beira-mozambique"),
    (("buzi",), "beira-mozambique"),
    (("inhaca", "kanyaka"), "maputo-mozambique"),
    (("portuguese island", "santa maria", "ilha dos portugueses"), "maputo-mozambique"),
    (("catembe", "maputo", "porto de maputo"), "maputo-mozambique"),
    (("mykonos", "delos", "tourlos"), "mykonos-greece"),
    (("paros", "parikia", "antiparos"), "paros-greece"),
    (("naxos",), "naxos-greece"),
    (("santorini", "thira", "athinios"), "santorini-greece"),
    (("ios",), "mykonos-greece"),
    (("rhodes", "mandraki", "dodecanese"), "rhodes-dodecanese-greece"),
    (("marmaris",), "bodrum-turkey"),
    (("fethiye",), "bodrum-turkey"),
    (("kusadasi", "kuşadası"), "cesme-izmir-turkey"),
    (("piraeus", "athens", "aegina", "poros", "spetses", "agistri", "hydra", "saronic"), "athens-saronic-greece"),
    (("dubrovnik", "cilipi", "cavtat", "elaphiti"), "dubrovnik-croatia"),
    (("korcula", "korčula", "korcula"), "korcula-croatia"),
    (("mljet", "polace", "sobra"), "korcula-croatia"),
    (("zadar", "kornati", "biograd", "murter"), "zadar-croatia"),
    (("kotor",), "kotor-montenegro"),
    (("limassol",), "limassol-cyprus"),
    (("larnaca", "lca"), "larnaca-cyprus"),
    (("paphos", "pfo", "coral bay"), "paphos-cyprus"),
    (("ayia napa", "protaras"), "ayia-napa-cyprus"),
    (("tallinn", "aegna"), "tallinn-estonia"),
    (("dublin", "dalkey", "killiney", "docklands"), "dublin-ireland"),
    (("como", "bellagio"), "lake-como-italy"),
    (("portofino", "cinque terre"), "portofino-cinque-terre-italy"),
    (("amalfi", "positano", "capri", "sorrento"), "amalfi-coast-italy"),
    (("the red sea", "shura island", "shura"), "red-sea-global-ksa"),
    (("amaala", "triple bay"), "amaala-ksa"),
    (("sindalah", "magna", "oxagon"), "neom-sindalah-ksa"),
    (("neom",), "neom-ksa"),
    (("tangier",), "tangier-morocco"),
    (("casablanca",), "casablanca-morocco"),
    (("agadir",), "agadir-essaouira-morocco"),
    (("al hoceima", "al-hoceima"), "al-hoceima-morocco"),
    (("split", "hvar", "brac"), "split-croatia"),
]

# Existing gold routes keyed by (market, from_label, to_label)
GOLD_ROUTE_WIRE: dict[tuple[str, str, str], str] = {
    ("bolt-greece", "Mykonos", "Paros"): "edge__paros-greece__mykonos",
    ("bolt-greece", "Mykonos", "Santorini (Thira)"): "edge__santorini-greece__mykonos",
}

# Finance node chips that are known copy-paste errors → always re-infer from labels
STALE_NODE_CHIPS = frozenset(
    {
        "athens-saronic-greece",
        "maputo-mozambique",
        "split-croatia",
        "amalfi-coast-italy",
        "limassol-cyprus",
        "neom-ksa",
    }
)

SINDALAH_GCN_EPS = {
    "from": "NEOM Sindalah — Sindalah Marina (IGY)",
    "to": "Magna resort cluster jetty (NEOM north-coast)",
}

CROATIA_CYPRUS_CITIES = [
    {"id": "zadar-croatia", "name": "Zadar", "coords": [15.2317, 44.1194], "country": "Croatia"},
    {"id": "paphos-cyprus", "name": "Paphos", "coords": [32.4242, 34.7750], "country": "Cyprus"},
    {"id": "ayia-napa-cyprus", "name": "Ayia Napa", "coords": [33.9998, 34.9828], "country": "Cyprus"},
]

CROATIA_CYPRUS_BPS = [
    {
        "id": "bp-zadar-gazenica-port",
        "name": "Zadar Gaženica Ferry Port",
        "shortName": "Zadar Gaženica Port",
        "parent_city_id": "zadar-croatia",
        "coords": [15.2317, 44.1194],
        "bp_type": "ferry_terminal",
    },
    {
        "id": "bp-murter-hramina-marina",
        "name": "Murter Hramina Marina (Kornati gateway)",
        "shortName": "Murter Hramina Marina",
        "parent_city_id": "zadar-croatia",
        "coords": [15.5922, 43.8250],
        "bp_type": "marina",
    },
    {
        "id": "bp-kornati-piskera",
        "name": "Kornati NP — ACI Piškera / Vela Proversa anchorage",
        "shortName": "Kornati Piškera Anchorage",
        "parent_city_id": "zadar-croatia",
        "coords": [15.3500, 43.8000],
        "bp_type": "anchorage",
    },
    {
        "id": "bp-paphos-harbour",
        "name": "Paphos Harbour (Kato Paphos / Castle quay)",
        "shortName": "Paphos Harbour",
        "parent_city_id": "paphos-cyprus",
        "coords": [32.4078, 34.7547],
        "bp_type": "harbour",
    },
    {
        "id": "bp-paphos-airport-jetty",
        "name": "Paphos International Airport (PFO) waterfront jetty",
        "shortName": "Paphos Airport Jetty",
        "parent_city_id": "paphos-cyprus",
        "coords": [32.4892, 34.7180],
        "bp_type": "jetty",
    },
    {
        "id": "bp-coral-bay-peyia",
        "name": "Coral Bay (Peyia) resort cluster jetty",
        "shortName": "Coral Bay Jetty",
        "parent_city_id": "paphos-cyprus",
        "coords": [32.3789, 34.8519],
        "bp_type": "jetty",
    },
    {
        "id": "bp-ayia-napa-marina",
        "name": "Ayia Napa Marina",
        "shortName": "Ayia Napa Marina",
        "parent_city_id": "ayia-napa-cyprus",
        "coords": [34.0019, 34.9828],
        "bp_type": "marina",
    },
    {
        "id": "bp-protaras-jetty",
        "name": "Protaras Fig Tree Bay / Pernera jetty",
        "shortName": "Protaras Jetty",
        "parent_city_id": "ayia-napa-cyprus",
        "coords": [34.0583, 35.0133],
        "bp_type": "jetty",
    },
    {
        "id": "bp-larnaca-airport-jetty",
        "name": "Larnaca International Airport (LCA) waterfront jetty",
        "shortName": "Larnaca Airport Jetty",
        "parent_city_id": "larnaca-cyprus",
        "coords": [33.6231, 34.8751],
        "bp_type": "jetty",
    },
]

MOZAMBIQUE_BPS = [
    {
        "id": "bp-inhaca-island-jetty",
        "name": "Inhaca Island Jetty (KaNyaka / MPDC)",
        "shortName": "Inhaca Island Jetty",
        "parent_city_id": "maputo-mozambique",
        "coords": [32.991, -25.968],
        "bp_type": "ferry_terminal",
    },
    {
        "id": "bp-portuguese-island-landing",
        "name": "Portuguese Island / Santa Maria Beach Landing",
        "shortName": "Portuguese Island Landing",
        "parent_city_id": "maputo-mozambique",
        "coords": [32.72, -26.05],
        "bp_type": "beach_landing",
    },
    {
        "id": "bp-inhambane-ferry-pier",
        "name": "Inhambane City Ferry Pier",
        "shortName": "Inhambane Ferry Pier",
        "parent_city_id": "inhambane-mozambique",
        "coords": [35.383, -23.865],
        "bp_type": "ferry_terminal",
    },
    {
        "id": "bp-maxixe-town-jetty",
        "name": "Maxixe Town Jetty",
        "shortName": "Maxixe Town Jetty",
        "parent_city_id": "inhambane-mozambique",
        "coords": [35.347, -23.859],
        "bp_type": "ferry_terminal",
    },
    {
        "id": "bp-beira-port",
        "name": "Porto da Beira (Beira Waterfront)",
        "shortName": "Porto da Beira",
        "parent_city_id": "beira-mozambique",
        "coords": [34.838, -19.815],
        "bp_type": "port",
    },
    {
        "id": "bp-buzi-estuary-landing",
        "name": "Buzi Town Landing (Buzi River Estuary)",
        "shortName": "Buzi Estuary Landing",
        "parent_city_id": "beira-mozambique",
        "coords": [34.55, -20.133],
        "bp_type": "jetty",
    },
]

MOZAMBIQUE_CITIES = [
    {
        "id": "inhambane-mozambique",
        "name": "Inhambane",
        "coords": [35.383, -23.865],
    },
    {
        "id": "beira-mozambique",
        "name": "Beira",
        "coords": [34.838, -19.815],
    },
]


def load_json(p: Path):
    return json.loads(p.read_text())


def save_json(p: Path, obj):
    p.write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n")


def city_from_text(text: str | None) -> str | None:
    if not text:
        return None
    n = norm_label(text)
    for tokens, city_id in CITY_HINTS:
        if any(t in n for t in tokens):
            return city_id
    return None


def infer_endpoint_cities(corridor: dict) -> tuple[str | None, str | None]:
    eps = corridor.get("endpoint_boarding_points") or {}
    from_city = city_from_text(eps.get("from") or corridor.get("from"))
    to_city = city_from_text(eps.get("to") or corridor.get("to"))
    if not from_city:
        from_city = city_from_text(corridor.get("from"))
    if not to_city:
        to_city = city_from_text(corridor.get("to"))
    return from_city, to_city


def should_patch_nodes(corridor: dict) -> bool:
    if corridor.get("_needs_geometry_binding"):
        return True
    a, b = corridor.get("from_node_id"), corridor.get("to_node_id")
    if not a or not b:
        return False
    if a in STALE_NODE_CHIPS or b in STALE_NODE_CHIPS:
        return True
    fc, tc = infer_endpoint_cities(corridor)
    if a == b:
        if fc and tc and fc != tc:
            return True
        if fc and fc != a:
            return True
    if fc and a != fc:
        return True
    if tc and b != tc:
        return True
    return False


def patch_corridor_nodes(corridor: dict) -> bool:
    if not should_patch_nodes(corridor):
        return False
    fc, tc = infer_endpoint_cities(corridor)
    if not fc:
        return False
    tc = tc or fc
    changed = False
    if corridor.get("from_node_id") != fc:
        corridor["from_node_id"] = fc
        changed = True
    if corridor.get("to_node_id") != tc:
        corridor["to_node_id"] = tc
        changed = True
    if changed:
        corridor["_geometry_bound_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return changed


def wire_route_id(market: str, corridor: dict, gold_ids: set[str]) -> bool:
    if corridor.get("route_id") and corridor["route_id"] in gold_ids:
        return False
    key = (market, corridor.get("from", ""), corridor.get("to", ""))
    rid = GOLD_ROUTE_WIRE.get(key)
    if rid and rid in gold_ids:
        corridor["route_id"] = rid
        corridor["_geometry_bound_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        return True
    return False


def existing_ids(fbt: dict) -> set[str]:
    ids = set()
    for tier in ("city", "priority_city"):
        for feat in fbt.get(tier, []):
            pid = (feat.get("properties") or {}).get("id")
            if pid:
                ids.add(pid)
    for poi in fbt.get("poi", []):
        pid = (poi.get("properties") or {}).get("id")
        if pid:
            ids.add(pid)
    return ids


def ensure_mozambique_surface(fbt: dict) -> dict:
    report = {"cities_added": [], "bps_added": [], "bps_reparented": []}
    seen = existing_ids(fbt)

    for city in MOZAMBIQUE_CITIES:
        if city["id"] in seen:
            continue
        fbt.setdefault("city", []).append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": city["coords"]},
                "properties": {
                    "id": city["id"],
                    "type": "city",
                    "name": city["name"],
                    "shortName": city["name"],
                    "fullName": city["name"],
                    "country": "Mozambique",
                    "region": "Africa",
                    "platform_class": "dual-platform",
                    "coords_resolved": True,
                    "coords_source": "geometry_bind_2026-06-20",
                    "confidence": "medium",
                    "status": "operational",
                    "tier_sort_key": 2,
                },
            }
        )
        seen.add(city["id"])
        report["cities_added"].append(city["id"])

    fbt["city"].sort(key=lambda x: (x.get("properties") or {}).get("id", ""))

    for bp in MOZAMBIQUE_BPS:
        if bp["id"] not in seen:
            fbt.setdefault("poi", []).append(
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": bp["coords"]},
                    "properties": {
                        "id": bp["id"],
                        "type": "poi",
                        "name": bp["name"],
                        "shortName": bp["shortName"],
                        "fullName": bp["name"],
                        "parent_city_id": bp["parent_city_id"],
                        "bp_type": bp["bp_type"],
                        "coords_resolved": True,
                        "confidence": "medium",
                        "status": "operational",
                        "_geometry_bind": True,
                        "last_enriched": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                    },
                }
            )
            seen.add(bp["id"])
            report["bps_added"].append(bp["id"])

    for poi in fbt.get("poi", []):
        props = poi.get("properties") or {}
        if props.get("id") == "bp-w6-b6cfc3305f" and props.get("parent_city_id") != "pemba-mozambique":
            props["parent_city_id"] = "pemba-mozambique"
            report["bps_reparented"].append("bp-w6-b6cfc3305f→pemba-mozambique")

    return report


def ensure_croatia_cyprus_surface(fbt: dict) -> dict:
    report = {"cities_added": [], "bps_added": []}
    seen = existing_ids(fbt)

    for city in CROATIA_CYPRUS_CITIES:
        if city["id"] in seen:
            continue
        fbt.setdefault("city", []).append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": city["coords"]},
                "properties": {
                    "id": city["id"],
                    "type": "city",
                    "name": city["name"],
                    "shortName": city["name"],
                    "fullName": city["name"],
                    "country": city["country"],
                    "region": "Europe",
                    "platform_class": "dual-platform",
                    "coords_resolved": True,
                    "coords_source": "geometry_bind_2026-06-20",
                    "confidence": "medium",
                    "status": "operational",
                    "tier_sort_key": 2,
                },
            }
        )
        seen.add(city["id"])
        report["cities_added"].append(city["id"])

    fbt["city"].sort(key=lambda x: (x.get("properties") or {}).get("id", ""))

    for bp in CROATIA_CYPRUS_BPS:
        if bp["id"] in seen:
            continue
        fbt.setdefault("poi", []).append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": bp["coords"]},
                "properties": {
                    "id": bp["id"],
                    "type": "poi",
                    "name": bp["name"],
                    "shortName": bp["shortName"],
                    "fullName": bp["name"],
                    "parent_city_id": bp["parent_city_id"],
                    "bp_type": bp["bp_type"],
                    "coords_resolved": True,
                    "confidence": "medium",
                    "status": "operational",
                    "_geometry_bind": True,
                    "last_enriched": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                },
            }
        )
        seen.add(bp["id"])
        report["bps_added"].append(bp["id"])

    return report


def patch_sindalah_gcn_eps(corridor: dict) -> bool:
    rid = corridor.get("route_id") or ""
    if not str(rid).startswith("gcn-7bd6efa01a"):
        return False
    eps = corridor.get("endpoint_boarding_points") or {}
    changed = False
    for side, val in SINDALAH_GCN_EPS.items():
        if eps.get(side) != val:
            eps[side] = val
            changed = True
    if changed:
        corridor["endpoint_boarding_points"] = eps
        corridor["_geometry_bound_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corridors", default=str(DEFAULT_CORRIDORS))
    ap.add_argument("--dc", default="data-clean")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    corridors_path = Path(args.corridors)
    dc = ROOT / args.dc
    corridors = load_json(corridors_path)
    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    routes = route_features(load_json(dc / "ROUTES.json"))
    gold_ids = {route_id_of(r) for r in routes}

    moz_surface_report = ensure_mozambique_surface(fbt)
    cc_surface_report = ensure_croatia_cyprus_surface(fbt)

    report = {
        "phase": "bind_pending_corridor_geometry",
        "generated": datetime.now(timezone.utc).isoformat(),
        "nodes_patched": [],
        "routes_wired": [],
        "sindalah_eps_patched": [],
        "mozambique_surface": moz_surface_report,
        "croatia_cyprus_surface": cc_surface_report,
        "bp_resolution_after": [],
    }

    for mkey, mval in (corridors.get("markets") or {}).items():
        for corr in mval.get("corridors") or []:
            label = f"{corr.get('from')} -> {corr.get('to')}"
            if patch_corridor_nodes(corr):
                report["nodes_patched"].append({"market": mkey, "corridor": label})
            if patch_sindalah_gcn_eps(corr):
                report["sindalah_eps_patched"].append({"market": mkey, "corridor": label})
            if wire_route_id(mkey, corr, gold_ids):
                report["routes_wired"].append(
                    {"market": mkey, "corridor": label, "route_id": corr["route_id"]}
                )

    bp_idx = build_bp_index(fbt)
    touched = report["nodes_patched"] + report["routes_wired"] + report["sindalah_eps_patched"]
    for row in touched:
        mkey = row["market"]
        label = row["corridor"]
        corr = next(
            c
            for c in corridors["markets"][mkey]["corridors"]
            if f"{c.get('from')} -> {c.get('to')}" == label
        )
        fb, tb, fc, tc = resolve_corridor_endpoints(corr, bp_idx)
        if fb and tb and fb != tb:
            report["bp_resolution_after"].append(
                {
                    "market": mkey,
                    "corridor": label,
                    "from_bp": fb,
                    "to_bp": tb,
                    "from_city": fc,
                    "to_city": tc,
                    "route_id": corr.get("route_id"),
                }
            )

    out_report = ROOT / "grok-routing-output/bind-pending-corridor-report.json"
    out_report.parent.mkdir(parents=True, exist_ok=True)
    out_report.write_text(json.dumps(report, indent=2) + "\n")

    print(
        f"bind: nodes={len(report['nodes_patched'])} wired={len(report['routes_wired'])} "
        f"sindalah_eps={len(report['sindalah_eps_patched'])} "
        f"bp_pairs={len(report['bp_resolution_after'])} "
        f"moz_cities={len(moz_surface_report['cities_added'])} moz_bps={len(moz_surface_report['bps_added'])} "
        f"cc_cities={len(cc_surface_report['cities_added'])} cc_bps={len(cc_surface_report['bps_added'])}"
    )
    print(f"report: {out_report}")

    if args.dry_run:
        print("DRY RUN — no files written")
        return

    save_json(corridors_path, corridors)
    save_json(dc / "FEATURES_BY_TYPE.json", fbt)
    print(f"APPLIED → {corridors_path}")
    print(f"APPLIED → {dc / 'FEATURES_BY_TYPE.json'}")


if __name__ == "__main__":
    main()