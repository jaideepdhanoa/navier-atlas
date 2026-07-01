#!/usr/bin/env python3
"""Auto-author PTA hand waypoints via channel_solver connect_chain."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-geometry"))

from channel_solver import connect_chain, get_land_checker, solve_hand  # noqa: E402

HANDOFF = ROOT / "handoff/partner-map-model"
DC = ROOT / "data-clean"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--partner", required=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    slug = args.partner
    dossier = json.loads((HANDOFF / f"PTA-DOSSIER-{slug}.json").read_text())
    nodes = {b["node"]: b for b in dossier["domestic_network"]["boarding_points"]}
    pairs = list(dossier["domestic_network"].get("domestic_pairs", []))

    lc = get_land_checker()
    catalog: dict[str, list] = {}
    report = {"partner": slug, "generated_at": utc_now(), "solved": [], "failed": []}

    for pair in pairs:
        fn, tn = pair["from"], pair["to"]
        if fn not in nodes or tn not in nodes:
            report["failed"].append({"pair_id": pair.get("pair_id"), "reason": "missing_node"})
            continue
        a = tuple(nodes[fn]["anchor_lnglat"])
        b = tuple(nodes[tn]["anchor_lnglat"])
        mids: list[tuple[float, float]] = []
        chain = connect_chain(lc, [a, b])
        if chain and len(chain) > 2:
            mids = [tuple(p) for p in chain[1:-1]]

        solved = solve_hand(lc, a, b, mids)
        if not solved or not solved.get("qa_pass"):
            report["failed"].append({"pair_id": pair.get("pair_id"), "from": fn, "to": tn})
            continue
        wps = solved.get("waypoints") or []
        catalog[f"{fn}|{tn}"] = wps
        report["solved"].append({"pair_id": pair.get("pair_id"), "waypoints": len(wps)})

    out = {
        "partner": slug,
        "generated_at": utc_now(),
        "waypoints": catalog,
    }
    path = DC / f"pta_hand_waypoints_{slug.replace('-', '_')}.json"
    receipt = HANDOFF / f"PTA-HAND-WAYPOINTS-{slug}.json"

    print(json.dumps({"solved": len(report["solved"]), "failed": len(report["failed"])}, indent=2))
    if args.apply:
        path.write_text(json.dumps(out, indent=2) + "\n")
        receipt.write_text(json.dumps(report, indent=2) + "\n")
        print(f"Wrote {path}")
    return 0 if not report["failed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())