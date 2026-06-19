#!/usr/bin/env python3
"""
Seal Bolt/Yango handoff boarding-points/*.json into FEATURES_BY_TYPE.json.
Every BP is either sealed as a POI or ledgered with an explicit reason — 0 silent drops.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from bolt_yango_shared import (
    INGEST,
    RSG_HOLD_CITIES,
    infer_country_region,
    is_internal_metadata_bp,
    load_json,
    load_land_mask,
    mint_bp_id,
    normalize_name,
    now_iso,
    resolve_city_id,
    save_json,
    scrub_field,
    water_distance_km,
    in_allowlist_bbox,
)

ROOT = Path(__file__).resolve().parents[2]
SPECIAL_SKIP = {"_JUNK-POI-REMEDIATION.json"}


def bp_type_label(bp_type: str | None) -> str | None:
    if not bp_type:
        return None
    return bp_type.replace("_", " ").title()


def collect_city_layers(fbt: dict) -> tuple[list, set[str], dict]:
    cities = fbt.setdefault("city", [])
    known: set[str] = set()
    meta: dict[str, dict] = {}
    for layer in ("city", "priority_city"):
        for feat in fbt.get(layer, []):
            props = feat.get("properties", feat)
            cid = props.get("id")
            if not cid:
                continue
            known.add(cid)
            meta[cid] = props
    return cities, known, meta


def build_poi_indexes(pois: list) -> tuple[dict, dict, dict]:
    by_id: dict[str, dict] = {}
    by_name: dict[tuple[str, str], str] = {}
    by_parent: dict[str, int] = {}
    for poi in pois:
        props = poi.get("properties", poi)
        pid = props.get("id")
        parent = props.get("parent_city_id")
        if pid:
            by_id[pid] = poi
        if parent and props.get("name"):
            by_name[(parent, normalize_name(props["name"]))] = pid
        if parent:
            by_parent[parent] = by_parent.get(parent, 0) + 1
    return by_id, by_name, by_parent


def make_city_feature(city_id: str, anchor: list[float], city_name: str | None, template: dict | None) -> dict:
    country, region = infer_country_region(city_id, city_name)
    name = city_name or city_id.replace("-", " ").title()
    short = (name.split(",")[0].split("(")[0].strip() or name)[:32]
    if template:
        country = template.get("country") or country
        region = template.get("region") or region
        name = template.get("name") or template.get("fullName") or name
        short = template.get("shortName") or short
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [anchor[0], anchor[1]]},
        "properties": {
            "id": city_id,
            "type": "city",
            "name": name,
            "shortName": short,
            "fullName": name,
            "country": country,
            "region": region,
            "platform_class": "dual-platform",
            "coords_resolved": True,
            "coords_source": "bolt_yango_handoff_2026-06-19",
            "confidence": "high",
            "status": "operational",
            "tier_sort_key": 2,
            "_bolt_yango_applied_at": now_iso(),
        },
    }


def make_poi_feature(city_id: str, bp: dict, sealed_id: str) -> dict:
    name = scrub_field(bp["name"]) or bp["name"]
    conf = bp.get("confidence") or "medium"
    operator = bp.get("operator")
    if operator and str(operator).lower().startswith("counterparty"):
        operator = None
    else:
        operator = scrub_field(operator)
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [bp["lng"], bp["lat"]]},
        "properties": {
            "id": sealed_id,
            "type": "poi",
            "name": name,
            "shortName": name.split("(")[0].strip(),
            "parent_city_id": city_id,
            "bp_type": bp.get("type", "public_pier"),
            "bp_type_label": bp_type_label(bp.get("type")),
            "relevance": bp.get("relevance"),
            "operator": operator,
            "coords_resolved": True,
            "confidence": conf,
            "precision": bp.get("precision"),
            "source": scrub_field(bp.get("source")),
            "formatted_address": scrub_field(bp.get("formatted_address")),
            "linked_locale": bp.get("linked_locale"),
            "_gazetteer_source": f"bolt_yango_handoff:{city_id}",
            "_tasklet_provenance": "bolt-yango-seal-2026-06-19",
            "_handoff_bp_id": bp.get("id"),
            "validation_log": bp.get("validation_log", []),
            "last_enriched": now_iso(),
            "status": "operational" if conf in ("high", "medium") else "aspirational",
        },
    }


def parse_city_file(path: Path) -> dict | None:
    data = load_json(path)
    if isinstance(data, list):
        return None
    if not isinstance(data, dict):
        return None
    return data


def parse_anchor(data: dict) -> list[float] | None:
    anchor = data.get("city_anchor") or data.get("anchor")
    if isinstance(anchor, dict):
        lng, lat = anchor.get("lng"), anchor.get("lat")
        if lng is not None and lat is not None:
            return [float(lng), float(lat)]
        return None
    if isinstance(anchor, list) and len(anchor) >= 2:
        return [float(anchor[0]), float(anchor[1])]
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dc", default="data-clean")
    ap.add_argument("--ingest", default=str(INGEST))
    ap.add_argument("--max-inland-km", type=float, default=0.15)
    args = ap.parse_args()

    ingest = Path(args.ingest)
    dc = ROOT / args.dc
    bp_dir = ingest / "boarding-points"
    allowlist = load_json(ingest / "inputs/bp_water_allowlist.json")
    junk_rows = load_json(bp_dir / "_JUNK-POI-REMEDIATION.json")
    junk_ids = {r["junk_id"] for r in junk_rows if r.get("junk_id")}

    fbt_path = dc / "FEATURES_BY_TYPE.json"
    fbt = load_json(fbt_path)
    cities, known, city_meta = collect_city_layers(fbt)
    pois = fbt.setdefault("poi", [])
    by_id, by_name, by_parent_before = build_poi_indexes(pois)
    mask = load_land_mask()

    report = {
        "phase": "apply_boarding_points",
        "files_total": 0,
        "files_processed": 0,
        "files_skipped": [],
        "cities_minted": [],
        "cities_updated_anchor": [],
        "sealed": [],
        "reconciled_existing": [],
        "dropped": [],
        "ledger": [],
        "pois_before": len(pois),
        "silent_drops": 0,
    }

    city_files = sorted(bp_dir.glob("*.json"))
    report["files_total"] = len(city_files)

    for path in city_files:
        fname = path.name
        if fname in SPECIAL_SKIP:
            report["files_skipped"].append({"file": fname, "reason": "junk_remediation_ledger"})
            for row in junk_rows:
                report["ledger"].append(
                    {
                        "file": fname,
                        "handoff_id": row.get("junk_id"),
                        "city": row.get("city"),
                        "action": "junk_repoint",
                        "reason": f"repoint_to:{row.get('repoint_id')}",
                        "name": row.get("junk_name"),
                    }
                )
            continue

        data = parse_city_file(path)
        if data is None:
            report["files_skipped"].append({"file": fname, "reason": "unparseable_shape"})
            report["ledger"].append({"file": fname, "action": "file_skip", "reason": "unparseable_shape"})
            continue

        report["files_processed"] += 1
        raw_city = data.get("city_id")
        if not raw_city:
            report["ledger"].append({"file": fname, "action": "file_skip", "reason": "missing_city_id"})
            continue

        city_id = resolve_city_id(raw_city, known)
        anchor = parse_anchor(data)
        bps = data.get("boarding_points") or []

        if city_id not in known:
            if not anchor:
                report["ledger"].append(
                    {"file": fname, "city": city_id, "action": "city_hold", "reason": "missing_city_anchor"}
                )
            else:
                cities.append(make_city_feature(city_id, anchor, data.get("city_name"), None))
                known.add(city_id)
                report["cities_minted"].append({"id": city_id, "file": fname, "n_bps": len(bps)})
        elif anchor:
            for layer in ("city", "priority_city"):
                for feat in fbt.get(layer, []):
                    props = feat.get("properties", feat)
                    if props.get("id") == city_id:
                        geom = feat.setdefault("geometry", {"type": "Point", "coordinates": [0, 0]})
                        geom["coordinates"] = [anchor[0], anchor[1]]
                        props["coords_resolved"] = True
                        props["coords_source"] = "bolt_yango_handoff_2026-06-19"
                        report["cities_updated_anchor"].append(city_id)
                        break

        hold_rsg = raw_city in RSG_HOLD_CITIES or city_id in RSG_HOLD_CITIES

        for bp in bps:
            handoff_id = bp.get("id") or ""
            name = bp.get("name") or handoff_id or "unknown"
            base = {
                "file": fname,
                "city": city_id,
                "handoff_id": handoff_id,
                "name": name,
            }

            if hold_rsg:
                entry = {**base, "action": "rsg_crosswalk_hold", "reason": "reuse_existing_rsg_pois"}
                report["dropped"].append(entry)
                report["ledger"].append(entry)
                continue

            if handoff_id in junk_ids:
                entry = {**base, "action": "junk_repoint", "reason": "listed_in_JUNK-POI-REMEDIATION"}
                report["dropped"].append(entry)
                report["ledger"].append(entry)
                continue

            meta_reason = is_internal_metadata_bp(bp)
            if meta_reason:
                entry = {**base, "action": "drop", "reason": meta_reason}
                report["dropped"].append(entry)
                report["ledger"].append(entry)
                continue

            lng, lat = bp.get("lng"), bp.get("lat")
            if lng is None or lat is None:
                entry = {**base, "action": "drop", "reason": "missing_coords"}
                report["dropped"].append(entry)
                report["ledger"].append(entry)
                continue

            sealed_id = mint_bp_id(city_id, bp)
            if handoff_id.startswith("bp-") and handoff_id in by_id:
                sealed_id = handoff_id
            elif handoff_id in by_id:
                sealed_id = handoff_id

            name_key = (city_id, normalize_name(name))
            if sealed_id not in by_id and name_key in by_name:
                existing_id = by_name[name_key]
                entry = {
                    **base,
                    "action": "reconciled_existing",
                    "sealed_id": existing_id,
                    "reason": "name_match_existing_poi",
                }
                report["reconciled_existing"].append(entry)
                report["ledger"].append(entry)
                continue

            if sealed_id in by_id:
                entry = {**base, "action": "already_sealed", "sealed_id": sealed_id}
                report["reconciled_existing"].append(entry)
                report["ledger"].append(entry)
                continue

            if not in_allowlist_bbox(lng, lat, allowlist):
                inland = water_distance_km(lng, lat, mask)
                if inland > args.max_inland_km:
                    entry = {
                        **base,
                        "action": "drop",
                        "reason": "water_adjacency_fail",
                        "water_distance_km": inland,
                    }
                    report["dropped"].append(entry)
                    report["ledger"].append(entry)
                    continue

            feat = make_poi_feature(city_id, bp, sealed_id)
            pois.append(feat)
            by_id[sealed_id] = feat
            by_name[name_key] = sealed_id
            entry = {**base, "action": "sealed", "sealed_id": sealed_id}
            report["sealed"].append(entry)
            report["ledger"].append(entry)

    report["pois_after"] = len(pois)
    report["pois_added"] = len(report["sealed"])
    report["ledger_count"] = len(report["ledger"])

    # 0 silent drops: every BP in every processed city file must appear in ledger
    accounted = 0
    expected = 0
    for path in city_files:
        if path.name in SPECIAL_SKIP:
            continue
        data = parse_city_file(path)
        if not data:
            continue
        expected += len(data.get("boarding_points") or [])
    accounted = len(report["ledger"]) - sum(
        1 for e in report["ledger"] if e.get("file") == "_JUNK-POI-REMEDIATION.json"
    )
    # junk ledger entries are separate from city BPs
    junk_ledger = sum(1 for e in report["ledger"] if e.get("action") == "junk_repoint" and e.get("file") == "_JUNK-POI-REMEDIATION.json")
    city_ledger = len(report["ledger"]) - junk_ledger
    report["expected_bps"] = expected
    report["accounted_bps"] = city_ledger
    report["silent_drops"] = max(0, expected - city_ledger)

    save_json(fbt_path, fbt)
    out = ROOT / "grok-routing-output" / "bolt-yango-bp-apply-report.json"
    save_json(out, report)

    print(
        f"BP apply: files={report['files_processed']} sealed={len(report['sealed'])} "
        f"reconciled={len(report['reconciled_existing'])} dropped={len(report['dropped'])} "
        f"pois {report['pois_before']}→{report['pois_after']} silent_drops={report['silent_drops']}"
    )
    print(f"report: {out}")

    if report["silent_drops"] > 0:
        print(f"✗ SILENT DROPS: {report['silent_drops']}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()