"""Coastal routing helpers for Bolt/Yango markets lane."""
from __future__ import annotations

import hashlib
import math
import re
import unicodedata
from pathlib import Path

R_EARTH_KM = 6371.0088
LAND_THRESH_KM = 0.05
NM_PER_KM = 1 / 1.852

# Bolt/Yango anchor cities targeted by routing lane
BOLT_YANGO_ANCHORS = frozenset(
    {
        "abidjan-cote-divoire",
        "aktau-kazakhstan",
        "al-wakrah-qatar",
        "baku-azerbaijan",
        "beirut-lebanon",
        "constanta-romania",
        "dakar-senegal",
        "dammam-khobar-ksa",
        "dublin-ireland",
        "helsinki-finland",
        "karachi-pakistan",
        "kuryk-kazakhstan",
        "larnaca-cyprus",
        "limassol-cyprus",
        "lisbon-tagus-portugal",
        "porto-douro-portugal",
        "maputo-mozambique",
        "tallinn-estonia",
        "tangier-morocco",
        "tel-aviv-israel",
        "tunis-tunisia",
    }
)

_LABEL_STOP = frozenset(
    {"the", "and", "of", "marina", "terminal", "pier", "port", "harbour", "harbor", "jetty", "city"}
)

# Finance corridor node chips → sealed city_id on the gold surface
NODE_CROSSWALK = {
    "dubai": "dubai-uae",
    "abu-dhabi": "abu-dhabi-uae",
    "sharjah": "sharjah-uae",
    "fujairah": "fujairah-uae",
    "ras-al-khaimah": "ras-al-khaimah-uae",
    "doha": "doha-qatar",
    "lisbon-tagus-portugal": "lisbon-tagus-portugal",
    "porto": "porto-douro-portugal",
    "algarve": "algarve-portugal",
}


def load_json(path: Path):
    import json

    return json.loads(path.read_text())


def save_json(path: Path, obj):
    import json

    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def save_routes(path: Path, features: list):
    import json

    path.write_text(json.dumps(features, separators=(",", ":")) + "\n")


def route_features(obj) -> list:
    return obj if isinstance(obj, list) else obj.get("features", [])


def route_id_of(feat: dict) -> str:
    p = feat.get("properties", feat)
    return p.get("id") or p.get("route_id") or ""


def mint_route_id(from_id: str, to_id: str, tag: str = "boltyango") -> str:
    seed = f"{tag}|{from_id}|{to_id}"
    return "rn-" + hashlib.md5(seed.encode()).hexdigest()[:12]


def _strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def norm_label(s: str | None) -> str:
    if not s:
        return ""
    s = _strip_accents(s.lower().strip())
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _tokens(s: str | None) -> set[str]:
    return {t for t in norm_label(s).split() if t and t not in _LABEL_STOP}


def labels_match(a: str | None, b: str | None) -> bool:
    na, nb = norm_label(a), norm_label(b)
    if not na or not nb:
        return False
    if na == nb or na in nb or nb in na:
        return True
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return False
    overlap = ta & tb
    need = min(2, min(len(ta), len(tb)))
    return len(overlap) >= max(1, need)


