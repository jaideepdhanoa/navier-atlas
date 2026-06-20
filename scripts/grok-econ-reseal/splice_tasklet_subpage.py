#!/usr/bin/env python3
"""Splice Tasklet sub-page parity handoff: partners + corridor bind + render finalize."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))

from apply_bolt_yango import (  # noqa: E402
    RouteIndexes,
    bind_route_refs,
    binding_stats,
    build_corridor_index,
    load_json,
    route_features,
    save_json,
)
from bolt_yango_routing_shared import build_bp_index  # noqa: E402

PRESERVE_KEYS = ("growth_case", "economics_url", "_growth_case_pending", "_ingest")


def finalize_render(fr: dict) -> None:
    if fr.get("render"):
        return
    if fr.get("route_id"):
        fr["render"] = "geometry"
    elif fr.get("_link_status") == "unlinked-no-route" and fr.get("_phase3_backbone"):
        # Aspirational legs (ireland Holyhead) keep explicit render; others stay null for review
        pass


def splice_partner(handoff: dict, current: dict, indexes, corridor_idx, url: str, bp_idx) -> dict:
    out = handoff
    for key in PRESERVE_KEYS:
        if current.get(key):
            out[key] = current[key]
    bind_route_refs(out, indexes, corridor_idx, url, bp_idx=bp_idx)
    for m in out.get("markets") or []:
        for ph in m.get("phases") or []:
            for fr in ph.get("featured_routes") or []:
                if fr.get("_phase3_backbone"):
                    finalize_render(fr)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dc", default="data-clean")
    ap.add_argument("--handoff", default=str(ROOT / "_ingest/tasklet-subpage-parity-2026-06-20b"))
    ap.add_argument("--corridors", default="")
    ap.add_argument("--econ-map", default=str(ROOT / "_ingest/sidecar-opex-refresh-2026-06-20/economics_url_map.json"))
    args = ap.parse_args()

    dc = ROOT / args.dc
    handoff = Path(args.handoff)
    corr_path = Path(args.corridors) if args.corridors else handoff / "corridors.json"
    econ_map = load_json(Path(args.econ_map))

    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    routes = route_features(load_json(dc / "ROUTES.json"))
    indexes = RouteIndexes(routes)
    corridor_idx = build_corridor_index(load_json(corr_path))
    bp_idx = build_bp_index(fbt)

    report = {"phase3_backbone": []}
    for partner in ("bolt", "yango"):
        hand = load_json(handoff / f"{partner}.json")
        cur = load_json(dc / f"partners/{partner}.json")
        url = econ_map.get("economics_url", {}).get(partner, "")
        out = splice_partner(hand, cur, indexes, corridor_idx, url, bp_idx)
        save_json(dc / f"partners/{partner}.json", out)
        stats = binding_stats(out)
        print(f"→ {partner}: linked={stats['linked']} unlinked={stats['unlinked']}")
        for m in out.get("markets") or []:
            for ph in m.get("phases") or []:
                for fr in ph.get("featured_routes") or []:
                    if not fr.get("_phase3_backbone"):
                        continue
                    row = {
                        "partner": partner,
                        "market": m.get("id"),
                        "from": fr.get("from_label"),
                        "to": fr.get("to_label"),
                        "route_id": fr.get("route_id"),
                        "status": fr.get("_link_status"),
                        "render": fr.get("render"),
                    }
                    report["phase3_backbone"].append(row)
                    print(f"  {row['market']}: {row['from']} → {row['to']} → {row['route_id'] or row['status']} render={row['render']}")

    out_report = ROOT / "grok-routing-output/tasklet-subpage-splice-report.json"
    save_json(out_report, report)
    print(f"→ report {out_report}")


if __name__ == "__main__":
    main()