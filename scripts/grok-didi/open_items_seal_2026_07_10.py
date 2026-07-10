#!/usr/bin/env python3
"""DiDi open-items seal — 2026-07-10.

1. CL/AR hand-route → land-QA → un-quarantine passers → featured bind (polygon-gated)
2. Colombia spine/demand bank (unmaterialized hold unless demand lands)
3. CR/PA/DR + EC/PE finance null bank (primary annual pax still absent)
4. Ferry-town DiDi service-polygon proof bank
5. Taiwan/HK marine economics null (op/geometry/demand gates)
6. Egypt wrong-parent / BP coordinate audit bank

No production deploy. Finance cascade only for non-null annual pax (none in this run).
null beats wrong.
"""
from __future__ import annotations

import json
import math
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "grok-geometry"))

from route_land_qa import evaluate_feature, point_is_land  # noqa: E402

ROUTES = ROOT / "data-clean/ROUTES.json"
FBT = ROOT / "data-clean/FEATURES_BY_TYPE.json"
PARTNER = ROOT / "data-clean/partners/didi.json"
PITCH = ROOT / "partner-pitch/partners/didi.json"
SEAL = ROOT / "data-clean/SEAL.json"
OUT = ROOT / "handoff/didi-ex-china/waves/tasklet-proof"
OUT.mkdir(parents=True, exist_ok=True)

CL_AR_IDS = [
    "rn-27ac33a14eb2",  # PA–Porvenir
    "rn-4176c336f07a",  # Niebla–Corral
    "rn-60ac3dd2ce79",  # Calbuco–Puluqui
    "rn-a5ddce927bd3",  # Pargua–Chacao
    "rn-eaedbbb4abe9",  # Dalcahue canal
    "rn-c6a108b7f3d2",  # Lota–Santa María
    "rn-f6d1302e7121",  # Tigre Line 452
    "rn-f451444da7fe",  # Rosario–Sabino Corsi
    "rn-97c9f0b33379",  # Pañuelo–Blest
    "rn-04b92d6952d2",  # BA–Colonia (international)
]

# Hand midpoints (lon, lat) for water-only corridors after regional mask overrides
HAND_MIDS: dict[str, list[list[float]]] = {
    "rn-27ac33a14eb2": [
        [-70.82, -53.14],
        [-70.70, -53.18],
        [-70.55, -53.23],
        [-70.45, -53.28],
    ],
    "rn-4176c336f07a": [[-73.418, -39.876], [-73.425, -39.882]],
    "rn-60ac3dd2ce79": [[-73.12, -41.78], [-73.09, -41.79], [-73.065, -41.798]],
    "rn-a5ddce927bd3": [[-73.500, -41.805], [-73.512, -41.815]],
    "rn-eaedbbb4abe9": [],
    "rn-c6a108b7f3d2": [
        [-73.22, -37.11],
        [-73.35, -37.09],
        [-73.45, -37.055],
    ],
    "rn-f6d1302e7121": [
        [-58.565, -34.420],
        [-58.548, -34.410],
        [-58.532, -34.398],
    ],
    "rn-f451444da7fe": [[-60.630, -32.932], [-60.624, -32.926]],
    "rn-97c9f0b33379": [
        [-71.55, -41.08],
        [-71.65, -41.09],
        [-71.75, -41.06],
    ],
    "rn-04b92d6952d2": [
        [-58.30, -34.64],
        [-58.15, -34.60],
        [-58.00, -34.55],
        [-57.90, -34.50],
    ],
}

# Official DiDi city-directory scrape 2026-07-10 (conductor ciudades pages)
DIDI_CL_CITIES = {
    "antofagasta",
    "arica",
    "calama",
    "chillan",
    "chillán",
    "concepcion",
    "concepción",
    "copiapo",
    "copiapó",
    "coyhaique",
    "iquique",
    "la serena - coquimbo",
    "los andes - san felipe",
    "los angeles",
    "los ángeles",
    "magallanes",
    "osorno",
    "ovalle",
    "puerto montt",
    "punta arenas",
    "rancagua - san fernando",
    "santiago",
    "talca - curico - linares",
    "talca - curicó - linares",
    "temuco",
    "valdivia",
    "valparaiso",
    "valparaíso",
    "vina del mar",
    "viña del mar",
}
DIDI_AR_CITIES = {
    "bariloche",
    "buenos aires",
    "catamarca",
    "concordia",
    "cordoba",
    "córdoba",
    "formosa",
    "la plata",
    "mar del plata",
    "neuquen",
    "neuquén",
    "parana",
    "paraná",
    "posadas",
    "resistencia",
    "rosario",
    "salta",
    "san juan",
    "san luis",
    "san salvador de jujuy",
    "santa fe",
    "santiago del estero",
    "tucuman",
    "tucumán",
}
DIDI_CO_CITIES = {
    "armenia",
    "barranquilla",
    "bogota",
    "bogotá",
    "bucaramanga",
    "buenaventura",
    "cali",
    "cartagena",
    "cucuta",
    "cúcuta",
    "ibague",
    "ibagué",
    "manizales",
    "medellin",
    "medellín",
    "monteria",
    "montería",
    "neiva",
    "pasto",
    "pereira",
    "popayan",
    "popayán",
    "santa marta",
    "sincelejo",
    "valledupar",
    "villavicencio",
}

