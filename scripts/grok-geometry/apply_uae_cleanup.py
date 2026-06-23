#!/usr/bin/env python3
"""Apply UAE locale + POI cleanup from UAE-CLEANUP-LEDGER.json (PR #82)."""
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

DEFAULT_LEDGER = ROOT / "handoff/uae-locale-cleanup-2026-06-24/inputs/UAE-CLEANUP-LEDGER.json"
REPORT_PATH = ROOT / "grok-routing-output/uae-cleanup-seal-report.json"

UAE_CITIES = frozenset(
    {"dubai-uae", "abu-dhabi-uae", "sharjah-uae", "ras-al-khaimah-uae", "fujairah-uae"}
)

CORRIDOR_LOCALE_RE = re.compile(
    r"corridor endpoint|mid-corridor|overland|from <place>|cross-emirate|cross-border|pointer",
    re.I,
)

# Legitimate distant outliers — do not residual-drop
ALLOWLIST_KEYWORDS: dict[str, tuple[str, ...]] = {
    "abu-dhabi-uae": (
        "sir bani yas", "delma", "dalma", "mugheirah", "sila", "marawah", "jebel dhanna",
        "ruwais", "mirfa", "al yasat", "dhafra", "western region",
    ),
    "sharjah-uae": ("khorfakkan", "kalba", "khor kalba"),
    "fujairah-uae": ("dibba", "aqah", "murbah", "dadna"),
}

WRONG_EMIRATE_TOKENS: dict[str, tuple[str, ...]] = {
    "dubai-uae": ("abu dhabi", "sharjah", "ajman", "ras al khaimah", "rak ", "fujairah", "khorfakkan"),
    "abu-dhabi-uae": ("dubai", "sharjah", "jumeirah", "deira", "marina dubai", "jbr"),
    "sharjah-uae": ("dubai marina", "dubai harbour", "abu dhabi", "ras al khaimah"),
    "ras-al-khaimah-uae": ("dubai", "abu dhabi", "sharjah"),
    "fujairah-uae": ("dubai", "abu dhabi"),
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def collect_drop_ids(ledger: dict) -> dict[str, str]:
    out: dict[str, str] = {}
    for row in ledger.get("locale_layer", {}).get("drop", []):
        out[row["id"]] = row.get("reason", "locale_layer.drop")
    for city, rows in (ledger.get("poi_layer", {}).get("drops") or {}).items():
        for row in rows:
            out[row["id"]] = row.get("reason", "poi_layer.drop")
    return out


def is_allowlisted(parent: str, name: str) -> bool:
    blob = name.lower()
    for kw in ALLOWLIST_KEYWORDS.get(parent, ()):
        if kw in blob:
            return True
    return False


def residual_drop_reason(parent: str, name: str) -> str | None:
    if is_allowlisted(parent, name):
        return None
    blob = name.lower()
    for tok in WRONG_EMIRATE_TOKENS.get(parent, ()):
        if tok in blob:
            return f"residual_gate wrong-emirate token ({tok.strip()})"
    return None


def drop_city_brief(city_briefs: Path, locale_id: str) -> bool:
    stub = city_briefs / f"{locale_id}.json"
    if stub.exists():
        stub.unlink()
        return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dc", default="data-clean")
    ap.add_argument("--ledger", default=str(DEFAULT_LEDGER))
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    dc = ROOT / args.dc
    ledger = load_json(Path(args.ledger))
    ledger_drops = collect_drop_ids(ledger)
    keep_locale_ids = {r["id"] for r in ledger.get("locale_layer", {}).get("keep", [])}

    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    clusters = load_json(dc / "CLUSTERS.json")
    city_briefs = dc / "city_briefs"

    locales_before = len(fbt.get("locale", []))
    uae_poi_before = sum(
        1 for p in fbt.get("poi", [])
        if (p.get("properties") or {}).get("parent_city_id") in UAE_CITIES
    )

    locale_actions: list[dict] = []
    poi_actions: list[dict] = []
    briefs_removed: list[str] = []

    # --- locale layer ---
    new_locales = []
    for loc in fbt.get("locale", []):
        props = loc.get("properties", loc)
        lid = props.get("id")
        parent = props.get("parent_city_id")
        if parent not in UAE_CITIES:
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

    # --- POI layer ---
    mask = load_land_mask() if args.apply else None
    new_pois = []
    for poi in fbt.get("poi", []):
        props = poi.get("properties", poi)
        pid = props.get("id")
        parent = props.get("parent_city_id")
        name = props.get("name") or ""
        if parent not in UAE_CITIES:
            new_pois.append(poi)
            continue
        if pid in ledger_drops:
            poi_actions.append({"id": pid, "action": "drop", "reason": ledger_drops[pid]})
            continue
        reason = residual_drop_reason(parent, name)
        if reason:
            poi_actions.append({"id": pid, "action": "drop", "reason": reason})
            continue
        coords = (poi.get("geometry") or {}).get("coordinates")
        if mask and coords and len(coords) >= 2:
            wd = water_distance_km(coords[0], coords[1], mask)
            if wd > 2.0 and not is_allowlisted(parent, name):
                poi_actions.append({"id": pid, "action": "drop", "reason": f"residual_gate water_distance_km={wd:.1f}"})
                continue
        poi_actions.append({"id": pid, "action": "keep"})
        if not props.get("source_url") and not props.get("_gazetteer_source"):
            props.setdefault("source_url", f"uae_gold:{pid}")
        new_pois.append(poi)

    # --- CLUSTERS.json locale refs ---
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

    dropped_locales = [a for a in locale_actions if a["action"] == "drop"]
    dropped_pois = [a for a in poi_actions if a["action"] == "drop"]
    kept_locales = [a for a in locale_actions if a["action"] == "keep"]
    kept_pois = [a for a in poi_actions if a["action"] == "keep"]

    report = {
        "at": utc_now(),
        "lane": "grok/apply_uae_cleanup",
        "apply": args.apply,
        "before": {"uae_locales": locales_before, "uae_pois": uae_poi_before},
        "after": {
            "uae_locales": len(kept_locales) if args.apply else locales_before - len(dropped_locales),
            "uae_pois": len(kept_pois) if args.apply else uae_poi_before - len(dropped_pois),
        },
        "locale_drops": len(dropped_locales),
        "poi_ledger_drops": sum(1 for a in dropped_pois if a["reason"] in ledger_drops.values() or a["id"] in ledger_drops),
        "poi_residual_drops": sum(1 for a in dropped_pois if a["id"] not in ledger_drops),
        "kept_locales": len(kept_locales),
        "kept_pois": len(kept_pois),
        "briefs_removed": briefs_removed,
        "cluster_locale_drops": cluster_locale_drops,
        "guardrail": "corridor-endpoint rows never promoted to locale pins",
        "silent_drops": 0,
        "actions": {"locale": locale_actions, "poi": poi_actions},
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    save_json(REPORT_PATH, report)
    print(json.dumps({k: report[k] for k in ("before", "after", "locale_drops", "poi_ledger_drops", "poi_residual_drops", "silent_drops")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())