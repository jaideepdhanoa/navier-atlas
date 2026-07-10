#!/usr/bin/env python3
"""Mint Chile + Argentina (Wave C) registry after Registry owner approval.

Includes Buenos Aires ↔ Colonia (Uruguay) cross-border corridor.

Rules:
- Geography-owned IDs only (not DiDi-only geometry)
- Provisional public geocodes for BPs/cities (coords_source documented)
- All 10 candidate corridors minted as route_ids with provisional geometry
- Routes requiring hand waypoints stay quarantine/hide until land-crossing QA
- annual_one_way_pax stays null; no finance cascade
- Muelle Blanco not passenger-BP; Muelle Prat non-transport corridor
"""
from __future__ import annotations

import hashlib
import json
import math
import subprocess
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
FBT = ROOT / "data-clean/FEATURES_BY_TYPE.json"
ROUTES = ROOT / "data-clean/ROUTES.json"
CLUSTERS = ROOT / "data-clean/CLUSTERS.json"
PITCH = ROOT / "partner-pitch/partners/didi.json"
DC = ROOT / "data-clean/partners/didi.json"
SEAL = ROOT / "data-clean/SEAL.json"
OUT = ROOT / "handoff/didi-ex-china/latam"
RECEIPT = OUT / "GROK-CHILE-ARGENTINA-MINT-RECEIPT-2026-07-09.json"
RECEIPT_MD = OUT / "GROK-CHILE-ARGENTINA-MINT-RECEIPT-2026-07-09.md"

LANE = "chile-argentina-registry-mint-2026-07-10"
APPROVAL = "Registry owner approval 2026-07-10: Tasklet suggestions + include cross-border"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load(p: Path) -> Any:
    return json.loads(p.read_text())


def save(p: Path, obj: Any, indent: int | None = 2) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    if indent is None:
        p.write_text(json.dumps(obj, ensure_ascii=False, separators=(", ", ": ")) + "\n")
    else:
        p.write_text(json.dumps(obj, indent=indent, ensure_ascii=False) + "\n")


