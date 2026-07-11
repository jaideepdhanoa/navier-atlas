#!/usr/bin/env python3
"""Fix display capitalization across Region → Cluster → City → Locale.

Rule (permanent):
  - cluster_id / city id / locale id stay kebab-case slugs (stable IDs).
  - Every user-visible name must be human Title Case (or proper local form),
    never the raw slug, never all-lowercase.
  - Canonical cluster display field is `cluster_label` (UI primary).
    Keep `label` and `display` aligned when present.

Usage:
  python3 scripts/grok-taxonomy/fix_display_capitalization_2026_07_11.py
  python3 scripts/grok-taxonomy/validate_cluster_taxonomy.py
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLUSTERS_PATH = ROOT / "data-clean/CLUSTERS.json"
FBT_PATH = ROOT / "data-clean/FEATURES_BY_TYPE.json"
RECEIPT_PATH = (
    ROOT
    / "handoff/backlog-clear-2026-07-11/TAXONOMY-DISPLAY-CAPITALIZATION-RECEIPT-2026-07-11.json"
)

# Explicit cluster_label overrides (country / market chips). Prefer proper nouns.
CLUSTER_LABEL_OVERRIDES: dict[str, str] = {
    "belgium": "Belgium",
    "hong-kong": "Hong Kong",
    "macau": "Macau",
}

# City id → human display names (never use raw slug as name).
CITY_NAME_OVERRIDES: dict[str, dict[str, str]] = {
    "bregenz": {"name": "Bregenz", "shortName": "Bregenz"},
    "hard-at": {"name": "Hard", "shortName": "Hard"},
    "klagenfurt": {"name": "Klagenfurt", "shortName": "Klagenfurt"},
    "krumpendorf": {"name": "Krumpendorf", "shortName": "Krumpendorf"},
    "velden-at": {"name": "Velden", "shortName": "Velden"},
    "korneuburg": {"name": "Korneuburg", "shortName": "Korneuburg"},
    "linz": {"name": "Linz", "shortName": "Linz"},
    "budapest": {"name": "Budapest", "shortName": "Budapest"},
    "siofok": {"name": "Siófok", "shortName": "Siófok"},
    "tihany": {"name": "Tihany", "shortName": "Tihany"},
    "tampere-finland": {"name": "Tampere", "shortName": "Tampere"},
    "turku-finland": {"name": "Turku", "shortName": "Turku"},
    "portsmouth-uk": {"name": "Portsmouth", "shortName": "Portsmouth"},
    "southampton-uk": {"name": "Southampton", "shortName": "Southampton"},
    "isle-of-wight-solent-uk": {
        "name": "Isle of Wight",
        "shortName": "Isle of Wight",
    },
    "bristol-uk": {"name": "Bristol", "shortName": "Bristol"},
    "kiel-germany": {"name": "Kiel", "shortName": "Kiel"},
    "laboe-germany": {"name": "Laboe", "shortName": "Laboe"},
    "rostock-germany": {"name": "Rostock", "shortName": "Rostock"},
    "berlin-waterways-germany": {"name": "Berlin", "shortName": "Berlin"},
    "bonn-rhine-germany": {"name": "Bonn", "shortName": "Bonn"},
    "cologne-rhine-germany": {"name": "Cologne", "shortName": "Cologne"},
    "dusseldorf-rhine-germany": {
        "name": "Düsseldorf",
        "shortName": "Düsseldorf",
    },
}

# Country / region suffix tokens stripped when humanizing city slugs.
_GEO_SUFFIXES = {
    "uk",
    "usa",
    "uae",
    "ksa",
    "at",
    "de",
    "fr",
    "pl",
    "hu",
    "fi",
    "no",
    "se",
    "dk",
    "nl",
    "be",
    "ch",
    "it",
    "es",
    "pt",
    "ie",
    "germany",
    "finland",
    "austria",
    "hungary",
    "poland",
    "france",
    "switzerland",
    "belgium",
    "netherlands",
    "norway",
    "sweden",
    "denmark",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def is_slugish(val: str | None, entity_id: str | None = None) -> bool:
    """True if val is missing, all-lowercase, or the raw kebab slug as display.

    Title Case of a single-word id is OK: id `belgium` → `Belgium`.
    """
    if not val or not str(val).strip():
        return True
    s = str(val).strip()
    # all-lowercase with at least one letter → never a proper display name
    if s == s.lower() and any(ch.isalpha() for ch in s):
        return True
    # leading lowercase letter (ASCII) is wrong for display chips
    if s[0].isascii() and s[0].islower() and s[0].isalpha():
        return True
    if entity_id:
        eid = str(entity_id).strip()
        if s == eid:
            return True
        if "-" in s and s.lower() == eid.lower():
            return True
    return False


def humanize_slug(slug: str) -> str:
    """Best-effort Title Case from a kebab-case id (fallback only)."""
    parts = [p for p in slug.split("-") if p]
    # Drop trailing geo suffixes for city-like ids when enough stem remains
    while len(parts) > 1 and parts[-1].lower() in _GEO_SUFFIXES:
        parts.pop()
    small = {"of", "the", "and", "de", "du", "da", "di", "van", "von", "la", "le"}
    out = []
    for i, p in enumerate(parts):
        low = p.lower()
        if i > 0 and low in small:
            out.append(low)
        else:
            out.append(low[:1].upper() + low[1:] if low else p)
    return " ".join(out) if out else slug


def resolve_cluster_label(c: dict) -> str:
    cid = c.get("cluster_id") or ""
    if cid in CLUSTER_LABEL_OVERRIDES:
        return CLUSTER_LABEL_OVERRIDES[cid]
    for key in ("cluster_label", "label", "display"):
        val = c.get(key)
        if val and not is_slugish(val, cid):
            return str(val).strip()
    return humanize_slug(cid)


def fix_clusters(clusters: list[dict]) -> list[dict]:
    changes = []
    for c in clusters:
        cid = c.get("cluster_id") or ""
        before = {
            "cluster_label": c.get("cluster_label"),
            "label": c.get("label"),
            "display": c.get("display"),
        }
        label = resolve_cluster_label(c)
        c["cluster_label"] = label
        # Explicit overrides always win on label/display too (country chips = country name).
        force_align = cid in CLUSTER_LABEL_OVERRIDES
        if force_align or is_slugish(c.get("label"), cid) or c.get("label") is None:
            c["label"] = label
        if force_align or is_slugish(c.get("display"), cid) or c.get("display") is None:
            c["display"] = label
        after = {
            "cluster_label": c.get("cluster_label"),
            "label": c.get("label"),
            "display": c.get("display"),
        }
        if before != after:
            changes.append({"cluster_id": cid, "before": before, "after": after})
    return changes


def fix_feature_names(fbt: dict) -> list[dict]:
    changes = []
    for kind in ("city", "priority_city", "locale"):
        for feat in fbt.get(kind) or []:
            p = feat.get("properties") or feat
            fid = p.get("id") or ""
            before = {
                "name": p.get("name"),
                "shortName": p.get("shortName"),
                "fullName": p.get("fullName"),
            }
            override = CITY_NAME_OVERRIDES.get(fid)
            if override:
                name = override["name"]
                short = override.get("shortName", name)
                full = override.get("fullName", name)
            else:
                name = p.get("name")
                short = p.get("shortName")
                full = p.get("fullName")
                if is_slugish(name, fid):
                    name = humanize_slug(fid)
                if is_slugish(short, fid):
                    short = name.split(",")[0].split("(")[0].strip() if name else humanize_slug(fid)
                if is_slugish(full, fid):
                    full = name
            if not name:
                name = humanize_slug(fid) if fid else "Unknown"
            if not short:
                short = name.split(",")[0].split("(")[0].strip()
            if not full:
                full = name
            p["name"] = name
            p["shortName"] = short
            p["fullName"] = full
            after = {
                "name": p.get("name"),
                "shortName": p.get("shortName"),
                "fullName": p.get("fullName"),
            }
            if before != after:
                changes.append(
                    {"kind": kind, "id": fid, "before": before, "after": after}
                )
    return changes


def main() -> int:
    clusters_doc = json.loads(CLUSTERS_PATH.read_text(encoding="utf-8"))
    fbt = json.loads(FBT_PATH.read_text(encoding="utf-8"))

    cluster_changes = fix_clusters(clusters_doc["clusters"])
    feature_changes = fix_feature_names(fbt)

    CLUSTERS_PATH.write_text(
        json.dumps(clusters_doc, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    # FEATURES_BY_TYPE is sealed compact (single-line) in-repo — do not pretty-print.
    FBT_PATH.write_text(
        json.dumps(fbt, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )

    receipt = {
        "at": utc_now(),
        "rule": "Display capitalization: human Title Case labels at every taxonomy tier; never raw slug / all-lowercase as user-visible name",
        "n_cluster_fixes": len(cluster_changes),
        "n_feature_fixes": len(feature_changes),
        "cluster_changes": cluster_changes,
        "feature_changes": feature_changes,
        "cluster_label_overrides": CLUSTER_LABEL_OVERRIDES,
        "city_name_overrides": {k: v["name"] for k, v in CITY_NAME_OVERRIDES.items()},
    }
    RECEIPT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT_PATH.write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": "OK",
                "n_cluster_fixes": len(cluster_changes),
                "n_feature_fixes": len(feature_changes),
                "receipt": str(RECEIPT_PATH.relative_to(ROOT)),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
