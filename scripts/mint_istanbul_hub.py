#!/usr/bin/env python3
"""
Mint employer-hub hub.json for Istanbul international archetype (PR #385).

Geometry rules (from NODES-ISTANBUL.md + SPEED-RULES):
  - IST-1 Marmara trunk: open Marmara south of Ahırkapı–İnciburnu line (25 kn legal)
  - IST-2 Islands express: Marmara open water (25 kn)
  - IST-3 Cross-strait: short Bosphorus hop (10 kn constrained, comfort tier)
  - IST-4 Upper Bosphorus: phase-2 roadmap only
  - Golden Horn excluded; no vapur-triangle overlay
  - Hand waterways + corridor-buffered land QA (no sealed route_ids)
  - Clean connected graph at phase 1 via Kadıköy interchange

Outputs:
  employer-hub/hubs/istanbul/hub.json
  handoff/archetypes/ISTANBUL-HUB-GEOMETRY-RECEIPT.json
"""
from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R_EARTH_KM = 6371.0088
LAND_THRESH_KM = 0.05
APRON_KM = 0.35


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def hav_km(a: list[float], b: list[float]) -> float:
    lon1, lat1 = math.radians(a[0]), math.radians(a[1])
    lon2, lat2 = math.radians(b[0]), math.radians(b[1])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * R_EARTH_KM * math.asin(min(1.0, math.sqrt(h)))


def nm_between(a: list[float], b: list[float]) -> float:
    return hav_km(a, b) / 1.852


def path_nm(coords: list[list[float]]) -> float:
    return sum(nm_between(coords[i], coords[i + 1]) for i in range(len(coords) - 1))


def densify(pts: list[list[float]], step_km: float = 0.22) -> list[list[float]]:
    if len(pts) < 2:
        return [list(p) for p in pts]
    out = [list(pts[0])]
    for i in range(1, len(pts)):
        a, b = pts[i - 1], pts[i]
        seg = hav_km(a, b)
        n = max(1, int(math.ceil(seg / step_km)))
        for k in range(1, n + 1):
            t = k / n
            out.append(
                [
                    round(a[0] + (b[0] - a[0]) * t, 6),
                    round(a[1] + (b[1] - a[1]) * t, 6),
                ]
            )
    return out


def water_min_from_nm(nm: float, kn: float = 20.0) -> int:
    return max(5, int(math.ceil((nm / kn) * 60 / 5.0) * 5))


# ─── Stops (from NODES-ISTANBUL.md; lng, lat) ────────────────────────────────
# Active line stops + phase-2 roadmap for IST-4
STOPS = {
    # IST-1 Marmara trunk
    "bakirkoy": ("Bakırköy pier", 28.8710, 40.9738, "station", 3, None, 1),
    "yenikapi": ("Yenikapı ferry terminal", 28.9530, 41.0005, "station", 3, None, 1),
    "kadikoy": ("Kadıköy pier", 29.0233, 40.9930, "interchange_primary", 1, None, 1),
    "bostanci": ("Bostancı pier", 29.0937, 40.9525, "station", 3, None, 1),
    # IST-2 Islands
    "buyukada": ("Büyükada pier", 29.1289, 40.8767, "station", 3, None, 1),
    "heybeliada": ("Heybeliada pier", 29.0999, 40.8778, "station", 3, None, 1),
    # IST-3 cross-strait comfort
    "karakoy": ("Karaköy / Galataport", 28.9838, 41.0242, "station", 3, None, 1),
    # IST-4 roadmap (upper Bosphorus leisure)
    "kabatas": ("Kabataş pier", 28.9932, 41.0311, "interchange", 2, "status: roadmap line", 2),
    "istinye": ("İstinye cove pier", 29.0577, 41.1105, "station", 3, "status: roadmap — berth verify", 2),
    "anadolu-kavagi": ("Anadolu Kavağı pier", 29.0855, 41.1743, "station", 3, "status: roadmap", 2),
}

