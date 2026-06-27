"""Shared helpers for Grok Bolt/Yango seal lane."""
from __future__ import annotations

import hashlib
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INGEST = ROOT / "_ingest/bolt-yango-seal-2026-06-19/bolt-yango-seal-2026-06-19"
AGG_DIR = ROOT / "_ingest/gold-delta-LB230-LB241/agg"

CITY_CROSSWALK = {
    "dubai": "dubai-uae",
    "abu-dhabi": "abu-dhabi-uae",
    "sharjah": "sharjah-uae",
    "doha": "doha-qatar",
    "neom-ksa": "neom-sindalah-ksa",
    "amaala-ksa": "red-sea-global-ksa",
    "antalya": "antalya-turkey",
    "bodrum": "bodrum-turkey",
    "cesme-izmir": "cesme-izmir-turkey",
    "bali": "bali-indonesia",
    "bangkok": "bangkok-thailand",
    "jakarta": "jakarta-indonesia",
    "el-gouna-egypt": "hurghada-el-gouna-egypt",
    "hurghada-egypt": "hurghada-el-gouna-egypt",
    "desaru-coast": "desaru-coast-malaysia",
    "hong-kong": "hong-kong-hk",
    "palma-mallorca-spain": "mallorca-spain",
    "lagos": "lagos-nigeria",
    "cote-divoire": "abidjan-cote-divoire",
    "manama": "manama-bahrain",
    "fujairah": "fujairah-uae",
    "ras-al-khaimah": "ras-al-khaimah-uae",
    "red-sea-global": "red-sea-global-ksa",
    "ksa-commercial": "jeddah-ksa",
    "phuket": "phuket-phang-nga-thailand",
    "penang": "penang-malaysia",
    "langkawi": "langkawi-malaysia",
    "singapore": "singapore-singapore",
    "koh-samui": "koh-samui-thailand",
    "istanbul": "istanbul-turkey",
}

# RSG alignment — do not mint duplicate low-confidence handoff POIs (NODE-ID-CROSSWALK).
RSG_HOLD_CITIES = {"neom-ksa", "amaala-ksa", "neom-sindalah-ksa", "red-sea-global-ksa"}

R_EARTH_KM = 6371.0088

COUNTRY_SUFFIX = {
    "uae": ("United Arab Emirates", "MENA"),
    "qatar": ("Qatar", "MENA"),
    "ksa": ("Saudi Arabia", "MENA"),
    "turkey": ("Turkey", "Europe"),
    "greece": ("Greece", "Europe"),
    "italy": ("Italy", "Europe"),
    "spain": ("Spain", "Europe"),
    "france": ("France", "Europe"),
    "portugal": ("Portugal", "Europe"),
    "croatia": ("Croatia", "Europe"),
    "ireland": ("Ireland", "Europe"),
    "uk": ("United Kingdom", "Europe"),
    "sweden": ("Sweden", "Europe"),
    "finland": ("Finland", "Europe"),
    "estonia": ("Estonia", "Europe"),
    "romania": ("Romania", "Europe"),
    "cyprus": ("Cyprus", "Europe"),
    "israel": ("Israel", "MENA"),
    "lebanon": ("Lebanon", "MENA"),
    "egypt": ("Egypt", "MENA"),
    "morocco": ("Morocco", "Africa"),
    "senegal": ("Senegal", "Africa"),
    "nigeria": ("Nigeria", "Africa"),
    "mozambique": ("Mozambique", "Africa"),
    "kenya": ("Kenya", "Africa"),
    "tanzania": ("Tanzania", "Africa"),
    "ivory-coast": ("Côte d'Ivoire", "Africa"),
    "cote-divoire": ("Côte d'Ivoire", "Africa"),
    "pakistan": ("Pakistan", "South Asia"),
    "kazakhstan": ("Kazakhstan", "Caspian"),
    "azerbaijan": ("Azerbaijan", "Caspian"),
    "tunisia": ("Tunisia", "Africa"),
    "indonesia": ("Indonesia", "SEA"),
    "thailand": ("Thailand", "SEA"),
    "malaysia": ("Malaysia", "SEA"),
    "philippines": ("Philippines", "SEA"),
    "vietnam": ("Vietnam", "SEA"),
    "singapore": ("Singapore", "SEA"),
    "japan": ("Japan", "East Asia"),
    "korea": ("Korea", "East Asia"),
    "china": ("China", "East Asia"),
    "india": ("India", "South Asia"),
    "australia": ("Australia", "Oceania"),
    "new-zealand": ("New Zealand", "Oceania"),
    "brazil": ("Brazil", "Americas"),
    "mexico": ("Mexico", "Americas"),
    "usa": ("United States", "Americas"),
    "belize": ("Belize", "Americas"),
    "panama": ("Panama", "Americas"),
    "colombia": ("Colombia", "Americas"),
    "dominican-republic": ("Dominican Republic", "Americas"),
    "fiji": ("Fiji", "Oceania"),
    "french-polynesia": ("French Polynesia", "Oceania"),
    "hk": ("Hong Kong", "East Asia"),
    "taiwan": ("Taiwan", "East Asia"),
    "bahrain": ("Bahrain", "MENA"),
    "oman": ("Oman", "MENA"),
    "jamaica": ("Jamaica", "Americas"),
    "mauritius": ("Mauritius", "Africa"),
    "south-africa": ("South Africa", "Africa"),
    "monaco": ("Monaco", "Europe"),
}