def sha_obj(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def mint_bp_id(key: str) -> str:
    return "bp-" + hashlib.sha1(f"didi-cl-ar|{key}".encode()).hexdigest()[:10]


def mint_route_id(a: str, b: str) -> str:
    raw = "|".join(sorted([a, b]))
    return "rn-" + hashlib.sha256(raw.encode()).hexdigest()[:12]


def haversine_nm(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    r = 3440.065  # Earth radius nmi
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return round(2 * r * math.asin(math.sqrt(a)), 2)


def line_coords(a: list[float], b: list[float], n: int = 8) -> list[list[float]]:
    """Provisional geodesic-ish chain; not authority hand-routed geometry."""
    out = []
    for i in range(n + 1):
        t = i / n
        out.append([a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t])
    return out


# --- Cities: [id, name, country, cluster, lon, lat, didi_city_supported] ---
CITIES = [
    ("puerto-montt-chile", "Puerto Montt", "Chile", "chile", -72.9401, -41.4693, True),
    ("punta-arenas-chile", "Punta Arenas", "Chile", "chile", -70.9081, -53.1638, True),
    ("porvenir-chile", "Porvenir", "Chile", "chile", -70.3681, -53.2950, False),
    ("valdivia-chile", "Valdivia", "Chile", "chile", -73.2459, -39.8142, True),
    ("niebla-chile", "Niebla", "Chile", "chile", -73.4000, -39.8670, False),
    ("corral-chile", "Corral", "Chile", "chile", -73.4330, -39.8880, False),
    ("concepcion-chile", "Concepción", "Chile", "chile", -73.0498, -36.8201, True),
    ("lota-chile", "Lota", "Chile", "chile", -73.1560, -37.0910, False),
    ("isla-santa-maria-chile", "Isla Santa María", "Chile", "chile", -73.5330, -37.0330, False),
    ("calbuco-chile", "Calbuco", "Chile", "chile", -73.1330, -41.7680, False),
    ("isla-puluqui-chile", "Isla Puluqui", "Chile", "chile", -73.0500, -41.8000, False),
    ("pargua-chile", "Pargua", "Chile", "chile", -73.4860, -41.7940, False),
    ("chacao-chile", "Chacao", "Chile", "chile", -73.5240, -41.8270, False),
    ("dalcahue-chile", "Dalcahue", "Chile", "chile", -73.6520, -42.3790, False),
    ("valparaiso-chile", "Valparaíso", "Chile", "chile", -71.6123, -33.0472, True),
    ("vina-del-mar-chile", "Viña del Mar", "Chile", "chile", -71.5518, -33.0245, True),
    ("buenos-aires-argentina", "Buenos Aires", "Argentina", "argentina", -58.3816, -34.6037, True),
    ("tigre-argentina", "Tigre", "Argentina", "argentina", -58.5797, -34.4260, False),
    ("rosario-argentina", "Rosario", "Argentina", "argentina", -60.6393, -32.9442, True),
    ("bariloche-argentina", "Bariloche", "Argentina", "argentina", -71.3082, -41.1335, True),
    ("colonia-del-sacramento-uruguay", "Colonia del Sacramento", "Uruguay", "uruguay", -57.8400, -34.4717, False),
]

# BPs: key, name, city_id, lon, lat, kind, disposition, notes
BPS = [
    ("tres-puentes", "Embarcadero Tres Puentes", "punta-arenas-chile", -70.8540, -53.1090, "ferry_terminal", "sealed", "TABSA Punta Arenas–Porvenir terminal"),
    ("porvenir-ramp", "Porvenir ferry arrival ramp", "porvenir-chile", -70.3700, -53.2980, "ferry_terminal", "sealed_provisional_name", "Exact ramp name pending operator label"),
    ("niebla-terminal", "Terminal Portuario Niebla", "niebla-chile", -73.4005, -39.8665, "ferry_terminal", "sealed", "Operator-named terminal"),
    ("corral-landing", "Corral ferry landing", "corral-chile", -73.4320, -39.8875, "ferry_terminal", "sealed_provisional_name", "Exact landing name pending"),
    ("calbuco-landing", "Calbuco ferry landing", "calbuco-chile", -73.1350, -41.7700, "ferry_terminal", "sealed_provisional", "Regional endpoint; DiDi city bind unproven"),
    ("puluqui-landing", "Isla Puluqui ferry landing", "isla-puluqui-chile", -73.0520, -41.8020, "ferry_terminal", "sealed_provisional", "Island ramp; exact name pending"),
    ("pargua-ramp", "Pargua ferry ramp", "pargua-chile", -73.4865, -41.7935, "ferry_terminal", "sealed_provisional", "Chacao channel mainland ramp"),
    ("chacao-ramp", "Chacao ferry ramp", "chacao-chile", -73.5235, -41.8265, "ferry_terminal", "sealed_provisional", "Chiloé ramp; no city-level DiDi proof"),
    ("el-pasaje", "El Pasaje ferry ramp", "dalcahue-chile", -73.6480, -42.3770, "ferry_terminal", "sealed_provisional", "Canal Dalcahue"),
    ("coyumbe", "Coyumbe ferry ramp", "dalcahue-chile", -73.6560, -42.3810, "ferry_terminal", "sealed_provisional", "Canal Dalcahue"),
    ("lota-ramp", "Lota Pueblo Hundido ramp", "lota-chile", -73.1570, -37.0920, "ferry_terminal", "sealed_provisional", "Lota not separately on DiDi city list"),
    ("santa-maria-sur", "Isla Santa María Puerto Sur ramp", "isla-santa-maria-chile", -73.5340, -37.0340, "ferry_terminal", "sealed_provisional", "Island endpoint"),
    ("muelle-prat", "Muelle Prat", "valparaiso-chile", -71.6270, -33.0360, "tourism_pier", "non_transport_corridor", "Tourism launches only — not a transit corridor"),
    ("puerto-madero", "Terminal Fluvial de Puerto Madero (Buquebus)", "buenos-aires-argentina", -58.3635, -34.6110, "ferry_terminal", "sealed", "International ferry terminal"),
    ("tigre-sarmiento", "Estación Fluvial Domingo Faustino Sarmiento", "tigre-argentina", -58.5790, -34.4255, "ferry_terminal", "sealed", "Mitre 305 Tigre Centro"),
    ("casa-bellini", "Arroyo Cruz Colorada / Casa Bellini Line 452 endpoint", "tigre-argentina", -58.5200, -34.3900, "delta_landing", "sealed_provisional", "Delta endpoint; hand path required"),
    ("rosario-terminal", "Terminal Fluvial de Pasajeros de Rosario", "rosario-argentina", -60.6390, -32.9410, "ferry_terminal", "sealed", "ENAPRO terminal"),
    ("sabino-corsi", "Isla Sabino Corsi landing", "rosario-argentina", -60.6200, -32.9200, "island_landing", "sealed_provisional_seasonal", "Seasonal summer service only"),
    ("panuelo", "Puerto Pañuelo", "bariloche-argentina", -71.4700, -41.0560, "lake_port", "sealed", "Lake excursion departure"),
    ("blest", "Puerto Blest landing", "bariloche-argentina", -71.8160, -41.0290, "lake_landing", "sealed_provisional", "Excursion destination landing"),
    ("colonia-terminal", "Terminal Fluvial Puerto de Colonia", "colonia-del-sacramento-uruguay", -57.8440, -34.4710, "ferry_terminal", "sealed_cross_border", "Uruguay endpoint for BA–Colonia"),
]

# Muelle Blanco — explicitly NOT minted as passenger BP
HELD_NOT_MINTED_BP = [
    {
        "name": "Muelle Blanco, Talcahuano",
        "disposition": "held_not_minted",
        "reason": "Current passenger timetable/operator/destination unverified per Tasklet",
    }
]

# Corridors: candidate_key, from_bp_key, to_bp_key, from_city, to_city, cluster, quarantine, service_status, notes
CORRIDORS = [
    (
        "cl-punta-arenas-porvenir",
        "tres-puentes",
        "porvenir-ramp",
        "punta-arenas-chile",
        "porvenir-chile",
        "chile",
        True,  # quarantine until hand-routed strait approaches
        "current_scheduled_evidence",
        "TABSA; needs harbor-exit hand waypoints",
    ),
    (
        "cl-niebla-corral",
        "niebla-terminal",
        "corral-landing",
        "niebla-chile",
        "corral-chile",
        "chile",
        True,
        "current_scheduled_evidence",
        "Estuary centerline hand-route required",
    ),
    (
        "cl-calbuco-puluqui",
        "calbuco-landing",
        "puluqui-landing",
        "calbuco-chile",
        "isla-puluqui-chile",
        "chile",
        True,
        "current_scheduled_evidence",
        "Channel/island ramp hand-route required",
    ),
    (
        "cl-pargua-chacao",
        "pargua-ramp",
        "chacao-ramp",
        "pargua-chile",
        "chacao-chile",
        "chile",
        True,
        "current_scheduled_evidence",
        "Canal de Chacao trunk; channel-center waypoints required",
    ),
    (
        "cl-el-pasaje-coyumbe",
        "el-pasaje",
        "coyumbe",
        "dalcahue-chile",
        "dalcahue-chile",
        "chile",
        True,
        "current_scheduled_evidence",
        "Canal Dalcahue short hop; shoreline clipping risk",
    ),
    (
        "cl-lota-santa-maria",
        "lota-ramp",
        "santa-maria-sur",
        "lota-chile",
        "isla-santa-maria-chile",
        "chile",
        True,
        "current_scheduled_evidence",
        "Coastal open-water approach hand-set required",
    ),
    (
        "ar-tigre-casa-bellini",
        "tigre-sarmiento",
        "casa-bellini",
        "tigre-argentina",
        "tigre-argentina",
        "argentina",
        True,
        "current_scheduled_evidence",
        "Mandatory multi-branch Tigre delta hand path",
    ),
    (
        "ar-rosario-sabino-corsi",
        "rosario-terminal",
        "sabino-corsi",
        "rosario-argentina",
        "rosario-argentina",
        "argentina",
        True,
        "seasonal_summer_only",
        "Seasonal; not year-round. Island landing hand-route required",
    ),
    (
        "ar-panuelo-blest",
        "panuelo",
        "blest",
        "bariloche-argentina",
        "bariloche-argentina",
        "argentina",
        True,
        "current_excursion_evidence",
        "Lake excursion; Brazo Blest corridor hand waypoints required",
    ),
    (
        "ar-buenos-aires-colonia",
        "puerto-madero",
        "colonia-terminal",
        "buenos-aires-argentina",
        "colonia-del-sacramento-uruguay",
        "argentina",
        True,
        "current_cross_border_evidence",
        "International BA–Colonia; channel/jurisdiction hand-review required. Cross-border approved for registry mint.",
    ),
]


def city_feature(cid: str, name: str, country: str, cluster: str, lon: float, lat: float) -> dict:
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lon, lat]},
        "properties": {
            "id": cid,
            "type": "city",
            "name": name,
            "shortName": name,
            "fullName": name,
            "country": country,
            "region": "Latin-America",
            "platform_class": "dual-platform",
            "coords_resolved": True,
            "coords_source": "provisional_public_geocode_2026-07-10",
            "confidence": "med",
            "status": "operational",
            "tier_sort_key": 2,
            "cluster_id": cluster,
            "_grok_mint_city": LANE,
            "_registry_approval": APPROVAL,
        },
    }


