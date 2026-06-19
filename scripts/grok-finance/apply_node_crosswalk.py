#!/usr/bin/env python3
"""Apply economics→atlas node_id crosswalk to corridors.json + global-corridor-network.json."""
from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_XWALK = ROOT / "grok-routing-output/NODE-ID-CROSSWALK-2026-06-19.json"
DEFAULT_CORR = ROOT / "_ingest/gold-delta-LB230-LB241/finance/model/corridors.json"
DEFAULT_GCN = ROOT / "_ingest/global-network-coverage/global-corridor-network.json"
DEFAULT_FBT = ROOT / "data-clean/FEATURES_BY_TYPE.json"
NODE_FIELDS = ("from_node_id", "to_node_id", "from", "to")


def load_json(path: Path) -> dict | list:
    return json.loads(path.read_text())


def save_json(path: Path, data: dict | list) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def remap_value(val: str | None, rename: dict[str, str]) -> str | None:
    if not val or not isinstance(val, str):
        return val
    return rename.get(val, val)


def apply_corridors(corr: dict, rename: dict[str, str]) -> int:
    n = 0
    for mval in corr.get("markets", {}).values():
        for row in mval.get("corridors", []):
            for field in NODE_FIELDS:
                old = row.get(field)
                new = remap_value(old, rename)
                if new != old:
                    row[field] = new
                    n += 1
    return n


def apply_gcn(gcn: dict, rename: dict[str, str]) -> int:
    n = 0
    for routes in gcn.get("network_by_country", {}).values():
        for route in routes:
            ids = route.get("node_ids") or []
            new_ids = [remap_value(i, rename) for i in ids]
            if new_ids != ids:
                route["node_ids"] = new_ids
                n += 1
    return n


def geometry_authority(fbt_path: Path) -> set[str]:
    fbt = load_json(fbt_path)
    ids = {c["properties"]["id"] for c in fbt.get("city", []) + fbt.get("priority_city", [])}
    ids |= {p["properties"].get("parent_city_id") for p in fbt.get("poi", []) if p["properties"].get("parent_city_id")}
    return ids


def geom_ready_report(corr: dict, authority: set[str], partners: tuple[str, ...] | None = None) -> dict:
    total = ready = 0
    missing: dict[str, int] = {}
    for mkey, mval in corr.get("markets", {}).items():
        if partners and mval.get("partner") not in partners:
            continue
        for row in mval.get("corridors", []):
            for field in ("from_node_id", "to_node_id"):
                nid = row.get(field)
                if not nid:
                    continue
                total += 1
                if nid in authority:
                    ready += 1
                else:
                    missing[nid] = missing.get(nid, 0) + 1
    return {
        "ready": ready,
        "total": total,
        "pct": round(100 * ready / total, 1) if total else 100.0,
        "missing": dict(sorted(missing.items(), key=lambda kv: -kv[1])),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--xwalk", type=Path, default=DEFAULT_XWALK)
    ap.add_argument("--corridors", type=Path, default=DEFAULT_CORR)
    ap.add_argument("--gcn", type=Path, default=DEFAULT_GCN)
    ap.add_argument("--fbt", type=Path, default=DEFAULT_FBT)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    xwalk = load_json(args.xwalk)
    rename = xwalk.get("renames", {})
    corr = load_json(args.corridors)
    gcn = load_json(args.gcn)
    authority = geometry_authority(args.fbt)

    before_all = geom_ready_report(corr, authority)
    before_by = geom_ready_report(corr, authority, ("bolt", "yango"))

    corr_hits = apply_corridors(corr, rename)
    gcn_hits = apply_gcn(gcn, rename)

    after_all = geom_ready_report(corr, authority)
    after_by = geom_ready_report(corr, authority, ("bolt", "yango"))

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "crosswalk": str(args.xwalk),
        "fields_remapped": {"corridors": corr_hits, "gcn_routes": gcn_hits},
        "geometry_ready": {
            "all_markets_before": before_all,
            "all_markets_after": after_all,
            "bolt_yango_before": before_by,
            "bolt_yango_after": after_by,
        },
        "rsg_nodes": {
            "neom-ksa": remap_value("neom-ksa", rename),
            "amaala-ksa": remap_value("amaala-ksa", rename),
        },
    }

    out_report = ROOT / "grok-routing-output/node-crosswalk-report.json"
    save_json(out_report, report)

    print(json.dumps(report, indent=2))

    if not args.apply:
        print("\nDRY RUN — pass --apply to write files")
        return

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for path in (args.corridors, args.gcn):
        bak = path.with_suffix(path.suffix + f".bak.{ts}")
        shutil.copy2(path, bak)
        print(f"backup: {bak}")

    save_json(args.corridors, corr)
    save_json(args.gcn, gcn)
    print(f"APPLIED → {args.corridors}")
    print(f"APPLIED → {args.gcn}")


if __name__ == "__main__":
    main()