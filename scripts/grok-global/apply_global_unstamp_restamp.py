#!/usr/bin/env python3
"""WS-4 — apply GLOBAL-UNSTAMP-RESTAMP.json + Eastern Province hygiene."""
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

from bolt_yango_routing_shared import load_json, route_features, route_id_of, save_routes  # noqa: E402

HANDOFF = ROOT / "handoff" / "yango-program" / "gulf-and-restamp"
RESTAMP_PATH = HANDOFF / "GLOBAL-UNSTAMP-RESTAMP.json"
GULF_PATH = HANDOFF / "GULF-AND-GROUPS.json"
ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"
CLUSTERS_PATH = ROOT / "data-clean" / "CLUSTERS.json"
REPORT_PATH = ROOT / "grok-routing-output" / "global-unstamp-restamp-report.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def props(feat: dict) -> dict:
    return feat.get("properties") or feat


def ensure_dammam_cluster(clusters_doc: dict) -> bool:
    clusters = clusters_doc.get("clusters") or []
    by_id = {c["cluster_id"]: c for c in clusters}
    if "dammam-eastern-province-ksa" in by_id:
        return False
    clusters.append(
        {
            "cluster_id": "dammam-eastern-province-ksa",
            "cluster_label": "Dammam / Eastern Province (KSA)",
            "region": "MENA",
            "type": "coastal",
            "anchor": [50.202, 26.474],
            "member_city_ids": ["dammam-khobar-ksa", "eastern-province-ksa"],
            "members_present": 2,
            "members_missing": [],
            "anchor_source": "careem_gulf_anchors",
            "_global_geometry_ws4": utc_now(),
        }
    )
    clusters_doc["clusters"] = clusters
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    restamp_doc = load_json(RESTAMP_PATH)
    gulf_doc = load_json(GULF_PATH)
    restamp_map: dict[str, str] = restamp_doc.get("restamp_route_to_cluster") or {}
    stampable_ep = set(gulf_doc.get("eastern_province_stampable_route_ids") or [])
    junk_ep = set(gulf_doc.get("eastern_province_junk_endpoint_route_ids") or [])

    routes = route_features(load_json(ROUTES_PATH))
    report: dict[str, Any] = {
        "generated": utc_now(),
        "mode": "apply" if args.apply else "dry-run",
        "restamp_applied": 0,
        "eastern_province_stamped": 0,
        "eastern_province_junk_dropped": 0,
        "already_stamped_skipped": 0,
        "unresolved_null_held": 0,
        "errors": [],
    }

    out: list[dict] = []
    for feat in routes:
        p = props(feat)
        rid = route_id_of(feat)
        if rid in junk_ep:
            report["eastern_province_junk_dropped"] += 1
            continue
        nf = copy.deepcopy(feat)
        np = props(nf)
        if rid in stampable_ep:
            np["cluster_id"] = "bahrain"
            report["eastern_province_stamped"] += 1
        elif not np.get("cluster_id"):
            target = restamp_map.get(rid)
            if target:
                np["cluster_id"] = target
                np["_global_unstamp_restamp"] = utc_now()
                report["restamp_applied"] += 1
            else:
                report["unresolved_null_held"] += 1
        else:
            report["already_stamped_skipped"] += 1
        out.append(nf)

    clusters_doc = load_json(CLUSTERS_PATH)
    cluster_added = ensure_dammam_cluster(clusters_doc)

    print(
        f"  restamp: {report['restamp_applied']} · EP stamped: {report['eastern_province_stamped']} "
        f"· junk dropped: {report['eastern_province_junk_dropped']} · null held: {report['unresolved_null_held']}"
    )

    if args.apply:
        save_routes(ROUTES_PATH, out)
        if cluster_added:
            CLUSTERS_PATH.write_text(json.dumps(clusters_doc, indent=2, ensure_ascii=False) + "\n")
        print(f"  wrote {ROUTES_PATH}")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())