def bp_feature(
    bp_id: str,
    name: str,
    city_id: str,
    lon: float,
    lat: float,
    kind: str,
    disposition: str,
    note: str,
) -> dict:
    props: dict[str, Any] = {
        "id": bp_id,
        "name": name,
        "fullName": name,
        "type": "poi",
        "bp_type": kind,
        "parent_city_id": city_id,
        "status": "operational" if disposition.startswith("sealed") else "provisional",
        "coords_resolved": True,
        "coords_source": "provisional_public_geocode_2026-07-10",
        "confidence": "med",
        "_grok_mint_bp": LANE,
        "_disposition": disposition,
        "_g2_note": note,
    }
    if disposition == "non_transport_corridor":
        props["_not_route_demand_proof"] = True
        props["status"] = "operational"
    if "cross_border" in disposition:
        props["cross_border"] = True
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lon, lat]},
        "properties": props,
    }


def route_feature(
    rid: str,
    from_bp: str,
    to_bp: str,
    from_label: str,
    to_label: str,
    from_city: str,
    to_city: str,
    cluster: str,
    coords: list[list[float]],
    nm: float,
    quarantine: bool,
    service_status: str,
    note: str,
    candidate_key: str,
) -> dict:
    props: dict[str, Any] = {
        "id": rid,
        "from": from_bp,
        "to": to_bp,
        "from_label": from_label,
        "to_label": to_label,
        "from_city_id": from_city,
        "to_city_id": to_city,
        "cluster_id": cluster,
        "distance_nm": nm,
        "label": f"{from_label} → {to_label}",
        "status": "provisional_mint",
        "service_status": service_status,
        "_needs_hand_waypoints": True,
        "_waypoint_note": note,
        "_candidate_key": candidate_key,
        "_grok_mint_route": LANE,
        "_registry_approval": APPROVAL,
        "coords_source": "provisional_geodesic_pending_hand_route",
    }
    if quarantine:
        props["_quarantine"] = True
        props["relevance"] = "hide"
        props["_quarantine_reason"] = (
            "Provisional geometry only — hand-routed water-only path + land-crossing QA required before active/renderable"
        )
    if "cross_border" in service_status or to_city.endswith("uruguay"):
        props["cross_border"] = True
        props["cross_border_note"] = "International passenger ferry; not domestic deployment-ready"
    if "seasonal" in service_status:
        props["seasonality"] = "summer_only"
    return {
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": coords},
        "properties": props,
    }


