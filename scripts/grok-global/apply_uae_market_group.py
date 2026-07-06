#!/usr/bin/env python3
"""WS-1 — unify UAE market scope across all 5 UAE partners.

Market uae = {uae, uae-east-coast}. East coast is UAE and must never be excluded.
"""
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

from partner_scope_py import load_clusters  # noqa: E402

HANDOFF = ROOT / "handoff" / "yango-program" / "gulf-and-restamp" / "MARKET-GROUPS.json"
PARTNERS_DIR = ROOT / "data-clean" / "partners"
PITCH_DIR = ROOT / "partner-pitch" / "partners"
REPORT_PATH = ROOT / "grok-routing-output" / "uae-market-group-apply-report.json"

UAE_ONLY_PARTNERS = frozenset({"careem", "noon"})
UAE_SCOPE_PARTNERS = ("careem", "noon", "bolt", "uber", "yango")
UAE_CLUSTERS = ("uae", "uae-east-coast")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def uae_city_ids(cluster_by_id: dict[str, dict]) -> list[str]:
    out: set[str] = set()
    for cid in UAE_CLUSTERS:
        c = cluster_by_id.get(cid)
        if c:
            out.update(c.get("member_city_ids") or [])
    return sorted(out)


def apply_uae_scope(
    partner: dict[str, Any],
    partner_id: str,
    cluster_by_id: dict[str, dict],
) -> tuple[dict[str, Any], dict[str, Any]]:
    doc = copy.deepcopy(partner)
    uae_cities = set(uae_city_ids(cluster_by_id))
    scope = dict(doc.get("_map_scope") or {})
    before_keys = list(scope.get("registry_keys") or [])

    if partner_id in UAE_ONLY_PARTNERS:
        registry_keys = sorted(UAE_CLUSTERS)
        cluster_city_ids = sorted(uae_cities)
        contested = sorted(UAE_CLUSTERS)
    else:
        registry_keys = sorted(set(before_keys) | set(UAE_CLUSTERS))
        cluster_city_ids = sorted(set(scope.get("cluster_city_ids") or []) | uae_cities)
        contested = sorted(set(scope.get("contested_cluster_ids") or []) | set(UAE_CLUSTERS))

    scope.update(
        {
            "_doc": "WS-1 UAE market group — {uae, uae-east-coast}",
            "generated": utc_now(),
            "source": "global_geometry_ws1_uae_market_group",
            "market_group": "uae",
            "registry_keys": registry_keys,
            "cluster_city_ids": cluster_city_ids,
            "contested_cluster_ids": contested,
            "inheritance_policy": scope.get("inheritance_policy") or "inherit_all_cluster_corridors",
        }
    )
    doc["_map_scope"] = scope
    return doc, {
        "partner_id": partner_id,
        "before_keys": before_keys,
        "after_keys": registry_keys,
        "cities": len(cluster_city_ids),
        "mode": "uae_only" if partner_id in UAE_ONLY_PARTNERS else "merge",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    _, cluster_by_id, _ = load_clusters()
    report: dict[str, Any] = {"generated": utc_now(), "mode": "apply" if args.apply else "dry-run", "partners": []}

    for pid in UAE_SCOPE_PARTNERS:
        path = PARTNERS_DIR / f"{pid}.json"
        partner = json.loads(path.read_text())
        updated, row = apply_uae_scope(partner, pid, cluster_by_id)
        report["partners"].append(row)
        print(f"  {pid}: {row['before_keys']} → {row['after_keys']} ({row['cities']} cities)")
        if args.apply:
            text = json.dumps(updated, indent=2) + "\n"
            path.write_text(text)
            pitch = PITCH_DIR / f"{pid}.json"
            if pitch.parent.is_dir():
                pitch.write_text(text)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())