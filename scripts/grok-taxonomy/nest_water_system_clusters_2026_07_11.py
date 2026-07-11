#!/usr/bin/env python3
"""Nest raw water-system clusters under country parents (Region→Cluster→City→Locale).

Wave1 mint left several Europe water-system clusters as top-level nav chips with
slug labels (e.g. gulf-of-gdansk-tricity). This matches the UK/Germany pattern from
PR #231: parent_cluster_id + nav_hidden + human-readable label; country node holds
the nav display and union of member cities.

Also writes/extends the permanent gate:
  scripts/grok-taxonomy/validate_cluster_taxonomy.py
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CLUSTERS_PATH = ROOT / "data-clean/CLUSTERS.json"
FBT_PATH = ROOT / "data-clean/FEATURES_BY_TYPE.json"
RECEIPT_PATH = (
    ROOT
    / "handoff/backlog-clear-2026-07-11"
    / "TAXONOMY-NEST-WATER-SYSTEMS-RECEIPT-2026-07-11.json"
)

# Country parents that must exist as top-level nav clusters.
COUNTRY_SEED: dict[str, dict[str, Any]] = {
    "poland": {
        "cluster_label": "Poland",
        "label": "Poland",
        "region": "Europe",
        "type": "coastal",
    },
    "hungary": {
        "cluster_label": "Hungary",
        "label": "Hungary",
        "region": "Europe",
        "type": "inland",
    },
    "austria": {
        "cluster_label": "Austria",
        "label": "Austria",
        "region": "Europe",
        "type": "inland",
    },
}

# Water-system / raw-slug cluster → country parent + display label.
# Children get parent_cluster_id + nav_hidden=true (routing anchors, not top-level chips).
NEST: dict[str, dict[str, str]] = {
    # Poland
    "gulf-of-gdansk-tricity": {
        "parent": "poland",
        "label": "Gdańsk / Tricity",
    },
    "kolobrzeg-parseta-baltic": {"parent": "poland", "label": "Kołobrzeg"},
    "lake-jamno-mielno": {"parent": "poland", "label": "Jamno / Mielno"},
    "leba-baltic-port": {"parent": "poland", "label": "Łeba"},
    "rewal-baltic-resort": {"parent": "poland", "label": "Rewal"},
    "szczecin-lagoon-swina": {"parent": "poland", "label": "Szczecin Lagoon"},
    "ustka-slupia-baltic": {"parent": "poland", "label": "Ustka"},
    "vistula-lagoon": {"parent": "poland", "label": "Vistula Lagoon"},
    # Hungary
    "hungarian-danube": {"parent": "hungary", "label": "Budapest Danube"},
    "lake-balaton-hungary": {"parent": "hungary", "label": "Lake Balaton"},
    "gyor-mosoni-danube": {"parent": "hungary", "label": "Győr / Mosoni-Duna"},
    # Austria
    "woerthersee-austria": {"parent": "austria", "label": "Wörthersee"},
    "korneuburg-klosterneuburg-danube": {
        "parent": "austria",
        "label": "Korneuburg–Klosterneuburg",
    },
    "linz-upper-danube": {"parent": "austria", "label": "Linz Danube"},
    "klopeiner-see-austria": {"parent": "austria", "label": "Klopeiner See"},
    # France
    "seine-estuary-le-havre": {"parent": "france", "label": "Le Havre / Seine"},
    # Multi-country lake — majority Swiss members; AT cities also on austria
    "lake-constance": {"parent": "switzerland", "label": "Lake Constance"},
}

# Known top-level country / sovereign / multi-island market clusters (allowed without parent).
# Water-system slugs must NOT be in this set.
ALLOWED_TOP_LEVEL_PREFIXES = ()  # unused; full set in validate script


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> int:
    cl = json.loads(CLUSTERS_PATH.read_text())
    clusters: list[dict] = cl["clusters"]
    by = {c["cluster_id"]: c for c in clusters}
    now = utc_now()
    receipt: dict[str, Any] = {
        "at": now,
        "source": "grok/taxonomy-nest-water-systems-2026-07-11",
        "countries_created": [],
        "nested": [],
        "country_members_unioned": {},
        "labels_fixed": [],
        "austria_cross_members_from_constance": [],
    }

    # 1) Ensure country parents exist
    for cid, seed in COUNTRY_SEED.items():
        if cid not in by:
            row = {
                "cluster_id": cid,
                "cluster_label": seed["cluster_label"],
                "label": seed["label"],
                "region": seed["region"],
                "type": seed["type"],
                "member_city_ids": [],
                "parent_cluster_id": None,
                "nav_hidden": False,
                "_taxonomy_nest_at": now,
            }
            clusters.append(row)
            by[cid] = row
            receipt["countries_created"].append(cid)
        else:
            # ensure display labels
            c = by[cid]
            if not c.get("cluster_label") or c.get("cluster_label") == cid:
                c["cluster_label"] = seed["cluster_label"]
                c["label"] = seed["label"]
                receipt["labels_fixed"].append(
                    {"cluster_id": cid, "label": seed["cluster_label"]}
                )

    # France already exists — ensure label
    if "france" in by:
        fr = by["france"]
        if not fr.get("cluster_label") or fr.get("cluster_label") == "france":
            fr["cluster_label"] = "France"
            fr["label"] = "France"

    # 2) Nest water-system children
    for child_id, spec in NEST.items():
        parent_id = spec["parent"]
        label = spec["label"]
        if child_id not in by:
            # create empty routing anchor if missing
            row = {
                "cluster_id": child_id,
                "cluster_label": label,
                "label": label,
                "region": "Europe",
                "type": "water_system",
                "member_city_ids": [],
                "parent_cluster_id": parent_id,
                "nav_hidden": True,
                "_taxonomy_nest_at": now,
            }
            clusters.append(row)
            by[child_id] = row
            receipt["nested"].append(
                {"cluster_id": child_id, "parent": parent_id, "label": label, "created": True}
            )
            continue

        child = by[child_id]
        before = {
            "parent": child.get("parent_cluster_id"),
            "label": child.get("cluster_label") or child.get("label"),
            "nav_hidden": child.get("nav_hidden"),
        }
        child["parent_cluster_id"] = parent_id
        child["nav_hidden"] = True
        child["cluster_label"] = label
        child["label"] = label
        child["region"] = by[parent_id].get("region") or child.get("region") or "Europe"
        child["_taxonomy_nest_at"] = now
        receipt["nested"].append(
            {
                "cluster_id": child_id,
                "parent": parent_id,
                "label": label,
                "before": before,
                "members": list(child.get("member_city_ids") or []),
            }
        )

    # 3) Union child members onto country parents (UK pattern)
    for child_id, spec in NEST.items():
        parent = by[spec["parent"]]
        child = by[child_id]
        p_members = list(parent.get("member_city_ids") or [])
        added = []
        for mid in child.get("member_city_ids") or []:
            if mid not in p_members:
                p_members.append(mid)
                added.append(mid)
        parent["member_city_ids"] = p_members
        if added:
            receipt["country_members_unioned"].setdefault(spec["parent"], []).extend(added)

    # 4) Lake Constance AT cities also on austria
    if "lake-constance" in by and "austria" in by:
        at = by["austria"]
        at_members = list(at.get("member_city_ids") or [])
        for mid in by["lake-constance"].get("member_city_ids") or []:
            # Austrian-side ids
            if mid in ("bregenz", "hard-at", "bregenz-austria", "hard-austria") or mid.endswith(
                "-austria"
            ) or mid in ("bregenz", "hard-at"):
                if mid not in at_members:
                    at_members.append(mid)
                    receipt["austria_cross_members_from_constance"].append(mid)
        # also bregenz/hard without suffix
        for mid in ("bregenz", "hard-at"):
            if mid in (by["lake-constance"].get("member_city_ids") or []) and mid not in at_members:
                at_members.append(mid)
                receipt["austria_cross_members_from_constance"].append(mid)
        at["member_city_ids"] = at_members

    # 5) Recompute members_present
    fbt_ok = False
    try:
        fbt = json.loads(FBT_PATH.read_text())
        city_ids = {
            (f.get("properties") or f).get("id")
            for f in fbt.get("city", [])
            if (f.get("properties") or f).get("id")
        }
        fbt_ok = True
    except Exception:
        city_ids = set()

    for c in clusters:
        mem = c.get("member_city_ids") or []
        if fbt_ok:
            present = [m for m in mem if m in city_ids]
            missing = [m for m in mem if m not in city_ids]
            c["members_present"] = len(present)
            c["members_missing"] = missing
        # ensure country top-level not hidden
        if c["cluster_id"] in COUNTRY_SEED or c["cluster_id"] in (
            "france",
            "switzerland",
            "germany",
            "uk",
            "belgium",
        ):
            if c.get("nav_hidden") is True and c.get("parent_cluster_id") is None:
                c["nav_hidden"] = False

    cl["clusters"] = clusters
    cl["_taxonomy_water_system_nest_at"] = now
    cl["_taxonomy_water_system_nest_note"] = (
        "Water-system clusters nest under country via parent_cluster_id + nav_hidden; "
        "country cluster is the nav chip. Region→Cluster→City→Locale."
    )
    CLUSTERS_PATH.write_text(json.dumps(cl, indent=2, ensure_ascii=False) + "\n")

    # 6) Align city feature region to parent country cluster region (best-effort)
    if fbt_ok:
        # map city → country via membership
        city_country: dict[str, str] = {}
        for child_id, spec in NEST.items():
            for mid in by[child_id].get("member_city_ids") or []:
                city_country[mid] = spec["parent"]
        for cid, country in [
            (m, p)
            for p, ms in receipt["country_members_unioned"].items()
            for m in ms
        ]:
            city_country.setdefault(cid, country)

        region_by_country = {
            cid: by[cid].get("region", "Europe") for cid in set(city_country.values()) if cid in by
        }
        n_city = 0
        for f in fbt.get("city", []):
            p = f.get("properties") or f
            cid = p.get("id")
            if cid in city_country:
                parent = city_country[cid]
                p["region"] = region_by_country.get(parent, p.get("region") or "Europe")
                # country display name
                country_label = (by[parent].get("cluster_label") or parent).title()
                if parent == "uk":
                    country_label = "United Kingdom"
                p.setdefault("country", country_label)
                n_city += 1
        FBT_PATH.write_text(json.dumps(fbt, ensure_ascii=False, separators=(",", ":")) + "\n")
        receipt["cities_region_aligned"] = n_city

    RECEIPT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT_PATH.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({k: receipt[k] for k in receipt if k != "nested"}, indent=2))
    print("nested", len(receipt["nested"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