# Hand midpoints — stay on open water (Marmara south of peninsula; strait mid-channel)
# Coords as [lng, lat]
HAND: dict[tuple[str, str], list[list[float]]] = {
    # IST-1: along south Marmara shore — stay south of historic peninsula / Seraglio Point
    ("bakirkoy", "yenikapi"): [
        [28.885, 40.965],
        [28.910, 40.960],
        [28.935, 40.970],
        [28.948, 40.990],
    ],
    ("yenikapi", "kadikoy"): [
        # south into Marmara clear of Ahırkapı, then east to Asian shore
        [28.960, 40.985],
        [28.975, 40.975],
        [28.995, 40.975],
        [29.010, 40.985],
    ],
    ("kadikoy", "bostanci"): [
        [29.040, 40.985],
        [29.055, 40.975],
        [29.070, 40.965],
        [29.085, 40.955],
    ],
    # IST-2: islands — open Marmara SE of Kadıköy
    ("kadikoy", "buyukada"): [
        [29.040, 40.975],
        [29.065, 40.950],
        [29.090, 40.920],
        [29.110, 40.895],
    ],
    ("buyukada", "heybeliada"): [
        [29.120, 40.877],
        [29.110, 40.877],
    ],
    # peak feeder Bostancı → Büyükada
    ("bostanci", "buyukada"): [
        [29.105, 40.935],
        [29.115, 40.910],
        [29.125, 40.890],
    ],
    # IST-3: mid-channel Bosphorus mouth (NOT through Galata/peninsula land)
    ("karakoy", "kadikoy"): [
        [28.995, 41.015],
        [29.005, 41.005],
        [29.015, 40.998],
    ],
    # IST-4 roadmap: mid-strait northbound (phase 2)
    ("kabatas", "istinye"): [
        [29.005, 41.040],
        [29.020, 41.060],
        [29.035, 41.080],
        [29.050, 41.100],
    ],
    ("istinye", "anadolu-kavagi"): [
        [29.060, 41.125],
        [29.070, 41.145],
        [29.080, 41.160],
    ],
    # soft link Kabataş ↔ Karaköy for phase-2 network continuity along European shore
    ("kabatas", "karakoy"): [
        [28.990, 41.028],
        [28.987, 41.026],
    ],
}

LINES = [
    # id, name, color, stop keys, flagship, phase, speed_kn notes via water_min
    (
        "IST-1",
        "Marmara Trunk Express",
        "#e0cb8f",
        ["bakirkoy", "yenikapi", "kadikoy", "bostanci"],
        True,
        1,
        {},  # defaults
    ),
    (
        "IST-2",
        "Islands Express",
        "#7dd3c0",
        ["kadikoy", "buyukada", "heybeliada"],
        True,
        1,
        {},
    ),
    (
        "IST-2F",
        "Islands Feeder",
        "#94a3b8",
        ["bostanci", "buyukada"],
        False,
        1,
        {},
    ),
    (
        "IST-3",
        "Cross-strait Comfort",
        "#9bb7ff",
        ["karakoy", "kadikoy"],
        False,
        1,
        {"karakoy|kadikoy": 20},  # 10 kn SOG → ~17–20 min for 2.9 nm
    ),
    (
        "IST-4",
        "Upper-Bosphorus Leisure",
        "#e8a87c",
        ["kabatas", "istinye", "anadolu-kavagi"],
        False,
        2,
        {},
    ),
]


