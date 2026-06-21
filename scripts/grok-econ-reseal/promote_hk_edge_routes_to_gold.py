#!/usr/bin/env python3
"""Promote Hong Kong intra-city edge routes from _ingest into data-clean ROUTES.json gold."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INGEST = ROOT / "_ingest" / "data-clean" / "ROUTES.json"
GOLD = ROOT / "data-clean" / "ROUTES.json"
REPORT = ROOT / "handoff" / "partner-map-model" / "hk-edge-promote-report.json"

PREFIX = "edge__hong-kong__"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path):
    return json.loads(path.read_text())


def save_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def enrich(props: dict) -> dict:
    out = dict(props)
    fc = out.get("from_city_id") or out.get("from")
    tc = out.get("to_city_id") or out.get("to")
    if fc and "__" in fc:
        out.setdefault("from_city_id", fc.split("__", 1)[0])
    elif fc:
        out.setdefault("from_city_id", fc)
    if tc and "__" in tc:
        out.setdefault("to_city_id", tc.split("__", 1)[0])
    elif tc:
        out.setdefault("to_city_id", tc)
    return out


def main() -> int:
    ingest = load_json(INGEST)
    gold = load_json(GOLD)
    ids = {(f.get("properties") or {}).get("id") for f in gold}
    promoted = []
    for feat in ingest:
        p = feat.get("properties") or {}
        rid = p.get("id")
        if not rid or not rid.startswith(PREFIX) or rid in ids:
            continue
        props = enrich(p)
        gold.append({"type": "Feature", "geometry": feat.get("geometry"), "properties": props})
        ids.add(rid)
        promoted.append({"route_id": rid, "distance_nm": props.get("distance_nm"), "label": props.get("label")})

    save_json(GOLD, gold)
    save_json(REPORT, {"at": utc_now(), "lane": "grok/promote_hk_edge_routes_to_gold", "promoted": promoted})
    print(json.dumps({"promoted": len(promoted), "routes": promoted}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())