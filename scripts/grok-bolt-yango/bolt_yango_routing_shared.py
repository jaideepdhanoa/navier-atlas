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
    "palma-mallorca-spain": "mallorca-spain",
    "cairo": "cairo-egypt",
    "hurghada-egypt": "hurghada-el-gouna-egypt",
    "el-gouna-egypt": "hurghada-el-gouna-egypt",
    "hurghada-el-gouna-egypt": "hurghada-el-gouna-egypt",
    "sharm-el-sheikh-egypt": "sharm-el-sheikh-egypt",
    "redsea-egypt": "redsea-egypt",
    "bangkok": "bangkok-thailand",
    "phuket": "phuket-phang-nga-thailand",
    "jakarta": "jakarta-indonesia",
    "bali": "jakarta-indonesia",
    "singapore": "singapore",
    "red-sea-global": "red-sea-global-ksa",
    "ksa-commercial": "jeddah-ksa",
    "lagos": "lagos-nigeria",
    "mykonos-greece": "mykonos-greece",
    "paros-greece": "paros-greece",
    "naxos-greece": "naxos-greece",
    "santorini-greece": "santorini-greece",
    "rhodes-dodecanese-greece": "rhodes-dodecanese-greece",
    "athens-saronic-greece": "athens-saronic-greece",
    "bolt-greece": "mykonos-greece",
    "dubrovnik-croatia": "dubrovnik-croatia",
    "korcula-croatia": "korcula-croatia",
    "split-croatia": "split-croatia",
    "lake-como-italy": "lake-como-italy",
    "portofino-cinque-terre-italy": "portofino-cinque-terre-italy",
    "amalfi-coast-italy": "amalfi-coast-italy",
    "maputo-mozambique": "maputo-mozambique",
    "vilanculos-bazaruto-mozambique": "vilanculos-bazaruto-mozambique",
    "pemba-mozambique": "pemba-mozambique",
    "inhambane-mozambique": "inhambane-mozambique",
    "beira-mozambique": "beira-mozambique",
    "amaala-ksa": "amaala-ksa",
    "neom-ksa": "neom-ksa",
    "neom-sindalah-ksa": "neom-sindalah-ksa",
    "paphos-cyprus": "paphos-cyprus",
    "ayia-napa-cyprus": "ayia-napa-cyprus",
    "zadar-croatia": "zadar-croatia",
    "red-sea-global": "red-sea-global-ksa",
    "bodrum": "bodrum-turkey",
    "cesme-izmir": "cesme-izmir-turkey",
    "antalya": "antalya-turkey",
}

# Extra parent_city_id search pools when a finance node maps to one canonical city
CITY_SEARCH_ALIASES: dict[str, list[str]] = {
    "red-sea-global-ksa": ["red-sea-global-ksa", "the-red-sea-archipelago-ksa"],
    "jakarta-indonesia": ["jakarta-indonesia"],
    "bangkok-thailand": ["bangkok-thailand"],
    "singapore": ["singapore"],
    "lagos-nigeria": ["lagos-nigeria"],
    "mykonos-greece": ["mykonos-greece", "paros-greece", "naxos-greece", "santorini-greece"],
    "paros-greece": ["paros-greece", "mykonos-greece", "naxos-greece"],
    "naxos-greece": ["naxos-greece", "paros-greece", "mykonos-greece", "santorini-greece"],
    "santorini-greece": ["santorini-greece", "mykonos-greece", "naxos-greece"],
    "rhodes-dodecanese-greece": ["rhodes-dodecanese-greece", "bodrum-turkey"],
    "athens-saronic-greece": ["athens-saronic-greece"],
    "red-sea-global-ksa": ["red-sea-global-ksa", "amaala-ksa", "the-red-sea-archipelago-ksa"],
    "amaala-ksa": ["amaala-ksa", "red-sea-global-ksa"],
    "pemba-mozambique": ["pemba-mozambique"],
    "vilanculos-bazaruto-mozambique": ["vilanculos-bazaruto-mozambique"],
    "maputo-mozambique": ["maputo-mozambique"],
    "inhambane-mozambique": ["inhambane-mozambique"],
    "beira-mozambique": ["beira-mozambique"],
    "limassol-cyprus": ["limassol-cyprus", "larnaca-cyprus", "paphos-cyprus", "ayia-napa-cyprus"],
    "larnaca-cyprus": ["larnaca-cyprus", "limassol-cyprus", "ayia-napa-cyprus", "paphos-cyprus", "beirut-lebanon"],
    "beirut-lebanon": ["beirut-lebanon", "larnaca-cyprus"],
    "paphos-cyprus": ["paphos-cyprus", "limassol-cyprus", "larnaca-cyprus"],
    "ayia-napa-cyprus": ["ayia-napa-cyprus", "larnaca-cyprus", "limassol-cyprus", "protaras"],
    "zadar-croatia": ["zadar-croatia", "split-croatia"],
    "neom-sindalah-ksa": ["neom-sindalah-ksa"],
}

