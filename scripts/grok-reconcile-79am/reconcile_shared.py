"""Shared helpers for Grok #79am reconcile + Palm/Marina bbox cleanup."""
from __future__ import annotations

import json
import math
import re
import unicodedata
from pathlib import Path

PALM_MARINA_BBOX = (55.09, 25.04, 55.19, 25.14)  # lon_min, lat_min, lon_max, lat_max
WATER_THRESHOLD_KM = 0.15
LAND_THRESHOLD_KM = 0.05

JUNK_NAME = re.compile(
    r"\b(gym|fitness|restaurant|bar\b|hotel|mall|clinic|church|school|residence|"
    r"apartment|coffee|spa|salon|shop|store|market|hostel|charter|cargo|container|"
    r"ihg|resort|view\s*point|viewpoint|dhow\s+cruise|rent\s+a\s+yacht|yacht\s+rental|"
    r"beach\b|barry'?s|aloe\s+bar|dockmaster|residences)\b",
    re.I,
)
TERMINAL_STRONG = re.compile(
    r"\b(ferry\s+station|ferry\s+terminal|water\s+bus|marine\s+transport\s+station|"
    r"cruise\s+terminal|dmyc|international\s+marine\s+club|water\s+taxi|rta)\b",
    re.I,
)
TERMINAL_JETTY = re.compile(r"\b(jetty|pier|wharf)\b", re.I)
TERMINAL_HARBOUR = re.compile(
    r"\b(dubai\s+harbour\s*[-–]\s*(bay\s+marina|cruise\s+terminal|yacht\s+club)|"
    r"bluewaters\s+ferry|bluewaters\s+marina)\b",
    re.I,
)

R_EARTH_KM = 6371.0088


def load_json(path: Path):
    return json.loads(path.read_text())


def save_json(path: Path, obj):
    path.write_text(json.dumps(obj, indent=2) + "\n")


def save_routes(path: Path, features: list):
    path.write_text(json.dumps(features, separators=(",", ":")) + "\n")


def route_features(obj) -> list:
    return obj if isinstance(obj, list) else obj.get("features", [])


def route_id_of(feat: dict) -> str:
    p = feat.get("properties", feat)
    return p.get("id") or p.get("route_id") or ""


def in_bbox(lon: float, lat: float, bbox=PALM_MARINA_BBOX) -> bool:
    w, s, e, n = bbox
    return w <= lon <= e and s <= lat <= n


def _slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode("ascii")
    s = s.lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


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


def water_distance_km(lon: float, lat: float, mask, step_km: float = 0.05, max_km: float = 0.35) -> float:
    if is_water(lon, lat, mask):
        return 0.0
    best = max_km
    for deg in range(0, 360, 45):
        br = math.radians(deg)
        d = step_km
        while d <= max_km:
            dlat = (d / R_EARTH_KM) * math.cos(br) * (180 / math.pi)
            dlon = (
                (d / R_EARTH_KM)
                * math.sin(br)
                / max(math.cos(math.radians(lat)), 1e-6)
                * (180 / math.pi)
            )
            if is_water(lon + dlon, lat + dlat, mask):
                best = min(best, d)
                break
            d += step_km
    return round(best, 4)


def build_crosswalk_index(crosswalk: dict) -> dict[str, str]:
    """bp_id -> crosswalk source key (first match)."""
    out: dict[str, str] = {}
    for key, vals in crosswalk.get("crosswalk", {}).items():
        for bp_id in vals:
            out.setdefault(bp_id, key)
    return out


def build_bp_indexes(features_by_type: dict) -> tuple[dict, dict]:
    """Return (bp_by_id props+coords, city__berth resolver)."""
    bp_by_id: dict[str, dict] = {}
    berth_index: dict[str, list[str]] = {}
    for poi in features_by_type.get("poi", []):
        props = poi.get("properties", poi)
        pid = props.get("id")
        if not pid:
            continue
        coords = poi.get("geometry", {}).get("coordinates", [None, None])
        bp_by_id[pid] = {"props": props, "coords": coords}
        city = props.get("parent_city_id") or ""
        for slug_src in (props.get("name"), props.get("shortName"), props.get("linked_locale")):
            if not slug_src:
                continue
            key = f"{city}__{_slug(slug_src)}"
            berth_index.setdefault(key, []).append(pid)
            berth_index.setdefault(f"*__{_slug(slug_src)}", []).append(pid)
    return bp_by_id, berth_index


def bp_visible(props: dict) -> bool:
    return not props.get("_quarantine") and props.get("relevance") != "hide"


