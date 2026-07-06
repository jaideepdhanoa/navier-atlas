#!/usr/bin/env python3
"""WS-5 — apply canonical market groups + derive post-WS-4."""
from __future__ import annotations

import argparse
import copy
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))

from bolt_yango_routing_shared import load_json, route_features  # noqa: E402


def route_props(feat: dict) -> dict:
    return feat.get("properties") or feat

GULF_PATH = ROOT / "handoff" / "yango-program" / "gulf-and-restamp" / "GULF-AND-GROUPS.json"
GROUPS_OUT = ROOT / "handoff" / "yango-program" / "gulf-and-restamp" / "MARKET-GROUPS.json"
ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"
PARTNERS_DIR = ROOT / "data-clean" / "partners"
PITCH_DIR = ROOT / "partner-pitch" / "partners"
REPORT_PATH = ROOT / "grok-routing-output" / "market-groups-apply-report.json"

UAE_PARTNERS = ("careem", "noon", "bolt", "uber", "yango")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def derive_market_groups(routes: list[dict], confirmed: dict[str, list[str]]) -> dict[str, list[str]]:
    """Post-WS-4: any cluster with stamped routes → group under country prefix where possible."""
    cluster_route_count: dict[str, int] = {}
    for feat in routes:
        cid = route_props(feat).get("cluster_id")
        if cid:
            cluster_route_count[cid] = cluster_route_count.get(cid, 0) + 1

    groups = {k: sorted(v) for k, v in confirmed.items()}
    # Qatar alias: empty qatar shell → doha-qatar + al-wakrah-qatar already in confirmed
    if "qatar" not in groups and "doha-qatar" in {c for cs in groups.values() for c in cs}:
        groups["qatar"] = groups.get("qatar", ["doha-qatar", "al-wakrah-qatar"])

    groups_doc = {
        "_doc": "WS-5 market groups — confirmed + derived post-WS-4",
        "generated": utc_now(),
        "groups": groups,
        "cluster_route_counts": {k: cluster_route_count.get(k, 0) for k in sorted(cluster_route_count)},
    }
    return groups_doc


def expand_partner_scope(partner: dict, groups: dict[str, list[str]]) -> dict:
    doc = copy.deepcopy(partner)
    scope = dict(doc.get("_map_scope") or {})
    reg = set(scope.get("registry_keys") or [])
    contested = set(scope.get("contested_cluster_ids") or [])
    cities = set(scope.get("cluster_city_ids") or [])

    expanded_reg: set[str] = set()
    for key in reg:
        expanded_reg.add(key)
        if key in groups:
            expanded_reg.update(groups[key])
    for market, cluster_ids in groups.items():
        if market in reg or any(c in reg for c in cluster_ids):
            expanded_reg.update(cluster_ids)
            contested.update(cluster_ids)

    scope["registry_keys"] = sorted(expanded_reg)
    scope["contested_cluster_ids"] = sorted(contested)
    scope["market_groups_applied"] = utc_now()
    doc["_map_scope"] = scope
    return doc


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    gulf = load_json(GULF_PATH)
    confirmed = gulf.get("confirmed_market_groups") or {}
    routes = route_features(load_json(ROUTES_PATH))
    groups_doc = derive_market_groups(routes, confirmed)
    groups = groups_doc["groups"]

    updated = 0
    for pid in sorted(PARTNERS_DIR.glob("*.json")):
        partner = json.loads(pid.read_text())
        reg = set((partner.get("_map_scope") or {}).get("registry_keys") or [])
        if not (reg & set(groups.keys()) | {c for cs in groups.values() for c in cs}):
            continue
        doc = expand_partner_scope(partner, groups)
        updated += 1
        if args.apply:
            text = json.dumps(doc, indent=2) + "\n"
            pid.write_text(text)
            pitch = PITCH_DIR / pid.name
            if pitch.parent.is_dir():
                pitch.write_text(text)

    print(f"  market groups: {len(groups)} markets · partners expanded: {updated}")

    if args.apply:
        GROUPS_OUT.write_text(json.dumps(groups_doc, indent=2) + "\n")

    report = {"generated": utc_now(), "groups": groups, "partners_updated": updated}
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())