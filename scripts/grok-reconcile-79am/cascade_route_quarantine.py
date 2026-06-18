#!/usr/bin/env python3
"""Quarantine routes touching explicitly quarantined BPs only."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def load_json(p: Path):
    return json.loads(p.read_text())


def save_routes(p: Path, features: list):
    p.write_text(json.dumps(features, separators=(",", ":")) + "\n")


def route_features(obj) -> list:
    return obj if isinstance(obj, list) else obj.get("features", [])


def build_quarantined_bps(fbt: dict) -> set[str]:
    out = set()
    for poi in fbt.get("poi", []):
        props = poi.get("properties", poi)
        if props.get("_quarantine") or props.get("relevance") == "hide":
            pid = props.get("id")
            if pid:
                out.add(pid)
    return out


def endpoint_bp(ep: str) -> str | None:
    if ep and ep.startswith("bp-"):
        return ep
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    args = ap.parse_args()

    work = Path(args.work)
    dc = work / "atlas-repo" / "data-clean"
    routes = route_features(load_json(dc / "ROUTES.json"))
    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    q_bps = build_quarantined_bps(fbt)

    quarantined = []
    for feat in routes:
        props = feat.get("properties", feat)
        rid = props.get("id") or props.get("route_id")
        fr, to = props.get("from"), props.get("to")
        bad = []
        for ep in (fr, to):
            bp = endpoint_bp(ep)
            if bp and bp in q_bps:
                bad.append(bp)
        if bad:
            props["_quarantine"] = True
            props["relevance"] = "hide"
            props["_quarantine_reason"] = f"quarantined_bp_endpoint {bad}"
            quarantined.append({"id": rid, "bad_bps": bad})
        else:
            props.pop("_quarantine", None)
            props.pop("relevance", None)

    save_routes(dc / "ROUTES.json", routes)
    report = {
        "total": len(routes),
        "quarantined": len(quarantined),
        "active": len(routes) - len(quarantined),
        "quarantined_bps": len(q_bps),
        "sample": quarantined[:30],
    }
    (work / "grok-routing-output" / "route-cascade-report.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )
    print(
        f"route cascade: total={report['total']} quarantined={report['quarantined']} "
        f"active={report['active']} (q_bps={len(q_bps)})"
    )


if __name__ == "__main__":
    main()