#!/usr/bin/env python3
"""Promote Tasklet seal-staging corridor specs → finance/model/corridors.json."""
from __future__ import annotations

import argparse
import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-tasklet-import"))

from tasklet_shared import (  # noqa: E402
    CORRIDORS_SRC,
    ROUTING_OUTPUT,
    find_staging_package,
    iter_staging_corridors,
    load_json,
    load_route_index,
    normalize_bound_corridor,
    partner_staging_dir,
    save_json,
    utc_now,
)


def corridor_filename(partner_id: str) -> str:
    return f"{partner_id}-corridors.json"


def bind_partner_market(
    package: Path,
    partner_id: str,
    route_by_pair: dict,
    route_meta: dict,
    dry_run: bool,
) -> dict:
    staging_dir = partner_staging_dir(package, partner_id)
    staging_path = staging_dir / corridor_filename(partner_id)
    if not staging_path.exists():
        raise FileNotFoundError(staging_path)

    staging = load_json(staging_path)
    market_meta = copy.deepcopy(staging.get("market") or {})
    market_meta["partner"] = partner_id
    market_meta.pop("corridors", None)

    corridors = []
    skipped = []
    for tier, raw in iter_staging_corridors(staging):
        row = normalize_bound_corridor(tier, raw, route_by_pair, route_meta, partner_id)
        if row is None:
            skipped.append({"tier": tier, "from": raw.get("from"), "to": raw.get("to")})
            continue
        corridors.append(row)

    market = {**market_meta, "corridors": corridors}
    return {
        "partner_id": partner_id,
        "market": market,
        "bound": len(corridors),
        "skipped": skipped,
        "staging": str(staging_path),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--package", help="seal-staging package dir (default: latest)")
    ap.add_argument("--partner", action="append", help="partner id (repeatable)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--seal-report", help="override seal report JSON path")
    args = ap.parse_args()

    package = find_staging_package(args.package)
    manifest = load_json(package / "seal-manifest.json")
    partners = args.partner or list((manifest.get("partners") or {}).keys())
    if not partners:
        print("✗ no partners in manifest", file=sys.stderr)
        return 1

    report_path = Path(args.seal_report) if args.seal_report else None
    route_by_pair, route_meta = load_route_index(report_path)

    corr = load_json(CORRIDORS_SRC)
    corr.setdefault("markets", {})
    report = {
        "at": utc_now(),
        "lane": "grok-tasklet-import/bind_corridors_from_staging",
        "package": str(package),
        "partners": {},
    }

    for pid in partners:
        result = bind_partner_market(package, pid, route_by_pair, route_meta, args.dry_run)
        report["partners"][pid] = {
            "bound": result["bound"],
            "skipped": result["skipped"],
            "staging": result["staging"],
        }
        if not args.dry_run:
            corr["markets"][pid] = result["market"]
        print(f"  {pid}: {result['bound']} corridors bound, {len(result['skipped'])} skipped")

    if not args.dry_run:
        save_json(CORRIDORS_SRC, corr)

    out = ROUTING_OUTPUT / "tasklet-corridors-bind-report.json"
    save_json(out, report)
    print(json_dump(report))
    return 0


def json_dump(obj) -> str:
    import json

    return json.dumps({"report": str(ROUTING_OUTPUT / "tasklet-corridors-bind-report.json"), **obj}, indent=2)


if __name__ == "__main__":
    raise SystemExit(main())