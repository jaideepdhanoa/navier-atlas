#!/usr/bin/env python3
"""Permanent gate: Region → Cluster → City → Locale taxonomy hygiene.

Fails when water-system / raw-slug clusters appear as top-level nav chips
(no parent_cluster_id) or when cluster_label equals the raw cluster_id.

Rule (locked):
  - Country (or multi-island market) clusters are top-level under a Region.
  - Water-system / city-group routing anchors nest under a country via
    parent_cluster_id + nav_hidden=true and a human-readable cluster_label.
  - Never surface hyphenated water-system IDs as top-level browse chips.
  - City features belong to a cluster's member_city_ids; locales nest under cities.

Usage:
  python3 scripts/grok-taxonomy/validate_cluster_taxonomy.py
  python3 scripts/grok-taxonomy/validate_cluster_taxonomy.py --json out.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLUSTERS_PATH = ROOT / "data-clean/CLUSTERS.json"

# Sovereign / multi-island / primary market clusters allowed at top level (no parent).
# Keep in sync with product nav — water systems must NOT be listed here.
ALLOWED_TOP_LEVEL = {
    # Europe countries
    "uk",
    "germany",
    "france",
    "spain",
    "italy",
    "norway",
    "sweden",
    "finland",
    "denmark",
    "belgium",
    "switzerland",
    "netherlands",
    "greece",
    "croatia",
    "turkey",
    "romania",
    "malta",
    "monaco",
    "montenegro",
    "portugal",
    "ireland",
    "iceland",
    "poland",
    "hungary",
    "austria",
    "cyprus",
    "estonia",
    # Wider markets (not water-system slugs)
    "uae",
    "saudi-arabia",
    "israel",
    "egypt",
    "morocco",
    "tunisia",
    "algeria",
    "qatar",
    "bahrain",
    "kuwait",
    "oman",
    "lebanon",
    "india",
    "indonesia",
    "thailand",
    "malaysia",
    "singapore",
    "vietnam",
    "philippines",
    "japan",
    "korea",
    "south-korea",
    "china",
    "hong-kong",
    "hong-kong-macau",
    "macau",
    "taiwan",
    "australia",
    "new-zealand",
    "usa",
    "canada",
    "mexico",
    "brazil",
    "argentina",
    "chile",
    "colombia",
    "peru",
    "ecuador",
    "panama",
    "costa-rica",
    "maldives",
    "seychelles",
    "mauritius",
    "fiji",
    "french-polynesia",
    "hawaii-usa",
    "abc-islands",
    "st-maarten-st-barths",
    "st-lucia-grenadines",
    "antigua-barbuda",
    "bahamas",
    "barbados",
    "belize",
    "cayman-islands",
    "cuba",
    "dominican-republic",
    "jamaica",
    "puerto-rico",
    "turks-caicos",
    "usvi-bvi",
    "kenya",
    "tanzania",
    "mozambique",
    "south-africa",
    "senegal",
    "nigeria",
    "cote-divoire",
    "madagascar",
    "sri-lanka",
    "pakistan",
    "brunei",
    "cambodia",
    "azerbaijan-caspian",
    "kazakhstan-caspian",
    "uruguay",
    # North America multi-city markets (product chips, not water-system leftovers)
    "new-york-usa",
    "boston-new-england-usa",
    "florida-usa",
    "san-francisco-bay-usa",
    "southern-california-usa",
    "great-lakes-usa",
    "san-juan-islands-usa",
    "bar-harbor-mdi-maine-usa",
    "salish-sea",
    "gulf-islands-bc-canada",
    "halifax-atlantic-canada",
    "galapagos-ecuador",
    "shanghai-china",
}

# Hyphen tokens that strongly signal a water-system routing anchor (must have parent).
# Avoid bare "harbor/harbour" — legitimate NA market chips use those words.
WATER_TOKENS = re.compile(
    r"(danube|balaton|constance|geneva|z[uü]rich|gdansk|gda[nń]sk|tricity|"
    r"parseta|slupia|jamno|vistula|szczecin|swina|oder|rhine|seine|solent|"
    r"fjord|lagoon|(^|-)lake-|woerther|w[oö]rther|klopeiner|travem|warnow|limfjord|"
    r"baltic|estuary|waterway|-canal-|(^|-)canal$)",
    re.I,
)


def is_raw_label(cluster_id: str, label: str | None) -> bool:
    if not label:
        return True
    return label.strip().lower() == cluster_id.strip().lower()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", dest="json_out")
    args = ap.parse_args()

    clusters = json.loads(CLUSTERS_PATH.read_text())["clusters"]
    errors: list[dict] = []
    warnings: list[dict] = []

    for c in clusters:
        cid = c.get("cluster_id") or ""
        parent = c.get("parent_cluster_id")
        label = c.get("cluster_label") or c.get("label")
        nav_hidden = bool(c.get("nav_hidden"))

        if parent:
            # Child must be nav_hidden
            if not nav_hidden:
                errors.append(
                    {
                        "cluster_id": cid,
                        "error": "child_cluster_missing_nav_hidden",
                        "parent_cluster_id": parent,
                    }
                )
            # Child must have human label
            if is_raw_label(cid, label):
                errors.append(
                    {
                        "cluster_id": cid,
                        "error": "child_cluster_raw_slug_label",
                        "label": label,
                    }
                )
            # Parent must exist
            if not any(x.get("cluster_id") == parent for x in clusters):
                errors.append(
                    {
                        "cluster_id": cid,
                        "error": "parent_cluster_missing",
                        "parent_cluster_id": parent,
                    }
                )
            continue

        # Top-level
        if WATER_TOKENS.search(cid) and not parent:
            # Water-system slug at top level → always hard error
            errors.append(
                {
                    "cluster_id": cid,
                    "error": "top_level_water_system_or_raw_slug",
                    "label": label,
                    "hint": "Set parent_cluster_id to country + nav_hidden=true + human cluster_label",
                }
            )
            continue

        if cid not in ALLOWED_TOP_LEVEL:
            # Multi-hyphen slug with raw label (Wave1 leftover style) → hard error
            hyphen_n = cid.count("-")
            if hyphen_n >= 2 and is_raw_label(cid, label):
                errors.append(
                    {
                        "cluster_id": cid,
                        "error": "top_level_water_system_or_raw_slug",
                        "label": label,
                        "hint": "Set parent_cluster_id to country + nav_hidden=true + human cluster_label",
                    }
                )
            else:
                warnings.append(
                    {
                        "cluster_id": cid,
                        "warning": "top_level_not_in_allowlist",
                        "label": label,
                    }
                )
        else:
            # Multi-hyphen allowlisted chips still need a human label (not raw id).
            if cid.count("-") >= 2 and is_raw_label(cid, label):
                errors.append(
                    {
                        "cluster_id": cid,
                        "error": "country_cluster_missing_display_label",
                        "label": label,
                    }
                )

    report = {
        "status": "PASS" if not errors else "FAIL",
        "rule": "Region→Cluster→City→Locale; water-systems nest under country with nav_hidden",
        "errors": errors,
        "warnings": warnings,
        "n_clusters": len(clusters),
        "n_errors": len(errors),
        "n_warnings": len(warnings),
    }
    text = json.dumps(report, indent=2, ensure_ascii=False)
    if args.json_out:
        Path(args.json_out).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
