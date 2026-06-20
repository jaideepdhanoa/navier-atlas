#!/usr/bin/env python3
"""Retag Yango Turkey coastal routes + mint missing intra/cross-border legs."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))

from bolt_yango_routing_shared import (  # noqa: E402
    build_bp_index,
    build_city_index,
    build_coastal_path,
    interior_land_km,
    load_json,
    load_land_mask,
    make_route_feature,
    mint_route_id,
    route_features,
    route_id_of,
    save_json,
    save_routes,
)

CITY_DISPLAY = {
    "bodrum-turkey": "Bodrum",
    "cesme-izmir-turkey": "Çeşme-İzmir",
    "istanbul-turkey": "Istanbul",
    "rhodes-dodecanese-greece": "Rhodes",
    "chios-north-aegean-greece": "Chios",
}

RETAG = {
    "rn-d57c0cac61b9": {
        "from_city_id": "bodrum-turkey",
        "to_city_id": "bodrum-turkey",
        "from_city": "Bodrum",
        "to_city": "Bodrum",
    },
    "rn-46ef20d42559": {
        "from_city_id": "bodrum-turkey",
        "to_city_id": "rhodes-dodecanese-greece",
        "from_city": "Bodrum",
        "to_city": "Rhodes",
    },
}

MINT_PAIRS = [
    ("bp-b927caa3b8", "bp-0371336126", "cesme-izmir-turkey", "cesme-izmir-turkey", "izmir_konak_karsiyaka"),
    ("bp-f92ad34f27", "bp-dc840061f0", "cesme-izmir-turkey", "chios-north-aegean-greece", "cesme_chios"),
    ("bp-69646a7be1", "bp-007d72dfaf", "cesme-izmir-turkey", "chios-north-aegean-greece", "kusadasi_samos"),
]

BP_REPARENT = {
    "bp-007d72dfaf": "chios-north-aegean-greece",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dc", default="data-clean")
    args = ap.parse_args()

    dc = ROOT / args.dc
    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    routes = route_features(load_json(dc / "ROUTES.json"))
    bp_idx = build_bp_index(fbt)
    cities = build_city_index(fbt)
    mask = load_land_mask()
    existing = {route_id_of(r) for r in routes}
    report = {"retagged": [], "minted": [], "bp_reparent": [], "generated": datetime.now(timezone.utc).isoformat()}

    for poi in fbt.get("poi", []):
        pid = poi["properties"]["id"]
        if pid in BP_REPARENT:
            old = poi["properties"].get("parent_city_id")
            poi["properties"]["parent_city_id"] = BP_REPARENT[pid]
            report["bp_reparent"].append({"bp": pid, "from": old, "to": BP_REPARENT[pid]})

    by_id = {route_id_of(r): r for r in routes}
    for rid, patch in RETAG.items():
        feat = by_id.get(rid)
        if not feat:
            continue
        props = feat.setdefault("properties", feat)
        props.update(patch)
        report["retagged"].append({"route_id": rid, **patch})

    new_feats = []
    for fb, tb, fc, tc, tag in MINT_PAIRS:
        if fb not in bp_idx or tb not in bp_idx:
            report.setdefault("skipped", []).append({"pair": [fb, tb], "reason": "bp-missing"})
            continue
        rid = mint_route_id(fb, tb, tag=tag)
        if rid in existing:
            report.setdefault("skipped", []).append({"route_id": rid, "reason": "exists"})
            continue
        a, b = bp_idx[fb]["coords"], bp_idx[tb]["coords"]
        coords = build_coastal_path(a, b, mask)
        land_km = interior_land_km(coords, mask)
        feat = make_route_feature(
            fb, tb, bp_idx[fb]["name"], bp_idx[tb]["name"], fc, tc, coords, cities, source=tag, land_km=land_km
        )
        new_feats.append(feat)
        existing.add(rid)
        report["minted"].append({"route_id": rid, "from": bp_idx[fb]["name"], "to": bp_idx[tb]["name"], "nm": feat["properties"]["distance_nm"]})

    if new_feats:
        routes.extend(new_feats)
        save_routes(dc / "ROUTES.json", routes)
    save_json(dc / "FEATURES_BY_TYPE.json", fbt)

    out = ROOT / "grok-routing-output/turkey-coast-retag-report.json"
    save_json(out, report)
    print(f"→ retagged {len(report['retagged'])}, minted {len(report['minted'])}, bp_reparent {len(report['bp_reparent'])}")
    print(f"→ report {out}")


if __name__ == "__main__":
    main()