# Tasklet endpoint_boarding_points labels → token hints for relaxed BP match
LABEL_HINTS: dict[str, list[str]] = {
    "shura island yacht marina the red sea": ["shura island marina"],
    "st regis red sea resort jetty ummahat island": ["ummahat alshaykh resort jetty", "st regis"],
    "nujuma a ritz carlton reserve island jetty": ["nujuma", "ritz carlton reserve"],
    "marina ancol dermaga marina ancol ancol marina": ["marina batavia", "marina ancol", "dermaga"],
    "pulau bidadari resort island jetty": ["bidadari"],
    "pulau putri resort island jetty": ["putri harbour", "putri resort"],
    "sathorn central pier saphan taksin": ["sathorn central pier"],
    "phra arthit pier n13": ["phra arthit"],
    "epe epe ayetoro jetty": ["epe", "ayetoro"],
    "badagry jegba marina commando jetty": ["badagry", "jegba", "commando"],
    "mykonos new port tourlos": ["mykonos new port", "tourlos"],
    "paros parikia port": ["parikia port"],
    "naxos town port chora": ["naxos port", "chora"],
    "santorini athinios port": ["athinios port"],
    "porto de maputo catembe pier public ferry departs the catembe side pier in maputo": [
        "catembe ferry terminal",
        "catembe",
    ],
    "inhaca island jetty new 1 km mpdc jetty opened mar 2026 replacing the old 120 m jetty closed 2013": [
        "inhaca island jetty",
        "inhaca",
    ],
    "ilha dos portugueses portuguese island santa maria beach landing no permanent jetty structures": [
        "portuguese island",
        "santa maria",
    ],
    "vilankulo vilanculos beachfront boat departure town jetty": ["vilanculos port"],
    "bazaruto archipelago national park island landings bazaruto benguerra magaruque santa carolina": [
        "bazaruto island lodge pier",
        "bazaruto",
    ],
    "inhambane city ferry pier inhambane peninsula": ["inhambane ferry pier", "inhambane"],
    "maxixe town jetty reconstructed japan funded repair after cyclone damage": ["maxixe town jetty", "maxixe"],
    "porto da beira beira waterfront": ["porto da beira", "beira port"],
    "buzi town landing buzi river estuary": ["buzi estuary landing", "buzi"],
    "pemba pemba bay waterfront paquitequete or tandanhangue jetty by road": ["pemba mz port"],
    "ibo island jetty quirimbas archipelago quirimbas national park": ["ibo island quay", "ibo"],
    "the red sea": ["shura island marina"],
    "shura island hub": ["shura island marina"],
    "neom sindalah sindalah marina igy": ["sindalah island marina"],
    "magna oxagon coast": ["magna resort cluster jetty"],
    "magna resort cluster jetty neom north coast": ["magna resort cluster jetty"],
    "paphos harbour kato paphos paphos castle harbour the established sea cruise departure quay": [
        "paphos harbour",
    ],
    "jetty adjacent to paphos international airport pfo": ["paphos airport jetty"],
    "paphos harbour kato paphos coral bay peyia resort cluster": ["paphos harbour", "coral bay"],
    "ayia napa marina opened 2020 360 berths yachts to 110 m superyacht capable hosted 100m m y lana": [
        "ayia napa marina",
    ],
    "ayia napa marina": ["ayia napa marina"],
    "protaras fig tree bay pernera jetties no full marina tender jetty boarding": ["protaras jetty"],
    "protaras fig tree bay pernera jetty tender jetty boarding": ["protaras jetty"],
    "larnaca port jetty adjacent to larnaca international airport lca": ["larnaca airport jetty"],
    "zadar gazenica old port murter hramina biograd na moru harbour": [
        "murter hramina marina",
        "zadar gazenica port",
    ],
    "kornati np vela provarsa aci piskera island anchorages": ["kornati piskera anchorage"],
    "cilipi cavtat area jetty airport waterfront": ["dubrovnik airport cilipi jetty"],
    "dubrovnik airport cilipi waterfront jetty": ["dubrovnik airport cilipi jetty"],
    "port gruz main resort transfer ferry hub": ["gruz port", "port gruz"],
    "dubrovnik old port gruz cavtat transfer dependent": ["gruz port", "dubrovnik old port"],
    "cavtat town waterfront quay": ["cavtat croatia quay", "cavtat town waterfront"],
    "larnaca port cyprus": ["larnaca commercial port", "larnaca port"],
    "jounieh port lebanon also marketed to beirut": ["jounieh port", "jounieh bay"],
    "beirut port jounieh port cedar waves departs jounieh marketed beirut jounieh": ["jounieh port"],
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


def _label_variants(label: str | None) -> list[str]:
    if not label:
        return []
    out = [label]
    primary = re.split(r"\s+[—–-]\s+", label, maxsplit=1)[0].strip()
    if primary and primary != label:
        out.append(primary)
    hints = LABEL_HINTS.get(norm_label(label))
    if hints:
        out.extend(hints)
    return out


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


def resolve_node_to_city(node_id: str | None, bp_idx: dict) -> str | None:
    if not node_id:
        return None
    if node_id.startswith("bp-"):
        row = bp_idx.get(node_id)
        if row and row.get("parent_city_id"):
            return row["parent_city_id"]
    if node_id in NODE_CROSSWALK:
        return NODE_CROSSWALK[node_id]
    if "__" in node_id:
        base = node_id.split("__", 1)[0]
        return NODE_CROSSWALK.get(base, base)
    return NODE_CROSSWALK.get(node_id, node_id)


def city_search_ids(city_id: str | None) -> list[str]:
    if not city_id:
        return []
    return list(dict.fromkeys(CITY_SEARCH_ALIASES.get(city_id, [city_id])))


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
    if city_id in ("lisbon-tagus-portugal", "porto-douro-portugal"):
        if any(t in blob for t in ("porto", "ribeira", "gaia", "douro")):
            cities.append("porto-douro-portugal")
        if any(t in blob for t in ("faro", "portimao", "lagos", "algarve", "cascais", "olhao", "deserta", "benagil")):
            cities.append("algarve-portugal")
        if any(t in blob for t in ("lisbon", "sodre", "belem", "cacilhas", "cascais")):
            cities.append("lisbon-tagus-portugal")
    if city_id in ("palma-mallorca-spain", "mallorca-spain"):
        if any(t in blob for t in ("ibiza", "eivissa", "formentera", "savina")):
            cities.append("ibiza-spain")
        if any(t in blob for t in ("menorca", "mao", "maó")):
            cities.append("menorca-spain")
        if any(t in blob for t in ("palma", "mallorca", "soller", "menorca")):
            cities.append("mallorca-spain")
    if city_id == "ibiza-spain":
        cities.append("mallorca-spain")
    if city_id in ("helsinki-finland", "tallinn-estonia", "stockholm-sweden"):
        cities.extend(["helsinki-finland", "tallinn-estonia", "stockholm-sweden"])
    if city_id == "istanbul-turkey" or "turkey" in (city_id or ""):
        if any(t in blob for t in ("bodrum", "marmaris", "gulluk", "gumusluk", "turgutreis", "didim", "yalikavak", "kos")):
            cities.append("bodrum-turkey")
        if any(t in blob for t in ("fethiye", "gocek", "oludeniz", "datca", "rhodes")):
            cities.extend(["bodrum-turkey", "cesme-izmir-turkey"])
        if any(t in blob for t in ("antalya", "kemer", "side")):
            cities.append("antalya-turkey")
        if any(t in blob for t in ("cesme", "izmir", "karşıyaka", "karsiyaka", "chios", "samos", "kusadasi")):
            cities.append("cesme-izmir-turkey")
        if any(t in blob for t in ("kadikoy", "kabatas", "bostanci", "buyukada", "istanbul", "karakoy", "besiktas")):
            cities.append("istanbul-turkey")
    if city_id == "dubai" or cities[0] == "dubai-uae":
        if any(t in blob for t in ("abu dhabi", "abudhabi", "corniche")):
            cities.append("abu-dhabi-uae")
    if city_id in ("mykonos-greece", "paros-greece", "naxos-greece", "santorini-greece"):
        cities.extend(["mykonos-greece", "paros-greece", "naxos-greece", "santorini-greece"])
    if city_id in ("red-sea-global-ksa", "amaala-ksa"):
        cities.extend(["red-sea-global-ksa", "amaala-ksa", "the-red-sea-archipelago-ksa"])
    if city_id in ("maputo-mozambique", "vilanculos-bazaruto-mozambique", "pemba-mozambique"):
        cities.extend(
            ["maputo-mozambique", "vilanculos-bazaruto-mozambique", "pemba-mozambique", "inhambane-mozambique", "beira-mozambique"]
        )
    if city_id == "rhodes-dodecanese-greece":
        cities.append("bodrum-turkey")
    if city_id == "dubrovnik-croatia":
        cities.extend(["dubrovnik-croatia", "korcula-croatia", "split-croatia"])
        if any(t in blob for t in ("kotor", "montenegro")):
            cities.append("kotor-montenegro")
    if city_id in ("limassol-cyprus", "larnaca-cyprus", "paphos-cyprus", "ayia-napa-cyprus"):
        cities.extend(["limassol-cyprus", "larnaca-cyprus", "paphos-cyprus", "ayia-napa-cyprus"])
    if city_id == "zadar-croatia":
        cities.extend(["zadar-croatia", "split-croatia"])
    if city_id == "neom-sindalah-ksa":
        cities.append("neom-sindalah-ksa")
    if any(t in blob for t in ("jounieh", "larnaca", "lebanon", "cyprus", "cedar waves")):
        cities.extend(["larnaca-cyprus", "beirut-lebanon"])
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
    search: list[str] = []
    for cid in (extra_cities or []) + ([city_id] if city_id else []):
        search.extend(city_search_ids(cid))
    search = list(dict.fromkeys(search))
    best = None
    best_score = 0
    for variant in _label_variants(label):
        for pid, row in bp_idx.items():
            if search and row.get("parent_city_id") not in search:
                continue
            if labels_match(variant, row.get("name")):
                score = len(_tokens(variant) & _tokens(row.get("name")))
                if score > best_score:
                    best_score = score
                    best = pid
    if best:
        return best
    # Relaxed: single strong token overlap (e.g. "Cacilhas (Almada)" ↔ "Cacilhas Ferry Terminal")
    for variant in _label_variants(label):
        for pid, row in bp_idx.items():
            if search and row.get("parent_city_id") not in search:
                continue
            overlap = _tokens(variant) & _tokens(row.get("name"))
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
    from_city = resolve_node_to_city(corridor.get("from_node_id"), bp_idx)
    to_city = resolve_node_to_city(
        corridor.get("to_node_id") or corridor.get("from_node_id"),
        bp_idx,
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
    cluster_id: str | None = None,
    cluster_city_id: str | None = None,
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

    feat: dict = {
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
    if cluster_id:
        feat["properties"]["cluster_id"] = cluster_id
    if cluster_city_id:
        feat["properties"]["cluster_city_id"] = cluster_city_id
    elif from_city and to_city and from_city == to_city:
        feat["properties"]["cluster_city_id"] = from_city
    elif from_city:
        feat["properties"]["cluster_city_id"] = from_city
    return feat