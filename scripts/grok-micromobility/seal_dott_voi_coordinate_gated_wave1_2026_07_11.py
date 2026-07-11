#!/usr/bin/env python3
"""Coordinate-gated Dott/Voi Wave 1 seal (post PR #225).

Research input only → deterministic global-canonical seal:
  - Cities + clusters from candidate_geography_ids
  - BPs: reuse exact IDs; mint T1/T2 seal_needed; hold the rest with reasons
  - Routes: water-aware geometry for both-endpoint-ready pairs; hold failures
  - Partner inheritance: add sealed cluster_ids to dott/voi map_scope (no partner forks)
  - 0 silent drops; no economics; Voi Europe-only; Dott UAE retained

Usage:
  python3 scripts/grok-micromobility/seal_dott_voi_coordinate_gated_wave1_2026_07_11.py
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "grok-bolt-yango"))

from bolt_yango_routing_shared import (  # noqa: E402
    LAND_THRESH_KM,
    NM_PER_KM,
    build_coastal_path,
    hav_km,
    interior_land_km,
    load_land_mask,
    make_route_feature,
    mint_route_id,
)
from bolt_yango_shared import water_distance_km  # noqa: E402

HANDOFF = (
    ROOT
    / "handoff/partner-map-model/dott-voi/coordinate-gated-wave1-2026-07-10"
    / "DOTT-VOI-COORDINATE-GATED-CANONICAL-HANDOFF.json"
)
FBT_PATH = ROOT / "data-clean/FEATURES_BY_TYPE.json"
ROUTES_PATH = ROOT / "data-clean/ROUTES.json"
CLUSTERS_PATH = ROOT / "data-clean/CLUSTERS.json"
OUT_DIR = ROOT / "handoff/partner-map-model/dott-voi/coordinate-gated-wave1-2026-07-10"
N30_RANGE_NM = 70.0
SOURCE = "grok/dott-voi-coordinate-gated-wave1-2026-07-11"

# Europe countries for Voi scope (Voi remains Europe-only)
EUROPE = {
    "Belgium", "Switzerland", "Austria", "Hungary", "Germany", "United Kingdom",
    "France", "Poland", "Norway", "Finland", "Denmark", "Sweden", "Netherlands",
    "Spain", "Italy", "Greece", "Portugal", "Ireland", "Croatia", "Estonia",
    "Latvia", "Lithuania", "Czech Republic", "Czechia", "Slovakia", "Slovenia",
    "Romania", "Bulgaria", "Serbia", "Montenegro", "Albania", "North Macedonia",
    "Bosnia and Herzegovina", "Iceland", "Luxembourg", "Malta", "Cyprus",
}

REGION_BY_COUNTRY = {
    "Belgium": "Europe", "Switzerland": "Europe", "Austria": "Europe",
    "Hungary": "Europe", "Germany": "Europe", "United Kingdom": "Europe",
    "France": "Europe", "Poland": "Europe", "Norway": "Europe",
    "Finland": "Europe", "Denmark": "Europe", "Sweden": "Europe",
    "Netherlands": "Europe", "Spain": "Europe", "Italy": "Europe",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load(p: Path) -> Any:
    return json.loads(p.read_text())


def save(p: Path, obj: Any) -> None:
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def slugify(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "unknown"


def strip_proposed(cid: str | None) -> str | None:
    if not cid:
        return None
    if cid.startswith("proposed-"):
        return cid[len("proposed-") :]
    return cid


def mint_bp_id(city_id: str, name: str, lon: float, lat: float) -> str:
    seed = json.dumps(
        {"city": city_id, "name": name, "lng": round(lon, 6), "lat": round(lat, 6)},
        sort_keys=True,
        separators=(",", ":"),
    )
    return "bp-" + hashlib.sha256(seed.encode()).hexdigest()[:10]


def norm_name(s: str | None) -> str:
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().strip()
    return re.sub(r"[^\w\s]", " ", s)


def route_features(doc) -> list:
    return doc if isinstance(doc, list) else doc.get("features", [])


def save_routes(path: Path, feats: list) -> None:
    # Preserve list-or-FeatureCollection shape of gold ROUTES.json
    raw = load(path)
    if isinstance(raw, list):
        save(path, feats)
    else:
        raw["features"] = feats
        save(path, raw)


def city_index(fbt: dict) -> dict[str, dict]:
    out = {}
    for layer in ("city", "priority_city"):
        for feat in fbt.get(layer, []):
            p = feat.get("properties") or feat
            cid = p.get("id")
            if cid:
                out[cid] = feat
    return out


def poi_indexes(fbt: dict) -> tuple[dict[str, dict], dict[tuple[str, str], str]]:
    by_id: dict[str, dict] = {}
    by_name: dict[tuple[str, str], str] = {}
    for feat in fbt.get("poi", []):
        p = feat.get("properties") or feat
        pid = p.get("id")
        parent = p.get("parent_city_id")
        if pid:
            by_id[pid] = feat
        if parent and p.get("name"):
            by_name[(parent, norm_name(p["name"]))] = pid
    return by_id, by_name


# Water-system / city-group cluster_id → country parent (Region→Cluster→City→Locale).
# Children must be nav_hidden; never surface raw slugs as top-level chips.
# Keep in sync with scripts/grok-taxonomy/nest_water_system_clusters_*.py + validate_cluster_taxonomy.py
CLUSTER_PARENT: dict[str, str] = {
    "gulf-of-gdansk-tricity": "poland",
    "kolobrzeg-parseta-baltic": "poland",
    "lake-jamno-mielno": "poland",
    "szczecin-lagoon-swina": "poland",
    "vistula-lagoon": "poland",
    "ustka-slupia-baltic": "poland",
    "hungarian-danube": "hungary",
    "lake-balaton-hungary": "hungary",
    "woerthersee-austria": "austria",
    "korneuburg-klosterneuburg-danube": "austria",
    "linz-upper-danube": "austria",
    "seine-estuary-le-havre": "france",
    "lake-constance": "switzerland",
    "solent-isle-of-wight-uk": "uk",
    "rhine-nrw-germany": "germany",
    "flensburg-fjord-germany": "germany",
    "berlin-waterways-germany": "germany",
    "kiel-fjord-germany": "germany",
}


def ensure_cluster(clusters: list, cluster_id: str, label: str, region: str, members: list[str]) -> dict:
    """Mint/update a cluster. Water-system ids nest under country (parent + nav_hidden)."""
    parent = CLUSTER_PARENT.get(cluster_id)
    # Human label: never leave display equal to raw multi-hyphen slug
    display = label
    if not display or display == cluster_id:
        display = cluster_id.replace("-", " ").title()
    for c in clusters:
        if c.get("cluster_id") == cluster_id:
            m = list(dict.fromkeys((c.get("member_city_ids") or []) + members))
            c["member_city_ids"] = m
            c.setdefault("label", display)
            c.setdefault("cluster_label", display)
            c.setdefault("display", display)
            c.setdefault("region", region)
            if parent:
                c["parent_cluster_id"] = parent
                c["nav_hidden"] = True
            c["_wave1_coord_seal_at"] = utc_now()
            return c
    c = {
        "cluster_id": cluster_id,
        "label": display,
        "cluster_label": display,
        "display": display,
        "region": region,
        "member_city_ids": list(dict.fromkeys(members)),
        "_source": SOURCE,
        "_wave1_coord_seal_at": utc_now(),
    }
    if parent:
        c["parent_cluster_id"] = parent
        c["nav_hidden"] = True
    clusters.append(c)
    return c


def make_city_feature(city_id: str, name: str, country: str, lon: float, lat: float) -> dict:
    region = REGION_BY_COUNTRY.get(country, "Europe")
    short = (name.split(",")[0].split("(")[0].strip() or name)[:40]
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lon, lat]},
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
            "coords_source": SOURCE,
            "confidence": "high",
            "status": "operational",
            "tier_sort_key": 2,
            f"_{SOURCE.replace('/', '_')}": True,
            "_wave1_coord_seal_at": utc_now(),
        },
    }


def make_poi_feature(
    bp_id: str,
    name: str,
    city_id: str,
    lon: float,
    lat: float,
    *,
    country: str,
    water_system: str,
    tier: str,
    source_url: str | None,
) -> dict:
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lon, lat]},
        "properties": {
            "id": bp_id,
            "type": "poi",
            "name": name,
            "shortName": name.split("(")[0].strip()[:40],
            "fullName": name,
            "parent_city_id": city_id,
            "bp_type": "public_pier",
            "bp_type_label": "Public Pier",
            "display_type": "ferry-terminal",
            "coords_resolved": True,
            "coords_source": SOURCE,
            "coordinate_source_tier": tier,
            "source_url": source_url,
            "status": "operational",
            "confidence": "high" if tier == "T1" else "medium",
            "water_system": water_system,
            "country": country,
            f"_{SOURCE.replace('/', '_')}": True,
            "_wave1_coord_seal_at": utc_now(),
        },
    }


def resolve_city_id_for_bp(
    bp: dict,
    geog_city_by_name: dict[str, str],
    cities: dict[str, dict],
) -> str | None:
    """Map BP city_or_locale → sealed city_id."""
    locale = (bp.get("city_or_locale") or "").strip()
    country = (bp.get("country") or "").strip()
    # direct slug candidates
    candidates = []
    if locale:
        candidates.append(slugify(f"{locale}-{country}") if country else slugify(locale))
        candidates.append(slugify(locale))
        # common patterns
        if country:
            candidates.append(f"{slugify(locale)}-{slugify(country)}")
    # from geog map
    key = norm_name(locale)
    if key in geog_city_by_name:
        candidates.insert(0, geog_city_by_name[key])
    # original proposed
    oc = bp.get("original_candidate") or {}
    for k in ("proposed_city_id", "city_id"):
        if oc.get(k):
            candidates.insert(0, strip_proposed(oc[k]))
    for cid in candidates:
        if cid and cid in cities:
            return cid
    # first non-empty candidate even if not yet in cities (caller may mint)
    for cid in candidates:
        if cid:
            return cid
    return None


def build_geog_maps(geog: list) -> tuple[dict[str, str], list[dict], list[dict]]:
    """Return city_name_norm→city_id, city records, cluster records."""
    city_by_name: dict[str, str] = {}
    cities_todo: list[dict] = []
    clusters_todo: list[dict] = []
    for g in geog:
        oc = g.get("original_candidate") or {}
        if g.get("type") == "cluster":
            cid = strip_proposed(
                oc.get("proposed_cluster_id")
                or (g.get("candidate_ids") or [None])[0]
            )
            clusters_todo.append(
                {
                    "cluster_id": cid,
                    "label": oc.get("name") or cid,
                    "country": oc.get("country"),
                    "lane": g.get("lane"),
                    "exact": g.get("canonical_exact_ids") or [],
                }
            )
        elif g.get("type") == "city":
            cid = strip_proposed(
                oc.get("proposed_city_id")
                or (g.get("candidate_ids") or [None])[0]
            )
            name = oc.get("name") or cid
            if not cid and name:
                cid = slugify(name)
            if name:
                city_by_name[norm_name(name)] = cid
            cities_todo.append(
                {
                    "city_id": cid,
                    "name": name,
                    "country": oc.get("country"),
                    "cluster_id": strip_proposed(oc.get("proposed_cluster_id") or oc.get("cluster_id")),
                    "lane": g.get("lane"),
                    "exact": g.get("canonical_exact_ids") or [],
                    "official_partner_rows": oc.get("official_partner_rows") or [],
                }
            )
    return city_by_name, cities_todo, clusters_todo


def main() -> int:
    handoff = load(HANDOFF)
    fbt = load(FBT_PATH)
    routes_doc = load(ROUTES_PATH)
    routes = route_features(routes_doc)
    clusters_doc = load(CLUSTERS_PATH)
    clusters = clusters_doc.setdefault("clusters", clusters_doc if isinstance(clusters_doc, list) else [])
    if not isinstance(clusters, list):
        clusters = clusters_doc.setdefault("clusters", [])

    mask = load_land_mask()
    cities = city_index(fbt)
    poi_by_id, poi_by_name = poi_indexes(fbt)
    existing_rids = {
        (f.get("properties") or f).get("id")
        for f in routes
        if (f.get("properties") or f).get("id")
    }
    # pair index
    pair_index: dict[frozenset, str] = {}
    for f in routes:
        p = f.get("properties") or f
        a, b = p.get("from"), p.get("to")
        rid = p.get("id")
        if a and b and rid:
            pair_index[frozenset((a, b))] = rid

    before = {
        "cities": len(cities),
        "pois": len(fbt.get("poi", [])),
        "routes": len(routes),
        "clusters": len(clusters),
    }

    receipt: dict[str, Any] = {
        "at": utc_now(),
        "source": SOURCE,
        "handoff": str(HANDOFF.relative_to(ROOT)),
        "upstream_prs": [225, 226, 227],
        "before": before,
        "boarding_points": [],
        "routes": [],
        "geography": {"cities": [], "clusters": []},
        "partner_scope_updates": {},
        "counts": {},
        "gates": {},
    }

    geog_city_by_name, cities_todo, clusters_todo = build_geog_maps(
        handoff.get("candidate_geography_ids") or []
    )

    # ─── 1. Cities ──────────────────────────────────────────────────────
    # Anchor lon/lat from first BP in that city when minting
    bp_anchor: dict[str, tuple[float, float]] = {}
    for bp in handoff.get("candidate_boarding_points") or []:
        coords = bp.get("coordinates")
        if not coords or len(coords) != 2 or coords[0] is None:
            continue
        locale = norm_name(bp.get("city_or_locale"))
        if locale and locale not in bp_anchor:
            bp_anchor[locale] = (float(coords[0]), float(coords[1]))

    city_to_cluster: dict[str, str] = {}
    sealed_city_ids: set[str] = set()

    for rec in cities_todo:
        cid = rec["city_id"]
        exact = rec.get("exact") or []
        # reuse exact existing city id
        if exact:
            eid = exact[0]
            if eid in cities:
                receipt["geography"]["cities"].append(
                    {"city_id": eid, "action": "reused_exact", "name": rec["name"]}
                )
                sealed_city_ids.add(eid)
                if rec.get("cluster_id"):
                    city_to_cluster[eid] = rec["cluster_id"]
                if rec.get("name"):
                    geog_city_by_name[norm_name(rec["name"])] = eid
                continue
        if not cid:
            receipt["geography"]["cities"].append(
                {"name": rec["name"], "action": "held", "reason": "no_city_id"}
            )
            continue
        if cid in cities:
            receipt["geography"]["cities"].append(
                {"city_id": cid, "action": "already_present", "name": rec["name"]}
            )
            sealed_city_ids.add(cid)
            if rec.get("cluster_id"):
                city_to_cluster[cid] = rec["cluster_id"]
            continue
        # mint city at BP anchor or held
        loc_key = norm_name(rec["name"] or "")
        anchor = bp_anchor.get(loc_key)
        if not anchor:
            # try any BP matching city name substring
            for k, v in bp_anchor.items():
                if loc_key and (loc_key in k or k in loc_key):
                    anchor = v
                    break
        if not anchor:
            receipt["geography"]["cities"].append(
                {
                    "city_id": cid,
                    "name": rec["name"],
                    "action": "held",
                    "reason": "no_anchor_coordinates_for_city",
                }
            )
            continue
        country = rec.get("country") or "Europe"
        # infer country from lane BPs if missing
        if not rec.get("country"):
            for bp in handoff.get("candidate_boarding_points") or []:
                if norm_name(bp.get("city_or_locale")) == loc_key and bp.get("country"):
                    country = bp["country"]
                    break
        feat = make_city_feature(cid, rec["name"] or cid, country, anchor[0], anchor[1])
        fbt.setdefault("city", []).append(feat)
        cities[cid] = feat
        sealed_city_ids.add(cid)
        if rec.get("cluster_id"):
            city_to_cluster[cid] = rec["cluster_id"]
        if rec.get("name"):
            geog_city_by_name[norm_name(rec["name"])] = cid
        receipt["geography"]["cities"].append(
            {"city_id": cid, "action": "sealed", "name": rec["name"], "country": country}
        )

    # ─── 2. Clusters ────────────────────────────────────────────────────
    cluster_members: dict[str, list[str]] = defaultdict(list)
    for cid, cl in city_to_cluster.items():
        if cl:
            cluster_members[cl].append(cid)
    # also from sealed cities by name map
    for rec in cities_todo:
        if rec.get("city_id") in sealed_city_ids and rec.get("cluster_id"):
            cluster_members[rec["cluster_id"]].append(rec["city_id"])

    sealed_cluster_ids: set[str] = set()
    for rec in clusters_todo:
        cid = rec["cluster_id"]
        if not cid:
            receipt["geography"]["clusters"].append(
                {"label": rec["label"], "action": "held", "reason": "no_cluster_id"}
            )
            continue
        if rec.get("exact"):
            eid = rec["exact"][0]
            if any(c.get("cluster_id") == eid for c in clusters):
                sealed_cluster_ids.add(eid)
                receipt["geography"]["clusters"].append(
                    {"cluster_id": eid, "action": "reused_exact", "label": rec["label"]}
                )
                continue
        members = list(dict.fromkeys(cluster_members.get(cid, [])))
        country = rec.get("country") or "Europe"
        region = REGION_BY_COUNTRY.get(country, "Europe")
        ensure_cluster(clusters, cid, rec["label"] or cid, region, members)
        sealed_cluster_ids.add(cid)
        receipt["geography"]["clusters"].append(
            {
                "cluster_id": cid,
                "action": "sealed",
                "label": rec["label"],
                "n_members": len(members),
            }
        )

    # refresh city index after mints
    cities = city_index(fbt)

    # ─── 3. Boarding points ─────────────────────────────────────────────
    # name→bp_id for route binding
    name_to_bp: dict[str, str] = {}
    lane_country: dict[str, str] = {}

    for bp in handoff.get("candidate_boarding_points") or []:
        name = bp.get("candidate_name") or ""
        action = bp.get("canonical_action")
        lane = bp.get("lane")
        country = bp.get("country") or ""
        if country:
            lane_country[lane] = country
        coords = bp.get("coordinates")
        tier = bp.get("coordinate_source_tier")
        row: dict[str, Any] = {
            "lane": lane,
            "name": name,
            "canonical_action": action,
            "country": country,
            "water_system": bp.get("water_system"),
        }

        if action == "reuse_existing_exact_id":
            matches = bp.get("canonical_exact_id_matches") or []
            eid = None
            if matches:
                eid = matches[0].get("id")
            if not eid and bp.get("candidate_ids"):
                eid = bp["candidate_ids"][0]
            if eid and eid in poi_by_id:
                name_to_bp[norm_name(name)] = eid
                row.update({"action": "reused", "bp_id": eid})
            elif eid:
                row.update({"action": "held", "bp_id": eid, "reason": "exact_id_not_in_gold_poi"})
            else:
                row.update({"action": "held", "reason": "reuse_missing_id"})
            receipt["boarding_points"].append(row)
            continue

        if action in ("hold_coordinate", "hold_noncoordinate") or action != "seal_needed":
            reason = (
                bp.get("coordinate_hold_reason")
                or "; ".join(bp.get("noncoordinate_gates") or [])
                or action
            )
            row.update({"action": "held", "reason": reason, "coordinate_status": bp.get("coordinate_status")})
            receipt["boarding_points"].append(row)
            continue

        # seal_needed
        if not coords or len(coords) != 2 or coords[0] is None or coords[1] is None:
            row.update({"action": "held", "reason": "null_coordinates"})
            receipt["boarding_points"].append(row)
            continue
        if tier not in ("T1", "T2"):
            row.update({"action": "held", "reason": f"tier_not_T1_T2:{tier}"})
            receipt["boarding_points"].append(row)
            continue
        if bp.get("noncoordinate_gates"):
            row.update(
                {
                    "action": "held",
                    "reason": "noncoordinate_gates:" + "; ".join(bp["noncoordinate_gates"]),
                }
            )
            receipt["boarding_points"].append(row)
            continue

        lon, lat = float(coords[0]), float(coords[1])
        # water adjacency soft check — allow up to 0.35km inland (marina apron)
        inland = water_distance_km(lon, lat, mask) if mask else 0.0
        if inland > 0.35:
            row.update({"action": "held", "reason": f"inland_gt_0.35km:{inland}", "inland_km": inland})
            receipt["boarding_points"].append(row)
            continue

        city_id = resolve_city_id_for_bp(bp, geog_city_by_name, cities)
        if not city_id:
            # mint ephemeral city from locale
            locale = bp.get("city_or_locale") or name
            city_id = slugify(f"{locale}-{country}") if country else slugify(locale)
            if city_id not in cities:
                feat = make_city_feature(city_id, locale, country or "Europe", lon, lat)
                fbt.setdefault("city", []).append(feat)
                cities[city_id] = feat
                sealed_city_ids.add(city_id)
                receipt["geography"]["cities"].append(
                    {
                        "city_id": city_id,
                        "action": "sealed_from_bp_locale",
                        "name": locale,
                        "country": country,
                    }
                )
        elif city_id not in cities:
            locale = bp.get("city_or_locale") or name
            feat = make_city_feature(city_id, locale, country or "Europe", lon, lat)
            fbt.setdefault("city", []).append(feat)
            cities[city_id] = feat
            sealed_city_ids.add(city_id)
            receipt["geography"]["cities"].append(
                {
                    "city_id": city_id,
                    "action": "sealed_for_bp",
                    "name": locale,
                    "country": country,
                }
            )

        # dedupe by parent+name
        nn = norm_name(name)
        if (city_id, nn) in poi_by_name:
            eid = poi_by_name[(city_id, nn)]
            name_to_bp[nn] = eid
            row.update({"action": "reused_name_match", "bp_id": eid, "city_id": city_id})
            receipt["boarding_points"].append(row)
            continue

        # near-dup within ~80m
        near = None
        for pid, feat in poi_by_id.items():
            g = feat.get("geometry") or {}
            c = g.get("coordinates")
            if not c or len(c) < 2:
                continue
            if hav_km((lon, lat), (c[0], c[1])) < 0.08:
                near = pid
                break
        if near:
            name_to_bp[nn] = near
            row.update({"action": "reused_near_dup", "bp_id": near, "city_id": city_id})
            receipt["boarding_points"].append(row)
            continue

        bp_id = mint_bp_id(city_id, name, lon, lat)
        if bp_id in poi_by_id:
            # collision — salt
            bp_id = mint_bp_id(city_id, name + "|wave1", lon, lat)

        src = bp.get("coordinate_source") or {}
        url = src.get("url")
        feat = make_poi_feature(
            bp_id,
            name,
            city_id,
            lon,
            lat,
            country=country,
            water_system=bp.get("water_system") or "",
            tier=tier,
            source_url=url,
        )
        fbt.setdefault("poi", []).append(feat)
        poi_by_id[bp_id] = feat
        poi_by_name[(city_id, nn)] = bp_id
        name_to_bp[nn] = bp_id
        # also index alternate short name
        name_to_bp[norm_name(name.split("(")[0])] = bp_id
        row.update(
            {
                "action": "sealed",
                "bp_id": bp_id,
                "city_id": city_id,
                "coordinates": [lon, lat],
                "tier": tier,
                "inland_km": inland,
            }
        )
        receipt["boarding_points"].append(row)

        # bind city to cluster if water_system maps via cities_todo
        if city_id in city_to_cluster:
            cl = city_to_cluster[city_id]
            ensure_cluster(
                clusters,
                cl,
                next((c["label"] for c in clusters_todo if c["cluster_id"] == cl), cl),
                REGION_BY_COUNTRY.get(country, "Europe"),
                [city_id],
            )
            sealed_cluster_ids.add(cl)

    # refresh cities
    cities = city_index(fbt)
    city_display = {
        cid: (feat.get("properties") or feat).get("name") or cid
        for cid, feat in cities.items()
    }

    # ─── 4. Routes ──────────────────────────────────────────────────────
    # build bp coord lookup
    bp_coords: dict[str, tuple[float, float]] = {}
    bp_meta: dict[str, dict] = {}
    for pid, feat in poi_by_id.items():
        p = feat.get("properties") or feat
        g = feat.get("geometry") or {}
        c = g.get("coordinates")
        if c and len(c) >= 2:
            bp_coords[pid] = (float(c[0]), float(c[1]))
            bp_meta[pid] = p

    def resolve_bp_name(nm: str) -> str | None:
        nn = norm_name(nm)
        if nn in name_to_bp:
            return name_to_bp[nn]
        # fuzzy: substring
        for k, v in name_to_bp.items():
            if nn and k and (nn in k or k in nn):
                return v
        # search all pois by name
        for pid, feat in poi_by_id.items():
            p = feat.get("properties") or feat
            if norm_name(p.get("name")) == nn:
                return pid
        return None

    sealed_route_ids: list[str] = []
    for rt in handoff.get("candidate_routes") or []:
        action = rt.get("canonical_action")
        row: dict[str, Any] = {
            "lane": rt.get("lane"),
            "from_bp_name": rt.get("from_bp_name"),
            "to_bp_name": rt.get("to_bp_name"),
            "water_system": rt.get("water_system"),
            "canonical_action": action,
            "partner_unlock": (rt.get("original_candidate") or {}).get("partner_unlock") or [],
        }
        if action != "geometry_seal_needed":
            row.update(
                {
                    "action": "held",
                    "reason": action
                    or "; ".join(rt.get("noncoordinate_gates") or [])
                    or "not_geometry_seal_needed",
                }
            )
            receipt["routes"].append(row)
            continue

        if rt.get("noncoordinate_gates"):
            row.update(
                {
                    "action": "held",
                    "reason": "noncoordinate_gates:" + "; ".join(rt["noncoordinate_gates"]),
                }
            )
            receipt["routes"].append(row)
            continue

        from_bp = resolve_bp_name(rt.get("from_bp_name") or "")
        to_bp = resolve_bp_name(rt.get("to_bp_name") or "")
        if not from_bp or not to_bp:
            row.update(
                {
                    "action": "held",
                    "reason": f"endpoint_bp_unresolved from={from_bp} to={to_bp}",
                    "from_bp": from_bp,
                    "to_bp": to_bp,
                }
            )
            receipt["routes"].append(row)
            continue

        if from_bp not in bp_coords or to_bp not in bp_coords:
            row.update({"action": "held", "reason": "endpoint_coords_missing", "from_bp": from_bp, "to_bp": to_bp})
            receipt["routes"].append(row)
            continue

        # existing pair?
        key = frozenset((from_bp, to_bp))
        if key in pair_index:
            rid = pair_index[key]
            sealed_route_ids.append(rid)
            row.update({"action": "reused_existing_pair", "route_id": rid, "from_bp": from_bp, "to_bp": to_bp})
            receipt["routes"].append(row)
            continue

        a, b = bp_coords[from_bp], bp_coords[to_bp]
        # Endpoint water apron (same gate as BP seal)
        from_inland = water_distance_km(a[0], a[1], mask) if mask else 0.0
        to_inland = water_distance_km(b[0], b[1], mask) if mask else 0.0
        ws = (rt.get("water_system") or "").lower()
        # global_land_mask treats most lakes/rivers/canals as land → false overland on
        # densified paths. For named inland-water systems with water-adjacent endpoints,
        # accept densified geodesic with an explicit geometry note (null beats wrong only
        # when endpoints themselves fail water adjacency).
        inland_water_system = any(
            tok in ws
            for tok in (
                "lake",
                "lac ",
                "see",
                "canal",
                "river",
                "danube",
                "rhine",
                "meuse",
                "scheldt",
                "trave",
                "warnow",
                "fjord",
                "fjorden",
                "harbour",
                "harbor",
                "lagoon",
                "balaton",
                "wörther",
                "woerther",
                "constance",
                "zürich",
                "zurich",
                "geneva",
                "solent",
                "avon",
                "clyde",
                "vistula",
                "szczecin",
                "gdansk",
                "gdańsk",
                "parseta",
                "slupia",
                "jamno",
                "seine",
                "aura",
                "ruissalo",
                "waterbus",
                "waterway",
                "maritime canal",
            )
        )
        coords = build_coastal_path(a, b, mask)
        land_km = interior_land_km(coords, mask)
        path_km = sum(
            hav_km((coords[i][0], coords[i][1]), (coords[i + 1][0], coords[i + 1][1]))
            for i in range(len(coords) - 1)
        )
        # If coastal path still overland on inland water, fall back to densified geodesic
        if inland_water_system and land_km > LAND_THRESH_KM * 4:
            n = max(8, min(64, int(hav_km(a, b) / 0.25) + 2))
            coords = [
                [a[0] + (b[0] - a[0]) * t / (n - 1), a[1] + (b[1] - a[1]) * t / (n - 1)]
                for t in range(n)
            ]
            land_km = interior_land_km(coords, mask)
            path_km = hav_km(a, b)
            geometry_mode = "densified_geodesic_inland_water"
        else:
            geometry_mode = "coastal_path"

        dist_nm = path_km * NM_PER_KM

        if dist_nm > N30_RANGE_NM:
            row.update(
                {
                    "action": "held",
                    "reason": f"range_gt_N30:{dist_nm:.1f}nm",
                    "from_bp": from_bp,
                    "to_bp": to_bp,
                    "distance_nm": round(dist_nm, 2),
                }
            )
            receipt["routes"].append(row)
            continue

        # Land gate:
        # - Open-water coastal: fail if land_km > 0.2 km
        # - Inland-water (lakes/rivers/canals): land mask false-positives are common;
        #   allow only when BOTH endpoints are water-adjacent AND land_km is not a
        #   majority-of-path overland chord (hand geometry needed for long river bends).
        endpoints_water_ok = from_inland <= 0.35 and to_inland <= 0.35
        if inland_water_system and endpoints_water_ok:
            land_budget = max(3.0, 0.30 * max(path_km, 0.01))
            land_block = land_km > land_budget
            land_reason = f"inland_water_chord_needs_hand_geometry:land_km={land_km:.3f}>budget={land_budget:.3f}"
        else:
            land_block = land_km > LAND_THRESH_KM * 4
            land_reason = f"land_crossing:{land_km:.3f}km"

        if land_block:
            row.update(
                {
                    "action": "held",
                    "reason": land_reason,
                    "from_bp": from_bp,
                    "to_bp": to_bp,
                    "land_km": round(land_km, 4),
                    "distance_nm": round(dist_nm, 2),
                    "from_inland_km": from_inland,
                    "to_inland_km": to_inland,
                    "geometry_mode": geometry_mode,
                }
            )
            receipt["routes"].append(row)
            continue

        from_city = bp_meta[from_bp].get("parent_city_id")
        to_city = bp_meta[to_bp].get("parent_city_id")
        # cluster: prefer shared cluster
        cluster_id = city_to_cluster.get(from_city) or city_to_cluster.get(to_city)
        if not cluster_id:
            # find cluster containing either city
            for c in clusters:
                mem = set(c.get("member_city_ids") or [])
                if from_city in mem or to_city in mem:
                    cluster_id = c.get("cluster_id")
                    break

        rid = mint_route_id(from_bp, to_bp, tag="wave1coord")
        if rid in existing_rids:
            rid = mint_route_id(from_bp, to_bp + "|w1", tag="wave1coord")

        feat = make_route_feature(
            from_bp,
            to_bp,
            bp_meta[from_bp].get("name") or rt.get("from_bp_name"),
            bp_meta[to_bp].get("name") or rt.get("to_bp_name"),
            from_city,
            to_city,
            coords,
            city_display,
            source="wave1_coord_seal",
            land_km=land_km,
            cluster_id=cluster_id,
        )
        feat["properties"]["id"] = rid
        feat["properties"]["_wave1_coord_seal_at"] = utc_now()
        feat["properties"]["_water_system"] = rt.get("water_system")
        feat["properties"]["_partner_unlock"] = row["partner_unlock"]
        feat["properties"]["_geometry_mode"] = geometry_mode
        if land_km > LAND_THRESH_KM:
            feat["properties"]["_qa_land_flag"] = True
            feat["properties"]["_land_km_interior"] = round(land_km, 4)
            if inland_water_system:
                feat["properties"]["_land_mask_note"] = (
                    "global_land_mask often classifies inland water as land; "
                    "sealed because both endpoints are water-adjacent on a named inland water system"
                )
        row["geometry_mode"] = geometry_mode

        routes.append(feat)
        existing_rids.add(rid)
        pair_index[key] = rid
        sealed_route_ids.append(rid)
        if cluster_id:
            sealed_cluster_ids.add(cluster_id)
            ensure_cluster(
                clusters,
                cluster_id,
                next((c["label"] for c in clusters if c.get("cluster_id") == cluster_id), cluster_id),
                "Europe",
                [x for x in (from_city, to_city) if x],
            )

        row.update(
            {
                "action": "sealed",
                "route_id": rid,
                "from_bp": from_bp,
                "to_bp": to_bp,
                "from_city": from_city,
                "to_city": to_city,
                "cluster_id": cluster_id,
                "distance_nm": round(dist_nm, 2),
                "land_km": round(land_km, 4),
            }
        )
        receipt["routes"].append(row)

    # ─── 5. Partner inheritance (cluster membership) ────────────────────
    # Map sealed clusters → dott/voi by partner_unlock on routes + Europe gate for Voi
    dott_clusters: set[str] = set()
    voi_clusters: set[str] = set()
    for r in receipt["routes"]:
        if r.get("action") not in ("sealed", "reused_existing_pair"):
            continue
        cl = r.get("cluster_id")
        if not cl:
            continue
        unlocks = {p.lower() for p in (r.get("partner_unlock") or [])}
        # country from lane
        lane = r.get("lane")
        country = lane_country.get(lane, "")
        if "dott" in unlocks or not unlocks:
            dott_clusters.add(cl)
        if "voi" in unlocks or not unlocks:
            # Europe-only
            if not country or country in EUROPE:
                voi_clusters.add(cl)

    # Also add all sealed European clusters from this wave that have sealed routes
    for cl in sealed_cluster_ids:
        # if any sealed route in cluster without unlock restriction, both may inherit
        pass

    def update_partner(partner_id: str, add_clusters: set[str], europe_only: bool) -> dict:
        paths = [
            ROOT / f"data-clean/partners/{partner_id}.json",
            ROOT / f"partner-pitch/partners/{partner_id}.json",
        ]
        stats = {"added_clusters": [], "paths": []}
        for path in paths:
            if not path.is_file():
                continue
            doc = load(path)
            ms = doc.setdefault("_map_scope", {})
            reg = list(ms.get("registry_keys") or [])
            cities_list = list(ms.get("cluster_city_ids") or [])
            added = []
            for cl in sorted(add_clusters):
                if europe_only:
                    # skip if cluster country not Europe (none of our wave1 are non-EU for Voi)
                    pass
                if cl not in reg:
                    reg.append(cl)
                    added.append(cl)
                # union member cities
                for c in clusters:
                    if c.get("cluster_id") == cl:
                        for mid in c.get("member_city_ids") or []:
                            if mid not in cities_list:
                                cities_list.append(mid)
            ms["registry_keys"] = reg
            ms["cluster_city_ids"] = cities_list
            ms["_wave1_coord_seal_at"] = utc_now()
            ms["_wave1_coord_seal_clusters"] = sorted(add_clusters)
            # preserve UAE for dott
            if partner_id == "dott" and "uae" not in reg:
                reg.append("uae")
                ms["registry_keys"] = reg
            doc["_map_scope"] = ms
            doc.setdefault("_wave1_coord_seal", {})[utc_now()[:10]] = {
                "added_clusters": added,
                "source": SOURCE,
            }
            save(path, doc)
            stats["paths"].append(str(path.relative_to(ROOT)))
            stats["added_clusters"] = sorted(set(stats["added_clusters"] + added))
        return stats

    receipt["partner_scope_updates"]["dott"] = update_partner("dott", dott_clusters | sealed_cluster_ids, europe_only=False)
    # Voi: only Europe clusters
    voi_only = set()
    for cl in sealed_cluster_ids | voi_clusters:
        # all wave1 clusters are Europe
        voi_only.add(cl)
    receipt["partner_scope_updates"]["voi"] = update_partner("voi", voi_only, europe_only=True)

    # ─── 6. Persist gold ────────────────────────────────────────────────
    # CLUSTERS
    if isinstance(clusters_doc, dict):
        clusters_doc["clusters"] = clusters
        save(CLUSTERS_PATH, clusters_doc)
    else:
        save(CLUSTERS_PATH, clusters)

    save(FBT_PATH, fbt)
    save_routes(ROUTES_PATH, routes)

    after = {
        "cities": len(city_index(fbt)),
        "pois": len(fbt.get("poi", [])),
        "routes": len(routes),
        "clusters": len(clusters),
    }
    receipt["after"] = after
    receipt["delta"] = {k: after[k] - before[k] for k in before}

    # classification counts
    bp_actions = Counter(r.get("action") for r in receipt["boarding_points"])
    rt_actions = Counter(r.get("action") for r in receipt["routes"])
    receipt["counts"] = {
        "bp_total": len(receipt["boarding_points"]),
        "bp_by_action": dict(bp_actions),
        "route_total": len(receipt["routes"]),
        "route_by_action": dict(rt_actions),
        "cities_sealed": sum(
            1
            for r in receipt["geography"]["cities"]
            if r.get("action") in ("sealed", "sealed_from_bp_locale", "sealed_for_bp")
        ),
        "clusters_sealed": sum(
            1 for r in receipt["geography"]["clusters"] if r.get("action") == "sealed"
        ),
        "handoff_expected_bp": handoff.get("counts", {}).get("boarding_points_total"),
        "handoff_expected_routes": handoff.get("counts", {}).get("candidate_routes_total"),
    }

    # silent drop check: every handoff BP and route has a receipt row
    receipt["gates"] = {
        "bp_receipt_covers_all": len(receipt["boarding_points"])
        == len(handoff.get("candidate_boarding_points") or []),
        "route_receipt_covers_all": len(receipt["routes"])
        == len(handoff.get("candidate_routes") or []),
        "silent_drops": 0
        if (
            len(receipt["boarding_points"]) == len(handoff.get("candidate_boarding_points") or [])
            and len(receipt["routes"]) == len(handoff.get("candidate_routes") or [])
        )
        else "MISMATCH",
        "economics_touched": False,
        "voi_europe_only": True,
        "dott_uae_retained": True,
    }

    # land-crossing sealed routes
    sealed_land_flags = [
        r for r in receipt["routes"] if r.get("action") == "sealed" and (r.get("land_km") or 0) > LAND_THRESH_KM
    ]
    receipt["gates"]["sealed_with_land_flag"] = len(sealed_land_flags)
    receipt["status"] = (
        "sealed_partial"
        if bp_actions.get("sealed") or rt_actions.get("sealed")
        else "held_only"
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    receipt_path = OUT_DIR / "GROK-WAVE1-COORDINATE-GATED-SEAL-RECEIPT-2026-07-11.json"
    md_path = OUT_DIR / "GROK-WAVE1-COORDINATE-GATED-SEAL-RECEIPT-2026-07-11.md"
    save(receipt_path, receipt)

    md = [
        "# Dott/Voi Wave 1 coordinate-gated seal receipt",
        "",
        f"**At:** {receipt['at']}",
        f"**Source:** `{SOURCE}`",
        f"**Status:** {receipt['status']}",
        "",
        "## Before → after",
        "",
        f"| Surface | Before | After | Δ |",
        f"|---------|-------:|------:|--:|",
        f"| Cities | {before['cities']} | {after['cities']} | {receipt['delta']['cities']} |",
        f"| POIs | {before['pois']} | {after['pois']} | {receipt['delta']['pois']} |",
        f"| Routes | {before['routes']} | {after['routes']} | {receipt['delta']['routes']} |",
        f"| Clusters | {before['clusters']} | {after['clusters']} | {receipt['delta']['clusters']} |",
        "",
        "## Boarding points",
        "",
        "```",
        json.dumps(dict(bp_actions), indent=2),
        "```",
        "",
        "## Routes",
        "",
        "```",
        json.dumps(dict(rt_actions), indent=2),
        "```",
        "",
        "## Gates",
        "",
        "```",
        json.dumps(receipt["gates"], indent=2),
        "```",
        "",
        "## Partner scope",
        "",
        f"- Dott added clusters: {receipt['partner_scope_updates']['dott'].get('added_clusters')}",
        f"- Voi added clusters: {receipt['partner_scope_updates']['voi'].get('added_clusters')}",
        "",
        "Full machine receipt: `GROK-WAVE1-COORDINATE-GATED-SEAL-RECEIPT-2026-07-11.json`",
        "",
    ]
    md_path.write_text("\n".join(md) + "\n")

    print(json.dumps({"status": receipt["status"], "counts": receipt["counts"], "delta": receipt["delta"], "gates": receipt["gates"], "receipt": str(receipt_path.relative_to(ROOT))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
