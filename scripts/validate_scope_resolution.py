#!/usr/bin/env python3
"""Hard gate: every partner registry key resolves, is aspirational, or is dropped.

Fails on silent-dark markets (geometry exists but scope does not include resolved cities).
Fails if Yango keys resolve to Turkey/KSA/Norway locked non-markets.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "grok-global"))

from partner_scope_py import load_clusters, partner_scope_city_ids  # noqa: E402
from scope_key_resolution import (  # noqa: E402
    COMMERCIAL_PARTNERS,
    SKIP_PARTNERS_PENDING_CONFIRM,
    check_yango_locked,
    geometry_for_resolution,
    load_geometry_index,
    load_pass4_artifacts,
    resolve_key,
)

PARTNERS_DIR = ROOT / "data-clean" / "partners"
REPORT_PATH = ROOT / "grok-routing-output" / "scope-resolution-validation-report.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def validate_partner(
    partner: dict[str, Any],
    partner_id: str,
    *,
    artifacts: dict[str, Any],
    stamped_clusters: set[str],
    route_cities: set[str],
    city_to_cluster: dict[str, str],
    cluster_cities: dict[str, set[str]],
    clusters: dict[str, dict],
    cluster_by_id: dict[str, dict],
    strict: bool,
) -> dict[str, Any]:
    scope = partner.get("_map_scope") or {}
    raw_keys = list(scope.get("registry_keys") or [])
    aspirational_declared = set(scope.get("aspirational_registry_keys") or [])
    scope_cities = set(partner_scope_city_ids(partner, cluster_by_id))

    errors: list[str] = []
    warnings: list[str] = []
    resolutions = []

    for key in raw_keys:
        r = resolve_key(
            key,
            artifacts=artifacts,
            stamped_clusters=stamped_clusters,
            route_cities=route_cities,
            city_to_cluster=city_to_cluster,
            cluster_cities=cluster_cities,
            clusters=clusters,
        )
        resolutions.append(r)

        if r.status == "dropped":
            errors.append(f"{key}: unresolved (must resolve, aspirational, or be removed)")
            continue

        if r.status == "unsealed-registered" and key not in aspirational_declared:
            errors.append(f"{key}: unsealed-registered but not in aspirational_registry_keys")

        geo_cities = geometry_for_resolution(
            r,
            stamped_clusters=stamped_clusters,
            route_cities=route_cities,
            cluster_cities=cluster_cities,
        )
        if geo_cities and not (geo_cities & scope_cities):
            errors.append(
                f"{key}: silent-dark — geometry exists for {sorted(geo_cities)[:3]} but scope lacks cities"
            )

    yango_errors = check_yango_locked(partner_id, resolutions, artifacts)
    errors.extend(yango_errors)

    # Keys removed by hygiene should not linger in registry_keys
    for key in raw_keys:
        if key in artifacts["prefix_junk"] or key in artifacts["unknown_drop"]:
            errors.append(f"{key}: hygiene key still present in registry_keys")

    # Duplicate alias pairs (underscore + hyphen) should be collapsed
    for key in raw_keys:
        alias = artifacts["aliases"].get(key)
        if alias and alias in raw_keys and key != alias:
            warnings.append(f"duplicate alias pair in registry_keys: {key} / {alias}")

    ok = len(errors) == 0
    if not strict and warnings:
        ok = ok  # warnings never fail non-strict

    return {
        "partner_id": partner_id,
        "ok": ok,
        "registry_keys": len(raw_keys),
        "errors": errors,
        "warnings": warnings,
        "by_status": {s: sum(1 for r in resolutions if r.status == s) for s in {r.status for r in resolutions}},
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", default=True)
    ap.add_argument("--partner", nargs="*", choices=COMMERCIAL_PARTNERS)
    args = ap.parse_args()

    artifacts = load_pass4_artifacts()
    stamped, route_cities, city_to_cluster, cluster_cities, clusters = load_geometry_index()
    _, cluster_by_id, _ = load_clusters()

    targets = list(args.partner) if args.partner else list(COMMERCIAL_PARTNERS)
    rows: list[dict[str, Any]] = []
    blockers: list[str] = []

    for pid in targets:
        path = PARTNERS_DIR / f"{pid}.json"
        if not path.is_file():
            blockers.append(f"{pid}: missing")
            continue

        partner = json.loads(path.read_text())
        row = validate_partner(
            partner,
            pid,
            artifacts=artifacts,
            stamped_clusters=stamped,
            route_cities=route_cities,
            city_to_cluster=city_to_cluster,
            cluster_cities=cluster_cities,
            clusters=clusters,
            cluster_by_id=cluster_by_id,
            strict=args.strict,
        )
        rows.append(row)
        status = "OK" if row["ok"] else "FAIL"
        print(f"  {pid}: {status} ({row['registry_keys']} keys)")
        if not row["ok"]:
            for e in row["errors"][:5]:
                print(f"    ✗ {e}")
                blockers.append(f"{pid}: {e}")
            if len(row["errors"]) > 5:
                print(f"    … +{len(row['errors']) - 5} more")

    report = {
        "generated": utc_now(),
        "lane": "validate_scope_resolution",
        "strict": args.strict,
        "partners_ok": sum(1 for r in rows if r.get("ok")),
        "partners_total": len(rows),
        "blockers": blockers,
        "partners": rows,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")

    if args.json:
        print(json.dumps(report, indent=2))

    return 2 if blockers else 0


if __name__ == "__main__":
    raise SystemExit(main())