#!/usr/bin/env python3
"""Materialize partner _map_scope from navier/handoff/partner-map-model/seal-scope/*.json.

Patches data-clean/partners/<partner>.json with cluster_city_ids + per-market render modes
so build-site + index.html can show the full network_footprint on the map (Grab-style),
not a card grid.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "navier" / "handoff" / "partner-map-model" / "seal-scope"
PARTNERS = ROOT / "data-clean" / "partners"

PARTNER_SLUGS = ("bolt", "yango", "grab", "uber", "didi")


def materialize(partner: str) -> dict | None:
    src = HANDOFF / f"{partner}.json"
    if not src.exists():
        return None
    seal = json.loads(src.read_text())
    markets = []
    cluster_ids: list[str] = []
    for row in seal.get("render") or []:
        ids = row.get("cluster_city_ids") or []
        cluster_ids.extend(ids)
        markets.append({
            "id": row.get("market"),
            "registry_key": row.get("registry_key"),
            "covered": row.get("covered"),
            "mode": row.get("mode"),
            "cluster_city_ids": ids,
            "corridors_sealed": row.get("corridors_sealed"),
            "corridors_total": row.get("corridors_total"),
        })
    scope = {
        "_doc": "LB-260 materialized from navier/handoff/partner-map-model/seal-scope — full footprint map scope",
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": str(src.relative_to(ROOT)),
        "cluster_city_ids": sorted(set(cluster_ids)),
        "markets": markets,
        "held": seal.get("held") or [],
        "ground_backlog": seal.get("ground_backlog") or [],
    }
    return scope


def main() -> int:
    targets = sys.argv[1:] if len(sys.argv) > 1 else list(PARTNER_SLUGS)
    for slug in targets:
        scope = materialize(slug)
        if scope is None:
            print(f"  skip {slug}: no seal-scope handoff")
            continue
        pj = PARTNERS / f"{slug}.json"
        if not pj.exists():
            print(f"  skip {slug}: missing {pj}")
            continue
        partner = json.loads(pj.read_text())
        partner["_map_scope"] = scope
        pj.write_text(json.dumps(partner, indent=2, ensure_ascii=False) + "\n")
        pitch = ROOT / "partner-pitch" / "partners" / f"{slug}.json"
        if pitch.parent.exists():
            pitch.write_text(pj.read_text())
        print(f"  ✓ {slug}: {len(scope['cluster_city_ids'])} cluster cities, {len(scope['markets'])} footprint markets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())