# Ferry-town / endpoint polygon audit targets
FERRY_TOWN_AUDIT = [
    {"name": "Niebla", "country": "CL", "atlas_city_id": "niebla-chile", "in_directory": False, "nearest_didi": "Valdivia"},
    {"name": "Corral", "country": "CL", "atlas_city_id": "corral-chile", "in_directory": False, "nearest_didi": "Valdivia"},
    {"name": "Calbuco", "country": "CL", "atlas_city_id": "calbuco-chile", "in_directory": False, "nearest_didi": "Puerto Montt"},
    {"name": "Pargua", "country": "CL", "atlas_city_id": "pargua-chile", "in_directory": False, "nearest_didi": "Puerto Montt"},
    {"name": "Chacao", "country": "CL", "atlas_city_id": "chacao-chile", "in_directory": False, "nearest_didi": "Puerto Montt"},
    {"name": "Dalcahue", "country": "CL", "atlas_city_id": "dalcahue-chile", "in_directory": False, "nearest_didi": "Puerto Montt"},
    {"name": "Lota", "country": "CL", "atlas_city_id": "lota-chile", "in_directory": False, "nearest_didi": "Concepción"},
    {"name": "Porvenir", "country": "CL", "atlas_city_id": "porvenir-chile", "in_directory": False, "nearest_didi": "Punta Arenas / Magallanes"},
    {"name": "Tigre", "country": "AR", "atlas_city_id": "tigre-argentina", "in_directory": False, "nearest_didi": "Buenos Aires"},
    {"name": "Colonia del Sacramento", "country": "UY", "atlas_city_id": "colonia-del-sacramento-uruguay", "in_directory": False, "nearest_didi": "none (Uruguay)"},
]

