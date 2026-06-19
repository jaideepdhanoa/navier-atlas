"""Shared helpers for Grok Bucket B routing lane."""
from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HANDOFF = ROOT / "_ingest/grok-bucketB-handoff-2026-06-19/boarding-points"
TIER12 = (
    "lisbon-tagus-portugal",
    "abidjan-cote-divoire",
    "al-wakrah-qatar",
    "dammam-khobar-ksa",
)
TIER3_CROSSWALK = {
    "neom-ksa": "neom-sindalah-ksa",
    "amaala-ksa": "red-sea-global-ksa",
}

CITY_META = {
    "lisbon-tagus-portugal": {
        "name": "Lisbon (Tagus Estuary)",
        "shortName": "Lisbon",
        "country": "Portugal",
        "region": "Europe",
    },
    "abidjan-cote-divoire": {
        "name": "Abidjan (Ébrié Lagoon)",
        "shortName": "Abidjan",
        "country": "Côte d'Ivoire",
        "region": "Africa",
    },
    "al-wakrah-qatar": {
        "name": "Al Wakrah (Qatar)",
        "shortName": "Al Wakrah",
        "country": "Qatar",
        "region": "MENA",
    },
    "dammam-khobar-ksa": {
        "name": "Dammam–Khobar (Eastern Province)",
        "shortName": "Dammam–Khobar",
        "country": "Saudi Arabia",
        "region": "MENA",
    },
}

R_EARTH_KM = 6371.0088
LAND_THRESH_KM = 0.05


def load_json(path: Path):
    return json.loads(path.read_text())


def save_json(path: Path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def save_routes(path: Path, features: list):
    path.write_text(json.dumps(features, separators=(",", ":")) + "\n")


def route_features(obj) -> list:
    return obj if isinstance(obj, list) else obj.get("features", [])


def route_id_of(feat: dict) -> str:
    p = feat.get("properties", feat)
    return p.get("id") or p.get("route_id") or ""


def mint_route_id(from_id: str, to_id: str, tag: str = "bucketb") -> str:
    seed = f"{tag}|{from_id}|{to_id}"
    return "rn-" + hashlib.md5(seed.encode()).hexdigest()[:12]


def hav_km(a: tuple[float, float], b: tuple[float, float]) -> float:
    lon1, lat1 = math.radians(a[0]), math.radians(a[1])
    lon2, lat2 = math.radians(b[0]), math.radians(b[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * R_EARTH_KM * math.asin(min(1.0, math.sqrt(h)))


def hav_nm(a: tuple[float, float], b: tuple[float, float]) -> float:
    return hav_km(a, b) / 1.852


def densify(a: tuple[float, float], b: tuple[float, float], n: int = 10) -> list[list[float]]:
    if n < 2:
        return [[a[0], a[1]], [b[0], b[1]]]
    out = []
    for i in range(n):
        t = i / (n - 1)
        out.append([a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t])
    return out


def load_land_mask():
    try:
        from global_land_mask import globe

        return globe
    except Exception:
        return None


def interior_land_km(coords: list, mask, step_km: float = 0.05, apron_km: float = 0.08) -> float:
    if mask is None or len(coords) < 2:
        return 0.0
    cum = 0.0
    segs = []
    for i in range(1, len(coords)):
        a = (coords[i - 1][0], coords[i - 1][1])
        b = (coords[i][0], coords[i][1])
        seg_km = hav_km(a, b)
        if seg_km <= 0:
            continue
        n = max(1, int(seg_km / step_km))
        for k in range(1, n + 1):
            t = k / n
            lon = a[0] + (b[0] - a[0]) * t
            lat = a[1] + (b[1] - a[1]) * t
            segs.append((lon, lat, cum + seg_km * t, seg_km / n))
        cum += seg_km
    total = cum
    bad = 0.0
    for lon, lat, c, d in segs:
        if c < apron_km or c > total - apron_km:
            continue
        try:
            if mask.is_land(lat, lon):
                bad += d
        except Exception:
            pass
    return bad


def build_bp_index(fbt: dict) -> dict[str, dict]:
    idx = {}
    for poi in fbt.get("poi", []):
        props = poi.get("properties", poi)
        pid = props.get("id")
        if not pid:
            continue
        coords = poi.get("geometry", {}).get("coordinates", [None, None])
        idx[pid] = {
            "props": props,
            "coords": (coords[0], coords[1]),
            "parent_city_id": props.get("parent_city_id"),
            "name": props.get("name") or pid,
        }
    return idx


def build_city_index(fbt: dict) -> dict[str, str]:
    out = {}
    for key in ("city", "priority_city"):
        for feat in fbt.get(key, []):
            props = feat.get("properties", feat)
            cid = props.get("id")
            if cid:
                out[cid] = props.get("name") or props.get("shortName") or cid
    return out


def city_display(cid: str | None, cities: dict[str, str]) -> str:
    if not cid:
        return "Unknown"
    return cities.get(cid, cid.replace("-", " ").title())


def platform_for(dist_nm: float) -> str:
    return "Quanta-LR" if dist_nm >= 70 else "Pioneer II"


def edge_class_for(from_city: str | None, to_city: str | None, dist_nm: float) -> str:
    if from_city and to_city and from_city == to_city:
        return "local"
    if dist_nm >= 70:
        return "regional"
    return "local"


def trip_scope_for(from_city: str | None, to_city: str | None) -> str:
    if from_city and to_city and from_city == to_city:
        return "intra_city"
    return "inter_city"