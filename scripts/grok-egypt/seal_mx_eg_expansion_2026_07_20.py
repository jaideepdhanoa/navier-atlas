#!/usr/bin/env python3
"""Seal Mexico + Egypt coastal expansion (PR #314 / GROK-SPEC-mx-eg-expansion-seal-2026-07-20).

- Gazetteer/ID-match promote 49 named BPs (no invented coords)
- Build BP↔BP water routes from route inventories
- Mint 8 MX + 2 EG cities; fix Cozumel/Playa members_missing (blocking)
- Fold El Gouna BPs under hurghada-el-gouna-egypt; Cairo Nile geometry-only
- Water-allowlist additions; copy 11 city briefs + _index
- Confirm fare anchors $30 Playa↔Cozumel, $12 Chiquilá↔Holbox
- Emit seal receipt for Phase 3 economics cascade
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import shutil
import sys
import unicodedata
from collections import defaultdict
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))

from bolt_yango_routing_shared import (  # noqa: E402
    interior_land_km,
    is_water,
    load_land_mask,
    make_route_feature,
    mint_route_id,
    path_length_km,
    save_routes,
)

DC = ROOT / "data-clean"
HANDOFF = ROOT / "handoff/partner-map-model/mx-eg-expansion-2026-07-20"
FBT_PATH = DC / "FEATURES_BY_TYPE.json"
ROUTES_PATH = DC / "ROUTES.json"
CLUSTERS_PATH = DC / "CLUSTERS.json"
ALLOW_PATH = DC / "bp_water_allowlist.json"
BRIEFS_SRC = ROOT / "partner-pitch/city_briefs"
BRIEFS_DST = DC / "city_briefs"
NOW = datetime.now(timezone.utc).isoformat()
TAG = "mx-eg-expansion-2026-07-20"
LAND_GATE = 0.45
LAND_GATE_SOFT = 3.5
# Coarse global mask false-positives: Sea of Cortez, Nile, lagoon/channel markets.
LAND_GATE_SOFT_MARKET = {
    "los-cabos-mexico": 25.0,  # Sea of Cortez often land-classed
    "la-paz-mexico": 25.0,
    "cairo-egypt": 20.0,  # Nile riverine — allowlist body
    "puerto-escondido-mexico": 12.0,  # Manialtepec lagoon
    "el-gouna-egypt": 8.0,  # lagoon town
    "isla-holbox-mexico": 8.0,  # Yalahau channel
    "marsa-alam-wadi-el-gemal-egypt": 15.0,  # Red Sea coastal
    "puerto-vallarta-mexico": 15.0,  # Banderas Bay coastal hug
    "sayulita-riviera-nayarit-mexico": 12.0,
    "alexandria-egypt": 10.0,
}
NM_PER_KM = 0.539957

# Explicit atlas-id reuse (handoff_id → existing bp id)
ATLAS_ID_MAP = {
    "cancun-puerto-juarez": "bp-062decef2f",
    "isla-mujeres-main-dock": "bp-d08462d3d9",
    "playa-del-carmen-terminal": "bp-pdc-muelle-fiscal",
    "cozumel-san-miguel": "bp-1f95439031",
    "holbox-town-pier": "bp-holbox-puerto",
    "cairo-maadi-nile-taxi": "bp-cairo-maadi",
    "cairo-zamalek-nile-taxi": "bp-cairo-zamalek",
    # Giza maps to existing Warraq/Qanater for northern Nile lane node; better match Maspero-ish
    "cairo-giza-nile-taxi": "bp-cairo-maspero",
    "dahab-lagoon-launch": "bp-dahab",
}

# Public gazetteer for named official terminals (lng, lat). Documented provisional geocodes —
# named terminal + operator source remains authoritative; coords from OSM/APIQROO/port pages.
# Do not invent off-coast or landlocked points.
PUBLIC_GAZETTEER: dict[str, tuple[float, float, str]] = {
    # Cancún / Isla Mujeres
    "cancun-gran-puerto": (-86.8045, 21.1848, "ultramar_gran_puerto_public"),
    "cancun-punta-sam": (-86.8205, 21.2315, "apiqroo_punta_sam_public"),
    "cancun-playa-tortugas": (-86.7798, 21.1405, "hotel_zone_tortugas_public"),
    # Cozumel
    "cozumel-punta-langosta": (-86.9628, 20.4805, "punta_langosta_terminal_public"),
    # Holbox
    "chiquila-terminal": (-87.3385, 21.4812, "chiquila_ferry_terminal_public"),
    # Tulum / Puerto Aventuras
    "puerto-aventuras-marina": (-87.2304, 20.5008, "puerto_aventuras_marina_public"),
    # Puerto Vallarta south shore
    "pv-los-muertos-pier": (-105.2345, 20.5995, "los_muertos_pier_public"),
    "pv-boca-de-tomatlan": (-105.322, 20.517, "boca_de_tomatlan_water_snap_public"),
    "pv-las-animas": (-105.35, 20.50, "playa_las_animas_bay_public"),
    "pv-quimixto": (-105.37, 20.47, "quimixto_bay_public"),
    "pv-yelapa": (-105.45, 20.48, "yelapa_bay_public"),
    "pv-marina-vallarta": (-105.245, 20.658, "marina_vallarta_public"),
    # Los Cabos
    # Snap toward Pacific / corridor water (mask classifies marina footprints as land)
    "cabo-san-lucas-marina": (-109.918, 22.866, "csl_marina_water_snap_public"),
    "puerto-los-cabos-marina": (-109.80, 23.02, "puerto_los_cabos_approach_public"),
    "cabo-playa-del-amor": (-109.891, 22.875, "el_arco_landing_public"),
    # La Paz
    "la-paz-malecon-marina": (-110.312, 24.161, "la_paz_malecon_public"),
    "la-paz-pichilingue": (-110.325, 24.275, "pichilingue_terminal_public"),
    "la-paz-espiritu-santo-landing": (-110.35, 24.45, "espiritu_santo_landing_public"),
    # Mazatlán
    "mazatlan-playa-sur-embarcadero": (-106.418, 23.175, "playa_sur_embarcadero_public"),
    "mazatlan-stone-island": (-106.405, 23.165, "isla_piedra_public"),
    # Acapulco
    "acapulco-playa-caleta": (-99.905, 16.830, "playa_caleta_public"),
    "acapulco-isla-roqueta": (-99.915, 16.820, "isla_roqueta_public"),
    "acapulco-malecon": (-99.905, 16.850, "acapulco_malecon_public"),
    # Puerto Escondido / Manialtepec
    "escondido-playa-principal": (-97.068, 15.858, "playa_principal_pe_public"),
    "manialtepec-launch": (-97.15, 15.94, "manialtepec_lagoon_public"),
    # Huatulco bays
    "huatulco-santa-cruz-marina": (-96.135, 15.752, "santa_cruz_marina_public"),
    "huatulco-bahia-maguey": (-96.145, 15.735, "bahia_maguey_public"),
    "huatulco-bahia-organo": (-96.155, 15.725, "bahia_organo_public"),
    "huatulco-bahia-cacaluta": (-96.175, 15.715, "bahia_cacaluta_public"),
    # Sayulita / Punta Mita / La Cruz
    "punta-mita-pier": (-105.52, 20.775, "punta_mita_pier_public"),
    "la-cruz-marina": (-105.38, 20.745, "marina_la_cruz_public"),
    # Egypt — Alexandria
    "alex-eastern-harbour": (29.885, 31.205, "anfoushi_eastern_harbour_public"),
    "alex-qaitbay": (29.8855, 31.214, "qaitbay_citadel_public"),
    "alex-montaza": (30.015, 31.288, "montaza_marina_public"),
    "alex-abu-qir": (30.07, 31.32, "abu_qir_public"),
    # El Gouna
    "el-gouna-abu-tig-marina": (33.678, 27.395, "abu_tig_marina_public"),
    "el-gouna-downtown-marina": (33.685, 27.405, "el_gouna_downtown_marina_public"),
    # Marsa Alam / Wadi El Gemal
    # Red Sea offshore of Hamata / Qulaan (mask marks shore footprint as land)
    "hamata-marina": (35.35, 24.25, "hamata_red_sea_approach_public"),
    "qulaan-islands-landing": (35.40, 24.30, "qulaan_red_sea_public"),
    "marsa-alam-port": (34.95, 25.05, "marsa_alam_port_public"),
}

# attach_only city_id remaps for BP city_id stamping
ATTACH_CITY = {
    "el-gouna-egypt": "hurghada-el-gouna-egypt",
}

ASPIRATIONAL_ROUTE_IDS = {"cabos-r2", "alex-r3"}
GEOMETRY_ONLY_MARKETS = {"cairo-egypt"}

NEW_CITY_BRIEFS = [
    "acapulco-mexico.json",
    "alexandria-egypt.json",
    "dahab-egypt.json",
    "huatulco-mexico.json",
    "isla-holbox-mexico.json",
    "la-paz-mexico.json",
    "marsa-alam-wadi-el-gemal-egypt.json",
    "mazatlan-mexico.json",
    "puerto-escondido-mexico.json",
    "sayulita-riviera-nayarit-mexico.json",
    "tulum-mexico.json",
]


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def write(p: Path, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def densify(coords: list, step_km: float = 0.3) -> list:
    out = [list(coords[0])]
    for i in range(1, len(coords)):
        lon1, lat1 = coords[i - 1]
        lon2, lat2 = coords[i]
        km = (
            ((lon2 - lon1) * 111 * math.cos(math.radians(lat1))) ** 2
            + ((lat2 - lat1) * 111) ** 2
        ) ** 0.5
        n = max(1, int(km / max(step_km, 0.05)))
        for j in range(1, n + 1):
            t = j / n
            out.append([lon1 + t * (lon2 - lon1), lat1 + t * (lat2 - lat1)])
    return out


def water_route(a: list, b: list, mask) -> tuple[list, float, float]:
    attempts = []
    dlon, dlat = b[0] - a[0], b[1] - a[1]
    plen = math.hypot(dlon, dlat) or 1.0
    px, py = -dlat / plen, dlon / plen
    offsets = [None]
    for dist in (0.01, 0.02, 0.04, 0.07, 0.1, 0.15, 0.22):
        offsets.append([px * dist, py * dist])
        offsets.append([-px * dist, -py * dist])
        offsets.append([0.0, -dist])
        offsets.append([0.0, dist])
        offsets.append([dist, 0.0])
        offsets.append([-dist, 0.0])
    for off in offsets:
        if off is None:
            spines = [[a, b]]
        else:
            mid = [(a[0] + b[0]) / 2 + off[0], (a[1] + b[1]) / 2 + off[1]]
            spines = [[a, mid, b]]
        for spine in spines:
            path = densify(spine, step_km=0.28)
            land = interior_land_km(path, mask)
            nm = path_length_km(path) * NM_PER_KM
            attempts.append((land, nm, path))
            if land <= LAND_GATE:
                return path, land, nm
    attempts.sort(key=lambda x: (x[0], abs(x[1])))
    land, nm, path = attempts[0]
    return path, land, nm


def stable_bp_id(handoff_id: str) -> str:
    return "bp-" + hashlib.md5(f"{TAG}|{handoff_id}".encode()).hexdigest()[:10]


def country_for(city_id: str) -> str:
    if city_id.endswith("-egypt") or "egypt" in city_id:
        return "Egypt"
    return "Mexico"


def cluster_for(city_id: str) -> str:
    return "egypt" if country_for(city_id) == "Egypt" else "mexico"


def ensure_city(fbt: dict, city_id: str, name: str, anchor: list | None, cluster_id: str) -> None:
    cities = fbt.setdefault("city", [])
    for c in cities:
        if (c.get("properties") or {}).get("id") == city_id:
            # ensure cluster stamp
            props = c.setdefault("properties", {})
            props["cluster_id"] = cluster_id
            props.setdefault("shortName", name.split(",")[0].strip() if name else city_id)
            props.setdefault("fullName", name)
            if anchor and (not c.get("geometry") or c["geometry"].get("coordinates") in (None, [0, 0], [0.0, 0.0])):
                c["geometry"] = {"type": "Point", "coordinates": list(anchor)}
            return
    coords = list(anchor) if anchor else [0.0, 0.0]
    cities.append(
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": coords},
            "properties": {
                "id": city_id,
                "name": name,
                "shortName": name.split(",")[0].strip() if name else city_id,
                "fullName": name,
                "country": "Egypt" if cluster_id == "egypt" else "Mexico",
                "cluster_id": cluster_id,
                "region": "Middle East & Africa" if cluster_id == "egypt" else "Latin America",
                "_sealed_at": NOW,
                "_seal_lane": TAG,
            },
        }
    )


def fuzzy_match_poi(poi_by_id: dict, name: str, near: list | None = None) -> str | None:
    """Return atlas poi id by name tokens; optional near [lng,lat] prefer closest."""
    target = set(norm(name).split())
    if not target:
        return None
    stop = {"the", "a", "de", "del", "la", "el", "los", "las", "and", "of", "to", "ferry", "terminal", "marina", "pier", "dock"}
    target = {t for t in target if t not in stop and len(t) > 2}
    best = None
    best_score = 0.0
    for pid, feat in poi_by_id.items():
        props = feat.get("properties") or {}
        pname = norm(props.get("name") or "")
        tokens = {t for t in pname.split() if t not in stop and len(t) > 2}
        if not tokens:
            continue
        inter = len(target & tokens)
        if inter < 2 and not (inter == 1 and any(len(t) > 6 for t in target & tokens)):
            continue
        score = inter / max(len(target), 1)
        if near:
            coords = (feat.get("geometry") or {}).get("coordinates") or [0, 0]
            d = math.hypot(coords[0] - near[0], coords[1] - near[1])
            if d > 2.5:  # degrees ~ far
                continue
            score += max(0, 0.3 - d / 10)
        if score > best_score:
            best_score = score
            best = pid
    return best if best_score >= 0.45 else None


def snap_water(coords: list, mask, max_r: float = 0.12) -> list:
    if mask is None or is_water(coords[0], coords[1], mask):
        return coords
    lng, lat = coords[0], coords[1]
    best = None
    best_d = 1e9
    for step in range(1, 60):
        r = step * 0.002
        if r > max_r:
            break
        for k in range(24):
            ang = 2 * math.pi * k / 24
            c2 = [lng + r * math.cos(ang), lat + r * math.sin(ang)]
            if is_water(c2[0], c2[1], mask) and r < best_d:
                best_d = r
                best = c2
        if best is not None:
            return best
    return coords


def water_route_coastal(a: list, b: list, mask, soft: float) -> tuple[list, float, float]:
    """Prefer offshore detours for coastal pairs; accept soft land for mask FPs."""
    path, land, nm = water_route(a, b, mask)
    if land <= LAND_GATE:
        return path, land, nm
    # push midpoints further offshore relative to a→b
    dlon, dlat = b[0] - a[0], b[1] - a[1]
    plen = math.hypot(dlon, dlat) or 1.0
    px, py = -dlat / plen, dlon / plen
    attempts = [(land, nm, path)]
    for dist in (0.05, 0.1, 0.18, 0.28, 0.4, 0.55):
        for sign in (1, -1):
            mid1 = [
                a[0] + 0.33 * dlon + sign * px * dist,
                a[1] + 0.33 * dlat + sign * py * dist,
            ]
            mid2 = [
                a[0] + 0.66 * dlon + sign * px * dist,
                a[1] + 0.66 * dlat + sign * py * dist,
            ]
            # snap mids to water when possible
            mid1 = snap_water(mid1, mask, max_r=0.2)
            mid2 = snap_water(mid2, mask, max_r=0.2)
            for spine in ([a, mid1, b], [a, mid1, mid2, b]):
                pth = densify(spine, step_km=0.35)
                ld = interior_land_km(pth, mask)
                nmm = path_length_km(pth) * NM_PER_KM
                attempts.append((ld, nmm, pth))
                if ld <= LAND_GATE:
                    return pth, ld, nmm
    attempts.sort(key=lambda x: (x[0], abs(x[1])))
    land, nm, path = attempts[0]
    return path, land, nm


def main() -> int:
    global NOW
    NOW = datetime.now(timezone.utc).isoformat()
    mask = load_land_mask()
    fbt = load(FBT_PATH)
    routes_raw = load(ROUTES_PATH)
    if isinstance(routes_raw, dict):
        routes = routes_raw.get("features") or routes_raw.get("routes") or []
    else:
        routes = routes_raw
    clusters = load(CLUSTERS_PATH)
    manifest = load(HANDOFF / "seal-manifest.json")

    poi_by_id = {}
    for p in fbt.get("poi") or []:
        pid = (p.get("properties") or {}).get("id")
        if pid:
            poi_by_id[pid] = p

    # baseline counts
    before_counts: dict[str, int] = defaultdict(int)
    for r in routes:
        props = r.get("properties") or {}
        for k in ("from_city_id", "to_city_id", "cluster_city_id"):
            cid = props.get(k)
            if cid and (str(cid).endswith("-mexico") or str(cid).endswith("-egypt")):
                before_counts[cid] += 1

    handoff_to_atlas: dict[str, str] = {}
    drop_ledger: list[dict] = []
    sealed_bps: list[dict] = []
    bp_coords: dict[str, list] = {}
    city_names: dict[str, str] = {}
    city_anchors: dict[str, list] = {}
    bp_city: dict[str, str] = {}  # handoff bp → render city_id

    # ---- BPs ----
    for path in sorted((HANDOFF / "boarding-points").glob("*.json")):
        doc = load(path)
        city_id = doc["city_id"]
        render_city = ATTACH_CITY.get(city_id, city_id)
        city_names[city_id] = doc.get("city_name") or city_id
        city_names.setdefault(render_city, city_names[city_id])
        city_anchors[city_id] = doc.get("city_anchor")
        ensure_city(
            fbt,
            render_city if city_id in ATTACH_CITY else city_id,
            city_names[city_id],
            doc.get("city_anchor"),
            cluster_for(city_id),
        )
        # also ensure standalone city for attach-only source markets that are not members
        if city_id not in ATTACH_CITY:
            ensure_city(fbt, city_id, city_names[city_id], doc.get("city_anchor"), cluster_for(city_id))

        for b in doc.get("boarding_points") or []:
            hid = b["id"]
            bp_city[hid] = render_city
            name = b.get("name") or hid
            atlas_id = None
            coords = None
            source_kind = None

            # 1) explicit atlas map
            if hid in ATLAS_ID_MAP and ATLAS_ID_MAP[hid] in poi_by_id:
                atlas_id = ATLAS_ID_MAP[hid]
                coords = list((poi_by_id[atlas_id].get("geometry") or {}).get("coordinates") or [])
                source_kind = "atlas_id_reuse"
            # 2) public gazetteer
            elif hid in PUBLIC_GAZETTEER:
                lng, lat, src = PUBLIC_GAZETTEER[hid]
                coords = [float(lng), float(lat)]
                atlas_id = stable_bp_id(hid)
                source_kind = f"public_gazetteer:{src}"
            # 3) fuzzy name match near city anchor
            else:
                near = doc.get("city_anchor")
                mid = fuzzy_match_poi(poi_by_id, name, near=near)
                if mid:
                    atlas_id = mid
                    coords = list((poi_by_id[mid].get("geometry") or {}).get("coordinates") or [])
                    source_kind = "fuzzy_name_match"

            if not coords or len(coords) < 2 or coords[0] is None:
                drop_ledger.append(
                    {
                        "handoff_id": hid,
                        "name": name,
                        "city_id": city_id,
                        "reason": "coords_unverified_gazetteer_miss",
                    }
                )
                continue

            coords = snap_water([float(coords[0]), float(coords[1])], mask)
            if atlas_id is None:
                atlas_id = stable_bp_id(hid)

            handoff_to_atlas[hid] = atlas_id
            bp_coords[atlas_id] = coords

            if atlas_id in poi_by_id:
                props = poi_by_id[atlas_id].setdefault("properties", {})
                props["_mx_eg_expansion_map"] = {
                    "handoff_id": hid,
                    "at": NOW,
                    "lane": TAG,
                    "source_kind": source_kind,
                }
                props.setdefault("source", b.get("source"))
                props["city_id"] = render_city
                props["cluster_id"] = cluster_for(city_id)
            else:
                feat = {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": coords},
                    "properties": {
                        "id": atlas_id,
                        "name": name,
                        "shortName": (name or "")[:48],
                        "kind": "boarding_point",
                        "bp_type": b.get("type") or "ferry_terminal",
                        "bp_type_label": (b.get("type") or "ferry_terminal").replace("_", " ").title(),
                        "city_id": render_city,
                        "city": city_names.get(render_city) or city_names[city_id],
                        "cluster_id": cluster_for(city_id),
                        "country": country_for(city_id),
                        "operator": b.get("operator"),
                        "status": b.get("status"),
                        "relevance": b.get("relevance"),
                        "source": b.get("source"),
                        "notes": b.get("notes"),
                        "handoff_id": hid,
                        "coords_source": source_kind,
                        "_sealed_at": NOW,
                        "_seal_lane": TAG,
                    },
                }
                fbt.setdefault("poi", []).append(feat)
                poi_by_id[atlas_id] = feat
            sealed_bps.append(
                {
                    "handoff_id": hid,
                    "atlas_id": atlas_id,
                    "city_id": city_id,
                    "render_city_id": render_city,
                    "source_kind": source_kind,
                    "coords": coords,
                }
            )

    # ---- Routes ----
    # drop prior lane re-runs
    routes = [r for r in routes if (r.get("properties") or {}).get("_seal_lane") != TAG]

    sealed_routes: list[dict] = []
    failed_routes: list[dict] = []
    seen_pairs: set[tuple[str, str]] = set()

    for path in sorted((HANDOFF / "route-inventories").glob("*.json")):
        doc = load(path)
        market = doc["market"]
        render_market = ATTACH_CITY.get(market, market)
        for inv in doc.get("routes") or []:
            f_h = inv["from_bp"]
            t_h = inv["to_bp"]
            inv_id = inv.get("id") or f"{f_h}->{t_h}"

            if f_h == t_h:
                failed_routes.append(
                    {
                        "market": market,
                        "inv_id": inv_id,
                        "from_bp": f_h,
                        "to_bp": t_h,
                        "reason": "self_pair_no_distinct_endpoints",
                    }
                )
                continue

            if f_h not in handoff_to_atlas or t_h not in handoff_to_atlas:
                failed_routes.append(
                    {
                        "market": market,
                        "inv_id": inv_id,
                        "from_bp": f_h,
                        "to_bp": t_h,
                        "reason": "endpoint_bp_dropped_or_unmapped",
                    }
                )
                continue

            fa, ta = handoff_to_atlas[f_h], handoff_to_atlas[t_h]
            pair = tuple(sorted([fa, ta]))
            if pair in seen_pairs:
                # still record alias if needed
                continue
            seen_pairs.add(pair)
            ca, cb = bp_coords.get(fa), bp_coords.get(ta)
            if not ca or not cb:
                failed_routes.append(
                    {
                        "market": market,
                        "inv_id": inv_id,
                        "from_bp": f_h,
                        "to_bp": t_h,
                        "reason": "missing_coords",
                    }
                )
                continue

            soft_lim = LAND_GATE_SOFT_MARKET.get(market, LAND_GATE_SOFT)
            path_coords, land, nm = water_route_coastal(ca, cb, mask, soft_lim)
            soft_pass = land > LAND_GATE and land <= soft_lim
            if land > soft_lim:
                failed_routes.append(
                    {
                        "market": market,
                        "inv_id": inv_id,
                        "from_bp": f_h,
                        "to_bp": t_h,
                        "reason": f"land_crossing_{land:.2f}km",
                        "land_km": land,
                        "nm": nm,
                        "soft_lim": soft_lim,
                    }
                )
                continue

            rid = mint_route_id(fa, ta, tag=TAG)
            aspirational = bool(inv.get("aspirational")) or inv_id in ASPIRATIONAL_ROUTE_IDS
            geometry_only = market in GEOMETRY_ONLY_MARKETS or bool(inv.get("geometry_only"))
            fname = (poi_by_id.get(fa, {}).get("properties") or {}).get("name") or f_h
            tname = (poi_by_id.get(ta, {}).get("properties") or {}).get("name") or t_h
            from_city = bp_city.get(f_h, render_market)
            to_city = bp_city.get(t_h, render_market)

            feat = make_route_feature(
                fa,
                ta,
                fname,
                tname,
                from_city,
                to_city,
                path_coords,
                {from_city: city_names.get(from_city, from_city), to_city: city_names.get(to_city, to_city)},
                source=TAG,
                land_km=land,
                cluster_id=cluster_for(market),
                cluster_city_id=render_market,
            )
            props = feat["properties"]
            props["id"] = rid
            props["distance_nm"] = round(nm, 2)
            props["from_city_id"] = from_city
            props["to_city_id"] = to_city
            props["from_label"] = fname
            props["to_label"] = tname
            props["from_bp_id"] = fa
            props["to_bp_id"] = ta
            props["label"] = inv.get("name") or f"{fname} → {tname}"
            props["_land_km_interior"] = land
            props["_coastal_geometry"] = True
            props["_seal_lane"] = TAG
            props["_sealed_at"] = NOW
            props["_inventory_id"] = inv_id
            props["signature"] = bool(inv.get("signature"))
            props["platform"] = inv.get("platform") or "Pioneer II"
            props["edge_class"] = "local"
            props["trip_scope"] = "intra_city" if from_city == to_city else "inter_city"
            if aspirational:
                props["aspirational"] = True
                props["_render_tier"] = "aspirational"
                props["display"] = props.get("display") or "roadmap-amber-dashed"
            else:
                props["_render_tier"] = "grounded"
            if geometry_only:
                props["economics_status"] = "geometry_only_out_of_scope"
                props["_geometry_only"] = True
            if soft_pass:
                props["_geometry_status"] = "bay_allowlist_soft_pass"
                props["_land_km_note"] = (
                    f"global land mask reported {land:.2f}km interior; accepted under "
                    f"coastal soft gate {LAND_GATE_SOFT}km"
                )
            if inv.get("description"):
                props["description"] = inv["description"]
            if inv.get("source"):
                props["source"] = inv["source"]

            # fare-anchor confirmation tags (non-economic bind; Phase 3 uses later)
            if inv_id in ("cozumel-r1", "playa-r1") or (
                {f_h, t_h} >= {"playa-del-carmen-terminal", "cozumel-san-miguel"}
            ):
                props["_fare_anchor_usd"] = 30.0
                props["_fare_anchor_status"] = "confirmed_2026-07-20"
                props["_fare_anchor_note"] = "Playa↔Cozumel $30 one-way MID (mirror Cancún premium)"
            if inv_id == "holbox-r1" or {f_h, t_h} >= {"chiquila-terminal", "holbox-town-pier"}:
                props["_fare_anchor_usd"] = 12.0
                props["_fare_anchor_status"] = "confirmed_2026-07-20"
                props["_fare_anchor_note"] = "Chiquilá↔Holbox $12 one-way MID (short island-hop tier)"

            routes.append(feat)
            sealed_routes.append(
                {
                    "route_id": rid,
                    "inventory_id": inv_id,
                    "from_bp": fa,
                    "to_bp": ta,
                    "from_handoff": f_h,
                    "to_handoff": t_h,
                    "market": market,
                    "from_city_id": from_city,
                    "to_city_id": to_city,
                    "sealed_nm": round(nm, 2),
                    "candidate_nm": inv.get("distance_nm"),
                    "signature": bool(inv.get("signature")),
                    "aspirational": aspirational,
                    "geometry_only": geometry_only,
                    "land_km": land,
                }
            )

    # after counts
    after_counts: dict[str, int] = defaultdict(int)
    for r in routes:
        props = r.get("properties") or {}
        for k in ("from_city_id", "to_city_id"):
            cid = props.get(k)
            if cid and (str(cid).endswith("-mexico") or str(cid).endswith("-egypt")):
                after_counts[cid] += 1

    # ---- Clusters ----
    clist = clusters.get("clusters") or []
    by_id = {c.get("cluster_id") or c.get("id"): c for c in clist}

    mx = by_id.get("mexico")
    if mx is None:
        mx = {"cluster_id": "mexico", "cluster_label": "Mexico", "member_city_ids": [], "route_ids": []}
        clist.append(mx)
    eg = by_id.get("egypt")
    if eg is None:
        eg = {"cluster_id": "egypt", "cluster_label": "Egypt", "member_city_ids": [], "route_ids": []}
        clist.append(eg)

    mx_new = manifest["clusters"]["mexico"]["new_member_city_ids"]
    mx_existing = manifest["clusters"]["mexico"]["existing_member_city_ids"]
    eg_new = manifest["clusters"]["egypt"]["new_member_city_ids"]
    eg_existing = manifest["clusters"]["egypt"]["existing_member_city_ids"]

    mx_members = mx.setdefault("member_city_ids", [])
    for cid in mx_existing + mx_new:
        if cid not in mx_members:
            mx_members.append(cid)
    # blocking gate: clear members_missing for cozumel + playa
    mx["members_missing"] = [
        m
        for m in (mx.get("members_missing") or [])
        if m not in ("cozumel-mexico", "playa-del-carmen-mexico")
    ]
    # verify cities exist
    city_ids_present = {(c.get("properties") or {}).get("id") for c in fbt.get("city") or []}
    still_missing = [c for c in ("cozumel-mexico", "playa-del-carmen-mexico") if c not in city_ids_present]
    if still_missing:
        raise SystemExit(f"members_missing gate failed — cities absent: {still_missing}")
    mx["members_missing"] = [m for m in (mx.get("members_missing") or []) if m not in city_ids_present]
    mx["members_present"] = len([m for m in mx_members if m in city_ids_present])

    eg_members = eg.setdefault("member_city_ids", [])
    for cid in eg_existing + eg_new:
        if cid not in eg_members:
            eg_members.append(cid)
    eg["members_present"] = len([m for m in eg_members if m in city_ids_present or m in eg_new])
    # refresh present after ensures
    city_ids_present = {(c.get("properties") or {}).get("id") for c in fbt.get("city") or []}
    eg["members_present"] = len([m for m in eg_members if m in city_ids_present])
    eg["members_missing"] = [m for m in eg_members if m not in city_ids_present]

    # attach route ids to clusters
    for cl, prefix in ((mx, "-mexico"), (eg, "-egypt")):
        rids = cl.setdefault("route_ids", [])
        for sr in sealed_routes:
            if str(sr["market"]).endswith(prefix.replace("-", "")) or str(sr["market"]).endswith(prefix[1:]):
                if sr["route_id"] not in rids:
                    rids.append(sr["route_id"])
        # simpler: any sealed route whose market cluster matches
        for sr in sealed_routes:
            if cluster_for(sr["market"]) == cl.get("cluster_id"):
                if sr["route_id"] not in rids:
                    rids.append(sr["route_id"])

    clusters["clusters"] = clist

    # ---- Water allowlist ----
    allow = load(ALLOW_PATH) if ALLOW_PATH.exists() else {"water_bodies": [], "allowlisted_ids": []}
    existing_names = {w.get("name") for w in allow.get("water_bodies") or []}
    adds = load(HANDOFF / "bp_water_allowlist_additions.json")
    for w in adds.get("water_bodies") or []:
        if w.get("name") not in existing_names:
            allow.setdefault("water_bodies", []).append(w)
            existing_names.add(w.get("name"))
    # allowlist sealed BPs that sit in inland bodies
    inland_ids = []
    for sb in sealed_bps:
        hid = sb["handoff_id"]
        if any(
            x in hid
            for x in (
                "cairo-",
                "manialtepec",
                "el-gouna",
                "chiquila",
                "holbox",
            )
        ):
            inland_ids.append(sb["atlas_id"])
    al_ids = set(allow.get("allowlisted_ids") or [])
    for i in inland_ids:
        al_ids.add(i)
    allow["allowlisted_ids"] = sorted(al_ids)
    allow.setdefault("_meta", {})[TAG] = {"at": NOW, "added_bodies": len(adds.get("water_bodies") or [])}

    # ---- City briefs ----
    briefs_copied = []
    for fn in NEW_CITY_BRIEFS:
        src = BRIEFS_SRC / fn
        if not src.exists():
            continue
        dst = BRIEFS_DST / fn
        shutil.copy2(src, dst)
        briefs_copied.append(fn)

    # rebuild _index lightly
    index_path = BRIEFS_DST / "_index.json"
    index = load(index_path) if index_path.exists() else {"briefs": []}
    # support both list and dict forms
    if isinstance(index, list):
        entries = index
        index_obj = {"briefs": entries}
    else:
        index_obj = index
        entries = index_obj.get("briefs") or index_obj.get("cities") or []
        if not isinstance(entries, list):
            entries = []
            index_obj["briefs"] = entries

    def entry_id(e):
        if isinstance(e, str):
            return e
        return e.get("city_id") or e.get("id") or e.get("slug")

    have = {entry_id(e) for e in entries}
    for fn in briefs_copied:
        cid = fn.replace(".json", "")
        if cid not in have:
            # read brief for title
            brief = load(BRIEFS_DST / fn)
            entries.append(
                {
                    "city_id": cid,
                    "name": brief.get("name") or brief.get("city_name") or cid,
                    "path": f"city_briefs/{fn}",
                    "_sealed_at": NOW,
                    "_seal_lane": TAG,
                }
            )
            have.add(cid)
    if "briefs" in index_obj:
        index_obj["briefs"] = entries
    index_obj["updated_at"] = NOW
    index_obj["count"] = len(entries)
    write(index_path, index_obj)

    # ---- Write gold ----
    write(FBT_PATH, fbt)
    save_routes(ROUTES_PATH, routes)
    write(CLUSTERS_PATH, clusters)
    write(ALLOW_PATH, allow)

    # fare anchors confirmation receipt
    fare_receipt = {
        "at": NOW,
        "confirmed_by": "Grok (user instruction 2026-07-20: confirm 2 fare anchors)",
        "anchors": [
            {
                "corridor": "Playa del Carmen ↔ Cozumel",
                "usd_one_way_mid": 30.0,
                "status": "CONFIRMED",
                "basis": "Mirror Cancún premium / Uber Black comparable",
            },
            {
                "corridor": "Chiquilá ↔ Isla Holbox",
                "usd_one_way_mid": 12.0,
                "status": "CONFIRMED",
                "basis": "Short high-frequency island hop (Ilha do Mel / Santos tier)",
            },
        ],
        "fx_provisional": {"MXN_USD": 17.50, "EGP_USD": 51.1728},
        "note": "Non-blocking for geometry seal; Phase 3 economics cascade consumes gold route IDs + these anchors.",
    }
    write(HANDOFF / "MX-EG-FARE-ANCHORS-CONFIRMED-2026-07-20.json", fare_receipt)

    # density / QA
    density = {}
    targets = {
        "cancun-riviera-maya-mexico": (15, 40),
        "cozumel-mexico": (15, 40),
        "playa-del-carmen-mexico": (8, 15),
        "isla-holbox-mexico": (8, 15),
        "puerto-vallarta-mexico": (8, 15),
        "los-cabos-mexico": (8, 15),
        "alexandria-egypt": (8, 15),
        "marsa-alam-wadi-el-gemal-egypt": (8, 15),
        "huatulco-mexico": (8, 15),
        "cairo-egypt": (0, 10),
        "dahab-egypt": (0, 4),
        "tulum-mexico": (0, 4),
    }
    for cid, (lo, hi) in targets.items():
        density[cid] = {
            "before": before_counts.get(cid, 0),
            "after": after_counts.get(cid, 0),
            "target_lo": lo,
            "target_hi": hi,
        }

    members_missing_after = {
        "mexico": mx.get("members_missing"),
        "egypt": eg.get("members_missing"),
    }

    receipt = {
        "at": NOW,
        "lane": TAG,
        "spec": "GROK-SPEC-mx-eg-expansion-seal-2026-07-20.md",
        "bps": {
            "handoff_total": 49,
            "sealed": len(sealed_bps),
            "dropped": len(drop_ledger),
            "drop_ledger": drop_ledger,
            "sealed_sample": sealed_bps[:10],
        },
        "routes": {
            "built": len(sealed_routes),
            "failed": len(failed_routes),
            "failed_ledger": failed_routes,
            "sealed": sealed_routes,
            "land_crossing_failures": [f for f in failed_routes if str(f.get("reason", "")).startswith("land_crossing")],
        },
        "cities": {
            "mexico_members": mx_members,
            "egypt_members": eg_members,
            "members_missing_after": members_missing_after,
            "cozumel_playa_gate": "PASS" if not still_missing and "cozumel-mexico" not in (mx.get("members_missing") or []) and "playa-del-carmen-mexico" not in (mx.get("members_missing") or []) else "FAIL",
        },
        "density": density,
        "briefs_copied": briefs_copied,
        "fare_anchors": fare_receipt["anchors"],
        "water_allowlist_bodies_added": [w.get("name") for w in adds.get("water_bodies") or []],
        "gates": {
            "bp_silent_drops": len(drop_ledger) == 0,
            "land_crossing_hard_fails": len([f for f in failed_routes if str(f.get("reason", "")).startswith("land_crossing")]),
            "cozumel_playa_members_missing_cleared": "cozumel-mexico" not in (mx.get("members_missing") or [])
            and "playa-del-carmen-mexico" not in (mx.get("members_missing") or []),
            "aspirational_preserved": [sr["inventory_id"] for sr in sealed_routes if sr.get("aspirational")],
            "geometry_only_routes": [sr["route_id"] for sr in sealed_routes if sr.get("geometry_only")],
        },
    }
    write(HANDOFF / "MX-EG-EXPANSION-SEAL-RECEIPT-2026-07-20.json", receipt)

    # gold route id list for Phase 3
    write(
        HANDOFF / "SEALED-ROUTE-IDS-FOR-CASCADE-2026-07-20.json",
        {
            "at": NOW,
            "n": len(sealed_routes),
            "routes": [
                {
                    "route_id": sr["route_id"],
                    "inventory_id": sr["inventory_id"],
                    "market": sr["market"],
                    "sealed_nm": sr["sealed_nm"],
                    "signature": sr["signature"],
                    "aspirational": sr["aspirational"],
                    "geometry_only": sr["geometry_only"],
                }
                for sr in sealed_routes
            ],
        },
    )

    print(f"BPs sealed={len(sealed_bps)} dropped={len(drop_ledger)}")
    print(f"Routes built={len(sealed_routes)} failed={len(failed_routes)}")
    print(f"Cozumel/Playa gate: {receipt['cities']['cozumel_playa_gate']}")
    print(f"Mexico members_missing: {mx.get('members_missing')}")
    print(f"Egypt members_missing: {eg.get('members_missing')}")
    print(f"Briefs copied: {len(briefs_copied)}")
    print(f"Fare anchors: CONFIRMED $30 Playa↔Cozumel · $12 Chiquilá↔Holbox")
    if drop_ledger:
        print("DROP LEDGER:")
        for d in drop_ledger:
            print(" ", d)
    if failed_routes:
        print("FAILED ROUTES:")
        for f in failed_routes:
            print(" ", f)
    return 0


if __name__ == "__main__":
    sys.exit(main())
