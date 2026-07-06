#!/usr/bin/env python3
"""Pass 1 — derive partner inheritance scopes; strip hand-curated corridor arrays."""
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

from partner_scope_py import load_clusters, partner_cluster_ids, partner_scope_city_ids  # noqa: E402

HANDOFF = ROOT / "handoff" / "uae-consolidation"
PARTNERS_DIR = ROOT / "data-clean" / "partners"
PITCH_DIR = ROOT / "partner-pitch" / "partners"
REPORT_PATH = ROOT / "grok-routing-output" / "global-partner-scope-derive-report.json"

STRIP_KEYS = (
    "featured_routes",
    "wow_corridors",
    "greenfield_corridors",
    "sourced_corridors",
    "featured_legs",
)

COMMERCIAL_PARTNERS = (
    "airasia-move",
    "bolt",
    "cabify",
    "careem",
    "didi",
    "gojek",
    "grab",
    "grab-thailand",
    "indrive",
    "kakao-mobility",
    "line",
    "line-man-wongnai",
    "lyft",
    "noon",
    "ola",
    "rapido",
    "uber",
    "uber-india",
    "yango",
    "yassir",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_contested_clusters() -> dict[str, list[str]]:
    doc = json.loads((HANDOFF / "CROSS-PARTNER-INHERITANCE-AUDIT.json").read_text())
    return doc.get("contested_clusters") or {}


def strip_container(obj: dict[str, Any], path: str, changes: list[str]) -> None:
    for key in STRIP_KEYS:
        if key in obj and obj[key]:
            n = len(obj[key]) if isinstance(obj[key], list) else 1
            obj[key] = [] if isinstance(obj[key], list) else None
            changes.append(f"cleared {path}.{key} ({n} entries)")
    wnn = obj.get("why_navier_now")
    if isinstance(wnn, dict) and wnn.get("wow_corridors"):
        n = len(wnn["wow_corridors"])
        wnn["wow_corridors"] = []
        changes.append(f"cleared {path}.why_navier_now.wow_corridors ({n} entries)")


def derive_partner(
    partner: dict[str, Any],
    contested: dict[str, list[str]],
    cluster_by_id: dict[str, dict],
    city_to_cluster: dict[str, str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    pid = partner.get("partner_id", "unknown")
    doc = copy.deepcopy(partner)
    changes: list[str] = []

    partner_clusters = sorted(
        cid for cid, partners in contested.items() if pid in partners
    )

    scope = dict(doc.get("_map_scope") or {})
    scope.update(
        {
            "_doc": "Global Pass 1 — inherit-all contested clusters (derive_partner_scopes_global.py)",
            "generated": utc_now(),
            "source": "global_consolidation_pass1",
            "inheritance_policy": "inherit_all_cluster_corridors",
            "contested_cluster_ids": partner_clusters,
        }
    )

    city_ids = sorted(partner_scope_city_ids(doc, cluster_by_id))
    scope["cluster_city_ids"] = city_ids
    scope["registry_keys"] = sorted(set(scope.get("registry_keys") or []) | set(partner_clusters))
    doc["_map_scope"] = scope
    changes.append(f"_map_scope: {len(partner_clusters)} contested clusters, {len(city_ids)} cities")

    strip_container(doc, "root", changes)
    for pi, ph in enumerate(doc.get("phases") or []):
        if isinstance(ph, dict):
            strip_container(ph, f"phases[{pi}]", changes)
    for mi, m in enumerate(doc.get("markets") or []):
        if not isinstance(m, dict):
            continue
        mk = m.get("slug") or m.get("id") or str(mi)
        strip_container(m, f"markets[{mk}]", changes)
        for pi, ph in enumerate(m.get("phases") or []):
            if isinstance(ph, dict):
                strip_container(ph, f"markets[{mk}].phases[{pi}]", changes)

    cluster_ids = sorted(partner_cluster_ids(set(city_ids), city_to_cluster) | set(partner_clusters))
    return doc, {
        "partner_id": pid,
        "contested_clusters": len(partner_clusters),
        "scope_cities": len(city_ids),
        "scope_cluster_ids": cluster_ids,
        "changes": changes,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--partner", nargs="*", choices=COMMERCIAL_PARTNERS)
    args = ap.parse_args()

    contested = load_contested_clusters()
    _, cluster_by_id, city_to_cluster = load_clusters()
    targets = list(args.partner) if args.partner else list(COMMERCIAL_PARTNERS)

    report: dict[str, Any] = {
        "generated": utc_now(),
        "mode": "apply" if args.apply else "dry-run",
        "partners": [],
    }

    for pid in targets:
        path = PARTNERS_DIR / f"{pid}.json"
        if not path.is_file():
            report["partners"].append({"partner_id": pid, "error": "missing"})
            continue
        partner = json.loads(path.read_text())
        updated, row = derive_partner(partner, contested, cluster_by_id, city_to_cluster)
        report["partners"].append(row)
        if args.apply:
            text = json.dumps(updated, indent=2) + "\n"
            path.write_text(text)
            pitch = PITCH_DIR / f"{pid}.json"
            if pitch.parent.is_dir():
                pitch.write_text(text)
        print(f"  {pid}: {row['contested_clusters']} clusters · {row['scope_cities']} cities")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())