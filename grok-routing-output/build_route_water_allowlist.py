#!/usr/bin/env python3
"""LB-242 — build data-clean/route_water_allowlist.json from qa_baseline.json."""
from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASELINE = ROOT / "data-clean/qa_baseline.json"
ROUTES_LIVE = ROOT / "data-clean/ROUTES.json"
ROUTES_DELTA = ROOT / "_ingest/gold-delta-LB230-LB241/data-clean/ROUTES.json"
REQUESTS = ROOT / "_review/grok-routing-v2/grok-routing-v2/failing-cases/route-requests.jsonl"
OUT = ROOT / "data-clean/route_water_allowlist.json"
RESTORE_OUT = Path(__file__).resolve().parent / "restored-routes-LB-242.json"

BBOX = {
    "great_lakes": (-93.5, 41.0, -75.5, 49.5),
    "belize_lagoon": (-89.5, 15.8, -87.5, 18.5),
    "mafia_channel": (38.5, -8.0, 40.5, -5.5),
    "bora_bora_lagoon": (-152.5, -17.2, -151.0, -16.2),
    "penghu": (119.2, 23.2, 119.8, 23.8),
    "palm_archipelago": (54.95, 24.95, 55.35, 25.25),
}

ID_PATTERNS = {
    "great_lakes": re.compile(
        r"chicago|lake-michigan|great-lakes|detroit|milwaukee|traverse|mackinac|"
        r"door-county|green-bay|new-buffalo|saugatuck|south-haven|lake-erie|"
        r"lake-ontario|lake-huron|muskegon|grand-haven",
        re.I,
    ),
    "belize_lagoon": re.compile(r"belize", re.I),
    "mafia_channel": re.compile(r"mafia|kilindoni|dar-es-salaam", re.I),
    "bora_bora_lagoon": re.compile(r"bora-bora|moorea|raiatea|tahaa|tahiti", re.I),
    "penghu": re.compile(r"penghu|magong|kaohsiung.*penghu", re.I),
    "palm_archipelago": re.compile(
        r"palm|jumeirah|atlantis|kempinski|waldorf|zabeel|anantara|one-only|"
        r"five-palm|rixos|bluewaters|dmyc|jbr-the-walk|dubai-harbour|"
        r"dubai-marina|dubai-creek",
        re.I,
    ),
}

RESTORE_IDS = {
    "e__chicago-lake-michigan-usa__dusable-harbor-chicago__new-buffalo-municipal-marina": "great_lakes",
    "e__belize-city-cayes-belize__belize-city-water-taxi__placencia-belize__placencia-village-pier": "belize_lagoon",
    "e__mafia-tanzania__kilindoni-port__dar-es-salaam-tanzania__dar-ferry-terminal": "mafia_channel",
}


def load_routes_index() -> dict:
    idx = {}
    for path in (ROUTES_LIVE, ROUTES_DELTA):
        if not path.exists():
            continue
        data = json.loads(path.read_text())
        feats = data["features"] if isinstance(data, dict) else data
        for f in feats:
            idx[f["properties"]["id"]] = f
    return idx


def load_deny() -> set[str]:
    deny = set()
    if not REQUESTS.exists():
        return deny
    for line in REQUESTS.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("route_id"):
            deny.add(row["route_id"])
    return deny


def route_bbox(f: dict) -> tuple[float, float, float, float]:
    coords = f["geometry"]["coordinates"]
    lons = [c[0] for c in coords]
    lats = [c[1] for c in coords]
    return min(lons), min(lats), max(lons), max(lats)


def overlaps(a: tuple, b: tuple) -> bool:
    return not (a[2] < b[0] or a[0] > b[2] or a[3] < b[1] or a[1] > b[3])


def classify(rid: str, feat: dict | None) -> str:
    if rid in RESTORE_IDS:
        return RESTORE_IDS[rid]
    props = (feat or {}).get("properties", {})
    text = " ".join(
        [
            rid,
            str(props.get("from_city_id", "")),
            str(props.get("to_city_id", "")),
            str(props.get("label", "")),
            str(props.get("from", "")),
            str(props.get("to", "")),
        ]
    )
    for cat, rx in ID_PATTERNS.items():
        if rx.search(text):
            return cat
    if feat:
        bb = route_bbox(feat)
        for cat, box in BBOX.items():
            if overlaps(bb, box):
                return cat
    return "global_inland_water_fp"


def main() -> None:
    baseline = json.loads(BASELINE.read_text())
    flagged = set(baseline["flagged_ids"])
    idx = load_routes_index()
    deny = load_deny()

    categories: dict[str, list[str]] = defaultdict(list)
    denied: list[str] = []

    for rid in sorted(flagged | set(RESTORE_IDS)):
        if rid in deny:
            denied.append(rid)
            continue
        cat = classify(rid, idx.get(rid))
        categories[cat].append(rid)

    ids = sorted({rid for cat_ids in categories.values() for rid in cat_ids})
    payload = {
        "_meta": {
            "lb": "LB-242",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "baseline_flagged": baseline["flagged_count"],
            "allowlisted_count": len(ids),
            "denied_active_fix_count": len(denied),
            "expected_effective_flagged": len(denied),
            "method": "qa_baseline flagged_ids minus grok route-requests resolve route_ids; "
            "categorized by id pattern + route bbox overlap",
            "deny_reason": "Grok Phase 3 active geometry fixes — must remain gate-visible",
        },
        "categories": {k: len(v) for k, v in sorted(categories.items())},
        "denied_active_fix_ids": sorted(denied),
        "restore_scrubbed_ids": sorted(RESTORE_IDS),
        "ids": ids,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n")

    restored = {
        "type": "FeatureCollection",
        "features": [idx[rid] for rid in sorted(RESTORE_IDS) if rid in idx],
    }
    RESTORE_OUT.write_text(json.dumps(restored, indent=2) + "\n")

    print(f"wrote {OUT} ({len(ids)} ids, {len(denied)} denied)")
    print(f"wrote {RESTORE_OUT} ({len(restored['features'])} features)")


if __name__ == "__main__":
    main()