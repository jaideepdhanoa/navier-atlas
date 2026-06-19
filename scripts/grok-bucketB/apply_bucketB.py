#!/usr/bin/env python3
"""Apply Bucket B Tier 1+2: mint city pins, replace/insert Tasklet POIs."""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from bucketB_shared import (
    CITY_META,
    HANDOFF,
    TIER12,
    TIER3_CROSSWALK,
    load_json,
    save_json,
)

ROOT = Path(__file__).resolve().parents[2]


def bp_type_label(bp_type: str | None) -> str | None:
    if not bp_type:
        return None
    return bp_type.replace("_", " ").title()


def make_city_feature(city_id: str, anchor: list[float]) -> dict:
    meta = CITY_META[city_id]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [anchor[0], anchor[1]]},
        "properties": {
            "id": city_id,
            "type": "city",
            "name": meta["name"],
            "shortName": meta["shortName"],
            "fullName": meta["name"],
            "country": meta["country"],
            "region": meta["region"],
            "platform_class": "dual-platform",
            "coords_resolved": True,
            "coords_source": "tasklet_bucketB_handoff",
            "confidence": "high",
            "status": "operational",
            "tier_sort_key": 2,
            "_bucketB_applied_at": now,
        },
    }


def make_poi_feature(city_id: str, bp: dict) -> dict:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    name = bp["name"]
    conf = bp.get("confidence") or "medium"
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [bp["lng"], bp["lat"]],
        },
        "properties": {
            "id": bp["id"],
            "type": "poi",
            "name": name,
            "shortName": name.split("(")[0].strip(),
            "parent_city_id": city_id,
            "bp_type": bp.get("type", "public_pier"),
            "bp_type_label": bp_type_label(bp.get("type")),
            "relevance": bp.get("relevance"),
            "operator": bp.get("operator") or None,
            "coords_resolved": True,
            "confidence": conf,
            "precision": bp.get("precision"),
            "source": bp.get("source"),
            "formatted_address": bp.get("formatted_address"),
            "linked_locale": bp.get("linked_locale"),
            "_gazetteer_source": f"tasklet_bucketB:{city_id}",
            "_tasklet_provenance": "grok-bucketB-handoff-2026-06-19",
            "validation_log": bp.get("validation_log", []),
            "last_enriched": now,
            "status": "operational" if conf in ("high", "medium") else "aspirational",
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    args = ap.parse_args()

    work = Path(args.work)
    dc = work / "atlas-repo" / "data-clean"
    fbt_path = dc / "FEATURES_BY_TYPE.json"
    fbt = load_json(fbt_path)

    report = {
        "phase": "apply",
        "tier12_cities": [],
        "tier3_crosswalk": TIER3_CROSSWALK,
        "pois_removed": [],
        "pois_added": [],
    }

    # Remove legacy Lisbon + Abidjan POIs (zero id overlap with handoff)
    replace_parents = {"lisbon-tagus-portugal", "abidjan-cote-divoire"}
    kept_pois = []
    for poi in fbt.get("poi", []):
        pid = poi.get("properties", poi).get("id")
        parent = poi.get("properties", poi).get("parent_city_id")
        if parent in replace_parents:
            report["pois_removed"].append({"id": pid, "parent": parent})
            continue
        kept_pois.append(poi)
    fbt["poi"] = kept_pois

    cities = fbt.setdefault("city", [])
    city_ids = {c.get("properties", c).get("id") for c in cities}

    for city_id in TIER12:
        handoff_path = HANDOFF / f"{city_id}-boarding-points.json"
        if not handoff_path.exists():
            print(f"✗ missing handoff: {handoff_path}", file=sys.stderr)
            sys.exit(1)
        data = load_json(handoff_path)
        anchor = data.get("city_anchor")
        if not anchor or len(anchor) < 2:
            print(f"✗ bad anchor: {city_id}", file=sys.stderr)
            sys.exit(1)

        if city_id not in city_ids:
            cities.append(make_city_feature(city_id, anchor))
            city_ids.add(city_id)
            report["tier12_cities"].append({"id": city_id, "action": "minted_city_pin"})
        else:
            for c in cities:
                props = c.get("properties", c)
                if props.get("id") == city_id:
                    c["geometry"]["coordinates"] = [anchor[0], anchor[1]]
                    props["coords_resolved"] = True
                    props["coords_source"] = "tasklet_bucketB_handoff"
                    break
            report["tier12_cities"].append({"id": city_id, "action": "updated_city_pin"})

        for bp in data.get("boarding_points", []):
            if bp.get("lng") is None or bp.get("lat") is None:
                continue
            feat = make_poi_feature(city_id, bp)
            fbt["poi"].append(feat)
            report["pois_added"].append({"id": bp["id"], "city": city_id, "confidence": bp.get("confidence")})

    save_json(fbt_path, fbt)
    out = work / "grok-routing-output" / "bucketB-apply-report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    save_json(out, report)

    print(
        f"bucketB apply: cities={len(report['tier12_cities'])} "
        f"pois_added={len(report['pois_added'])} pois_removed={len(report['pois_removed'])}"
    )
    print(f"report: {out}")


if __name__ == "__main__":
    main()