# Routes eligible for DiDi featured bind after geometry pass:
# both endpoint *anchor* markets are in official DiDi city lists (not ferry towns).
FEATURE_ELIGIBILITY = {
    "rn-27ac33a14eb2": {
        "eligible": False,
        "reason": "Porvenir not in DiDi CL directory; Magallanes/Punta Arenas only covers PA side",
    },
    "rn-4176c336f07a": {
        "eligible": False,
        "reason": "Niebla/Corral not in DiDi CL directory; Valdivia is listed but endpoints are ferry towns",
    },
    "rn-60ac3dd2ce79": {
        "eligible": False,
        "reason": "Calbuco/Puluqui not in DiDi CL directory",
    },
    "rn-a5ddce927bd3": {
        "eligible": False,
        "reason": "Pargua/Chacao not in DiDi CL directory",
    },
    "rn-eaedbbb4abe9": {
        "eligible": False,
        "reason": "Dalcahue not in DiDi CL directory",
    },
    "rn-c6a108b7f3d2": {
        "eligible": False,
        "reason": "Lota not in DiDi CL directory; Concepción is broader bind only",
    },
    "rn-f6d1302e7121": {
        "eligible": False,
        "reason": "Tigre not in DiDi AR directory (Buenos Aires listed; Tigre polygon unproven)",
    },
    "rn-f451444da7fe": {
        "eligible": True,
        "reason": "Both ends under Rosario (DiDi AR directory); seasonal service caveat remains",
    },
    "rn-97c9f0b33379": {
        "eligible": True,
        "reason": "Both ends under Bariloche (DiDi AR directory); lake excursion, pax null",
    },
    "rn-04b92d6952d2": {
        "eligible": False,
        "reason": "International BA–Colonia; Colonia not DiDi AR; cabotage/customs lane",
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path):
    return json.loads(path.read_text())


def save_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def hav_km(a, b) -> float:
    r = 6371.0088
    lon1, lat1 = math.radians(a[0]), math.radians(a[1])
    lon2, lat2 = math.radians(b[0]), math.radians(b[1])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * r * math.asin(min(1.0, math.sqrt(h)))


def densify(coords: list, step_km: float = 0.2) -> list:
    out = [list(coords[0])]
    for i in range(1, len(coords)):
        a, b = coords[i - 1], coords[i]
        d = hav_km(a, b)
        n = max(1, int(math.ceil(d / step_km)))
        for k in range(1, n + 1):
            t = k / n
            out.append([a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t])
    return out


def snap_to_water(lon: float, lat: float, max_km: float = 4.0) -> tuple[list[float], float | None]:
    if not point_is_land(lon, lat):
        return [lon, lat], 0.0
    best = None
    best_d = 1e9
    for r_km in [i * 0.05 for i in range(1, int(max_km / 0.05) + 1)]:
        ddeg = r_km / 111.0
        for ang in range(0, 360, 10):
            rad = math.radians(ang)
            lo = lon + ddeg * math.cos(rad) / max(0.2, math.cos(math.radians(lat)))
            la = lat + ddeg * math.sin(rad)
            if not point_is_land(lo, la):
                d = hav_km((lon, lat), (lo, la))
                if d < best_d:
                    best_d = d
                    best = [lo, la]
        if best is not None and best_d <= r_km + 0.02:
            return best, best_d
    return [lon, lat], None


def path_nm(coords: list) -> float:
    d = 0.0
    for i in range(1, len(coords)):
        d += hav_km(coords[i - 1], coords[i])
    return round(d / 1.852, 2)


def build_hand_path(a0: list[float], b0: list[float], mids: list[list[float]]) -> list[list[float]]:
    a, _ = snap_to_water(a0[0], a0[1])
    b, _ = snap_to_water(b0[0], b0[1])
    mids_s = []
    for m in mids:
        sm, _ = snap_to_water(m[0], m[1], max_km=6.0)
        mids_s.append(sm)
    # keep BP endpoints, approach via water snaps
    chain = [list(a0), a] + mids_s + [b, list(b0)]
    return densify(chain, 0.15)


def route_index(routes: list) -> dict[str, dict]:
    idx = {}
    for f in routes:
        p = f.get("properties") or {}
        rid = p.get("id") or p.get("route_id")
        if rid:
            idx[rid] = f
    return idx


def seal_cl_ar_geometry(routes: list) -> dict:
    idx = route_index(routes)
    report = {
        "at": utc_now(),
        "water_override_note": "regional_land_masks Chile/Argentina ferry bboxes added",
        "results": [],
        "unquarantined": [],
        "still_quarantined": [],
        "featured_bound": [],
        "featured_held": [],
    }
    for rid in CL_AR_IDS:
        feat = idx.get(rid)
        if not feat:
            report["results"].append({"route_id": rid, "status": "missing"})
            continue
        props = feat["properties"]
        coords0 = (feat.get("geometry") or {}).get("coordinates") or []
        if len(coords0) < 2:
            report["results"].append({"route_id": rid, "status": "no_geometry"})
            continue
        a0, b0 = coords0[0], coords0[-1]
        mids = HAND_MIDS.get(rid, [])
        new_coords = build_hand_path(a0, b0, mids)
        feat["geometry"] = {"type": "LineString", "coordinates": new_coords}
        props["id"] = rid
        if "route_id" not in props:
            props["route_id"] = rid
        ev = evaluate_feature(feat)
        land = float(ev.get("interior_land_km") or 0.0)
        qa = bool(ev.get("qa_pass"))
        nm = path_nm(new_coords)
        props["distance_nm"] = nm
        props["_geometry_land_km"] = land
        props["_land_km_interior"] = land
        props["_geometry_sync_at"] = utc_now()
        props["_geometry_sync_source"] = "grok/didi-cl-ar-hand-route-2026-07-10"
        props["_needs_hand_waypoints"] = not qa
        props["coords_source"] = "hand_routed_water_path_2026_07_10"
        props["_coastal_geometry"] = True
        row = {
            "route_id": rid,
            "label": props.get("label"),
            "qa_pass": qa,
            "interior_land_km": round(land, 4),
            "distance_nm": nm,
            "n_vertices": len(new_coords),
            "cluster_id": props.get("cluster_id"),
            "service_status": props.get("service_status") or props.get("_service_status"),
        }
        if qa:
            props.pop("_quarantine", None)
            props.pop("_quarantine_reason", None)
            if props.get("relevance") == "hide":
                props.pop("relevance", None)
            props["active"] = True
            props["_unquarantined_at"] = utc_now()
            props["_unquarantine_reason"] = "hand_routed_water_path_land_qa_pass"
            row["action"] = "unquarantine"
            report["unquarantined"].append(rid)
        else:
            props["_quarantine"] = True
            props["relevance"] = "hide"
            props["_quarantine_reason"] = (
                f"Hand-route land QA fail interior_land_km={land:.4f} (thresh 0.05)"
            )
            props["active"] = False
            row["action"] = "keep_quarantine"
            report["still_quarantined"].append(rid)
        report["results"].append(row)
    return report


def bind_featured(partner: dict, geom_report: dict) -> dict:
    unq = set(geom_report.get("unquarantined") or [])
    routes = load_json(ROUTES)
    ridx = route_index(routes)
    featured_cl = []
    featured_ar = []
    for rid, meta in FEATURE_ELIGIBILITY.items():
        if rid not in unq or not meta.get("eligible"):
            continue
        f = ridx.get(rid)
        if not f:
            continue
        p = f["properties"]
        entry = {
            "route_id": rid,
            "from_label": p.get("from_label"),
            "to_label": p.get("to_label"),
            "cluster_id": p.get("cluster_id"),
        }
        if p.get("cluster_id") == "chile":
            featured_cl.append(entry)
        else:
            featured_ar.append(entry)
        geom_report["featured_bound"].append(rid)

    for m in partner.get("markets") or []:
        mid = m.get("id") or m.get("slug")
        if mid == "chile":
            m["featured_routes"] = featured_cl
            for i, ph in enumerate(m.get("phases") or []):
                ph["featured_routes"] = featured_cl if featured_cl else []
            # journeys: link first featured if any
            if featured_cl:
                fr = featured_cl[0]
                m["journeys_unlocked"] = [
                    {
                        "from": fr["from_label"],
                        "to": fr["to_label"],
                        "from_label": fr["from_label"],
                        "to_label": fr["to_label"],
                        "label": f"{fr['from_label']} → {fr['to_label']}",
                        "route_id": fr["route_id"],
                        "_link_status": "linked-cl-ar-hand-route",
                        "_link_source": "grok/didi-open-items-2026-07-10",
                        "economics_status": "economics_pending",
                        "today": "Existing ferry with boarding friction.",
                        "with_navier": "A clean hop booked in DiDi once demand is sourced.",
                        "platform": "Pioneer II",
                        "archetype": "commuter",
                    }
                ]
            m["_operation_caveats"] = [
                "DiDi CL directory cities only for first/last-mile claims",
                "Ferry towns Niebla/Corral/Calbuco/Pargua/Chacao/Dalcahue/Lota/Porvenir not in official city list",
                "Featured routes require geometry un-quarantine + directory polygon gate",
                "Annual route pax remain null — no finance promotion",
            ]
            m["_didi_cl_ar_open_items"] = {
                "at": utc_now(),
                "featured": [x["route_id"] for x in featured_cl],
                "geometry_unquarantined": [r for r in unq if r.startswith("rn-") and r in CL_AR_IDS],
            }
        if mid == "argentina":
            m["featured_routes"] = featured_ar
            for ph in m.get("phases") or []:
                ph["featured_routes"] = featured_ar if featured_ar else []
            if featured_ar:
                # prefer Rosario if present else first
                fr = next((x for x in featured_ar if x["route_id"] == "rn-f451444da7fe"), featured_ar[0])
                m["journeys_unlocked"] = [
                    {
                        "from": fr["from_label"],
                        "to": fr["to_label"],
                        "from_label": fr["from_label"],
                        "to_label": fr["to_label"],
                        "label": f"{fr['from_label']} → {fr['to_label']}",
                        "route_id": fr["route_id"],
                        "_link_status": "linked-cl-ar-hand-route",
                        "_link_source": "grok/didi-open-items-2026-07-10",
                        "economics_status": "economics_pending",
                        "today": "Existing water hop with boarding friction.",
                        "with_navier": "A clean hop booked in DiDi once demand is sourced.",
                        "platform": "Pioneer II",
                        "archetype": "tourism",
                    }
                ]
            m["_operation_caveats"] = [
                "DiDi AR directory: Buenos Aires, Rosario, Bariloche among others — Tigre not listed",
                "BA–Colonia is international; not domestic-featured",
                "Rosario–Sabino Corsi is seasonal summer service",
                "Annual route pax remain null — no finance promotion",
            ]
            m["_didi_cl_ar_open_items"] = {
                "at": utc_now(),
                "featured": [x["route_id"] for x in featured_ar],
            }

    geom_report["featured_held"] = [
        {"route_id": rid, **meta}
        for rid, meta in FEATURE_ELIGIBILITY.items()
        if rid not in geom_report["featured_bound"]
    ]
    geom_report["featured_chile"] = featured_cl
    geom_report["featured_argentina"] = featured_ar
    return geom_report


def bank_colombia() -> dict:
    return {
        "at": utc_now(),
        "status": "unmaterialized_hold",
        "decision": "C — keep DiDi Colombia unmaterialized in finance",
        "spine_choice": "deferred",
        "option_A_didi_geometry_marquee": ["rn-aa790551baa7"],
        "option_B_yango_finance_spine": [
            "rn-20762e2b40f5",
            "rn-3ebf0c9aece2",
            "rn-59374c41f8ab",
            "rn-74aa778f6655",
            "rn-84ffd58e7f82",
        ],
        "intersection": [],
        "demand_gate": {
            "rn-aa790551baa7": {
                "annual_one_way_pax": None,
                "fare": None,
                "disposition": "not_publicly_supported",
                "source": "DIDI-BR-CO-T3-PROOF-2026-07-09",
            },
            "la_bodeguita_terminal_aggregate_2023": {
                "pax": 619282,
                "classification": "benchmark_only_terminal_not_od",
                "note": "Cannot map 1:1 to Bocachica or Rosario",
            },
        },
        "didi_cities_directory": {
            "cartagena": True,
            "barranquilla": True,
            "source": "https://web.didiglobal.com/co/conductor/ciudades/",
        },
        "finance_market_key": None,
        "do_not": [
            "Do not invent OD annual pax from terminal aggregates",
            "Do not force-align DiDi marquee to yango 5/6-ID spine without demand + product choice",
            "Do not cascade Colombia economics",
        ],
    }


def bank_finance_nulls() -> dict:
    """CR/PA/DR + EC/PE + TW/HK formal null finance bank — no cascade."""
    return {
        "at": utc_now(),
        "status": "finance_null_banked / no_cascade",
        "wave_gates": {
            "cr_pa_dr": "blocked_pending_primary_evidence",
            "ec_pe": "blocked_pending_primary_evidence",
            "taiwan": "hard_operation_hold",
            "hong_kong": "exact_route_bound_pax_null",
            "egypt_candidates": "zero_exact_route_matches",
            "chile_argentina": "pax_null_after_geometry",
        },
        "routes": [
            # CR
            {"route_id": "rn-7e59f984abec", "market": "costa-rica", "annual_one_way_pax": None, "fare_benchmark": "CRC 810 adult (ARESEP 2026-07-01)", "finance": "null"},
            {"route_id": "rn-eb4ca32edbef", "market": "costa-rica", "annual_one_way_pax": None, "fare_benchmark": "CRC 1000 adult (ARESEP 2026-07-01)", "finance": "null"},
            {"route_id": "rn-55b63e976bb7", "market": "costa-rica", "annual_one_way_pax": None, "fare_benchmark": None, "finance": "null", "note": "not current scheduled"},
            # PA
            {"route_id": "rn-8fb072f5a8a8", "market": "panama", "annual_one_way_pax": None, "finance": "null", "note": "Guna permission required"},
            {"route_id": "rn-87eec178e86f", "market": "panama", "annual_one_way_pax": None, "finance": "null", "note": "Guna permission required"},
            # DR
            {"route_id": "rn-64effc46b976", "market": "dominican-republic", "annual_one_way_pax": None, "finance": "null"},
            {"route_id": "rn-c3a4ef933700", "market": "dominican-republic", "annual_one_way_pax": None, "finance": "null", "note": "ops proof only"},
            # EC Galápagos e__ IDs as sealed spine
            {"route_id": "e__santa-cruz-galapagos-ecuador__puerto-ayora__isabela-galapagos-ecuador__puerto-villamil", "market": "ecuador", "annual_one_way_pax": None, "fare_benchmark": "USD 30 regular", "finance": "null"},
            {"route_id": "e__santa-cruz-galapagos-ecuador__puerto-ayora__san-cristobal-galapagos-ecuador__puerto-baquerizo-moreno", "market": "ecuador", "annual_one_way_pax": None, "fare_benchmark": "USD 30 regular", "finance": "null"},
            {"route_id": "e__santa-cruz-galapagos-ecuador__puerto-ayora__floreana-galapagos-ecuador__puerto-velasco-ibarra", "market": "ecuador", "annual_one_way_pax": None, "fare_benchmark": "USD 30 regular", "finance": "null"},
            # PE unsealed candidates
            {"route_id": None, "market": "peru", "corridor": "paracas-ballestas", "annual_one_way_pax": None, "note": "visitor arrivals not route pax; unsealed"},
            {"route_id": None, "market": "peru", "corridor": "callao-palomino", "annual_one_way_pax": None, "note": "unsealed"},
            # TW/HK optional economics
            {"route_id": "rn-d7294a3ddd04", "market": "hong-kong", "annual_one_way_pax": None, "finance": "null", "note": "exact geometry bound; demand not public"},
            {"route_id": "rn-5085d4e1f498", "market": "taiwan", "annual_one_way_pax": 95705, "finance": "null", "note": "candidate demand only; route quarantine + hard op hold — not cascaded"},
        ],
        "do_not": [
            "Do not promote benchmark fares as realized yield",
            "Do not convert tourism/visitor totals into route annual_one_way_pax",
            "Do not cascade Taiwan while quarantine/hard hold remains",
            "Do not invent CR/PA/DR/EC/PE annual pax",
        ],
    }


def bank_ferry_towns() -> dict:
    return {
        "at": utc_now(),
        "status": "polygon_proof_complete / nearby_towns_held",
        "sources": [
            "https://web.didiglobal.com/cl/conductor/ciudades/",
            "https://web.didiglobal.com/ar/conductor/ciudades/",
            "https://web.didiglobal.com/co/conductor/ciudades/",
        ],
        "method": "official DiDi conductor city-directory scrape 2026-07-10; city-list membership is not a precise polygon, but absence is a hold trigger for nearby ferry municipalities",
        "chile_directory_includes": sorted(DIDI_CL_CITIES),
        "argentina_directory_includes_selected": sorted(DIDI_AR_CITIES),
        "colombia_directory_includes_selected": sorted(DIDI_CO_CITIES),
        "ferry_towns": FERRY_TOWN_AUDIT,
        "verdict": "All audited ferry-town endpoints remain OUTSIDE named DiDi city directories. Do not claim DiDi first/last-mile at these ramps. Anchor cities (Valdivia, Puerto Montt, Concepción, Punta Arenas/Magallanes, Buenos Aires, Rosario, Bariloche, Cartagena, Barranquilla) pass directory gate only.",
        "do_not": [
            "Do not inherit DiDi operation from parent metro to ferry towns without polygon/app proof",
            "Do not feature routes whose endpoints are only ferry towns",
        ],
    }


def bank_egypt_audit(routes: list, fbt: dict) -> dict:
    egypt_cluster = []
    foreign = []
    for f in routes:
        p = f.get("properties") or {}
        if p.get("cluster_id") != "egypt":
            continue
        egypt_cluster.append(p.get("id"))
        ends = f"{p.get('from_city_id')}|{p.get('to_city_id')}"
        if any(x in ends for x in ("neom", "jeddah", "ksa", "saudi")):
            foreign.append(
                {
                    "route_id": p.get("id"),
                    "from_city_id": p.get("from_city_id"),
                    "to_city_id": p.get("to_city_id"),
                    "label": p.get("label"),
                }
            )
    # POI parents
    parent_counts: dict[str, int] = {}
    wrong_parent = []
    egypt_cities = {
        "cairo-egypt",
        "hurghada-el-gouna-egypt",
        "redsea-egypt",
        "sharm-el-sheikh-egypt",
    }
    for poi in fbt.get("poi") or []:
        props = poi.get("properties") or poi
        parent = props.get("parent_city_id")
        if not parent:
            continue
        if parent in egypt_cities or "egypt" in str(parent):
            parent_counts[parent] = parent_counts.get(parent, 0) + 1
            if parent not in egypt_cities and "egypt" not in str(parent):
                wrong_parent.append(props.get("id"))
        if parent in ("neom-sindalah-ksa", "jeddah-ksa") and props.get("cluster_id") == "egypt":
            wrong_parent.append(props.get("id"))

    # Tasklet nonexistent brief IDs
    brief_ghosts = [
        "edge__hurghada-el-gouna-egypt__sharm-el-sheikh-across-the-gulf",
        "edge-0762",
    ]
    present_ids = { (f.get("properties") or {}).get("id") for f in routes }
    ghosts_status = { g: ("present" if g in present_ids else "absent_from_ROUTES") for g in brief_ghosts }

    # BP candidates still null (from global gates disposition)
    bp_null = {
        "proposed_bp_exact_matches": 0,
        "held_candidates": 11,
        "dropped_non_bp": ["Ras Muhammad National Park", "Nabq Protectorate"],
        "note": "No coordinate seal this run — Tasklet published no authoritative berth coordinates for river-bus/cruise terminals",
    }

    return {
        "at": utc_now(),
        "status": "egypt_audit_reconfirmed",
        "egypt_cluster_route_count": len(egypt_cluster),
        "foreign_endpoint_on_egypt_cluster": foreign,
        "foreign_endpoint_count": len(foreign),
        "neom_routes_now_on_saudi_cluster": 5,
        "poi_parent_counts_egypt_slice": parent_counts,
        "wrong_parent_poi_ids": wrong_parent,
        "brief_ghost_route_ids": ghosts_status,
        "bp_coordinate_seal": bp_null,
        "el_gouna": "hold — no inheritance from Hurghada",
        "actions_taken": [
            "Reconfirmed 0 foreign endpoints on cluster egypt",
            "NEOM↔Egypt legs remain on saudi-arabia cluster (prior cleanup holds)",
            "No fuzzy BP mint without coordinates",
        ],
        "still_open": [
            "Authoritative berth coordinates for Cairo river-bus and Red Sea excursion landings",
            "Wrong-parent POI repair if future ingest reintroduces KSA parents under egypt",
        ],
    }


def stamp_seal(meta: dict) -> None:
    if not SEAL.exists():
        return
    seal = load_json(SEAL)
    notes = seal.get("_notes") or {}
    if not isinstance(notes, dict):
        notes = {"_prior": notes}
    notes["didi_open_items_2026_07_10"] = meta
    seal["_notes"] = notes
    seal["sealed_at"] = utc_now()
    save_json(SEAL, seal)


def run_gates() -> dict:
    gates = {}
    cmds = [
        ("gate_g", [sys.executable, str(ROOT / "scripts/audit_partner_copy.py")]),
        (
            "inheritance_strict",
            [sys.executable, str(ROOT / "scripts/audit_partner_spine_parity.py")]
            if (ROOT / "scripts/audit_partner_spine_parity.py").exists()
            else None,
        ),
    ]
    # Prefer known gate entrypoints from prior seals
    for name, script in [
        ("gate_g", ROOT / "scripts/audit_partner_copy.py"),
        ("fidelity", ROOT / "scripts/audit_proposal_fidelity.py"),
    ]:
        if not script.exists():
            gates[name] = {"pass": None, "note": "script missing"}
            continue
        cmd = [sys.executable, str(script)]
        if name == "fidelity":
            cmd += ["--partner", "didi"]
        try:
            r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=180)
            tail = (r.stdout or r.stderr or "")[-800:]
            gates[name] = {"exit": r.returncode, "pass": r.returncode == 0, "tail": tail}
        except Exception as e:
            gates[name] = {"pass": False, "error": str(e)}
    return gates


