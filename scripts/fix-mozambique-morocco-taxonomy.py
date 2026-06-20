#!/usr/bin/env python3
"""Normalize Mozambique + Morocco cluster/city taxonomy (LB-260 housekeeping)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DC = ROOT / "data-clean"


def load(p: Path):
    return json.loads(p.read_text())


def save(p: Path, obj):
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def patch_city(fbt: dict, city_id: str, **props):
    for tier in ("city", "priority_city"):
        for f in fbt.get(tier, []):
            p = f.get("properties") or {}
            if p.get("id") == city_id:
                p.update(props)
                return True
    return False


def add_city(fbt: dict, feature: dict):
    fbt.setdefault("city", []).append(feature)
    # keep stable sort by id
    fbt["city"].sort(key=lambda x: (x.get("properties") or {}).get("id", ""))


def main():
    clusters = load(DC / "CLUSTERS.json")
    fbt = load(DC / "FEATURES_BY_TYPE.json")

    # --- Mozambique: country label only; member cities are real city nodes ---
    for c in clusters["clusters"]:
        if c["cluster_id"] == "mozambique":
            c["cluster_label"] = "Mozambique"
            c["member_city_ids"] = [
                "maputo-mozambique",
                "vilanculos-bazaruto-mozambique",
                "pemba-mozambique",
            ]
            c["members_present"] = len(c["member_city_ids"])

    # --- Morocco: wire all marquee cities under the country cluster ---
    for c in clusters["clusters"]:
        if c["cluster_id"] == "morocco":
            c["member_city_ids"] = [
                "tangier-morocco",
                "casablanca-morocco",
                "al-hoceima-morocco",
                "agadir-essaouira-morocco",
            ]
            c["members_present"] = len(c["member_city_ids"])

    # --- City display names (city tier, not cluster tier) ---
    patch_city(
        fbt,
        "casablanca-morocco",
        name="Casablanca",
        shortName="Casablanca",
        fullName="Casablanca",
    )
    patch_city(
        fbt,
        "agadir-essaouira-morocco",
        name="Agadir",
        shortName="Agadir",
        fullName="Agadir",
    )

    existing_ids = {
        (f.get("properties") or {}).get("id")
        for tier in ("city", "priority_city")
        for f in fbt.get(tier, [])
    }

    if "vilanculos-bazaruto-mozambique" not in existing_ids:
        add_city(
            fbt,
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [35.31278, -21.99889]},
                "properties": {
                    "id": "vilanculos-bazaruto-mozambique",
                    "type": "city",
                    "name": "Vilanculos",
                    "shortName": "Vilanculos",
                    "fullName": "Vilanculos",
                    "country": "Mozambique",
                    "region": "Africa",
                    "platform_class": "dual-platform",
                    "coords_resolved": True,
                    "coords_source": "taxonomy_fix_2026-06-20",
                    "confidence": "high",
                    "status": "operational",
                    "tier_sort_key": 2,
                },
            },
        )

    if "pemba-mozambique" not in existing_ids:
        add_city(
            fbt,
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [40.51778, -12.97]},
                "properties": {
                    "id": "pemba-mozambique",
                    "type": "city",
                    "name": "Pemba",
                    "shortName": "Pemba",
                    "fullName": "Pemba",
                    "country": "Mozambique",
                    "region": "Africa",
                    "platform_class": "dual-platform",
                    "coords_resolved": True,
                    "coords_source": "taxonomy_fix_2026-06-20",
                    "confidence": "high",
                    "status": "operational",
                    "tier_sort_key": 2,
                },
            },
        )

    # Pemba MZ port belongs under Pemba city, not Vilanculos
    for tier in fbt:
        for f in fbt.get(tier, []):
            p = f.get("properties") or {}
            if p.get("id") == "bp-w6-fa25528cb6":
                p["parent_city_id"] = "pemba-mozambique"

    save(DC / "CLUSTERS.json", clusters)
    save(DC / "FEATURES_BY_TYPE.json", fbt)
    print("patched CLUSTERS.json + FEATURES_BY_TYPE.json")
    print("mozambique cluster_label → Mozambique")
    print("morocco members → tangier, casablanca, al-hoceima, agadir")
    print("city nodes added/renamed for vilanculos + pemba")


if __name__ == "__main__":
    main()