def load_json(path: Path):
    return json.loads(path.read_text())


def save_json(path: Path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def normalize_name(name: str) -> str:
    s = (name or "").lower().strip()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^\w\s]", "", s)
    return s


def resolve_city_id(raw: str, known: set[str]) -> str:
    if raw in known:
        return raw
    mapped = CITY_CROSSWALK.get(raw)
    if mapped and mapped in known:
        return mapped
    if mapped:
        return mapped
    for cid in known:
        if cid == raw or cid.startswith(raw + "-") or raw.startswith(cid + "-"):
            return cid
    return CITY_CROSSWALK.get(raw, raw)


def infer_country_region(city_id: str, city_name: str | None) -> tuple[str, str]:
    parts = city_id.split("-")
    for i in range(len(parts) - 1, 0, -1):
        suffix = "-".join(parts[i:])
        if suffix in COUNTRY_SUFFIX:
            return COUNTRY_SUFFIX[suffix]
        if parts[i] in COUNTRY_SUFFIX:
            return COUNTRY_SUFFIX[parts[i]]
    if city_name and "," in city_name:
        country = city_name.split(",")[-1].strip()
        return country, "Global"
    return "Global", "Global"


def mint_bp_id(city_id: str, bp: dict) -> str:
    raw = bp.get("id") or ""
    if raw.startswith("bp-"):
        return raw
    seed = json.dumps(
        {"city": city_id, "id": raw, "lng": bp.get("lng"), "lat": bp.get("lat"), "name": bp.get("name")},
        sort_keys=True,
        separators=(",", ":"),
    )
    return "bp-" + hashlib.sha256(seed.encode()).hexdigest()[:10]


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
            dlon = (d / R_EARTH_KM) * math.sin(br) / max(math.cos(math.radians(lat)), 1e-6) * (180 / math.pi)
            if is_water(lon + dlon, lat + dlat, mask):
                best = min(best, d)
                break
            d += step_km
    return round(best, 4)


def in_allowlist_bbox(lon: float, lat: float, allowlist: dict, pid: str | None = None) -> bool:
    if pid and pid in allowlist.get("allowlisted_ids", {}):
        return True
    for body in allowlist.get("water_bodies", []):
        bbox = body.get("bbox")
        if not bbox or len(bbox) != 4:
            continue
        min_lon, max_lon, min_lat, max_lat = bbox
        if min_lon <= lon <= max_lon and min_lat <= lat <= max_lat:
            return True
    for pt in allowlist.get("points", []):
        plon = pt.get("lng", pt.get("lon", 0))
        plat = pt.get("lat", 0)
        if abs(plon - lon) < 0.02 and abs(plat - lat) < 0.02:
            return True
    for entry in allowlist.get("allowlisted_ids", {}).values():
        elon = entry.get("lng", entry.get("lon", 0))
        elat = entry.get("lat", 0)
        if abs(elon - lon) < 0.02 and abs(elat - lat) < 0.02:
            return True
    return False


INTERNAL_BP_MARKERS = (
    "absence wedge",
    "flag-and-exclude",
    "flag and exclude",
    "chain-gap-as-wedge",
    "counterparty pointer",
    "cross-border pointer",
    "cross-cluster pointer",
    "— pointer",
    "pointer —",
    "(pointer)",
    "(hide",
    "do not engage",
    "hard hold",
    "politically-active",
    "asymmetric-recognition",
)

EXCLUSION_SCRUB_RE = [
    (re.compile(r"\bexclusive\b", re.I), ""),
    (re.compile(r"\bwedges?\b", re.I), "gap"),
    (re.compile(r"\bconvener\b", re.I), "host"),
    (re.compile(r"\bcounterpart(?:y|ies)\b", re.I), "peer"),
    (re.compile(r"\bflag[\s_-]?and[\s_-]?exclude\b", re.I), "sovereign-hold"),
]


def is_internal_metadata_bp(bp: dict) -> str | None:
    """Return drop reason if BP is internal Tasklet metadata, not a public pier."""
    blob = " ".join(
        str(bp.get(k) or "")
        for k in ("name", "notes", "operator", "formatted_address", "source")
    ).lower()
    for marker in INTERNAL_BP_MARKERS:
        if marker in blob:
            return f"internal_metadata:{marker}"
    return None


def scrub_field(text: str | None) -> str | None:
    if not text:
        return text
    out = text
    for pat, repl in EXCLUSION_SCRUB_RE:
        out = pat.sub(repl, out)
    out = re.sub(r"\s+", " ", out).strip(" -—")
    return out or None


def fmt_usd_millions(val: float | None) -> str | None:
    if val is None:
        return None
    if val >= 1_000_000_000:
        return f"${val / 1_000_000_000:.2f}B".replace(".00B", "B")
    if val >= 1_000_000:
        return f"${round(val / 1_000_000)}M"
    if val >= 1_000:
        return f"${round(val / 1_000)}K"
    return f"${round(val)}"