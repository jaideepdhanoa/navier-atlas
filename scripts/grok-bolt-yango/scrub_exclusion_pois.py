#!/usr/bin/env python3
"""Remove/scrub POIs that trip the externalization exclusion-token sweep."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from bolt_yango_shared import is_internal_metadata_bp, load_json, save_json, scrub_field

ROOT = Path(__file__).resolve().parents[2]

TOKEN_RES = [
    re.compile(r"\bexclusive\b", re.I),
    re.compile(r"\bwedges?\b", re.I),
    re.compile(r"\bconvener\b", re.I),
    re.compile(r"\bcounterpart(?:y|ies)\b", re.I),
    re.compile(r"\bflag[\s_-]?and[\s_-]?exclude\b", re.I),
]


def poi_blob(props: dict) -> str:
    return json.dumps(props)


def has_token(props: dict) -> bool:
    blob = poi_blob(props)
    return any(p.search(blob) for p in TOKEN_RES)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dc", default="data-clean")
    args = ap.parse_args()

    fbt_path = ROOT / args.dc / "FEATURES_BY_TYPE.json"
    fbt = load_json(fbt_path)
    removed = []
    scrubbed = []
    kept = []

    out_pois = []
    for poi in fbt.get("poi", []):
        props = poi.get("properties", poi)
        bp = {
            "id": props.get("id"),
            "name": props.get("name"),
            "operator": props.get("operator"),
            "notes": props.get("notes"),
            "source": props.get("source"),
            "formatted_address": props.get("formatted_address"),
        }
        meta = is_internal_metadata_bp(bp)
        if meta:
            removed.append({"id": props.get("id"), "reason": meta})
            continue
        if has_token(props):
            for key in (
                "name",
                "shortName",
                "operator",
                "source",
                "formatted_address",
                "fullName",
                "_handoff_bp_id",
            ):
                if key in props and props[key]:
                    props[key] = scrub_field(str(props[key]))
            for key, val in list(props.items()):
                if key.startswith("_") and isinstance(val, str) and any(p.search(val) for p in TOKEN_RES):
                    props[key] = scrub_field(val)
            if has_token(props):
                removed.append({"id": props.get("id"), "reason": "exclusion_token_after_scrub"})
                continue
            scrubbed.append(props.get("id"))
        out_pois.append(poi)

    fbt["poi"] = out_pois
    save_json(fbt_path, fbt)
    report = {"removed": removed, "scrubbed": scrubbed, "poi_count": len(out_pois)}
    out = ROOT / "grok-routing-output" / "bolt-yango-exclusion-scrub-report.json"
    save_json(out, report)
    print(f"scrub: removed={len(removed)} scrubbed={len(scrubbed)} pois={len(out_pois)}")


if __name__ == "__main__":
    main()