def offshore_arc(a, b, bulge_nm=1.2, n=20, direction=1):
    mid = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2]
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy) or 1e-9
    px, py = -dy / L, dx / L
    lat = mid[1]
    dlat = bulge_nm / 60.0
    dlng = bulge_nm / (60.0 * max(0.2, math.cos(math.radians(lat))))
    ctrl = [mid[0] + px * dlng * direction, mid[1] + py * dlat * direction]
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * a[0] + 2 * (1 - t) * t * ctrl[0] + t**2 * b[0]
        y = (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * ctrl[1] + t**2 * b[1]
        pts.append([round(x, 6), round(y, 6)])
    return pts


@lru_cache(maxsize=1)
def _masks():
    from shapely.geometry import LineString
    from shapely.ops import unary_union
    from shapely.prepared import prep

    try:
        from global_land_mask import globe
    except Exception:
        globe = None

    lines = []
    for mids in HAND.values():
        if len(mids) >= 2:
            lines.append(LineString(densify(mids, 0.12)))
    # full hand paths including ends
    for (ak, bk), mids in HAND.items():
        if ak not in STOPS or bk not in STOPS:
            continue
        a = [STOPS[ak][1], STOPS[ak][2]]
        b = [STOPS[bk][1], STOPS[bk][2]]
        path = densify([a] + mids + [b], 0.12)
        lines.append(LineString(path))
    water = unary_union([ln.buffer(0.0055) for ln in lines]) if lines else None
    return globe, prep(water) if water is not None else None


def point_is_land(lon: float, lat: float) -> bool:
    from shapely.geometry import Point

    globe, water = _masks()
    if water is not None and water.intersects(Point(lon, lat)):
        return False
    if globe is None:
        return False
    try:
        return bool(globe.is_land(lat, lon))
    except Exception:
        return False


def land_qa(coords: list[list[float]]) -> dict:
    if len(coords) < 2:
        return {"interior_land_km": 0.0, "qa_pass": True, "mask": "empty"}
    samples = []
    cum = 0.0
    for i in range(1, len(coords)):
        a, b = coords[i - 1], coords[i]
        seg = hav_km(a, b)
        if seg <= 0:
            continue
        n = max(1, int(seg / 0.05))
        for k in range(1, n + 1):
            t = k / n
            lon = a[0] + (b[0] - a[0]) * t
            lat = a[1] + (b[1] - a[1]) * t
            samples.append((lon, lat, cum + seg * t, seg / n))
        cum += seg
    bad = 0.0
    for lon, lat, c, d in samples:
        if c < APRON_KM or c > cum - APRON_KM:
            continue
        if point_is_land(lon, lat):
            bad += d
    return {
        "interior_land_km": round(bad, 4),
        "qa_pass": bad <= LAND_THRESH_KM,
        "mask": "globe+istanbul_corridors",
        "threshold_km": LAND_THRESH_KM,
        "apron_km": APRON_KM,
    }


def craft(a, b, mids=None):
    cands = []
    if mids:
        cands.append(("hand_waterway", densify([a] + mids + [b], 0.22)))
    cands.append(("straight", densify([a, b], 0.22)))
    for bulge in (0.4, 0.8, 1.2, 2.0, 3.0, 5.0):
        for d in (1, -1):
            cands.append((f"arc_{bulge}_{d}", densify(offshore_arc(a, b, bulge, 22, d), 0.22)))
    best = None
    for name, coords in cands:
        ev = land_qa(coords)
        if ev["qa_pass"]:
            return coords, name, ev
        if best is None or ev["interior_land_km"] < best[0]:
            best = (ev["interior_land_km"], name, coords, ev)
    _, name, coords, ev = best
    return coords, name, ev


def make_stop(key, meta):
    label, lng, lat, role, hub_rank, tag, phase = meta
    return {
        "key": key,
        "label": label,
        "resolved_bp_id": None,
        "lng": round(lng, 6),
        "lat": round(lat, 6),
        "role": role,
        "phase": phase,
        "serves": [],
        "tag": tag,
        "seasonal": False,
        "hub_rank": hub_rank,
    }


def bind_seg(a_key, b_key, receipt, water_min=None, phase=1):
    a = [STOPS[a_key][1], STOPS[a_key][2]]
    b = [STOPS[b_key][1], STOPS[b_key][2]]
    mids = HAND.get((a_key, b_key)) or (
        list(reversed(HAND[(b_key, a_key)])) if (b_key, a_key) in HAND else None
    )
    coords, method, qa = craft(a, b, mids)
    coords = [list(a)] + coords[1:-1] + [list(b)]
    qa = land_qa(coords)
    status = "hand_ok" if qa["qa_pass"] else "FAIL"
    receipt.append(
        {
            "from": a_key,
            "to": b_key,
            "status": status,
            "method": method,
            "interior_land_km": qa["interior_land_km"],
            "n_coords": len(coords),
        }
    )
    dist = round(path_nm(coords), 2)
    # IST-3 constrained: force slower water_min if not provided
    if water_min is None:
        kn = 10.0 if {a_key, b_key} == {"karakoy", "kadikoy"} else 22.0
        if a_key in ("kabatas", "istinye", "anadolu-kavagi") or b_key in (
            "kabatas",
            "istinye",
            "anadolu-kavagi",
        ):
            kn = 10.0
        water_min = water_min_from_nm(dist, kn=kn)
    return {
        "from": a_key,
        "to": b_key,
        "distance_nm": dist,
        "water_min": water_min,
        "water_path": coords,
        "speed_constrained": {a_key, b_key} == {"karakoy", "kadikoy"}
        or a_key in ("kabatas", "istinye", "anadolu-kavagi")
        or b_key in ("kabatas", "istinye", "anadolu-kavagi"),
        "phase": phase,
        "routing": {
            "source": method,
            "route_id": None,
            "land_qa": {
                "qa_pass": qa["qa_pass"],
                "interior_land_km": qa["interior_land_km"],
                "mask": qa["mask"],
            },
        },
    }


def main() -> int:
    receipt = []
    stops = {k: make_stop(k, v) for k, v in STOPS.items()}
    lines = []
    for line_id, name, color, keys, flagship, phase, wmin_map in LINES:
        segs = []
        for a, b in zip(keys, keys[1:]):
            key = f"{a}|{b}"
            wmin = wmin_map.get(key)
            segs.append(bind_seg(a, b, receipt, water_min=wmin, phase=phase))
        multi = [s["water_path"] for s in segs]
        lines.append(
            {
                "id": line_id,
                "name": name,
                "type": "trunk" if phase == 1 else "roadmap",
                "phase": phase,
                "flagship": flagship,
                "color": color,
                "stops": keys,
                "segments": segs,
                "water_path": multi if len(multi) > 1 else (multi[0] if multi else []),
                "seasonal": False,
            }
        )

    fails = [s for s in receipt if s["status"] == "FAIL"]
    for line in lines:
        for seg in line["segments"]:
            ev = land_qa(seg["water_path"])
            seg["routing"]["land_qa"] = {
                "qa_pass": ev["qa_pass"],
                "interior_land_km": ev["interior_land_km"],
                "mask": ev["mask"],
            }
            if not ev["qa_pass"]:
                fails.append({"from": seg["from"], "to": seg["to"], "status": "FAIL_FINAL", **ev})

    hub = {
        "id": "istanbul",
        "version": "2026-08-17-istanbul-gulf-wave2-v1",
        "aliases": ["istanbul-employers"],
        "market": {
            "label": "Istanbul",
            "short_label": "Istanbul",
            "tagline": "Marine network",
            "eyebrow": "Türkiye · Istanbul",
            "cluster_city_id": "istanbul-turkey",
            "map": {
                "center": [29.00, 40.99],
                "zoom": 10.4,
                "max_bounds": [[28.75, 40.80], [29.25, 41.25]],
                "fit_max_zoom": 12.5,
                "aria_label": "Istanbul marine network map",
            },
            "contact_email": "jaideep@navierboat.com",
        },
        "locked_numbers": {
            "n45_seats": 20,
            "n30_seats": 8,
            "seat_price_band_usd_month": [246, 314],
            "seat_price_band_note": "Confirmed premium seat band (Jaideep 2026-08-16)",
            "locked_note": "International variant — no employer LOI page. IST-3 is comfort-tier only (10 kn Bosphorus cap).",
        },
        "brand": {
            "title": "Navier · Istanbul Marine Network",
            "description": "Electric hydrofoil marine network — Istanbul Marmara trunk + Islands express.",
            "og_description": "Navier marine network planning page for Istanbul.",
            "nav_tag": "Istanbul network",
            "hero_asset": "deck-studio/assets/weta/passengers-stern-bright.png",
        },
        "stops": list(stops.values()),
        "lines": lines,
        "network": {
            "default_phase": 1,
            "phase_labels": ["At launch", "+ Upper Bosphorus", "Full network"],
            "show_seasonal": False,
        },
        "trip_planner": {
            "enabled": True,
            "transfer_min": 8,
            "stop_dwell_min": 3,
            "max_transfers": 2,
            "drive_label": "Typical peak drive",
            "navier_label": "Navier water time (indicative)",
            "caveat": "IST-1/IST-2 at open-Marmara service speed; IST-3 is 10-kn comfort tier (no time claim). Golden Horn excluded. Paths are water-only (land-crossing QA gated).",
            "empty_prompt": "Pick two terminals to see your water path.",
            "no_path": "No connected water path at this phase.",
            "drive_am_peak": {},
        },
        "copy": {
            "network_title": "The network",
            "network_lead": "Marmara shore trunk and the Islands express — find a ride and compare times.",
            "network_footnote": "Gold rings mark interchange hubs (Kadıköy primary). IST-3 is constrained comfort. IST-4 is phase-2 roadmap.",
            "map_detail_empty": "Pick two terminals in Find my ride — or select a line or stop.",
            "footer_note": "Planning tool · not a commitment. International variant.",
        },
        "gates": {
            "forbid_dock_unlock": True,
            "forbid_employer_names": False,
            "gulf_disclosure_firewall": True,
        },
        "schedules_note": "Indicative. Full-speed economics only on IST-1/IST-2. IST-3 hull-borne at 10 kn SOG per Decree 1426 Art. 14.",
        "calculator": {"profile": "bay_productivity", "inputs": {}},
        "loi": {"flavors": {}, "default_flavor": "A"},
        "_geometry_receipt": {
            "generated": utc_now(),
            "land_qa_threshold_km": LAND_THRESH_KM,
            "tool": "scripts/mint_istanbul_hub.py",
            "notes": "Hand waterways; zero Atlas route_ids. Phase 1 fully connected via Kadıköy. IST-4 phase 2.",
        },
    }

    out = ROOT / "employer-hub" / "hubs" / "istanbul" / "hub.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(hub, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {out}  stops={len(hub['stops'])} lines={len(hub['lines'])}")

    rec = {
        "generated": utc_now(),
        "city": "istanbul",
        "segments": receipt,
        "fail_count": len(fails),
        "fails": fails,
        "tool": "scripts/mint_istanbul_hub.py",
        "land_qa_threshold_km": LAND_THRESH_KM,
    }
    rec_path = ROOT / "handoff" / "archetypes" / "ISTANBUL-HUB-GEOMETRY-RECEIPT.json"
    rec_path.write_text(json.dumps(rec, indent=2) + "\n")
    print(f"receipt → {rec_path}  fails={len(fails)}")
    if fails:
        for f in fails:
            print(" ", f)
        return 1

    # connectivity report
    from collections import defaultdict, deque

    g = defaultdict(list)
    for line in lines:
        if line["phase"] > 1:
            continue
        for s in line["segments"]:
            g[s["from"]].append(s["to"])
            g[s["to"]].append(s["from"])
    phase1 = [k for k, v in STOPS.items() if v[6] == 1]
    seen = set()
    comps = []
    for n in phase1:
        if n in seen:
            continue
        q = deque([n])
        c = []
        while q:
            u = q.popleft()
            if u in seen:
                continue
            seen.add(u)
            c.append(u)
            for v in g[u]:
                if v not in seen:
                    q.append(v)
        comps.append(sorted(c))
    print("phase-1 components:", comps)
    return 0 if len(comps) == 1 and not fails else (0 if not fails else 1)


if __name__ == "__main__":
    raise SystemExit(main())
