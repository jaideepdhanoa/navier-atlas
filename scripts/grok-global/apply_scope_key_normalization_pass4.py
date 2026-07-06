#!/usr/bin/env python3
"""Pass 4 — normalize partner _map_scope registry keys for view-parity inheritance."""
from __future__ import annotations

import argparse
import copy
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "grok-global"))

from partner_scope_py import load_clusters, partner_cluster_ids  # noqa: E402
from scope_key_resolution import (  # noqa: E402
    COMMERCIAL_PARTNERS,
    SKIP_PARTNERS_PENDING_CONFIRM,
    canonical_registry_key,
    check_yango_locked,
    expanded_city_ids,
    load_geometry_index,
    load_pass4_artifacts,
    resolve_key,
)

PARTNERS_DIR = ROOT / "data-clean" / "partners"
PITCH_DIR = ROOT / "partner-pitch" / "partners"
REPORT_PATH = ROOT / "grok-routing-output" / "scope-key-normalization-pass4-report.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_partner_scope(
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
) -> tuple[dict[str, Any], dict[str, Any]]:
    doc = copy.deepcopy(partner)
    scope = dict(doc.get("_map_scope") or {})
    raw_keys = list(scope.get("registry_keys") or [])

    resolutions = [
        resolve_key(
            k,
            artifacts=artifacts,
            stamped_clusters=stamped_clusters,
            route_cities=route_cities,
            city_to_cluster=city_to_cluster,
            cluster_cities=cluster_cities,
            clusters=clusters,
        )
        for k in raw_keys
    ]

    new_registry: set[str] = set()
    aspirational: set[str] = set()
    dropped: list[str] = []
    resolved_cities: set[str] = set(scope.get("cluster_city_ids") or [])
    resolved_clusters: set[str] = set(scope.get("contested_cluster_ids") or [])

    for r in resolutions:
        if r.status == "dropped":
            dropped.append(r.key)
            continue
        if r.status == "unsealed-registered":
            aspirational.add(r.key)
            canon = canonical_registry_key(r)
            if canon:
                new_registry.add(canon)
            continue
        canon = canonical_registry_key(r)
        if canon:
            new_registry.add(canon)
        resolved_cities.update(r.city_ids)
        if r.cluster_id:
            resolved_clusters.add(r.cluster_id)

    # Near-miss city ids: register resolved cities under their cluster footprint
    for cid in sorted(resolved_clusters):
        if cid in cluster_cities:
            resolved_cities.update(cluster_cities[cid])

    resolved_clusters.update(
        partner_cluster_ids(resolved_cities, city_to_cluster)
    )

    scope.update(
        {
            "_doc": "Global Pass 4 — scope-key normalization (apply_scope_key_normalization_pass4.py)",
            "generated": utc_now(),
            "source": "global_scope_key_pass4",
            "inheritance_policy": "inherit_all_cluster_corridors",
            "registry_keys": sorted(new_registry),
            "cluster_city_ids": sorted(resolved_cities),
            "contested_cluster_ids": sorted(resolved_clusters),
            "aspirational_registry_keys": sorted(aspirational),
            "scope_key_resolution": {
                "raw_key_count": len(raw_keys),
                "canonical_key_count": len(new_registry),
                "dropped": dropped,
                "aspirational": sorted(aspirational),
                "by_status": {},
            },
        }
    )

    by_status: dict[str, int] = {}
    for r in resolutions:
        by_status[r.status] = by_status.get(r.status, 0) + 1
    scope["scope_key_resolution"]["by_status"] = by_status

    doc["_map_scope"] = scope
    yango_errors = check_yango_locked(partner_id, resolutions, artifacts)

    row: dict[str, Any] = {
        "partner_id": partner_id,
        "raw_keys": len(raw_keys),
        "canonical_keys": len(new_registry),
        "dropped": len(dropped),
        "aspirational": len(aspirational),
        "scope_cities": len(resolved_cities),
        "scope_clusters": len(resolved_clusters),
        "by_status": by_status,
        "yango_locked_errors": yango_errors,
        "skipped": False,
    }
    return doc, row


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--partner", nargs="*", choices=COMMERCIAL_PARTNERS)
    args = ap.parse_args()

    artifacts = load_pass4_artifacts()
    stamped, route_cities, city_to_cluster, cluster_cities, clusters = load_geometry_index()
    _, cluster_by_id, _ = load_clusters()

    targets = list(args.partner) if args.partner else list(COMMERCIAL_PARTNERS)
    report: dict[str, Any] = {
        "generated": utc_now(),
        "mode": "apply" if args.apply else "dry-run",
        "partners": [],
        "blockers": [],
    }

    for pid in targets:
        path = PARTNERS_DIR / f"{pid}.json"
        if not path.is_file():
            report["partners"].append({"partner_id": pid, "error": "missing"})
            report["blockers"].append(f"{pid}: missing partner file")
            continue

        partner = json.loads(path.read_text())
        updated, row = normalize_partner_scope(
            partner,
            pid,
            artifacts=artifacts,
            stamped_clusters=stamped,
            route_cities=route_cities,
            city_to_cluster=city_to_cluster,
            cluster_cities=cluster_cities,
            clusters=clusters,
            cluster_by_id=cluster_by_id,
        )
        report["partners"].append(row)

        if row.get("yango_locked_errors"):
            for err in row["yango_locked_errors"]:
                report["blockers"].append(f"{pid}: {err}")

        print(
            f"  {pid}: {row['raw_keys']}→{row['canonical_keys']} keys · "
            f"{row['scope_cities']} cities · dropped {row['dropped']} · aspirational {row['aspirational']}"
        )

        if args.apply:
            text = json.dumps(updated, indent=2) + "\n"
            path.write_text(text)
            pitch = PITCH_DIR / f"{pid}.json"
            if pitch.parent.is_dir():
                pitch.write_text(text)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")
    return 2 if report["blockers"] else 0


if __name__ == "__main__":
    raise SystemExit(main())