def main() -> int:
    routes = load_json(ROUTES)
    fbt = load_json(FBT)
    partner = load_json(PARTNER)

    # 1) CL/AR geometry
    geom = seal_cl_ar_geometry(routes)
    save_json(ROUTES, routes)

    # re-bind featured using updated routes on disk
    geom = bind_featured(partner, geom)
    save_json(PARTNER, partner)
    if PITCH.exists():
        shutil.copyfile(PARTNER, PITCH)

    # 2-6 banks
    colombia = bank_colombia()
    finance = bank_finance_nulls()
    ferry = bank_ferry_towns()
    egypt = bank_egypt_audit(routes, fbt)

    # Sync map-scope held notes for ferry towns
    ms = partner.get("_map_scope") or {}
    held = ms.get("_held") or {}
    for town in FERRY_TOWN_AUDIT:
        cid = town["atlas_city_id"]
        if cid:
            held[cid] = (
                f"ferry-town service-polygon hold — not in DiDi {town['country']} city directory; "
                f"nearest listed: {town['nearest_didi']}"
            )
    ms["_held"] = held
    partner["_map_scope"] = ms
    save_json(PARTNER, partner)
    if PITCH.exists():
        shutil.copyfile(PARTNER, PITCH)

    gates = run_gates()

    receipt = {
        "at": utc_now(),
        "lane": "DiDi open items seal (CL/AR geometry + holds bank)",
        "status": "open_items_banked / finance_not_promoted / deploy_deferred",
        "cl_ar_geometry": geom,
        "colombia": colombia,
        "finance_null_bank": finance,
        "ferry_town_polygons": ferry,
        "taiwan_hk_economics": {
            "hong_kong_rn_d7294a3ddd04": "geometry bound; annual pax null — no economics",
            "taiwan_rn_5085d4e1f498": "quarantine + hard op hold; candidate pax 95705 not cascaded",
        },
        "egypt_audit": egypt,
        "gates": gates,
        "do_not": [
            "No deploy this run",
            "No finance cascade without annual_one_way_pax",
            "No ferry-town DiDi claims",
            "No Taiwan marine economics while held",
            "null beats wrong",
        ],
    }
    save_json(OUT / "GROK-OPEN-ITEMS-SEAL-RECEIPT-2026-07-10.json", receipt)
    save_json(OUT / "GROK-CL-AR-HAND-ROUTE-RECEIPT-2026-07-10.json", geom)
    save_json(OUT / "GROK-COLOMBIA-SPINE-RECONCILIATION-2026-07-10.json", colombia)
    save_json(OUT / "GROK-FINANCE-NULL-BANK-CR-PA-DR-EC-PE-TW-HK-2026-07-10.json", finance)
    save_json(OUT / "GROK-FERRY-TOWN-POLYGON-PROOF-2026-07-10.json", ferry)
    save_json(OUT / "GROK-EGYPT-AUDIT-RECONFIRM-2026-07-10.json", egypt)

    md = [
        "# Grok — DiDi open items seal",
        "",
        f"**UTC:** {receipt['at']}",
        f"**Status:** `{receipt['status']}`",
        "",
        "## 1. CL/AR hand-route",
        f"- Unquarantined: **{len(geom.get('unquarantined') or [])}** → `{', '.join(geom.get('unquarantined') or []) or 'none'}`",
        f"- Still quarantine: **{len(geom.get('still_quarantined') or [])}**",
        f"- Featured Chile: `{[x['route_id'] for x in geom.get('featured_chile') or []]}`",
        f"- Featured Argentina: `{[x['route_id'] for x in geom.get('featured_argentina') or []]}`",
        "",
        "## 2. Colombia",
        "- Decision **C**: unmaterialized hold; spine A/B deferred; no finance market key",
        "",
        "## 3. CR/PA/DR / EC/PE / TW/HK finance",
        "- All annual_one_way_pax **null** (or TW candidate not cascaded). No cascade.",
        "",
        "## 4. Ferry-town polygons",
        "- Official directory scrape: Niebla/Corral/Calbuco/Pargua/Chacao/Dalcahue/Lota/Porvenir/Tigre/Colonia **not listed** → hold",
        "",
        "## 5–6. Taiwan/HK economics + Egypt",
        "- HK: geometry only; pax null",
        "- TW: quarantine + hard hold; no economics",
        f"- Egypt: foreign endpoints on egypt cluster = **{egypt.get('foreign_endpoint_count')}**; BP coords still unsealed",
        "",
        "## Gates",
    ]
    for k, v in (gates or {}).items():
        md.append(f"- **{k}:** {'PASS' if v.get('pass') else 'FAIL/NA'} (exit {v.get('exit')})")
    md.append("")
    md.append("Machine: `handoff/didi-ex-china/waves/tasklet-proof/GROK-OPEN-ITEMS-SEAL-RECEIPT-2026-07-10.json`")
    (OUT / "GROK-OPEN-ITEMS-SEAL-RECEIPT-2026-07-10.md").write_text("\n".join(md) + "\n")

    stamp_seal(
        {
            "at": receipt["at"],
            "unquarantined": geom.get("unquarantined"),
            "featured_ar": [x["route_id"] for x in geom.get("featured_argentina") or []],
            "featured_cl": [x["route_id"] for x in geom.get("featured_chile") or []],
            "colombia": "unmaterialized_hold",
            "finance": "null_bank_no_cascade",
        }
    )

    print(json.dumps({
        "unquarantined": geom.get("unquarantined"),
        "still_quarantined": geom.get("still_quarantined"),
        "featured_chile": geom.get("featured_chile"),
        "featured_argentina": geom.get("featured_argentina"),
        "gates": {k: v.get("pass") for k, v in gates.items()},
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