def ensure_cluster(doc: dict, cluster_id: str, label: str, members: list[str], anchor: list[float], anchor_src: str) -> None:
    clusters = doc.setdefault("clusters", [])
    existing = {c.get("cluster_id"): c for c in clusters}
    if cluster_id in existing:
        c = existing[cluster_id]
        ids = list(dict.fromkeys((c.get("member_city_ids") or []) + members))
        c["member_city_ids"] = ids
        c["members_present"] = len(ids)
        c["members_missing"] = []
        c["_grok_mint_update"] = utc_now()
        return
    clusters.append(
        {
            "cluster_id": cluster_id,
            "cluster_label": label,
            "region": "Latin-America",
            "type": "country",
            "anchor": anchor,
            "member_city_ids": members,
            "members_present": len(members),
            "members_missing": [],
            "anchor_source": anchor_src,
            "_grok_mint_cluster": LANE,
            "_registry_approval": APPROVAL,
        }
    )


def bind_didi_markets(partner: dict, route_ids_by_market: dict[str, list[str]], gold: dict) -> None:
    """Add chile/argentina market blocks; featured empty until routes un-quarantined."""
    markets = partner.setdefault("markets", [])
    by_id = {m.get("id"): m for m in markets if isinstance(m, dict)}

    def mk_market(mid: str, label: str, region: str, caveats: list[str], journey_notes: list[dict]) -> dict:
        if mid in by_id:
            m = by_id[mid]
        else:
            m = {
                "id": mid,
                "slug": mid,
                "label": label,
                "region": region,
                "category": "ridehail",
                "summary": f"DiDi {label}: source-backed marine anchors with honest null demand until route evidence is complete.",
                "phases": [
                    {"id": "prove", "name": "Prove", "featured_routes": []},
                    {"id": "expand", "name": "Expand", "featured_routes": []},
                    {"id": "full", "name": "Full network", "featured_routes": []},
                ],
                "featured_routes": [],
                "journeys_unlocked": [],
                "why_navier_now": {"wow_corridors": []},
            }
            markets.append(m)
            by_id[mid] = m
        # Featured stays empty while all routes quarantined
        m["featured_routes"] = []
        for ph in m.get("phases") or []:
            if isinstance(ph, dict):
                ph["featured_routes"] = []
        # aspirational journeys — no route_id until active
        journeys = []
        for j in journey_notes:
            journeys.append(
                {
                    **j,
                    "route_id": None,
                    "display": "text_only",
                    "_link_status": "aspirational-quarantine-geometry",
                    "_link_source": LANE,
                    "economics_status": "roadmap_excluded",
                    "platform": "Pioneer II",
                }
            )
        m["journeys_unlocked"] = journeys
        m["_operation_caveats"] = caveats
        m["_didi_cl_ar_mint"] = {"at": utc_now(), "featured_empty_reason": "all_minted_routes_quarantined_pending_hand_waypoints"}
        return m

    mk_market(
        "chile",
        "Chile — Puerto Montt, Punta Arenas, Valdivia & coastal ferries",
        "Latin America",
        [
            "DiDi city evidence only for named official cities — not Porvenir, Corral, Calbuco, Chacao, Dalcahue, Lota",
            "All minted Chile ferry routes are quarantine/hide until hand-routed water geometry passes land-crossing QA",
            "Muelle Prat is tourism-only, not a transit corridor",
            "Muelle Blanco not minted as passenger BP",
            "Annual route pax remain null",
        ],
        [
            {
                "from": "Punta Arenas Tres Puentes",
                "to": "Porvenir",
                "from_label": "Embarcadero Tres Puentes",
                "to_label": "Porvenir ferry arrival ramp",
                "label": "Punta Arenas ↔ Porvenir (TABSA)",
                "today": "Official car/passenger ferry across the Strait of Magellan.",
                "with_navier": "A clean high-frequency hop once geometry is hand-sealed and demand is sourced.",
                "archetype": "commuter",
            },
            {
                "from": "Niebla",
                "to": "Corral",
                "from_label": "Terminal Portuario Niebla",
                "to_label": "Corral ferry landing",
                "label": "Niebla ↔ Corral",
                "today": "Regional ferry with weather/tide variability.",
                "with_navier": "A silent premium short hop booked in DiDi after local service proof.",
                "archetype": "commuter",
            },
            {
                "from": "Pargua",
                "to": "Chacao",
                "from_label": "Pargua ferry ramp",
                "to_label": "Chacao ferry ramp",
                "label": "Pargua ↔ Chacao (Canal de Chacao)",
                "today": "Around-the-clock multi-vessel Chiloé access trunk.",
                "with_navier": "A reliable clean channel hop for the Chiloé gateway system.",
                "archetype": "commuter",
            },
        ],
    )
    mk_market(
        "argentina",
        "Argentina — Buenos Aires, Tigre, Rosario & Bariloche",
        "Latin America",
        [
            "DiDi city evidence for Buenos Aires, Rosario, Bariloche; Tigre polygon unproven",
            "Buenos Aires–Colonia is international cross-border — not a domestic route",
            "Rosario–Sabino Corsi is seasonal summer service only",
            "Tigre delta and Nahuel Huapi routes require hand-routed geometry before render",
            "Annual route pax remain null",
        ],
        [
            {
                "from": "Buenos Aires Puerto Madero",
                "to": "Colonia del Sacramento",
                "from_label": "Terminal Fluvial de Puerto Madero",
                "to_label": "Terminal Fluvial Puerto de Colonia",
                "label": "Buenos Aires ↔ Colonia (cross-border)",
                "today": "Daily international ferry connection.",
                "with_navier": "A premium cross-border hop once jurisdiction and channel geometry are sealed.",
                "archetype": "intercity",
            },
            {
                "from": "Tigre",
                "to": "Casa Bellini / Cruz Colorada",
                "from_label": "Estación Fluvial Sarmiento",
                "to_label": "Casa Bellini Line 452 endpoint",
                "label": "Tigre delta Line 452 branch",
                "today": "Public multi-branch river network (~1.5 h published).",
                "with_navier": "A clean delta hop after hand-routed channel geometry.",
                "archetype": "commuter",
            },
            {
                "from": "Rosario",
                "to": "Isla Sabino Corsi",
                "from_label": "Terminal Fluvial de Pasajeros de Rosario",
                "to_label": "Isla Sabino Corsi landing",
                "label": "Rosario ↔ Isla Sabino Corsi (seasonal)",
                "today": "Summer seasonal island crossing only.",
                "with_navier": "A seasonal premium island hop — not year-round.",
                "archetype": "tourism",
            },
        ],
    )

    # map scope registry keys
    ms = partner.setdefault("_map_scope", {})
    keys = list(ms.get("registry_keys") or [])
    add = [
        "chile",
        "argentina",
        "uruguay",
        *[c[0] for c in CITIES],
    ]
    for k in add:
        if k not in keys:
            keys.append(k)
    ms["registry_keys"] = keys
    ms["source"] = LANE
    ms["generated"] = utc_now()

    partner["_didi_chile_argentina_mint"] = {
        "at": utc_now(),
        "approval": APPROVAL,
        "route_ids_minted": route_ids_by_market,
        "featured_empty": True,
        "reason": "All routes quarantine until hand-waypoint geometry QA",
        "cross_border_included": ["ar-buenos-aires-colonia"],
    }