def gazetteer_promote(
    bp_id: str,
    name: str,
    crosswalk_keys: dict[str, str],
    verdict: str | None = None,
) -> tuple[bool, str | None]:
    """Return (promote, source_id)."""
    if JUNK_NAME.search(name or ""):
        return False, None
    cw = crosswalk_keys.get(bp_id)
    if cw and (TERMINAL_STRONG.search(name or "") or TERMINAL_HARBOUR.search(name or "") or TERMINAL_JETTY.search(name or "")):
        return True, cw
    if TERMINAL_STRONG.search(name or "") or TERMINAL_HARBOUR.search(name or ""):
        return True, f"terminal_name:{_slug(name)[:48]}"
    if TERMINAL_JETTY.search(name or "") and verdict == "KEEP":
        return True, f"jetty_keep:{_slug(name)[:48]}"
    if verdict == "KEEP" and re.search(r"\b(marina|harbour|port)\b", name or "", re.I):
        return False, None
    return False, None


def resolve_endpoint(
    ep: str,
    bp_by_id: dict,
    berth_index: dict,
    city_ids: set[str],
) -> tuple[str | None, str]:
    """Resolve endpoint to bp_id (or city id). Returns (resolved_id, scheme)."""
    if not ep:
        return None, "empty"
    if ep.startswith("bp-"):
        return ep, "bp"
    if "__" in ep:
        if ep in berth_index:
            return berth_index[ep][0], "city__berth"
        city, slug = ep.split("__", 1)
        key = f"{city}__{slug}"
        if key in berth_index:
            return berth_index[key][0], "city__berth"
        wild = f"*__{slug}"
        if wild in berth_index:
            return berth_index[wild][0], "city__berth"
        return None, "city__berth_unresolved"
    if ep in city_ids:
        return ep, "bare_city"
    if ep in bp_by_id:
        return ep, "bare_bp"
    return None, "unresolved"


def endpoint_blocked(
    ep: str,
    bp_by_id: dict,
    berth_index: dict,
    city_ids: set[str],
) -> tuple[bool, str]:
    """True when endpoint resolves to a quarantined/missing BP (global cascade)."""
    if not ep:
        return True, "empty"
    if ep in city_ids:
        return False, "bare_city"
    resolved, scheme = resolve_endpoint(ep, bp_by_id, berth_index, city_ids)
    if scheme == "bare_city" and resolved:
        return False, scheme
    if not resolved:
        if ep.startswith("bp-") or "__" in ep:
            return True, scheme
        return False, "bare_unknown"
    props = bp_by_id.get(resolved, {}).get("props", {})
    if not bp_visible(props):
        return True, f"{scheme}_quarantined"
    return False, scheme


def endpoint_survives(
    ep: str,
    bp_by_id: dict,
    berth_index: dict,
    city_ids: set[str],
) -> tuple[bool, str]:
    """Palm bbox strict gate — surviving BP must carry gazetteer promotion."""
    blocked, scheme = endpoint_blocked(ep, bp_by_id, berth_index, city_ids)
    if blocked:
        return False, scheme
    if not ep or ep in city_ids:
        return True, scheme
    resolved, _ = resolve_endpoint(ep, bp_by_id, berth_index, city_ids)
    if not resolved:
        return True, scheme
    props = bp_by_id.get(resolved, {}).get("props", {})
    if not props.get("_gazetteer_source") and not props.get("_gate4_promoted"):
        return False, "no_gazetteer"
    return True, scheme


def route_touches_bbox(feat: dict, bp_by_id: dict, bbox=PALM_MARINA_BBOX) -> bool:
    props = feat.get("properties", feat)
    for ep in (props.get("from"), props.get("to")):
        if ep and ep.startswith("bp-") and ep in bp_by_id:
            lon, lat = bp_by_id[ep]["coords"][:2]
            if lon is not None and in_bbox(lon, lat, bbox):
                return True
    coords = feat.get("geometry", {}).get("coordinates") or []
    for lon, lat in (coords[0], coords[-1]) if coords else []:
        if in_bbox(lon, lat, bbox):
            return True
    for lon, lat in coords[:: max(1, len(coords) // 8)]:
        if in_bbox(lon, lat, bbox):
            return True
    return False


def load_qa_module(work: Path):
    import sys

    for candidate in (
        work / "partner-pitch" / "_tools",
        Path(__file__).resolve().parents[2] / "_ingest/grok-phase3-ci-pilot-2026-06-18/partner-pitch/_tools",
    ):
        qa_path = candidate / "qa_land_crossing.py"
        if qa_path.exists():
            sys.path.insert(0, str(candidate))
            import qa_land_crossing  # noqa: WPS433

            return qa_land_crossing
    raise RuntimeError("qa_land_crossing.py not found")


def overlay_path(work: Path) -> Path:
    for p in (
        work / "partner-pitch" / "_tools" / "uae_gulf_land.wkb",
        work / "grok-routing-output" / "uae_gulf_land_v2.wkb",
        Path(__file__).resolve().parents[2] / "grok-routing-output/uae_gulf_land_v2.wkb",
    ):
        if p.exists():
            return p
    raise RuntimeError("UAE land overlay WKB not found")