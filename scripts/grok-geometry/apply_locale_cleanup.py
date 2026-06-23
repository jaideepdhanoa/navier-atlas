#!/usr/bin/env python3
"""Apply locale + POI cleanup from Tasklet ledger (Thailand PR #89, Bolt PR #90)."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
from bolt_yango_shared import load_json, save_json, water_distance_km, load_land_mask  # noqa: E402

CORRIDOR_LOCALE_RE = re.compile(
    r"via |cross-gulf|cross-border|round s tip|gulf-of-thailand|corridor|gateway|"
    r"pointer|endpoint|\+| / ",
    re.I,
)

SOVEREIGN_EXCLUDE = frozenset(
    {"neom-ksa", "neom-sindalah-ksa", "amaala-ksa", "red-sea-global", "red-sea-global-ksa", "sindalah-ksa"}
)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def in_scope(parent: str, scope: set[str] | None, suffixes: tuple[str, ...] | None) -> bool:
    if parent in SOVEREIGN_EXCLUDE:
        return False
    if scope is not None:
        return parent in scope
    if suffixes:
        return any(parent.endswith(f"-{s}") for s in suffixes)
    return False


def collect_ledger_actions(ledger: dict) -> tuple[dict[str, str], dict[str, dict], set[str]]:
    """Returns (drop_reasons, retag_map, keep_locale_ids)."""
    drops: dict[str, str] = {}
    retags: dict[str, dict] = {}

    poi = ledger.get("poi_layer", {})
    for row in (poi.get("dedup_exact_drops", {}).get("drops") or []):
        drops[row["id"]] = row.get("reason", "dedup_exact")
    for row in (poi.get("junk_annotation_drops", {}).get("drops") or poi.get("junk_drops", {}).get("drops") or []):
        drops[row["id"]] = row.get("reason", "junk_drop")
    for row in (poi.get("retag_identity", {}).get("retags") or []):
        retags[row["id"]] = row

    keep_locale = {r["id"] for r in ledger.get("locale_layer", {}).get("keep", [])}
    for row in ledger.get("locale_layer", {}).get("drop", []):
        drops[row["id"]] = row.get("reason", "locale_drop")

    return drops, retags, keep_locale


def rekey_endpoint(val: str | None, old_city: str, new_city: str, pid: str) -> str | None:
    if not val:
        return val
    if val == pid:
        return pid
    if val.startswith(f"{old_city}__"):
        return f"{new_city}__{val.split('__', 1)[1]}"
    if val == old_city:
        return new_city
    return val


def drop_city_brief(city_briefs: Path, locale_id: str) -> bool:
    stub = city_briefs / f"{locale_id}.json"
    if stub.exists():
        stub.unlink()
        return True
    return False


def fuzzy_dup_key(name: str) -> str:
    n = re.sub(r"[^\w\s]", "", (name or "").lower())
    n = re.sub(r"\s+", " ", n).strip()
    for strip in ("pier", "jetty", "marina", "port", "ferry", "terminal", "mainland gateway"):
        n = n.replace(strip, "")
    return re.sub(r"\s+", " ", n).strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dc", default="data-clean")
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--report", required=True)
    ap.add_argument("--lane", default="grok/apply_locale_cleanup")
    ap.add_argument("--scope-suffix", action="append", default=[])
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    dc = ROOT / args.dc
    ledger = load_json(Path(args.ledger))
    ledger_drops, retag_map, keep_locale_ids = collect_ledger_actions(ledger)

    suffixes = tuple(args.scope_suffix or ledger.get("scope_suffixes") or ("thailand",))
    excluded = set(ledger.get("excluded") or ())
    if excluded:
        suffixes = tuple(s for s in suffixes if s not in excluded)

    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    clusters = load_json(dc / "CLUSTERS.json")
    city_briefs = dc / "city_briefs"
    routes_raw = load_json(dc / "ROUTES.json")
    routes_is_list = isinstance(routes_raw, list)
    routes = routes_raw if routes_is_list else routes_raw.get("features", [])

    def scoped_poi_count() -> int:
        return sum(
            1 for p in fbt.get("poi", [])
            if in_scope((p.get("properties") or {}).get("parent_city_id", ""), None, suffixes)
        )

    def scoped_locale_count() -> int:
        return sum(
            1 for loc in fbt.get("locale", [])
            if in_scope((loc.get("properties") or loc).get("parent_city_id", ""), None, suffixes)
        )

    poi_before = scoped_poi_count()
    locales_before = scoped_locale_count()

    locale_actions: list[dict] = []
    poi_actions: list[dict] = []
    briefs_removed: list[str] = []
    route_rehomes = 0

    # --- locale layer ---
    new_locales = []
    for loc in fbt.get("locale", []):
        props = loc.get("properties", loc)
        lid = props.get("id")
        parent = props.get("parent_city_id", "")
        if not in_scope(parent, None, suffixes):
            new_locales.append(loc)
            continue
        if lid in ledger_drops:
            locale_actions.append({"id": lid, "action": "drop", "reason": ledger_drops[lid]})
            if args.apply:
                drop_city_brief(city_briefs, lid)
                briefs_removed.append(lid)
            continue
        if lid not in keep_locale_ids:
            locale_actions.append({"id": lid, "action": "drop", "reason": "not in keep[]"})
            if args.apply:
                drop_city_brief(city_briefs, lid)
                briefs_removed.append(lid)
            continue
        if CORRIDOR_LOCALE_RE.search(props.get("name") or ""):
            locale_actions.append({"id": lid, "action": "drop", "reason": "corridor-artifact guardrail"})
            continue
        locale_actions.append({"id": lid, "action": "keep"})
        new_locales.append(loc)

    # --- POI layer: dedup + retag + junk ---
    poi_by_id: dict[str, dict] = {}
    for poi in fbt.get("poi", []):
        props = poi.get("properties", poi)
        poi_by_id[props.get("id")] = poi

    # fuzzy near-duplicate merge within same parent (residual gate)
    merge_drop: set[str] = set()
    by_parent_key: dict[tuple[str, str], list[str]] = {}
    for pid, poi in poi_by_id.items():
        props = poi.get("properties", poi)
        parent = props.get("parent_city_id", "")
        if not in_scope(parent, None, suffixes) or pid in ledger_drops:
            continue
        key = (parent, fuzzy_dup_key(props.get("name") or ""))
        if key[1]:
            by_parent_key.setdefault(key, []).append(pid)

    for key, ids in by_parent_key.items():
        if len(ids) < 2:
            continue
        keep_id = min(ids)
        for drop_id in ids:
            if drop_id != keep_id:
                merge_drop.add(drop_id)
                poi_actions.append({
                    "id": drop_id, "action": "drop",
                    "reason": f"residual_gate fuzzy_dup merge -> {keep_id}",
                })

    new_pois = []
    retag_applied: dict[str, str] = {}
    mask = load_land_mask() if args.apply else None

    for poi in fbt.get("poi", []):
        props = poi.get("properties", poi)
        pid = props.get("id")
        parent = props.get("parent_city_id", "")
        name = props.get("name") or ""

        if not in_scope(parent, None, suffixes):
            new_pois.append(poi)
            continue

        if pid in ledger_drops or pid in merge_drop:
            if pid in ledger_drops:
                poi_actions.append({"id": pid, "action": "drop", "reason": ledger_drops[pid]})
            continue

        if pid in retag_map:
            row = retag_map[pid]
            new_parent = row["to"]
            retag_applied[pid] = new_parent
            props["parent_city_id"] = new_parent
            props["_locale_cleanup_retag"] = row.get("reason", "retag_identity")
            poi_actions.append({"id": pid, "action": "retag", "from": row["from"], "to": new_parent})
            new_pois.append(poi)
            continue

        coords = (poi.get("geometry") or {}).get("coordinates")
        if mask and coords and len(coords) >= 2:
            wd = water_distance_km(coords[0], coords[1], mask)
            if wd > 3.0:
                poi_actions.append({"id": pid, "action": "drop", "reason": f"residual_gate water_distance_km={wd:.1f}"})
                continue

        poi_actions.append({"id": pid, "action": "keep"})
        if not props.get("source_url") and not props.get("_gazetteer_source"):
            props.setdefault("source_url", f"locale_cleanup:{pid}")
        new_pois.append(poi)

    # --- route endpoint rehome ---
    for route in routes:
        props = route.get("properties", route)
        changed = False
        for field in ("from", "to", "from_city_id", "to_city_id"):
            val = props.get(field)
            if not val:
                continue
            for pid, new_parent in retag_applied.items():
                row = retag_map[pid]
                old_parent = row["from"]
                new_val = rekey_endpoint(val, old_parent, new_parent, pid)
                if new_val != val:
                    props[field] = new_val
                    changed = True
        if changed:
            route_rehomes += 1
            rid = props.get("id", "")
            if rid and "__" in rid:
                parts = rid.split("__")
                if len(parts) >= 3:
                    for i, part in enumerate(parts[:2]):
                        for pid, new_parent in retag_applied.items():
                            row = retag_map[pid]
                            if part == row["from"]:
                                parts[i] = new_parent
                    props["id"] = "__".join(parts)

    cluster_locale_drops = 0
    if args.apply:
        fbt["locale"] = new_locales
        fbt["poi"] = new_pois
        save_json(dc / "FEATURES_BY_TYPE.json", fbt)

        for cl in clusters.get("clusters") or []:
            members = cl.get("member_locale_ids") or cl.get("locale_ids")
            if not isinstance(members, list):
                continue
            before = len(members)
            cl["member_locale_ids"] = [m for m in members if m not in ledger_drops]
            cluster_locale_drops += before - len(cl["member_locale_ids"])
        save_json(dc / "CLUSTERS.json", clusters)

        if routes_is_list:
            save_json(dc / "ROUTES.json", routes)
        else:
            routes_raw["features"] = routes
            save_json(dc / "ROUTES.json", routes_raw)

    dropped_locales = [a for a in locale_actions if a["action"] == "drop"]
    dropped_pois = [a for a in poi_actions if a["action"] == "drop"]
    retagged = [a for a in poi_actions if a["action"] == "retag"]
    kept_locales = [a for a in locale_actions if a["action"] == "keep"]
    kept_pois = [a for a in poi_actions if a["action"] == "keep"]

    report = {
        "at": utc_now(),
        "lane": args.lane,
        "ledger": str(args.ledger),
        "apply": args.apply,
        "scope_suffixes": list(suffixes),
        "before": {"scoped_locales": locales_before, "scoped_pois": poi_before},
        "after": {
            "scoped_locales": len(kept_locales) if args.apply else locales_before - len(dropped_locales),
            "scoped_pois": len(kept_pois) if args.apply else poi_before - len(dropped_pois),
        },
        "dedup_drops": sum(1 for a in dropped_pois if "dedup" in a.get("reason", "").lower()),
        "junk_drops": sum(1 for a in dropped_pois if "junk" in a.get("reason", "").lower() or "annotation" in a.get("reason", "").lower()),
        "retags": len(retagged),
        "fuzzy_merges": len(merge_drop),
        "locale_drops": len(dropped_locales),
        "route_rehomes": route_rehomes,
        "kept_locales": len(kept_locales),
        "kept_pois": len(kept_pois),
        "briefs_removed": briefs_removed,
        "cluster_locale_drops": cluster_locale_drops,
        "guardrail": "corridor-artifact rows never promoted to locale pins",
        "silent_drops": 0,
        "actions": {"locale": locale_actions, "poi": poi_actions},
    }
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    save_json(report_path, report)
    print(json.dumps({k: report[k] for k in (
        "before", "after", "dedup_drops", "junk_drops", "retags", "fuzzy_merges",
        "locale_drops", "route_rehomes", "silent_drops",
    )}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())