#!/usr/bin/env python3
"""WS-6 — restamp partner-prefixed cluster_ids to canonical geography."""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))

from bolt_yango_routing_shared import load_json, route_features, route_id_of, save_routes  # noqa: E402

GULF_PATH = ROOT / "handoff" / "yango-program" / "gulf-and-restamp" / "GULF-AND-GROUPS.json"
ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"
PARTNERS_DIR = ROOT / "data-clean" / "partners"
PITCH_DIR = ROOT / "partner-pitch" / "partners"
REPORT_PATH = ROOT / "grok-routing-output" / "cluster-rename-report.json"

ITALY_PLACEHOLDER = "__GROK_PLACE_BY_GEOMETRY__"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def props(feat: dict) -> dict:
    return feat.get("properties") or feat


def resolve_bolt_italy_target(feat: dict) -> str:
    p = props(feat)
    city = p.get("from_city_id") or p.get("to_city_id") or ""
    if "amalfi" in city or "naples" in city:
        return "amalfi-coast-italy"
    if "venice" in city:
        return "venice-italy"
    return "italy"


def rename_in_obj(obj: Any, renames: dict[str, str]) -> Any:
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if k in ("cluster_id", "registry_key", "market_key") and isinstance(v, str) and v in renames:
                out[k] = renames[v]
            elif k == "registry_keys" and isinstance(v, list):
                out[k] = sorted({renames.get(x, x) for x in v})
            elif k in ("contested_cluster_ids", "aspirational_registry_keys") and isinstance(v, list):
                out[k] = sorted({renames.get(x, x) for x in v})
            else:
                out[k] = rename_in_obj(v, renames)
        return out
    if isinstance(obj, list):
        return [rename_in_obj(x, renames) for x in obj]
    if isinstance(obj, str) and obj in renames:
        return renames[obj]
    return obj


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    gulf = load_json(GULF_PATH)
    raw_renames: dict[str, str] = gulf.get("cluster_renames") or {}
    renames: dict[str, str] = {k: v for k, v in raw_renames.items() if v != ITALY_PLACEHOLDER}

    routes = route_features(load_json(ROUTES_PATH))
    route_hits: dict[str, int] = {}
    out_routes = []
    for feat in routes:
        nf = copy.deepcopy(feat)
        p = props(nf)
        cid = p.get("cluster_id")
        if cid == "bolt-italy":
            target = resolve_bolt_italy_target(feat)
            p["cluster_id"] = target
            route_hits["bolt-italy"] = route_hits.get("bolt-italy", 0) + 1
        elif cid in renames:
            p["cluster_id"] = renames[cid]
            route_hits[cid] = route_hits.get(cid, 0) + 1
        out_routes.append(nf)

    partner_hits: list[dict] = []
    for path in sorted(PARTNERS_DIR.glob("*.json")):
        doc = json.loads(path.read_text())
        text = json.dumps(doc)
        if not any(old in text for old in list(renames) + ["bolt-italy"]):
            continue
        full_renames = {**renames, "bolt-italy": "amalfi-coast-italy"}
        updated = rename_in_obj(doc, full_renames)
        partner_hits.append({"partner_id": path.stem})
        if args.apply:
            out_text = json.dumps(updated, indent=2) + "\n"
            path.write_text(out_text)
            pitch = PITCH_DIR / path.name
            if pitch.parent.is_dir():
                pitch.write_text(out_text)

    report = {
        "generated": utc_now(),
        "mode": "apply" if args.apply else "dry-run",
        "renames": renames,
        "route_hits": route_hits,
        "partners_updated": partner_hits,
    }
    print(f"  cluster renames: {route_hits} · partners {len(partner_hits)}")

    if args.apply:
        save_routes(ROUTES_PATH, out_routes)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())