def hav_km(a: tuple[float, float], b: tuple[float, float]) -> float:
    lon1, lat1 = math.radians(a[0]), math.radians(a[1])
    lon2, lat2 = math.radians(b[0]), math.radians(b[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * R_EARTH_KM * math.asin(min(1.0, math.sqrt(h)))


def path_length_km(coords: list) -> float:
    total = 0.0
    for i in range(1, len(coords)):
        total += hav_km((coords[i - 1][0], coords[i - 1][1]), (coords[i][0], coords[i][1]))
    return total


def hav_nm(a: tuple[float, float], b: tuple[float, float]) -> float:
    return hav_km(a, b) * NM_PER_KM


def load_land_mask():
    try:
        from global_land_mask import globe

        return globe
    except Exception:
        return None


def is_water(lon: float, lat: float, mask) -> bool:
    if mask is None:
        return True
    try:
        return not bool(mask.is_land(lat, lon))
    except Exception:
        return True


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


def densify(a: tuple[float, float], b: tuple[float, float], n: int = 12) -> list[list[float]]:
    if n < 2:
        return [[a[0], a[1]], [b[0], b[1]]]
    out = []
    for i in range(n):
        t = i / (n - 1)
        out.append([a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t])
    return out


def push_seaward(
    mid: tuple[float, float],
    a: tuple[float, float],
    b: tuple[float, float],
    mask,
) -> tuple[float, float] | None:
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy) or 1.0
    px, py = -dy / length, dx / length
    for scale in (0.015, 0.03, 0.05, 0.08, 0.12, 0.18, 0.25):
        for sign in (-1, 1):
            lon = mid[0] + sign * px * scale
            lat = mid[1] + sign * py * scale
            if is_water(lon, lat, mask):
                return (lon, lat)
    return None


def coastal_waypoints(
    a: tuple[float, float],
    b: tuple[float, float],
    mask,
    *,
    n_mid: int | None = None,
    dist_nm: float | None = None,
) -> list[tuple[float, float]]:
    """Insert seaward midpoints so paths follow open water, not straight chords over land."""
    if dist_nm is None:
        dist_nm = hav_nm(a, b)
    if n_mid is None:
        if dist_nm >= 40:
            n_mid = 4
        elif dist_nm >= 15:
            n_mid = 3
        elif dist_nm >= 5:
            n_mid = 2
        else:
            n_mid = 1
    wps = []
    for i in range(1, n_mid + 1):
        t = i / (n_mid + 1)
        mid = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
        wp = push_seaward(mid, a, b, mask)
        if wp:
            wps.append(wp)
    return wps


def build_coastal_path(
    a: tuple[float, float],
    b: tuple[float, float],
    mask,
    manual_waypoints: list[tuple[float, float]] | None = None,
) -> list[list[float]]:
    pts = [a]
    if manual_waypoints:
        pts.extend(manual_waypoints)
    else:
        pts.extend(coastal_waypoints(a, b, mask))
    pts.append(b)
    coords: list[list[float]] = []
    for i in range(len(pts) - 1):
        seg = densify(pts[i], pts[i + 1], 14)
        coords.extend(seg if not coords else seg[1:])
    return coords


def build_bp_index(fbt: dict) -> dict[str, dict]:
    idx = {}
    for poi in fbt.get("poi", []):
        props = poi.get("properties", poi)
        pid = props.get("id")
        if not pid:
            continue
        coords = poi.get("geometry", {}).get("coordinates", [None, None])
        idx[pid] = {
            "coords": (coords[0], coords[1]),
            "parent_city_id": props.get("parent_city_id"),
            "name": props.get("name") or props.get("shortName") or pid,
        }
    return idx


def build_city_index(fbt: dict) -> dict[str, str]:
    out = {}
    for key in ("city", "priority_city"):
        for feat in fbt.get(key, []):
            props = feat.get("properties", feat)
            cid = props.get("id")
            if cid:
                out[cid] = props.get("shortName") or props.get("name") or cid
    return out


def city_display(cid: str | None, cities: dict[str, str]) -> str:
    if not cid:
        return "Unknown"
    return cities.get(cid, cid.replace("-", " ").title())


def platform_for(dist_nm: float) -> str:
    return "Quanta-LR" if dist_nm >= 70 else "Pioneer II"


def edge_class_for(from_city: str | None, to_city: str | None, dist_nm: float) -> str:
    if from_city and to_city and from_city != to_city:
        return "regional" if dist_nm >= 70 else "local"
    return "local"


def trip_scope_for(from_city: str | None, to_city: str | None) -> str:
    if from_city and to_city and from_city == to_city:
        return "intra_city"
    return "inter_city"


def _corridor_city_ids(city_id: str | None, from_label: str | None, to_label: str | None) -> list[str]:
    if not city_id:
        return []
    cities = [NODE_CROSSWALK.get(city_id, city_id)]
    blob = norm_label(f"{from_label or ''} {to_label or ''}")
    if city_id == "lisbon-tagus-portugal":
        if any(t in blob for t in ("porto", "ribeira", "gaia", "douro")):
            cities.append("porto-douro-portugal")
        if any(t in blob for t in ("faro", "portimao", "lagos", "algarve", "cascais")):
            cities.append("algarve-portugal")
    if city_id == "dubai" or cities[0] == "dubai-uae":
        if any(t in blob for t in ("abu dhabi", "abudhabi", "corniche")):
            cities.append("abu-dhabi-uae")
    return list(dict.fromkeys(cities))


def resolve_bp_by_label(
    city_id: str | None,
    label: str | None,
    bp_idx: dict,
    *,
    extra_cities: list[str] | None = None,
) -> str | None:
    if not label:
        return None
    search = list(dict.fromkeys((extra_cities or []) + ([city_id] if city_id else [])))
    best = None
    best_score = 0
    for pid, row in bp_idx.items():
        if search and row.get("parent_city_id") not in search:
            continue
        if labels_match(label, row.get("name")):
            score = len(_tokens(label) & _tokens(row.get("name")))
            if score > best_score:
                best_score = score
                best = pid
    if best:
        return best
    # Relaxed: single strong token overlap (e.g. "Cacilhas (Almada)" ↔ "Cacilhas Ferry Terminal")
    for pid, row in bp_idx.items():
        if search and row.get("parent_city_id") not in search:
            continue
        overlap = _tokens(label) & _tokens(row.get("name"))
        strong = [t for t in overlap if len(t) >= 4]
        if strong:
            score = len(strong)
            if score > best_score:
                best_score = score
                best = pid
    return best


def resolve_corridor_endpoints(
    corridor: dict,
    bp_idx: dict,
) -> tuple[str | None, str | None, str | None, str | None]:
    from_city = NODE_CROSSWALK.get(corridor.get("from_node_id"), corridor.get("from_node_id"))
    to_city = NODE_CROSSWALK.get(
        corridor.get("to_node_id") or corridor.get("from_node_id"),
        corridor.get("to_node_id") or corridor.get("from_node_id"),
    )
    eps = corridor.get("endpoint_boarding_points") or {}
    from_label = eps.get("from") or corridor.get("from")
    to_label = eps.get("to") or corridor.get("to")
    cities = _corridor_city_ids(from_city, from_label, to_label)

    from_bp = resolve_bp_by_label(from_city, from_label, bp_idx, extra_cities=cities)
    to_bp = resolve_bp_by_label(to_city, to_label, bp_idx, extra_cities=cities)

    if not from_bp and from_city == to_city:
        from_bp = resolve_bp_by_label(from_city, corridor.get("from"), bp_idx, extra_cities=cities)
    if not to_bp and from_city == to_city:
        to_bp = resolve_bp_by_label(to_city, corridor.get("to"), bp_idx, extra_cities=cities)

    return from_bp, to_bp, from_city, to_city


def make_route_feature(
    from_id: str,
    to_id: str,
    from_name: str,
    to_name: str,
    from_city: str | None,
    to_city: str | None,
    coords: list,
    cities: dict[str, str],
    *,
    source: str = "boltyango",
    land_km: float = 0.0,
) -> dict:
    dist_nm = path_length_km(coords) * NM_PER_KM
    rid = mint_route_id(from_id, to_id)
    fc = city_display(from_city, cities)
    tc = city_display(to_city, cities)
    label = f"{from_name} → {to_name}"
    if from_city and to_city and from_city != to_city:
        city_label = f"{fc} → {tc}"
    elif from_city:
        city_label = f"{fc}: {label}"
    else:
        city_label = label

    return {
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": coords},
        "properties": {
            "id": rid,
            "platform": platform_for(dist_nm),
            "distance_nm": round(dist_nm, 1),
            "edge_class": edge_class_for(from_city, to_city, dist_nm),
            "from": from_id,
            "to": to_id,
            "from_node": from_id,
            "to_node": to_id,
            "from_label": from_name,
            "to_label": to_name,
            "from_city": fc,
            "to_city": tc,
            "from_city_id": from_city,
            "to_city_id": to_city,
            "label": city_label,
            "trip_scope": trip_scope_for(from_city, to_city),
            "trip_purpose": trip_scope_for(from_city, to_city),
            "traffic_weight": 0.55,
            f"_{source}": True,
            "_land_km_interior": round(land_km, 4),
            "_coastal_geometry": True,
        },
    }