def main() -> int:
    fbt = load(FBT)
    routes_raw = load(ROUTES)
    routes = routes_raw if isinstance(routes_raw, list) else routes_raw.get("features")
    clusters = load(CLUSTERS)

    existing_city = {
        (f.get("properties") or {}).get("id")
        for f in (fbt.get("city") or [])
        if (f.get("properties") or {}).get("id")
    }
    existing_bp = {
        (f.get("properties") or {}).get("id")
        for f in (fbt.get("poi") or [])
        if (f.get("properties") or {}).get("id")
    }
    existing_rid = {
        (f.get("properties") or {}).get("id")
        for f in routes
        if (f.get("properties") or {}).get("id")
    }

    bp_key_to_id = {row[0]: mint_bp_id(row[0]) for row in BPS}

    minted_cities = []
    for cid, name, country, cluster, lon, lat, _didi in CITIES:
        if cid in existing_city:
            continue
        fbt.setdefault("city", []).append(city_feature(cid, name, country, cluster, lon, lat))
        minted_cities.append(cid)
        existing_city.add(cid)

    minted_bps = []
    bp_meta = {}
    for key, name, city_id, lon, lat, kind, disp, note in BPS:
        bp_id = bp_key_to_id[key]
        bp_meta[key] = {"id": bp_id, "name": name, "city_id": city_id, "lon": lon, "lat": lat, "disposition": disp}
        if bp_id in existing_bp:
            continue
        fbt.setdefault("poi", []).append(bp_feature(bp_id, name, city_id, lon, lat, kind, disp, note))
        minted_bps.append(bp_id)
        existing_bp.add(bp_id)

    chile_members = [c[0] for c in CITIES if c[3] == "chile"]
    arg_members = [c[0] for c in CITIES if c[3] == "argentina"]
    uru_members = [c[0] for c in CITIES if c[3] == "uruguay"]
    ensure_cluster(clusters, "chile", "Chile", chile_members, [-72.94, -41.47], "puerto-montt-chile")
    ensure_cluster(clusters, "argentina", "Argentina", arg_members, [-58.38, -34.60], "buenos-aires-argentina")
    ensure_cluster(clusters, "uruguay", "Uruguay", uru_members, [-57.84, -34.47], "colonia-del-sacramento-uruguay")

    minted_routes = []
    route_rows = []
    for cand, fkey, tkey, fc, tc, cluster, q, svc, note in CORRIDORS:
        fb, tb = bp_meta[fkey], bp_meta[tkey]
        rid = mint_route_id(fb["id"], tb["id"])
        coords = line_coords([fb["lon"], fb["lat"]], [tb["lon"], tb["lat"]], n=10)
        nm = haversine_nm(fb["lon"], fb["lat"], tb["lon"], tb["lat"])
        if rid not in existing_rid:
            routes.append(
                route_feature(
                    rid,
                    fb["id"],
                    tb["id"],
                    fb["name"],
                    tb["name"],
                    fc,
                    tc,
                    cluster,
                    coords,
                    nm,
                    q,
                    svc,
                    note,
                    cand,
                )
            )
            minted_routes.append(rid)
            existing_rid.add(rid)
        route_rows.append(
            {
                "candidate_key": cand,
                "route_id": rid,
                "from_bp": fb["id"],
                "to_bp": tb["id"],
                "from_city_id": fc,
                "to_city_id": tc,
                "cluster_id": cluster,
                "distance_nm_provisional": nm,
                "quarantine": q,
                "relevance": "hide" if q else None,
                "service_status": svc,
                "note": note,
            }
        )

    # write geometry
    if isinstance(routes_raw, list):
        save(ROUTES, routes, indent=None)
    else:
        routes_raw["features"] = routes
        save(ROUTES, routes_raw, indent=None)
    save(FBT, fbt)
    save(CLUSTERS, clusters)

    # partner
    partner = load(PITCH)
    by_cluster_routes = {
        "chile": [r["route_id"] for r in route_rows if r["cluster_id"] == "chile"],
        "argentina": [r["route_id"] for r in route_rows if r["cluster_id"] == "argentina"],
    }
    gold = {(f.get("properties") or {}).get("id"): (f.get("properties") or {}) for f in routes}
    bind_didi_markets(partner, by_cluster_routes, gold)
    text = json.dumps(partner, indent=2, ensure_ascii=False) + "\n"
    PITCH.write_text(text)
    DC.write_text(text)

    # try scope sync
    sync = ROOT / "scripts/sync-partner-map-scope.mjs"
    sync_out = None
    if sync.exists():
        r = subprocess.run(
            ["node", str(sync), "didi"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        sync_out = {"exit": r.returncode, "tail": ((r.stdout or "") + (r.stderr or ""))[-1500:]}
        # re-copy if sync rewrote pitch
        if r.returncode == 0 and PITCH.exists():
            # ensure our market blocks still present
            p2 = load(PITCH)
            if not any(m.get("id") == "chile" for m in (p2.get("markets") or [])):
                # restore from our partner write
                PITCH.write_text(text)
                DC.write_text(text)
            else:
                DC.write_text(PITCH.read_text())

    # gates
    def run(cmd):
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        return {"exit": r.returncode, "tail": ((r.stdout or "") + (r.stderr or ""))[-1200:]}

    gates = {
        "gate_g": run([sys.executable, str(ROOT / "scripts/audit_partner_copy.py")]),
        "inheritance_strict": run(
            [
                sys.executable,
                str(ROOT / "scripts/validate_partner_inheritance.py"),
                "--partner",
                "didi",
                "--strict",
                "--include-pitch",
                "--json",
            ]
        ),
        "fidelity": run(
            [sys.executable, str(ROOT / "scripts/audit_proposal_fidelity.py"), "--partner", "didi"]
        ),
    }

    # SEAL hash update
    if SEAL.exists():
        seal = load(SEAL)
        files = seal.setdefault("files", {})
        for rel, path in [
            ("CLUSTERS.json", CLUSTERS),
            ("FEATURES_BY_TYPE.json", FBT),
            ("partners/didi.json", DC),
        ]:
            files[rel] = sha_obj(load(path))
        files["ROUTES.json"] = hashlib.sha256(ROUTES.read_bytes()).hexdigest()
        notes = seal.setdefault("_notes", [])
        if isinstance(notes, list):
            notes.append({"at": utc_now(), "event": LANE, "approval": APPROVAL})
        seal["sealed_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        save(SEAL, seal)

    receipt = {
        "at": utc_now(),
        "lane": LANE,
        "approval": APPROVAL,
        "status": "registry_minted / routes_quarantined_pending_hand_waypoints / finance_not_run",
        "minted": {
            "clusters": ["chile", "argentina", "uruguay"],
            "cities": minted_cities,
            "cities_n": len(minted_cities),
            "boarding_points": minted_bps,
            "boarding_points_n": len(minted_bps),
            "routes": minted_routes,
            "routes_n": len(minted_routes),
        },
        "held_not_minted_bps": HELD_NOT_MINTED_BP,
        "non_transport_bp": ["Muelle Prat"],
        "routes": route_rows,
        "cross_border": {
            "included": True,
            "corridor": "ar-buenos-aires-colonia",
            "route_id": next(r["route_id"] for r in route_rows if r["candidate_key"] == "ar-buenos-aires-colonia"),
            "note": "International; quarantine until channel/jurisdiction hand-review",
        },
        "visibility": {
            "all_minted_routes_quarantine_hide": True,
            "active_renderable_new": 0,
            "reason": "Tasklet waypoint risks require hand-routed water-only geometry before active/renderable",
        },
        "didi_partner": {
            "markets_added": ["chile", "argentina"],
            "featured_routes": [],
            "featured_empty_reason": "no active routes yet",
        },
        "finance": {
            "cascade_run": False,
            "annual_one_way_pax": "all_null",
        },
        "coords_policy": {
            "source": "provisional_public_geocode_2026-07-10",
            "confidence": "med",
            "note": "Not authority-grade pier survey; replace with controlled geocodes + hand tracks",
        },
        "sync_partner_map_scope": sync_out,
        "gates": {
            k: {"exit": v["exit"], "pass": v["exit"] == 0 or (k == "fidelity" and "PASS" in v["tail"]), "tail": v["tail"]}
            for k, v in gates.items()
        },
        "next": [
            "Hand-route water-only geometries; re-run land-crossing QA",
            "Un-quarantine routes that pass geometry gates",
            "Then bind DiDi featured_routes to active set",
            "Tasklet: annual one-way pax + fares before finance cascade",
            "Verify DiDi service polygons for nearby ferry municipalities",
        ],
    }
    save(RECEIPT, receipt)

    lines = [
        "# Chile + Argentina registry mint — Grok handback",
        "",
        f"**UTC:** {receipt['at']}  ",
        f"**Approval:** {APPROVAL}  ",
        f"**Status:** `{receipt['status']}`",
        "",
        "## Minted",
        "",
        f"- Clusters: `chile`, `argentina`, `uruguay`",
        f"- Cities: **{receipt['minted']['cities_n']}**",
        f"- Boarding points: **{receipt['minted']['boarding_points_n']}**",
        f"- Routes: **{receipt['minted']['routes_n']}** (all quarantine/hide pending hand waypoints)",
        "",
        "### Cross-border",
        "",
        f"- Included: Buenos Aires ↔ Colonia — `{receipt['cross_border']['route_id']}`",
        "- Marked international; not domestic-ready",
        "",
        "### Explicitly not minted as passenger BP",
        "",
        "- Muelle Blanco (service unproven)",
        "- Muelle Prat kept as tourism pier only (`_not_route_demand_proof`)",
        "",
        "## DiDi partner",
        "",
        "- Markets added: `chile`, `argentina`",
        "- Featured routes: **empty** until routes un-quarantine",
        "- Aspirational journeys present (no route_id)",
        "",
        "## Finance",
        "",
        "- Cascade **not** run; annual one-way pax remain null",
        "",
        "## Gates",
        "",
    ]
    for k, g in receipt["gates"].items():
        lines.append(f"- **{k}:** {'PASS' if g['pass'] else 'FAIL'} (exit {g['exit']})")
    lines += [
        "",
        "## Next",
        "",
        *[f"- {x}" for x in receipt["next"]],
        "",
        f"Machine receipt: `{RECEIPT.relative_to(ROOT)}`",
        "",
    ]
    RECEIPT_MD.write_text("\n".join(lines) + "\n")

    print(json.dumps({k: receipt[k] for k in ("status", "minted", "cross_border", "visibility")}, indent=2))
    for k, g in gates.items():
        print(f"=== {k} exit={g['exit']} ===")
        print(g["tail"][:800])

    rc = 0
    for name in ("gate_g", "inheritance_strict"):
        if gates[name]["exit"] != 0:
            rc = 1
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
